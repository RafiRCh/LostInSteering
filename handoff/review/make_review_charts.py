import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = "D:/Cloud Extension/QPAIN/Working paper/LostInSteering"
R = ROOT + "/results/08_unified_scale_run/"
OUT = ROOT + "/handoff/review/figures/"
P = {
    "0.5B": R + "notebook_3_0.5b/run08_notebook_3/Qwen2.5-0.5B-Instruct-fp16/",
    "1.5B": R + "run08_notebook_1/Qwen2.5-1.5B-Instruct-fp16/",
    "3B": R + "run08_notebook_1/Qwen2.5-3B-Instruct-fp16/",
    "7B": R + "notebook_1_final/run08_notebook_1/Qwen2.5-7B-Instruct-fp16/",
    "14B": R + "run08_notebook_2/Qwen2.5-14B-Instruct-nf4/",
}
P7R = R + "7b_dose_all_langs_recheck/run08_notebook_1/Qwen2.5-7B-Instruct-fp16/"
LANGS = ["en", "es", "zh", "hi", "bn", "ar"]
LN = {"en": "English", "es": "Spanish", "zh": "Chinese", "hi": "Hindi", "bn": "Bengali", "ar": "Arabic"}
BLUE, ORANGE, GREY, DARK, PURPLE = "#2a6fbb", "#e07b20", "#9a9a9a", "#444444", "#7b4fa0"
plt.rcParams.update({"font.size": 9.5, "axes.facecolor": "white", "figure.facecolor": "white",
                     "axes.spines.top": False, "axes.spines.right": False,
                     "savefig.dpi": 200, "savefig.facecolor": "white"})


def save(fig, name):
    fig.savefig(OUT + name, dpi=200, bbox_inches="tight")
    plt.close(fig)


# ---- 1 random drift
d = pd.read_csv(P7R + "dose_response.csv")
fig, ax = plt.subplots(figsize=(7, 3.8))
y = np.arange(len(LANGS))[::-1]
for i, l in enumerate(LANGS):
    b = d[(d.lang == l) & (d.method == "base")].aw.iloc[0]
    for m, off, mk, c in [(-8, 0.14, "o", GREY), (-24, -0.14, "s", DARK)]:
        v = (d[(d.lang == l) & (d.method == "Random") & (d.mult == m)].aw.iloc[0] - b) * 100
        ax.plot([0, v], [y[i] + off] * 2, color=c, lw=1, zorder=1)
        ax.plot(v, y[i] + off, mk, color=c, ms=6, zorder=2)
        ax.text(v + (0.5 if v >= 0 else -0.5), y[i] + off, f"{v:+.1f}", va="center",
                ha="left" if v >= 0 else "right", fontsize=8.5)
        if l == "hi":
            print("Chart 1 hi", m, round(v, 2))
for x in (8, -8):
    ax.axvline(x, ls="--", color="#b04040", lw=1)
ax.axvline(0, color="black", lw=0.8)
ax.text(8.3, 5.62, "paper: within 8 points", fontsize=8.5, color="#b04040", ha="left")
ax.text(-8.3, 5.62, "paper: within 8 points", fontsize=8.5, color="#b04040", ha="right")
ax.set_ylim(-0.6, 5.9)
ax.set_xlim(-19, 16)
ax.set_yticks(y)
ax.set_yticklabels([LN[l] for l in LANGS])
ax.set_xlabel("Change in false-claim agreement vs. baseline (percentage points)")
ax.legend(handles=[Line2D([], [], marker="o", color=GREY, ls="", label="random vector, α = 8"),
                   Line2D([], [], marker="s", color=DARK, ls="", label="random vector, α = 24")],
          loc="lower left", frameon=False)
save(fig, "r1_random_drift.png")

# ---- 2 persona minus CAA
models = ["1.5B", "3B", "7B", "14B"]
rows = []
for m in models:
    me = pd.read_csv((P7R if m == "7B" else P[m]) + "matched_effect.csv")
    me = me[me.target_aw_reduction == 0.5]
    for l in LANGS:
        if l not in set(me.lang):
            continue
        c = me[(me.lang == l) & (me.method == "CAA")].iloc[0]
        p = me[(me.lang == l) & (me.method == "Persona")].iloc[0]
        both = bool(c.reachable) and bool(p.reachable)
        rows.append(dict(model=m, lang=l, c_ok=bool(c.reachable), p_ok=bool(p.reachable),
                         diff=p.retention - c.retention if both else np.nan))
r2 = pd.DataFrame(rows)
print("Chart 2 values (persona - CAA retention):")
for _, r in r2.dropna(subset=["diff"]).iterrows():
    print(f"  {r.model} {r.lang}: {r['diff']:+.4f}")
