# LostInSteering: Cross-Lingual Sycophancy Steering

Last updated: 2026-11-21 (handoff from the claude.ai cloud project to local Claude Code sessions)

This file records the context and history of the project so a new collaborator or AI session can continue without asking questions. Session instructions are in `CLAUDE.md`. A per-thread record of the cloud work is in `handoff/THREAD_LOG.md`. The previous version of this file (Nov 20) is kept at `handoff/project-files/memory/PROJECT_MEMORY_2026-11-20.md`.

## Goal and thesis

LostInSteering is a cross-lingual audit of sycophancy steering. The target is a paper for NeurIPS, ACL, or an alignment venue; the current draft is in IEEE conference format. The question is whether English-derived sycophancy steering vectors (Contrastive Activation Addition, CAA, and persona vectors) protect speakers of other languages or leave them with failure modes.

Current thesis:

- Stance representations transfer across languages with high geometric fidelity. Cosine similarity to the English vector rises with scale.
- Factual CAA anti-steering sharply cuts agreement with true claims in every language. This is called "truth collapse".
- Interpretation, not directly measured: the vector acts like a general contrarian knob rather than an honesty fix. Keep this causal reading separate from what the data shows, which is the drop in true-claim agreement.

## Setup

- Languages (6): English, Spanish, Chinese, Hindi, Bengali, Arabic (en, es, zh, hi, bn, ar).
- Models: Qwen2.5, 0.5B to 14B. Only Qwen has steering results.
- Compute: Kaggle free 2x T4 tier, with an 11.2h session cutoff. Kaggle account: lynxsilver.
- Repo: https://github.com/RafiRCh/LostInSteering (remote `origin`). Older fork: https://github.com/Ariffurrhmn/LostInSteering (remote `old-arif`).
- Local folder: D:\Cloud Extension\QPAIN\Working paper\LostInSteering (PC "Arifs").

## Nov 18 audit: three flaws in earlier runs

1. The opinion sycophancy metric was at floor, so earlier opinion transfer claims are withdrawn.
2. Persona vector "retention" reflected an inert vector, not a real fix.
3. Run 04 (7B) and Runs 07a/07b used different protocols, so they cannot be compared directly on scale.

Run 08 was built in response. It uses one unified protocol with forced-choice opinions, logit-margin metrics, a matched-effect persona comparison, and controls.

## Ground rules

- Keep claims matched to the evidence.
- Make no cross-scale claims from runs that used different protocols.
- Do not revive the withdrawn opinion transfer ratios or the old persona "retention" result.
- Run 08 is the source of truth. Report disagreements with earlier runs plainly.
- Flag small samples. Item pools run from 74 to 173, and Bengali is the bottleneck. Avoid overclaiming.
- Null or negative results are valid findings, for example persona vectors also failing.
- Keep causal claims (such as "contrarian knob") separate from what the data directly shows.

## Writing style rule

All prose in the project (paper drafts, docs, briefs, summaries, chat posts) follows the humanizer skill (github.com/blader/humanizer, SKILL.md). Keep every fact, number and claim intact. Accuracy and evidence-matching take priority over style. Papers are written with the user's paper-writer skill (private repo github.com/Ariffurrhmn/Paper-Writer; a copy is in `handoff/skills/paper-writer` (copy it to `.claude/skills/` to install it) and in `handoff/project-files/paper-writing/paper-writing-kit.zip`).

## Run 08 status: complete (Nov 21, 2026)

