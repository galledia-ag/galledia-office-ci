---
name: galledia-praesentation
description: >
  Erstellt eine Galledia-Praesentation (PowerPoint, .pptx) im CI/CD
  gemaess Markenhandbuch v1.5. Verwende diesen Skill immer wenn ein User
  eine Praesentation, Slides, ein Pitch-Deck, eine Kundenpraesentation
  oder einen Foliensatz im Galledia-Design erstellen will. Triggert auf:
  "Praesentation", "Foliensatz", "Slides", "Pitch", "Pitch-Deck",
  "Foliendeck", "Kundenpraesentation", "PowerPoint", "PPT", "Vortrag",
  "Praesentationsdeck". Liefert eine .pptx mit Galledia-Layouts (Titel
  rot/tuerkis/bronze/purple/lila, Agenda, Inhalt, Zwischenfolie) und der
  korrekten Galledia-Typografie (Volte/Volte Rounded). Generierung
  erfolgt ueber den MCP-Server galledia-office. Arbeitssprache:
  Schweizer Hochdeutsch.
---

# Galledia Praesentation

PowerPoint mit 16 Galledia-Slide-Layouts in CI-Farben, Volte-Schrift
und Galledia-G als Watermark. Erstellung Folie-fuer-Folie konfigurierbar.

## Workflow

### Schritt 1 — Slide-Struktur planen

Frage den User nach:
- Anzahl Folien
- Inhalt je Folie (Titel + optional Subtitle/Content/Items)
- Layout je Folie (siehe Tabelle unten)
- Ziel-Organisation (Default: `Galledia Fachmedien AG`)

### Verfuegbare Layouts

| Key | Was | Wann verwenden |
|---|---|---|
| `title`, `title_red` | Titelfolie rot (Vollflaeche) | Eroeffnungsfolie |
| `title_turquoise` | Titelfolie tuerkis | Variation |
| `title_bronze`, `title_purple`, `title_lila` | Weitere Akzentfarben | Kapiteltitel |
| `section`, `section_red` | Zwischenfolie rot | Kapiteltrenner |
| `section_turquoise`, `section_bronze`, `section_purple`, `section_lila` | Andere Farben | |
| `agenda` | 01_Agenda 5 | Inhaltsuebersicht |
| `agenda_22` | 01_Agenda 22 | Alternative Agenda |
| `content` | 02_wenigText | Standard-Inhaltsfolie |
| `content_long` | 04_vielText | Detail-Folien |
| `default` | DEFAULT SLIDE | Generischer Inhalt |
| `blank` | Leer | Custom-Inhalt |

### Schritt 2 — JSON aufbauen

```
{
  "organisation": "Galledia Fachmedien AG",
  "slides": [
    {"layout": "title", "title": "...", "subtitle": "..."},
    {"layout": "agenda", "title": "Übersicht", "items": ["...", "..."]},
    {"layout": "content", "title": "...", "content": "Zeile 1\nZeile 2\n· Bullet"},
    {"layout": "section", "title": "Kapitel ..."}
  ]
}
```

**Pro Folie:**
- `layout` (Pflicht) — Key aus Tabelle oben
- `title` — Folientitel
- `subtitle` — Untertitel (v.a. fuer Titelfolien)
- `content` — Hauptinhalt als String mit `\n` und `· ` fuer Bullets
- `items` — Alternative zu content als Array (z.B. Agenda)

**Optional Top-Level:**
- `replace_existing_slides` (Default `true`) — wenn `false` bleiben die
  22 Vorlage-Beispielfolien drin und neue werden angehaengt

### Schritt 3 — MCP-Tool aufrufen

`mcp__galledia-office__generate_galledia_praesentation` mit dem JSON.

Returns wie bei den anderen Skills. Bei Erfolg Datei dem User anbieten.

## CI-Regeln

- `organisation` muss eine der 5 OE sein (siehe `references/schreibweisen.md`)
- Keine "Galledia AG", "Galledia Gruppe", "Fax" im Text
- Keine geraden Anfuehrungszeichen — `« »` verwenden

## V1-Limitationen

- Nur Text-Inhalte. Bilder, Tabellen, Diagramme: in PowerPoint manuell
  einfuegen
- `[[MasterProperty(...)]]`-Platzhalter aus der Original-Vorlage werden
  automatisch durch `organisation` ersetzt

## Was NICHT in diesem Skill

- Brief → `galledia-brief`
- Kurzbrief → `galledia-kurzbrief`
