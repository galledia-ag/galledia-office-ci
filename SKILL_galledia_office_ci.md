---
name: Galledia-Office-Dok-CI-CD
description: >
  Galledia Office CI/CD — erstellt alle CI-konformen Galledia-Dokumente in einem Skill.
  Routing: Brief (.docx formal) → «Brief», «Anschreiben», «Geschäftsbrief», «Kundenbrief».
  Kurzbrief (.docx 1-seitig mit Checkboxen) → «Kurzbrief», «Begleitschreiben», «Memo», «Kurzmitteilung».
  Dokument (.docx mehrseitig) → «Offerte», «Angebot», «Dokumentation», «Schulungsunterlagen».
  Präsentation (.pptx) → «Präsentation», «Deck», «Slides», «PowerPoint».
  Markenhandbuch v1.5. Volte-Schriften. Galledia-Logos. Schweizer Hochdeutsch (kein ß).
version: "1.2"
---

# Galledia Office CI/CD

Alle CI-konformen Galledia-Office-Dokumente in einem Skill.

## Routing

| Anfrage enthält | → Workflow |
|---|---|
| «Brief», «Anschreiben», «Geschäftsbrief», «Kundenbrief», «Begleitbrief» | **1. Brief** |
| «Kurzbrief», «Kurzmitteilung», «Begleitschreiben», «Memo», «Transmittal» | **2. Kurzbrief** |
| «Offerte», «Angebot», «Dokumentation», «Schulungsunterlagen», «mehrseitiges Dokument» | **3. Dokument** |
| «Präsentation», «Deck», «Slides», «PowerPoint», «.pptx» | **4. Präsentation** |

Bei Unklarheit kurz nachfragen, dann den richtigen Workflow starten.

> ⚠️ **KRITISCH — Tool-Routing:**
> - Präsentation: **NUR Code Execution** (`helpers.py` + `Vorlage_5.pptx`).  
>   Das MCP-Tool `generate_galledia_praesentation` ist **DEPRECATED** — **NIE aufrufen**, auch wenn es verfügbar erscheint.
> - Brief / Kurzbrief: **NUR** `mcp__galledia-office__generate_galledia_brief` / `generate_galledia_kurzbrief`

---

# CI-Referenz (Markenhandbuch v1.5)

## Organisationseinheiten — exakte Schreibweise

| Schreibweise | Typ |
|---|---|
| `galledia group ag` | Dachmarke / Holding — **komplett klein** |
| `Galledia Fachmedien AG` | Verlag (Rapperswil-Jona, Luzern, Zürich) |
| `Galledia Regionalmedien AG` | Regionalmedien (Berneck) |
| `Galledia Print AG` | Druckerei |
| `Galledia Digital AG` | Digital |

**Verboten:** ~~Galledia AG~~ · ~~Galledia Gruppe~~ · ~~Galledia Group AG~~ · ~~Galledia GmbH~~ · ~~GALLEDIA FACHMEDIEN AG~~

## Telefon-Format

| Format | Beispiel |
|---|---|
| Festnetz | `T +41 58 344 96 22` |
| Mobile | `M +41 78 846 24 16` |

Immer `+41`, Prefix `T`/`M`, kein Fax (nicht mehr verwendet).

## Sonderzeichen

| Zweck | Zeichen |
|---|---|
| Aufzählung | `·` (Mittelpunkt U+00B7) |
| Anführungszeichen | `«` `»` (Guillemets) |
| Trenner | `\|` (Pipe) |
| Gedankenstrich | `—` (em dash) |

## Standorte und Adressen

**Galledia Fachmedien AG**

| Standort | Strasse | PLZ Ort | Tel |
|---|---|---|---|
| Zürich | Baslerstrasse 60 | 8048 Zürich | T +41 58 344 98 98 |
| Rapperswil-Jona | Tiefenaustrasse 2 | 8640 Rapperswil-Jona | T +41 44 928 56 11 |
| Luzern | Maihofstrasse 76 | 6006 Luzern | T +41 58 344 91 50 |
| Flawil | Burgauerstrasse 50 | 9230 Flawil | T +41 58 344 96 96 |

