"""Build handoff/PLAN.pdf (Gantt chart, task table, notes) from handoff/PLAN.md.

PLAN.md is the source of truth. Edit it, then run:  python tools/build_plan_pdf.py
"""
import os, re, sys, io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                Image, PageBreak, KeepTogether)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "handoff", "PLAN.md")
OUT = os.path.join(HERE, "..", "handoff", "PLAN.pdf")

OWNER_COL = {"You": "#D97706", "Claude": "#1D70B8", "Both": "#7C3AED", "External": "#64748B"}
INK, MUTED, BORDER, ROW = "#1E293B", "#64748B", "#CBD5E1", "#F1F5F9"


def parse(md):
    lines = md.splitlines()
    tasks, notes, done_lines, intro, how = [], {}, [], [], []
    extra = {}
    section, cur = None, None
    for ln in lines:
        if ln.startswith("## "):
            section, cur = ln[3:].strip(), None
            continue
        if section not in (None, "Tasks", "Task notes", "How to use it") and not section.startswith("Already done"):
            extra.setdefault(section, []).append(ln)
            continue
        if section == "Tasks" and re.match(r"\| [A-Z]\d+ \|", ln):
            c = [x.strip() for x in ln.strip().strip("|").split("|")]
            needs = [] if c[3] in ("-", "") else [x.strip() for x in c[3].split(",")]
            tasks.append(dict(id=c[0], task=c[1], owner=c[2], needs=needs, days=float(c[4]), model=c[5], status=c[6]))
        elif section == "Task notes":
            m = re.match(r"### ([A-Z]\d+)\s+(.*)", ln)
            if m:
                cur = m.group(1); notes[cur] = []
            elif cur and ln.strip().startswith("- "):
                notes[cur].append(ln.strip()[2:])
        elif section and section.startswith("Already done") and ln.strip().startswith("- "):
            done_lines.append(ln.strip()[2:])
        elif section == "How to use it" and ln.strip().startswith("- "):
            how.append(ln.strip()[2:])
        elif section is None and ln.strip() and not ln.startswith("#"):
            intro.append(ln.strip())
    return tasks, notes, done_lines, how, " ".join(intro), extra


def schedule(tasks):
    by = {t["id"]: t for t in tasks}
    for t in tasks:
        for n in t["needs"]:
            if n not in by:
                sys.exit(f"{t['id']} needs unknown task {n}")
    memo = {}
    def start(i, stack=()):
        if i in stack:
            sys.exit(f"dependency cycle at {i}")
        if i not in memo:
            t = by[i]
            memo[i] = max([start(n, stack + (i,)) + by[n]["days"] for n in t["needs"]], default=0.0)
        return memo[i]
    for t in tasks:
        t["start"] = start(t["id"]); t["end"] = t["start"] + t["days"]
    # critical path: walk back from the task that ends last
    last = max(tasks, key=lambda t: t["end"]); crit = set(); cur = last
    while cur:
        crit.add(cur["id"])
        prev = [by[n] for n in cur["needs"] if abs(by[n]["end"] - cur["start"]) < 1e-9]
        cur = max(prev, key=lambda t: t["days"]) if prev else None
    for t in tasks:
        t["critical"] = t["id"] in crit
    return sorted(tasks, key=lambda t: (t["start"], "EQHT".find(t["id"][0]), int(t["id"][1:])))


