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
| `content` | 04_vielText | **Standard fuer Inhaltsfolien mit Fliesstext und Bullets** |
| `content_long` | 04_vielText | Alias zu content (gleicher Layout) |
| `content_short`, `content_plakativ` | 02_wenigText | Plakative Kurz-Botschaften (3-5 Worte HUGE), z.B. „Einfach. Persoenlich. Wirkungsvoll." |
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
- `content` — Hauptinhalt als String mit `\n` fuer Zeilenumbrueche
- `items` — Alternative zu content als Array (z.B. Agenda)

**Bullets:** Schreibe einfach jede Zeile fuer sich (mit `\n` getrennt) —
PowerPoint setzt die Bullet-Glyphe automatisch ueber den Layout-Style.
Wenn du `· ` oder `- ` am Zeilenanfang setzt, wird das vom Skript
entfernt (sonst Doppel-Bullet).

**Layout-Wahl ist entscheidend fuer das Aussehen:**
- Volltextfolien mit Bulletlisten oder Fliesstext → `content` (default)
- Nur 3-5 Stichworte plakativ HUGE → `content_short`
- Eine Agenda mit Aufzaehlung → `agenda`
- Kapitel-Trennung → `section`

**Optional Top-Level:**
- `replace_existing_slides` (Default `true`) — wenn `false` bleiben die
  22 Vorlage-Beispielfolien drin und neue werden angehaengt

### Schritt 3 — MCP-Tool aufrufen

`mcp__galledia-office__generate_galledia_praesentation` mit dem JSON.

Returns: `{filename, mimetype, download_url, size_bytes,
expires_in_seconds, report, validation_errors}`.

### Schritt 4 — Link dem User praesentieren

**WICHTIG: Versuche NIE selbst, die `download_url` per HTTP/curl/web_fetch
herunterzuladen.** Praesentiere die URL als Markdown-Link mit dem
`filename` als sichtbarem Text:

```markdown
Hier ist deine Praesentation: [Praesentation_Kunde_X.pptx](https://office-mcp.epimetheus.uk/files/...)
```

Liste kurz die generierten Folien stichwortartig auf (Layout + Titel)
damit der User sieht, was drin ist. Antworte sachlich.

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
