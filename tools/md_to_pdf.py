"""Render a simple Markdown file (headings, paragraphs, bullets, numbered lists, tables) to a PDF.

Usage: python tools/md_to_pdf.py input.md output.pdf
"""
import re, sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

INK, MUTED, BORDER, ROW, HEAD = "#1E293B", "#64748B", "#CBD5E1", "#F1F5F9", "#E2E8F0"


def inline(s):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"`([^`]+)`", r'<font face="Courier">\1</font>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    return s


def build(src, dst):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=10, leading=13.6,
                          textColor=colors.HexColor(INK), spaceAfter=5)
    small = ParagraphStyle("s", parent=body, fontSize=8.8, leading=11, spaceAfter=0)
    h1 = ParagraphStyle("h1", parent=body, fontName="Helvetica-Bold", fontSize=17, leading=21, spaceAfter=8)
    h2 = ParagraphStyle("h2", parent=body, fontName="Helvetica-Bold", fontSize=12.5, leading=16, spaceBefore=10, spaceAfter=4)
    bullet = ParagraphStyle("bl", parent=body, leftIndent=14, bulletIndent=3, spaceAfter=3)
    m = 0.9 * inch
    pw, ph = letter
    uw = pw - 2 * m
    doc = SimpleDocTemplate(dst, pagesize=letter, leftMargin=m, rightMargin=m, topMargin=m, bottomMargin=m)
    st, para, table = [], [], []

    def flush_para():
        if para:
            st.append(Paragraph(inline(" ".join(para)), body)); para.clear()

    def flush_table():
        if not table:
            return
        rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in table if not re.match(r"^\|[-| :]+\|$", r.strip())]
        n = len(rows[0])
        lens = [max(len(r[i]) for r in rows) for i in range(n)]
        w = [min(max(l, 16), 70) for l in lens]   # keep short columns readable, long ones from taking over
        widths = [uw * x / sum(w) for x in w]
        data = [[Paragraph(("<b>%s</b>" % inline(c)) if i == 0 else inline(c), small) for c in r] for i, r in enumerate(rows)]
        t = Table(data, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor(BORDER)),
                               ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(HEAD)),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)] +
                              [("BACKGROUND", (0, i), (-1, i), colors.HexColor(ROW)) for i in range(2, len(data), 2)]))
        st.append(Spacer(1, 3)); st.append(t); st.append(Spacer(1, 8)); table.clear()

    for ln in open(src, encoding="utf8").read().splitlines():
        s = ln.strip()
        num = re.match(r"^(\d+)\. (.*)", s)
        if s.startswith("# "):
            flush_para(); flush_table(); st.append(Paragraph(inline(s[2:]), h1))
        elif s.startswith("## "):
            flush_para(); flush_table(); st.append(Paragraph(inline(s[3:]), h2))
        elif s.startswith("|"):
            flush_para(); table.append(s)
        elif s.startswith("- "):
            flush_para(); flush_table(); st.append(Paragraph(inline(s[2:]), bullet, bulletText="•"))
        elif num:
            flush_para(); flush_table(); st.append(Paragraph(inline(num.group(2)), bullet, bulletText=num.group(1) + "."))
        elif not s:
            flush_para(); flush_table()
        elif re.match(r"^(Prepared for|From|Date|Status):", s):
            flush_para(); st.append(Paragraph(f'<font color="{MUTED}">{inline(s)}</font>', ParagraphStyle("meta", parent=body, spaceAfter=1)))
        else:
            flush_table(); para.append(s)
    flush_para(); flush_table()

    def footer(c, d):
        c.saveState(); c.setFont("Helvetica", 8); c.setFillColor(colors.HexColor(MUTED))
        c.drawRightString(pw - m, 0.5 * inch, f"Page {d.page}"); c.restoreState()
    doc.build(st, onFirstPage=footer, onLaterPages=footer)
    print("wrote", dst)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
