---
name: galledia-praesentation
description: >
  Erstellt und bearbeitet PowerPoint-Präsentationen im Galledia Corporate Design.
  Verwenden wenn: ein Deck, Slides oder .pptx für Galledia / Galledia Fachmedien / ZSW
  erstellt, gefüllt oder überarbeitet werden soll. Liefert CI-Mechanik (Layouts, Farben,
  Schriften, Regeln) — nicht den Inhalt.
version: "1.0"
template: assets/Vorlage_6.pptx
---

# Galledia-Präsentation

## Zweck
Ansprechende, abwechslungsreiche Decks im Galledia-CI. CI = Rahmen (Farben, Schrift, Logo,
Layouts). Gestaltung = freie Komposition INNERHALB dieses Rahmens. Niemals ein Einheits-Layout.

---

## Voraussetzungen

| Asset | Pfad | Status |
|---|---|---|
| Template | `assets/Vorlage_6.pptx` | ✅ bereit |
| Volte Regular | `assets/fonts/Volte-Regular.otf` | ✅ bereit |
| Volte Regular Italic | `assets/fonts/Volte-RegularItalic.otf` | ✅ bereit |
| Volte Semibold | `assets/fonts/Volte-Semibold.otf` | ✅ bereit |
| Volte Rounded Regular | `assets/fonts/VolteRounded-Regular.otf` | ✅ bereit |
| Volte Rounded Semibold | `assets/fonts/VolteRounded-Semibold.otf` | ✅ bereit |
| Logo rot (Bildmarke)          | `assets/logo/logo_rot.png`              | ✅ bereit |
| Logo rot + Schriftzug         | `assets/logo/logo_rot_schriftzug.png`   | ✅ bereit |
| Logo weiss (Bildmarke)        | `assets/logo/logo_weiss.png`            | ✅ bereit |
| Logo weiss + Schriftzug       | `assets/logo/logo_weiss_schriftzug.png` | ✅ bereit |
| Logo schwarz (Bildmarke)      | `assets/logo/logo_schwarz.png`          | ✅ bereit |
| Logo schwarz + Schriftzug     | `assets/logo/logo_schwarz_schriftzug.png` | ✅ bereit |
| Helper-Library | `helpers.py` | ✅ bereit |

Tools: `pip install python-pptx Pillow --break-system-packages`

---

## Goldene Regel: «Reduced to the max»

Markenwerte: einfach — persönlich — wirkungsvoll. Pro Folie EINE Aussage.
Lieber 8 klare Folien als 4 volle. Whitespace ist Teil des Designs.

**Treatment nach Inhalt (Markenhandbuch S. 42):**
- emotional / plakativ → Bild dominant, wenig Text → `02_wenigText`, Titelfolie, Zwischenfolie
- informativ / sachlich → typografisch, strukturiert → `04_vielText`, Agenda
- Niemals ALLE Folien typografisch → Bleiwüste

---

## Inhalt zuerst — die wichtigste Regel

Eine Präsentation ist nur so gut wie ihr Inhalt. Reihenfolge der Inhaltsquellen:

**1. Aktueller Gesprächs-/Projektkontext (höchste Priorität)**
Wenn der Nutzer um eine **Zusammenfassung dieses Projekts / Gesprächs** bittet, ist der Inhalt bereits da — im aktuellen Gespräch und im Projekt-Wissen. Diesen TATSÄCHLICHEN Inhalt zusammenfassen:
- Konkrete Entscheidungen, Schritte, Resultate, Versionen, Zahlen aus dem Gespräch
- Was wurde gebaut, was wurde gelöst, was sind die nächsten Schritte
- **Niemals auf generische Aussagen abstrahieren, wenn die Spezifika vor dir liegen.** Eine «Zusammenfassung» die den realen Inhalt durch Wikipedia-Bullets ersetzt, ist ein Totalausfall.

**2. Chat-Historie durchsuchen (`conversation_search`)**
Bei Galledia-internen Themen, die nicht im aktuellen Gespräch stehen (Jenny, ASMIQ, Digital Twin, n8n, m&k, Press-Release-Pipeline, Archiv): zuerst suchen — echte Zahlen, Architektur, Status, Namen sammeln.

**3. Pflichtabfrage**
Nur wenn Kontext und Historie nichts liefern oder das Thema extern ist.


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

