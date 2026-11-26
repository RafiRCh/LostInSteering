# LostInSteering: instructions for Claude Code sessions

This folder holds a cross-lingual audit of sycophancy steering. The question is whether English-derived anti-sycophancy steering vectors (Contrastive Activation Addition, CAA, and persona vectors) protect speakers of other languages or leave them with failure modes. Six languages: en, es, zh, hi, bn, ar. Models: Qwen2.5 0.5B to 14B. Compute: Kaggle free tier, 2x T4. Target venue: NeurIPS, ACL or an alignment venue; the current draft is in IEEE conference format.

The work started in a claude.ai cloud project and moved here on Nov 21, 2026. Read these before doing anything substantial:

1. `PROJECT_MEMORY.md` (root): full context, findings with numbers, caveats and history.
2. `handoff/THREAD_LOG.md`: what each cloud thread did and found.
3. `paper/CLAIMS_AND_OPEN_ITEMS.md`: every claim in the draft mapped to its Run 08 file.

## Ground rules (from the user, always on)

- Keep claims matched to the evidence.
- No cross-scale claims from runs with different protocols. Runs 04, 07a and 07b used different protocols from each other and from Run 08.
- Do not revive the withdrawn opinion transfer ratios or the old persona "retention" result.
- Run 08 is the source of truth. If it disagrees with earlier runs, say so plainly.
- Flag small samples. Item pools run from 74 to 173, and Bengali is the bottleneck.
- Null or negative results are valid findings. Report them honestly (persona is one).
- Keep causal readings (such as "contrarian knob") separate from what the data directly shows.
- Never write a token or credential into any file, memory or commit. Kaggle tokens go in the shell environment only (`KAGGLE_API_TOKEN`) or come from `kaggle auth login`.
- Don't commit or push unless the user asks.

## Writing style

All prose (paper, docs, summaries, chat replies) follows the humanizer skill: https://github.com/blader/humanizer. Keep every fact, number and claim intact; accuracy and the evidence rules beat style. For paper writing use the paper-writer skill, which loads the latest humanizer each time. Both skills are saved in `handoff/skills/` (paper-writer, and humanizer as an offline v4.0.0 copy). They are not installed yet, because the cloud tools could not write to `.claude/`. To install them for this project, run in PowerShell from this folder: `New-Item -ItemType Directory -Force .claude\skills; Copy-Item -Recurse -Force handoff\skills\* .claude\skills\`. The user's own copy of the paper-writer skill lives in the private repo https://github.com/Ariffurrhmn/Paper-Writer.

## Where things are

| What | Path |
|---|---|
| Run 08 notebook and source | `notebooks/08_unified_scale_run.ipynb`, `notebooks/src/08_unified_scale_run.py` (convert with `tools/py2ipynb.py`) |
| Run 08 run guide | `docs/RUN_08.md`, `docs/FRIEND_RUN_GUIDE.md` |
| Extra Kaggle notebooks (0.5B, 7B dose) | `notebooks/kaggle_08x/` |
| Run 08 results | `results/08_unified_scale_run/` (see below) |
| Earlier runs (different protocols) | `results/01_*` to `results/07b_*` |
| Paper (IEEE, final citations) | `paper/main.tex`, `paper/references.bib`, `paper/figures/`, `paper/tables/`, `paper/lost_in_steering_overleaf.zip` |
| Figure and table scripts | `paper/scripts/make_figures.py`, `make_tables.py`, `load_run08.py` |
| Opinion floor fix (not applied) | `handoff/patches/opinion-floor-0.10-0.90.patch` |
| Run 08 results commit (not pushed) | `handoff/git/run08-results.bundle` |
| Snapshot of all cloud project files | `handoff/project-files/` |
| Paper-writing guide and skill kit | `handoff/project-files/paper-writing/` |

Which Run 08 folder to use for each model:

| Model | Folder |
|---|---|
| 0.5B fp16 | `notebook_3_0.5b` |
| 1.5B, 3B fp16 | `run08_notebook_1` |
| 7B fp16 and nf4 | `notebook_1_final` for the full run; `7b_dose_all_langs_recheck` for the 6-language matched-effect data. `run08_notebook_1` holds only a partial 7B. |
| 14B nf4 | `run08_notebook_2` |
| Do not use | `7b_dose_all_langs` (incomplete download, no new rows) |

## Status as of Nov 21, 2026

