"""Draw the revision roadmap chart for the journal-eligibility report."""
from pathlib import Path
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
OUT = HERE / "figures" / "j1_roadmap.png"

# (phase, task, start_week, length_weeks, kind)
TASKS = [
    ("1  Fix", "Correct numbers, abstract, figure issues", 0, 1, "fix"),
    ("1  Fix", "Report the opinion-vector control", 0, 1, "fix"),
    ("1  Fix", "Add statements (data, AI use, funding, COI, ethics)", 0, 1, "fix"),
    ("2  Strengthen", "Paired-bootstrap CIs (retention, persona, languages)", 1, 2, "analysis"),
    ("2  Strengthen", "Read and cite the two 2026 papers; restate novelty", 1, 1, "analysis"),
    ("3  Extend", "Second model family under Run 08 (needs approval)", 2, 4, "compute"),
    ("3  Extend", "Optional: truth-preserving layer or objective", 3, 3, "compute"),
    ("4  Reframe", "Reframe as protocol + benchmark; Zenodo DOI", 5, 2, "write"),
    ("4  Reframe", "Pre-submission scope email to MLST editors", 5, 1, "write"),
    ("5  Submit", "Final check against MLST rules; submit", 7, 1, "submit"),
]
COLORS = {"fix": "#2a6fbb", "analysis": "#5b9bd5", "compute": "#e07b20",
          "write": "#7b4fa0", "submit": "#2e8b57"}
LABELS = {"fix": "Fixes in the text", "analysis": "Analysis on existing data",
          "compute": "New Kaggle runs", "write": "Writing and packaging", "submit": "Submission"}

fig, ax = plt.subplots(figsize=(7.2, 3.9), dpi=200)
n = len(TASKS)
for i, (phase, task, s, d, kind) in enumerate(TASKS):
    y = n - 1 - i
    ax.barh(y, d, left=s, height=0.6, color=COLORS[kind], edgecolor="white")
    ax.text(-0.15, y, task, ha="right", va="center", fontsize=7.5)
ax.set_yticks([])
ax.set_xlim(0, 8)
ax.set_xticks(range(0, 9))
ax.set_xlabel("Week (estimate; depends on Kaggle quota and supervisor approval)", fontsize=8)
ax.tick_params(axis="x", labelsize=7.5)
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.grid(axis="x", color="#e5e5e5", linewidth=0.6)
ax.set_axisbelow(True)
handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS[k]) for k in COLORS]
ax.legend(handles, [LABELS[k] for k in COLORS], fontsize=7, ncol=3, frameon=False,
          loc="upper center", bbox_to_anchor=(0.2, -0.2))
fig.tight_layout()
OUT.parent.mkdir(exist_ok=True)
fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print(OUT)
