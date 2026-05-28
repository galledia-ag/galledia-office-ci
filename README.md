# Galledia Office CI Plugin

Claude Code Plugin für CI/CD-konforme Office-Dokumente der Galledia-Gruppe.

**Aktueller Stand (V0.2):** Drei Skills im Plugin:
- `galledia-brief` — Geschäftsbrief (.docx)
- `galledia-kurzbrief` — Kurzbrief / Begleitschreiben mit 10 Notizoptionen (.docx)
- `galledia-praesentation` — PowerPoint-Präsentation mit 16 Slide-Layouts (.pptx)

Alle auf Basis der offiziellen Galledia-Vorlagen gemäss Markenhandbuch v1.5.

## Was macht das Plugin

Wenn ein:e Mitarbeiter:in in Claude Code schreibt:

> *Erstelle einen Brief an die Müller AG wegen unserer Inserate-Offerte für 2026*

dann erkennt der **`galledia-brief`**-Skill die Anfrage, sammelt die nötigen Daten (Empfänger, Betreff, Inhalt), prüft sie gegen die Galledia-CI-Regeln (Schreibweise „Galledia Fachmedien AG" etc., Telefonformat, Bullets `·`, Guillemets `« »`) und liefert eine fertige `.docx` — fertig zum Versand.

Die Vorlage wird **nicht** verändert; nur ihre Platzhalter (Word Content Controls + Bookmarks) werden befüllt. Layout, Logo, Volte-Schrift, Schutzzone, Adresszeile kommen alle automatisch aus der `.dotx`.

## Installation für Mitarbeitende

Voraussetzung: Claude Code installiert, Python 3.10+ verfügbar.

```bash
# 1. Plugin-Marketplace hinzufügen (einmalig pro MA)
/plugin marketplace add <git-enterprise-url>/galledia-office-ci

# 2. Plugin aktivieren
/plugin install galledia-office-ci

# 3. Python-Abhängigkeit (einmalig)
python -m pip install lxml
```

Ab dann steht der `galledia-brief`-Skill automatisch zur Verfügung — keine weitere Konfiguration nötig.

## Repo-Struktur

```
galledia-office-ci/
├── .claude-plugin/plugin.json
├── skills/
│   └── galledia-brief/
│       ├── SKILL.md                        ← Skill-Definition + CI-Regeln
│       ├── references/
│       │   ├── schreibweisen.md            ← 5 OE, Telefon, Sonderzeichen
│       │   ├── adressbloecke.md            ← Standorte (Flawil, ZH, FF, LU, …)
│       │   └── markenhandbuch_kurzfassung.md
│       ├── templates/
│       │   └── Brief-Vorlage Galledia.dotx ← Offizielle Word-Vorlage
│       └── scripts/
│           ├── fill_brief.py               ← Python-Befüller
│           ├── example_input.json          ← Beispiel-Eingabe
│           └── README.md                   ← Skript-API-Doku
├── test/                                   ← Test-Outputs (in .gitignore)
└── README.md (diese Datei)
```

## CI/CD-Regeln (durchgesetzt)

| Regel | Umsetzung |
|---|---|
| **5 Organisationseinheiten** | `galledia group ag` (klein!), `Galledia Fachmedien AG`, `Galledia Regionalmedien AG`, `Galledia Print AG`, `Galledia Digital AG` — alles andere führt zu Validierungsfehler |
| **Telefonformat** | `T +41 58 344 96 22` / `M +41 79 XXX XX XX` — Regex-validiert |
| **Bullets** | `·` (Mittelpunkt), nicht `-` oder `•` |
| **Anführungszeichen** | `« »` (Guillemets), nicht `"` |
| **Fax** | Verboten — Validierung weist ab |
| **Volte-Schrift** | Aus Vorlage, automatisch (auf allen MA-Geräten installiert) |
| **Logo, Adresszeile, Schutzzone** | Kommen direkt aus der `.dotx` |

## Vorlagen aktualisieren

Wenn das Markenhandbuch sich ändert (z.B. neue OE, neue Standort-Adresse):

1. Pull Request gegen dieses Repo öffnen
2. `templates/Brief-Vorlage Galledia.dotx` ersetzen (von Designer:in bereitgestellt) und/oder `references/*.md` anpassen
3. Version in `.claude-plugin/plugin.json` bumpen (semver)
4. PR mergen → MA bekommen Update via `/plugin update` (oder automatisch beim nächsten Start)

Es gibt aktuell keinen dedizierten Brand-Guard — Template-Pflege läuft über die normale Entwicklungs-Pipeline.

## Roadmap

| Version | Inhalt | Status |
|---|---|---|
| V0.1 | Brief (`.docx`) | ✅ Fertig |
| V0.1.2 | Encoding-Robustheit (UTF-8/BOM/cp1252/Mojibake-Auto-Repair) | ✅ Fertig |
| V0.2 | Kurzbrief (`.docx`) + Präsentation (`.pptx`) | ✅ Fertig |
| V0.3 | Skill-Bundles für Marketing-/Sales-Templates | geplant |

## Technischer Hintergrund

Die Galledia-Vorlagen nutzen ein officeatwork-Setup mit:
- **Content Controls** (`<w:sdt>`) mit `w:tag`-Identifikation (z.B. `AdressBlock`, `RecipientAddress`)
- **Data Binding** auf `customXml/item4.xml` (officeatwork CustomXMLPart) — dort liegen die effektiven Werte
- **Bookmarks** für freie Textbereiche (`Subject`, `Text`)

Das `fill_brief.py`-Skript:
1. Validiert die Eingabe gegen Galledia-CI-Regeln
2. Liest die `.dotx` als ZIP-Archiv ein (kein `python-docx` — das beschädigt die Vorlagen-Struktur)
3. Aktualisiert `customXml/item4.xml` (autoritative Datenquelle für Word)
4. Aktualisiert die SDT-Inline-Content (Cache + Fallback)
5. Aktualisiert Bookmark-Bereiche (`Subject`, `Text`)
6. Patcht `[Content_Types].xml` (`template.main+xml` → `document.main+xml`)
7. Schreibt als `.docx` raus

## Test

Test-Brief generieren:

```powershell
python skills/galledia-brief/scripts/fill_brief.py `
  --input skills/galledia-brief/scripts/example_input.json `
  --output test/Testbrief.docx
```

## Quellen

- Galledia Markenhandbuch v1.5 (7.6.2021)
- Brief-Vorlage Galledia.dotx (offizielle Word-Vorlage)

## Kontakt

Bei Fragen zur Verwendung oder bei CI-Verstössen, die der Skill nicht erkennt: Issue im Repo eröffnen.
