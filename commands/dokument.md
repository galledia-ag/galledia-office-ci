---
description: Galledia-Dokument im CI/CD erstellen (Vorlage_Dokument, Code Execution)
allowed-tools: ["Code Execution"]
---

Aktiviere den `galledia-dokument`-Skill und erstelle ein mehrseitiges
Galledia-Dokument (Offerte, Anleitung, Konzept, Report, Manual, Schulungs-
unterlagen) im CI/CD gemaess Markenhandbuch v1.5.

Im Gegensatz zum Brief/Kurzbrief ist dies eine MEHRSEITIGE Vorlage mit
Cover, Header/Footer und Platz fuer ausfuehrlichen Body-Inhalt.

Generierung erfolgt via **Code Execution** (`fill_dokument.py` aus dem Plugin),
nicht via MCP-Server. Setup-Block aus dem SKILL.md ausfuehren:
1. `pip install python-docx --break-system-packages`
2. Assets laden (`fill_dokument.py` + `Vorlage_Dokument.dotx`)
3. `build_document(...)` mit Pflichtfeldern aufrufen

**Pflichtfelder** (siehe SKILL.md):
- `titel`, `untertitel`, `datum`, `rechtseinheit`, `adresse`
- `abschnitte` (Liste mit Kapiteln + Inhaltsblöcken)

Falls der User in `$ARGUMENTS` Infos mitgegeben hat, übernimm sie.
Fehlende Pflichtfelder vor dem Build nachfragen — nie Inhalte selbst erfinden,
ausser der User sagt explizit «mach selbst».

User-Input: $ARGUMENTS
