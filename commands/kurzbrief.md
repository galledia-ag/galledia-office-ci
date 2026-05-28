---
description: Generiere einen Galledia-Kurzbrief (Begleitschreiben mit 10 Notizoptionen)
allowed-tools: ["mcp__galledia-office__generate_galledia_kurzbrief"]
---

Aktiviere den `galledia-kurzbrief`-Skill und erstelle einen Kurzbrief —
ein 1-seitiges Begleitschreiben mit 10 vordefinierten Notizoptionen
und Checkboxen.

Falls der User in `$ARGUMENTS` schon Informationen mitgegeben hat
(Empfaenger, Betreff, Beilagen, etc.), uebernimm sie. Im Gegensatz zum
normalen Brief gibt es KEINEN Brieftext-Body.

Nachfragen falls fehlend:
- Empfaenger
- Betreff
- ggf. welche Note ueberschrieben werden soll (z.B. Note10 = "Beilagen: ...")

Rufe `mcp__galledia-office__generate_galledia_kurzbrief` auf, dem User
den `download_url` als Markdown-Link mit `filename` praesentieren.

User-Input: $ARGUMENTS
