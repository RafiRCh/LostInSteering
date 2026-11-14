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

### Step 1: knowledge probe (`notebooks/02_knowledge_probe.ipynb`) - ready to run

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

### Step 2: steering v2 (`notebooks/03_steering_v2.ipynb`) - to be written after step 1

Same design as smoke test v1, with these changes:
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
