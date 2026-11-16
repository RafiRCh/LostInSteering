# Steering v2 (original CAA vector): results notes

**Run:** 2026-11-15 on Kaggle (2× T4), notebook `notebooks/03_steering_v2.ipynb`, Kaggle kernel `arifurrhmn/notebook2557ee43e2`.
Full run (`QUICK = False`), `Qwen/Qwen2.5-7B-Instruct`, `VECTOR_TYPE = "caa"`, runtime 2 h 32 min.
Output folder: `steering_v2/` (the `.pt` vector file is downloaded but git-ignored).

**Setup:** all 615 Global-MMLU-Lite questions probed in 6 languages (en, es, zh, hi, bn, ar); 128 questions known in all 6 and
under 600 tokens form the item pool. A "teacher" claims a wrong (or right) answer and asks "am I right?". Each item is shown with
"agree" as A and as B, 5-fold cross-fitting, bootstrap 95% CIs over items, English / native / random vectors,
layers 12 to 23, multiplier ±8 (= 8% of the layer's activation norm at the strength chosen by calibration).

**Verdict printed by the notebook: NOT YET.** Checks 1 to 4 pass, checks 5 and 6 fail.

| Check | Result |
|---|---|
| 1. Item pool >= 100 | PASS (128) |
| 2. Model sycophantic on known items in >= 4 languages | PASS |
| 3. Clear English effect, beats random | PASS (0.33, CI 0.26 to 0.40, layer 17) |
| 4. Native vector beats random in >= 4 languages | PASS (6 of 6) |
| 5. Honesty improves in English under anti-steering | **FAIL** (-0.12, CI -0.19 to -0.04) |
| 6. English agree_true drops < 0.15 | **FAIL** (drops 0.27) |

## What worked

- **Baseline sycophancy gradient (no steering).** Honesty = agree_true minus agree_wrong, higher is better:
  English 0.62, Spanish 0.53, Chinese 0.57, Arabic 0.47, Hindi 0.34, Bengali 0.26. Agreement with a wrong claim:
  Chinese 0.17, English 0.23, Spanish 0.34, Arabic 0.37, Bengali 0.43, Hindi 0.54. Matches notebook 02 on a larger pool.
- **A clear steering effect.** Best layer is 17 (English steerability 0.29 in the sweep; sharp peak, layers 20 to 23 are flat).
  Random-vector control stays at zero (small negative in Hindi and Bengali).
- **Transfer is nearly complete.** English vector vs native vector, steerability ratio (CI): Spanish 1.02 (1.00 to 1.03),
  Chinese 1.49 (1.36 to 1.65), Hindi 0.92 (0.89 to 0.95), Bengali 1.01 (1.00 to 1.02), Arabic 0.81 (0.76 to 0.85).
  Cosine of native vector to English at layer 17: es 0.92, zh 0.90, ar 0.87, hi 0.85, bn 0.81.
  Hindi and Bengali do **not** transfer worse, contrary to the smoke test v1 hint.

## What did not work

1. **The vector is a general "agree" knob, not an honesty knob** (same problem as smoke test v1). Anti-steering lowers agreement with
   TRUE claims as much as with wrong ones, so honesty gets worse in every language
   (change at -8: en -0.12, es -0.07, zh -0.22, hi -0.11, bn -0.08 (CI crosses 0), ar -0.13).
   English at -8: agree_wrong 0.23 -> 0.08, but agree_true 0.85 -> 0.58.
2. **Calibration had no good choice.** Only the weakest step (1% of norm per multiplier unit) kept honesty within 0.10 of baseline,
   so it was chosen even though it fell short of the 0.30 steerability target at the calibration layer.

## Caveats

- Layer and step size were picked on the first 32 pool items (English only), which are also in the final test set. Small selection effect.
- 128 items; CIs for Bengali and Hindi are wider than for English.
- Forced-choice A/B scoring only. Free-text answers were not scored (only a 3-item script check in `generations.csv`).

## Files (in `steering_v2/`)

| File | Contents |
|---|---|
| `checks.json`, `config.json` | verdict and run settings |
| `transfer_summary.csv/.png` | **main result**: steerability, transfer ratio, honesty gain per language with CIs |
| `dose_response.csv/.png` | agree_wrong, agree_true, honesty vs multiplier (English, native, random vectors) |
| `layer_sweep.csv`, `layer_sweep_heatmaps.png` | steerability per layer and language |
| `baseline.csv`, `calibration.csv` | unsteered sycophancy; strength calibration |
| `cosine_to_english__caa.csv`, `cosine_to_english__caa_debiased.csv`, `cosine_to_english.png` | vector similarity by layer |
| `item_pool.json`, `probe_accuracy.csv`, `probe_known.csv` | which questions are in the pool, probe accuracy |
| `per_item_results.csv.gz` | every per-item probability (for re-analysis) |
| `generations.csv` | free-text answers with and without steering |
| `vectors.pt` | all vectors (git-ignored; re-download with `kaggle kernels output arifurrhmn/notebook2557ee43e2`) |
| `../notebook2557ee43e2.log` | full Kaggle log |

Next run: [`../03b_steering_v2_debiased/NOTES.md`](../03b_steering_v2_debiased/NOTES.md).
