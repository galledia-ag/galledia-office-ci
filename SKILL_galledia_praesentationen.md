---
name: Galledia-Praesentationen
description: >
  Erstellt CI-konforme Galledia-PowerPoint-Präsentationen (.pptx) via Code Execution.
  Auslöser: «Präsentation», «Deck», «Slides», «PowerPoint», «.pptx», «Foliensatz»,
  «Pitch», «GL-Präsentation», «Kundenpräsentation», «fasse … als Präsentation zusammen».
  Markenhandbuch v1.5, Vorlage_5, Volte-Schriften, Galledia-Rot #E61C52, Logos.
  NUR für Präsentationen — Brief/Kurzbrief/Dokument laufen über einen separaten Skill.
version: "1.0"
---

# Galledia Präsentationen

CI-konforme PowerPoint via Code Execution. **Es gibt KEIN Präsentations-Tool.**
Niemals `tool_search` oder `generate_galledia_praesentation` aufrufen — diese existieren nicht
bzw. sind deprecated. Der gesamte Ablauf ist Python-Code im `bash_tool`.

---

## Ablauf in 3 Schritten

### Schritt 1 — Inhalt klären (VOR dem Code)

Eine Präsentation ist nur so gut wie ihr Inhalt. Inhaltsquellen in dieser Reihenfolge:

1. **Aktueller Gesprächs-/Projektkontext** — Wenn um eine Zusammenfassung dieses Projekts/Gesprächs
   gebeten wird, ist der Inhalt bereits da. Die TATSÄCHLICHEN Fakten, Zahlen, Entscheidungen
   verwenden — niemals auf generische Aussagen abstrahieren.
2. **Chat-Historie** (`conversation_search`) — Bei Galledia-internen Themen (Jenny, ASMIQ,
   Digital Twin, n8n, m&k, Press-Release-Pipeline, Mediaberatung) zuerst die echten Details
   holen: Zahlen, Architektur, Status, Namen.
3. **Pflichtabfrage** — Nur wenn Kontext und Historie nichts liefern. Dann fragen:
   Datum + Rechtseinheit, Kernbotschaft, Zielgruppe, 3 wichtigste Fakten/Zahlen, Storyline.
   Bei «mir egal» → plausiblen Inhalt erfinden, aber mit denselben Qualitätsprinzipien.

**Niemals generische Wikipedia-Bullets, wenn echte Daten verfügbar sind.**

### Schritt 2 — Setup (immer zuerst ausführen)

```bash
python3 << 'PYEOF'
import os, sys, urllib.request
D = "/tmp/galledia_praes"; os.makedirs(f"{D}/assets/logo", exist_ok=True)
B = "https://raw.githubusercontent.com/galledia-ag/galledia-office-ci/main/skills/galledia-praesentation"
for n, u in [("helpers.py","helpers.py"),
             ("assets/Vorlage_5.pptx","assets/Vorlage_5.pptx"),
             ("assets/logo/logo_rot.png","assets/logo/logo_rot.png"),
             ("assets/logo/logo_weiss.png","assets/logo/logo_weiss.png"),
             ("assets/logo/logo_schwarz.png","assets/logo/logo_schwarz.png")]:
    d = f"{D}/{n}"
    if not os.path.exists(d):
        urllib.request.urlretrieve(f"{B}/{u}", d)
        print(f"OK {n} ({os.path.getsize(d):,})")
print("Setup fertig")
PYEOF
```

```bash
pip install python-pptx Pillow --break-system-packages -q
```

### Schritt 3 — Präsentation bauen

```bash
cat > /tmp/build.py << 'PYEOF'
import sys; sys.path.insert(0, "/tmp/galledia_praes")
from helpers import *

prs = build_presentation(datum="29. Mai 2026", rechtseinheit="Galledia Fachmedien AG")
# ... Folien hier ...
prs.save("/mnt/user-data/outputs/Praesentation.pptx")
print("gespeichert")
PYEOF
python3 /tmp/build.py
```

Danach die Datei mit `present_files` zeigen.

---

## Funktionen (alle aus helpers.py)

| Funktion | Zweck |
|---|---|
| `build_presentation(datum, rechtseinheit)` | Initialisiert Deck mit Fusszeile |
| `add_title(prs, titel, untertitel)` | Titelfolie (Kernbotschaft in den Untertitel) |
| `add_agenda(prs, [punkte], folio)` | Agenda — 1 Zeile pro Punkt |
| `add_content(prs, "viel", kapitel, headline, body, folio)` | Inhaltsfolie mit dichtem Text |
| `kpi_grid(prs, [(zahl,label),...], kicker, headline, folio)` | 2–4 Zahlen-Callouts |
| `two_column(prs, head_l, [items], head_r, [items], kicker, headline, col2_red, folio)` | Vergleich |
| `flow_pipeline(prs, [(titel,sub),...], kicker, headline, folio)` | Prozess/Pipeline |
| `numbered_steps(prs, [(titel,beschr),...], kicker, headline, folio)` | Nummerierte Schritte |
| `timeline(prs, [(titel,beschr),...], kicker, headline, folio)` | Zeitstrahl |
| `add_section(prs, "01", titel)` | Roter Kapitel-Anker (nur Decks >15 Folien) |
| `add_discussion(prs)` / `add_closing(prs)` | Diskussions- / Schlussfolie |

`kicker` + `headline` sind bei kpi_grid/two_column/flow_pipeline/numbered_steps/timeline **Pflicht** —
sonst bleibt der Seitenkopf leer.

## body_text-Format (add_content)

