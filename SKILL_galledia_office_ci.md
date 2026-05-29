---
name: Galledia-Office-Dok-CI-CD
description: >
  Galledia Office CI/CD — erstellt alle CI-konformen Galledia-Dokumente in einem Skill.
  Routing: Brief (.docx formal) → «Brief», «Anschreiben», «Geschäftsbrief», «Kundenbrief».
  Kurzbrief (.docx 1-seitig mit Checkboxen) → «Kurzbrief», «Begleitschreiben», «Memo», «Kurzmitteilung».
  Dokument (.docx mehrseitig) → «Offerte», «Angebot», «Dokumentation», «Schulungsunterlagen».
  Präsentationen → separater Skill «Galledia-Praesentationen».
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

Bei Unklarheit kurz nachfragen, dann den richtigen Workflow starten.

> ⚠️ **KRITISCH — Tool-Routing:**
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

---

> **Präsentationen** (.pptx) laufen über den separaten Skill **«Galledia-Praesentationen»** — dieser Skill deckt nur Brief, Kurzbrief und Dokument ab.
