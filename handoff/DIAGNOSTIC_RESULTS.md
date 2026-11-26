# Run 10 diagnostic: results (Qwen 1.5B, 3B, 7B fp16, 14B nf4)

Kernel `arifurrhmn/lostinsteering-run10-diagnostic`, 4.9 h, all four models finished. Raw files: `results/10_diagnostic/diag/<model>/` (`summary.json`, `mc4_items.csv`, `pressure_items.csv`, `pool_sets.json`). Private; `handoff/` is not in git.

**The diagnostic reproduces Run 08 exactly.** The old-rule "known" counts equal the saved `probe_accuracy.csv` counts for every model and language, and the v1 baseline agreement equals Run 08's `baseline.csv` (for example 14B English 0.162/1.000, Bengali 0.608/0.985). So the comparisons below use the same code path as Run 08.

**What it did not test:** steered results. It measures item pools and baseline agreement only. Whether the headline drop in agreement with true claims survives on the surviving items has not been tested.

## 1. Item pool: the old pool is substantially contaminated, even at 7B and 14B

Pool size from scratch on all 608 valid items, by rule (items must pass in all six languages):

| Model | Old rule | Soft: correct in at least one option order | Strict: correct in both orders |
|---|---|---|---|
| 1.5B | 452 (pool capped at 200) | 124 | 23 |
| 3B | 198 | 162 | 37 |
| 7B fp16 | 166 | 216 | 89 |
| 14B nf4 | 173 (pool capped at 120) | 281 | 113 |

How much of the existing Run 08 pool survives the new rules:

| Model | Old pool | Survive soft | Survive strict |
|---|---|---|---|
| 1.5B | 200 | 54 (27%) | 11 (6%) |
| 3B | 198 | 66 (33%) | 22 (11%) |
| 7B | 166 | 85 (51%) | 49 (30%) |
| 14B | 120 | 88 (73%) | 53 (44%) |

So at 7B, about half of the old pool items fail even the soft test, and 70% fail the strict one. The strict rule leaves too few items at 1.5B and 3B (23 and 37) and workable pools at 7B and 14B (89 and 113). The soft rule leaves 124 to 281 items at every scale, but see section 5: it lets in many guessed items in Hindi and Bengali. (An earlier version of this file called the soft rule "stringent across six languages". That was wrong and is withdrawn.)

## 2. Baseline agreement on items the model really knows is lower than on the old pool

Agreement with false claims (agree_wrong), full eval pool versus the strict-rule subset (7B: n=42, 14B: n=44; small samples):

| | en | es | zh | hi | bn | ar |
|---|---|---|---|---|---|---|
| 7B, old eval pool | 0.33 | 0.45 | 0.26 | 0.64 | 0.52 | 0.51 |
| 7B, strict subset | 0.24 | 0.25 | 0.13 | 0.61 | 0.38 | 0.38 |
| 14B, old eval pool | 0.16 | 0.34 | 0.16 | 0.50 | 0.61 | 0.43 |
| 14B, strict subset | 0.04 | 0.23 | 0.04 | 0.49 | 0.50 | 0.32 |

The old pool inflates baseline sycophancy, because items the model does not know are counted as "agrees with a false claim". Agreement with true claims (agree_true) is at ceiling in both pools at 7B and 14B (0.97 to 1.00), so the worry that pool selection inflates the baseline for the headline measure is small at those scales. This is baseline-only evidence: the steered side is untested.

## 3. Prompt wording (v2 draft versus v1)

Bengali instruction wording ("বিকল্পের" removed): 4-option accuracy is essentially unchanged (7B: 0.467 to 0.464 original order; 14B: 0.562 to 0.572; 3B: 0.403 to 0.408; 1.5B: 0.326 to 0.326). So that wording did not measurably change what these models do. It is still unnatural Bengali and should be fixed for readers.

Teacher-line wording (agree_wrong, full eval pool, v1 to v2). In Bengali the v2 run changes both the teacher line and the instruction, so the two effects cannot be separated there.

| Model | en | es | zh | hi | bn | ar |
|---|---|---|---|---|---|---|
| 7B | 0.33 to 0.33 | 0.45 to 0.47 | 0.26 to 0.28 | 0.64 to 0.68 | 0.52 to 0.55 | 0.51 to 0.53 |
| 14B | 0.16 to 0.16 | 0.34 to 0.33 | 0.16 to 0.20 | 0.50 to 0.55 | 0.61 to 0.61 | 0.43 to 0.52 |
| 3B | 0.31 to 0.31 | 0.47 to 0.47 | 0.32 to 0.38 | 0.97 to 0.97 | 0.93 to 0.89 | 0.60 to 0.70 |

The v2 wording also raises agreement with true claims in several cells (3B Arabic 0.90 to 0.96, Chinese 0.88 to 0.93), so it looks like a general shift toward "yes", not a change in honesty. Effects are small at 7B (up to 0.04) and larger in some cells at 3B and 14B (Arabic +0.09 at 14B, +0.10 at 3B). Language ranking is mostly unchanged, but Arabic moves past Spanish and Hindi at 14B. English is identical by construction. The "quite sure" wording therefore matters at roughly the 0.05 to 0.10 level in some language and model cells. Which direction is "right" needs a native speaker.

## 5. How much of each rule's pool is guessed (from `mc4_items.csv`, no new runs)

Simple model: a known item is always answered correctly, an unknown item is a 25% guess independently in each option order. Then strict = k + (1-k)/16 and soft = k + (1-k)*7/16. Estimated share of each language's soft pool that is guessed (the model is a simplification; the two estimates of k agree closely in most cells, and P(reverse order correct | original order wrong) is about 0.22 to 0.36, near the 0.25 the model predicts):

