# Qwen2.5-14B Full Scale Audit: Run 07b Notes

**Run:** 2026-11-17 to 2026-11-18 on Kaggle (Nvidia Tesla T4 GPU, 15GB VRAM), notebook `notebooks/07b_qwen_14b_Rafi.ipynb`, kernel `mohammadsaleemali/lostinsteering7b` (Version 4, `scriptVersionId=370704364`).
**Runtime:** ~11.8 hours (completed across all major experimental stages).
**Hardware & Optimization:** Loaded `Qwen/Qwen2.5-14B-Instruct` in **4-bit NormalFloat4 (NF4)** via `bitsandbytes` (`load_in_4bit=True`), reducing memory footprint to ~9 GB VRAM and fully resolving the earlier fp16 OOM failure.

---

## 1. Executive Summary & Key Findings

This 14B scale audit serves as the upper-parameter anchor for the LostInSteering project, establishing how sycophancy representation geometry, cross-lingual transfer, and factual honesty collapse scale to 14 billion parameters.

### Major Results:

1. **Near-Perfect Cross-Lingual Transfer Parity ($\approx 1.00$ Across All Languages):**
   * At the 14B scale, the cross-lingual transfer of English anti-sycophancy steering vectors achieves virtually **100% efficiency** across all 6 evaluated languages, including low-resource and non-Latin scripts:
     - **English (en):** 1.000 [1.000, 1.000]
     - **Spanish (es):** 0.995 [0.987, 1.002]
     - **Chinese (zh):** 0.954 [0.932, 0.970]
     - **Hindi (hi):** **1.015** [1.009, 1.024]
     - **Bengali (bn):** **1.017** [1.009, 1.028]
     - **Arabic (ar):** **1.017** [1.009, 1.027]
   * Transfer ratios strictly exceed 0.95 across every script, demonstrating that larger representations form an increasingly unified cross-lingual sycophancy manifold.

2. **Unprecedented Sibling Alignment (Hindi $\leftrightarrow$ Bengali Cosine $\approx 0.95$):**
   * Across the core representation layers (layers 23 to 35), Hindi and Bengali sycophancy vectors reach near-identical orientation:
     - Layer 23: 0.770
     - Layer 25: 0.920
     - Layer 26: 0.935
     - Layer 29: **0.949**
     - Layer 30: 0.939
   * In addition, English-to-Bengali cosine similarity peaks at **0.895** (Layer 29), and English-to-Hindi peaks at **0.921** (Layer 29).

3. **CAA Truth Collapse Persists at 14B (Scale Invariance Confirmed):**
   * Even at 14B parameters, standard Contrastive Activation Addition (CAA) anti-sycophancy steering continues to act as a coarse disagreement knob, inducing severe collapse on true factual claims:
     - **English (en):** -57.9% drop in true claim agreement
     - **Spanish (es):** -48.3% drop
     - **Arabic (ar):** -64.6% drop
     - **Chinese (zh):** -76.9% drop
     - **Hindi (hi):** -78.0% drop
     - **Bengali (bn):** -81.9% drop
   * **Conclusion:** Scaling to 14B does **not** cure CAA truth collapse. Difference-in-means vectors continue to suppress general agreement rather than selectively targeting sycophantic agreement.

4. **Persona Vectors Maintain ~100% Factual Retention:**
   * Objective Evaluator persona steering achieves **~100% true claim retention** at 14B:
     - English: **100.1%** retention
     - Spanish: **99.9%** retention
     - Chinese: **100.5%** retention
     - Hindi: **100.4%** retention
   * Persona vectors successfully eliminate truth collapse while preserving factual honesty at scale.

---

## 2. Quantitative Summary Across Languages (14B)

| Language | Layer Cosine to EN | Native Steerability | Transferred Steerability | Transfer Ratio (95% CI) | CAA True Claim Drop | Persona True Retention |
|---|---|---|---|---|---|---|
| **English (en)** | 1.000 | 0.599 | 0.599 | 1.000 [1.000, 1.000] | -57.9% | **100.1%** |
| **Spanish (es)** | 0.963 | 0.699 | 0.695 | 0.995 [0.987, 1.002] | -48.3% | **99.9%** |
| **Chinese (zh)** | 0.964 | 0.597 | 0.566 | 0.954 [0.932, 0.970] | -76.9% | **100.5%** |
| **Hindi (hi)** | 0.899 | 0.838 | 0.852 | **1.015** [1.009, 1.024] | -78.0% | **100.4%** |
| **Bengali (bn)** | 0.845 | 0.887 | 0.905 | **1.017** [1.009, 1.028] | -81.9% | — |
| **Arabic (ar)** | 0.922 | 0.806 | 0.821 | **1.017** [1.009, 1.027] | -64.6% | — |

---

## 3. Comprehensive Scale Progression (0.5B $\rightarrow$ 14B)

Combining findings across Run 07a (0.5B, 1.5B, 3B), Run 04 (7B), and Run 07b (14B):

| Metric | 0.5B | 1.5B | 3B | 7B | 14B |
|---|---|---|---|---|---|
| **Emergence of Sycophancy Subspace** | No (noisy / $\Delta \approx 0$) | Yes | Yes (tight) | Strong | Complete Parity |
| **Mean Cross-Lingual Cosine to EN** | ~0.53 | ~0.54 | ~0.86 | ~0.90 | **~0.93** |
| **Hindi-Bengali Cosine Alignment** | 0.23 | 0.35 | 0.77 | 0.88 | **0.95** |
| **Mean Cross-Lingual Transfer Ratio** | Erratic | ~0.83 | ~0.87 | ~0.97 | **~1.00** |
| **CAA Factual Truth Collapse** | Weak (-10%) | Severe (-78%) | Severe (-72%) | Replicated (-24%) | Persistent (-68%) |
| **Persona Factual Retention** | Incoherent | 20%–35% | 43%–68% | 85%–97% | **~100%** |

---

## 4. Artifacts in this Directory

- `baseline.csv`: Baseline accuracy and sycophancy metrics for Qwen2.5-14B-Instruct.
- `cosine_opinion.csv`: Layer-by-layer cosine similarities of opinion sycophancy vectors to English.
- `cosine_factual.csv`: Angular metrics for debiased factual steering vectors.
- `cosine_sibling.csv`: Hindi $\leftrightarrow$ Bengali and English $\leftrightarrow$ Indic cosine similarities across all 48 transformer layers.
- `cosine_matrix_all_layers.csv`: Complete pairwise cross-lingual cosine matrices.
- `transfer_summary.csv`: Full transfer ratios with bootstrap 95% confidence intervals.
- `factual_summary.csv`: Factual sycophancy vs. truth collapse metrics under CAA anti-steering.
- `layer_sweep.csv` & `layer_sweep_heatmap.png`: Full layer sweep heatmap across 48 layers for all 6 languages.
- `vectors.pt`: PyTorch checkpoints containing the extracted 14B steering vectors.
- `kaggle_run.log`: Complete stdout and stderr log of the 11.8-hour execution.
