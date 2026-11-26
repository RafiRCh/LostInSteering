"""Build a shareable PDF from handoff/review/review.md.

Steps: parse front matter, convert Markdown to HTML (tables, sane lists),
turn image lines into numbered figures (grey placeholder when the file is
missing), write review.html, print it with Microsoft Edge headless, and
report the page count with PyMuPDF.

Run from anywhere:  python "<repo>/handoff/review/build_pdf.py"
"""

import html
import re
import subprocess
import sys
import time
from pathlib import Path

import fitz  # PyMuPDF
import markdown

HERE = Path(__file__).resolve().parent
import sys as _sys
# Optional: python build_pdf.py <source.md> <output.pdf>
SRC_MD = HERE / (_sys.argv[1] if len(_sys.argv) > 1 else "review.md")
OUT_HTML = SRC_MD.with_suffix(".html")
OUT_PDF = HERE / (_sys.argv[2] if len(_sys.argv) > 2 else "LostInSteering_referee_report.pdf")
EDGE = Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")

IMAGE_LINE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")

CSS = """
@page { size: A4; margin: 18mm 16mm; }
:root {
  --ink: #1d1d1f;
  --muted: #5f6368;
  --heading: #1f3a5f;
  --border: #c9cfd6;
  --head-bg: #e6ecf3;
  --note-bg: #f2f4f7;
}
* { box-sizing: border-box; }
html, body { background: #fff; }
body {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 10.5pt;
  line-height: 1.45;
  color: var(--ink);
  margin: 0;
}
.doc-title { font-size: 20pt; color: var(--heading); margin: 0 0 4pt 0; line-height: 1.2; }
.doc-subtitle { font-size: 12pt; color: var(--muted); margin: 0 0 6pt 0; font-style: italic; }
.doc-date { font-size: 9.5pt; color: var(--muted); margin: 0 0 8pt 0; }
.doc-note {
  font-size: 9pt; color: #333; background: var(--note-bg);
  border-left: 3px solid var(--heading); padding: 6pt 9pt; margin: 0 0 14pt 0;
}
.doc-rule { border: 0; border-top: 1px solid var(--border); margin: 0 0 6pt 0; }
h1, h2, h3 {
  font-family: "Segoe UI", Arial, Helvetica, sans-serif;
  color: var(--heading);
  line-height: 1.25;
  page-break-after: avoid;
  break-after: avoid;
}
h1 { font-size: 14pt; margin: 20pt 0 6pt 0; padding-bottom: 3pt; border-bottom: 1px solid var(--border); }
h2 { font-size: 12pt; margin: 14pt 0 4pt 0; }
h3 { font-size: 10.5pt; margin: 10pt 0 3pt 0; }
p { margin: 0 0 7pt 0; orphans: 3; widows: 3; }
ul, ol { margin: 0 0 7pt 0; padding-left: 18pt; }
li { margin: 0 0 3pt 0; }
strong { color: #111; }
code {
  font-family: Consolas, "Courier New", monospace;
  font-size: 9pt; background: #f1f3f5; padding: 0 2pt; border-radius: 2px;
}
table {
  width: 100%; border-collapse: collapse; margin: 4pt 0 10pt 0;
  font-family: "Segoe UI", Arial, Helvetica, sans-serif; font-size: 8.5pt;
  line-height: 1.35;
}
thead { display: table-header-group; }
tr { page-break-inside: avoid; }
th, td { border: 1px solid var(--border); padding: 3pt 5pt; vertical-align: top; text-align: left; }
th { background: var(--head-bg); color: var(--heading); font-weight: bold; }
figure {
  text-align: center; margin: 10pt auto 12pt auto; max-width: 100%;
  page-break-inside: avoid; break-inside: avoid;
}
figure img { max-width: 100%; max-height: 95mm; width: auto; height: auto; display: block; margin: 0 auto; }
p:has(+ ul), p:has(+ ol) { break-after: avoid; page-break-after: avoid; }
figcaption {
  font-size: 9pt; font-style: italic; color: var(--muted);
  margin-top: 4pt; line-height: 1.35; text-align: left;
}
.missing-fig {
  border: 1px dashed #999; background: #e4e4e4; color: #444;
  font-family: Consolas, "Courier New", monospace; font-size: 9pt;
  text-align: center; padding: 28pt 10pt; margin: 0 auto;
}
"""


