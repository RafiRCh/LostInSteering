# Run 08 guide: unified corrected protocol

Notebook: `notebooks/08_unified_scale_run.ipynb` (generated from `notebooks/src/08_unified_scale_run.py` by `python tools/py2ipynb.py <src.py> <out.ipynb>`; edit the .py, regenerate the notebook).

**Status: written and statically checked only (it parses and has no undefined names). It has NOT been run on a GPU, so expect to fix small first-run bugs. No smoke test is planned; the first stages of a real run (knowledge probe, then baseline with `FLOOR CHECK` lines) act as the early check.**

## Run order

| Preset | Models | Rough time (2x T4) |
|---|---|---|
| **`notebook_1`** (hand out) | 1.5B, 3B, 7B fp16, 7B NF4 | 7-10 h, may need one resume |
| **`notebook_2`** (hand out) | 14B NF4 | 9-11 h |
| `small` | 1.5B, 3B (fp16) | 2-4 h |
| `7b` | 7B fp16 and 7B NF4 (quantisation control) | 3-5 h |
| `14b` | 14B NF4 | 9-11 h (estimate; stops cleanly at 11.2 h) |

The three presets are independent, so run them at the same time on different Kaggle accounts. Set `PRESET` at the top of the "Setup" cell. Each run writes `run08_<preset>/<model>-<quant>/`.

## Checkpointing and resuming

- Every single evaluation (one language, one steering setting, one item set) is saved to `<model>/_cache/` the moment it finishes, as are the knowledge-probe result for each language, each vector-extraction pass and each persona pair. Stage CSVs are written when a stage ends.
- If a run crashes or stops at the time limit, add its output as an input dataset to a new run of the same preset. The notebook finds it under `/kaggle/input`, copies the cache over and recomputes only what is missing. A model whose `diagnostics.json` exists is skipped without loading.
- At 11.2 h the notebook stops cleanly (finishing the current evaluation) so Kaggle saves the output. A run that Kaggle kills at 12 h may not save its output, which is why the clean stop exists. Do not rely on being killed.
- The cache is keyed on the exact settings, so changing a setting (multipliers, pool size) recomputes only the affected pieces; changing the model or quantisation uses a different folder.

## What to look at in the first hour

1. `FLOOR CHECK` lines (printed after the baseline stage, right after the knowledge probe): `op_syc` (opinion sycophancy baseline) should be well away from 0 and 1. If it is still below 0.03 or above 0.97 for most languages, the opinion task still needs a redesign (the margin-based slopes still work, but the headline rates will not). If so, stop the run and tell me: the cache (probe, baseline) is kept, so a fixed notebook resumes without losing that work.
2. `layers:` line: persona `steer_persona_raw` should be negative. If not, persona steering does not work in that model and the paper should say so.
3. `diagnostics.json`, `transfer_*.csv` (`native_valid` column), `matched_effect.csv`.

## Outputs per model (in `<model>-<quant>/`)

`baseline.csv`, `caa_collapse.csv`, `transfer_factual.csv`, `transfer_opinion.csv`, `opinion_headline.csv`, `dose_response.csv` + `.png`, `matched_effect.csv`, `controls.csv`, `capability_mmlu.csv`, `transfer_matrix_sibling.csv`, `residual_decomposition.csv`, `generations.csv`, `layer_sweep.csv` + `.png`, `cosine_*.csv`, `probe_accuracy.csv`, `item_pool.json`, `vectors.pt`, `diagnostics.json`.

## Known limits (state these in the paper)

- Qwen2.5 family only; translations of the opinion items are from Shah et al. and not native-speaker checked.
- 14B is NF4; the 7B NF4 run measures how much quantisation alone changes the results.
- Opinion replies are cut to about 300 characters.
- The persona vector is built from 6 English system-prompt pairs; the matched-effect comparison is interpolated from a small dose grid with no confidence intervals.
- Cross-task controls apply the sign found on the other task's layer.
