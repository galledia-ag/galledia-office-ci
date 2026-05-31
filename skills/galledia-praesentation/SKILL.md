---
name: galledia-praesentation
description: >
  Erstellt und bearbeitet PowerPoint-Präsentationen im Galledia Corporate Design.
  Verwenden wenn: ein Deck, Slides oder .pptx für Galledia / Galledia Fachmedien / ZSW
  erstellt, gefüllt oder überarbeitet werden soll. Liefert CI-Mechanik (Layouts, Farben,
  Schriften, Regeln) — nicht den Inhalt.
version: "0.0.6"
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

## Goldene Regel: dichte Folien, klarer Rahmen

Markenwerte: einfach — persönlich — wirkungsvoll. "Einfach" heisst **eine Aussage pro Folie**, nicht **eine Zeile pro Folie**. Jede Folie muss sich beim Vorbeiscrollen wie eine vollständige, abgeschlossene Mini-Story lesen — Headline + Beweis + Detail. Eine Folie mit nur 2 Bullets wirkt unfertig und ist ein Qualitätsfehler.

**Dichte-Soll (verbindlich):**
- Inhaltsfolien (`04_vielText`, `kpi_grid`, `two_column`, `flow_pipeline`, `timeline`, `numbered_steps`): **3–5 Bullets ODER 3–4 KPIs ODER 4–6 Pipeline-Knoten** + Headline + Kapiteltitel + idealerweise Sub-Bullets / Zwischentitel im Body.
- Aussage-Folien (`02_wenigText`): bewusst reduziert — Headline gross + 1–2 Lead-Sätze. NUR für Kernbotschaften, Zwischenfazits, emotionale Anker. Maximal **jede 4. Folie**.
- Titel/Section/Closing: Strukturelemente, zählen nicht zur Dichte-Rechnung.

**Default-Variante = `viel`.** `wenig` ist die Ausnahme, nicht die Regel.

**Treatment nach Inhalt (Markenhandbuch S. 42):**
- informativ / sachlich / Analyse / Status / Roadmap → `04_vielText`, `kpi_grid`, `two_column`, `flow_pipeline`, `timeline`, `numbered_steps` — **das ist der Default**
- emotional / plakativ / Kernbotschaft → `02_wenigText`, Titelfolie, Zwischenfolie — sparsam einsetzen
- Niemals alle Folien gleich. Mindestens 3 verschiedene Layouts pro Deck.

Whitespace ist gestaltet, nicht leer. Leere Bullet-Slots sind kein Whitespace, sondern eine Lücke.

---

## Mindestumfang & Layout-Mix (verbindlich)

**Folienzahl-Untergrenzen:**

| Thema | Min. Folien | Typische Spanne |
|---|---|---|
| Trivial (1 Aussage, internes Statement) | 5 | 5–7 |
| Standard-Update / Statusbericht | 12 | 12–16 |
| Konzept / Strategie / Roadmap | 15 | 15–22 |
| Pitch / Investor / Kunden-Präsi | 16 | 16–25 |

**Pro Hauptkapitel mindestens 2 Inhaltsfolien** (nicht eine Zwischenfolie + eine Inhaltsfolie — das ist zu dünn). Wenn ein Kapitel nur eine Inhaltsfolie hergibt, ist es kein eigenes Kapitel.

**Pflicht-Layout-Mix pro Deck (ab 10 Folien):**
- mindestens **1× `kpi_grid`** (Zahlen kommen IMMER vor, auch in "weichen" Themen — Zeitpunkte, Anzahl Beteiligter, Budget, Termine)
- mindestens **1× `two_column`** (Vergleich Heute/Ziel, Vorher/Nachher, Wir/Sie, Risiko/Chance)
- mindestens **1× `flow_pipeline` ODER `numbered_steps` ODER `timeline`** (Prozess oder Abfolge)
- maximal **60% der Folien dürfen `add_content` sein** — sonst Bleiwüste
- maximal **25% der Folien dürfen `add_content(..., 'wenig', ...)` sein** — sonst Luftnummer

Wenn ein Deck nur `add_content`-Folien hat: **STOP**, Layout-Mix einplanen.

---

## Inhalt zuerst — die wichtigste Regel

Eine Präsentation ist nur so gut wie ihr Inhalt. Eine "mager wirkende" Präsentation hat fast immer eine Inhalts-Ursache, keine Layout-Ursache. Reihenfolge der Inhaltsquellen:

