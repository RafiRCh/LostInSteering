# Run 11 notebooks: how to run

Four Kaggle notebooks, one per folder. Each loads the same Run 08 protocol (v3 prompts, strict item pool).

| Folder | What it runs | Time | Needs HF token? |
|---|---|---|---|
| `lostinsteering-run11-smoke-v2` | Smoke test: Qwen 0.5B (should skip) and Gemma 4 E4B (must finish every stage) | about 1 h | Optional |
| `llama-8b-needs-hf-secret` | Llama 3.1 8B Instruct, fp16 | about 8 h | **Yes**, plus the licence accepted on Hugging Face |
| `lostinsteering-run11-gemma-e4b` | Gemma 4 E4B, fp16 | several hours | Optional |
| `lostinsteering-run11-gemma-12b` | Gemma 4 12B, nf4 | about 10 h | Optional |

## Steps (same for each)
1. On Kaggle: New Notebook > File > Import Notebook, upload the `.ipynb` from the folder.
2. Settings: Accelerator **GPU T4 x2**, Internet **on**.
3. Add-ons > Secrets: add a secret named `HF_TOKEN` with your own Hugging Face token (read access), and **attach it to the notebook** (tick the box). Never paste the token into a cell.
4. For Llama: accept the licence at https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct with the same Hugging Face account first.
5. Save Version > Save & Run All. Do not run two or more GPU notebooks past your account limit (2 at once).
6. When it finishes, download the output (`run08_*` folder) and send it back. If the session stops at its time budget, attach that output to a new run of the same notebook to resume.

If `HF_TOKEN` is not attached, the gated Llama notebook stops at its token check, and the others download anonymously (slower).
