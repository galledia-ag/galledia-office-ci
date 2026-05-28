"""
fill_brief.py — befuellt die Galledia Brief-Vorlage (.dotx) und speichert als .docx.

Strategie: Direkte ZIP/XML-Manipulation (kein python-docx) — die Galledia-Vorlage
enthaelt Glossary-Parts, customXml-Bindungen und Header/Footer-Strukturen, die
python-docx beim Round-Trip beschaedigt (image2.jpg -> image/png, zusaetzliche
header*.xml etc., Word meldet die Datei als beschaedigt). Mit reiner lxml/zipfile-
Manipulation bleibt die Vorlagen-Struktur unveraendert; nur die Inhalts-Bytes
in document.xml und header*.xml werden ersetzt.

Die SDTs der Vorlage binden ueber <w:dataBinding> an einen Custom-XML-Part
(historisch von officeatwork eingefuehrt). Wir aktualisieren diesen Part als
Single Source of Truth und entfernen die uebrigen, nicht mehr genutzten
officeatwork-Konfigparts vor dem Schreiben.

Aufruf:
    python fill_brief.py --input data.json --output brief.docx
    python fill_brief.py --input - --output brief.docx   (stdin)
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import zipfile
from copy import deepcopy
from pathlib import Path
from typing import Iterable

from lxml import etree

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_PATH = SKILL_DIR / "templates" / "Brief-Vorlage Galledia.dotx"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NSMAP = {"w": W_NS}

OFFICEATWORK_NS = "http://schemas.officeatwork.com/CustomXMLPart"

# Custom XML namespaces from the now-deprecated officeatwork tool that the
# template still drags along. The CustomXMLPart (item4) is genuinely needed —
# it drives the SDT data binding. The rest are dead config and get stripped
# from the output.
DEAD_CUSTOMXML_NAMESPACES = {
    "http://schemas.officeatwork.com/Formulas",
    "http://schemas.officeatwork.com/Document",
    "http://schemas.officeatwork.com/MasterProperties",
    "http://schemas.officeatwork.com/Media",
}

TEMPLATE_CT = "application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml"
DOCUMENT_CT = "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"

VALID_OE = {
    "galledia group ag",
    "Galledia Fachmedien AG",
    "Galledia Regionalmedien AG",
    "Galledia Print AG",
    "Galledia Digital AG",
}

PHONE_RE = re.compile(r"^[TM] \+41 \d{2,3}( \d{2,3}){2,3}$")

FORBIDDEN = [
    (re.compile(r"\bGalledia AG\b"), "Es gibt keine 'Galledia AG' — exakte OE verwenden"),
    (re.compile(r"\bGalledia Gruppe\b"), "Heisst 'galledia group ag' (klein geschrieben)"),
    (re.compile(r"\bGalledia Group AG\b"), "Heisst 'galledia group ag' (klein geschrieben)"),
    (re.compile(r"\bGalledia GmbH\b"), "Alle Galledia-OE sind AG, keine GmbH"),
    (re.compile(r"(?i)\bfax\b"), "Fax wird nicht mehr verwendet"),
]


class ValidationError(Exception):
    pass


# ---------------------------------------------------------------------------
# Input decoding & mojibake repair
# ---------------------------------------------------------------------------

# Common mojibake sequences that indicate UTF-8 bytes read as Latin-1/cp1252.
# Detecting any of these signals the string was double-encoded somewhere upstream.
MOJIBAKE_MARKERS = (
    "Ã¼", "Ã¶", "Ã¤", "ÃŸ",         # ü ö ä ß as UTF-8 bytes read as Latin-1
    "Ãœ", "Ã–", "Ã„",               # Ü Ö Ä
    "Ã©", "Ã¨", "Ã ", "Ã§",         # é è à ç
    "Â·", "Â«", "Â»", "Â§", "Â°",   # · « » § °
    "â€™", "â€œ", "â€",              # smart quotes / dashes UTF-8 → Win-1252
)


def _decode_input(raw: bytes) -> str:
    """
    Decode JSON input bytes. Tolerates UTF-8 with/without BOM, falls back to
    cp1252 if UTF-8 fails (rare but happens when a caller writes JSON in the
    Windows default codepage).
    """
    # UTF-8 with optional BOM
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw[3:].decode("utf-8")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("cp1252")


def _repair_mojibake(obj):
    """
    Recursively walk a JSON-loaded structure and repair mojibake in strings.
    """
    if isinstance(obj, dict):
        return {k: _repair_mojibake(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_repair_mojibake(v) for v in obj]
    if isinstance(obj, str):
        return _fix_mojibake_string(obj)
    return obj


def _fix_mojibake_string(s: str) -> str:
    """
    If `s` looks like mojibake (UTF-8 bytes interpreted as Latin-1/cp1252),
    return the repaired version. Otherwise return the original.
    """
    if not s or not any(m in s for m in MOJIBAKE_MARKERS):
        return s
    try:
        # Round-trip: re-encode as Latin-1 to get back the original UTF-8 bytes,
        # then decode them properly as UTF-8.
        repaired = s.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s
    return repaired


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(data: dict) -> None:
    errors: list[str] = []

    oe = data.get("sender_oe", "")
    if oe not in VALID_OE:
        errors.append(
            f"sender_oe '{oe}' ist keine gueltige OE. "
            f"Erlaubt: {sorted(VALID_OE)}"
        )

    for field in ("sender_contact_phone", "sender_contact_mobile"):
        val = (data.get(field) or "").strip()
        if val and not PHONE_RE.match(val):
            errors.append(
                f"{field} '{val}' entspricht nicht dem Galledia-Format "
                f"(z.B. 'T +41 58 344 96 22')"
            )

    body_text = " ".join(_collect_all_text(data))
    for pat, msg in FORBIDDEN:
        if pat.search(body_text):
            errors.append(f"Verbotene Schreibweise: {msg}")

    for field in ("subject", "introduction", "body", "closing"):
        val = data.get(field, "")
        if isinstance(val, str) and ('"' in val):
            errors.append(
                f"{field} enthaelt gerade Anfuehrungszeichen \". "
                f"Galledia-CI verlangt Guillemets « »."
            )

    if errors:
        raise ValidationError("\n".join(f"- {e}" for e in errors))


def _collect_all_text(data: dict) -> Iterable[str]:
    for v in data.values():
        if isinstance(v, str):
            yield v
        elif isinstance(v, list):
            for x in v:
                if isinstance(x, str):
                    yield x


# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------

def qn(tag: str) -> str:
    return f"{{{W_NS}}}{tag}"


def _find_sdts_by_tag(root, tag: str):
    return [
        sdt for sdt in root.iter(qn("sdt"))
        if (t := sdt.find(f".//{qn('tag')}")) is not None and t.get(qn("val")) == tag
    ]


def _make_w(tag_name: str, **attrs) -> etree._Element:
    el = etree.SubElement(etree.Element(qn("wrap")), qn(tag_name))
    el.getparent().remove(el)
    for k, v in attrs.items():
        el.set(qn(k), v)
    return el


def _new_element(tag_name: str) -> etree._Element:
    return etree.Element(qn(tag_name))


def _set_run_text_with_breaks(run, lines: list[str]) -> None:
    """Replace all content of run with w:t + w:br segments. Keeps w:rPr if present."""
    rpr = run.find(qn("rPr"))
    # remove all children except rPr
    for child in list(run):
        if child.tag != qn("rPr"):
            run.remove(child)
    for i, line in enumerate(lines):
        if i > 0:
            run.append(_new_element("br"))
        t = _new_element("t")
        t.text = line
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        run.append(t)


def _set_paragraph_lines(p, lines: list[str]) -> None:
    """Replace runs in paragraph with text. Multi-line lines use w:br between."""
    runs = p.findall(qn("r"))
    if not runs:
        r = _new_element("r")
        _set_run_text_with_breaks(r, lines)
        p.append(r)
        return
    # keep first run; populate it; drop the rest
    _set_run_text_with_breaks(runs[0], lines)
    for r in runs[1:]:
        p.remove(r)


def _replace_sdt_content(sdt, lines: list[str]) -> None:
    """Replace the content of a single <w:sdt>."""
    if not lines:
        lines = [""]
    sdt_content = sdt.find(qn("sdtContent"))
    if sdt_content is None:
        return

    paragraphs = sdt_content.findall(qn("p"))
    if len(paragraphs) == 1:
        # Single paragraph with internal line breaks (<w:br/>) — replace its runs
        # with one run containing text + <w:br/> separators. Also drop adjacent
        # <w:proofErr> markers since they reference the old text.
        p = paragraphs[0]
        for el in list(p):
            if el.tag in (qn("r"), qn("proofErr")):
                p.remove(el)
        r = _new_element("r")
        _set_run_text_with_breaks(r, lines)
        p.append(r)
    elif paragraphs:
        # Genuine multi-paragraph SDT — clone first as template, one per line.
        # Strip w14:paraId/textId on clones to avoid duplicate IDs.
        template_p = deepcopy(paragraphs[0])
        _strip_paraid_attrs(template_p)
        for p in paragraphs:
            sdt_content.remove(p)
        for line in lines:
            new_p = deepcopy(template_p)
            _set_paragraph_lines(new_p, [line])
            sdt_content.append(new_p)
    else:
        # Inline SDT — runs are directly inside sdtContent.
        runs = sdt_content.findall(qn("r"))
        # Also drop any inline proofErr markers
        for el in list(sdt_content):
            if el.tag == qn("proofErr"):
                sdt_content.remove(el)
        if not runs:
            r = _new_element("r")
            _set_run_text_with_breaks(r, lines)
            sdt_content.append(r)
        else:
            _set_run_text_with_breaks(runs[0], lines)
            for r in runs[1:]:
                sdt_content.remove(r)


W14_NS = "http://schemas.microsoft.com/office/word/2010/wordml"


def _strip_paraid_attrs(p) -> None:
    """Remove w14:paraId and w14:textId attributes — they must be unique per document."""
    for attr in (f"{{{W14_NS}}}paraId", f"{{{W14_NS}}}textId"):
        if attr in p.attrib:
            del p.attrib[attr]


def set_content_control(root, tag: str, value) -> int:
    if isinstance(value, str):
        lines = value.split("\n")
    else:
        lines = [s for x in value for s in str(x).split("\n")]
    empty = not any(l.strip() for l in lines)
    sdts = _find_sdts_by_tag(root, tag)
    for sdt in sdts:
        sdt_pr = sdt.find(qn("sdtPr"))
        if sdt_pr is not None:
            for el in list(sdt_pr):
                if el.tag == qn("showingPlcHdr"):
                    sdt_pr.remove(el)
        if empty:
            # Word renders the docPart placeholder ("Klicken oder tippen...")
            # whenever the SDT content is truly empty, even with showingPlcHdr
            # cleared. A single space keeps the SDT "filled" without visible text.
            _replace_sdt_content(sdt, [" "])
        else:
            _replace_sdt_content(sdt, lines)
    return len(sdts)


# ----- Bookmarks -----

def set_bookmark_text(root, bookmark_name: str, items) -> bool:
    """
    items can be:
      - str (single paragraph)
      - list[str] (each = paragraph, inner \\n become <w:br/>)
      - list[dict] with keys 'lines' (list[str]) and optional 'style' (paragraph
        style ID like 'Aufzhlungszeichen' for bullets).
    """
    if isinstance(items, str):
        items = [items]
    if not items:
        items = [""]

    # Normalize to list of {"lines": [...], "style": str|None}
    normalized: list[dict] = []
    for item in items:
        if isinstance(item, dict):
            normalized.append({
                "lines": item.get("lines", [""]),
                "style": item.get("style"),
            })
        else:
            normalized.append({"lines": _split_inner_lines(str(item)), "style": None})

    bm_start = None
    for el in root.iter(qn("bookmarkStart")):
        if el.get(qn("name")) == bookmark_name:
            bm_start = el
            break
    if bm_start is None:
        return False

    bm_id = bm_start.get(qn("id"))
    paragraphs_in_range: list = []
    inside = False
    bm_end = None
    for el in root.iter():
        if el is bm_start:
            inside = True
            continue
        if el.tag == qn("bookmarkEnd") and el.get(qn("id")) == bm_id:
            bm_end = el
            break
        if inside and el.tag == qn("p"):
            paragraphs_in_range.append(el)

    if bm_end is None or not paragraphs_in_range:
        return False

    template_p = deepcopy(paragraphs_in_range[0])
    for tag_to_remove in (qn("bookmarkStart"), qn("bookmarkEnd")):
        for el in list(template_p.iter(tag_to_remove)):
            el.getparent().remove(el)

    # Fill existing paragraphs in-place. Only change pStyle when the item
    # explicitly requested one — otherwise keep the template's original style
    # (e.g. the Subject bookmark is bold via its pStyle).
    for i, p in enumerate(paragraphs_in_range):
        if i < len(normalized):
            _set_paragraph_lines(p, normalized[i]["lines"])
            if normalized[i]["style"] is not None:
                _set_paragraph_style(p, normalized[i]["style"])
        else:
            _set_paragraph_lines(p, [""])

    # Append extra paragraphs (cloned from template) when items > existing paragraphs.
    if len(normalized) > len(paragraphs_in_range):
        last_p = paragraphs_in_range[-1]
        parent = last_p.getparent()
        insert_at = list(parent).index(last_p) + 1
        for offset, item in enumerate(normalized[len(paragraphs_in_range):]):
            new_p = deepcopy(template_p)
            _strip_paraid_attrs(new_p)
            _set_paragraph_lines(new_p, item["lines"])
            if item["style"] is not None:
                _set_paragraph_style(new_p, item["style"])
            parent.insert(insert_at + offset, new_p)

    return True


def _set_paragraph_style(p, style_id: str | None) -> None:
    """Set or clear the <w:pStyle> of a paragraph."""
    pPr = p.find(qn("pPr"))
    if style_id is None:
        if pPr is not None:
            for el in list(pPr):
                if el.tag == qn("pStyle"):
                    pPr.remove(el)
        return
    if pPr is None:
        pPr = _new_element("pPr")
        p.insert(0, pPr)
    # remove existing pStyle, then prepend new one
    for el in list(pPr):
        if el.tag == qn("pStyle"):
            pPr.remove(el)
    pStyle = _new_element("pStyle")
    pStyle.set(qn("val"), style_id)
    pPr.insert(0, pStyle)


def _split_inner_lines(text: str) -> list[str]:
    """Split a single 'logical paragraph' on \\n into lines (rendered as <w:br/>)."""
    if not text:
        return [""]
    return text.split("\n")


BULLET_PREFIXES = ("· ", "• ")


def _parse_body(body: str) -> list[dict]:
    """
    Parse free-form body text into a list of paragraph items.

    Rules:
      - Lines starting with '· ' or '• ' become bullet paragraphs (Aufzhlungszeichen
        style). The bullet prefix is stripped — Word renders the bullet from the
        style's numbering definition.
      - Blank lines separate regular paragraphs.
      - Otherwise, consecutive non-bullet lines are collected into one paragraph
        (with <w:br/> between lines).
    """
    items: list[dict] = []
    current_lines: list[str] = []

    def flush():
        if current_lines:
            items.append({"lines": list(current_lines), "style": None})
            current_lines.clear()

    for raw_line in body.split("\n"):
        line = raw_line.rstrip()
        stripped = line.lstrip()
        if any(stripped.startswith(p) for p in BULLET_PREFIXES):
            flush()
            text = stripped[2:].strip()
            items.append({"lines": [text], "style": "Aufzhlungszeichen"})
        elif stripped == "":
            flush()
        else:
            current_lines.append(line)
    flush()

    return items or [{"lines": [""], "style": None}]


# ---------------------------------------------------------------------------
# CustomXml (officeatwork) binding
# ---------------------------------------------------------------------------

def _strip_dead_customxml(zip_bytes: dict[str, bytes]) -> list[str]:
    """
    Remove customXml items whose root namespace is in DEAD_CUSTOMXML_NAMESPACES.
    Updates the document relationships and [Content_Types].xml accordingly.
    Returns the list of items that were removed (for the report).
    """
    removed: list[str] = []
    to_remove_paths: set[str] = set()
    # Map item path -> propsN path (same N)
    for name in list(zip_bytes):
        if not (name.startswith("customXml/item") and name.endswith(".xml")
                and "itemProps" not in name):
            continue
        try:
            root = etree.fromstring(zip_bytes[name])
        except etree.XMLSyntaxError:
            continue
        ns = etree.QName(root.tag).namespace
        if ns in DEAD_CUSTOMXML_NAMESPACES:
            removed.append(name)
            to_remove_paths.add(name)
            # Matching itemProps and rels paths
            num = re.search(r"item(\d+)\.xml$", name).group(1)
            to_remove_paths.add(f"customXml/itemProps{num}.xml")
            to_remove_paths.add(f"customXml/_rels/item{num}.xml.rels")

    if not removed:
        return []

    # Update word/_rels/document.xml.rels: drop relationships pointing to removed items
    rels_path = "word/_rels/document.xml.rels"
    if rels_path in zip_bytes:
        rels_root = etree.fromstring(zip_bytes[rels_path])
        removed_targets = {p.replace("customXml/", "../customXml/") for p in to_remove_paths
                           if p.startswith("customXml/item") and "Props" not in p
                           and "_rels" not in p}
        for rel in list(rels_root):
            target = rel.get("Target", "")
            if target in removed_targets:
                rels_root.remove(rel)
        zip_bytes[rels_path] = etree.tostring(
            rels_root, xml_declaration=True, encoding="UTF-8", standalone=True
        )

    # Update [Content_Types].xml: drop Override entries for removed parts
    ct_path = "[Content_Types].xml"
    if ct_path in zip_bytes:
        ct_root = etree.fromstring(zip_bytes[ct_path])
        removed_partnames = {f"/{p}" for p in to_remove_paths if not p.endswith(".rels")}
        for override in list(ct_root):
            if etree.QName(override.tag).localname != "Override":
                continue
            if override.get("PartName") in removed_partnames:
                ct_root.remove(override)
        zip_bytes[ct_path] = etree.tostring(
            ct_root, xml_declaration=True, encoding="UTF-8", standalone=True
        )

    # Finally remove the files themselves
    for path in to_remove_paths:
        zip_bytes.pop(path, None)

    return removed


def _find_officeatwork_part(zip_bytes: dict[str, bytes]) -> str | None:
    """Return path of customXml/itemN.xml whose root namespace is officeatwork CustomXMLPart."""
    for name, raw in zip_bytes.items():
        if not (name.startswith("customXml/item") and name.endswith(".xml")
                and "itemProps" not in name):
            continue
        try:
            root = etree.fromstring(raw)
        except etree.XMLSyntaxError:
            continue
        if root.tag == f"{{{OFFICEATWORK_NS}}}officeatwork":
            return name
    return None


def _patch_officeatwork_part(raw: bytes, data: dict) -> bytes:
    """Patch element values in the officeatwork CustomXMLPart with our data."""
    root = etree.fromstring(raw)

    sig1_lines = [data["sender_contact_name"]]
    if data.get("sender_contact_phone"):
        sig1_lines.append(data["sender_contact_phone"])
    if data.get("sender_contact_mobile"):
        sig1_lines.append(data["sender_contact_mobile"])
    if data.get("sender_contact_email"):
        sig1_lines.append(data["sender_contact_email"])

    sig_name = data.get("signatory_name") or data["sender_contact_name"]
    sig_role = data.get("signatory_role", "")
    if isinstance(sig_role, list):
        sig_role = "\n".join(s for s in sig_role if s)

    updates = {
        "Organisation": data["sender_oe"],
        "AdressBlockOrganisation": data["sender_oe"],
        # Trailing empty line creates visual spacing before "Ihr Kontakt" below.
        "AdressBlock": "\n".join([data["sender_street"], data["sender_city"], ""]),
        "Address1": data["sender_street"],
        "Address2": data["sender_city"],
        "City": data["date_city"],
        "Date": data["date"],
        "Introduction": data.get("introduction", "Sehr geehrte Damen und Herren"),
        "Closing": data.get("closing", "Freundliche Grüsse"),
        "RecipientAddress": "\n".join(data["recipient_lines"]),
        "AdressBlockSignature1": "\n".join(sig1_lines),
        "AdressBlockSignature2": data.get("sender_contact_extra", ""),
        "Doc.Contact": data.get("contact_label", "Ihr Kontakt"),
        "Signature1": "\n".join(filter(None, [sig_name, sig_role])),
        "Signature2": "",
        "CopyTo": data.get("copy_to", ""),
    }

    for child in list(root):
        local = etree.QName(child.tag).localname
        if local in updates:
            val = updates[local]
            # Word renders the docPart placeholder ("Klicken oder tippen...") if
            # the bound value is empty. A single space keeps the binding non-empty
            # without visible text.
            child.text = val if val else " "
            for sub in list(child):
                child.remove(sub)

    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


# ---------------------------------------------------------------------------
# Main fill
# ---------------------------------------------------------------------------

def fill(data: dict, template: Path, output: Path) -> dict:
    validate(data)

    report: dict = {"tags_filled": {}, "bookmarks_filled": {}}

    # Read template zip into memory; parse each XML part; write modified parts back.
    with zipfile.ZipFile(str(template), "r") as zin:
        zip_bytes = {name: zin.read(name) for name in zin.namelist()}

    # --- Strip dead customXml parts left over from the deprecated officeatwork tool ---
    removed = _strip_dead_customxml(zip_bytes)
    if removed:
        report["customxml_stripped"] = removed

    # --- Update customXml binding (CustomXMLPart, drives SDT values) ---
    # Word reads SDT values from here when <w:dataBinding> is set, so this is
    # the authoritative source. The part still uses the legacy officeatwork
    # CustomXMLPart namespace because the SDTs reference it via storeItemID;
    # renaming would invalidate every binding in the .dotx.
    aw_part_name = _find_officeatwork_part(zip_bytes)
    if aw_part_name:
        zip_bytes[aw_part_name] = _patch_officeatwork_part(zip_bytes[aw_part_name], data)
        report["customxml_patched"] = aw_part_name

    # Identify XML parts we need to modify: document, header, footer
    xml_parts = [
        name for name in zip_bytes
        if name == "word/document.xml"
        or (name.startswith("word/header") and name.endswith(".xml"))
        or (name.startswith("word/footer") and name.endswith(".xml"))
    ]

    parser = etree.XMLParser(remove_blank_text=False)
    trees = {name: etree.parse(io.BytesIO(zip_bytes[name]), parser) for name in xml_parts}
    roots = {name: trees[name].getroot() for name in xml_parts}

    def apply_to_all(tag: str, value) -> int:
        total = 0
        for r in roots.values():
            total += set_content_control(r, tag, value)
        return total

    def apply_bookmark(name: str, value) -> bool:
        for r in roots.values():
            if set_bookmark_text(r, name, value):
                return True
        return False

    # --- Content controls ---
    report["tags_filled"]["Address2"] = apply_to_all("Address2", data["sender_city"])
    report["tags_filled"]["Address1"] = apply_to_all("Address1", data["sender_street"])
    report["tags_filled"]["AdressBlockOrganisation"] = apply_to_all(
        "AdressBlockOrganisation", data["sender_oe"]
    )
    # AdressBlockOrganisation already sets the OE on a separate line above; this
    # block only carries street/city plus a trailing blank line for spacing.
    sender_block_lines = [data["sender_street"], data["sender_city"], ""]
    report["tags_filled"]["AdressBlock"] = apply_to_all("AdressBlock", sender_block_lines)
    contact_label = data.get("contact_label", "Ihr Kontakt")
    report["tags_filled"]["Doc.Contact"] = apply_to_all("Doc.Contact", contact_label)

    sig1_lines: list[str] = [data["sender_contact_name"]]
    if data.get("sender_contact_phone"):
        sig1_lines.append(data["sender_contact_phone"])
    if data.get("sender_contact_mobile"):
        sig1_lines.append(data["sender_contact_mobile"])
    if data.get("sender_contact_email"):
        sig1_lines.append(data["sender_contact_email"])
    report["tags_filled"]["AdressBlockSignature1"] = apply_to_all(
        "AdressBlockSignature1", sig1_lines
    )
    report["tags_filled"]["AdressBlockSignature2"] = apply_to_all(
        "AdressBlockSignature2", data.get("sender_contact_extra", "")
    )

    report["tags_filled"]["RecipientAddress"] = apply_to_all(
        "RecipientAddress", data["recipient_lines"]
    )
    report["tags_filled"]["City"] = apply_to_all("City", data["date_city"])
    report["tags_filled"]["Date"] = apply_to_all("Date", data["date"])
    report["tags_filled"]["Introduction"] = apply_to_all(
        "Introduction", data.get("introduction", "Sehr geehrte Damen und Herren")
    )
    report["tags_filled"]["Closing"] = apply_to_all(
        "Closing", data.get("closing", "Freundliche Grüsse")
    )
    report["tags_filled"]["Organisation"] = apply_to_all("Organisation", data["sender_oe"])
    sig_name = data.get("signatory_name") or data["sender_contact_name"]
    report["tags_filled"]["Signature1"] = apply_to_all("Signature1", sig_name)
    sig_role = data.get("signatory_role", "")
    report["tags_filled"]["Signature2"] = apply_to_all("Signature2", sig_role)
    if data.get("copy_to"):
        report["tags_filled"]["CopyTo"] = apply_to_all("CopyTo", data["copy_to"])

    # --- Bookmarks ---
    if "subject" in data:
        report["bookmarks_filled"]["Subject"] = apply_bookmark("Subject", data["subject"])

    body = data.get("body", "")
    body_items = _parse_body(body) if isinstance(body, str) else list(body)
    if body_items:
        report["bookmarks_filled"]["Text"] = apply_bookmark("Text", body_items)

    if data.get("enclosures"):
        report["bookmarks_filled"]["CustomFieldEnclosures"] = apply_bookmark(
            "CustomFieldEnclosures", data["enclosures"]
        )

    # --- Serialize modified XML parts back into zip ---
    for name in xml_parts:
        zip_bytes[name] = etree.tostring(
            trees[name],
            xml_declaration=True,
            encoding="UTF-8",
            standalone=True,
        )

    # --- Rewrite [Content_Types].xml: template -> document ---
    ct = zip_bytes["[Content_Types].xml"].decode("utf-8")
    ct = ct.replace(TEMPLATE_CT, DOCUMENT_CT)
    zip_bytes["[Content_Types].xml"] = ct.encode("utf-8")

    # --- Write output zip ---
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(str(output), "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data_bytes in zip_bytes.items():
            zout.writestr(name, data_bytes)

    report["output"] = str(output)
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description="Galledia Brief Generator")
    ap.add_argument("--input", required=True, help="Pfad zur JSON-Eingabe oder '-' fuer stdin")
    ap.add_argument("--output", required=True, help="Pfad fuer Ausgabe-.docx")
    ap.add_argument("--template", default=str(TEMPLATE_PATH), help="Pfad zur .dotx-Vorlage")
    args = ap.parse_args()

    if args.input == "-":
        # Read stdin as raw bytes, decode UTF-8 explicitly. The default
        # sys.stdin encoding on Windows is cp1252, which corrupts non-ASCII
        # input from callers that pipe UTF-8 (e.g. Claude tools).
        raw = sys.stdin.buffer.read()
        data = json.loads(_decode_input(raw))
    else:
        with open(args.input, "rb") as f:
            data = json.loads(_decode_input(f.read()))

    data = _repair_mojibake(data)

    try:
        report = fill(data, Path(args.template), Path(args.output))
    except ValidationError as e:
        print("VALIDIERUNG FEHLGESCHLAGEN:", file=sys.stderr)
        print(str(e), file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
