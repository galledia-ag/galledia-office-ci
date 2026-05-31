---
name: galledia-kurzbrief
description: >
  Erstellt einen Galledia-Kurzbrief (transmittal sheet / kurze Mitteilung)
  im CI/CD gemaess Markenhandbuch v1.5. Verwende diesen Skill immer wenn
  ein User einen Kurzbrief, eine kurze Mitteilung, ein Begleitschreiben
  fuer Unterlagen, eine Aktennotiz oder ein Memo mit Standardoptionen
  ("zur Kenntnisnahme", "zur Erledigung", "Beilagen" etc.) erstellen will.
  Triggert auf: "Kurzbrief", "Kurzmitteilung", "kurze Mitteilung",
  "Begleitschreiben", "Aktennotiz", "Memo", "Transmittal", "Beilage zur".
  Im Gegensatz zum normalen Brief (galledia-brief) hat der Kurzbrief
  KEINEN Brieftext-Body, sondern 10 vordefinierte Notizoptionen mit
  Checkboxen. Die Generierung erfolgt ueber den MCP-Server galledia-office.
  Arbeitssprache: Schweizer Hochdeutsch.
version: "0.0.6"
---

# Galledia Kurzbrief

1-seitiges Begleitschreiben fuer Beilagen mit 10 vordefinierten
Notizoptionen (Checkboxen — werden im gedruckten Dokument manuell
angekreuzt).

## Workflow

### Schritt 1 — Daten sammeln (Hard-Stop bei fehlenden Pflichtfeldern)

**Kurzbriefe muessen versandfertig generiert werden — keine Platzhalter.**
Wenn ein Pflichtfeld fehlt ODER Claude sich unsicher ist: **STOP**, gezielte
Rueckfrage, KEIN MCP-Aufruf bevor alles vollstaendig ist.

#### Pflichtfelder — ABSENDER (Galledia-Mitarbeiter)

| Feld | Beispiel | Pflicht |
|---|---|---|
| `sender_oe` (Aktiengesellschaft) | `Galledia Fachmedien AG` | ✅ |
| `sender_first_name` | `Stefan` | ✅ |
| `sender_last_name` | `Zimmermann` | ✅ |
| `sender_street` | `Buckhauserstrasse 24` | ✅ |
| `sender_zip` + `sender_city` | `8048 Zürich` | ✅ |
| `sender_contact_email` | `stefan.zimmermann@galledia.ch` | ✅ |
| `sender_contact_phone` ODER `sender_contact_mobile` (mind. eines) | `T +41 58 344 96 22` / `M +41 79 555 12 34` | ✅ (eines) |

OE muss exakt eine der 5 sein: `galledia group ag` (klein!), `Galledia Fachmedien AG`,
`Galledia Regionalmedien AG`, `Galledia Print AG`, `Galledia Digital AG`.

`sender_contact_name` wird automatisch aus `sender_first_name` + `sender_last_name` gebildet.

#### Pflichtfelder — EMPFAENGER

| Feld | Beispiel | Pflicht |
|---|---|---|
| `recipient_salutation` | `Herr` / `Frau` (ggf. mit Titel) | ✅ |
| `recipient_first_name` | `Hans` | ✅ |
| `recipient_last_name` | `Mueller` | ✅ |
| `recipient_company` | `Mueller AG` | ⬜ optional |
| `recipient_street` | `Bahnhofstrasse 1` | ✅ |
| `recipient_zip` + `recipient_city` | `8001 Zuerich` | ✅ |

Diese Felder werden zu `recipient_lines` (Liste) zusammengefuegt.

#### Pflichtfelder — ALLGEMEIN

| Feld | Beispiel | Pflicht |
|---|---|---|
| `date_city` | `Zuerich` | ✅ |
| `date` | `28. Mai 2026` | ✅ |
| `subject` | `Unterlagen zum Vertrag` | ✅ |

Kein `body` — stattdessen werden die `notes` (siehe unten) angekreuzt.

#### Anrede — HART (nie generisch wenn Name bekannt)

