---
description: Generiere eine Galledia-PowerPoint-Praesentation im CI/CD
allowed-tools: ["mcp__galledia-office__generate_galledia_praesentation"]
---

Aktiviere den `galledia-praesentation`-Skill und erstelle eine
PowerPoint-Praesentation (.pptx) mit Galledia-Layouts in CI-Farben
(Rot/Tuerkis/Bronze/Purple/Lila), Volte-Schrift und Galledia-G als
Watermark.

Falls der User in `$ARGUMENTS` schon Folien-Struktur mitgegeben hat,
uebernimm sie. Sonst frage nach:
- Anzahl/Reihenfolge der Folien
- Titel + Inhalt je Folie
- Welches Layout je Folie (title / agenda / content / section / etc.)

Verfuegbare Layouts: title (rot/tuerkis/bronze/purple/lila), section
(gleiche Farb-Varianten), agenda, content, content_long, default, blank.

Rufe `mcp__galledia-office__generate_galledia_praesentation` auf, dem
User den `download_url` als Markdown-Link praesentieren. Liste die
generierten Folien kurz stichwortartig auf.

User-Input: $ARGUMENTS