**Galledia Digital AG:** Bahnhofstrasse 4, 9470 Buchs SG, T +41 58 344 92 42

**Galledia Print AG:** Flawil (HQ) Burgauerstrasse 50, 9230 Flawil · Baar (Multicolor) Sihlbruggstrasse 105a, 6340 Baar

**galledia group ag (Holding):**
- Primär: Burgauerstrasse 50, 9230 Flawil, T +41 58 344 96 96
- Offiziell: Hafnerwisenstrasse 1, 9442 Berneck, T +41 71 747 22 22

Adresszeile Brief-Kopf-Format: `PLZ Ort | Organisationseinheit | Strasse`

## Farben

| Name | HEX | Verwendung |
|---|---|---|
| Galledia-Rot | `#E61C52` | Primärfarbe, Logo, Akzente |
| Galledia-Schwarz | `#000000` | Text |
| Grau 1–4 | `#404040` `#666666` `#A6A6A6` `#D9D9D9` | Sekundärtext, Strukturen |
| Hellgrau | `#F2F2F5` | Karten-Hintergrund, Tabellen |

## Schriften

| Font | Verwendung |
|---|---|
| Volte Regular | Grundtext, Fliesstext |
| Volte Semibold | Titel, Zwischentitel, Hervorhebungen |
| Volte Rounded Semibold | Plakative Headlines (nur Präsentation) |

Schweizer Hochdeutsch: `ss` statt `ß` (also «Grüsse», nicht «Grüße»).

---

# 1. Brief

Formaler Geschäftsbrief im Galledia-CI. Generierung via MCP `galledia-office`.

## Pflichtfelder

- `sender_oe` — eine der 5 Organisationseinheiten (exakte Schreibweise!)
- `sender_street`, `sender_city`
- `sender_contact_name`
- `recipient_lines` — Liste (eine Zeile pro Eintrag)
- `date_city`, `date` (z.B. `Zürich` / `28. Mai 2026`)
- `subject` (Betreff)
- `body` (Brieftext; `\n\n` = Absatz, `\n` = Zeilenumbruch, `· ` am Anfang = Aufzählungspunkt)

## Optionale Felder

`sender_contact_phone`, `sender_contact_mobile`, `sender_contact_email`,
`introduction` (Default: `Sehr geehrte Damen und Herren`),
`closing` (Default: `Freundliche Grüsse`),
`signatory_name`, `signatory_role`, `enclosures`, `copy_to`

## Workflow

1. Fehlende Pflichtfelder erfragen (bereits genannte NICHT nochmals fragen)
2. CI-Validierung: OE-Schreibweise korrekt? Telefonformat `T +41 …`? Keine verbotenen Begriffe?
3. MCP-Tool aufrufen: `mcp__galledia-office__generate_galledia_brief`
4. Download-Link präsentieren:
   ```
   Hier ist der Brief: [Dateiname.docx](URL)
   Gültig für 60 Minuten.
   ```
   **Wichtig:** URL NIE selbst per curl/fetch herunterladen — nur als Link ausgeben.

---

# 2. Kurzbrief

1-seitiges Begleitschreiben mit 10 vordefinierten Checkboxen (werden gedruckt angekreuzt).
Generierung via MCP `galledia-office`.

## Pflichtfelder (identisch Brief, aber OHNE `body`)

`sender_oe`, `sender_street`, `sender_city`, `sender_contact_name`,
`recipient_lines`, `date_city`, `date`, `subject`

## Notizoptionen (Checkboxen)

| Key | Standard-Text |
|---|---|
| `Note1` | zur Kenntnisnahme |
| `Note2` | zu Ihren Akten |
| `Note3` | auf Ihren Wunsch |
| `Note4` | mit Dank zurück |
| `Note5` | zur Erledigung |
| `Note6` | gemäss telefonischer Besprechung |
| `Note7` | zur Stellungnahme |
| `Note8` | gemäss Ihrer Anfrage |
| `Note9` | per E-Mail an: |
| `Note10` | Beilagen: |

Einzelne Notes überschreiben: `notes = {"Note10": "Beilagen: Vertrag, AGB"}`

