---
name: galledia-praesentation
description: >
  Erstellt eine Galledia-Praesentation (PowerPoint, .pptx) im Galledia-CI/CD
  (Markenhandbuch v1.5). Verwende diesen Skill immer wenn ein User eine
  Praesentation, Slides, ein Pitch-Deck, eine Kundenpraesentation oder einen
  Foliensatz im Galledia-Design erstellen will. Triggert auf: "Praesentation",
  "Foliensatz", "Slides", "Pitch", "Pitch-Deck", "Foliendeck",
  "Kundenpraesentation", "PowerPoint", "PPT", "Vortrag", "Praesentationsdeck".
  Liefert eine .pptx mit Galledia-Layouts (Titel rot/tuerkis/bronze/purple/lila,
  Agenda, Inhalt, Zwischenfolie) und der korrekten Galledia-Typografie
  (Volte/Volte Rounded). Arbeitssprache: Schweizer Hochdeutsch (ss statt ss).
---

# Galledia Praesentation

Du erstellst CI/CD-konforme PowerPoint-Praesentationen. Die Vorlage
(`templates/Präsentationsvorlage Galledia.potx`) liefert 16 Slide-Layouts
in Galledia-CI mit korrekten Farben, Schriften (Volte/Volte Rounded) und
dem Galledia-G als Watermark. Das Skript `scripts/fill_praesentation.py`
befuellt die Slides programmatisch.

## Workflow

1. **Daten sammeln**: User fragt nach Praesentation. Frage gezielt nach
   - Anzahl/Reihenfolge der Folien
   - Titel, Untertitel, Inhalt je Folie
   - Ziel-Organisation (default: Galledia Fachmedien AG)
2. **Slide-Struktur planen** (siehe Layout-Optionen unten)
3. **Generieren** via `fill_praesentation.py`
4. **.pptx liefern**: User kann in PowerPoint weiter feinarbeiten

## Verfuegbare Slide-Layouts

| Key | Was | Wann verwenden |
|---|---|---|
| `title`, `title_red` | Titelfolie rot (Vollflaeche Rot, Titel + Untertitel) | Eroeffnungsfolie |
| `title_turquoise`, `title_bronze`, `title_purple`, `title_lila` | Andere Akzentfarben | Variation/Kapiteltitel |
| `section`, `section_red` | Zwischenfolie rot (Kapiteltrenner) | Zwischen Sektionen |
| `section_turquoise` etc. | Zwischenfolien in anderen Farben | |
| `agenda` | 01_Agenda 5 (klassische Agenda) | Inhaltsuebersicht |
| `agenda_22` | 01_Agenda 22 (Variante) | |
| `content` | 02_wenigText (Standard-Inhaltsfolie) | Hauptinhalte |
| `content_long` | 04_vielText (mehr Platz fuer Text) | Detailfolien |
| `default` | DEFAULT SLIDE | Generischer Inhalt |
| `blank` | Leere Folie | Custom-Inhalt |

## JSON-Schema

```json
{
  "organisation": "Galledia Fachmedien AG",
  "slides": [
    {
      "layout": "title",
      "title": "Hauptueberschrift",
      "subtitle": "Untertitel oder Kunde | Datum"
    },
    {
      "layout": "agenda",
      "title": "Übersicht der Themen",
      "items": ["Punkt 1", "Punkt 2", "Punkt 3"]
    },
    {
      "layout": "content",
      "title": "Folientitel",
      "content": "Zeile 1\nZeile 2\n· Bullet 1\n· Bullet 2"
    },
    {
      "layout": "section",
      "title": "Kapitel: Loesungsansatz"
    }
  ]
}
```

### Pflichtfelder

| Feld | Beschreibung |
|---|---|
| `slides` | Array von Slide-Definitionen (siehe oben) |

### Optional

| Feld | Default |
|---|---|
| `organisation` | `Galledia Fachmedien AG` |
| `replace_existing_slides` | `true` — bestehende Vorlage-Beispiele werden geloescht. Falls `false`: Vorlage-Folien bleiben erhalten und neue werden angehaengt |

### Pro Slide

| Feld | Wann |
|---|---|
| `layout` | Pflicht — siehe Layout-Tabelle oben |
| `title` | Folientitel |
| `subtitle` | Untertitel (vor allem bei Titelfolien) |
| `content` | Hauptinhalt als String (mit `\n` fuer Zeilenumbrueche) |
| `items` | Array — Alternative zu `content` fuer Listen (Agenda etc.) |

## Aufruf

**Primaerer Weg: MCP-Tool `mcp__galledia-office__generate_galledia_praesentation`**

```python
result = mcp__galledia_office__generate_galledia_praesentation(data={
    "organisation": "Galledia Fachmedien AG",
    "slides": [
        {"layout": "title", "title": "...", "subtitle": "..."},
        {"layout": "agenda", "title": "...", "items": ["...", "..."]},
        {"layout": "content", "title": "...", "content": "..."}
    ]
})
```

Returns: `{filename, mimetype, content_base64, size_bytes, report, validation_errors}`.
`mimetype` ist `application/vnd.openxmlformats-officedocument.presentationml.presentation`.

**Fallback** (Claude Code Desktop, ohne MCP):

```powershell
python "<skill-dir>/scripts/fill_praesentation.py" --input <data.json> --output <out.pptx>
```

## CI-Regeln

- Organisation muss eine der 5 OE sein (siehe `references/schreibweisen.md`)
- Keine "Galledia AG", "Galledia Gruppe", "Fax" im Text
- Keine geraden Anfuehrungszeichen `"` — Galledia-CI verlangt `« »`
- Standard-Schriften (Volte, Volte Rounded) kommen aus der Vorlage — nicht aendern

## V1-Limitationen (zur Kenntnis)

- Nur Text-Inhalte. Bilder, Tabellen, Diagramme: in PowerPoint manuell einfuegen
- `[[MasterProperty("Organisation", ...)]]`-Platzhalter aus der Original-Vorlage
  werden automatisch durch `organisation` ersetzt
- Wenn `slides` nicht angegeben wird: nur MasterProperty-Replace,
  alle 22 Beispielfolien bleiben drin (gut zum Ausprobieren)

## Was NICHT in diesem Skill

- Brief (.dotx) → `galledia-brief`
- Kurzbrief / Mitteilung → `galledia-kurzbrief`