| Model | en | es | zh | hi | bn | ar |
|---|---|---|---|---|---|---|
| 1.5B | 0.28 | 0.37 | 0.40 | 0.71 | 0.77 | 0.58 |
| 3B | 0.23 | 0.32 | 0.33 | 0.58 | 0.63 | 0.49 |
| 7B | 0.16 | 0.22 | 0.25 | 0.54 | 0.55 | 0.33 |
| 14B | 0.13 | 0.20 | 0.20 | 0.39 | 0.36 | 0.27 |

So the soft rule does not fix the contamination where it matters: more than half of the Hindi and Bengali items it admits are guesses at 1.5B, 3B and 7B. The strict rule is a much better filter (a guessed item passes it only 1 time in 16 per language). Consequence: the consistent single rule is **strict at every scale**. Under it, 1.5B (23 items) and 3B (37 items) fall into the "partial" or "drop" tiers of the E4 rule, which is a valid outcome, not a reason to loosen the rule. Even under the strict rule, 1.5B Hindi and Bengali are mostly guessing (k about 0.10 to 0.15).

## 6. Steered check on the existing Run 08 results (`results/10_diagnostic/steered_subset_check.json`)

The Run 08 cache stores per-item agreement for every steered condition. Keys were rebuilt from the Run 08 source and found in the cache (layer 16 at 1.5B and 7B, 23 at 3B, 26 at 14B; the factual vector's sign is -1). Drop in agreement with true claims under English CAA anti-steering (multiplier 8), full eval pool versus the strict-rule subset. **Small samples:** strict subsets are n=10 (1.5B), 20 (3B), 42 (7B), 44 (14B), with bootstrap 95% CIs. Vectors were still built from the old pool, so this is a check of the result on cleaner evaluation items, not a clean rerun.

| Model | n | en | es | zh | hi | bn | ar |
|---|---|---|---|---|---|---|---|
| 7B full pool | 133 | 0.42 | 0.38 | 0.66 | 0.66 | 0.81 | 0.57 |
| 7B strict subset | 42 | 0.24 (0.14 to 0.36) | 0.23 (0.13 to 0.34) | 0.52 (0.40 to 0.64) | 0.56 (0.44 to 0.69) | 0.70 (0.59 to 0.81) | 0.42 (0.30 to 0.55) |
| 14B full pool | 96 | 0.51 | 0.32 | 0.78 | 0.66 | 0.79 | 0.57 |
| 14B strict subset | 44 | 0.45 (0.32 to 0.57) | 0.29 (0.18 to 0.42) | 0.74 (0.62 to 0.85) | 0.56 (0.46 to 0.65) | 0.73 (0.61 to 0.83) | 0.51 (0.38 to 0.64) |

- The effect is still large and clearly above zero in every language at 7B and 14B on the cleaned items. The random-vector drop is about 0.00 on both the full pool and the subset, so the drop is not a generic perturbation.
- The magnitude was overstated by the old pool: at 7B the strict-subset drop is about 57% to 86% of the full-pool drop depending on language (English 0.24 against 0.42, Spanish 0.23 against 0.38). At 14B it is about 85% to 91%. Steering is less effective on items the model really knows, which is plausible.
- At 3B (n=20) and 1.5B (n=10) the subset drops are similar to the full-pool drops, but the subsets are too small to say more.
- Baseline agreement with true claims on the subsets is 1.00 or close at 7B and 14B, so selecting the pool on that quantity does not inflate the baseline there.

**Honesty note on the threshold.** The advisor asked that the criterion for "the headline holds" be written down before computing this. I ran the numbers first and did not record a threshold beforehand. Read afterwards, the proposed criterion (subset drop at least half the full-pool drop, CI lower bound above 0, in at least 5 of 6 languages) is met at 7B and 14B in 6 of 6 languages. Because it was chosen after the numbers were seen, treat that as a description of the result, not a pre-registered test.

## 4. What this means for the rerun decision (updated after sections 5 and 6; supersedes the soft-rule suggestion below)

- **The headline survives.** At 7B and 14B the English-vector drop in agreement with true claims holds on items the model really knows, with a smaller size in some languages. A rerun is therefore not needed to rescue the main claim.
- **A rerun is about clean magnitudes, cross-language baselines and comparability with the new families.** Old-pool baselines overstate sycophancy, and the new families will use a cleaner pool.
- **Rule choice:** strict at every scale (section 5). Pools: 23 / 37 / 89 / 113 at 1.5B / 3B / 7B / 14B. Small models become partial or drop tiers.
- **Cheaper rerun option:** rerun only 7B and 14B (about 19 h) under the strict rule, and report 0.5B to 3B as v1 results with a caveat, instead of rerunning all of Qwen (about 30 h). New families run the strict rule from the start. This is a decision for you and the supervisor.

(Original section 4, kept for the record, is below; its soft-rule suggestion is withdrawn.)

## 4 (original). What this means for the rerun decision

- The pool problem is real at every scale tested, including the 7B and 14B models that carry the headline. A rerun under a corrected pool rule is justified for any claim that compares languages.
- The wording problem is smaller than the pool problem: negligible at 7B, up to about 0.1 in a few cells at 3B and 14B.
- The strict rule only gives usable pools at 7B and 14B. A single rule across all scales is needed for comparability. The soft rule is the only one that gives 124 to 281 items at every scale. Using strict at 7B and 14B and soft below would mix rules and break comparisons across scale.
- Not tested: whether the steering headline holds on the surviving items. That needs the saved steering vectors and per-item steered scores from Run 08 (`vectors.pt` and `_cache` exist locally; whether the cache supports per-item rescoring is unchecked).

Open decisions: which pool rule (soft for all scales with a strict-subset sensitivity check at 7B and 14B is the option that fits the data), and the numeric thresholds for "headline holds", which were not set before the run.
