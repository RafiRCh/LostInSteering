# Roadmap

Last updated: 2026-11-14

## Scope decision

This paper stays about **sycophancy**. One extra behavior, **refusal**, may be added only as a reference point
(earlier work found refusal directions carry over across languages), so the paper can say "refusal transfers,
sycophancy does / does not". A broad "does steering transfer for every behavior" study is a separate, later paper
(see `vault/00 - Backlog.md`).

## Contributions we are aiming for

1. **Main finding:** how much of the English vector's effect carries over to each language.
2. **Fair method:** compare the English vector with a vector built in each language (the "transfer gap").
3. **Where and why it breaks:** by language (resource level), by kind of sycophancy, by layer, plus side effects.
4. **Bonus:** release the multilingual test items.

## Next steps: how to run the v2 tests

v2 is two notebooks run in order. The first decides the model and the clean question pool for the second.

### Step 1: knowledge probe (`notebooks/02_knowledge_probe.ipynb`) - done 2026-11-14, Qwen2.5-7B chosen (74 items)

What it does: tests Qwen2.5-7B, Mistral-7B and Phi-3.5-mini in all 6 languages on arithmetic (3 difficulty
levels) and on Global-MMLU-Lite (human-translated exam questions, public). Then, on questions the model knows in
all 6 languages, it measures how often the model caves to a "teacher" with a wrong answer.

1. Import it on Kaggle, **GPU T4 x2**, **Internet On**, then **Save & Run All (Commit)**. Rough estimate: 40 to 60 min.
2. Download: `kaggle kernels output <user>/<slug> -p results/02_knowledge_probe/`
3. Look at `model_choice_summary.csv` (last cell). It flags which models are usable:
   knows enough in every language, has 60+ questions known in all 6, is actually sycophantic, and still separates
   right from wrong.
4. Write `results/02_knowledge_probe/NOTES.md` and **decide the model for v2**.

What to watch for:
- `known_in_all_6` below about 60 for every model → raise `N_MMLU` to 615 (all available) or add a gated model.
- `agree_wrong` near 0 for a model → it is not sycophantic on facts; use it only as a contrast.
- Big `agree_wrong` differences between languages for one model are already a result worth noting.

### Step 2: steering v2 (`notebooks/03_steering_v2.ipynb`, `03b`, `03c`) - runs complete, verdict NOT YET (see `results/03_steering_v2/`, `03b_steering_v2_debiased/`, and `03c_steering_v2_debiased_flip/`)

**Results summary (2026-11-16):**
- **Run 03 (original CAA):** clear effect at layer 17, transfers to all 6 languages (ratio 0.8 to 1.5), but lowers agreement with true claims too, degrading honesty (checks 5 & 6 fail).
- **Run 03b (debiased vector):** layer selection chose layer 13 (steerability ~0.03); revealed large negative steerability at layers 16 to 17 (-0.63 at layer 17).
- **Run 03c (debiased, sign flipped, layer 17):** massive steerability (0.61 EN) and near-perfect multilingual transfer (ratios 0.96 to 1.07 across all 6 languages, cosine similarities 0.89 to 0.96). However, anti-steering induces generic contrarianism: agree_wrong drops from 0.23 to 0.002, but agree_true collapses from 0.85 to 0.10, causing honesty to drop by -0.52 (checks 5 & 6 fail decisively).

**Key takeaway & Next directions:**
1. **Empirical finding established:** The acquiescence/agreement direction is deeply multilingual and transfers cleanly across high- and low-resource languages (Spanish, Chinese, Hindi, Bengali, Arabic).
2. **Methodological boundary:** CAA difference-in-means vectors (even when debiased against true-claim differences) act as an "agree <-> disagree" dial, failing to isolate sycophancy from general factual agreement on teacher-framed QA items.
3. **Paths forward:**
   - Report this as a primary finding: steering general agreement vs sycophancy-specific steering.
   - Test alternative sycophancy formulations where agreement does not conflate with factual correctness: e.g., opinion-based sycophancy (original Anthropic dataset), caving under pushback (re-asking questions), or over-praise.
   - Alternatively, evaluate intermediate/gentle steering multipliers (e.g. -1 to -2) or persona-based steering vectors.