print("  bars:", r2["diff"].notna().sum(), "positive:", (r2["diff"] > 0).sum(),
      "min/max:", round(r2["diff"].min(), 4), round(r2["diff"].max(), 4))
print("  caa-only (x) cells:", [(r.model, r.lang) for _, r in r2.iterrows() if r.c_ok and not r.p_ok])
fig, ax = plt.subplots(figsize=(7, 4.0))
x = 0
ticks = []
groups = []
for m in models:
    s = x
    for l in LANGS:
        sel = r2[(r2.model == m) & (r2.lang == l)]
        if sel.empty:
            continue
        r = sel.iloc[0]
        if not np.isnan(r["diff"]):
            ax.bar(x, r["diff"], width=0.8, color=ORANGE)
            ax.text(x, r["diff"] + (0.0015 if r["diff"] >= 0 else -0.0015), f"{r['diff']:+.3f}",
                    ha="center", va="bottom" if r["diff"] >= 0 else "top", fontsize=7, rotation=90)
        elif r.c_ok and not r.p_ok:
            ax.plot(x, 0, "x", color=ORANGE, ms=8, mew=2)
        ticks.append((x, l.upper()))
        x += 1
    groups.append((m, (s + x - 1) / 2))
    x += 1
ax.axhline(0, color="black", lw=0.8)
ax.set_xticks([t[0] for t in ticks])
ax.set_xticklabels([t[1] for t in ticks], fontsize=8)
ax.set_ylim(-0.058, 0.058)
for m, c in groups:
    ax.text(c, -0.0, f"Qwen2.5-{m}", ha="center", va="top", fontsize=9.5, transform=ax.get_xaxis_transform(), clip_on=False) if False else ax.annotate(f"Qwen2.5-{m}", (c, 0), xycoords=ax.get_xaxis_transform(), xytext=(0, -16), textcoords="offset points", ha="center", va="top", fontsize=9.5, annotation_clip=False)
ax.text(0, -0.1, "EN English, ES Spanish, ZH Chinese, HI Hindi, BN Bengali, AR Arabic",
        transform=ax.transAxes, fontsize=8, color=DARK, va="top") if False else None
ax.set_ylabel("persona − CAA retention")
ax.set_xlabel("EN English, ES Spanish, ZH Chinese, HI Hindi, BN Bengali, AR Arabic", fontsize=8, labelpad=26)
ax.legend(handles=[Line2D([], [], marker="s", color=ORANGE, ls="", label="persona minus CAA (both reach 50% reduction)"),
                   Line2D([], [], marker="x", color=ORANGE, ls="", mew=2,
                          label="persona never halves false-claim agreement")],
          loc="upper right", frameon=False, fontsize=8.5)
save(fig, "r2_persona_minus_caa.png")

# ---- 3 opinion vector control (7B)
c7 = pd.read_csv(P["7B"] + "controls.csv")
c7 = c7[(c7.target == "factual") & (c7.control == "opinion_vec")].set_index("lang")
ca = pd.read_csv(P["7B"] + "caa_collapse.csv").set_index("lang")
fig, axs = plt.subplots(1, 2, figsize=(7, 3.9), sharey=True)
y = np.arange(6)[::-1]
for ax, (ttl, bk, ck, ok) in zip(axs, [("Agrees with a false claim", "base_aw", "anti_aw", "aw"),
                                       ("Agrees with a true claim", "base_at", "anti_at", "at")]):
    for i, l in enumerate(LANGS):
        b = ca.loc[l, bk] * 100
        c = ca.loc[l, ck] * 100
        o = c7.loc[l, ok] * 100
        ax.plot([b, c], [y[i]] * 2, color=BLUE, lw=0.8, alpha=.6, zorder=1)
        ax.plot([b, o], [y[i]] * 2, color=PURPLE, lw=0.8, alpha=.6, zorder=1)
        ax.plot(b, y[i], "o", color=DARK, ms=6, zorder=2)
        ax.plot(c, y[i], "o", color=BLUE, ms=6, zorder=2)
        ax.plot(o, y[i], "D", color=PURPLE, ms=5.5, zorder=3)
    ax.set_xlim(-3, 105)
    ax.set_xlabel(ttl + " (%)")
    ax.grid(axis="x", color="#e5e5e5", lw=.6)
axs[0].set_yticks(y)
axs[0].set_yticklabels([LN[l] for l in LANGS])
fig.legend(handles=[Line2D([], [], marker="o", color=DARK, ls="", label="baseline"),
                    Line2D([], [], marker="o", color=BLUE, ls="", label="English CAA, α = 8"),
                    Line2D([], [], marker="D", color=PURPLE, ls="", label="opinion vector, α = 8")],
           loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.06))
