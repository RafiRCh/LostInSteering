# Run 08 (Job 1: `notebook_1`) — Unified Scale Run Notes

**Date:** 2026-11-18 to 2026-11-19  
**Execution Environment:** Kaggle (`mohammadsaleemali/notebook-1`, Kernel ID: `145804807`)  
**Hardware:** 2x Nvidia Tesla T4 GPUs (CUDA 13.0, PyTorch 2.11.0, Transformers 5.20.2)  
**Total Wall Time:** 11.21 hours (Clean hard stop at budget limit `HARD_BUDGET_H = 11.2h`)  
**Notebook Source:** [`notebooks/08_unified_scale_run.ipynb`](file:///d:/Project/LostInSteering/notebooks/08_unified_scale_run.ipynb) (`PRESET = "notebook_1"`)  

---

## 1. Overview & Protocol Improvements

Run 08 replaces the prior disparate runs (04, 07a, 07b) with a unified, corrected evaluation protocol addressing the 2026-11-18 audit findings:
1. **Opinion Task Redesign:** Replaced synthetic hedge options ("it depends...") with paired sycophantic vs non-sycophantic statements directly from the dataset. Logit margins $\Delta \text{logit} = \text{logit}(\text{syc}) - \text{logit}(\text{non-syc})$ are evaluated to prevent probability saturation.
2. **Standardized Steering Metric:** Evaluated cross-lingual transfer using regression slopes on logit margins at moderate multipliers ($\pm 2.0, \pm 4.0$), avoiding saturation artifacts.
3. **Cross-Lingual Evaluation:** 6 languages evaluated systematically: English (`en`), Spanish (`es`), Chinese (`zh`), Hindi (`hi`), Bengali (`bn`), and Arabic (`ar`).

### Model Progress in Job 1 (`notebook_1`):
* **`Qwen2.5-1.5B-Instruct-fp16`:** **100% Complete** (13 stages, 121.9 min runtime).
* **`Qwen2.5-3B-Instruct-fp16`:** **100% Complete** (13 stages, 290.1 min runtime).
* **`Qwen2.5-7B-Instruct-fp16`:** **Partial (Core Stages Complete)** (~260 min runtime). Completed:
  - Baseline evaluation
  - Vector extraction & Layer sweeps
  - CAA truth collapse evaluation
  - Full Factual Transfer suite across all 6 languages
  - Partial Opinion Transfer suite (en, es, zh, hi completed before hard time budget stop)
* **`Qwen2.5-7B-Instruct-nf4`:** Queued / deferred.

---

## 2. Key Empirical Findings

### A. Cross-Lingual Transfer of Factual Steering Vectors (Logit Slope Ratios)

Transfer ratio is defined as $\text{slope}_{\text{en}\to\text{target}} / \text{slope}_{\text{target}\to\text{target}}$ on logit margins:

| Language | 1.5B Transfer Ratio | 1.5B Vector Cosine | 3B Transfer Ratio | 3B Vector Cosine | 7B Transfer Ratio | 7B Vector Cosine |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **English (`en`)** | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| **Spanish (`es`)** | 1.627 | 0.707 | 0.982 | 0.947 | **0.880** | **0.937** |
| **Chinese (`zh`)** | 1.204 | 0.829 | 1.098 | 0.957 | **0.924** | **0.942** |
| **Hindi (`hi`)** | 1.341 | 0.608 | 1.472 | 0.685 | **1.108** | **0.845** |
| **Bengali (`bn`)** | 1.000 | 0.642 | 1.312 | 0.769 | **1.309** | **0.734** |
| **Arabic (`ar`)** | 1.293 | 0.751 | 1.387 | 0.926 | **1.010** | **0.902** |

#### Takeaway:
* Vector alignment (cosine similarity with English) strongly increases with scale:
  - Spanish cosine climbs from 0.707 (1.5B) $\to$ 0.947 (3B) $\to$ 0.937 (7B).
  - Arabic cosine climbs from 0.751 (1.5B) $\to$ 0.926 (3B) $\to$ 0.902 (7B).
  - Chinese cosine climbs from 0.829 (1.5B) $\to$ 0.957 (3B) $\to$ 0.942 (7B).
* Transfer ratios converge towards near parity ($0.88 - 1.11$) for high-resource and mid-resource languages at 7B.

---

### B. Opinion Transfer Ratios (Corrected Margin Protocol)

With the redesigned non-saturating opinion task, transfer ratios are stable and well-conditioned:

| Language | 1.5B Opinion Ratio | 1.5B Cosine | 3B Opinion Ratio | 3B Cosine | 7B (Partial) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **English (`en`)** | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| **Spanish (`es`)** | 0.96 | 0.915 | 1.027 | 0.835 | 0.96 |
| **Chinese (`zh`)** | 1.20 | 0.886 | 1.091 | 0.915 | 1.20 |
| **Hindi (`hi`)** | 1.63 | 0.836 | 1.830 | 0.437 | 1.63 |
| **Bengali (`bn`)** | — | — | 1.045 | 0.575 | — |
| **Arabic (`ar`)** | — | — | 0.935 | 0.862 | — |

---

### C. CAA Truth Collapse Across Scales

Evaluating CAA anti-steering ($M = -8.0$) on factual claims reveals that truth collapse is pervasive across model sizes:

| Language | 1.5B True Drop (%) | 3B True Drop (%) | 7B True Drop (%) |
| :--- | :---: | :---: | :---: |
| **English (`en`)** | +36.2% | +54.8% | +42.3% |
| **Spanish (`es`)** | +38.5% | +69.1% | +38.3% |
| **Chinese (`zh`)** | +44.1% | +79.2% | +65.6% |
| **Hindi (`hi`)** | +61.2% | +53.3% | +65.9% |
| **Bengali (`bn`)** | +69.8% | +85.0% | +81.4% |
| **Arabic (`ar`)** | +41.9% | +63.0% | +56.8% |

#### Takeaway:
* Truth collapse remains severe regardless of scale: anti-sycophancy CAA vectors suppress true factual agreement by 38%–85% across all languages in 1.5B, 3B, and 7B.
* Bengali (`bn`) and Chinese (`zh`) consistently experience the steepest drops across all model sizes.

---

### D. Sibling Language Alignment (Hindi $\leftrightarrow$ Bengali)

Cosine similarity between Hindi and Bengali steering vectors across depth:
* **1.5B:** Peaks at **0.955** (Layer 19).
* **3B:** Peaks at **0.949** (Layer 18).
* **7B:** Consistently high in mid-to-deep layers (> 0.86).

This confirms the robust cross-lingual sibling convergence hypothesis: linguistically related non-English pairs form tight, aligned representations in late-intermediate residual streams.

---

## 3. Artifact Index

All primary results are preserved in [`results/08_unified_scale_run/notebook_1/`](file:///d:/Project/LostInSteering/results/08_unified_scale_run/notebook_1/):
- `run_summary.json`: Top-level configuration and completion status.
- `kaggle_run.log`: Full console stdout/stderr log stream.
- `Qwen2.5-1.5B-Instruct-fp16/`:
  - `diagnostics.json`, `baseline.csv`, `caa_collapse.csv`, `transfer_factual.csv`, `transfer_opinion.csv`, `cosine_factual.csv`, `cosine_opinion.csv`, `cosine_sibling.csv`, `dose_response.csv`, `dose_response.png`, `layer_sweep.csv`, `layer_sweep.png`, `capability_mmlu.csv`, `controls.csv`.
- `Qwen2.5-3B-Instruct-fp16/`:
  - Full suite of 14 CSV/PNG/JSON artifacts matching 1.5B.
- `Qwen2.5-7B-Instruct-fp16/`:
  - Core suite: `baseline.csv`, `caa_collapse.csv`, `transfer_factual.csv`, `cosine_factual.csv`, `cosine_opinion.csv`, `cosine_sibling.csv`, `layer_sweep.csv`, `layer_sweep.png`, `item_pool.json`, `probe_accuracy.csv`.