**1. Aktueller Gesprächs-/Projektkontext (höchste Priorität)**
Wenn der Nutzer um eine **Zusammenfassung dieses Projekts / Gesprächs** bittet, ist der Inhalt bereits da — im aktuellen Gespräch und im Projekt-Wissen. Diesen TATSÄCHLICHEN Inhalt zusammenfassen:
- Konkrete Entscheidungen, Schritte, Resultate, Versionen, Zahlen aus dem Gespräch
- Was wurde gebaut, was wurde gelöst, was sind die nächsten Schritte
- Namen, Daten, Versionen, Beträge AKTIV extrahieren — nicht weglassen, weil sie "zu detailliert" wirken
- **Niemals auf generische Aussagen abstrahieren, wenn die Spezifika vor dir liegen.** Eine «Zusammenfassung» die den realen Inhalt durch Wikipedia-Bullets ersetzt, ist ein Totalausfall.

**2. Chat-Historie aktiv durchsuchen (`conversation_search`)**
Bei Galledia-internen Themen, die nicht im aktuellen Gespräch stehen (Jenny, ASMIQ, Digital Twin, n8n, m&k, Press-Release-Pipeline, Archiv): zuerst suchen — echte Zahlen, Architektur, Status, Namen sammeln. **Mehrere Suchen** mit verschiedenen Begriffen, nicht nur eine. Ziel: 10–20 echte Fakten zum Thema.

**3. Projekt-Wissen / Memory durchforsten**
`memory/`-Dateien und CLAUDE.md auf Themen-relevante Einträge prüfen.

**4. Pflichtabfrage**
Nur wenn 1–3 nichts liefern oder das Thema extern ist.

**Inhalts-Tiefe-Test vor dem Bauen:**
Kannst du für jedes geplante Kapitel mindestens 3–4 spezifische Fakten (Zahl, Name, Datum, Betrag, konkrete Entscheidung) nennen? Wenn nein → zurück zu Quelle 1–3, mehr Material sammeln. Niemals mit zu wenig Material in den Build gehen — das produziert exakt die magere Optik, die zu vermeiden ist.

## Pflichtabfrage — IMMER vor dem Bauen

Bevor Code geschrieben wird, diese Fragen stellen — ausser sie sind bereits beantwortet oder aus Gespräch/Historie bekannt:

1. **Datum + Rechtseinheit** (Fusszeile)
2. **Kernbotschaft** — Was soll die Zielgruppe nach der Präsentation denken/tun/entscheiden? (1 Satz)
3. **Zielgruppe + Anlass** — GL-Sitzung, Kundenpräsi, Investor, internes Team? Wie viel wissen sie schon?
4. **Storyline / Kapitelstruktur** — 3–6 Hauptkapitel, je mit Kapiteltitel
5. **Mindestens 8–12 konkrete Fakten/Zahlen/Namen/Zeiträume/Beträge** — das Rohmaterial. Bei <10 Folien reichen 6, bei 15+ Folien sind 12–20 nötig. Beispiele: «3'900h/Monat», «Q3 2026», «Jenny Hostettler», «96 GB VRAM», «CHF 240k», «5 Verlagsobjekte». **Ohne dieses Material wird das Deck generisch.**
6. **Erwarteter Umfang** — wenn der User keine Zahl nennt, vorschlagen nach Tabelle in Abschnitt "Mindestumfang" (Default: 15 Folien für Standard-Themen).

**Wenn der User sagt «mir egal», «nur ein Test», «füll selbst»:** akzeptieren, ABER:
- Chat-Historie + Projekt-Wissen aktiv durchsuchen (`conversation_search`) nach echten Galledia-Fakten zum Thema
- Plausibel-aber-spezifisch erfinden — niemals «Vorteile», «Mehrwert», «Synergien», «Effizienzsteigerung» ohne Zahl dahinter
- Mindest-Folienzahl und Layout-Mix trotzdem einhalten

**Wenn der User explizit «kurzes Deck» / «Übersicht» / «5 Folien» sagt:** seine Vorgabe gilt, Mindestumfang-Tabelle wird übersteuert.


## Qualitätsprinzipien (verbindlich)

Claude leitet den Nutzer zu professionellen, **dicht befüllten** Folien — nicht zu formatierten Aufzählungen, aber auch nicht zu Luft-Folien.

