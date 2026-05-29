# -*- coding: utf-8 -*-
"""3-Folien-Test mit Pattern-Architektur."""
import sys
sys.path.insert(0, r"C:\Users\zimste\Projekte\office-ci-mcp")
from pathlib import Path
from src.generators.fill_praesentation import fill, TEMPLATE_PATH

data = {
    "organisation": "Galledia Fachmedien AG",
    "enforce_mandatory_slides": False,
    "slides": [
        {
            "pattern": "hero_split",
            "hero_text": "AI HUB",
            "hero_subtitle": "Motorex AG\nForschung & Entwicklung",
            "title": "Modularer On-Site AI-Hub",
            "description": "Lokale KI-Infrastruktur für die F&E – sicher, skalierbar, lizenzfrei.",
            "bullets": [
                "Datensicherheit – keine Cloud",
                "Open Source – keine Lizenzkosten",
                "Phase 1 → Phase 2 ohne Neuinvestition",
            ],
            "footer": "Konzept · Mai 2026",
        },
        {
            "pattern": "numbered_agenda",
            "title": "Agenda",
            "slide_no": 2, "total": 3,
            "context": "F&E AI-Hub Konzept",
            "items": [
                {"title": "Ausgangslage & Ziel", "teaser": "Warum brauchen wir einen lokalen AI-Hub?"},
                {"title": "Kernprinzipien", "teaser": "Datensicherheit, Open Source, Modularität"},
                {"title": "Hardware & Skalierung", "teaser": "Stufenweise Investition Phase 1 → 2"},
                {"title": "Phasenplan & Roadmap", "teaser": "Konkrete Schritte und Zeitrahmen"},
            ],
        },
        {
            "pattern": "card_grid_3",
            "title": "Drei Kernprinzipien",
            "slide_no": 3, "total": 3,
            "context": "F&E AI-Hub Konzept",
            "cards": [
                {
                    "icon": "🛡",
                    "title": "Datensicherheit",
                    "bullets": [
                        "Alle Daten lokal auf eigenem Server",
                        "Keine Cloud-API-Aufrufe",
                        "Rezepturen, SAP & LIMS geschützt",
                        "Strikte Zugriffskontrolle via ACLs",
                    ],
                },
                {
                    "icon": "⊜",
                    "title": "Keine Lizenzkosten",
                    "bullets": [
                        "Open-Source-Modelle (Llama, Mistral)",
                        "Einmalige Hardware-Investition",
                        "Keine Kosten pro User oder API-Call",
                        "Kein Vendor-Lock-in",
                    ],
                },
                {
                    "icon": "⚡",
                    "title": "Modularität",
                    "bullets": [
                        "Start: PDF & Office-Dokumente",
                        "Phase 2: SAP, CRM, LIMS über API",
                        "Plug-and-Play: OCR, Vision, Whisper",
                        "Docker-Container: einfach erweiterbar",
                    ],
                },
            ],
        },
    ],
}

out = Path(r"C:\Users\zimste\Projekte\Galledia_CI_CD_Office-Dokumente\test\Patterns_Test.pptx")
report = fill(data, TEMPLATE_PATH, out)
print(f"Output: {out}")
print(f"Slides: {report.get('slides_added')}")
