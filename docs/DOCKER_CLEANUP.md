# Docker-Cleanup: MCP-Server PPTX-Endpoint deprecieren

## Status nach v1.0.0

| Funktion | MCP-Route | Status |
|---|---|---|
| Brief (.docx) | `generate_galledia_brief` | ✅ aktiv — noch benötigt |
| Kurzbrief (.docx) | `generate_galledia_kurzbrief` | ✅ aktiv — noch benötigt |
| Präsentation (.pptx) | `generate_galledia_praesentation` | ⚠️ deprecated — nicht mehr aufgerufen |

## Was zu tun ist

Die MCP-Instanz (`office-mcp.epimetheus.uk`, Docker auf Mac Studio) läuft
weiter für Brief + Kurzbrief. Der PPTX-Endpoint wird nicht mehr aufgerufen.

**Sofortmassnahmen (optional, da kein Schaden durch toten Code):**
```bash
# Im office-ci-mcp Repo: PPTX-Route auskommentieren oder entfernen
# Danach rebuild + restart:
cd ~/Projekte/office-ci-mcp
docker compose up -d --build mcp-server
```

**Vollständige MCP-Abschaltung** (erst wenn Word-Skills gebaut sind):
1. `skills/galledia-brief/SKILL.md` und `galledia-kurzbrief/SKILL.md` auf
   Code Execution umstellen (analog zur Präsentation)
2. `.mcp.json` aus diesem Repo entfernen
3. `plugin.json`: `"mcpServers"` entfernen
4. Docker-Container stoppen:
   ```bash
   cd ~/Projekte/office-ci-mcp
   docker compose down
   ```
5. Optional: Cloudflare Tunnel für `office-mcp.epimetheus.uk` deaktivieren

## Nächster Schritt

Word-Skills (Kurzbrief, Brief, Dokument) als Code-Execution-Skills bauen —
analog `galledia-praesentation`. Dann vollständige MCP-Ablösung möglich.
