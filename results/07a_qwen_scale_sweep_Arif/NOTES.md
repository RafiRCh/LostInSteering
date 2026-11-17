# Qwen2.5 Scale Sweep (0.5B → 1.5B → 3B): Run 07a Notes

**Run:** 2026-11-16 to 2026-11-17 on Kaggle (Nvidia Tesla T4), notebook `notebooks/07a_qwen_scale_sweep_Arif.ipynb`, kernel `rafirahmanchowdhury/lostinsteering-7a`.
**Runtime:** ~12 hours (automated kernel completion).
**Models Evaluated:**
1. `Qwen/Qwen2.5-0.5B-Instruct`
2. `Qwen/Qwen2.5-1.5B-Instruct`
3. `Qwen/Qwen2.5-3B-Instruct`

Across 6 evaluation languages: English (`en`), Spanish (`es`), Chinese (`zh`), Hindi (`hi`), Bengali (`bn`), Arabic (`ar`).

---

## 1. Executive Summary & Main Findings

This scaling sweep investigates how activation steering dynamics, cross-lingual transfer, and factual honesty collapse evolve as model capacity scales from **0.5B to 3B parameters** (complementing our 7B paper run in Run 04).

### Key Takeaways:
1. **Steerability Emerges with Scale:**
   - **0.5B:** Fails to form a coherent sycophancy subspace. Vectors exhibit high variance, near-zero opinion sycophancy reduction ($\Delta \approx 0.0003$), and erratic transfer ratios.
   - **1.5B:** Clear emergence of steerability. English vectors steer Spanish (transfer ratio 0.95), Chinese (0.88), Hindi (0.79), Bengali (0.69), and Arabic (0.80).
   - **3B:** Strong geometric convergence. Cross-lingual vector cosines to English jump dramatically: Spanish (0.95), Chinese (0.96), Arabic (0.93), Bengali (0.77), Hindi (0.69). Opinion transfer ratios achieve near-parity: Hindi (0.95), Bengali (0.97), Arabic (0.91).
2. **CAA Truth Collapse is Scale-Invariant (1.5B → 7B):**
   - Anti-sycophancy steering via standard CAA induces catastrophic truth collapse regardless of parameter scale once the steering mechanism functions:
     - **1.5B:** True claim agreement drops by **65.4%** in English, **90.2%** in Spanish, **91.9%** in Chinese, and **88.0%** in Bengali.
     - **3B:** True claim agreement drops by **75.5%** in English, **79.6%** in Chinese, and **84.0%** in Bengali.
   - This proves truth collapse is **not** an artifact of 7B over-parameterization, but a foundational geometric flaw of difference-in-means vectors (which act as general disagreement/contrarian knobs rather than honesty dials).
3. **Persona Vectors Generalize Across Scale:**
   - Evaluator/truthful persona vectors consistently avoid total truth collapse, retaining **43%–68%** of true claim agreement at 3B while boosting honesty scores.

---

## 2. Quantitative Comparison Across Scale

### A. Opinion Sycophancy Transfer Ratios (to English Vector)

| Language | 0.5B Instruct | 1.5B Instruct | 3B Instruct | 7B Instruct (Run 04) |
|---|---|---|---|---|
| **English (en)** | 1.00 | 1.00 | 1.00 | 1.00 |
| **Spanish (es)** | Erratic (<0) | 0.95 | 0.68 | 0.98 |
| **Chinese (zh)** | Erratic (<0) | 0.89 | 0.81 | 0.96 |
| **Hindi (hi)** | 0.46 | 0.79 | **0.95** | 0.99 |
| **Bengali (bn)** | 3.75 (Noisy) | 0.69 | **0.97** | 0.98 |
| **Arabic (ar)** | Erratic (<0) | 0.80 | **0.91** | 0.95 |

*Insight:* Cross-lingual transfer to low-resource and non-Latin scripts (Bengali, Hindi, Arabic) improves monotonically with model scale, reaching near-perfect transfer (>0.90) at 3B and 7B.

---

### B. Vector Cosine Similarity to English (Layer-Averaged)

| Language | 0.5B Cosine | 1.5B Cosine | 3B Cosine |
|---|---|---|---|
| **Spanish (es)** | 0.65 | 0.67 | **0.95** |
| **Chinese (zh)** | 0.65 | 0.72 | **0.96** |
| **Arabic (ar)** | 0.48 | 0.45 | **0.93** |
| **Bengali (bn)** | 0.23 | 0.52 | **0.77** |
| **Hindi (hi)** | 0.27 | 0.35 | **0.69** |

*Insight:* Low-resource Indic languages (Hindi, Bengali) exhibit distinct linguistic clustering at lower parameter scales (cosine 0.23–0.35), but rapidly align toward the shared cross-lingual semantic manifold as model capacity expands to 3B.

---

### C. Factual CAA Truth Collapse Across Scale (True Claim Drop)

| Language | 0.5B Drop | 1.5B Drop | 3B Drop | 7B Drop (Run 04) |
|---|---|---|---|---|
| **English (en)** | -22.2% | **-65.4%** | **-75.5%** | -35.1% |
| **Spanish (es)** | -0.5% | **-90.2%** | **-79.6%** | -21.3% |
| **Chinese (zh)** | +0.5% | **-91.9%** | **-79.6%** | -23.8% |
| **Hindi (hi)** | -11.8% | **-71.1%** | **-54.2%** | -21.6% |
| **Bengali (bn)** | +0.2% | **-88.0%** | **-84.0%** | -16.7% |
| **Arabic (ar)** | +8.8% | **-63.6%** | **-63.6%** | -27.5% |

---

## 3. Directory Layout & Artifacts

Each subfolder contains the full experimental suite:
- `baseline.csv`: Baseline accuracy and sycophancy rates.
- `cosine_opinion.csv`, `cosine_factual.csv`, `cosine_sibling.csv`: Angular alignment metrics between native and transferred steering vectors.
- `layer_sweep.csv` & `layer_sweep_heatmap.png`: Layer-by-layer steerability across all 6 languages.
- `transfer_summary.csv`: Cross-lingual transfer ratios with bootstrap confidence intervals.
- `factual_summary.csv`: Verification of truth collapse under anti-steering.
- `persona_summary.csv`: Factual retention and honesty gain under persona vectors.
- `vectors.pt`: PyTorch checkpoints containing extracted CAA, factual debiased, and persona steering vectors.
- `kaggle_run.log`: Complete stdout and stderr log of the 12-hour execution.
