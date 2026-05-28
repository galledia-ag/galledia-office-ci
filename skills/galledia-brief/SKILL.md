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
---

# Galledia Geschaeftsbrief

Du hilfst dem User, einen CI/CD-konformen Geschaeftsbrief zu erstellen.
Die eigentliche Generierung macht der MCP-Server `galledia-office`
(siehe https://github.com/galledia-ag/office-ci-mcp), der die offizielle
Galledia-Vorlage automatisch befuellt — Logo, Volte-Schrift, Schutzzone,
Adresszeile, Schreibweisen kommen alle korrekt aus der Vorlage.

## Workflow

### Schritt 1 — Daten sammeln

Frage den User nach **fehlenden Pflichtfeldern**. Frage NIE nach Daten, die
der User schon in seiner Anfrage genannt hat. Ableitbare Werte
(z.B. aktuelles Datum, Absender-Name aus Kontext) selbstaendig setzen und
nur kurz erwaehnen.

**Pflichtfelder:**
- `sender_oe` — eine von: `galledia group ag` (klein!),
  `Galledia Fachmedien AG`, `Galledia Regionalmedien AG`,
  `Galledia Print AG`, `Galledia Digital AG`
- `sender_street`, `sender_city` (z.B. `Buckhauserstrasse 24` / `8048 Zürich`)
- `sender_contact_name` (Sachbearbeiter:in)
- `recipient_lines` — Liste von Strings (Empfaenger-Adresse, je Zeile ein Eintrag)
- `date_city` (Absendeort, z.B. `Zürich`) und `date` (z.B. `28. Mai 2026`)
- `subject` (Betreff)
- `body` (Brieftext)

**Optionale Felder:**
- `sender_contact_phone` — Format `T +41 58 344 96 22`
- `sender_contact_mobile` — Format `M +41 78 846 24 16`
- `sender_contact_email`
- `introduction` — Default `Sehr geehrte Damen und Herren`
- `closing` — Default `Freundliche Grüsse`
- `signatory_name`, `signatory_role` (mehrere Rollen via `\n` trennen
  oder als Array)
- `enclosures`, `copy_to`

**Body-Format:**
- Doppelte Newlines `\n\n` = Absatzwechsel
- Einfache Newlines `\n` = Zeilenumbruch im selben Absatz
- Zeilen mit `· ` am Anfang werden zu Word-Aufzaehlungspunkten

### Schritt 2 — CI-Validierung im Kopf

Pruefe vor dem Aufruf:
- Schreibweise der OE exakt eine der 5 erlaubten
- Telefonformat `T +41 …` / `M +41 …`
- Keine geraden Anfuehrungszeichen — Galledia verlangt `« »` (Guillemets)
- Keine verbotenen Begriffe: "Galledia AG", "Galledia Gruppe",
  "Galledia GmbH", "Fax" (letzteres verwendet Galledia nicht mehr)

Bei Verstoss: User darauf hinweisen, KEIN Brief generieren.

### Schritt 3 — MCP-Tool aufrufen

Rufe `mcp__galledia-office__generate_galledia_brief` mit dem gesammelten
JSON-Datensatz auf.

Das Tool liefert zurueck:
- `filename` — z.B. `Brief_Offerte_2026.docx`
- `mimetype` — Word-Dokument
- `content_base64` — Datei-Inhalt
- `size_bytes`, `report`, `validation_errors`

Bei `validation_errors`: Fehler dem User zeigen und korrekte Werte
vorschlagen, dann erneut.

Bei Erfolg: Datei dem User als Download anbieten.

## CI-Regeln (Markenhandbuch v1.5)

Siehe `references/schreibweisen.md`, `references/adressbloecke.md` und
`references/markenhandbuch_kurzfassung.md` fuer die vollstaendigen Regeln
und Standort-Adressen.

## Was NICHT in diesem Skill

- Kurzbrief mit Standardoptionen → `galledia-kurzbrief`
- PowerPoint-Praesentation → `galledia-praesentation`
- Offerten / Angebote → laufen ueber das CRM-Buchungs-Tooling
  (`fachmedien-mediaberatung`-Plugin)
