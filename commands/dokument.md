---
description: Generiere ein laengeres Galledia-Dokument (Offerte/Anleitung/Konzept)
allowed-tools: ["mcp__galledia-office__generate_galledia_dokument"]
---

Aktiviere den `galledia-dokument`-Skill und erstelle ein mehrseitiges
Galledia-Dokument (Offerte, Anleitung, Konzept, Report, Manual usw.)
im CI/CD gemaess Markenhandbuch v1.5.

Im Gegensatz zum normalen Brief ist dies eine MEHRSEITIGE Vorlage mit
Cover, Header/Footer und Platz fuer ausfuehrlichen Body-Inhalt.

Falls der User in `$ARGUMENTS` schon Infos gibt (Titel, Empfaenger,
Dokumenttyp), uebernimm sie. Mindestens noetig: `sender_oe` und
`cover_title`.

Rufe `mcp__galledia-office__generate_galledia_dokument` auf, dem User
den `download_url` als Markdown-Link praesentieren. Erwaehne, dass die
Beispiel-Inhalte in Word noch durch eigene Inhalte ersetzt werden
muessen.

User-Input: $ARGUMENTS