## Workflow

1. Pflichtfelder sammeln
2. CI-Validierung (gleich wie Brief)
3. MCP-Tool: `mcp__galledia-office__generate_galledia_kurzbrief`
4. Download-Link präsentieren (gleich wie Brief)

---

# 3. Dokument

Mehrseitiges CI-konformes Dokument (.docx): Offerten, Angebote, Dokumentationen, Schulungsunterlagen.
Generierung via Code Execution (`fill_dokument.py` + `Vorlage_Dokument.dotx`).

## Pflichtabfrage

- **Dokumenttitel** (z.B. «KI-Hub Offerte»)
- **Untertitel / Anlass** (z.B. «Angebot für XY AG»)
- **Datum** mit Ort (z.B. «Stäfa, 29. Mai 2026»)
- **Rechtseinheit** (z.B. «Galledia Fachmedien AG»)
- **Adresse** (z.B. «Seestrasse 90a\n8712 Stäfa»)
- **Struktur** — Kapitel und Inhalte (wenn unklar: erst Gliederung vorschlagen)

## Setup

```bash
pip install python-docx --break-system-packages
```

```python
import os, sys, urllib.request
_DIR = "/tmp/galledia_dokument"
os.makedirs(f"{_DIR}/assets", exist_ok=True)
sys.path.insert(0, _DIR)
_BASE = "https://raw.githubusercontent.com/galledia-ag/galledia-office-ci/main/skills/galledia-dokument"
for _name, _url in [
    ("fill_dokument.py",             "fill_dokument.py"),
    ("assets/Vorlage_Dokument.dotx", "assets/Vorlage_Dokument.dotx"),
]:
    _dest = f"{_DIR}/{_name}"
    if not os.path.exists(_dest):
        urllib.request.urlretrieve(f"{_BASE}/{_url}", _dest)
        print(f"✓ {_name} ({os.path.getsize(_dest):,} bytes)")

from fill_dokument import build_document
```

## Verwendung

```python
build_document(
    titel         = "KI-Hub Offerte",
    untertitel    = "Angebot AI-Infrastruktur",
    datum         = "Stäfa, 29. Mai 2026",
    rechtseinheit = "Galledia Fachmedien AG",
    adresse       = "Seestrasse 90a\n8712 Stäfa",       # \n = Zeilenumbruch
    empfaenger    = "XY AG\nz.H. Herr Max Muster\nCH-8000 Zürich",  # optional
    abschnitte    = [
        {
            "titel": "Ausgangslage",
            "inhalt": [
                {"typ": "text",    "inhalt": "Fliesstext..."},
                {"typ": "bullet",  "inhalt": "Aufzählungspunkt"},
                {"typ": "h2",      "inhalt": "Unterkapitel"},
                {"typ": "h3",      "inhalt": "Abschnitt"},
                {"typ": "tabelle", "inhalt": [
                    ["Spalte A", "Spalte B"],   # Kopfzeile (schwarz, F2F2F5)
                    ["Wert 1",   "Wert 2"],
                ]},
            ]
        },
    ],
    output_path = "output.docx",
)
```

## Aufbau: Deckblatt → TOC (eigene Seite) → Inhalt

Ort/Datum und Rechtseinheit nur auf dem Deckblatt — nicht am Schluss wiederholen.
TOC: in Word mit F9 aktualisieren.

---

# 4. Präsentation

CI-konforme PowerPoint (.pptx) via Code Execution (`helpers.py` + `Vorlage_5.pptx`).

> ⚠️ **KRITISCH:** `generate_galledia_praesentation` MCP ist **DEPRECATED** — **NIE aufrufen**.

---

## Pflichtabfrage — IMMER vor dem Bauen

Bevor Code geschrieben wird — ausser bereits in der Anfrage enthalten:

1. **Datum + Rechtseinheit** (Fusszeile)
2. **Kernbotschaft** — Was soll die Zielgruppe denken/tun/entscheiden?
3. **Zielgruppe** — GL, Kunde, Team, Investor?
4. **Storyline** — Grober Aufbau (Problem → Lösung → Nächste Schritte?)

