# LostInSteering work plan

Shared between you and every Claude session. This file is the source; `handoff/PLAN.pdf` is built from it with `python tools/build_plan_pdf.py`. Last updated Nov 21, 2026. Mode: ALL WORK PAUSED (Nov 21). The next step is a proposal to the supervisor; Kaggle runs and everything else wait until it is approved. The paper stays private.

## How to use it

- Before starting a task, check that everything in its "Needs" column is `done`. Then set its status to `doing (you)` or `doing (claude)`.
- When it is finished, set `done`, add the PR or commit to the task's notes below, and rebuild the PDF.
- Claude sessions read this file at the start of substantial work (CLAUDE.md points here). If you did something outside a session, mark it here so the next session knows.
- Days are rough calendar spans for the chart, not promises. Kaggle tasks count wall-clock time, mostly unattended. Free Kaggle GPU quota is about 30 h a week (check your quota page), so full runs spread over weeks.
- Model column: which Claude model to run the session on. Opus 5.5 for protocol design, notebook changes and analysis. Sonnet 5.5 for git, downloads, verification and routine code. Haiku 5.5 for small text edits. "None" means a manual step for you.

## Tasks

| ID | Task | Owner | Needs | Days | Model | Status |
|---|---|---|---|---|---|---|
| E1 | Write the model screening notebook | Claude | - | 1 | Opus | done |
| E2 | Accept gated licences on Hugging Face (Llama, Gemma) | You | - | 0.1 | None | paused |
| E3 | Run the screening notebook on Kaggle | You | E1, E2 | 0.5 | None | paused |
| E4 | Pick the families for full runs from the screening | Both | E3 | 0.2 | Opus | paused |
| E5 | Extend the Run 08 notebook to the picked families | Claude | E4 | 1.5 | Opus | paused |
| E10 | Code the corrected protocol: v2 prompts, strict pool rule, no padding fallback; screening notebook reports strict and soft pool sizes and guessed share | Claude | E4 | 1 | Opus | doing (claude) |
| E6 | Kaggle smoke test of the extended notebook | You | E5, E10 | 0.5 | None | paused |
| E11 | Rerun all of Qwen (0.5B to 14B) under the corrected protocol, old results kept as v1 | You | E6 | 8 | None | paused |
| E7 | Full Run 08 on each picked model | You | E6 | 6 | None | paused |
| E8 | Download, verify and floor-check the new results | Claude | E7 | 0.5 | Sonnet | paused |
| E9 | Cross-family analysis (same metrics as Qwen) | Claude | E8 | 2 | Opus | paused |
| Q1 | Optional: fill skipped 7B nf4 stages (Qwen) | Both | - | 1 | Sonnet | paused |
| Q2 | Optional: 7B nf4 rerun on the fp16 item pool (Qwen) | Both | - | 1 | Sonnet | paused |
| Q3 | Optional: larger opinion item pool | Both | E5 | 3 | Opus | paused |
| H1 | Update the repo README status table | Claude | - | 0.1 | Haiku | paused |

## Candidate model families

Decision (Nov 21): the next Kaggle phase adds two new families, Gemma and Llama, small models only (each run finishes in one Kaggle session). No new Qwen runs: Qwen2.5 0.5B to 14B is already done under Run 08. Muse and DeepSeek are out because no small version exists. Release facts come from web searches on Nov 21, not from checked Hugging Face model cards; E1 confirms repo names, sizes and licences first.

Hardware limit: 2x T4 (16 GB each, no bfloat16, so fp16 or nf4 only) and an 11.2 h Kaggle session. Run 08 took about 2 h at 1.5B, 5 h at 3B, 7.5 to 8 h at 7B and 10.8 h at 14B nf4.

The real filter is knowledge: Run 08 keeps only items the model knows in all six languages, so every model is screened first (E1, E3).

