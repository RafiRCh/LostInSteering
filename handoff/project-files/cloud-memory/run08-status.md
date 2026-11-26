---
name: run08-status
description: Run 08 Kaggle job status, resume mechanics, and floor-check threshold mismatch (as of 2026-11-20)
metadata:
  type: project
  modified: 2026-11-20T15:59:44.715Z
---

Run 08 has only two presets that matter: notebook_1 (1.5B, 3B, 7B fp16, 7B nf4) and notebook_2 (14B nf4). notebook_2 finished 2026-11-19 (GENS skipped). notebook_1 needed a second Kaggle session (resume dataset lostinsteering-run08-nb1-resume); that session finished 7B fp16 (206 min) and was on 7B nf4 CONTROLS at ~10h on 2026-11-20. 0.5B is NOT in any Run 08 preset (only the reduced "smoke" test).

Resume gotcha: the 11.2h clock restarts each session. Stages CONTROLS/CAPABILITY/MATRIX/RESIDUAL/GENS are core=False and get SKIPPED after 10.3h, but diagnostics.json is still written, so a plain resume treats the model as complete and will not fill the skipped stages. To fill them, delete that model's diagnostics.json in /kaggle/working after the resume copy.

Floor check mismatch: code flags opinion only when op_syc < 0.03 or > 0.97, not the project's 0.10-0.90 rule. At 7B (fp16 and nf4) only hi and bn pass 0.10-0.90; en, es, ar, zh fail.

**Why:** deadline for final CSVs is 2026-11-21; these facts decide what is left to run.
**How to apply:** don't trust the printed "ok" on FLOOR CHECK lines; recheck baseline.csv op_syc against 0.10-0.90. See [[run08-results]].
