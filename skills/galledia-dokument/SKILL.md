---
name: galledia-dokument
description: >
  Erstellt ein laengeres Galledia-Dokument (.docx) — fuer Offerten,
  Anleitungen, Konzepte, Reports, technische Dokumentationen,
  Whitepapers, Pflichten-/Lastenhefte. Verwende diesen Skill immer wenn
  ein User ein MEHRSEITIGES Galledia-Dokument braucht — KEIN Brief
  (das ist galledia-brief) und KEIN Kurzbrief (das ist galledia-
  kurzbrief). Triggert auf: "Dokument", "Offerte" (mehrseitig),
  "Angebot (Doku)", "Anleitung", "Manual", "Handbuch", "Konzept",
  "Report", "Studie", "Dokumentation", "Whitepaper", "Pflichtenheft",
  "Lastenheft". Liefert eine .docx im Galledia-CI mit korrektem Theme
  (Galledia2018-1, vollstaendige Akzentfarben-Palette).
---

# Galledia Dokument

Du erstellst ein laengeres Galledia-Dokument auf Basis der offiziellen
Dokumentvorlage. Das Dokument hat Cover-Seite, Header mit Logo, Footer
mit Adressblock, korrektes Galledia-Theme (Volte + alle Akzentfarben) —
und Platz fuer Body-Inhalt, den der User in Word selbst editiert.

## V1-Scope (heute)

Das Tool liefert das **Geruest** mit Theme + Header/Footer + Cover-Titel.
Den Body-Inhalt schreibt der User selbst in Word — die Vorlage zeigt
eine Beispiel-Struktur. Der User loescht/ueberschreibt diese.

## Workflow

### Schritt 1 — Daten sammeln

**Pflichtfeld:** `sender_oe` (eine der 5 OE).

**Optional:** `sender_street`, `sender_city`, `sender_contact_name`,
`sender_contact_phone`, `sender_contact_mobile`, `sender_contact_email`,
`recipient_lines`, `date_city`, `date`, `signatory_name`, `signatory_role`.

**Wichtig: `cover_title`** — ersetzt die Original-Ueberschrift des
Templates. Setze hier den gewuenschten Dokumenttitel, z.B.
`Konzept Digital-Marketing 2026` oder `Anleitung Buchungsformular V2`.

### Schritt 2 — CI-Validierung

Wie bei Brief — siehe `references/schreibweisen.md`.

### Schritt 3 — MCP-Tool aufrufen

`mcp__galledia-office__generate_galledia_dokument` mit dem JSON.

### Schritt 4 — Link + Hinweis

Download-Link als Markdown-Link mit Filename praesentieren. PLUS:
dem User klar sagen, dass er die Beispiel-Inhalte in Word ueberschreiben
oder loeschen muss — das Skill liefert das Geruest, nicht den Inhalt.

**WICHTIG: Niemals selbst die download_url per HTTP/curl/web_fetch
herunterladen.**

## Was NICHT in diesem Skill

- 1-seitiger Brief → `galledia-brief`
- Begleitschreiben / Memo → `galledia-kurzbrief`
- Praesentation → `galledia-praesentation`