| Family | Models | Sizes that fit | Licence | Risk on T4 or Run 08 |
|---|---|---|---|---|
| Gemma (Google) | Gemma 4, the latest generation (Apr 2026) | E2B, E4B fp16; 12B nf4 if the model card's 12B is released | Check model card | High. Gemma 3 overflowed in fp16 on T4 and Gemma 4 is untested there. Image-text models with a new per-layer-embedding architecture; needs a recent transformers |
| Llama (Meta) | Llama 3.2 Instruct 1B and 3B (Sep 2024), Llama 3.1 8B Instruct (Jul 2024) | 1B, 3B, 8B fp16 | Llama Community, gated | Low on the technical side: standard layers, system role works, notebook 06 already targeted 3.1-8B. Languages: officially 8 incl. en, es, hi; zh, ar and bn are not official, so Bengali may fail the probe |

Why these Llama versions: they are the newest Meta models that run on Kaggle. Llama 4 (Apr 2025) has no small dense model, Meta has released no Llama since, and its successor Muse comes as a 30B model (Muse Glimmer) or larger. This is the answer to "why not the latest Meta model", and the paper should say it.

Not used:
- New Qwen generations (Qwen3.5, Qwen3.8): Qwen is already covered by the Qwen2.5 sweep.
- Muse Glimmer (30B) and Muse Spark Open (816B MoE): no small version, and 30B needs 2 to 3 sessions.
- DeepSeek: its current open models (V4-Flash 284B MoE, V4.1-Flash 552B backbone) are far beyond 2x T4. R1-Distill models are 2025 Qwen and Llama fine-tunes, not a separate family.
- Mistral, Phi, Aya and the rest: out of scope.

Rough Kaggle budget: Llama 1B, 3B, 8B about 15 h; Gemma 4 E2B, E4B about 8 h, plus 12B about 10 h if it exists. About 25 to 35 h, roughly one week of free quota.

## Already done (Nov 21)

- Skills installed in `.claude/skills/` (paper-writer, humanizer v4.0.0 offline copy).
- PR 1 merged into main as 1c72467: notebook opinion floor check is 0.10/0.90.
- PR 2 merged into main as 691bef7: final Run 08 results, one folder per job, duplicates removed.
- Local checkout synced to 691bef7. All `_cache` files and `vectors.pt` kept. `paper/` and `_cache/` are excluded from git in `.git/info/exclude` (local only).
- Opinion floor recheck: `paper/OPINION_FLOOR_RECHECK.md`. "20 of 30 cells pass" holds. The 14B en, es and hi passes sit within one or two items of 0.10.
- Paper loader repointed: 7B reads from `notebook_1_final` with three fp16 files from `7b_dose_all_langs_recheck`. Tables and figures rebuild byte-identical.

## Decisions (Nov 21)

- Everything below is paused until the supervisor has seen and approved a proposal. Draft: `proposal/supervisor_proposal.md` and `.pdf` (local only, excluded from git; PDF built with `python tools/md_to_pdf.py`). Resume from E2 (licences) and E3 (run the screening kernel).

- Experiments first. All paper work is paused until the Kaggle runs are done.
- The next Kaggle phase runs only small Gemma and Llama models (Gemma 4 E2B, E4B, maybe 12B; Llama 3.2 1B, 3B and 3.1 8B), one Kaggle session each. No new Qwen runs; Qwen2.5 is the completed sweep. No Muse, DeepSeek or other families.
- The paper stays private. Never commit or push `paper/` to the repo, which is public.
- No native-speaker check is available. When the paper resumes, state it as a limitation: the factual templates and opinion translations were not checked by native speakers.
- The leaked Kaggle token is the user's call; no task for it here. Tokens still never go into files or commits.
- Access to the private Paper-Writer repo is not needed for now; the offline skill copy works.

## Decisions (Nov 26)

