# Qwen2.5-14B Scale Audit: Run 07b Notes

**Status: PARTIAL. Audited and corrected 2026-11-18.**

**Run:** 2026-11-17 to 2026-11-18 on Kaggle (2x Tesla T4), notebook `notebooks/07b_qwen_14b_Rafi.ipynb`, kernel `mohammadsaleemali/lostinsteering7b` (Version 4).
**Runtime:** about 11.8 hours. The kernel hit the Kaggle 12-hour limit and was killed during the PERSONA stage (log ends after `hi`). It did not complete.
**Model:** `Qwen/Qwen2.5-14B-Instruct`, loaded in 4-bit NF4 (about 10 GB across both GPUs). This fixed the earlier fp16 OOM.

---

## 1. What ran and what did not

| Stage | Status | Output |
|---|---|---|
| Knowledge probe, pool of 173 items | Done | `probe_accuracy.csv`, `item_pool.json` |
| Vector extraction | Done | cosines (`cosine_*.csv`); `vectors.pt` is **not** in the repo |
| Layer sweep (stride 3, N=24, refined near best) | Done, best layer 27 | `layer_sweep.csv`, heatmap |
| Baseline | Done | `baseline.csv` |
| Opinion | Done, **unreliable** (see 2.1) | `opinion_summary.csv` |
| Factual (CAA truth collapse) | Done | `factual_summary.csv` |
| Transfer | Done, **interpret with caution** (see 2.3) | `transfer_summary.csv` |
| Persona | **Incomplete**: en, es, zh, hi only; bn and ar missing. No `persona_summary.csv` | log only |
| Controls, MMLU capability, transfer matrices, layer sensitivity, residual decomposition, dose-response, persona-extended, generations | **Not run** | none |

Also missing: `vectors.pt`, `checks.json`, `paper_main_table.csv`. The old `all_results.json` was deleted.

---

## 2. What the data supports

### 2.0 Reliable results

1. **CAA truth collapse at 14B** (true-claim agreement after anti-steering at multiplier -8, layer 27, from `factual_summary.csv`):

   | Language | Base agree_true | After anti-steering | Drop |
   |---|---|---|---|
   | en | 99.9% | 42.0% | 57.9% |
   | es | 99.9% | 51.6% | 48.3% |
   | zh | 99.2% | 22.3% | 76.9% |
   | hi | 99.1% | 21.1% | 78.0% |
   | bn | 98.6% | 16.7% | 81.9% |
   | ar | 99.8% | 35.2% | 64.6% |

   Agreement with wrong claims also falls to 1-6%, and honesty (agree_true minus agree_wrong) falls in every language. The vector behaves as a general disagreement knob. A random-vector control was not run, so we have not shown it is specific to the learned direction.
2. **Vector geometry** (`cosine_*.csv`): Hindi-Bengali cosine of factual vectors is about 0.95 at layer 29. Cosine similarity shows directional alignment only; it does not show behavioral equivalence.
3. **Baselines** (`baseline.csv`): baseline honesty differs a lot by language (en 78%, zh 78%, es 62%, ar 51%, hi 50%, bn 40%).
4. **Knowledge probe** (`probe_accuracy.csv`): items known out of 608 were en 412, es 428, zh 315, hi 399, bn 355, ar 414. The pool of 173 items is known in all six languages, so it is shaped by the weakest language.

### 2.1 Opinion results: unreliable

Baseline opinion sycophancy is already near zero in every language (en 0.4%, es 0.0007%, zh 0.9%, hi 0.004%, bn 0.1%, ar 1.4%). The "disagree" option in the prompt is a hedge ("it depends, there are other perspectives") that the model nearly always picks. After steering the rate moves by about one percentage point, and in the wrong direction. The transfer ratios in `opinion_summary.csv` (for example -4646, +9272, -6718) are ratios of near-zero numbers and are meaningless. **No opinion conclusion can be drawn from this run.**

### 2.2 Layer sweep and sign

The best layer by absolute value was 27, with steerability -0.626 for English, so the code multiplies the vector by -1. This is a sign convention only and is applied consistently across the sweep, transfer, factual and persona stages. It is not a bug, but it should be stated whenever vectors are compared. The sweep uses only N=24 items for the coarse pass.

### 2.3 Transfer: interpret with caution

`transfer_summary.csv` reports English-vector steerability of 0.57-0.90 and transfer ratios of 0.95-1.02. These are measured on the factual task at multiplier +/-8, where probabilities swing close to their extremes. Ratios above 1 whose confidence intervals exclude 1 (hi, bn, ar: 1.015-1.017) mean the English vector steered those languages better than their own native vector. That pattern suggests saturation or weak native vectors, not stronger "unified geometry". The English row's interval [1,1] is trivial by construction. Pool size is 173 items. **We cannot claim cross-lingual parity from this run.** Dose-response at smaller multipliers (not run) is needed.

### 2.4 Persona: not supported

The log shows persona retention of 99.9-100.5% for en, es, zh, hi, but `aw_drop` is negative (-0.03 to -0.05), meaning agreement with wrong claims **increased** slightly. Baseline agree_true is already about 99%, so retention near 100% is expected from a vector that changes nothing. This is the same pattern seen at 7B (run 04, honesty gain about 0). **There is no evidence in this run that persona vectors reduce sycophancy.** The persona vector is built from only 3 prompt pairs.

---

## 3. Scale comparison: not valid yet

An earlier version of this file compared 0.5B to 14B in one table and called truth collapse "scale invariant". That is withdrawn:

- Run 04 (7B) used a different protocol (different prompts, baseline agree_true 49-74% instead of about 99%) from 07a/07b, so its numbers cannot sit on the same axis.
- True-claim drops are -17% to -35% at 7B, versus -48% to -82% at 14B, which is not invariant.
- The opinion metric is at floor at 3B, 7B and 14B.

A valid scale axis needs one notebook and one protocol run at 3B, 7B and 14B.

---

## 4. Next steps

1. Fix the opinion task (neutral binary choice, calibrated baseline) and re-test on a small model locally.
2. Compare persona and CAA at matched effect size; report agree_wrong and honesty change, not only retention. Add more than 3 persona prompt pairs.
3. Re-run 3B and 7B with this notebook.
4. Check whether the Kaggle Version 4 output still has `vectors.pt` and cached CSVs; if so, attach it as an input dataset and resume to fill the missing stages (persona bn/ar, controls, MMLU capability, matrices, dose-response).

---

## 5. Artifacts in this directory

- `Qwen2.5-14B-Instruct/baseline.csv`, `probe_accuracy.csv`, `item_pool.json`
- `cosine_opinion.csv`, `cosine_factual.csv`, `cosine_sibling.csv`, `cosine_matrix_all_layers.csv`
- `layer_sweep.csv`, `layer_sweep_partial.csv`, `layer_sweep_heatmap.png`
- `opinion_summary.csv` (unreliable), `factual_summary.csv`, `transfer_summary.csv` (caution)
- `kaggle_run.log`: raw stdout/stderr (JSON lines), ends mid-PERSONA
