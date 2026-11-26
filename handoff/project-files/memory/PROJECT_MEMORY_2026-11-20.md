# LostInSteering: Cross-Lingual Sycophancy Steering

Last updated: 2026-11-20

This file records the context and history of the project so a new collaborator or AI session can continue without asking questions.

## Goal and thesis

LostInSteering is a cross-lingual audit of sycophancy steering. The target is a paper for NeurIPS, ACL, or an alignment venue. The question is whether English-derived sycophancy steering vectors (Contrastive Activation Addition, CAA, and persona vectors) protect speakers of other languages or leave them with failure modes.

Current thesis:

- Stance representations transfer across languages with high geometric fidelity. Cosine similarity to the English vector rises with scale.
- Factual CAA anti-steering sharply cuts agreement with true claims in every language. This is called "truth collapse".
- Interpretation, not directly measured: the vector acts like a general contrarian knob rather than an honesty fix. Keep this causal reading separate from what the data shows, which is the drop in true-claim agreement.

## Setup

- Languages (6): English, Spanish, Chinese, Hindi, Bengali, Arabic (en, es, zh, hi, bn, ar).
- Models: Qwen2.5, 0.5B to 14B.
- Compute: Kaggle free 2x T4 tier, with an 11.2h session cutoff.
- Repo: https://github.com/RafiRCh/LostInSteering
- Local folder: D:\Cloud Extension\QPAIN\Working paper\LostInSteering

## Nov 18 audit: three flaws in earlier runs

1. The opinion sycophancy metric was at floor, so earlier opinion transfer claims are withdrawn.
2. Persona vector "retention" reflected an inert vector, not a real fix.
3. Run 04 (7B) and Runs 07a/07b used different protocols, so they cannot be compared directly on scale.

Run 08 was built in response. It uses one unified protocol with forced-choice opinions, logit-margin metrics, a matched-effect persona comparison, and controls. Final CSVs are due Nov 21, 2026, and drafting starts right after.

## Ground rules

- Keep claims matched to the evidence.
- Make no cross-scale claims from runs that used different protocols.
- Do not revive the withdrawn opinion transfer ratios or the old persona "retention" result.
- Run 08 is the source of truth. Report disagreements with earlier runs plainly.
- Flag small samples. Item pools run from 74 to 173, and Bengali is the bottleneck. Avoid overclaiming.
- Null or negative results are valid findings, for example persona vectors also failing.
- Keep causal claims (such as "contrarian knob") separate from what the data directly shows.

## Writing style rule

All prose in the project (paper drafts, docs, briefs, summaries, chat posts) follows the humanizer skill (github.com/blader/humanizer, SKILL.md). Keep every fact, number and claim intact. Accuracy and evidence-matching take priority over style.

## Run 08 status as of Nov 20, 2026

- notebook_1 (1.5B, 3B, 7B fp16, 7B nf4) finished in 10.5h. It needed a second Kaggle session, using the resume dataset lostinsteering-run08-nb1-resume. That session finished 7B fp16 in 206 min and was on 7B nf4 controls at about 10h.
- Output was pulled on Nov 20 to results/08_unified_scale_run/notebook_1_final. The 1.5B and 3B CSVs are in the Nov 19 copy, run08_notebook_1. The 14B CSVs are in run08_notebook_2.
- In 7B nf4, the capability, matrix, residual and gens stages were skipped.
- notebook_2 (14B nf4) finished on Nov 19. Its gens stage was skipped.
- 0.5B is not in any Run 08 preset. Only the reduced "smoke" test covers it.
- Two new private Kaggle notebooks under the lynxsilver account are ready for the user to run. Local copies are in notebooks/kaggle_08x/.

| Notebook | Purpose | Time | Needs |
|---|---|---|---|
| lostinsteering-run08-0-5b | Full 0.5B run | about 1 to 1.5h | No input; HF_TOKEN Kaggle secret |
| lostinsteering-run08-7b-dose-all-langs | Adds zh and ar to the persona vs CAA matched comparison | about 45 to 60 min | The finished run's output as input |

Resume gotcha: the 11.2h clock restarts each session. The controls, capability, matrix, residual and gens stages are core=False and get skipped after 10.3h. The diagnostics.json file is still written, so a plain resume treats the model as complete and will not fill the skipped stages. To fill them, delete that model's diagnostics.json in /kaggle/working after the resume copy.

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

Cosine to the English vector at 7B:

- es and zh: about .93
- ar: .90
- hi: .79 to .84
- bn: .73
- The random control is null.

Opinion sycophancy:

- It fails the 0.10 to 0.90 floor in most cells.
- Cells that pass: 1.5B in all 6 languages; 3B in es, hi and bn; 7B (fp16 and nf4) in hi and bn; 14B in en, es and hi (bn is 0.099 at 14B, just under the floor). Chinese is at floor from 3B up.
- The notebook's own floor check uses 0.03 and flags only values below 0.03 or above 0.97. That does not match the project's 0.10 to 0.90 rule, so do not trust its printed "ok". Recheck baseline.csv op_syc against 0.10 to 0.90.
- The CAA opinion vector is inert. It moves the metric by 0.01 or less.
- Persona anti-steering raises opinion sycophancy in hi, bn and ar.
- The persona_works flag only checks the sign of the sweep, so it should not be cited.

Persona vs CAA at matched effect (run for en, es, hi, bn only):

- In hi and bn, persona is no better than CAA. Retention is about 0.69 to 0.77 at a 50% cut. This is a null result for persona as a fix.
- In en and es, persona cannot reach a 50% cut.

## Caveats

- 7B nf4 and fp16 used different item pools (156 vs 133 factual eval items), so nf4 vs fp16 is not a pure quantization comparison.
- Item pools are small (74 to 173), and Bengali is the bottleneck.
- Opinion results are mostly outside the usable floor range, so they support few claims.

## Recommendation for the paper

Build the paper on truth collapse plus cosine similarity. Limit or drop the opinion claims.

## Open items and next steps

- Final Run 08 CSVs are due Nov 21, 2026. Drafting starts right after.
- The user runs the two new Kaggle notebooks (0.5B full run, and the 7B dose run with zh and ar).
- Skipped stages in 7B nf4 (capability, matrix, residual, gens) and the skipped gens stage in 14B are unfilled. Filling them needs the diagnostics.json deletion described above.
- Recheck all opinion cells against the 0.10 to 0.90 floor before citing them.
- The Kaggle CLI on the user's PC needs a fresh token, because the old one expired in November 2026.

## Security note

A Kaggle API token was exposed in chat and should be rotated. Never write tokens into project files or memory.
