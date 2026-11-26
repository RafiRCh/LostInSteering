---
name: run08-results
description: Run 08 headline numbers and where each result file lives (as of 2026-11-20 pull)
metadata:
  type: project
  modified: 2026-11-20T17:13:32.990Z
---

Final notebook_1 output pulled 2026-11-20 to results/08_unified_scale_run/notebook_1_final on the user's PC (D:\...\LostInSteering). 7B nf4 finished (10.51h session) but CAPABILITY, MATRIX-SIBLING, RESIDUAL, GENS were skipped. 1.5B/3B CSVs are in the Nov 19 copy run08_notebook_1; 14B in run08_notebook_2. 7B nf4 and fp16 used different item pools (156 vs 133 factual eval items), so nf4 vs fp16 is not a pure quantization comparison.

Opinion floor (0.10-0.90 rule), baseline op_syc passes: 1.5B all 6; 3B es/hi/bn; 7B fp16 and nf4 hi/bn only; 14B en/es/hi (bn 0.099). zh at floor from 3B up.
Truth collapse replicates at 7B (true_drop nf4/fp16: en 43/42%, es 31/38, zh 64/66, hi 66/66, bn 84/81, ar 53/57).
Opinion: CAA opinion vector changes op_syc by <=0.01; persona anti-steer raises op_syc in hi/bn/ar. diagnostics persona_works=True only checks the sweep sign; don't cite it.
Matched effect (en/es/hi/bn only): persona retention equals CAA in hi/bn (~0.69-0.77 at 50% cut); persona can't reach 50% in en/es. Null result for persona as a fix.

Kaggle CLI on the user's PC needs a fresh token (old one expired 2026-11). Never store the token in memory. See [[run08-status]].