| Empfaenger | `introduction` |
|---|---|
| `Herr`, Name bekannt | `Sehr geehrter Herr {Nachname}` |
| `Frau`, Name bekannt | `Sehr geehrte Frau {Nachname}` |
| Mit Titel | `Sehr geehrter Herr Dr. {Nachname}` |
| Nur Firmenadresse | `Sehr geehrte Damen und Herren` |

**Niemals** `Sehr geehrte Damen und Herren` wenn der Empfaenger-Name bekannt ist.

#### Optional

- `closing` — Default `Freundliche Grüsse`
- `signatory_name`, `signatory_role`
- `notes` — dict[str, str], um einzelne Notizoptionen zu ueberschreiben
- `recipient_company`

### Notes (Standardoptionen mit Checkboxen)

10 vordefinierte Optionen aus der Galledia-Vorlage:

| # | Default-Text |
|---|---|
| `Note1` | zur Kenntnisnahme |
| `Note2` | zu Ihren Akten |
| `Note3` | auf Ihren Wunsch |
| `Note4` | mit Dank zurück |
| `Note5` | zur Erledigung |
| `Note6` | gemäss telefonischer Besprechung |
| `Note7` | zur Stellungnahme |
| `Note8` | gemäss Ihrer Anfrage |
| `Note9` | per E-Mail an: *(Original "per Fax an Nummer:" — Galledia v1.5: kein Fax mehr)* |
| `Note10` | Beilagen: |

**Ueberschreiben einzelner Notes:**
```
notes = {"Note10": "Beilagen: Vertrag, AGB"}
```

### Schritt 2 — CI-Validierung

Identisch zum Brief:
- OE exakt eine der 5 erlaubten Schreibweisen
- Telefonformat **zwingend** `T +41 58 ...` bzw. `M +41 79 ...`
- E-Mail plausibel
- Anrede konsistent mit `recipient_salutation`
- Keine geraden Anfuehrungszeichen — `« »` (Guillemets)
- Keine verbotenen Begriffe: "Galledia AG", "Galledia Gruppe", "Galledia GmbH", "Fax"

Siehe `references/schreibweisen.md` fuer Details.

### Schritt 2a — Versandfertig-Checkliste (Pflicht vor MCP-Call)

Bevor du `mcp__galledia-office__generate_galledia_kurzbrief` aufrufst, fasse
den Kurzbrief zusammen und hole vom User eine Bestaetigung:

```
Bereit zum Generieren — bitte kurz pruefen:

ABSENDER:    Stefan Zimmermann, Galledia Fachmedien AG
             Buckhauserstrasse 24, 8048 Zuerich
             stefan.zimmermann@galledia.ch, T +41 58 344 96 22

EMPFAENGER:  Herr Hans Mueller
             Mueller AG, Bahnhofstrasse 1, 8001 Zuerich

DATUM:       Zuerich, 28. Mai 2026
BETREFF:     Unterlagen zum Vertrag
ANREDE:      Sehr geehrter Herr Mueller
ANGEKREUZT:  zur Kenntnisnahme, Beilagen: Vertrag, AGB
GRUSS:       Freundliche Gruesse / Stefan Zimmermann

Alles korrekt? Dann generiere ich den Kurzbrief.
```

Bei "ja" → MCP-Call. Bei Korrekturen → anpassen und erneut zeigen.
Bei vager Antwort → nicht generieren, nachfragen.

### Schritt 3 — MCP-Tool aufrufen

`mcp__galledia-office__generate_galledia_kurzbrief` mit dem JSON.

Returns: `{filename, mimetype, download_url, size_bytes,
expires_in_seconds, report, validation_errors}`.

### Schritt 4 — Link dem User praesentieren

**WICHTIG: Versuche NIE selbst, die `download_url` per HTTP/curl/web_fetch
herunterzuladen.** Praesentiere die URL als Markdown-Link mit dem
`filename` als sichtbarem Text:

```markdown
Hier ist der Kurzbrief: [Kurzbrief_Vertragsentwurf.docx](https://office-mcp.epimetheus.uk/files/...)
```

Erwaehne kurz die wichtigsten Felder (Empfaenger, Betreff, ueberschriebene
Notes). Antworte sachlich, ohne den Inhalt zu wiederholen.

## Was NICHT in diesem Skill

- Voller Brief mit Brieftext → `galledia-brief`
- Praesentation → `galledia-praesentation`