fig.tight_layout()
print("Chart 3 opinion-vec aw:", {l: round(c7.loc[l, "aw"], 3) for l in LANGS},
      "at:", {l: round(c7.loc[l, "at"], 3) for l in LANGS})
save(fig, "r3_opinion_vec_control.png")

# ---- 4 honesty gap heatmap
mods = ["0.5B", "1.5B", "3B", "7B", "14B"]
H = []
for m in mods:
    t = pd.read_csv(P[m] + "caa_collapse.csv").set_index("lang")
    H.append([t.loc[l, "base_at"] - t.loc[l, "base_aw"] for l in LANGS])
H = np.array(H)
print("Chart 4 gaps:\n", pd.DataFrame(H, index=mods, columns=LANGS).round(3))
fig, ax = plt.subplots(figsize=(7, 3.1))
im = ax.imshow(H, cmap="Blues", vmin=0, vmax=H.max(), aspect="auto")
for i in range(5):
    for j in range(6):
        ax.text(j, i, f"{H[i, j]:.2f}", ha="center", va="center", fontsize=9.5,
                color="white" if H[i, j] > 0.6 * H.max() else "black")
ax.set_xticks(range(6))
ax.set_xticklabels([LN[l] for l in LANGS])
ax.set_yticks(range(5))
ax.set_yticklabels(["Qwen2.5-0.5B", "Qwen2.5-1.5B", "Qwen2.5-3B", "Qwen2.5-7B", "Qwen2.5-14B (nf4)"])
for s in ax.spines.values():
    s.set_visible(False)
cb = fig.colorbar(im, ax=ax, pad=0.02)
cb.set_label("baseline gap: true minus false agreement")
save(fig, "r4_honesty_gap.png")

# ---- 5 sample sizes
nf, no = [], []
for m in mods:
    dg = json.load(open(P[m] + "diagnostics.json"))
    nf.append(dg["n_eval_factual"])
    no.append(dg["n_eval_opinion"])
pa = pd.read_csv(P["7B"] + "probe_accuracy.csv").set_index("lang")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.6), gridspec_kw={"width_ratios": [1.1, 1]})
xx = np.arange(5)
w = .38
b1 = a1.bar(xx - w / 2, nf, w, color=BLUE, label="factual eval items")
b2 = a1.bar(xx + w / 2, no, w, color=GREY, label="opinion eval items")
for b in list(b1) + list(b2):
    a1.text(b.get_x() + b.get_width() / 2, b.get_height() + 2, str(int(b.get_height())), ha="center", fontsize=8)
a1.set_xticks(xx)
a1.set_xticklabels(mods)
a1.set_xlabel("Qwen2.5 model")
a1.set_ylabel("Evaluation items per language")
a1.set_ylim(0, 200)
a1.legend(frameon=False, fontsize=8.5, loc="upper right")
k = [int(pa.loc[l, "known"]) for l in LANGS]
tot = int(pa.loc["en", "total"])
bb = a2.bar(range(6), k, color=BLUE, width=.7)
for b, v in zip(bb, k):
    a2.text(b.get_x() + b.get_width() / 2, v + 8, str(v), ha="center", fontsize=8.5)
a2.axhline(tot, color=DARK, ls="--", lw=1)
a2.text(5.4, tot + 10, f"{tot} items", ha="right", fontsize=8.5)
a2.set_xticks(range(6))
a2.set_xticklabels([LN[l] for l in LANGS], rotation=35, ha="right")
a2.set_ylim(0, 700)
a2.set_ylabel("Known items (Qwen2.5-7B probe)")
fig.tight_layout()
print("Chart 5:", nf, no, k, tot)
save(fig, "r5_sample_sizes.png")

# ---- 6 slope vs drop
tr = pd.read_csv(P["7B"] + "transfer_factual.csv").set_index("lang")
bs = pd.read_csv(P["7B"] + "baseline.csv").set_index("lang")
fig, ax = plt.subplots(figsize=(7, 4))
for l in LANGS:
    sx = tr.loc[l, "slope_en"]
    dy = ca.loc[l, "true_drop"] * 100
    ax.plot(sx, dy, "o", color=BLUE, ms=8)
    ax.annotate(f"{LN[l]}, margin {bs.loc[l, 'margin_true']:.1f}", (sx, dy), xytext=((-8, -4) if sx > 1.5 else (8, -4)),
                textcoords="offset points", fontsize=9, ha=("right" if sx > 1.5 else "left"))
    print("Chart 6", l, round(sx, 2), round(dy, 1), round(bs.loc[l, "margin_true"], 1))
ax.set_xlabel("English-vector slope (logit margin per unit α)")
ax.set_ylabel("drop in true-claim agreement at α = 8 (pp)")
ax.grid(color="#eee", lw=.6)
ax.margins(x=0.1, y=0.12)
save(fig, "r6_slope_vs_drop.png")
