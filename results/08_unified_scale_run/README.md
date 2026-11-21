# Run 08 results

Each folder is one Kaggle job's output, kept under the name it was downloaded with. Caches (`_cache/`) and `vectors.pt` files are not in git.

| Model | Folder |
|---|---|
| Qwen2.5-0.5B fp16 | `notebook_3_0.5b/run08_notebook_3/` |
| Qwen2.5-1.5B fp16, 3B fp16 | `run08_notebook_1/` |
| Qwen2.5-7B fp16 and nf4 | `notebook_1_final/run08_notebook_1/` (full run) |
| Qwen2.5-7B fp16, matched effect and dose for all six languages | `7b_dose_all_langs_recheck/run08_notebook_1/Qwen2.5-7B-Instruct-fp16/` |
| Qwen2.5-14B nf4 | `run08_notebook_2/` |

Notes:

- `run08_notebook_1/NOTES.md` and `run08_notebook_2/NOTES.md` are the job notes. The notebook_1 notes were written before 7B finished, and both were written before the opinion floor moved to 0.10/0.90, so `PROJECT_MEMORY.md` and the paper take precedence where they disagree.
- `notebook-1.log` and `notebook-2.log` are the Kaggle logs for jobs 1 and 2.
- `7b_dose_all_langs_recheck` keeps only what that run changed: the 7B fp16 `matched_effect.csv`, `dose_response.csv`/`.png` and `diagnostics.json` (which add zh and ar to the matched-effect comparison), plus `run_summary.json` and the log. For 7B fp16, read those files from here and everything else from `notebook_1_final`. The run's other outputs were identical to `notebook_1_final` and were removed. That includes its nf4 `matched_effect.csv`, whose completion was unconfirmed (no nf4 DONE line in the log).
- 7B nf4 skipped capability, matrix, residual and gens. 14B skipped gens. The 7B fp16 and nf4 runs used different item pools (133 and 156 factual eval items).
- The `opinion_floor_or_ceiling` flags in every `diagnostics.json` use the old 0.03/0.97 rule. Recheck opinion cells against 0.10/0.90 using `baseline.csv` `op_syc` before you cite them.

Removed in this layout: the older `notebook_1/` and `notebook_2/` folders, which were the same files as `run08_notebook_1/` and `run08_notebook_2/` apart from line endings (their logs are `notebook-1.log` and `notebook-2.log`), and the partial 7B fp16 in `run08_notebook_1/`, which `notebook_1_final` replaces. The partial 7B is still in git history at commit afe9140 under `notebook_1/Qwen2.5-7B-Instruct-fp16/`.