«Mir egal» / «füll selbst» → plausiblen Inhalt erfinden, Qualitätsprinzipien trotzdem anwenden.

---

## Inhaltsdichte (VERBINDLICH — wichtigste Regel)

**Maximal viel Kontext pro Folie — NIEMALS auf mehr Folien verteilen.**

```
❌ 3 Bullets pro Folie → 8 Folien
✅ 10–15 Zeilen pro Folie → 5–6 Folien
```

Richtwert für `add_content("viel")`: 3–4 Abschnittsüberschriften, je 3–4 Bullets = 12–16 Zeilen.
Der Nutzer soll nicht nachfragen müssen «kannst du mehr Inhalt hinzufügen».

---

## Formatierungsregeln body_text (VERBINDLICH)

### 1. Aufzählungszeichen — Echte PowerPoint-Bullets

Kein manuelles `·` als Zeichen — `fmt(slide)` setzt echte Bullets automatisch:

| Notation | Zeichen | Farbe | Ebene |
|---|---|---|---|
| `·` am Zeilenanfang | ● ausgefüllt | Schwarz | Ebene 1 |
| `··` am Zeilenanfang | ○ hohl | Grau #666666 | Ebene 2 |

### 2. Abschnittsüberschriften — Volte Semibold, KEINE Versalien

```python
# ❌ FALSCH — Versalien
"MESSBARE EFFIZIENZGEWINNE\n· Bullet\n"

# ✅ RICHTIG — Titel-Gross/Kleinschreibung
"Messbare Effizienzgewinne\n· Bullet\n"
```

### 3. Bullet-Länge — max. 55 Zeichen

Zu lange Bullets wrappen ohne korrekten Einzug. Lieber aufteilen:

```
❌ · Kontext: 400k Token (200'000 Wörter), 256k Input @ 98% Accuracy Long-Context
✅ · Kontext: 400k Token = 200'000 Wörter
✅ · 256k Input @ 98% Accuracy (Long-Context)
```

### 4. Leerzeile zwischen Abschnitten

```python
body = (
    "Abschnitt 1\n"
    "· Bullet A\n"
    "\n"           # ← Leerzeile trennt Abschnitte
    "Abschnitt 2\n"
    "· Bullet B\n"
)
```

---

## `fmt()` — IMMER nach jedem `add_content()` aufrufen

```python
from pptx.oxml.ns import qn
from pptx.dml.color import RGBColor
from lxml import etree

SB    = "Volte Semibold"
BLACK = RGBColor(0x00, 0x00, 0x00)

def _set_bullet(para, level=0):
    """Echtes PowerPoint-Aufzählungszeichen mit hängendem Einzug."""
    pPr = para._p.get_or_add_pPr()
    pPr.set("marL", str(457200 + level * 457200))  # 0.5" / 1.0"
    pPr.set("indent", "-342900")                    # hängend
    for tag in ("a:buNone", "a:buChar", "a:buFont", "a:buClr", "a:buSzPct"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    etree.SubElement(pPr, qn("a:buFont")).set("typeface", "Arial")
    sc = etree.SubElement(etree.SubElement(pPr, qn("a:buClr")), qn("a:srgbClr"))
    sc.set("val", "000000" if level == 0 else "666666")
    etree.SubElement(pPr, qn("a:buChar")).set(
        "char", "\u25CF" if level == 0 else "\u25CB")  # ● oder ○

def fmt(slide):
    """
    Nach add_content() aufrufen. Setzt:
    - Nicht-Bullet-Zeilen → Volte Semibold (Abschnittstitel)
    - ·  Zeilen           → Bullet Ebene 1 ● schwarz
    - ·· Zeilen           → Bullet Ebene 2 ○ grau
    """
    ph = {p.placeholder_format.idx: p for p in slide.placeholders}
    if 13 not in ph:
        return
    for para in ph[13].text_frame.paragraphs:
        t = para.text.strip()
        if not t:
            continue
        if t.startswith("··"):
            for r in para.runs:
                r.text = r.text.replace("··", "", 1).lstrip()
            _set_bullet(para, level=1)
        elif t.startswith("·"):
            for r in para.runs:
                r.text = r.text.replace("·", "", 1).lstrip()
            _set_bullet(para, level=0)
        else:
            for r in para.runs:
                r.font.name = SB
                r.font.color.rgb = BLACK
                r.font.bold = None

# Verwendung:
s = add_content(prs, "viel", "Strategie", "Use Cases mit ROI",
    "Use Case 1\n"
    "· Heute: 15 Min/Lead. Agent: 2 Min\n"
    "·· LinkedIn → ICP-Filter → Outreach\n"
    "·· Replies tracken → Eskalation Sales\n"
    "· ROI: CHF 260k/Jahr bei CHF 5.4k Kosten\n",
    folio="3")
fmt(s)  # ← IMMER
```