CI-konforme PowerPoint (.pptx) via Code Execution (`helpers.py` + `Vorlage_6.pptx`).

## Inhalt zuerst — die wichtigste Regel

Eine Präsentation ist nur so gut wie ihr Inhalt. Reihenfolge der Inhaltsquellen:

**1. Aktueller Gesprächs-/Projektkontext (höchste Priorität)**
Wenn der Nutzer um eine **Zusammenfassung dieses Projekts / Gesprächs** bittet, ist der Inhalt bereits da — im aktuellen Gespräch und im Projekt-Wissen. Diesen TATSÄCHLICHEN Inhalt zusammenfassen:
- Konkrete Entscheidungen, Schritte, Resultate, Versionen, Zahlen aus dem Gespräch
- Was wurde gebaut, was wurde gelöst, was sind die nächsten Schritte
- **Niemals auf generische Aussagen abstrahieren, wenn die Spezifika vor dir liegen.** Eine «Zusammenfassung» die den realen Inhalt durch Wikipedia-Bullets ersetzt, ist ein Totalausfall.

**2. Chat-Historie durchsuchen (`conversation_search`)**
Bei Galledia-internen Themen, die nicht im aktuellen Gespräch stehen (Jenny, ASMIQ, Digital Twin, n8n, m&k, Press-Release-Pipeline, Archiv): zuerst suchen — echte Zahlen, Architektur, Status, Namen sammeln.

**3. Pflichtabfrage**
Nur wenn Kontext und Historie nichts liefern oder das Thema extern ist.

## Pflichtabfrage — IMMER vor dem Bauen

Bevor Code geschrieben wird, diese Fragen stellen — ausser sie sind bereits beantwortet oder aus der Historie bekannt:

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
    ("assets/Vorlage_6.pptx",        "assets/Vorlage_6.pptx"),
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

**body_text-Format für `add_content()` — strikte Konvention:**

Der Renderer parst das body_text-String zeilenweise und unterscheidet drei Zeilen-Typen:

| Zeile beginnt mit | Rendering |
|---|---|
| `• `, `- `, `* `, oder `· ` | **Bullet Ebene 1** — Volte 19pt Regular, schwarz, mit echtem PowerPoint-Bullet `•` |
| `•• `, `-- `, oder `·· ` (oder Einrückung + Bullet) | **Bullet Ebene 2** — Volte 17pt Regular, grau, mit `–` und Einrückung |
| Beliebiger Text **ohne** Bullet-Marker | **Zwischentitel** — Volte Semibold 22pt, schwarz, Abstand davor |
| Leerzeile | kleiner Abstand |

`**bold**`-Markdown wird automatisch gestrippt (Bold rendern wir via Schrift, nicht via Marker). Du brauchst Sterne also nicht — und falls sie reinrutschen, schaden sie nicht.

```python
# ✅ RICHTIG — alle drei Bullet-Marker funktionieren gleich:
body = """Stammdaten
• Company, Person — mit Custom-Feldern (Suchname, MwSt-Nr)
• Verlagsobjekt — Stammdaten, Rabattstaffeln, Beraterkommission

Verkauf
• Opportunity mit Angebotsnummer (Format 2026-00001)
• Angebotspaket — Bundle mit Listenpreis, Rabatt, Endpreis
"""
# «Stammdaten» und «Verkauf» werden als Zwischentitel (Semibold 22pt) gerendert,
# die `• `-Zeilen als echte Bullets (Regular 19pt).
```

```python
# ❌ FALSCH — `**bold**` ist unnötig (wird gestrippt), aber ASCII-Bullets fehlen:
body = "**Stammdaten**\nCompany, Person — ohne Marker bleibt's Semibold-Zwischentitel"
# → die zweite Zeile wird fälschlich als weiterer Zwischentitel gerendert.
```


---

## Workflow (4 Schritte)

**Pflicht vor dem ersten `build_presentation()`-Aufruf:**
Wenn Datum und/oder Rechtseinheit im Gespräch nicht bekannt sind → User fragen:
- «Für welches Datum soll die Fusszeile gesetzt werden? (Beispiel: 29. Mai 2026)»
- «Für welche Rechtseinheit? (Beispiel: Galledia Fachmedien AG)»
Erst nach Antwort fortfahren.

