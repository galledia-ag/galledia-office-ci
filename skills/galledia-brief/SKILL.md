---
name: galledia-brief
description: >
  Erstellt einen Geschaeftsbrief im Galledia-CI/CD (Markenhandbuch v1.5).
  Verwende diesen Skill IMMER, wenn der User einen Brief, Geschaeftsbrief,
  Anschreiben, Kundenbrief, Offertschreiben, Mahnung oder ein aehnliches
  Schreiben im Namen einer Galledia-Organisationseinheit erstellen will.
  Triggert auf: "Brief", "schreibe einen Brief", "Geschaeftsbrief",
  "Anschreiben", "Kundenbrief", "Schreiben an", "Offertschreiben",
  "Begleitbrief", "Bewerbungsschreiben (von Galledia an Kandidat)".
  Liefert eine fertige .docx im Galledia-CI als Download.
  Arbeitssprache: Schweizer Hochdeutsch (ss statt scharf-s, also "Grüsse"
  nicht "Grüße"). Die Dokumentengenerierung erfolgt ausschliesslich ueber
  den MCP-Server galledia-office (kein lokales Python-Skript noetig).
version: "0.0.6"
---

# Galledia Geschaeftsbrief

Du hilfst dem User, einen CI/CD-konformen Geschaeftsbrief zu erstellen.
Die eigentliche Generierung macht der MCP-Server `galledia-office`
(siehe https://github.com/galledia-ag/office-ci-mcp), der die offizielle
Galledia-Vorlage automatisch befuellt — Logo, Volte-Schrift, Schutzzone,
Adresszeile, Schreibweisen kommen alle korrekt aus der Vorlage.

## Workflow

### Schritt 1 — Daten sammeln (Hard-Stop bei fehlenden Pflichtfeldern)

**Briefe muessen versandfertig generiert werden — keine Platzhalter, keine
`<TODO>`-Markierungen, keine "wird vom User in Word ergaenzt".** Wenn ein
Pflichtfeld fehlt ODER Claude sich unsicher ist (z.B. Vorname unbekannt,
nur Initiale, OE nicht eindeutig): **STOP**, gezielte Rueckfrage stellen,
KEIN MCP-Aufruf bevor alles vollstaendig ist.

Frage NIE nach Daten, die der User schon genannt hat. Werte, die eindeutig
ableitbar sind (heutiges Datum, Sender-Stadt aus OE-Adresse): selbstaendig
setzen und kurz erwaehnen.

#### Pflichtfelder — ABSENDER (Galledia-Mitarbeiter)

| Feld | Beispiel | Pflicht |
|---|---|---|
| `sender_oe` (Aktiengesellschaft) | `Galledia Fachmedien AG` | ✅ |
| `sender_first_name` | `Stefan` | ✅ |
| `sender_last_name` | `Zimmermann` | ✅ |
| `sender_street` | `Buckhauserstrasse 24` | ✅ |
| `sender_zip` + `sender_city` | `8048 Zürich` | ✅ |
| `sender_contact_email` | `stefan.zimmermann@galledia.ch` | ✅ |
| `sender_contact_phone` ODER `sender_contact_mobile` (mind. eines) | `T +41 58 344 96 22` / `M +41 79 555 12 34` | ✅ (eines davon) |

OE muss exakt eine der 5 sein: `galledia group ag` (klein!), `Galledia Fachmedien AG`,
`Galledia Regionalmedien AG`, `Galledia Print AG`, `Galledia Digital AG`.

Legacy-Feld: `sender_contact_name` wird automatisch aus `sender_first_name` + `sender_last_name`
zusammengesetzt — du musst es nicht separat angeben.

#### Pflichtfelder — EMPFAENGER

| Feld | Beispiel | Pflicht |
|---|---|---|
| `recipient_salutation` | `Herr` / `Frau` (ggf. mit Titel: `Frau Dr.`) | ✅ |
| `recipient_first_name` | `Hans` | ✅ |
| `recipient_last_name` | `Mueller` | ✅ |
| `recipient_company` (falls Firma) | `Mueller AG` | ⬜ optional, aber meist da |
| `recipient_street` | `Bahnhofstrasse 1` | ✅ |
| `recipient_zip` + `recipient_city` | `8001 Zuerich` | ✅ |

Diese Felder werden im MCP-Payload zu `recipient_lines` (Liste, je Zeile ein Eintrag) zusammengefuegt.

#### Pflichtfelder — ALLGEMEIN

| Feld | Beispiel | Pflicht |
|---|---|---|
| `date_city` | `Zuerich` | ✅ |
| `date` | `28. Mai 2026` | ✅ |
| `subject` | `Offerte fuer Inserat Q3 2026` | ✅ |
| `body` | Brieftext (siehe Body-Format unten) | ✅ |

#### Anrede — HART (nie generisch wenn Name bekannt)

| Empfaenger | Anrede (`introduction`) |
|---|---|
| `recipient_salutation = Herr`, Name bekannt | `Sehr geehrter Herr {Nachname}` |
| `recipient_salutation = Frau`, Name bekannt | `Sehr geehrte Frau {Nachname}` |
| Mit Titel | `Sehr geehrter Herr Dr. {Nachname}` |
| Nur Firmenadresse, kein Personenname | `Sehr geehrte Damen und Herren` |

**Niemals** `Sehr geehrte Damen und Herren` wenn der Empfaenger-Name bekannt ist —
das ist ein Briefkultur-Fehler und wirkt unprofessionell.

#### Optionale Felder

- `closing` — Default `Freundliche Grüsse`
- `signatory_name`, `signatory_role` (mehrere Rollen via `\n` oder Array)
- `enclosures` — Liste der Beilagen (z.B. `["Offerte_Q3_2026.pdf", "AGB.pdf"]`)
- `copy_to` — CC-Empfaenger
- `recipient_company` — wenn Empfaenger einer Firma zugeordnet ist

#### Body-Format

- Doppelte Newlines `\n\n` = Absatzwechsel
- Einfache Newlines `\n` = Zeilenumbruch im selben Absatz
- Zeilen mit `· ` am Anfang werden zu Word-Aufzaehlungspunkten

#### Rueckfrage-Beispiele

Wenn ein Feld fehlt, **gezielt fragen**, nicht generisch:

✅ "Wie heisst der Empfaenger genau? Ich brauche Anrede (Herr/Frau), Vor- und Nachname."
✅ "Welche Telefon- oder Mobilnummer soll ich im Absenderblock auffuehren?"
✅ "Welche Rechtseinheit soll als Absender stehen — Fachmedien AG, Regionalmedien AG, Print AG, Digital AG oder galledia group ag?"

❌ "Bitte gib mir noch alle fehlenden Infos." (zu vage)
❌ "Soll ich einen Default verwenden?" (Defaults sind verboten bei Personendaten)

### Schritt 2 — CI-Validierung im Kopf

Pruefe vor dem Aufruf:
- OE exakt eine der 5 erlaubten Schreibweisen
- Telefonformat **zwingend** `T +41 58 344 96 22` bzw. `M +41 79 555 12 34` (mit Leerzeichen, ohne Bindestrich)
- E-Mail plausibel (Format `vorname.nachname@galledia.ch` oder `@fachmedien.ch`)
- Anrede konsistent mit `recipient_salutation` (Herr/Frau ↔ "Sehr geehrter Herr" / "Sehr geehrte Frau")
- Keine geraden Anfuehrungszeichen — Galledia verlangt `« »` (Guillemets)
- Keine verbotenen Begriffe: "Galledia AG", "Galledia Gruppe", "Galledia GmbH", "Fax"

Bei Verstoss: User darauf hinweisen, **KEIN Brief generieren**.

### Schritt 2a — Versandfertig-Checkliste (Pflicht vor MCP-Call)

Bevor du `mcp__galledia-office__generate_galledia_brief` aufrufst, fasse den
Brief in einem kompakten Block zusammen und hole vom User eine Bestaetigung:

```
Bereit zum Generieren — bitte kurz pruefen:

ABSENDER:    Stefan Zimmermann, Galledia Fachmedien AG
             Buckhauserstrasse 24, 8048 Zuerich
             stefan.zimmermann@galledia.ch, T +41 58 344 96 22

EMPFAENGER:  Herr Hans Mueller
             Mueller AG, Bahnhofstrasse 1, 8001 Zuerich

DATUM:       Zuerich, 28. Mai 2026
BETREFF:     Offerte fuer Inserat Q3 2026
ANREDE:      Sehr geehrter Herr Mueller
GRUSS:       Freundliche Gruesse / Stefan Zimmermann
BEILAGEN:    Offerte_Q3_2026.pdf

Alles korrekt? Dann generiere ich den Brief.
```

Bei "ja" / Bestaetigung → MCP-Call. Bei Korrekturen → anpassen und erneut zeigen.
Bei Unsicherheit (User antwortet vage) → nicht generieren, nachfragen.

### Schritt 3 — MCP-Tool aufrufen

Rufe `mcp__galledia-office__generate_galledia_brief` mit dem gesammelten
JSON-Datensatz auf.

Das Tool liefert zurueck:
- `filename` — z.B. `Brief_Offerte_2026.docx`
- `mimetype` — Word-Dokument
- `download_url` — fertiger HTTPS-Link zur Datei (TTL 1h)
- `size_bytes`, `expires_in_seconds`, `report`, `validation_errors`

Bei `validation_errors`: Fehler dem User zeigen und korrekte Werte
vorschlagen, dann erneut.

### Schritt 4 — Link dem User praesentieren

**WICHTIG: Versuche NIE selbst, die `download_url` per HTTP/curl/web_fetch
herunterzuladen.** Das ist nicht dein Job — das macht der User selbst.
Praesentiere die URL einfach als Markdown-Link mit dem `filename` als
sichtbarem Text:

```markdown
Hier ist der Brief: [Brief_Offerte_2026.docx](https://office-mcp.epimetheus.uk/files/...)

Gueltig fuer 60 Minuten.
```

Antworte kurz und sachlich. Wiederhole nicht den ganzen Brieftext im
Chat — der User oeffnet die Datei in Word. Erwaehne nur stichwortartig
was generiert wurde (Empfaenger, Betreff) und ob es Hinweise gibt
(z.B. Validierungs-Warnings die ok sind).

## CI-Regeln (Markenhandbuch v1.5)

Siehe `references/schreibweisen.md`, `references/adressbloecke.md` und
`references/markenhandbuch_kurzfassung.md` fuer die vollstaendigen Regeln
und Standort-Adressen.

## Was NICHT in diesem Skill

- Kurzbrief mit Standardoptionen → `galledia-kurzbrief`
- PowerPoint-Praesentation → `galledia-praesentation`
- Offerten / Angebote → laufen ueber das CRM-Buchungs-Tooling
  (`fachmedien-mediaberatung`-Plugin)
