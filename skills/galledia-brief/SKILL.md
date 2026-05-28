---
name: galledia-brief
description: >
  Erstellt einen Geschaeftsbrief im Galledia-CI/CD (Markenhandbuch v1.5).
  Verwende diesen Skill IMMER, wenn der User einen Brief, Geschaeftsbrief,
  Anschreiben, Kundenbrief, Offertschreiben, Mahnung oder ein aehnliches
  Schreiben im Namen einer Galledia-Organisationseinheit erstellen will.
  Triggert auf: "Brief", "schreibe einen Brief", "Geschaeftsbrief",
  "Anschreiben", "Kundenbrief", "Schreiben an", "Offertschreiben",
  "Begleitbrief". Liefert eine fertige .docx im Galledia-CI als Download.
  Arbeitssprache: Schweizer Hochdeutsch (ss statt ss, also "Grüsse" nicht "Grüße").
---

# Galledia Geschaeftsbrief

Du erstellst CI/CD-konforme Geschaeftsbriefe fuer die Galledia-Gruppe. Die
offizielle Word-Vorlage (`templates/Brief-Vorlage Galledia.dotx`) liegt
mit im Skill und enthaelt Logo, Volte-Schrift, Schutzzone und Adresszeile
bereits korrekt — die fuellst du nur noch mit Inhalten. Das Python-Skript
`scripts/fill_brief.py` uebernimmt die XML-Manipulation und liefert eine
fertige `.docx`.

---

## Workflow (in dieser Reihenfolge)

### Schritt 1 — Daten sammeln

Frage den User nach allen fehlenden Pflicht-Feldern. Frage NIE nach Daten,
die der User in seiner Anfrage schon genannt hat. Wenn ein Feld plausibel
abgeleitet werden kann (z.B. Datum = heute, sender_contact_name aus Kontext),
nutze die Ableitung und erwaehne sie kurz.

### Schritt 2 — Validierung gegen Galledia-CI

Pruefe vor dem Generieren:

- **Organisationseinheit** ist genau eine von:
  `galledia group ag` (klein!), `Galledia Fachmedien AG`,
  `Galledia Regionalmedien AG`, `Galledia Print AG`, `Galledia Digital AG`
- **Telefonformat**: `T +41 58 344 96 22` bzw. `M +41 79 XXX XX XX`
  (Praefix `T`/`M`, Leerzeichen, `+41` Pflicht)
- **Sonderzeichen**: Bullets `·`, Anfuehrungszeichen `« »` (nie `"`),
  Trenner `|`. KEIN `-`, `•`, `*` als Aufzaehlung.
- **Verboten**: "Galledia AG", "Galledia Gruppe", "Fax"

Bei Verstoss: KEIN Brief generieren, sondern den User auf den Fehler
hinweisen und korrigieren lassen.

### Schritt 3 — Brief generieren

Baue ein JSON-Objekt mit allen Daten zusammen (siehe Schema unten) und
rufe `fill_brief.py` via Python aus. Das Skript validiert nochmal,
befuellt die Vorlage und schreibt die `.docx`-Datei.

**Aufruf** (Python-Code-Tool, NICHT Shell):

```python
import json, subprocess, sys
from pathlib import Path

skill_dir = Path(__file__).parent if "__file__" in dir() else Path.cwd()
# Wenn skill_dir nicht stimmt: nutze den Skill-Pfad aus dem Plugin-Kontext

data = {
    "sender_oe": "...",
    "sender_street": "...",
    # ... (siehe Schema)
}

output_path = "/tmp/brief.docx"  # oder ein anderer schreibbarer Pfad
result = subprocess.run(
    [sys.executable, str(skill_dir / "scripts" / "fill_brief.py"),
     "--input", "-", "--output", output_path],
    input=json.dumps(data), text=True, capture_output=True
)
print(result.stdout)
if result.returncode != 0:
    print("FEHLER:", result.stderr)
```

Alternative — falls `subprocess` nicht verfuegbar oder unkomfortabel:
importiere direkt:

```python
import sys
sys.path.insert(0, str(skill_dir / "scripts"))
from fill_brief import fill, ValidationError

try:
    report = fill(data, skill_dir / "templates" / "Brief-Vorlage Galledia.dotx",
                  Path(output_path))
    print(report)
except ValidationError as e:
    print("CI-Verstoss:", e)
```

### Schritt 4 — Ergebnis dem User liefern

- Bei Erfolg: Die `.docx`-Datei dem User zum Download anbieten
- Bei Validierungsfehler: Fehlertext anzeigen, korrekte Werte vorschlagen,
  erneut versuchen

---

## JSON-Schema

### Pflichtfelder

| Feld | Beispiel | Hinweis |
|---|---|---|
| `sender_oe` | `Galledia Fachmedien AG` | exakte Schreibweise — siehe `references/schreibweisen.md` |
| `sender_street` | `Buckhauserstrasse 24` | |
| `sender_city` | `8048 Zürich` | mit PLZ |
| `sender_contact_name` | `Stefan Zimmermann` | Sachbearbeiter:in |
| `recipient_lines` | `["Müller AG", "Hans Müller", "Bahnhofstrasse 1", "8001 Zürich"]` | Array, je Zeile ein Eintrag |
| `date_city` | `Zürich` | Absendeort, ohne PLZ |
| `date` | `28. Mai 2026` | Datum |
| `subject` | `Offerte für Inserate-Kampagne 2026` | Betreff |
| `body` | siehe unten | Brieftext |

### Optional

| Feld | Beispiel | Default |
|---|---|---|
| `sender_contact_phone` | `T +41 58 344 96 22` | — |
| `sender_contact_mobile` | `M +41 78 846 24 16` | — |
| `sender_contact_email` | `vorname.nachname@galledia.ch` | — |
| `introduction` | `Sehr geehrter Herr Müller` | `Sehr geehrte Damen und Herren` |
| `closing` | `Freundliche Grüsse` | `Freundliche Grüsse` |
| `signatory_name` | `Stefan Zimmermann` | = `sender_contact_name` |
| `signatory_role` | siehe unten | — |
| `enclosures` | `Beilagen: Offerte 2026-123` | — |
| `copy_to` | `Kopie an: Geschäftsleitung` | — |

### Body-Format

`body` ist ein String. Regeln:

- **Absatzwechsel:** Doppelter Newline `\n\n`
- **Zeilenumbruch im selben Absatz:** Einfacher Newline `\n`
- **Bullet-Liste:** Zeile mit `· ` am Anfang → wird zu Word-Aufzaehlung
  (Style `Aufzhlungszeichen`). Der `·` im Input erscheint **nicht** im
  Output — Word setzt den richtigen Bullet-Punkt automatisch.

Beispiel:
```
"vielen Dank für Ihr Interesse.\n\nWir bieten:\n· Basic: …\n· Premium: …\n\nGerne …"
```

### signatory_role (mehrere Rollen)

- String mit `\n`-Trenner: `"Leitung Fachmedien & Digital\nMitglied der Gruppenleitung"`
- Oder Array: `["Leitung Fachmedien & Digital", "Mitglied der Gruppenleitung"]`

---

## Was NICHT zu diesem Skill gehoert

- Offerten/Angebote → das macht `fachmedien-mediaberatung`-Plugin via CRM
- Kurzbrief → kommt in V2 als separater Skill `galledia-kurzbrief`
- Praesentation → V3, separater Skill `galledia-praesentation`

## Referenzen im Skill-Bundle

- `references/schreibweisen.md` — 5 OE, Telefon, Sonderzeichen
- `references/adressbloecke.md` — alle Galledia-Standorte mit Adressen
- `references/markenhandbuch_kurzfassung.md` — extrahierte CI-Kernregeln
- `templates/Brief-Vorlage Galledia.dotx` — die offizielle Word-Vorlage
- `scripts/fill_brief.py` — Befuellungs-Skript (lxml, kein python-docx)
- `scripts/example_input.json` — vollstaendiges Beispiel-Input