```
Zwischentitel ohne Präfix          → Volte Semibold, fett, mit Abstand davor
· Text mit Punkt-Präfix            → Ebene-1-Bullet (•, schwarz)
·· Text mit Doppelpunkt-Präfix     → Ebene-2-Bullet (–, grau, eingerückt)
Leerzeile                          → Abstand
```

helpers.py rendert diese automatisch als echte PowerPoint-Bullets — kein manuelles `•` setzen.

## Qualitätsprinzipien (verbindlich)

**Headline = Aussage, nicht Thema — UND max. 32 Zeichen:**
```
❌ «KI-Anwendungen»                    → Thema, keine Aussage
❌ «Der Verlags-Manager am Lebensende» → 34 Zeichen, zu lang → Fehler
✅ «KI spart 3'900 h/Monat»            → Aussage, 22 Zeichen
```
Headline max. **32 Zeichen**, Kapiteltitel max. **35 Zeichen** — sonst bricht der Build
mit einem klaren Fehler ab (CI: 72pt bzw. 30pt müssen auf eine Zeile passen).
Das zwingt zu knackigen Titeln. Lieber die Aussage in den Body als in eine lange Headline.

**Zahlen statt Adjektive:** «39% weniger Aufwand», nicht «signifikante Steigerung».

**Inhaltsdichte:** Lieber 10–15 Zeilen auf einer `add_content("viel")`-Folie als auf mehrere
dünne Folien verteilen. Pro Inhaltsfolie 2–3 Zwischentitel mit je 2–4 Bullets.

**Layout-Wahl — HARTE REGEL:**

`add_content` (einspaltig) ist der **Standard**. Spezial-Layouts sind die **Ausnahme** und
nur erlaubt, wenn ihre Bedingung **vollständig** erfüllt ist:

```
add_content("viel")  → STANDARD. Immer wählen, ausser eine der Bedingungen unten greift klar.
add_content("wenig") → wenig Text, eine Kernaussage (≤ 4 Bullets, kein Vergleich)

kpi_grid     → NUR bei 2–4 echten Zahlen/Metriken (z.B. «4'800», «CHF 1'140»)
two_column   → NUR echter Vergleich MIT mindestens 3 substantiellen Punkten PRO Spalte
flow_pipeline→ NUR ein Prozess mit 3–5 Schritten (A → B → C)
timeline     → NUR Phasen über Zeit (Q1 → Q2 → Q3)
numbered_steps→ NUR nummerierte Handlungsschritte (2–4 Schritte)
```

**Verboten:**
```
❌ two_column mit < 3 Punkten pro Spalte  → stattdessen add_content
❌ two_column für «wenig Text»            → stattdessen add_content
❌ kpi_grid ohne echte Zahlen             → stattdessen add_content
```

**Im Zweifel immer `add_content`.** Lieber eine dichte einspaltige Folie als ein
halbleeres Spezial-Layout. Wenig Text heisst NIE zweispaltig.

**Kapiteltitel beschreibend:** «Ausgangslage», «Resultate» — nie «01», «02».

**Typische Struktur:** Titel → Agenda → Ausgangslage/Problem → Lösung (visuell) →
Beweis/Zahlen → Nächste Schritte → Schluss.

## CI-Regeln

- Schrift: Volte (Text/Kapiteltitel), Volte Semibold (Headlines). Kein Volte Rounded im Inhalt.
- Keine Versalien. Keine Folienübergänge.
- Farben: Galledia-Rot #E61C52, Schwarz, Grau #404040/#666666, Hellgrau #F2F2F5.
- Fusszeile immer via `build_presentation(datum=..., rechtseinheit=...)` setzen.
- Schweizer Hochdeutsch (kein ß).

---

## Vollständiges Beispiel

```python
import sys; sys.path.insert(0, "/tmp/galledia_praes")
from helpers import *

prs = build_presentation(datum="29. Mai 2026", rechtseinheit="Galledia Fachmedien AG")

add_title(prs, "KI in den Fachmedien",
          "Wie Automatisierung 3'900 Stunden pro Monat freisetzt")

add_agenda(prs, ["Ausgangslage", "Lösung", "Resultate", "Nächste Schritte"], folio="2")

add_content(prs, "viel", "Ausgangslage", "60% der Zeit floss in Routine",
    "Wo die Zeit verloren ging\n"
    "· Lead-Recherche: täglich 2 Stunden pro Berater\n"
    "·· manuell über Google und Branchenverzeichnisse\n"
    "· Angebotserstellung: Tage statt Minuten\n"
    "· Nachfassen: ohne System, oft vergessen\n"
    "\n"
    "Was das kostete\n"
    "· 60% der Vertriebszeit ohne Kundenkontakt\n"
    "· Verlorene Abschlüsse durch späte Reaktion", folio="3")

flow_pipeline(prs, [("Apollo","Lead-Quelle"), ("Claude","Anschreiben"),
                    ("n8n","Versand"), ("CRM","Tracking")],
              kicker="Lösung", headline="Die ASMIQ-Pipeline", folio="4")

kpi_grid(prs, [("4'800","Leads"), ("CHF 1'140","ARPU"), ("3'900 h","gespart/Monat")],
         kicker="Resultate", headline="Messbare Wirkung seit Januar 2026", folio="5")

numbered_steps(prs, [("Voice Agent","Mehrsprachige Qualifizierung"),
                     ("Archiv-Portal","3 Mio. Artikel als B2B-Angebot")],
               kicker="Ausblick", headline="Nächste Schritte 2026", folio="6")

add_closing(prs)
prs.save("/mnt/user-data/outputs/KI_Fachmedien.pptx")
print("gespeichert")
```
