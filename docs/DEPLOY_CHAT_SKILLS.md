# Chat Skills deployen

Skills im **Claude Chat** (Web/Desktop/Mobile) werden separat provisioniert –
unabhängig vom Cowork-Plugin (das via Git-Sync automatisch aktuell bleibt).

## Überblick

| Surface | Mechanismus | Sync |
|---|---|---|
| Cowork (Plugin) | marketplace.json → Git-Sync | automatisch nach Push |
| Chat (Web/Desktop) | Org Settings → Skills → Upload SKILL.md | manuell nach Push |

---

## Einmalig: Org-Setup

### 1. Code Execution aktivieren (Voraussetzung für Präsentation + Dokument)
Organization settings → Capabilities:
- [x] Code execution and file creation
- [x] Skills

### 2. MCP-Connector für Brief + Kurzbrief (Chat)
Organization settings → Connectors → MCP hinzufügen:
- Name: `galledia-office`
- URL: `https://office-mcp.epimetheus.uk/mcp`

---

## Skills hochladen

Organization settings → Skills → **[+ Upload]** → jeweilige SKILL.md-Datei wählen

| Skill | Datei im Repo | Tool | Status |
|---|---|---|---|
| Präsentation | `skills/galledia-praesentation/SKILL.md` | Code Execution | ✅ bereit |
| Brief | `skills/galledia-brief/SKILL.md` | MCP galledia-office | ✅ bereit (MCP-Connector nötig) |
| Kurzbrief | `skills/galledia-kurzbrief/SKILL.md` | MCP galledia-office | ✅ bereit (MCP-Connector nötig) |
| Dokument | `skills/galledia-dokument/SKILL.md` | Code Execution | ⏳ Vorlage ausstehend |

**Wichtig:** Nur die SKILL.md-Datei hochladen — nicht helpers.py oder Assets.
Der Präsentations-Skill holt fehlende Assets zur Laufzeit von GitHub:
```
https://raw.githubusercontent.com/galledia-ag/galledia-office-ci/main/skills/galledia-praesentation/
```

---

## Update-Prozess nach Git-Änderungen

```bash
# 1. Änderung in Git committen + pushen
git add -A && git commit -m "..." && git push origin main

# 2. Cowork: automatisch (Marketplace-Sync, bis 30 Min.)

# 3. Chat: manuell re-upload
#    Organization settings → Skills → [Skill anklicken] → [Neu hochladen]
#    → aktualisierte SKILL.md aus lokalem Repo-Ordner wählen
```

---

## Aktivierungsstatus (für Org-Owner konfigurierbar)

- **Default on**: Skill ist für alle Mitglieder automatisch aktiv
- **Available**: Erscheint im Katalog, MA aktivieren selbst
- **Required**: Fest für alle, nicht deaktivierbar

Empfehlung: `galledia-praesentation` und `galledia-brief` → **Default on**

---

## Roadmap Chat-Skills

| Version | Änderung |
|---|---|
| v1.0.0 (jetzt) | Präsentation per Code Execution in Chat verfügbar |
| v1.1.0 | Brief + Kurzbrief auf Code Execution umgestellt (kein MCP-Connector mehr nötig) |
| v1.2.0 | Dokument-Skill (sobald Designer-Vorlage geliefert) |