---

## `preflight()` — PFLICHT vor `present_files()`

```python
def preflight(prs):
    """Prüft CI-Regeln. Bei Fehler: Abbruch vor Ausgabe."""
    errors, warnings = [], []
    has_vis = False

    for i, slide in enumerate(prs.slides, 1):
        ph = {p.placeholder_format.idx: p for p in slide.placeholders}

        # Headline ≤ 35 Zeichen
        if 11 in ph:
            hl = ph[11].text_frame.text.strip()
            if len(hl) > 35:
                errors.append(f"Folie {i}: Headline {len(hl)} Zeichen: «{hl}»")

        # body_text Prüfungen
        if 13 in ph:
            for para in ph[13].text_frame.paragraphs:
                t = para.text.strip()
                if not t:
                    continue
                # Versalien
                if not t.startswith("·") and t == t.upper() and len(t) > 3:
                    errors.append(f"Folie {i}: Versalien: «{t}»")
                # Semibold gesetzt?
                if not t.startswith("·"):
                    for r in para.runs:
                        if r.font.name not in (SB, None):
                            warnings.append(f"Folie {i}: Titel nicht Semibold: «{t}»")
                # Bullet-Länge
                if t.startswith("·") and len(t) > 57:
                    warnings.append(f"Folie {i}: Bullet zu lang: «{t[:45]}…»")

        # Titelfolie: Untertitel
        if i == 1 and 12 in ph and not ph[12].text_frame.text.strip():
            errors.append("Folie 1: Kein Untertitel auf Titelfolie.")

        # Visualisierungsfolie erkennen
        if 11 in ph and 13 not in ph:
            has_vis = True

    if not has_vis:
        warnings.append("Keine Visualisierungsfolie (kpi_grid/flow_pipeline).")

    for w in warnings:
        print(f"⚠️  {w}")
    if errors:
        for e in errors:
            print(f"❌  {e}")
        raise ValueError(f"Pre-Flight: {len(errors)} Fehler — Ausgabe abgebrochen.")

    print(f"✅  Pre-Flight OK ({len(prs.slides)} Folien, {len(warnings)} Hinweise)")
```

---

## Titelfolie: Untertitel IMMER befüllen

```python
# ❌  add_title(prs, "KI 2026", "")
# ✅
add_title(prs, "KI 2026: Chancen und Roadmap", "Trends, Modelle, Use Cases")
```

---

## Headline-Länge: max. 35 Zeichen (überall)

Gilt für `add_content`, `kpi_grid`, `two_column`, `flow_pipeline`.

```python
# ❌  "18 Monate: Validierung → Skalierung → Transformation"  (53 Z.)
# ✅  "Galledia: 18-Monatsplan"  (23 Z.)
```

---

## `two_column()` — NUR auf ausdrücklichen Wunsch

Standard ist `add_content("viel")` mit Abschnittsüberschriften.
`two_column()` nur bei expliziten Begriffen: «Vergleich», «Gegenüberstellung», «zwei Spalten».

---

## Visualisierungsfolien — Mindestens 1–2 pro Präsentation

`source=` bei Visualisierungen IMMER befüllen:

```python
kpi_grid(prs, [...], kicker="...", headline="...", folio="5",
    source="Workday Research 2026 | Expleo April 2026")

flow_pipeline(prs, [...], kicker="Roadmap", headline="Galledia: 18-Monatsplan",
    folio="7", source="Interne Planung Galledia Fachmedien AG")
```