| Model | Result folder under results/08_unified_scale_run/ | Notes |
|---|---|---|
| 0.5B fp16 | notebook_3_0.5b | Kernel lostinsteering-run08-0-5b. DONE in 60.7 min, all 11 stages. Persona split-half cosine 0.17, so the 0.5B persona result is weak. Opinion transfer native-valid for en, es, bn only. |
| 1.5B, 3B fp16 | run08_notebook_1 | Nov 19 copy of notebook_1. |
| 7B fp16 | notebook_1_final | All stages. run08_notebook_1 holds only a partial 7B. |
| 7B nf4 | notebook_1_final | Capability, matrix, residual and gens skipped at the 10.3h budget. Different item pool from fp16 (156 vs 133 factual eval items). |
| 7B dose, 6 languages | 7b_dose_all_langs_recheck | Kernel lostinsteering-run08-7b-dose-all-langs. Adds zh and ar to the matched-effect comparison. DONE for fp16 in 19.2 min. nf4 has a matched_effect.csv but no DONE line in the log, so unconfirmed. |
| 14B nf4 | run08_notebook_2 | Finished Nov 19. Gens skipped. |
| (do not use) | 7b_dose_all_langs | First download was incomplete: no log, no new rows. |

Resume gotcha: the 11.2h clock restarts each session. The controls, capability, matrix, residual and gens stages are core=False and get skipped after 10.3h. diagnostics.json is still written, so a plain resume treats the model as complete. To fill skipped stages, delete that model's diagnostics.json in /kaggle/working after the resume copy.

Floor check: the notebook flags opinion only below 0.03 or above 0.97, which does not match the project's 0.10 to 0.90 rule. All existing Run 08 outputs carry the old flags. A patch that makes it 0.10/0.90 and configurable is in `handoff/patches/opinion-floor-0.10-0.90.patch` (not yet applied or pushed).

## Key findings from Run 08

Truth collapse replicates at 7B in all 6 languages. Drop in true-claim agreement:

| Language | nf4 | fp16 |
|---|---|---|
| en | 43% | 42% |
| es | 31% | 38% |
| zh | 64% | 66% |
| hi | 66% | 66% |
| bn | 84% | 81% |
| ar | 53% | 57% |

From the paper's claim table (`paper/CLAIMS_AND_OPEN_ITEMS.md`):

- At 7B fp16, subtracting the English CAA vector (alpha 8) lowers agreement with false claims to 3 to 16%, and lowers agreement with true claims by 42/38/66/66/81/57 points (en/es/zh/hi/bn/ar). The smallest bootstrap CI lower bound is 32 points. 133 eval items.
- The honesty gap shrinks (en -0.18, zh -0.45, bn -0.33).
- Collapse at 3B is 53 to 85 points and at 14B 32 to 79 points. 1.5B rejects nearly everything. 0.5B barely steers and has no honesty gap. No cross-size comparison at fixed alpha.
- No dose gives falling false-claim agreement with flat true-claim agreement (7B dose_response, 100 items, no CIs).
- MMLU change under CAA at 7B is -5.3 to -0.7 points; random vector -0.7 to +2.0; 14B worst is -11 (bn). 150 items (100 at 14B).
- CAA retention at a 50% cut: 1.5B .51 to .62, 3B .56 to .67, 7B .68 to .83, 14B en .90 and hi .77. Interpolated, no CIs. Retention does not rise with size in every language (en .60 at 1.5B and 3B; hi .77 at 7B and 14B).
- Cosine to English at 7B: es .94, zh .94, ar .90, hi .84, bn .73. Mean rises from .43 (0.5B) to .92 (14B); 14B is nf4 with a smaller pool. Random control is null.
- Factual transfer ratio at 7B is .88 to 1.31; other sizes .94 to 1.63. Random slope within 0.04 of zero at 7B. Opinion ratios stay withdrawn.

Opinion sycophancy:

- Under the 0.10 to 0.90 rule, 20 of 30 cells pass: 1.5B all 6 languages; 3B es, hi, bn; 7B (fp16 and nf4) hi and bn; 14B en, es, hi (bn is 0.099, just under). zh is at floor from 3B up. See `paper/tables/opinion_floor_pass.csv`.
- The CAA opinion vector is inert: in passing cells at 3B and up it changes op_syc by 0.03 or less (0.01 or less at 7B).
- Persona anti-steering raises opinion sycophancy in 7 of 8 passing cells at 3B and up (at 7B: hi, bn and ar).
- The persona_works flag only checks the sign of the sweep, so it should not be cited.

