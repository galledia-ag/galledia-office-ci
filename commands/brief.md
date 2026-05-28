---
description: Generiere einen Galledia-Geschaeftsbrief im CI/CD
allowed-tools: ["mcp__galledia-office__generate_galledia_brief"]
---

Aktiviere den `galledia-brief`-Skill und erstelle einen Galledia-Geschaeftsbrief
im CI/CD gemaess Markenhandbuch v1.5.

Falls der User in `$ARGUMENTS` schon Informationen mitgegeben hat
(Empfaenger, Betreff, Inhalt, etc.), uebernimm sie. Fehlende Pflichtfelder
nachfragen:

- Empfaenger-Adresse (mehrzeilig)
- Betreff
- Brieftext (Body)
- ggf. Absender-OE (sonst Default Galledia Fachmedien AG falls Kontext passt)
- ggf. Anrede

Validiere gegen Galledia-CI (5 OE-Schreibweisen, keine "Fax",
Telefonformat T/M +41). Rufe dann das MCP-Tool
`mcp__galledia-office__generate_galledia_brief` auf und gib dem User
den `download_url` als Markdown-Link mit dem `filename` als Linktext.

Nie selbst per HTTP herunterladen — Link nur praesentieren.

User-Input: $ARGUMENTS
