---
description: Galledia-Präsentation im CI/CD erstellen (Vorlage_5, Code Execution)
allowed-tools: ["Code Execution"]
---

Aktiviere den `galledia-praesentation`-Skill und erstelle eine CI/CD-konforme
PowerPoint-Präsentation (.pptx) mit Vorlage_5, Volte-Schrift und Galledia-Logos.

**Pflichtabfrage vor dem Start:**
- Datum der Präsentation (für Fusszeile, z.B. «29. Mai 2026»)
- Rechtseinheit (z.B. «Galledia Fachmedien AG»)
- Präsentationsinhalt / Storyline (wenn nicht in $ARGUMENTS)

Verwende `helpers.py` und die Funktionen aus dem Skill:
`build_presentation()`, `add_title()`, `add_agenda()`, `add_content()`,
`kpi_grid()`, `two_column()`, `flow_pipeline()`, `numbered_steps()`,
`timeline()`, `add_closing()` — nie direkt MCP aufrufen.

Fusszeile immer setzen: `build_presentation(datum=..., rechtseinheit=...)`.
Keine Versalien. Keine Folienübergänge. Kein Volte Rounded in generiertem Text.

User-Input: $ARGUMENTS