- **Rerun all of Qwen (0.5B, 1.5B, 3B, 7B, 14B) under the corrected protocol,** then the new families under the same code. The cheaper "7B and 14B only" option was offered and not chosen. Reasons and evidence: `handoff/PROMPT_RECHECK_REPORT.md`, `handoff/DIAGNOSTIC_RESULTS.md`, raw files in `results/10_diagnostic/`.
- **Pool rule: strict at every scale** (the model's top letter among A to D is correct in all six languages, in the original and in a reversed option order). The soft rule (either order) was rejected: the Run 10 diagnostic estimates that more than half of the Hindi and Bengali items it admits are guessed at 1.5B, 3B and 7B. Pools from scratch: 23 / 37 / 89 / 113 items at 1.5B / 3B / 7B / 14B. Small models (1.5B, likely 0.5B and 3B) will fall into the partial or drop tiers of E4; that is a valid outcome. The padding fallback in the code is removed.
- Run 10 diagnostic done (Nov 26): the Run 08 steering headline holds on cleaned items at 7B and 14B (smaller in some languages; the old pool overstated the size); the old Run 08 results stay as the "v1 protocol" for a sensitivity comparison.
- No native speakers are available (user, Nov 26). The native-speaker check is dropped as a blocker. Substitute: the Gemini review (done, triaged in `GEMINI_REVIEW_TRIAGE.md`), back-translations in the prompt files, and an explicit limitation in the paper. `PROMPTS_V3_DRAFT.md` is the final prompt text unless the user changes it.
- Still open before any rerun: the 300-character opinion cut (D2); numeric thresholds for what counts as a changed result when v1 and v3 are compared (not yet set); whether the screening runs on the v3 prompts or the v1 prompts (see E10); supervisor approval. Everything stays paused until then.

## Decisions (Nov 25)

- Full rerun of every model (Qwen and the new families) under one corrected protocol; the old Qwen results stay as the "v1 protocol" and become a prompt-sensitivity comparison. Details and reasons: `handoff/PROMPT_RECHECK_REPORT.md`. Still paused until the supervisor approves.
- **Item pool definition changes (approved by the user Nov 25).** The v1 probe counted an item as known when the model preferred "Yes, you are right" to a true teacher claim, which a yes-biased model passes. The rerun builds the pool from the 4-option exam question instead. Proposed rule (to confirm when E5 is coded): the model's top letter among A to D is the correct one in all six languages, in the original option order and in one reversed order, to limit letter bias. Side effects to expect: pools shrink, most for Bengali and Hindi and for small models; the "pad with items known in most languages" fallback in the code must be removed or made explicit; per-model pool sizes must be reported. The screening notebook should report pool size under both the old and the new rule.
- Prompt text for the rerun comes from `handoff/PROMPTS_V3_DRAFT.md` (intensity wording, Bengali instruction, gender wording; no native-speaker check, stated as a limitation). The 300-character opinion cut is still an open decision (D2 in `PROMPTS_V2_DRAFT.md`).

## Paused: paper

Resume these after E9. Before writing, check how `main.tex` describes the item pool: the Run 08 probe counts an item as known when the model agrees with the true answer shown in slot A, which a yes-biased model passes (Qwen 0.5B passed 604 of 608 in Bengali). In order: compile the IEEE draft (Overleaf or local TeX); review the compiled PDF against the evidence (Opus); revise it, adding the small-sample flags and the native-speaker limitation (Opus, paper-writer); refresh citations, including the Persona Vectors NeurIPS 2026 proceedings entry and the two 2026 sycophancy preprints (Sonnet); add the cross-family results (Opus); choose the venue and prepare the submission (Opus). If any committed file mentions the paper's contents, keep it out of the public repo until submission.

## Task notes

### E1 Screening notebook
- Built as a `screen` preset inside `notebooks/src/08_unified_scale_run.py`, so the screen runs the exact code the full runs will use. Kaggle notebook: `notebooks/09_family_screening.ipynb` (generated from the source with `PRESET = "screen"`; regenerate, don't edit it).
- Per model it runs load, compatibility checks, the Run 08 probe and pool, a 4-option MMLU accuracy per language (chance 0.25), and the Run 08 baseline. It writes `screening.json` per model and `screening_summary.csv`, never `diagnostics.json`.
- Compatibility checks: model class and decoder-layer path, manual head vs full forward (and logit softcapping), BOS exactly once, system role kept, chat-template date pinned (Llama 3.x writes today's date otherwise), letter tokens A to D, fp16 activation headroom, non-finite scores per language, steering hook changes scores and stays finite.
- Qwen2.5-1.5B runs first as a regression anchor: its item pool must match Run 08 exactly and its baseline within 0.005. If the anchor fails, stop and check before reading anything else.
- The loader now handles image-text models and other layer paths; for Qwen it resolves to the same modules as before, and Qwen's chat text is unchanged.
- Status (Nov 21): built, not committed. Kernel folder `notebooks/kaggle_09/lostinsteering-run09-screening/` (private kernel `arifurrhmn/lostinsteering-run09-screening`, version 1 pushed Nov 21; https://www.kaggle.com/code/arifurrhmn/lostinsteering-run09-screening). Local CPU dry run on Qwen2.5-0.5B was stopped early at the user's request: compatibility checks passed (layer path `model`, letters, system role) and the probe started; nothing after that was tested locally. Qwen chat text is unchanged by the new date argument (checked on 0.5B and 1.5B tokenizers).
- Order: Qwen2.5-1.5B anchor, Llama 3.2-1B, Gemma 4 E2B, Llama 3.2-3B, Gemma 4 E4B, Llama 3.1-8B, Gemma 4 12B nf4 (skipped if the repo does not exist). Estimated 4 to 5 h. Gated repos that are not accepted are skipped with a message, not a crash.

### E2 Gated licences
- On Hugging Face, accept the licence pages for meta-llama/Llama-3.2-1B-Instruct, Llama-3.2-3B-Instruct and Llama-3.1-8B-Instruct, and any gated Gemma 4 repos, with the account whose HF_TOKEN is in Kaggle Secrets.

### E3 Run the screening
- Kaggle: the kernel is already pushed (see E1). Open it, attach the HF_TOKEN secret (Add-ons > Secrets), check the accelerator is GPU T4 x2, then Save and Run All. The pushed version 1 runs without the secret and stops at the token check. If it stops early, attach its output as input to a new run; finished models are skipped.
- Download the output to `results/09_family_screening/`. Check the REGRESSION ANCHOR line first.

### E4 Pick families
- Rule, fixed before the screen runs and calibrated on Qwen2.5 baselines (honesty = agree_true minus agree_wrong on the Run 08 pool):
  - Qwen anchors: 0.5B has honesty under 0.03 in every language (uninformative). 1.5B is at least 0.10 in 3 of 6 languages (hi, bn, ar near 0). 3B is at least 0.10 in 4 of 6 (hi 0.03, bn 0.07). 7B and 14B are at least 0.33 in all six.
  - Full: compatibility all_ok (or a failure E5 can fix, such as the system-role fallback), no non-finite scores, honesty at least 0.30 in all six languages.
  - Partial (usable as a scale point, with per-language caveats, like Qwen 1.5B and 3B): honesty at least 0.10 in at least 3 languages.
  - Drop: below that (the Qwen 0.5B level), non-finite scores that fp16 cannot avoid, or a compatibility failure E5 cannot fix.
  - Also report 4-option accuracy (flag any language under 0.35), known_in_all_6, the pool size, and how many op_syc cells pass 0.10/0.90.
- Keep several sizes per family where they pass, so scale can be checked within each family under one protocol.
- Done when: the list of model IDs, sizes and quantisation is written here.

### E5 Extend Run 08
- Nov 25: E5 now also covers the protocol corrections in "Decisions (Nov 25)": v2 prompts, the 4-option pool rule, and the open reply-cut decision. Qwen is rerun under the same code.
- Same protocol, or results are not comparable. Edit `notebooks/src/08_unified_scale_run.py`, regenerate with `tools/py2ipynb.py`.
- Already done in E1: image-text loading, a generic layer accessor, the pinned chat date. Still needed: a system-role fallback if a template rejects it, any fp16 fix the screen calls for, and one preset per picked model plus a smoke preset.
- Check that the Qwen path is unchanged (regenerate and run the Qwen smoke preset).
- Done when: a PR is open and merged.

### E10 Corrected protocol (added Nov 26)
- **Status Nov 26:** pool rule and screening report are coded in `notebooks/src/08_unified_scale_run.py` (`POOL_RULE = "strict"`, `POOL_MIN_RUN = 20`, helpers `format_mc4`, `mc4_letter`, `pool_sets`, `guessed_shares`); notebooks 08 and 09 regenerated, `kaggle_09` copy updated. Tested: the pool functions reproduce the Run 10 diagnostic sizes exactly (23/37/89/113 strict, 124/162/216/281 soft), and the probe block was run against a simulated model for strict, soft-small, weak-model skip, screening, cache reuse and stale-pool rebuild. NOT tested on a real model or GPU yet. Screening kernel `arifurrhmn/lostinsteering-run09-screening` pushed as version 2 on Nov 26. **Nov 26 later:** v3 prompt text is in the code (`PROMPT_VERSION = "v3"`, `apply_prompt_version`); v1 reproduces Run 08 text exactly and v3 reproduces `PROMPTS_V3_DRAFT.md` exactly (checked by script); the Qwen 1.5B regression anchor runs on v1; a folder holding results from one prompt version refuses to be resumed under another. Screening kernel version 3 is ready in `notebooks/kaggle_09/` but NOT pushed: the Kaggle CLI login expired (Nov 26), so `kaggle auth login` must be run first. Version 2 (old prompts) is on Kaggle but never ran past the token check. **Still to do for E10:** a smoke run of the 08 notebook on a real GPU, decision D2 (default: keep the 300-character cut) and the numeric threshold decision.
- Behaviour: strict pool, no padding; a model below `POOL_MIN_RUN` is skipped and `diagnostics.json` records `skipped_pool_too_small`; `item_pool_meta.json` records the rule, so an old `item_pool.json` from another rule is rebuilt, not reused; screening keeps the old-rule pool for the baseline and anchor and reports old, soft and strict sizes.
- The v3 prompt text can go into the code as soon as the 300-character opinion cut (D2) is decided; no native-speaker check is needed or available. The pool-rule and screening-report parts are already coded.
- Changes: v2 prompt text; strict pool rule with no padding fallback; the screening notebook reports strict and soft pool sizes and the guessed-share estimate (method in `results/10_diagnostic/`); regenerate notebooks with `tools/py2ipynb.py` and run the smoke preset.

### E11 Qwen rerun (added Nov 26)
- All five Qwen sizes, old results kept untouched as v1. 7B nf4 stays optional (Q1, Q2) unless a quantization claim is wanted. About 30 h of Kaggle time; the Resume gotcha under E7 applies.

### E6 Smoke test
- Run the smoke preset on Kaggle. HF_TOKEN goes in Kaggle Secrets, never in the notebook.

### E7 Full runs
- One Kaggle kernel per model. Resume gotcha: after the 10.3 h mark, optional stages are skipped but `diagnostics.json` is still written. Delete that model's `diagnostics.json` after the resume copy to fill them.
- Download with `kaggle kernels output <user>/<slug> -p results/<folder>`, and download again if the log or rows are missing.
- With about 30 GPU hours a week, the lineup takes about one week. Each model finishes in one session. Start with Llama 3.2-3B and Gemma 4 E4B.

### E8 Verify new results
- Check DONE lines, the stage list, item counts and the 0.10/0.90 opinion floor. Add the folders to the results README and to `paper/scripts/load_run08.py` (the loader stays local).

### E9 Cross-family analysis
- The same tables as for Qwen: truth collapse, transfer, matched effect, cosine, opinion floor. Keep claims within the Run 08 protocol, flag small pools, and keep causal readings apart from what the data shows.

### Q1 Optional: 7B nf4 skipped stages
- About 1.8 h of Kaggle time. Fills capability, matrix, residual and gens for Qwen 7B nf4. Can run in a spare Kaggle slot at any time.

### Q2 Optional: 7B nf4 on the fp16 item pool
- The 7B fp16 and nf4 runs used different item pools (133 and 156 factual eval items), so they are not a clean quantisation comparison. Only needed for a quantisation claim.

### Q3 Optional: larger opinion item pool
- Only needed for stronger opinion claims. It would make the 14B cells less fragile. It changes the protocol, so build it into E5 if wanted and rerun Qwen for comparability.

### H1 README status table
- The README status table still says Run 08 is "written, not yet run". The README is public, so describe the runs, not the paper's findings.