**Pyramid Principle — jede Folie hat eine Hauptaussage:**
```
❌ Titel: «KI-Anwendungen»  (Thema, keine Aussage)
✅ Titel: «KI spart 3'900 Stunden pro Monat»  (Aussage mit Beweis)
```

**Zahlen statt Adjektive — generische Begriffe sind verboten:**
```
❌ «Signifikante Effizienzsteigerung»
❌ «Vorteile», «Mehrwert», «Synergien», «Best Practices», «Optimierung», «Transformation» — als Standalone-Bullet
✅ «39% weniger manuelle Arbeit — 3'900h/Monat»
✅ «Jenny Hostettler übernimmt Q3 2026 die ASMIQ-Pipeline»
```
Wenn ein Bullet ohne Zahl/Name/Datum/Betrag auskommt, gehört er meistens nicht aufs Slide. Ausnahme: Storyline-Anker und Zwischentitel.

**Inhaltsdichte pro Folie (verbindlich):**
```
❌ Folie mit nur Headline + 2 Bullets  → wirkt leer, Qualitätsfehler
✅ Headline + Kapiteltitel + 3–5 Bullets + ggf. Sub-Bullets / Zwischentitel
✅ Headline + 3–4 KPI-Callouts mit Zahl + Label
✅ Headline + 2 Spalten à 3–4 Bullets
✅ Headline + 4–6 Pipeline-Knoten
```

**Sub-Bullets aktiv nutzen** — verdoppeln die Informationsdichte ohne neue Folie:
```
• Stammdaten ASMIQ
•• Company, Person mit Custom-Feldern (Suchname, MwSt-Nr)
•• 5 Verlagsobjekte mit Rabattstaffeln und Beraterkommission
• Opportunity-Pipeline
•• Angebotsnummern Format 2026-00001
•• Bundle-Pakete mit Listenpreis, Rabatt, Endpreis
```

**Visuelle Beweise statt Bullet-Listen — bei jeder passenden Gelegenheit:**
```
→ Zahlen → kpi_grid()
→ Vergleich → two_column()
→ Prozess → flow_pipeline() / numbered_steps()
→ Zeitverlauf → timeline()
→ Statement → image_bleed() oder add_content('wenig', ...)
```

**Eine Aussage pro Folie — aber mit Beweis:**
Die Aussage steht in der Headline. Die 3–5 Bullets / KPIs / Schritte sind der BEWEIS dafür, nicht weitere Aussagen. So entstehen dichte Folien mit klarer Hierarchie statt 6 gleichrangige Bullets.