### Step 3: Complete Paper Run (`notebooks/04_complete_paper_run.ipynb`) - done 2026-11-16 (see `results/04_complete_paper_run/NOTES.md`)

**Results Summary:**
- Executed in **55 minutes** on 2× Tesla T4 with dual-GPU balanced memory allocation (7.62 GB per GPU).
- **Factual CAA Truth Collapse:** Confirmed across all 6 languages (agree_true drops by 16.7% to 35.1%; EN: -35.1%, ES: -21.3%, ZH: -23.8%, HI: -21.6%, BN: -16.7%, AR: -27.5%).
- **Persona Vector Success:** Steering with an English "objective evaluator" persona vector preserves **85% to 97%** of true claim agreement (EN: 95.1%, ES: 97.1%, ZH: 91.4%, AR: 93.4%, HI: 88.2%, BN: 84.6%), solving the truth collapse of CAA.
- **Multilingual Transfer:** Cross-lingual transfer ratios remain high across diverse scripts (mean ratio ~1.03).
- **All primary experiments complete.** Camera-ready tables and figures generated in `results/04_complete_paper_run/complete_paper_results/`.

### Step 4: Cross-Model Generalization Audit (`notebooks/05_cross_model_audit.ipynb`) - ready to run

**Objective:** Verify whether the factual honesty collapse under anti-steering replicates across model families (meta-llama/Llama-3.1-8B-Instruct or CohereForAI/aya-23-8B).
- Tests the exact same 128 Global-MMLU-Lite item pool across all 6 languages.
- Hardware: Kaggle 2× T4 GPU, Internet On. Requires `HF_TOKEN` in Kaggle Secrets if running Llama-3.1.
- Est. runtime: ~2.0 hours.


How to run: import on Kaggle (GPU T4 x2, Internet On). First set `QUICK = True` and run it once (~30 min, 1.5B model)
to check the code; then set `QUICK = False` and *Save & Run All (Commit)*. The full run takes about 3 to 5 h; the
notebook prints an estimate after step 1 and checkpoints CSVs after every step. Download into `results/03_steering_v2/`.

How the notebook solves the "only 74 items" problem: it re-probes **all 615** Global-MMLU-Lite questions (notebook 02
used 300), keeps those known in all 6 languages (expected ~150), and uses **5-fold cross-fitting**: vectors for each
fold are built from the other folds, so every item is used for building *and* testing but never both at once.
The translated opinion dataset is **not** in this notebook; it is left for a later `03b`/`04` if needed.

Original plan (what the notebook implements):
- items: the `known_all_langs__<model>.json` list from step 1 (questions the model knows), plus the opinion
  sycophancy dataset from the original CAA work, translated;
- A/B balanced: each item shown with "agree" as A and as B;
- 150 to 200 vector-building items per language, separate test items;
- multipliers up to about ±8, vector scaled to each layer's typical activation size; finer layer sweep (12 to 23);
- honesty score (agree_true − agree_wrong) next to agree_wrong;
- bootstrap error bars; report the transfer ratio only where the native vector clearly beats the random one;
- save all vectors (`torch.save`) so later analyses (e.g. Hindi → Bengali) need no re-run.

Pass condition: clear English effect, native vectors beat random in at least 4 languages, honesty score improves
(not just less agreement overall).

### After v2 passes

1. Add 2 to 3 kinds of sycophancy (agreeing with wrong facts, caving under pushback, over-praising).
2. Check whether ready-made persona vectors (Chen et al. 2025; Kelkar et al. 2026) can be downloaded for our model.
   If not, drop that comparison from the proposal.
3. Native-speaker checks for Bengali, Hindi, Arabic items (start finding people now; it takes longest).
4. Second model, final runs, writing.

## Supervisor update (draft talking points)

Pipeline proven on free Kaggle in under 30 minutes; steering signal present in all 6 languages; early sign that
the English vector lines up less with Hindi and Bengali. The test task is being redesigned because the model did
not know enough arithmetic. Ask: is "sycophancy + refusal as a reference point" an acceptable scope?
