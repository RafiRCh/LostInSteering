# Steering v2b (debiased vector): results notes

**Run:** 2026-11-15 on Kaggle (2× T4), notebook `notebooks/03b_steering_v2_debiased.ipynb`, Kaggle kernel `arifurrhmn/notebook0b33290537`.
Full run, `Qwen/Qwen2.5-7B-Instruct`, `VECTOR_TYPE = "caa_debiased"`, runtime about 2 h 56 min. Everything else is identical to
[`../03_steering_v2/NOTES.md`](../03_steering_v2/NOTES.md) (same 128 items, same folds, same seed).
Output folder: `steering_v2/` (`.pt` vector file git-ignored).

**Why this run:** run 03 failed checks 5 and 6 (the original vector lowers agreement with true claims as much as with wrong ones).
`caa_debiased` = (agree minus disagree on WRONG claims) minus (the same difference on TRUE claims), meant to remove a plain "say yes" direction.

**Verdict printed by the notebook: NOT YET.** Checks 3, 4 and 5 fail. Check 6 passes only because the chosen vector does almost nothing.

| | Original (03) | Debiased (03b, notebook's chosen layer 13) |
|---|---|---|
| English steerability | 0.33 | 0.03 |
| Native beats random | 6 of 6 | 3 of 6 (Hindi, Bengali "pass" only with negative English-to-native ratios) |
| English honesty change | -0.12 | +0.007 (CI -0.010 to +0.027) |
| English agree_true drop | 0.27 | 0.007 |
| Cosine to English vector at best layer | 0.81 to 0.92 | 0.11 to 0.54 |

Cosine between the original and debiased English vectors is between -0.28 and +0.31 across layers 12 to 23, so subtracting the true-claim
difference changes the direction a lot: the original vector was mostly the generic "agree" direction.

## An important caveat, found after the first read (do not skip)

The notebook picks `BEST_LAYER` with `idxmax` of English steerability, i.e. the **most positive** value. For the debiased vector the
layer sweep shows large **negative** steerability at layers 14 to 17 (English vector, English items):

| layer | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|
| steerability | -0.17 | -0.24 | -0.56 | **-0.63** | -0.07 |

A negative value means adding the vector **lowers** agreement with the wrong claim: the debiased direction does have a strong effect at
layers 16 to 17, but with the opposite sign to the one the notebook assumes, and `idxmax` ignored it (it picked layer 13, steerability 0.007).
So the statement "debiasing removes the steerable direction" is **not established**. What is established: at the layer the notebook chose, there is no effect;
and the sign convention for the debiased vector may need flipping. We do not yet know what honesty (agree_true minus agree_wrong) does at layers 16 to 17
with the sign flipped; the final evaluation never ran there.

## What we can say now

- The original agree direction transfers across languages almost fully (run 03), but it is not sycophancy-specific.
- The simple debiasing here did not give a working, honest sycophancy vector at the layer the notebook picked.
- There is an unexplored lead: debiased vector, layers 16 to 17, sign flipped (or select layer by absolute steerability).

## Next step (not done)

Rerun the evaluation steps with `BEST_LAYER` chosen by |steerability| and the sign taken from the English sweep, then check checks 3 to 6.
Vectors are in the Kaggle output (`vectors.pt`, git-ignored); `kaggle kernels output arifurrhmn/notebook0b33290537` re-downloads them.

## Files

Same layout as run 03 (`steering_v2/` plus `notebook0b33290537.log`): `checks.json`, `transfer_summary.csv/.png`, `dose_response.csv/.png`,
`layer_sweep.csv`, `calibration.csv`, `baseline.csv`, cosine files, `per_item_results.csv.gz`, `generations.csv`, `item_pool.json`.