**Roter Faden — typische Struktur für 15-Folien-Deck:**
```
Folie 1:  Titel (Thema + Kernbotschaft im Untertitel)
Folie 2:  Agenda (4–6 Kapitel)
Folie 3:  Zwischenfolie Kapitel 1 — Ausgangslage
Folie 4:  Ausgangslage / Status quo (add_content viel, 4 Bullets mit Zahlen)
Folie 5:  KPI-Grid mit 3–4 Schlüsselzahlen
Folie 6:  Zwischenfolie Kapitel 2 — Problem
Folie 7:  Problem-Analyse (two_column Heute/Lücke)
Folie 8:  Wirkung des Problems (add_content viel mit Sub-Bullets)
Folie 9:  Zwischenfolie Kapitel 3 — Lösung
Folie 10: Lösungskonzept (flow_pipeline 4–5 Knoten)
Folie 11: Lösungsdetail (add_content viel)
Folie 12: Zwischenfolie Kapitel 4 — Umsetzung
Folie 13: Roadmap (timeline mit 4–5 Phasen)
Folie 14: Nächste Schritte (numbered_steps mit 3–4 Schritten)
Folie 15: Schlussfolie
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
_FILES = [
    "helpers.py",
    "assets/Vorlage_6.pptx",
    "assets/logo/logo_rot.png",
    "assets/logo/logo_rot_schriftzug.png",
    "assets/logo/logo_weiss.png",
    "assets/logo/logo_weiss_schriftzug.png",
    "assets/logo/logo_schwarz.png",
    "assets/logo/logo_schwarz_schriftzug.png",
]
for _name in _FILES:
    _dest = f"{_DIR}/{_name}"
    if not os.path.exists(_dest):
        try:
            urllib.request.urlretrieve(f"{_BASE}/{_name}", _dest)
            print(f"✓ {_name} ({os.path.getsize(_dest):,} bytes)")
        except Exception as e:
            # HARD-STOP: Niemals from-scratch improvisieren ohne CI-Assets.
            raise RuntimeError(
                f"Asset-Download fehlgeschlagen ({_name}): {e}. "
                f"Plugin/Repo nicht erreichbar — Skill abbrechen und Asset-Fehler "
                f"an User melden. NIEMALS mit python-pptx ohne Vorlage_6/Volte/"
                f"Logos eine 'Galledia'-Präsentation bauen (CI-Verstoss garantiert)."
            )

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
add_content(prs, "viel", "KI-Trends", "Headline max. 32 Zeichen", "Text", folio="3")
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

**Längen-Limits (HART, vom Code erzwungen):**

| Parameter | Max-Zeichen | Wo |
|---|---|---|
| `headline` (Argument zu `add_content` / `kpi_grid` / `two_column` etc.) | **32** | bei 72pt auf 1 Zeile |
| `kicker` / `kapitel` (Kapiteltitel-Argument, immer als 2. Positional) | **35** | bei 30pt auf 1 Zeile |
| `title` von `add_title()` | **40** für 1-Zeilen-Optik (≤40 = 1 Zeile, >40 = 2 Zeilen) |
| Agenda-Items | **~55** je Punkt, 1 Zeile |

⚠️ **Wichtig für LLM-Generierung:** Plane Headlines von Anfang an **knackig und unter 32 Zeichen**. Der Code raised ValueError bei Überschreitung — du musst sonst die ganze Präsentation neu generieren.

```python
# ❌ FALSCH — 37 Zeichen, ValueError
kpi_grid(prs, kpis, headline="Start ins neue Geschäftsjahr gelungen", ...)
# ✅ RICHTIG — 22 Zeichen
kpi_grid(prs, kpis, headline="Gelungener Jahresstart", ...)

# ❌ FALSCH — 34 Zeichen
two_column(prs, ..., headline="Turnaround Print — vier Baustellen", ...)
# ✅ RICHTIG — 27 Zeichen
two_column(prs, ..., headline="Print dreht — vier Baustellen", ...)
```

**Tipp für knackige Headlines:** Aussage statt Beschreibung, Verben statt Substantive, weglassen statt erklären.

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

## Anti-Bleiwüste UND Anti-Luftnummer (Pflichtprüfung pro Folie)

Beide Extreme sind Fehler. Pro Folie prüfen:

**Gegen Bleiwüste:**
- Jede Folie hat ≥1 visuelles Element (Bild, Piktogramm, grosse Zahl, Diagramm, Farbfläche, Pipeline-Shapes).
- Max. **8 Zeilen** Body-Text (inkl. Sub-Bullets) — bei mehr splitten.
- Max. **5 Top-Level-Bullets** — sonst splitten oder in `two_column`.
- Vergleich/Prozess/Timeline als Shapes statt als Bullet-Liste.

**Gegen Luftnummer:**
- Min. **3 Bullets ODER 3 KPIs ODER 4 Pipeline-Knoten** auf Inhaltsfolien — bei weniger entweder dichter füllen oder mit Nachbarfolie zusammenlegen.
- Min. **eine konkrete Zahl/Name/Datum** auf jeder Sach-Inhaltsfolie (Ausnahmen: Section, Closing, bewusste Aussage-Folie mit `02_wenigText`).
- KEIN Bullet, der nur aus generischen Begriffen besteht (`Vorteile`, `Effizienz`, `Mehrwert`, `Synergien`, `Optimierung`, `Best Practices`, `Skalierung` ohne Kontext).
- KEIN Kapitel mit nur 1 Inhaltsfolie nach der Zwischenfolie — dann ist es kein Kapitel.

**Rhythmus:**
- Roter Farbrhythmus: mindestens jede 3.–4. Folie ein Rot-Anker (Zwischenfolie oder rote Akzentfolie).
- Layout-Rhythmus: in 10 aufeinanderfolgenden Inhaltsfolien max. 6× `add_content` — Rest aus `kpi_grid` / `two_column` / `flow_pipeline` / `timeline` / `numbered_steps` / `image_bleed`.
- KEINE Akzentlinien unter Titeln. KEINE dekorativen Vollbalken. Vollflächige rote Cover/Zwischenfolien sind dagegen CI-Signatur und ausdrücklich erwünscht.

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
