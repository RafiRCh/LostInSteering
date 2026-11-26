# LostInSteering: instructions for Claude Code sessions

This folder holds a cross-lingual audit of sycophancy steering. The question is whether English-derived anti-sycophancy steering vectors (Contrastive Activation Addition, CAA, and persona vectors) protect speakers of other languages or leave them with failure modes. Six languages: en, es, zh, hi, bn, ar. Models: Qwen2.5 0.5B to 14B. Compute: Kaggle free tier, 2x T4. Target venue: NeurIPS, ACL or an alignment venue; the current draft is in IEEE conference format.

The work started in a claude.ai cloud project and moved here on Nov 21, 2026. Read these before doing anything substantial:

0. `handoff/PLAN.md`: the shared task list (what is done, what is next, who does it).
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
- The paper stays private (decided Nov 21). Never commit or push `paper/` or paper findings to the repo, which is public. `paper/` and `_cache/` are in `.git/info/exclude`.
- Experiments first (decided Nov 21). Paper work is paused until the new Kaggle runs are done. No native-speaker check is available; the paper will state that as a limitation.

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
| Opinion floor fix | merged to main (1c72467); patch kept at `handoff/patches/` |
| Run 08 results commit | merged to main (691bef7); bundle kept at `handoff/git/` |
| Shared task list and model candidates | `handoff/PLAN.md` (PDF: `handoff/PLAN.pdf`) |
| Snapshot of all cloud project files | `handoff/project-files/` |
| Paper-writing guide and skill kit | `handoff/project-files/paper-writing/` |

Which Run 08 folder to use for each model:

| Model | Folder |
|---|---|
| 0.5B fp16 | `notebook_3_0.5b` |
| 1.5B, 3B fp16 | `run08_notebook_1` |
| 7B fp16 and nf4 | `notebook_1_final` for the full run; `7b_dose_all_langs_recheck` for the 7B fp16 `matched_effect.csv`, `dose_response.csv` and `diagnostics.json` (6-language matched effect). In git, the recheck folder holds only those files; the local copy is fuller. |
| 14B nf4 | `run08_notebook_2` |
| Do not use | `7b_dose_all_langs` (incomplete download, no new rows) |

## Status as of Nov 21, 2026

- Run 08 is complete for Qwen2.5 0.5B, 1.5B, 3B, 7B (fp16 and nf4) and 14B (nf4). 7B nf4 skipped capability, matrix, residual and gens; 14B skipped gens.
- Only Qwen has steering results. Mistral-7B and Phi-3.5-mini appear only in the notebook 02 knowledge probe (no steering). Llama notebooks 05 and 06 exist with no results. Gemma appears nowhere. The user plans to add Llama, Gemma, Mistral and other well-known families. Any new family must run the Run 08 protocol to be comparable.
- Paper draft in IEEE format, title "Lost in Steering: English Anti-Sycophancy Vectors Suppress Agreement with True Claims Across Six Languages". Persona is in the main text as a null result. 14 references, all checked on Nov 21. Not yet compiled after the IEEE switch.
- The existing Run 08 outputs carry the old 0.03/0.97 opinion floor flags. Any opinion cell must be rechecked against 0.10 to 0.90 using `baseline.csv` op_syc before it is cited. The paper already uses the 0.10 rule (20 of 30 cells pass; `paper/tables/opinion_floor_pass.csv`).

## Local git state (updated Nov 21, after the merges)

- Remotes: `origin` = https://github.com/RafiRCh/LostInSteering (public), `old-arif` = https://github.com/Ariffurrhmn/LostInSteering. The local `gh` login (Ariffurrhmn) has push access to origin.
- `main` = `origin/main` = 691bef7. PR 1 (floor fix, 1c72467) and PR 2 (Run 08 results, 691bef7) are merged. The results folder layout is described in `results/08_unified_scale_run/README.md`.
- Still untracked on purpose: `paper/` (private), `handoff/`, `PROJECT_MEMORY.md`, `CLAUDE.md`, `.claude/`, `notebooks/kaggle_08x/`, `tools/build_*`, and local-only duplicates in `results/08_unified_scale_run/7b_dose_all_langs*` that hold caches. Never delete whole results folders: `_cache/` and `vectors.pt` live there and are not in git.

## Next steps

**All work is paused (Nov 21) until the supervisor approves a proposal; do not start Kaggle runs or plan tasks without the user's go-ahead.** The current task list is `handoff/PLAN.md` (tasks T1 to T24 with owners, dependencies and suggested models). It replaces the numbered list below, which is kept for history. Before substantial work, read PLAN.md, check that the task's "Needs" are done, and mark it `doing (claude)`. When finished, mark it `done` with the PR or commit and rebuild the PDF with `python tools/build_plan_pdf.py`.

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

- Accounts: lynxsilver (Run 08 kernels) and arifurrhmn (the CLI login on this PC since Nov 21; Run 09 screening kernel `arifurrhmn/lostinsteering-run09-screening`, folder `notebooks/kaggle_09/`). Kaggle is blocked from Claude's cloud machines, so all Kaggle work runs on this PC.
- Kernels: `lynxsilver/lostinsteering` (Run 08 notebook_1), `lynxsilver/lostinsteering-run08-0-5b`, `lynxsilver/lostinsteering-run08-7b-dose-all-langs`. Resume dataset: `lostinsteering-run08-nb1-resume`.
- Download: `kaggle kernels output <user>/<slug> -p results/<folder>`. If the first download is missing the log or new rows, download again (this happened with the 7B dose run).
- Resume gotcha: the 11.2h hard stop restarts each session. Optional stages are skipped after 10.3h, but diagnostics.json is still written, so a plain resume treats the model as done. Delete that model's diagnostics.json after the resume copy to fill skipped stages.
- HF_TOKEN goes in Kaggle Add-ons > Secrets, never in a notebook.
