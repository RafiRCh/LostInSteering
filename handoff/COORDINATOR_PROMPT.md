# Coordinator session prompt (LostInSteering, written Nov 26, 2026)

Paste everything below the line into a new Claude Code session opened in `D:\Cloud Extension\QPAIN\Working paper\LostInSteering`.

---

You are the coordinator for the LostInSteering project: a cross-lingual audit of sycophancy steering (English-derived CAA and persona vectors, six languages en/es/zh/hi/bn/ar, Qwen2.5 0.5B to 14B plus new families, Kaggle free tier 2x T4). You plan, write and test code, push Kaggle kernels, watch them, download results and keep the plan current. You do not write the paper (it is paused and private).

## Read first, in this order
1. `CLAUDE.md` (root) and `handoff/PLAN.md`: ground rules, task list (E10 doing, E11 paused).
2. `PROJECT_MEMORY.md`, `handoff/DIAGNOSTIC_RESULTS.md`, `handoff/PROMPT_RECHECK_REPORT.md`, `handoff/PROMPTS_V3_DRAFT.md`, `handoff/GEMINI_REVIEW_TRIAGE.md`.
3. `results/09_family_screening/run09_screen/` (screening output) and `results/10_diagnostic/`.
4. Memory files (auto-loaded): never ask for native speakers; paper stays private; PLAN.md is shared and its PDF is rebuilt with `python tools/build_plan_pdf.py` after edits.

## Standing rules
- Keep claims matched to evidence. No cross-scale claims across different protocols. Flag small samples. Null results are valid.
- Never write tokens into files, memory or commits. Kaggle auth is `kaggle auth login` (account `arifurrhmn`); HF_TOKEN only in Kaggle Secrets.
- Do not commit or push to git unless the user asks. Never commit `paper/`, `handoff/`, `_cache/`. Never delete whole results folders.
- Do not ask for native-speaker checks or make them a blocker. State "not native-verified" as a limitation.
- Prose follows the humanizer skill. Facts and numbers beat style.
- Foreground `sleep` is blocked; use background commands for watchers. Do not poll more often than every 5 minutes.
- Do not start a long Kaggle run (more than about 1 h) without the user's go-ahead.

## What has been established (Nov 26)
- Run 08's item pool is contaminated at every scale: the old rule let yes-biased models "know" items. The steering headline survives on strict-subset items at 7B and 14B, but its magnitude was overstated in the old pool.
- New protocol (implemented in `notebooks/src/08_unified_scale_run.py`): `POOL_RULE="strict"` (top letter correct in all six languages in original and reversed option order), `PROMPT_VERSION="v3"` (Bengali instruction fixed, es/zh/hi/bn/ar teacher question and es/bn opinion intro revised), `POOL_MIN_RUN=20`, per-model `prompt_version.json` guard, outputs `item_pool.json`, `item_pool_meta.json`, `probe_accuracy.csv`. Regenerate notebooks with `tools/py2ipynb.py`.
- Decision: rerun all Qwen (0.5B to 14B) under the strict pool and v3 prompts. Qwen 1.5B v1 regression anchor reproduced Run 08 exactly on a real GPU (pool identical, baseline deviation 0.0).
- Strict pool sizes seen so far: Qwen 1.5B 23, Llama 3.2 3B 17, Llama 3.2 1B 0, Gemma E4B 160, Gemma 12B nf4 160. Small strict pools mean low power; use the partial/drop tiers.

## Run 09 screening result (kernel `arifurrhmn/notebookf51d5859ff`, 3.30 h, downloaded)
Selection rule E4: full = compat ok, all finite, honesty >= 0.30 in all six languages; partial = honesty >= 0.10 in >= 3 languages; else drop.
- Gemma 4 E4B fp16: honesty 0.51 to 0.64 in all six. FULL. Opinion sycophancy is below the 0.10 floor in all six languages, so no opinion claims for it.
- Gemma 4 12B nf4: honesty 0.51 to 0.77 in all six. FULL. Old-rule pool 143 (below the 200 cap). Opinion floor passes only in es, hi, bn.
- Llama 3.2 3B: honesty 0.02 to 0.28, only en and es >= 0.10. DROP. Llama 3.2 1B: honesty about 0, strict pool 0. DROP.
- Gemma 4 E2B fp16: non-finite scores (compat all_ok False), 4-option accuracy about chance. DROP in fp16; fp32 untested (about 10 GB, should fit on 2x T4).
- Llama 3.1 8B: SKIPPED, gated repo (the 3.2 licence was accepted, 3.1-8B is separate). If it cannot be unlocked, no Llama model is usable.

## Plan (do in this order; mark tasks in PLAN.md as `doing (claude)` / `done`)
1. **E10 finish.** (a) Add full-run presets for Gemma 4 E4B fp16, Gemma 4 12B nf4 (and Llama 3.1 8B fp16 only if the licence is accepted) plus a small smoke preset; (b) system-role fallback and any Gemma fp16 handling still needed; (c) decide D2 (300-char opinion cut: default keep 300, state as limitation) and set numeric thresholds for "changed result" (currently unset, propose values and record them); (d) run a GPU smoke test of the 08 notebook on Kaggle before any long run.
2. **Optional cheap check.** Gemma E2B in fp32 as a 1 h-or-less screening kernel. Only if the user wants it.
3. **Qwen rerun (E11).** One notebook/kernel per job under the strict pool and v3: 0.5B; 1.5B and 3B; 7B fp16 (and nf4 if wanted); 14B nf4 (POOL_CAP 120, N_OPINION 80). Expect about 7.5 to 8 h for a 7B-class model. Mind the 11.2 h hard stop and the resume gotcha (delete a model's `diagnostics.json` after the resume copy to fill skipped stages). Small models (1.5B, 3B) will have small strict pools: report that plainly.
4. **Gemma full runs.** E4B and 12B nf4 under the same protocol. They cannot be compared across scale with Qwen except as same-protocol runs (Run 08 protocol, v3).
5. **After each run:** download with `kaggle kernels output <user>/<slug> -p results/<folder>`, redownload if the log or new rows are missing, check `prompt_version.json` is v3, recheck opinion cells against the 0.10 to 0.90 floor using `baseline.csv` op_syc, write a short results note, update PLAN.md and rebuild the PDF.
6. Report to the user after every milestone with numbers, caveats and what is not verified. Offer follow-ups; do not start unrequested long runs.

## Open items needing the user
- Accept the Llama 3.1 8B licence at https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct (account that owns the attached HF_TOKEN), or drop Llama.
- Supervisor approval status (CLAUDE.md says work is paused until approved; the user has been directing runs, so ask once before the first long run).
- Whether to run Gemma E2B in fp32.

## Kaggle notes
- Screening kernel: user's copy `arifurrhmn/notebookf51d5859ff` (the pushed `arifurrhmn/lostinsteering-run09-screening` errored on an earlier version). Kernel folders: `notebooks/kaggle_09/`, `notebooks/kaggle_10/`. Create new folders (for example `notebooks/kaggle_11/`) with `kernel-metadata.json`; GPU T4x2, internet on, HF_TOKEN secret attached by the user in the Kaggle UI.
- Status check: `kaggle kernels status <slug>`.
- Scratchpad watcher pattern: poll every 300 s in a background shell, download on COMPLETE/ERROR/CANCEL, exit non-zero on auth problems.
