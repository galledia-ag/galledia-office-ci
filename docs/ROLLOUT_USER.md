# Roll-out für Galledia-Mitarbeitende — galledia-office-ci

Diese Anleitung richtet sich an alle Galledia-MA, die mit Claude
Geschäftsdokumente (Briefe, Kurzbriefe, Präsentationen) im offiziellen
Galledia-CI/CD erstellen wollen.

## Voraussetzungen

- Cowork-Zugang auf claude.ai (Galledia-Organisation)
- Galledia-E-Mail (für Cloudflare-Access-Authentifizierung)
- Word und PowerPoint installiert (für das Öffnen der generierten Dateien)

**Keine** lokale Python-Installation, **kein** Claude Code, **keine**
zusätzlichen Tools nötig — der MCP-Server läuft zentral.

## Installation (einmalig, ~2 Minuten)

1. claude.ai öffnen → mit Galledia-Account einloggen
2. **Sidebar → Plugins** (oder Organisationseinstellungen → Plugins)
3. Plugin `galledia-office-ci` suchen → **Installieren** klicken
4. Neue Chat-Session öffnen

Das war's. Beim ersten Aufruf wird Cloudflare Access dich per Email-PIN
authentifizieren — danach ist die Verbindung gespeichert.

## Verwendung

### Brief schreiben

Einfach in einem Chat formulieren — z.B.:

> Schreibe mir einen Brief an die Müller AG, Hans Müller, Bahnhofstrasse 1,
> 8001 Zürich. Betreff: Offerte für Q3 2026. Inhalt: kurze Vorstellung
> unseres Angebots mit drei Paketen (Basic, Premium, Custom) und einer
> Bitte um Rückruf.

Claude sammelt fehlende Daten (z.B. dein Standort), generiert das Dokument
und liefert dir einen Download-Link. Du klickst → Word öffnet sich → fertig.

**Slash-Command-Variante:**
```
/brief Empfänger Müller AG, Hans Müller, Bahnhofstrasse 1, 8001 Zürich. Betreff: Offerte Q3 2026.
```

### Kurzbrief / Begleitschreiben

Für 1-seitige Begleitschreiben mit Checkboxen ("zur Kenntnisnahme",
"Beilagen:", etc.):

> Erstelle einen Kurzbrief an die ABC AG, Anna Beispiel, Beispielstrasse 1,
> 8001 Zürich. Betreff: Unterlagen zur Vertragsunterzeichnung.
> Beilagen: Vertrag, AGB, NDA.

Oder via Slash-Command: `/kurzbrief`

### Präsentation

> Erstelle eine Präsentation für die ABC AG: Titelfolie "Vorstellung
> Galledia Fachmedien", Untertitel "ABC AG | 28. Mai 2026". Agenda mit
> 4 Punkten. Inhaltsfolie zu unseren Stärken. Zwischenfolie "Nächste
> Schritte" in rot.

Oder via Slash-Command: `/praesentation`

## Was ist im CI eingehalten

- Logo (Galledia-G in Rot)
- Volte-Schriftart
- 5 Organisationseinheiten in korrekter Schreibweise:
  - `galledia group ag` (klein)
  - `Galledia Fachmedien AG`
  - `Galledia Regionalmedien AG`
  - `Galledia Print AG`
  - `Galledia Digital AG`
- Telefonformat `T +41 58 344 96 22` / `M +41 79 XXX XX XX`
- Sonderzeichen: Bullets `·`, Anführungszeichen `« »`, Trenner `|`
- Standort-Adressen aller Galledia-Niederlassungen
- Kein "Fax" mehr (laut Markenhandbuch v1.5)

Falls du versuchst, "Galledia AG" oder "Galledia Gruppe" zu schreiben,
weist das System das ab — kein Dokument im falschen CI.

## Troubleshooting

### "VM service not running" oder ähnliche Sandbox-Fehler

Das ist kosmetisch — das Plugin nutzt einen externen MCP-Server, nicht die
Cowork-Sandbox. Falls die Fehlermeldung kommt: einfach den Inhalt der
Antwort scrollen, der Download-Link kommt trotzdem.

### Cloudflare-Access-Login wiederholt nötig

Cookies löschen oder Browser im Inkognito-Modus testen. Falls persistent:
Bei IT melden.

### Tool wurde nicht getriggert

Sag explizit "Brief schreiben" / "Kurzbrief erstellen" / "Präsentation
machen" — Claude erkennt die Schlüsselwörter aus den Skill-Descriptions.

### Datei sieht nicht im CI aus

Sehr selten — kann passieren wenn die Volte-Schrift in Word nicht
installiert ist. Beim IT-Team Schrift-Paket anfragen: `Volte Regular`,
`Volte Semibold`, `Volte Rounded Regular`, `Volte Rounded Semibold`.

### Anderer Fehler

E-Mail an [stefan.zimmermann@galledia.ch](mailto:stefan.zimmermann@galledia.ch)
mit Screenshot.

## Datenschutz

- Generierte Dokumente bleiben **60 Minuten** auf dem MCP-Server und
  werden danach automatisch gelöscht
- Niemand ausser dem authentifizierten Galledia-User kann auf die Download-
  Links zugreifen (Cloudflare Access + Token-basierte URLs)
- Eingegebene Daten gehen via Cowork → MCP-Server → bleiben im
  Galledia-Netzwerk

## Was geht (noch) nicht

- **Bilder/Diagramme** in Präsentationen — manuell in PowerPoint einfügen
- **Tabellen** im Brief — manuell in Word ergänzen
- **Mailmerge** für Serienbriefe — in Arbeit, V0.6
- **Direkte Anbindung an CRM** für Empfänger-Daten — separater Workflow
  via `fachmedien-mediaberatung`-Plugin