```python
from helpers import build_presentation, add_title, add_section, add_content
from helpers import kpi_grid, two_column, flow_pipeline, numbered_steps, add_closing

prs = build_presentation(          # Datum + Rechtseinheit IMMER setzen
    datum="29. Mai 2026",          # ← vom User bestätigt
    rechtseinheit="Galledia Fachmedien AG"  # ← vom User bestätigt
)
add_title(prs, "Titel", "Untertitel | Datum")
add_section(prs, "01", "Ausgangslage")
add_content(prs, "viel", "Kapiteltitel", "Headline", "Textkörper...", folio="3/12")
kpi_grid(prs, [("96 GB","VRAM"), ("256 GB","RAM"), ("6 TB","NVMe")])
two_column(prs, "Heute", bullets_l, "Ziel 2026", bullets_r, col2_red=True)
flow_pipeline(prs, ["Netzlaufwerk","Parsing","Vektor-DB","Antwort"])
numbered_steps(prs, [("Hardware","..."), ("Deployment","..."), ("Indizierung","...")])
add_closing(prs)                    # Schlussfolie (rotes Layout, weisses Logo)
prs.save("output.pptx")
```

**Farbrhythmus:** rote Zwischenfolien als Kapitel-Anker → helle Inhaltsfolien dazwischen.
Nie zwei Zwischenfolien hintereinander, nie alle Folien gleich.

---

## Layout-Entscheidungstabelle (Vorlage_6)

| Inhaltstyp | Layout-Name | Platzhalter |
|---|---|---|
| Deck-Titel | `Titelfolie` | idx=0 Titel, idx=10 Untertitel |
| Kapitel-Anker / Abschnitt | `2_Zwischenfolie rot` | keine — Textbox manuell |
| Agenda wenig (≤5 Punkte) | `01_Agenda 5` | idx=0 Label, idx=11 leer, idx=13 Punkte, idx=14 Folio |
| Agenda viel (6–12 Punkte) | `01_Agenda 22` | idx=0 Label, idx=11 leer, idx=13 Punkte, idx=14 Folio |
| Grosse Aussage / Kernbotschaft | `02_wenigText` | idx=0 Kapiteltitel, idx=11 Headline 72pt, idx=13 Lead, idx=14 Folio, idx=15 Quelle |
| Detail / Text / Struktur | `04_vielText` | idx=0 Kapiteltitel, idx=11 Headline, idx=13 Textkörper, idx=14 Folio, idx=15 Quelle |
| KPI, Zweispalter, Pipeline, Timeline | `Leer` | idx=0/11/13 leer lassen, idx=14 Folio — Shapes via helpers.py |
| Diskussion / Interaktion | `Abschlussfolie` | keine — zeigt Piktogramm + «Diskussion» |
| Piktogramm-Referenz | `Piktogramme` | idx=0 Titel |
| Schluss-/Abschlussfolie | `Schlussfolie` | keine — zeigt weisses Logo auf Rot |

**Hinweis `Leer`:** Im Bearbeitungsmodus zeigt das Layout leere Platzhalter-Rahmen
(Bekanntes Problem aus Vorlage_6). In Render + Präsentation unsichtbar. Kein Blocker.

---

## CI-Farb-Tokens (aus Template-Theme — verbindlich)

```python
# helpers.py exportiert diese als Konstanten
RED   = RGBColor(0xE6, 0x1C, 0x52)   # Galledia-Rot  — Primärfarbe
BLACK = RGBColor(0x00, 0x00, 0x00)   # Galledia-Schwarz
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
G1    = RGBColor(0x40, 0x40, 0x40)   # Grau 1 (64/64/64)
G2    = RGBColor(0x66, 0x66, 0x66)   # Grau 2 (102/102/102)
G3    = RGBColor(0xA6, 0xA6, 0xA6)   # Grau 3
G4    = RGBColor(0xD9, 0xD9, 0xD9)   # Grau 4
GL    = RGBColor(0xF2, 0xF2, 0xF5)   # Hintergrundgrau (Karten)
TURK  = RGBColor(0x22, 0xAA, 0x9F)   # Türkis — NUR Info-/Quote-Panels
```

