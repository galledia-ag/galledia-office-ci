---
name: galledia-praesentation
description: >
  Erstellt und bearbeitet PowerPoint-Präsentationen im Galledia Corporate Design.
  Verwenden wenn: ein Deck, Slides oder .pptx für Galledia / Galledia Fachmedien / ZSW
  erstellt, gefüllt oder überarbeitet werden soll. Liefert CI-Mechanik (Layouts, Farben,
  Schriften, Regeln) — nicht den Inhalt.
version: "1.0"
template: assets/Vorlage_5.pptx
---

# Galledia-Präsentation

## Zweck
Ansprechende, abwechslungsreiche Decks im Galledia-CI. CI = Rahmen (Farben, Schrift, Logo,
Layouts). Gestaltung = freie Komposition INNERHALB dieses Rahmens. Niemals ein Einheits-Layout.

---

## Voraussetzungen

| Asset | Pfad | Status |
|---|---|---|
| Template | `assets/Vorlage_5.pptx` | ✅ bereit |
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

## Layout-Entscheidungstabelle (Vorlage_5)

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
(Bekanntes Problem aus Vorlage_5). In Render + Präsentation unsichtbar. Kein Blocker.

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