def gantt(tasks):
    n = len(tasks)
    fig, ax = plt.subplots(figsize=(10.2, 0.27 * n + 1.1), dpi=200)
    plt.rcParams["font.family"] = "DejaVu Sans"
    for y, t in enumerate(tasks):
        optional = t["task"].lower().startswith("optional")
        done = t["status"].lower().startswith("done")
        col = "#0D9488" if done else OWNER_COL.get(t["owner"], MUTED)
        w = max(t["days"], 0.12)
        ax.barh(y, w, left=t["start"], height=0.62, color=col, alpha=0.45 if optional else 0.95,
                hatch="///" if optional else None, edgecolor=INK if t["critical"] else col,
                linewidth=1.4 if t["critical"] else 0.5)
        ax.text(t["end"] + 0.15, y, f"{t['model']}" + ("  (done)" if done else ""), va="center",
                fontsize=6.3, color=MUTED)
    ax.set_yticks(range(n))
    ax.set_yticklabels([f"{t['id']}  {t['task'][:60]}" for t in tasks], fontsize=6.6, color=INK)
    ax.invert_yaxis()
    ax.set_xlabel("Days from start (rough calendar span; tasks start when everything they need is done)", fontsize=7, color=MUTED)
    ax.tick_params(axis="x", labelsize=6.5, colors=MUTED)
    ax.set_xlim(0, max(t["end"] for t in tasks) + 2.2)
    ax.grid(axis="x", color=BORDER, linewidth=0.5); ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    handles = [Patch(color=c, label=k) for k, c in OWNER_COL.items()]
    handles += [Patch(facecolor="white", edgecolor=INK, linewidth=1.4, label="Critical path"),
                Patch(facecolor="#CBD5E1", hatch="///", label="Optional")]
    ax.legend(handles=handles, ncol=6, fontsize=6.5, frameon=False, loc="lower left",
              bbox_to_anchor=(0, 1.0))
    fig.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=200); plt.close(fig); buf.seek(0)
    return buf, fig.get_size_inches()


def inline(s):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"`([^`]+)`", r'<font face="Courier" size="7.5">\1</font>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    return s


def render_section(lines, body, small, bullet, uw):
    out, table, para = [], [], []
    def flush_para():
        if para:
            out.append(Paragraph(inline(" ".join(para)), body)); out.append(Spacer(1, 3)); para.clear()
    def flush_table():
        if not table:
            return
        rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in table if not re.match(r"^\|[-| ]+\|$", r.strip())]
        ncol = len(rows[0]); w = uw / ncol
        widths = [w * f for f in ([1.25, 0.95, 0.9, 1.25, 1.85, 0.6] if ncol == 6 else [1] * ncol)]
        widths = [x * uw / sum(widths) for x in widths]
        data = [[Paragraph(("<b>%s</b>" % inline(c)) if i == 0 else inline(c), small) for c in r] for i, r in enumerate(rows)]
        t = Table(data, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor(BORDER)),
                               ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                               ("VALIGN", (0, 0), (-1, -1), "TOP")] +
                              [("BACKGROUND", (0, i), (-1, i), colors.HexColor(ROW)) for i in range(2, len(data), 2)]))
        out.append(t); out.append(Spacer(1, 5)); table.clear()
    for ln in lines:
        st = ln.strip()
        if st.startswith("|"):
            flush_para(); table.append(st)
        elif st.startswith("- "):
            flush_para(); flush_table(); out.append(Paragraph(inline(st[2:]), bullet, bulletText="•"))
        elif not st:
            flush_para(); flush_table()
        else:
            flush_table(); para.append(st)
    flush_para(); flush_table()
    return out