**Gewichtung:** dominant Rot/Schwarz/Grau. Türkis, Purple, Blau, Bronze NUR für Infografiken
und Akzente — nie als Hauptfarbe.

---

## CI-Schrift-Tokens

| Verwendung | Font-Name |
|---|---|
| Plakative Titel / Headlines | `Volte Rounded Semibold` |
| Fliesstext / Lead / Labels | `Volte` |
| Zwischentitel / Hervorhebung | `Volte Semibold` |
| Italic (Hervorhebung im Text) | `Volte` + italic=True |

Ausrichtung: **linksbündig** auf Inhaltsfolien. **Zentriert** nur auf Titelfolie/Cover.
Body-Text grundsätzlich in Schwarz.

---

## CI-Mikroregeln (verbindlich)

- **Logo:** nur Rot, Weiss oder Schwarz. Nie mit Box/Umform auf Bildern. Nie verzerren.
  Schutzzone wahren. Unter 8 mm Breite → nur Bildmarke (G), ohne Schriftzug.
  **Farbwahl:** Rot-Logo auf weissem/hellem Hintergrund · Weiss-Logo auf rotem/dunklem Hintergrund · Schwarz-Logo auf hellem Hintergrund (alternative zu Rot).
  **Skill-Funktion:** `add_logo(slide, variant='rot')` bzw. `variant='weiss'` — platziert Bildmarke rechts unten.
- **Bullets:** Aufzählungszeichen `•` (Punkt). Zitate in Guillemets `« »`. Separator `|`.
- **Formen:** Kästen und Linien immer mit abgerundeten Ecken (Motiv konsistent).
- **Bildwelt:** authentische Menschen «wie du und ich», warmes weiches Licht, erdige Töne,
  partielle Highlights in Galledia-Rot. Keine offensichtlichen Stock-Models.
- **Piktogramme:** plakativ (gross/dominant) oder informativ (klein). In Schwarz/Weiss/Rot
  oder Akzentfarbe. Piktogramme NICHT mit dem Galledia-Alphabet mischen.
- **Fusszeile (idx=14):** Format `«n / total»` z.B. `«3 / 12»`. Auf Titelfolie und
  Schlussfolie weglassen.
- **Quellenangabe (idx=15):** nur setzen wenn Quellen vorhanden. Format:
  `Quelle: [Quelle 1] / [Quelle 2, Jahr]`.

---

## Anti-Bleiwüste (Pflichtprüfung pro Folie)

- Jede Folie hat ≥1 visuelles Element (Bild, Piktogramm, grosse Zahl, Diagramm, Farbfläche).
- Max. 6 Zeilen / 3 Bullets pro Folie — sonst splitten.
- Kennzahlen als KPI-Callout (Zahl 52–72 pt, Label klein darunter) statt im Fliesstext.
- Vergleich/Prozess/Timeline als Shapes statt als Bullet-Liste.
- Roter Farbrhythmus einhalten (mindestens jede 3.–4. Folie ein Rot-Anker).
- KEINE Akzentlinien unter Titeln. KEINE dekorativen Vollbalken. Vollflächige rote
  Cover/Zwischenfolien sind dagegen CI-Signatur und ausdrücklich erwünscht.

---

## Quellenangabe und Fusszeile setzen

```python
# In native Layouts (04_vielText, 02_wenigText):
ph[14].text = "«5 / 12»"                                        # Folienzahl
ph[15].text = "Quelle: Gartner 2025 / Schätzung Galledia F&E"  # optional

# Auf Leer (via helpers.add_footer):
add_footer(slide, folio="5 / 12", source="Gartner 2025")
```

---

## QA (verbindlich vor Abgabe)

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
rm -f slide-*.jpg && pdftoppm -jpeg -r 120 output.pdf slide
```

Subagent-Inspektion: Textüberlauf, Kontrast, Überlappung, Schriftsubstitution, Platzhalter-Reste.

```bash
extract-text output.pptx | grep -iE "xxx|lorem|Mastertitel|Kapiteltitel 30pt|Themenpunkt"
```

---

## Erweiterung: Word-Vorlagen (Phase 2)

Brief, Kurzbrief und Dokument folgen in einer zweiten Skill-Sektion (`## Word-Vorlagen`).
Selbe CI-Tokens, selbe Fonts, python-docx als Builder. Sobald Word-Templates geliefert werden.
