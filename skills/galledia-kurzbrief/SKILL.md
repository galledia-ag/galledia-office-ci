---
name: galledia-kurzbrief
description: >
  Erstellt einen Galledia-Kurzbrief (transmittal sheet / kurze Mitteilung) im
  Galledia-CI/CD (Markenhandbuch v1.5). Verwende diesen Skill immer wenn ein
  User einen Kurzbrief, eine kurze Mitteilung, ein Begleitschreiben fuer
  Unterlagen, eine Aktennotiz oder ein Memo mit Standardoptionen
  ("zur Kenntnisnahme", "zur Erledigung", "Beilagen" etc.) erstellen will.
  Triggert auf: "Kurzbrief", "Kurzmitteilung", "kurze Mitteilung",
  "Begleitschreiben", "Aktennotiz", "Memo", "Transmittal", "Beilage zur".
  Im Gegensatz zum normalen Brief (galledia-brief) hat der Kurzbrief KEINEN
  Brieftext-Body, sondern 10 vordefinierte Notizoptionen mit Checkboxen.
  Arbeitssprache: Schweizer Hochdeutsch (ss statt ss).
---

# Galledia Kurzbrief

Du erstellst einen Kurzbrief — ein 1-seitiges Begleitschreiben fuer Beilagen
und kurze Mitteilungen. Layout, Logo, Volte-Schrift kommen aus der Vorlage.
Der Kurzbrief enthaelt 10 Standardoptionen mit Checkboxen, die im
gedruckten Dokument manuell angekreuzt werden.

## Workflow

1. Daten sammeln (Empfaenger, Absender, Betreff)
2. CI-Validierung (siehe Brief-Skill, gleiche Regeln)
3. Generieren via `scripts/fill_kurzbrief.py`
4. Ergebnis als .docx liefern; User kreuzt die zutreffenden Optionen in
   Word an und druckt aus

## JSON-Schema (Pflichtfelder)

Wie galledia-brief, aber **ohne** `body`. Mit `subject` (Betreff).

| Feld | Beispiel |
|---|---|
| `sender_oe` | `Galledia Fachmedien AG` |
| `sender_street` | `Buckhauserstrasse 24` |
| `sender_city` | `8048 Zürich` |
| `sender_contact_name` | `Stefan Zimmermann` |
| `recipient_lines` | `["Müller AG", "Hans Müller", "Bahnhofstrasse 1", "8001 Zürich"]` |
| `date_city` | `Zürich` |
| `date` | `28. Mai 2026` |
| `subject` | `Unterlagen zur Generalversammlung` |

## JSON-Schema (Optional)

| Feld | Default | Hinweis |
|---|---|---|
| `sender_contact_phone` | — | Format `T +41 …` |
| `sender_contact_mobile` | — | Format `M +41 …` |
| `sender_contact_email` | — | |
| `introduction` | `Sehr geehrte Damen und Herren` | |
| `closing` | `Freundliche Grüsse` | |
| `signatory_name` | = `sender_contact_name` | |
| `signatory_role` | — | Mit `\n` zwischen mehreren Rollen |
| `notes` | siehe unten | Optionale Ueberschreibungen einzelner Notizoptionen |

## Notes (Standardoptionen mit Checkboxen)

Der Kurzbrief enthaelt 10 vordefinierte Optionen. Defaults gemaess
Galledia-Vorlage:

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
| `Note9` | per E-Mail an: *(Original-Vorlage hatte "per Fax an Nummer:" — Fax verwendet Galledia nicht mehr)* |
| `Note10` | Beilagen: |

Ueberschreiben via:
```json
"notes": {
  "Note9": "per Bote an:",
  "Note10": "Beilagen: GV-Protokoll, Jahresrechnung"
}
```

## Aufruf

**Primaerer Weg: MCP-Tool `mcp__galledia-office__generate_galledia_kurzbrief`**

```python
result = mcp__galledia_office__generate_galledia_kurzbrief(data={
    "sender_oe": "Galledia Fachmedien AG",
    ...,
    "notes": {"Note10": "Beilagen: ..."}  # optional
})
```

Returns: `{filename, mimetype, content_base64, size_bytes, report, validation_errors}`.

Bei Erfolg: Datei dem User als Download anbieten.
Bei Validation-Fehler: User informieren und korrigieren.

**Fallback** (Claude Code Desktop, ohne MCP):

```powershell
python "<skill-dir>/scripts/fill_kurzbrief.py" --input <data.json> --output <out.docx>
```

## CI-Regeln

Identisch zum Brief — siehe `references/schreibweisen.md`:
- 5 OE-Schreibweisen, `galledia group ag` klein
- Telefonformat `T +41 … / M +41 …`
- Bullets `·`, Guillemets `« »`
- Verboten: "Galledia AG", "Galledia Gruppe", "Fax"

## Was NICHT in diesem Skill

- Voller Brief mit Brieftext → `galledia-brief`
- Praesentation → `galledia-praesentation`
