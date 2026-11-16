# Steering v2c (debiased vector, sign flipped, layer 17): results notes

**Run:** 2026-11-16 on Kaggle (2× T4), notebook `notebooks/03c_steering_v2_debiased_flip.ipynb`, Kaggle kernel `arifurrhmn/lostinsteering-03c-debiased-flip`.
Full run (`QUICK = False`), `Qwen/Qwen2.5-7B-Instruct`, `VECTOR_TYPE = "caa_debiased"`, `BEST_LAYER = 17`, runtime 2 h 57 min (177 min).
Output folder: `steering_v2_debiased_flip/` (`.pt` vector file git-ignored).

**Why this run:** run 03b found that while layer 13 had steerability ~0, layers 16 to 17 had large negative steerability (-0.63 at layer 17). This run tested whether flipping the vector sign and locking evaluation to layer 17 produces a true sycophancy/honesty steering vector.

**Verdict printed by the notebook: NOT YET.** Checks 1 to 4 pass cleanly; checks 5 and 6 fail decisively.

| Check | Result |
|---|---|
| 1. Item pool >= 100 | PASS (128) |
| 2. Model sycophantic on known items in >= 4 languages | PASS |
| 3. Clear English effect, beats random | PASS (0.61, CI 0.54 to 0.69 at layer 17) |
| 4. Native vector beats random in >= 4 languages | PASS (6 of 6) |
| 5. Honesty improves in English under anti-steering | **FAIL** (-0.52, CI -0.60 to -0.43) |
| 6. English agree_true drops < 0.15 | **FAIL** (drops 0.75, from 0.85 to 0.10) |

## Comparison across v2 runs

| Metric / Check | Original CAA (03, layer 17) | Debiased (03b, layer 13) | Debiased + Flipped (03c, layer 17) |
|---|---|---|---|
| **English steerability** | 0.33 [0.26, 0.40] | 0.03 [-0.04, 0.07] | **0.61** [0.54, 0.69] |
| **Native beats random** | 6 of 6 | 3 of 6 | **6 of 6** (all CI > 0.44) |
| **Transfer ratio (all langs)** | 0.81 to 1.49 | mostly unmeasurable | **0.96 to 1.07** (near perfect 1.0) |
| **Cosine to English vector** | 0.81 to 0.92 | 0.11 to 0.54 | **0.89 to 0.96** |
| **English honesty change (anti-steer)** | -0.12 [-0.19, -0.04] | +0.007 [-0.01, +0.03] | **-0.52** [-0.60, -0.43] |
| **English agree_true drop** | 0.27 (0.85 -> 0.58) | 0.007 (0.85 -> 0.84) | **0.75** (0.85 -> 0.10) |

## Key Findings

1. **Massive steerability and near-perfect multilingual alignment:**
   - Sign flipping at layer 17 yields very high steerability (0.61 in EN, 0.71 in ES, 0.55 in ZH, 0.79 in HI, 0.78 in BN, 0.69 in AR).
   - Transfer ratios from the English vector are remarkably consistent around 1.0:
     - Spanish: 0.96 [0.94, 0.97] (cosine 0.96)
     - Chinese: 1.05 [1.03, 1.08] (cosine 0.96)
     - Hindi: 1.07 [1.05, 1.09] (cosine 0.90)
     - Bengali: 0.96 [0.94, 0.97] (cosine 0.89)
     - Arabic: 1.00 [0.99, 1.01] (cosine 0.95)
   - The geometric representation of this activation direction is shared across scripts and languages.

2. **The "Honesty" failure (Checks 5 & 6):**
   - Anti-steering at -8 crushes agreement with *everything*:
     - `agree_wrong` drops from 0.23 -> 0.002.
     - `agree_true` collapses from 0.85 -> 0.10.
   - Consequently, honesty (`agree_true - agree_wrong`) falls from +0.62 to +0.10 (honesty change = -0.52).
   - In qualitative generations, anti-steering induces generic contrarianism / refusal rather than calibrated honesty: the model disagrees with whatever claim is put in the prompt, whether factually true or false.

## Project Implications

Across runs 03, 03b, and 03c, the central empirical pattern is now decisive:
- **Acquiescence / Agreement / Contrarian directions transfer cross-lingually with high fidelity (~100% transfer ratio).**
- **However, CAA difference-in-means vectors (whether raw or debiased by subtracting true-claim differences) do not isolate sycophancy from general acquiescence.** They operate as an "agree <-> disagree" dial, not a "truthfulness / honesty" dial.
- As anticipated in `docs/ROADMAP.md`:
  > *"if honesty still does not improve, report 'agreement transfers, sycophancy-specific steering does not separate' and consider pushback / over-praise sycophancy."*

## Files (in `steering_v2_debiased_flip/`)

| File | Contents |
|---|---|
| `checks.json`, `config.json` | verdict and run settings |
| `transfer_summary.csv/.png` | steerability, transfer ratios, and honesty changes per language |
| `dose_response.csv/.png` | agree_wrong, agree_true, and honesty vs multiplier |
| `layer_sweep.csv`, `layer_sweep_heatmaps.png` | steerability per layer and language |
| `baseline.csv`, `calibration.csv` | unsteered sycophancy; strength calibration |
| `cosine_to_english__*.csv`, `cosine_to_english.png` | vector cosine similarities across layers |
| `item_pool.json`, `probe_accuracy.csv`, `probe_known.csv` | 128 items known in all 6 languages |
| `per_item_results.csv.gz` | per-item probabilities across folds and conditions |
| `generations.csv` | free-text qualitative completions |
| `vectors.pt` | steering vectors (git-ignored) |
| `../lostinsteering-03c-debiased-flip.log` | full Kaggle execution log |