def parse_front_matter(text):
    """Return (metadata dict, body text). Simple key: value lines only."""
    lines = text.splitlines()
    meta = {}
    if not lines or lines[0].strip() != "---":
        return meta, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return meta, text
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        meta[key.strip()] = value
    body = "\n".join(lines[end + 1:])
    return meta, body


def convert_body(body):
    """Markdown body -> HTML, with figure lines swapped for placeholders."""
    figures = []  # list of (alt, src)
    out_lines = []
    for line in body.splitlines():
        m = IMAGE_LINE.match(line.strip())
        if m:
            token = f"FIGPLACEHOLDER{len(figures)}END"
            figures.append((m.group(1).strip(), m.group(2).strip()))
            out_lines.append(token)
            out_lines.append("")  # blank line so the token is its own paragraph
        else:
            out_lines.append(line)
    html_body = markdown.markdown(
        "\n".join(out_lines), extensions=["tables", "sane_lists"]
    )

    for i, (alt, src) in enumerate(figures):
        number = i + 1
        caption = html.escape(f"Figure {number}. {alt}")
        img_path = (HERE / src).resolve()
        if img_path.is_file():
            uri = html.escape(img_path.as_uri(), quote=True)
            figure = (
                f'<figure><img src="{uri}" alt="{html.escape(alt, quote=True)}">'
                f"<figcaption>{caption}</figcaption></figure>"
            )
        else:
            print(f"  [warn] missing image, placeholder used: {src}")
            figure = (
                "<figure><div class=\"missing-fig\">"
                f"Image not yet available: {html.escape(src)}</div>"
                f"<figcaption>{caption}</figcaption></figure>"
            )
        token = f"FIGPLACEHOLDER{i}END"
        html_body = html_body.replace(f"<p>{token}</p>", figure)
        html_body = html_body.replace(token, figure)
    return html_body, len(figures)


def build_document(meta, body_html):
    title = html.escape(meta.get("title", "Report"))
    subtitle = meta.get("subtitle", "")
    date = meta.get("date", "")
    note = meta.get("note", "")
    parts = [f'<h1 class="doc-title">{title}</h1>']
    if subtitle:
        parts.append(f'<p class="doc-subtitle">{html.escape(subtitle)}</p>')
    if date:
        parts.append(f'<p class="doc-date">{html.escape(date)}</p>')
    if note:
        parts.append(f'<div class="doc-note">{html.escape(note)}</div>')
    parts.append('<hr class="doc-rule">')
    head_block = "\n".join(parts)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
{head_block}
{body_html}
</body>
</html>
"""


def print_pdf(html_uri):
    if not EDGE.is_file():
        sys.exit(f"Microsoft Edge not found at {EDGE}")
    if OUT_PDF.exists():
        OUT_PDF.unlink()
    args = [
        str(EDGE),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={OUT_PDF}",
        html_uri,
    ]
    subprocess.run(args, check=False, timeout=180, capture_output=True)
    # Edge can return before the file is fully written, so poll briefly.
    for _ in range(60):
        if OUT_PDF.is_file() and OUT_PDF.stat().st_size > 0:
            time.sleep(0.5)
            return
        time.sleep(0.5)
    sys.exit("Edge did not produce the PDF")


def main():
    text = SRC_MD.read_text(encoding="utf-8")
    meta, body = parse_front_matter(text)
    body_html, n_fig = convert_body(body)
    OUT_HTML.write_text(build_document(meta, body_html), encoding="utf-8")
    print(f"Wrote {OUT_HTML} ({n_fig} figures)")

    print_pdf(OUT_HTML.as_uri())
    with fitz.open(OUT_PDF) as doc:
        pages = doc.page_count
    print(f"PDF: {OUT_PDF}")
    print(f"Pages: {pages}")


if __name__ == "__main__":
    main()
