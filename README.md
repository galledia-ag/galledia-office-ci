# Galledia Office CI Plugin

Claude-Plugin für CI/CD-konforme Office-Dokumente der Galledia-Gruppe.

**v1.0.0** — Hybride Architektur:
- `galledia-praesentation` — PowerPoint (**Code Execution**, Vorlage_5 + Volte + Logos)
- `galledia-brief` — Geschäftsbrief (.docx, MCP `galledia-office`)
- `galledia-kurzbrief` — Kurzbrief (.docx, MCP `galledia-office`)
- `galledia-dokument` — Dokument für Offerten/Schulungen (.docx)

## Verwendung

```
/praesentation Erstelle eine Präsentation zu unserem KI-Hub-Projekt
/brief         Schreibe einen Brief an Kunde XY wegen...
/kurzbrief     Kurzmitteilung an...
```

Oder natürliche Sprache — der passende Skill erkennt die Anfrage automatisch.

## Architektur

```
galledia-office-ci/
├── .claude-plugin/
│   ├── plugin.json          ← Skill-Bundle-Manifest
│   └── marketplace.json     ← Org-Marketplace-Konfiguration
├── .mcp.json                ← MCP brief/kurzbrief (epimetheus.uk)
├── commands/                ← Slash-Commands /praesentation /brief etc.
├── skills/
│   ├── galledia-praesentation/
│   │   ├── SKILL.md         ← Instruktionen + CI-Regeln
│   │   ├── helpers.py       ← python-pptx Builder-Library
│   │   ├── assets/
│   │   │   ├── Vorlage_5.pptx      ← Galledia-Template (10 Layouts)
│   │   │   ├── fonts/              ← Volte-Familie (5 OTF)
│   │   │   └── logo/               ← Logos rot/weiss/schwarz (6 PNG)
│   │   └── references/      ← Markenhandbuch, Schreibweisen, Adressen
│   ├── galledia-brief/      ← Word-Brief (MCP-basiert)
│   ├── galledia-kurzbrief/  ← Word-Kurzbrief (MCP-basiert)
│   └── galledia-dokument/   ← Word-Dokument (in Entwicklung)
└── docs/
    └── DOCKER_CLEANUP.md    ← Roadmap MCP-Ablösung
```

## Präsentation — verfügbare Layouts (Vorlage_5)

| Layout | Typ |
|---|---|
| Titelfolie | Rote Vollflächige, Galledia-Logo |
| Zwischenfolie | Kapitel-Anker in Rot |
| 01_Agenda 5 / 01_Agenda 22 | 5 oder 6–12 Punkte |
| 02_wenigText | Kernbotschaft plakativ |
| 04_vielText | Strukturierter Inhalt + Quellenangabe |
| Leer | Freie Komposition (KPI, Zweispalter, Pipeline, Timeline) |
| Abschlussfolie | Diskussions-Folie mit Piktogramm |
| Schlussfolie | Rot, weisses Galledia-Logo |

## Deployment (Org-Marketplace)

**Organization settings → Cowork → Plugin-Marketplace → Git-Repo:**
```
https://github.com/galledia-ag/galledia-office-ci
Branch: main
```

Nach jedem `git push main` → Marketplace synct automatisch (bis 30 Min).

## Vorlagen aktualisieren

| Asset | Pfad | Lieferant |
|---|---|---|
| PowerPoint-Vorlage | `skills/galledia-praesentation/assets/Vorlage_5.pptx` | Designer (Prepress Flawil) |
| Volte-Fonts | `skills/galledia-praesentation/assets/fonts/` | Brand-Guard |
| Logos | `skills/galledia-praesentation/assets/logo/` | M:\\\_organisation\\20_logos |
| Word-Briefvorlage | `skills/galledia-brief/` | Designer |

## Roadmap

| Version | Inhalt | Status |
|---|---|---|
| v0.1–v0.3 | Brief, Kurzbrief (MCP) | ✅ |
| **v1.0.0** | **Präsentation → Code Execution (Vorlage_5 + Volte + Logos)** | **✅ aktuell** |
| v1.1.0 | Word-Skills Brief + Kurzbrief als Code Execution | geplant |
| v1.2.0 | Dokument-Skill | geplant |
| v1.3.0 | MCP vollständig abgelöst, Docker-Cleanup | geplant |

Detaillierter MCP-Ablöseplan: `docs/DOCKER_CLEANUP.md`

## Kontakt

Fragen zur CI oder Template-Updates: stefan.zimmermann@galledia.ch
