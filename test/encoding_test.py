"""Test encoding scenarios for fill_brief.py input — all 5 should succeed now."""
import json, sys, subprocess, zipfile, re
from pathlib import Path

base = Path(r"C:\Users\zimste\Projekte\Galledia_CI_CD_Office-Dokumente")
input_data = {
    "sender_oe": "Galledia Fachmedien AG",
    "sender_street": "Buckhauserstrasse 24",
    "sender_city": "8048 Zürich",
    "sender_contact_name": "Stefan Zimmermann",
    "recipient_lines": ["Müller AG", "Hans Müller", "Bahnhofstrasse 1", "8001 Zürich"],
    "date_city": "Zürich",
    "date": "28. Mai 2026",
    "subject": "Vorstellung",
    "body": "Test mit Umlauten: ä ö ü\n\n· Bullet eins\n· Bullet zwei",
    "introduction": "Sehr geehrter Herr Müller",
    "signatory_name": "Stefan Zimmermann",
    "signatory_role": "Leitung Fachmedien & Digital\nMitglied der Gruppenleitung",
}

# Test 5: Pre-mojibaked input (simulates what Claude apparently sent)
mojibake_data = {
    k: (v.encode("utf-8").decode("latin-1") if isinstance(v, str) else
        [s.encode("utf-8").decode("latin-1") if isinstance(s, str) else s for s in v] if isinstance(v, list) else v)
    for k, v in input_data.items()
}
# Spot check
print(f"Mojibake sample: sender_city = {mojibake_data['sender_city']!r}  (should look broken)")
print(f"Mojibake sample: body = {mojibake_data['body'][:50]!r}")

scenarios = [
    ("utf8",     base/"test"/"in_utf8.json",     lambda p: p.write_text(json.dumps(input_data, ensure_ascii=False), encoding="utf-8")),
    ("cp1252",   base/"test"/"in_cp1252.json",   lambda p: p.write_text(json.dumps(input_data, ensure_ascii=False), encoding="cp1252")),
    ("utf8_bom", base/"test"/"in_utf8_bom.json", lambda p: p.write_text(json.dumps(input_data, ensure_ascii=False), encoding="utf-8-sig")),
    ("ascii",    base/"test"/"in_ascii.json",    lambda p: p.write_text(json.dumps(input_data, ensure_ascii=True), encoding="utf-8")),
    ("mojibake", base/"test"/"in_mojibake.json", lambda p: p.write_text(json.dumps(mojibake_data, ensure_ascii=False), encoding="utf-8")),
]

script = base / "skills" / "galledia-brief" / "scripts" / "fill_brief.py"
all_ok = True
for name, p, writer in scenarios:
    writer(p)
    out = base / "test" / f"out_{name}.docx"
    out.unlink(missing_ok=True)
    r = subprocess.run([sys.executable, str(script), "--input", str(p), "--output", str(out)],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        print(f"  {name}: FAIL (rc={r.returncode})")
        print(f"    stderr: {r.stderr[:400]}")
        all_ok = False
        continue
    # Verify the document text doesn't contain mojibake
    with zipfile.ZipFile(str(out), "r") as zf:
        doc = zf.read("word/document.xml").decode("utf-8")
    has_mojibake = any(m in doc for m in ("Ã¼", "Ã¶", "Ã¤", "Â·"))
    has_correct_umlauts = "Müller" in doc and "Zürich" in doc
    status = "OK" if (not has_mojibake and has_correct_umlauts) else f"WRONG (mojibake={has_mojibake}, correct={has_correct_umlauts})"
    print(f"  {name}: {status}")
    if has_mojibake:
        all_ok = False

print(f"\n{'ALL TESTS PASSED' if all_ok else 'SOME TESTS FAILED'}")