- Run 08 is complete for Qwen2.5 0.5B, 1.5B, 3B, 7B (fp16 and nf4) and 14B (nf4). 7B nf4 skipped capability, matrix, residual and gens; 14B skipped gens.
- Only Qwen has steering results. Mistral-7B and Phi-3.5-mini appear only in the notebook 02 knowledge probe (no steering). Llama notebooks 05 and 06 exist with no results. Gemma appears nowhere. The user plans to add Llama, Gemma, Mistral and other well-known families. Any new family must run the Run 08 protocol to be comparable.
- Paper draft in IEEE format, title "Lost in Steering: English Anti-Sycophancy Vectors Suppress Agreement with True Claims Across Six Languages". Persona is in the main text as a null result. 14 references, all checked on Nov 21. Not yet compiled after the IEEE switch.
- The existing Run 08 outputs carry the old 0.03/0.97 opinion floor flags. Any opinion cell must be rechecked against 0.10 to 0.90 using `baseline.csv` op_syc before it is cited. The paper already uses the 0.10 rule (20 of 30 cells pass; `paper/tables/opinion_floor_pass.csv`).

## Local git state (checked Nov 21)

- Remotes: `origin` = https://github.com/RafiRCh/LostInSteering, `old-arif` = https://github.com/Ariffurrhmn/LostInSteering.
- Local `main` is at 554ecb0. `origin/main` is at 243d173, two commits ahead (Run 08 Job 1 and Job 2 notes), fetched but not merged. Run `git pull --ff-only` first.
- Many files are untracked: the newer results folders, `paper/`, `notebooks/kaggle_08x/`, `PROJECT_MEMORY.md`, `CLAUDE.md`, `handoff/`.

## Next steps

0. Install the two skills from `handoff/skills/` into `.claude/skills/` (command in "Writing style" above).
1. Revoke the Kaggle token that was pasted in the cloud chat (https://www.kaggle.com/settings/api) and make a new one.
2. Fix GitHub write access for RafiRCh/LostInSteering if pushes are wanted from Claude sessions. Cloud sessions had read-only access.
3. Apply the floor patch: after `git pull --ff-only`, run `git am handoff/patches/opinion-floor-0.10-0.90.patch` (it applies cleanly on 243d173).
4. Push the Run 08 results: `git fetch handoff/git/run08-results.bundle claude/project-thread-p0b29i:run08-results`, then merge or push that branch. The commit adds files that already exist untracked in `results/08_unified_scale_run/`, so git may refuse to overwrite them. They came from this folder, so check they match (`git diff --no-index`) and then let the branch version take their place. Alternatively, recreate the commit locally from the same file list. Decide whether to drop the older `notebook_1/` and `notebook_2/` folders in the repo, which duplicate some results.
5. Recheck all Run 08 opinion cells at 0.10/0.90 (the paper did this; the notebook flags did not).
6. Decide on access to the private Paper-Writer repo (make it public or give sessions a way to read it).
7. Compile the IEEE draft: upload `paper/lost_in_steering_overleaf.zip` to Overleaf (IEEEtran conference, pdfLaTeX + BibTeX). There is no local LaTeX check yet. Then review the figures in the compiled PDF.
8. Paper items still open: native-speaker check of the factual templates and opinion translations; switch Persona Vectors to its NeurIPS 2026 proceedings entry once published; the two 2026 arXiv sycophancy preprints may have newer versions.
9. Update the repo README status table, which still says Run 08 is "written, not yet run".
10. Planned: more model families (Llama, Gemma, Mistral and others) under the Run 08 protocol. Llama or another family needs code changes plus about 7.5 to 8h of Kaggle time per 7B-class model. Optional: 7B nf4 rerun on the fp16 item pool (only for a quantization claim), a larger opinion item pool (only for opinion claims), and filling the skipped 7B nf4 stages (about 1.8h; delete that model's diagnostics.json after the resume copy).

## Kaggle notes

- Account: lynxsilver. Kaggle is blocked from Claude's cloud machines, so all Kaggle work runs on this PC.
- Kernels: `lynxsilver/lostinsteering` (Run 08 notebook_1), `lynxsilver/lostinsteering-run08-0-5b`, `lynxsilver/lostinsteering-run08-7b-dose-all-langs`. Resume dataset: `lostinsteering-run08-nb1-resume`.
- Download: `kaggle kernels output <user>/<slug> -p results/<folder>`. If the first download is missing the log or new rows, download again (this happened with the 7B dose run).
- Resume gotcha: the 11.2h hard stop restarts each session. Optional stages are skipped after 10.3h, but diagnostics.json is still written, so a plain resume treats the model as done. Delete that model's diagnostics.json after the resume copy to fill skipped stages.
- HF_TOKEN goes in Kaggle Add-ons > Secrets, never in a notebook.
