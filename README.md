# Galledia Office CI Plugin

Claude-Plugin für CI/CD-konforme Office-Dokumente der Galledia-Gruppe.

**v0.0.5** — Hybride Architektur (4 Skills, 2 Mechanismen):

| Skill | Output | Mechanismus | Wo läuft die Generierung |
|---|---|---|---|
| `galledia-brief` | `.docx` | MCP-Server | Server (Cloudflare Access, zentrale Vorlage) |
| `galledia-kurzbrief` | `.docx` | MCP-Server | Server (Cloudflare Access, zentrale Vorlage) |
| `galledia-dokument` | `.docx` | Code Execution | Sandbox (`fill_dokument.py` + `Vorlage_Dokument.dotx`) |
| `galledia-praesentation` | `.pptx` | Code Execution | Sandbox (`helpers.py` + `Vorlage_6.pptx` + Logos) |

## Verwendung

```
/brief         Schreibe einen Brief an Kunde XY wegen…
/kurzbrief     Kurzmitteilung an…
/dokument      Erstelle eine Offerte / Schulungsunterlagen für…
/praesentation Erstelle eine Präsentation zu unserem KI-Hub-Projekt
```

Oder natürliche Sprache — der passende Skill erkennt die Anfrage automatisch
über die Trigger-Wörter in der Skill-Description.

## Warum zwei Mechanismen?

**MCP (Brief, Kurzbrief)** — zentraler Server hostet die offizielle Vorlage.
Vorteil: ein Update am Server gilt für alle 200 User sofort, keine
Plugin-Re-Distribution nötig. Auth via Cloudflare Access stellt sicher, dass
nur Galledia-Domains (`@galledia.ch` / `@fachmedien.ch`) Briefe generieren.

**Code Execution (Dokument, Präsentation)** — komplexe Layouts mit vielen
Varianten (Layouts, KPI-Grids, Pipelines, Timelines) brauchen volle Kontrolle.
Python-Skript läuft im Sandbox, lädt Template + Assets via Raw-URL aus diesem
Repo. Vorteil: keine Server-Abhängigkeit, voll customizable.

Hard-Stop im Setup-Block: falls Assets nicht erreichbar → klarer Fehler, kein
Improvisieren von Claude (verhindert CI-Verstösse durch fehlende Schrift/Logo).

## Repo-Struktur

```
galledia-office-ci/
├── .claude-plugin/
│   ├── plugin.json          ← Skill-Bundle-Manifest
│   └── marketplace.json     ← Org-Marketplace-Konfiguration
├── .mcp.json                ← MCP brief/kurzbrief (epimetheus.uk)
├── commands/                ← Slash-Commands /brief, /kurzbrief, /dokument, /praesentation
├── skills/
│   ├── galledia-brief/      ← MCP-basiert (nur SKILL.md, kein Code)
│   ├── galledia-kurzbrief/  ← MCP-basiert (nur SKILL.md, kein Code)
│   ├── galledia-dokument/
│   │   ├── SKILL.md
│   │   ├── fill_dokument.py ← python-docx Builder
│   │   └── assets/Vorlage_Dokument.dotx
│   └── galledia-praesentation/
│       ├── SKILL.md
│       ├── helpers.py       ← python-pptx Builder
│       └── assets/
│           ├── Vorlage_6.pptx      ← Galledia-Template (10 Layouts)
│           ├── fonts/              ← Volte-Familie (5 OTF)
│           └── logo/               ← Logos rot/weiss/schwarz (6 PNG)
└── docs/
    ├── ROLLOUT_USER.md      ← Anleitung für End-User
    ├── ROLLOUT_EMAIL.md     ← Ankündigungs-E-Mail-Vorlage
    ├── DEPLOY_CHAT_SKILLS.md
    └── archive/             ← Alte Org-Level-Skills (V1, abgelöst durch Plugin)
```

## Präsentation — verfügbare Layouts (Vorlage_6)

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

⚠️ **Bekannter Anthropic-Bug:** Das Plugin-Repo muss **temporär privat** sein
beim ersten Hinzufügen im Org-Dropdown — public Repos erscheinen aktuell
nicht in der Auswahl. Nach erfolgreicher Installation kann das Repo auf
**public** umgestellt werden (nötig, damit der Sandbox Code Execution die
Raw-URL-Assets abrufen kann).

Nach jedem `git push main` → Marketplace synct automatisch (bis 30 Min).
Bei hängender Sync: Plugin deinstallieren + neu hinzufügen erzwingt
frischen Re-Index.

## Vorlagen aktualisieren

| Asset | Pfad | Lieferant |
|---|---|---|
| PowerPoint-Vorlage | `skills/galledia-praesentation/assets/Vorlage_6.pptx` | Designer (Prepress Flawil) |
| Volte-Fonts | `skills/galledia-praesentation/assets/fonts/` | Brand-Guard |
| Logos | `skills/galledia-praesentation/assets/logo/` | `M:\_organisation\20_logos` |
| Word-Dokumentvorlage | `skills/galledia-dokument/assets/Vorlage_Dokument.dotx` | Designer |
| Word-Brief/Kurzbrief | im MCP-Server `office-ci-mcp` | Designer |

## Roadmap

| Version | Inhalt | Status |
|---|---|---|
| 0.0.1 | Initial Plugin-Architektur | ✅ |
| 0.0.2 | Vorlage_5 → Vorlage_6 (1-Spalter-Fix) | ✅ |
| 0.0.3 | Forgiving body_text Parser (`**`, `•`, `-`, `*` Akzeptanz) | ✅ |
| 0.0.4 | Headline-Length-Doku korrigiert (32 statt 35) | ✅ |
| **0.0.5** | **Pre-Rollout Cleanup: SKILL-Hygiene, Hard-Stop, Dokument-Setup, Cmd-Konsistenz** | **✅ aktuell** |
| 0.1.0 | Brief + Kurzbrief auf Code Execution migrieren (MCP-Ablösung) | geplant |
| 0.2.0 | Smoke-Test-Suite, eigene Domain für MCP-Server | geplant |

Detaillierter MCP-Ablöseplan: `docs/DOCKER_CLEANUP.md`

## Kontakt

Fragen zur CI oder Template-Updates: stefan.zimmermann@galledia.ch
