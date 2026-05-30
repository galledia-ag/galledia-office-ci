# -*- coding: utf-8 -*-
"""Test der 3 neuen Patterns: kpi_tiles, process_flow, spec_table."""
import sys
sys.path.insert(0, r"C:\Users\zimste\Projekte\office-ci-mcp")
from pathlib import Path
from src.generators.fill_praesentation import fill, TEMPLATE_PATH

data = {
    "organisation": "Galledia Fachmedien AG",
    "date": "29. Mai 2026",
    "enforce_mandatory_slides": False,
    "slides": [
        {
            "title": "Performance-Optimierung pgvector",
            "subtitle": "Vektorsuche im Vergleich",
            "tiles": [
                {"value": "229'073", "label": "Einträge\nin pgvector", "sublabel": "Document Chunks", "color": "red"},
                {"value": "685 ms", "label": "Vektorsuche\nohne Optimierung", "sublabel": "Sequential Scan", "color": "black"},
                {"value": "< 10 ms", "label": "Vektorsuche\nmit HNSW-Index", "sublabel": "Einmaliger Setup-Aufwand: ~2 Min.", "color": "green"},
            ],
            "callout": {
                "title": "Was ist ein HNSW-Index?",
                "text": "HNSW (Hierarchical Navigable Small World) baut eine Navigationskarte über alle Vektoren. Statt alle 229'073 Einträge zu vergleichen (Sequential Scan = 685 ms), springt die Suche direkt zu den ähnlichsten Vektoren. Einmaliger Aufwand: wenige Minuten. Minimaler Qualitätsverlust (~1% geringere Recall-Rate, in der Praxis nicht spürbar).",
                "color": "green",
            },
        },
        {
            "title": "Hardware-Konfiguration",
            "subtitle": "AI-Hub Phase 1",
            "hero": {
                "value": "10–13",
                "unit": "TCHF",
                "label": "Einmalige Investition\nohne laufende Lizenzkosten",
                "accent": "Erweiterbar auf Phase 2",
            },
            "specs": [
                {"label": "GPU", "title": "1× NVIDIA RTX 5090", "subtitle": "32 GB VRAM – Modell + KV-Cache"},
                {"label": "CPU", "title": "AMD Threadripper PRO", "subtitle": "Hohe Taktung für Dokument-Parsing"},
                {"label": "RAM", "title": "128 GB DDR5 ECC", "subtitle": "Aufrüstbar auf 256 GB für Phase 2"},
                {"label": "SSD", "title": "1 TB + 2 TB NVMe", "subtitle": "System/Modelle + Vektorindex"},
                {"label": "Gehäuse", "title": "2× PCIe 5.0 x16 Slots", "subtitle": "Zweite GPU nachrüstbar für Phase 2"},
                {"label": "Netzteil", "title": "Min. 1600W", "subtitle": "Reserve für spätere GPU-Erweiterung"},
            ],
        },
        {
            "title": "Pipeline-Architektur RAG",
            "subtitle": "Dokumentenverarbeitung end-to-end",
            "steps": [
                {"icon": "📄", "title": "Dokument\nEingabe", "subtitle": "PDF, DOCX,\nXLSX, Scans"},
                {"icon": "🔍", "title": "Chunking\n& OCR", "subtitle": "Unstructured.io\nTesseract"},
                {"icon": "💾", "title": "Vektor-\ndatenbank", "subtitle": "pgvector\nPostgreSQL"},
                {"icon": "🖥", "title": "LLM\nInference", "subtitle": "Llama 3\nvia Ollama"},
                {"icon": "📈", "title": "Antwort\nan User", "subtitle": "Open WebUI\nChat-Interface"},
            ],
            "callout": {
                "title": "Was bedeutet RAG?",
                "text": "RAG = Retrieval Augmented Generation: Das Modell antwortet nicht aus dem Training heraus, sondern aus euren konkreten Dokumenten. Sichere, aktuelle, nachvollziehbare Antworten.",
            },
        },
    ],
}

out = Path(r"C:\Users\zimste\Projekte\Galledia_CI_CD_Office-Dokumente\test\NewPatterns.pptx")
report = fill(data, TEMPLATE_PATH, out)
print(f"Output: {out}  Slides: {report.get('slides_added')}")
