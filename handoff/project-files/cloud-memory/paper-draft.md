---
name: paper-draft
description: Where the Lost in Steering paper draft, figures and claim table live (first draft 2026-11-21) and what is still open
metadata:
  type: project
  modified: 2026-11-21T05:50:10.260Z
---

First full draft written 2026-11-21 with the paper-writer skill (from paper-writing/paper-writing-kit.zip; the GitHub repo Ariffurrhmn/Paper-Writer needs a login) and humanizer v4.0.0.

Files: /mnt/project-files/paper/ (main.tex, references.bib, figures/, tables/, scripts/make_figures.py + make_tables.py + load_run08.py, CLAIMS_AND_OPEN_ITEMS.md, lost_in_steering_overleaf.zip). Same copy on the user's PC at D:\Cloud Extension\QPAIN\Working paper\LostInSteering\paper\.

Data sources used: 0.5B notebook_3_0.5b; 1.5B/3B run08_notebook_1; 7B fp16+nf4 from 7b_dose_all_langs_recheck (NOT 7b_dose_all_langs, incomplete); 14B run08_notebook_2.

Converted to IEEE conference format (IEEEtran, IEEEtranN bib style, figure* for wide figures, figures rendered at 7.0in / 3.45in) on 2026-11-21 because the user wants IEEE. Title chosen: "Lost in Steering: English Anti-Sycophancy Vectors Suppress Agreement with True Claims Across Six Languages"; persona kept in main text as a null result.

Other model families: only Qwen has steering results. Mistral-7B and Phi-3.5-mini were in the notebook 02 knowledge probe only (no steering); Llama notebooks 05/06 have no results in the repo. The user believes Llama/Gemma were run, so check the local PC if they mention it again.

No LaTeX in the cloud container (tectonic download blocked), so the draft is compiled in Overleaf. Open: 4 [CITE] placeholders, bib written from memory, the 5 team decisions are settled in the IEEE version.

Corrections made while checking: CAA matched retention does not rise in every language (en .60 at 1.5B and 3B; hi .77 at 7B and 14B); 7B transfer ratio is .88-1.31, so English is not "at least as strong" everywhere. See [[run08-results]].