def build():
    tasks, notes, done_lines, how, intro, extra = parse(open(SRC, encoding="utf8").read())
    tasks = schedule(tasks)
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=8.6, leading=11.2, textColor=colors.HexColor(INK))
    small = ParagraphStyle("s", parent=body, fontSize=7.6, leading=9.4)
    h1 = ParagraphStyle("h1", parent=body, fontName="Helvetica-Bold", fontSize=17, leading=21, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=body, fontName="Helvetica-Bold", fontSize=11.5, leading=14, spaceBefore=8, spaceAfter=4)
    h3 = ParagraphStyle("h3", parent=body, fontName="Helvetica-Bold", fontSize=8.8, leading=11, spaceBefore=5, spaceAfter=1)
    bullet = ParagraphStyle("bl", parent=body, leftIndent=10, bulletIndent=2)

    pw, ph = landscape(letter); m = 0.5 * inch; uw = pw - 2 * m
    doc = SimpleDocTemplate(OUT, pagesize=(pw, ph), leftMargin=m, rightMargin=m, topMargin=m, bottomMargin=m,
                            title="LostInSteering work plan", author="LostInSteering")
    st = [Paragraph("LostInSteering work plan", h1), Paragraph(inline(intro), body), Spacer(1, 4)]
    st += [Paragraph(inline(x), bullet, bulletText="•") for x in how]

    st += [Paragraph("Already done", h2)] + [Paragraph(inline(x), bullet, bulletText="•") for x in done_lines]
    for name in [k for k in extra if k.startswith("Decisions")]:
        st += [Paragraph(name, h2)] + render_section(extra[name], body, small, bullet, uw)
    ready = [t for t in tasks if not t["status"].lower().startswith("done")
             and all(next(u for u in tasks if u["id"] == n)["status"].lower().startswith("done") for n in t["needs"])]
    st += [Paragraph("Can start now", h2),
           Paragraph("Everything these tasks need is done. Critical-path tasks (outlined in the chart) set the finish date, so start those first.", small), Spacer(1, 3)]
    st += [Paragraph(inline(f"<b>{t['id']}</b> {t['task']} ({t['owner']}, {t['model']})" + ("  [critical path]" if t["critical"] else "")).replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>"),
                     bullet, bulletText="•") for t in ready]

    img, (wi, hi) = gantt(tasks)
    scale = min(uw / (wi * inch), (ph - 2 * m - 0.75 * inch) / (hi * inch))
    st += [PageBreak(), Paragraph("Dependency chart", h2),
           Image(img, width=wi * inch * scale, height=hi * inch * scale)]

    st += [PageBreak(), Paragraph("Tasks in dependency order", h2),
           Paragraph("Start is the earliest day a task can begin once everything in Needs is finished. "
                     "Tasks with the same start can run in parallel. Bold IDs are on the critical path.", small), Spacer(1, 4)]
    hdr = ["Start", "ID", "Task", "Owner", "Needs", "Model", "Status"]
    rows = [[Paragraph(f"<b>{h}</b>", small) for h in hdr]]
    for t in tasks:
        idtxt = f"<b>{t['id']}</b>" if t["critical"] else t["id"]
        rows.append([Paragraph(f"{t['start']:g}", small), Paragraph(idtxt, small), Paragraph(inline(t["task"]), small),
                     Paragraph(t["owner"], small), Paragraph(", ".join(t["needs"]) or "-", small),
                     Paragraph(t["model"], small), Paragraph(t["status"], small)])
    cw = [0.45, 0.4, 4.6, 0.7, 1.2, 0.7, 0.9]
    tbl = Table(rows, colWidths=[c * inch for c in cw], repeatRows=1)
    style = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor(BORDER)),
             ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for i, t in enumerate(tasks, 1):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor(ROW)))
        style.append(("TEXTCOLOR", (3, i), (3, i), colors.HexColor(OWNER_COL.get(t["owner"], MUTED))))
    tbl.setStyle(TableStyle(style)); st.append(tbl)
    for name in [k for k in extra if not k.startswith("Decisions")]:
        st += [PageBreak(), Paragraph(name, h2)] + render_section(extra[name], body, small, bullet, uw)

    st += [PageBreak(), Paragraph("Task notes", h2)]
    by = {t["id"]: t for t in tasks}
    for tid in sorted(notes, key=lambda x: ("EQHT".find(x[0]), int(x[1:]))):
        t = by.get(tid)
        head = f"{tid}  {inline(t['task'])}" if t else tid
        meta = f"{t['owner']} · needs {', '.join(t['needs']) or 'nothing'} · {t['model']} · {t['status']}" if t else ""
        block = [Paragraph(head, h3), Paragraph(f'<font color="{MUTED}">{inline(meta)}</font>', small)]
        block += [Paragraph(inline(x), bullet, bulletText="•") for x in notes[tid]]
        st.append(KeepTogether(block))

    def footer(c, d):
        c.saveState(); c.setFont("Helvetica", 7); c.setFillColor(colors.HexColor(MUTED))
        c.drawString(m, 0.3 * inch, "Built from handoff/PLAN.md by tools/build_plan_pdf.py. Edit the markdown, not this PDF.")
        c.drawRightString(pw - m, 0.3 * inch, f"Page {d.page}"); c.restoreState()
    doc.build(st, onFirstPage=footer, onLaterPages=footer)
    print("wrote", os.path.normpath(OUT), "with", len(tasks), "tasks")


if __name__ == "__main__":
    build()
