---
name: Galledia-Office-Dok-CI-CD
description: >
  Galledia Office CI/CD — erstellt alle CI-konformen Galledia-Dokumente in einem Skill.
  Routing: Brief (.docx formal) → «Brief», «Anschreiben», «Geschäftsbrief», «Kundenbrief».
  Kurzbrief (.docx 1-seitig mit Checkboxen) → «Kurzbrief», «Begleitschreiben», «Memo», «Kurzmitteilung».
  Dokument (.docx mehrseitig) → «Offerte», «Angebot», «Dokumentation», «Schulungsunterlagen».
  Präsentation (.pptx) → «Präsentation», «Deck», «Slides», «PowerPoint».
  Markenhandbuch v1.5. Volte-Schriften. Galledia-Logos. Schweizer Hochdeutsch (kein ß).
version: "1.1"
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

## Pflichtabfrage — IMMER vor dem Bauen

Bevor Code geschrieben wird, diese Fragen stellen — ausser sie sind bereits beantwortet:

1. **Datum + Rechtseinheit** (Fusszeile)
2. **Kernbotschaft** — Was soll die Zielgruppe nach der Präsentation denken/tun/entscheiden?
3. **3 wichtigste Fakten/Zahlen** — Konkrete Daten, keine Meinungen
4. **Zielgruppe** — GL, Kunde, Team, Investor?
5. **Storyline** — Grober Aufbau (Problem → Lösung → Nächste Schritte?)

Wenn der Nutzer sagt «mir egal», «nur ein Test», «füll selbst» → akzeptieren, plausiblen Inhalt zum Thema erfinden, aber dennoch Qualitätsprinzipien anwenden.

## Qualitätsprinzipien (verbindlich)

Claude leitet den Nutzer zu professionellen, aussagekräftigen Folien — nicht zu formatierten Aufzählungen.

**Pyramid Principle — jede Folie hat eine Hauptaussage:**
```
❌ Titel: «KI-Anwendungen»  (Thema, keine Aussage)
✅ Titel: «KI spart 3'900 Stunden pro Monat»  (Aussage mit Beweis)
```

**Zahlen statt Adjektive:**
```
❌ «Signifikante Effizienzsteigerung»
✅ «39% weniger manuelle Arbeit — 3'900h/Monat»
```

**Visuelle Beweise statt Bullet-Listen:**
```
❌ 5 Bullets zu «Vorteilen von KI»  → add_content("viel")
✅ 3 KPI-Callouts mit konkreten Zahlen  → kpi_grid()
✅ Vorher/Nachher-Vergleich  → two_column()
✅ Prozess in 4 Schritten  → flow_pipeline()
```

**Eine Aussage pro Folie — nie mehr als 3 Bullets:**
```
❌ 6 Bullets auf einer Inhaltsfolie
✅ 3 Bullets max — oder aufteilen auf 2 Folien
```

**Roter Faden — typische Struktur:**
```
Folie 1: Titel (Thema + Kernbotschaft im Untertitel)
Folie 2: Agenda
Folie 3: Ausgangslage / Problem (mit Zahl oder Fakt)
Folie 4: Lösung / Kernaussage (visuell — KPI, Pipeline, Zweispalter)
Folie 5: Beweis / Ergebnis (Zahlen, Vergleich)
Folie 6: Nächste Schritte (nummerierte Schritte)
Folie 7: Schlussfolie
```

## Setup

```bash
pip install python-pptx Pillow --break-system-packages
```

```python
# Assets von GitHub laden (Verzeichnisstruktur für helpers.py erhalten)
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
```

## Pflichtregeln — Häufige Fehler

**add_agenda():**
```python
# ❌ FALSCH — 2 Zeilen pro Punkt, Teaser verboten
add_agenda(prs, ["KI-Anwendungen
Status und Hintergrund", "Roadmap
Massnahmen"])
# ✅ RICHTIG — 1 Zeile pro Punkt, kein Zusatz
add_agenda(prs, ["KI-Anwendungen", "Roadmap", "Nächste Schritte"], folio="2")
```

