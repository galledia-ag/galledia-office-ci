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
version: "0.0.5"
---

# Galledia Kurzbrief

1-seitiges Begleitschreiben fuer Beilagen mit 10 vordefinierten
Notizoptionen (Checkboxen — werden im gedruckten Dokument manuell
angekreuzt).

## Workflow

### Schritt 1 — Daten sammeln

**Pflichtfelder** (identisch zum Brief, aber **ohne** `body`):
- `sender_oe`, `sender_street`, `sender_city`, `sender_contact_name`
- `recipient_lines` (Liste)
- `date_city`, `date`
- `subject` (Betreff)

**Optional:**
- `sender_contact_phone`, `sender_contact_mobile`, `sender_contact_email`
- `introduction` (Default `Sehr geehrte Damen und Herren`)
- `closing` (Default `Freundliche Grüsse`)
- `signatory_name`, `signatory_role`
- `notes` — dict[str, str], um einzelne Notizoptionen zu ueberschreiben

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

Identisch zum Brief — siehe `references/schreibweisen.md`.

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
