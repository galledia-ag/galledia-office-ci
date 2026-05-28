# fill_brief.py

Befuellt die Galledia Brief-Vorlage und liefert eine fertige `.docx`.

## Aufruf

```powershell
# Mit Datei
python fill_brief.py --input data.json --output mein_brief.docx

# Mit stdin
Get-Content data.json | python fill_brief.py --input - --output mein_brief.docx
```

## JSON-Struktur

Siehe `example_input.json`.

| Pflichtfeld | Typ | Beschreibung |
|---|---|---|
| `sender_oe` | string | Eine der 5 OE — siehe `references/schreibweisen.md` |
| `sender_street` | string | z.B. `Buckhauserstrasse 24` |
| `sender_city` | string | z.B. `8048 Zürich` |
| `sender_contact_name` | string | `Vorname Nachname` |
| `recipient_lines` | array[string] | Empfaenger-Adresse, je Zeile ein Eintrag |
| `date_city` | string | Absendeort, z.B. `Zürich` |
| `date` | string | z.B. `28. Mai 2026` |
| `subject` | string | Betreff |
| `body` | string oder array | Brieftext. `\n\n` = neuer Absatz, `\n` = Zeilenumbruch im selben Absatz. Zeilen mit `· ` am Anfang werden zu Word-Bulletpoints (Style `Aufzhlungszeichen`). |

| Optional | Typ | Default |
|---|---|---|
| `sender_contact_phone` | string | — |
| `sender_contact_mobile` | string | — |
| `sender_contact_email` | string | — |
| `introduction` | string | `Sehr geehrte Damen und Herren` |
| `closing` | string | `Freundliche Grüsse` |
| `signatory_name` | string | = `sender_contact_name` |
| `signatory_role` | string oder array | Mehrere Rollen mit `\n` trennen oder als Array uebergeben. Wird je Rolle auf eigener Zeile gerendert. |
| `enclosures` | string | — |
| `copy_to` | string | — |

## Validierung

Das Skript prueft vor dem Generieren:
- OE-Schreibweise gegen die 5 erlaubten Werte
- Telefonformat (`T +41 …` / `M +41 …`)
- Verbotene Begriffe (`Galledia AG`, `Galledia Gruppe`, `Fax`, ...)
- Gerade Anfuehrungszeichen `"` (CI verlangt `« »`)

Bei Verletzung: Exit-Code 2, Fehlertext nach stderr.

## Exit Codes

- `0` — Erfolg
- `2` — Validierungsfehler
- `1` — sonstiger Fehler (z.B. Datei nicht gefunden)