**add_content() — Kapiteltitel:**
```python
# ❌ FALSCH — Zahlen als Kapiteltitel
add_content(prs, "viel", "01", "Headline", "Text", folio="3")
# ✅ RICHTIG — beschreibendes Wort
add_content(prs, "viel", "KI-Trends", "Headline max. 35 Zeichen", "Text", folio="3")
```

**kpi_grid() / two_column() / flow_pipeline() — kicker + headline PFLICHT:**
```python
# ❌ FALSCH — kicker und headline fehlen → leerer Seitenkopf
two_column(prs, "Heute", items_l, "Ziel", items_r, folio="4")
# ✅ RICHTIG
two_column(prs, "Heute", items_l, "Ziel 2026", items_r,
           kicker="Transformation", headline="Heute vs. Ziel 2026",
           col2_red=True, folio="4")

# ❌ FALSCH
kpi_grid(prs, [("96 GB","VRAM")], folio="3")
# ✅ RICHTIG
kpi_grid(prs, [("96 GB","VRAM"), ("256 GB","RAM"), ("6 TB","NVMe")],
         kicker="Hardware", headline="R&D AI-Workhorse", folio="3")
```

**Headline-Länge:**
```python
# ❌ FALSCH — zu lang, läuft über
add_content(prs, "viel", "KI-Trends", "KI in der Redaktion und Vermarktung 2026", ...)
# ✅ RICHTIG — max. 35 Zeichen
add_content(prs, "viel", "KI-Trends", "KI in Redaktion und Sales", ...)
```

## Verwendung

```python
prs = build_presentation(datum="29. Mai 2026", rechtseinheit="Galledia Fachmedien AG")
add_title(prs, "KI in Medien", "Chancen und Anwendungen")
add_agenda(prs, ["KI-Anwendungen", "Chancen und Anforderungen"], folio="2")
add_content(prs, "viel", "KI-Anwendungen",
            "KI in Redaktion und Sales",
            "· Inhaltsautomatisierung\n· Lead-Generierung\n· Personalisierung",
            folio="3")
two_column(prs, "Chancen", ["Effizienz", "Neue Erlöse"],
           "Anforderungen", ["Datenschutz", "Infrastruktur"],
           kicker="Einschätzung", headline="Chancen vs. Anforderungen",
           col2_red=True, folio="4")
add_closing(prs)
prs.save("output.pptx")
```

## Layouts (Vorlage_5)

| Inhalt | Funktion |
|---|---|
| Deck-Titel | `add_title(prs, titel, untertitel)` |
| Kapitel-Anker (rot) | `add_section(prs, "01", "Kapitel")` |
| Agenda ≤5 Punkte | `add_agenda(prs, items, variant="agenda5")` |
| Agenda 6–12 Punkte | `add_agenda(prs, items, variant="agenda22")` |
| Kernbotschaft | `add_content(prs, "wenig", ...)` |
| Text / Struktur | `add_content(prs, "viel", ...)` |
| KPI-Callouts | `kpi_grid(prs, [(zahl, label), ...])` |
| Zweispalter | `two_column(prs, head_l, items_l, head_r, items_r)` |
| Pipeline / Flow | `flow_pipeline(prs, nodes)` |
| Numm. Schritte | `numbered_steps(prs, [(titel, beschr), ...])` |
| Timeline | `timeline(prs, [(titel, beschr), ...])` |
| Diskussion | `add_discussion(prs)` |
| Schlussfolie | `add_closing(prs)` |

## CI-Regeln Präsentation

- **Schrift:** `Volte` (Text/Labels) · `Volte Semibold` (Headlines) · `Volte Rounded Semibold` nur vordefinierte Layouts
- **Keine Versalien.** Keine Folienübergänge. Max. 6 Zeilen / 3 Bullets pro Folie.
- **Fusszeile:** Format `Folie N, Datum, Rechtseinheit` — immer über `build_presentation(datum=..., rechtseinheit=...)` setzen.
- **Logo:** Rot auf hell · Weiss auf rot/dunkel · `add_logo(slide, variant='rot')`
- **Roter Rhythmus:** mindestens jede 3.–4. Folie ein Rot-Anker (Zwischenfolie oder roter KPI).
