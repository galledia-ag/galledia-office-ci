# -*- coding: utf-8 -*-
"""Generate test presentation with the same structure that failed before."""
import sys
sys.path.insert(0, r"C:\Users\zimste\Projekte\office-ci-mcp")
from pathlib import Path
from src.generators.fill_praesentation import fill, TEMPLATE_PATH

data = {
    "organisation": "Galledia Fachmedien AG",
    "slides": [
        {
            "layout": "title",
            "title": "Digitaler Zwilling",
            "subtitle": "Mein persönlicher KI-Assistent — 24/7 verfügbar",
        },
        {
            "layout": "content",
            "title": "Vision & Ziel",
            "subtitle": "Ein KI-System, das mich kennt",
            "content": "· Aggregation aller Kanäle: E-Mail, WhatsApp, Dokumente\n· Volltext- und Vektorsuche über 50 000+ Nachrichten\n· Automatische Klassifizierung, Priorisierung und Antwortvorschläge",
        },
        {
            "layout": "content",
            "title": "Architektur & Stack",
            "subtitle": "Workflow & Daten",
            "content": "· n8n 2.17.7 — vollautomatische Verarbeitungs-Pipelines\n· Supabase (Schema «arbeit»): 52 000+ Nachrichten, 223 000+ Dokument-Chunks\n· Embeddings: nomic-embed-text via Ollama",
        },
        {
            "layout": "content",
            "title": "Status & Nächste Schritte",
            "subtitle": "Wo wir stehen",
            "content": "· Message-Embeddings & Summaries: 100 %\n· INBOUND-Klassifizierung (Urgency, Sentiment): 100 %\n· OUTBOUND-Backfill (~55 %) und Dokument-Chunking (~52 %) laufen",
        },
    ],
}

out = Path(r"C:\Users\zimste\Projekte\Galledia_CI_CD_Office-Dokumente\test\Praes_Digitaler_Zwilling_v2.pptx")
report = fill(data, TEMPLATE_PATH, out)
print(f"Output: {out}")
print(f"Slides: {report.get('slides_added')}")
print(f"Auto-injected: {report.get('auto_injected_slides', 0)}")