---

## Typische Folienstruktur (6–8 Folien)

```
Folie 1: Titel  (Titel + Untertitel BEIDE befüllt)
Folie 2: Inhaltsfolie  (12–16 Zeilen, fmt() aufrufen)
Folie 3: Inhaltsfolie  (12–16 Zeilen, fmt() aufrufen)
Folie 4: Inhaltsfolie  (12–16 Zeilen, fmt() aufrufen)
Folie 5: kpi_grid()  mit source=
Folie 6: Inhaltsfolie  (12–16 Zeilen, fmt() aufrufen)
Folie 7: flow_pipeline()  mit source=
Folie 8: Closing
```

---

## Setup

```bash
pip install python-pptx Pillow --break-system-packages
```

```python
import os, sys, urllib.request
_DIR = "/tmp/galledia_praesentation"
os.makedirs(f"{_DIR}/assets/logo", exist_ok=True)
sys.path.insert(0, _DIR)
_BASE = "https://raw.githubusercontent.com/galledia-ag/galledia-office-ci/main/skills/galledia-praesentation"
for _name, _url in [
    ("helpers.py",                   "helpers.py"),
    ("assets/Vorlage_5.pptx",        "assets/Vorlage_5.pptx"),
    ("assets/logo/logo_rot.png",     "assets/logo/logo_rot.png"),
    ("assets/logo/logo_weiss.png",   "assets/logo/logo_weiss.png"),
    ("assets/logo/logo_schwarz.png", "assets/logo/logo_schwarz.png"),
]:
    _dest = f"{_DIR}/{_name}"
    if not os.path.exists(_dest):
        urllib.request.urlretrieve(f"{_BASE}/{_url}", _dest)
        print(f"✓ {_name} ({os.path.getsize(_dest):,} bytes)")

from helpers import (build_presentation, add_title, add_section, add_agenda,
                     add_content, add_closing, add_discussion,
                     kpi_grid, two_column, flow_pipeline, numbered_steps, timeline)
from pptx.oxml.ns import qn
from pptx.dml.color import RGBColor
from lxml import etree

# fmt(), _set_bullet(), preflight() hier einfügen (siehe oben)
```

---

## Layouts (Vorlage_5)

| Inhalt | Funktion |
|---|---|
| Deck-Titel | `add_title(prs, titel, untertitel)` |
| Kapitel-Anker (rot) | `add_section(prs, "01", "Kapitel")` |
| Agenda ≤5 Punkte | `add_agenda(prs, items, variant="agenda5")` |
| Agenda 6–12 Punkte | `add_agenda(prs, items, variant="agenda22")` |
| Kernbotschaft | `add_content(prs, "wenig", ...)` |
| Text / Struktur | `add_content(prs, "viel", ...)` + `fmt(slide)` |
| KPI-Callouts | `kpi_grid(prs, [...], source=...)` |
| Zweispalter | `two_column(...)` — NUR auf Wunsch |
| Pipeline / Flow | `flow_pipeline(prs, nodes, source=...)` |
| Numm. Schritte | `numbered_steps(prs, [...])` |
| Timeline | `timeline(prs, [...])` |
| Diskussion | `add_discussion(prs)` |
| Schlussfolie | `add_closing(prs)` |

---

## CI-Kurzreferenz Präsentation

| Regel | Wert |
|---|---|
| Schrift Fliesstext | Volte Regular |
| Schrift Abschnittstitel | Volte Semibold via `fmt()` |
| Versalien | VERBOTEN |
| Headline max. | 35 Zeichen |
| Bullet max. | 55 Zeichen |
| Zeilen pro Folie | 12–16 |
| Bullet Ebene 1 | ● schwarz via `·` |
| Bullet Ebene 2 | ○ grau via `··` |
| two_column | Nur auf ausdrücklichen Wunsch |
| Titelfolie Untertitel | IMMER befüllen |
| source= Visualisierungen | IMMER befüllen |
| preflight() | IMMER vor present_files() |
| Folienübergänge | VERBOTEN |
