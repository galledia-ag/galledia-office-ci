---
name: galledia-brief
description: Erstellt einen Geschaeftsbrief im Galledia-CI/CD (gemaess Markenhandbuch v1.5). Verwende diesen Skill IMMER, wenn der User einen Brief, Geschaeftsbrief, Anschreiben, Kundenbrief, Offertschreiben, Mahnung oder ein aehnliches Schreiben im Namen einer Galledia-Organisationseinheit erstellen will. Triggert auf: "Brief", "schreibe einen Brief", "Geschaeftsbrief", "Anschreiben", "Kundenbrief", "Schreiben an", "Offertschreiben", "Begleitbrief", "Bewerbungsschreiben (von Galledia an Kandidat)". Liefert eine fertige .docx im Galledia-CI.
---

# Galledia Geschaeftsbrief

Dieser Skill befuellt die offizielle Galledia-Brief-Vorlage (`templates/Brief-Vorlage Galledia.dotx`) ueber `python-docx` und liefert eine fertige `.docx`. Layout, Schriften (Volte), Logo, Schutzzone und Adresszeile kommen automatisch aus der Vorlage — du musst sie nicht selbst gestalten.

## Workflow (in dieser Reihenfolge)

1. **Daten sammeln** — frage den User nach allem, was fehlt (siehe Felder unten). Frage nicht nach Daten, die der User schon in der Anfrage genannt hat.
2. **Validieren** gegen `references/schreibweisen.md` — insbesondere OE-Schreibweise und Telefonformat. Bei Verstoss: nachfragen, NICHT raten.
3. **Skript aufrufen** mit gesammelten Daten (siehe "Aufruf" unten).
4. **Ergebnis** dem User als Pfad zur generierten Datei melden.

## Pflicht-Felder

| Feld | Beispiel | Quelle / Default |
|---|---|---|
| `sender_oe` | `Galledia Fachmedien AG` | User fragen; Default nach Kontext (siehe Mail-Adresse des Users) |
| `sender_street` | `Buckhauserstrasse 24` | aus `references/adressbloecke.md` (je nach Standort) |
| `sender_city` | `8048 Zuerich` | aus `references/adressbloecke.md` |
| `sender_contact_name` | `Stefan Zimmermann` | Aktueller User (aus `userEmail`-Context ableitbar) |
| `sender_contact_role` | `Leitung Fachmedien & Digital` | User fragen falls unbekannt |
| `sender_contact_phone` | `T +41 58 344 96 22` | User fragen falls unbekannt |
| `sender_contact_mobile` | `M +41 78 846 24 16` | optional |
| `sender_contact_email` | `stefan.zimmermann@galledia.ch` | aus userEmail |
| `recipient_lines` | `["Mueller AG", "Hans Mueller", "Bahnhofstrasse 1", "8001 Zuerich"]` | User fragen |
| `date_city` | `Zuerich` | leitet sich aus `sender_city` ab |
| `date` | `28. Mai 2026` | heute oder vom User vorgegeben |
| `subject` | `Offerte fuer Inserate-Kampagne 2026` | User fragen |
| `introduction` | `Sehr geehrter Herr Mueller` | Default `Sehr geehrte Damen und Herren` falls User nichts sagt |
| `body` | mehrere Absaetze | User-Anfrage. Bullets: jede Zeile mit `· ` am Anfang wird zum Word-Aufzaehlungspunkt (kein literaler `·` im Output). Zwei Newlines `\n\n` = Absatzwechsel; ein Newline `\n` = Zeilenumbruch im selben Absatz. |
| `closing` | `Freundliche Gruesse` | Default |
| `signatory_name` | `Stefan Zimmermann` | meist = sender_contact_name |
| `signatory_role` | `Leitung Fachmedien & Digital\nMitglied der Gruppenleitung` | optional. Mehrere Rollen mit `\n` trennen (eine Rolle pro Zeile). Alternativ als JSON-Array `["Rolle 1", "Rolle 2"]`. |
| `enclosures` | `Beilagen: Offerte 2026-123` | optional |
| `copy_to` | `Kopie an: Geschaeftsleitung` | optional |

## CI-Regeln (Pflicht — bei Verstoss validiert das Skript)

- **OE-Schreibweise**: Genau eine der 5 in `references/schreibweisen.md`. `galledia group ag` IMMER klein. Toechter immer Gross.
- **Telefonformat**: `T +41 58 344 XX XX` bzw. `M +41 79 XXX XX XX` — Praefix `T`/`M`, Leerzeichen, Laendervorwahl Pflicht.
- **Sonderzeichen im Text**: Bullets `·` (Mittelpunkt), Anfuehrungszeichen `«` `»` (Guillemets), Trenner `|`. KEIN `-`, `•`, `*` als Aufzaehlung. KEIN `"` als Anfuehrung.
- **Fax**: NICHT mehr verwenden.
- **Schreibweise im Text**: Keine "Galledia AG", keine "Galledia Gruppe", keine "Galledia GmbH".

## Aufruf

Das Skript liegt unter `scripts/fill_brief.py`. Aufruf ueber eine JSON-Eingabe:

```powershell
python "<skill-dir>/scripts/fill_brief.py" --input <data.json> --output <out.docx>
```

Beispiel-Daten siehe `scripts/example_input.json`.

Der Skill nimmt die User-Anfrage entgegen, baut die JSON-Struktur im Speicher und ruft das Skript mit `--input -` (stdin) auf, um keine temporaere Datei anzulegen — siehe `scripts/README.md`.

## Was NICHT in diesem Skill liegt

- Offerten / Angebote: laufen ueber das CRM-Buchungs-Tooling (`buchungsformular_*`)
- Kurzbrief: kommt in V2 (separates Skill `galledia-kurzbrief`)
- Praesentation: kommt in V3 (separates Skill `galledia-praesentation`)

## Referenzen

- `references/schreibweisen.md` — OE, Telefon, Sonderzeichen
- `references/adressbloecke.md` — Standorte und deren Adressen
- `references/markenhandbuch_kurzfassung.md` — extrahierte Kernregeln aus dem Markenhandbuch
- `templates/Brief-Vorlage Galledia.dotx` — die Word-Vorlage (NICHT direkt editieren — Aenderungen ueber PR)
