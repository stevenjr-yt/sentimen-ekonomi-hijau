"""Generate PDF dari semua dokumen Markdown di folder docs/.
Menggunakan weasyprint + markdown.
"""
import pathlib, markdown, sys

try:
    from weasyprint import HTML, CSS
except ImportError:
    sys.exit("weasyprint not installed. Run: pip install weasyprint")

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DL   = ROOT / "web" / "downloads"
DL.mkdir(parents=True, exist_ok=True)

CSS_STR = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono&display=swap');
@page { margin: 2.2cm 2cm; size: A4; }
body { font-family: 'Inter', Arial, sans-serif; font-size: 11pt; color: #1e293b; line-height: 1.7; }
h1 { font-size: 20pt; color: #064e3b; border-bottom: 3px solid #34d399; padding-bottom: 8px; margin-top: 0; }
h2 { font-size: 15pt; color: #065f46; border-left: 4px solid #34d399; padding-left: 10px; margin-top: 28px; }
h3 { font-size: 12pt; color: #047857; margin-top: 20px; }
h4 { font-size: 11pt; color: #065f46; }
code, pre { font-family: 'JetBrains Mono', 'Courier New', monospace; font-size: 9pt; background: #f1f5f9; padding: 2px 5px; border-radius: 4px; }
pre { padding: 12px 16px; border-left: 3px solid #34d399; overflow-x: auto; }
table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 9.5pt; }
th { background: #064e3b; color: #fff; padding: 8px 10px; text-align: left; }
td { padding: 7px 10px; border-bottom: 1px solid #e2e8f0; }
tr:nth-child(even) td { background: #f8fafc; }
blockquote { border-left: 4px solid #fbbf24; background: #fffbeb; margin: 16px 0; padding: 10px 16px; border-radius: 0 8px 8px 0; }
strong { color: #064e3b; }
a { color: #059669; }
hr { border: none; border-top: 1px solid #e2e8f0; margin: 24px 0; }
.page-break { page-break-before: always; }
"""

files = {
    "Laporan_Project.md": "Laporan_Project.pdf",
    "Paper_Jurnal.md": "Paper_Jurnal.pdf",
    "Studi_Literatur.md": "Studi_Literatur.pdf",
}

for md_name, pdf_name in files.items():
    md_path = DOCS / md_name
    pdf_path = DL / pdf_name
    if not md_path.exists():
        print(f"SKIP {md_name} — tidak ditemukan")
        continue
    md_text = md_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"]
    )
    full_html = f"""<!DOCTYPE html>
<html lang="id">
<head><meta charset="utf-8"/>
<style>{CSS_STR}</style>
</head>
<body>{html_body}</body>
</html>"""
    try:
        HTML(string=full_html, base_url=str(ROOT)).write_pdf(
            str(pdf_path),
            stylesheets=[CSS(string=CSS_STR)]
        )
        size_kb = pdf_path.stat().st_size // 1024
        print(f"✅ {pdf_name} ({size_kb} KB) → {pdf_path}")
    except Exception as e:
        print(f"❌ {pdf_name}: {e}")

print("\nSelesai. PDF tersimpan di web/downloads/")
