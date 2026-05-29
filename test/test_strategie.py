# -*- coding: utf-8 -*-
"""Reproduktion der Strategie-Fachmedien-Praesentation MIT Auto-Patterns."""
import sys
sys.path.insert(0, r"C:\Users\zimste\Projekte\office-ci-mcp")
from pathlib import Path
from src.generators.fill_praesentation import fill, TEMPLATE_PATH

data = {
    "organisation": "Galledia Fachmedien AG",
    "date": "29. Mai 2026",
    "slides": [
        {
            "title": "Strategie Fachmedien 2026",
            "subtitle": "Portfolio · Fusion · KI-Roadmap",
        },
        # Agenda wird automatisch eingefuegt
        {
            "title": "Grösse und aktuelle Zahlen",
            "subtitle": "Portfolio & Q1/2026-Performance",
            "content": "Über 119 Fach- und Verbandsmedien sowie 80+ Online-Plattformen\nNettoertrag Q1/2026: TCHF 4'522 (–315 vs. Budget, –279 vs. Vorjahr)\nDB III Q1/2026: TCHF 362 (–156 vs. Budget)\nEBIT Q1/2026: TCHF –146 (negativ)\nThemen-Cluster: Auto/Motorrad, Bau/Immo, Management, Sicherheit, Transport",
            "body_size": "small",
        },
        {
            "title": "Drei Säulen der Strategie",
            "subtitle": "Strategische Ausrichtung 2026",
            "cards": [
                {"icon": "📦", "title": "Portfolio-Bereinigung",
                 "bullets": ["Schwache Verlagsobjekte abstossen", "Fokus auf Top-30 Marken", "Cluster-Optimierung"]},
                {"icon": "🤝", "title": "Fusion mit ZSW",
                 "bullets": ["Closing 1.6.2026", "Synergien Vertrieb", "Geteilte Infrastruktur"]},
                {"icon": "🤖", "title": "KI-Roadmap",
                 "bullets": ["Lokaler AI-Hub", "Automatisierte Recherche", "Content-Beschleunigung"]},
            ],
        },
        # Schlussfolie wird automatisch angehaengt
    ],
}

out = Path(r"C:\Users\zimste\Projekte\Galledia_CI_CD_Office-Dokumente\test\Strategie_v2.pptx")
report = fill(data, TEMPLATE_PATH, out)
print(f"Output: {out}")
print(f"Slides: {report.get('slides_added')}")
print(f"Auto-injected: {report.get('auto_injected_slides', 0)}")
