# -*- coding: utf-8 -*-
"""3-Folien-Test: Titelfolie + Inhaltsfolie + Schlussfolie."""
import sys
sys.path.insert(0, r"C:\Users\zimste\Projekte\office-ci-mcp")
from pathlib import Path
from src.generators.fill_praesentation import fill, TEMPLATE_PATH

data = {
    "organisation": "Galledia Fachmedien AG",
    "enforce_mandatory_slides": False,  # keine Agenda dazwischen
    "date": "28. Mai 2026",
    "slides": [
        {
            "layout": "title",
            "title": "Galledia Office CI",
            "subtitle": "Testfoliensatz für Stefan",
        },
        {
            "layout": "content",
            "title": "Was das Plugin kann",
            "subtitle": "Vier Dokumenttypen im CI/CD",
            "content": "Brief — 1-seitiges Anschreiben\nKurzbrief — Begleitschreiben mit 10 Notizoptionen\nPräsentation — PowerPoint mit 16 Galledia-Layouts\nDokument — mehrseitige Vorlage für Offerten/Anleitungen",
        },
        {
            "layout": "section",
        },
    ],
}

out = Path(r"C:\Users\zimste\Projekte\Galledia_CI_CD_Office-Dokumente\test\Testfoliensatz_3.pptx")
report = fill(data, TEMPLATE_PATH, out)
print(f"Output: {out}")
print(f"Slides: {report.get('slides_added')}  /  Footer-Layouts gepatcht: {report.get('footer_layouts_patched')}")