Persona vs CAA at matched effect:

- Persona minus CAA retention is -0.04 to +0.02 in the 13 cells where both reach the target. Null result for persona as a fix.
- At 7B persona never reaches the 50% target in en, es, zh or ar (23 to 30% cut at alpha 24).
- 7B zh and ar (from the recheck run): CAA reaches 0.5 in zh (retention 0.681) and ar (0.747); at 0.8 only ar CAA reaches it (retention 0.492). Persona reaches neither target in zh or ar.

## Caveats

- 7B nf4 and fp16 used different item pools, so nf4 vs fp16 is not a pure quantization comparison. Make no quantization claim.
- Item pools are small (74 to 173), and Bengali is the bottleneck.
- Opinion results are mostly outside the usable floor range, so they support few claims.
- The 0.5B persona vector is weak (split-half cosine 0.17).

## Other model families

Only Qwen2.5 has steering results. Mistral-7B and Phi-3.5-mini appear only in the notebook 02 knowledge probe (no steering, different protocol; Mistral was at chance in hi and bn, which is why Qwen was chosen). Llama notebooks 05 and 06 exist but have no results anywhere in the repo or the local results folder. Gemma appears nowhere. The user remembers running Llama and Gemma; no files support that so far. The user plans to add Llama, Gemma, Mistral and other well-known families, which need the Run 08 protocol to be comparable (code changes plus about 7.5 to 8h of Kaggle per 7B-class model).

## Paper (Nov 21, 2026)

- Location: `paper/` (main.tex, references.bib, figures/, tables/, scripts/, CLAIMS_AND_OPEN_ITEMS.md, lost_in_steering_overleaf.zip).
- Format: IEEE conference (IEEEtran, IEEEtranN bib style, figure* for wide figures, figures at 7.0in and 3.45in).
- Title: "Lost in Steering: English Anti-Sycophancy Vectors Suppress Agreement with True Claims Across Six Languages". The user says this can still change.
- Settled decisions: factual truth collapse leads; the opinion floor check stays in the main text as a short section; persona is in the main text as a null result next to CAA; the paper is Qwen-only with other families as planned work; run allocation is listed as future work.
- References: 14 entries, all four former [CITE] gaps filled, all checked on Nov 21 against ACL Anthology, conference pages and arXiv. Persona Vectors is cited as arXiv; switch to NeurIPS 2026 proceedings when out. Yong et al. is a NeurIPS 2023 SoLaR workshop paper.
- Data sources used: 0.5B notebook_3_0.5b; 1.5B and 3B run08_notebook_1; 7B fp16 and nf4 from 7b_dose_all_langs_recheck; 14B run08_notebook_2.
- Not done: compiling the IEEE version (no LaTeX was available in the cloud; use Overleaf), native-speaker check of templates and translations.
- The user compiled the earlier non-IEEE draft and did not like it; that is why it was converted.

## Open items and next steps

1. Revoke the Kaggle token that was pasted in cloud chat and make a new one.
2. Get GitHub write access for Claude sessions on RafiRCh/LostInSteering if wanted (cloud access was read-only).
3. Apply `handoff/patches/opinion-floor-0.10-0.90.patch` (after `git pull --ff-only`; local main is two commits behind origin/main).
4. Push the Run 08 results commit in `handoff/git/run08-results.bundle` (branch claude/project-thread-p0b29i, tip 4aabd39, parent 243d173). 201 files, CSV/JSON/log/PNG only.
5. Recheck all Run 08 opinion cells at 0.10/0.90 before citing them.
6. Decide on access to the private Paper-Writer repo.
7. Compile on Overleaf and review figures.
8. Update the repo README status table for Run 08.
9. Add more model families under the Run 08 protocol.

## Security note

A Kaggle API token was exposed in cloud chat and should be revoked. Never write tokens into project files, memory or commits. Use `kaggle auth login` or a shell-only `KAGGLE_API_TOKEN`.
