# LostInSteering

**Do English sycophancy steering vectors work in other languages?**

AI models tend to agree with users even when the user is wrong (*sycophancy*). Researchers can reduce this with
*activation steering*: a direction inside the model ("vector") that is added while it answers. These vectors are
almost always built and tested in English. This project measures how much of that effect carries over to
Spanish, Chinese, Hindi, Bengali and Arabic, and where it breaks.

**Main contribution (one sentence):** a safety fix made in English may not protect users of other languages,
and we measure how much protection is lost, per language, per kind of sycophancy, and per layer, using a vector
built in each language as the fair comparison.

## Status

| Step | Notebook | Status | Results |
|---|---|---|---|
| 1. Smoke test v1 | `notebooks/01_smoke_test_v1.ipynb` | Done (2026-11-14). Verdict: **NOT YET** | [`results/01_smoke_test_v1/`](results/01_smoke_test_v1/NOTES.md) |
| 2. Knowledge probe (3 models) | `notebooks/02_knowledge_probe.ipynb` | Done (2026-11-14). Verdict: **Qwen2.5-7B chosen (74 known items)** | [`results/02_knowledge_probe/`](results/02_knowledge_probe/NOTES.md) |
| 3. Steering v2 | `notebooks/03_steering_v2.ipynb` | Done (2026-11-15). Verdict: **NOT YET**. Agree direction transfers to all 6 languages, but it is not honesty-specific | [`results/03_steering_v2/`](results/03_steering_v2/NOTES.md) |
| 3b. Steering v2, debiased vector | `notebooks/03b_steering_v2_debiased.ipynb` | Done (2026-11-15). Verdict: **NOT YET**. No effect at chosen layer 13; negative effect at layers 16 to 17 | [`results/03b_steering_v2_debiased/`](results/03b_steering_v2_debiased/NOTES.md) |
| 3c. Steering v2, debiased flip | `notebooks/03c_steering_v2_debiased_flip.ipynb` | Done (2026-11-16). Verdict: **NOT YET**. Strong transfer (ratio ~1.0) at layer 17, but acts as contrarian/agreement knob rather than honesty dial | [`results/03c_steering_v2_debiased_flip/`](results/03c_steering_v2_debiased_flip/NOTES.md) |
| 4. Complete Paper Run (All-in-One) | `notebooks/04_complete_paper_run.ipynb` | Done (2026-11-16). **All experiments complete**. Replicated CAA truth collapse across 6 languages (-17% to -35%); Persona vectors retain 85–97% factual truth | [`results/04_complete_paper_run/`](results/04_complete_paper_run/NOTES.md) |
| 4b. Opinion Sycophancy (Modular) | `notebooks/04_opinion_sycophancy.ipynb` | Standalone opinion sycophancy run (Shah et al., 2026) | `results/04_opinion_sycophancy/` |
| 5. Cross-Model Audit (Optional) | `notebooks/05_cross_model_audit.ipynb` | Standalone Llama-3.1-8B replication of factual steering | `results/05_cross_model_audit/` |
| 6. Llama Full Replication | `notebooks/06_llama_full_replication.ipynb` | Standalone full Llama replication | `results/06_llama_full_replication/` |
| 7a. Qwen Scale Sweep (0.5B, 1.5B, 3B) | `notebooks/07a_qwen_scale_sweep_Arif.ipynb` | Running on Kaggle (`lostinsteering-7a`) | Pending completion |
| 7b. Qwen Scale Audit (14B) | `notebooks/07b_qwen_14b_Rafi.ipynb` | Failed (2026-11-16). CUDA OOM on single T4 | [`results/07b_qwen_14b_Rafi/`](results/07b_qwen_14b_Rafi/NOTES.md) |

The full plan and what to do next is in [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Repository layout

```
LostInSteering/
├── README.md               this file
├── docs/
│   ├── ROADMAP.md          next steps, how to run v2, open decisions
│   └── proposal/           research proposal (PDF)
├── notebooks/              Kaggle notebooks, numbered in the order they are run
├── results/                one folder per notebook run, same number as the notebook
│   └── 01_smoke_test_v1/   CSVs, charts, Kaggle log, NOTES.md (what the results mean)
└── vault/                  Obsidian notes: backlog of parked ideas
```

## How we run things

Everything runs on **Kaggle** (free GPU, 2× T4). Nothing needs to run locally.

1. Kaggle → *Create → New Notebook → File → Import Notebook* → pick a notebook from `notebooks/`.
2. Settings: **Accelerator: GPU T4 x2**, **Internet: On** (phone-verified account needed).
3. Run with **Save Version → Save & Run All (Commit)**. You can close the tab; it runs in the background.
4. When it finishes, download the outputs into the matching `results/` folder:
   ```bash
   kaggle kernels output <kaggle-username>/<notebook-slug> -p results/<NN_name>/
   ```
   (The CLI only sees *committed* runs. Interactive runs must be downloaded from the notebook's Output panel.)
5. Add a short `NOTES.md` in that results folder: what ran, the verdict, what surprised you.

No Hugging Face token is needed for the default (Qwen, Mistral, Phi) models. For gated models (Llama, Aya),
add a Kaggle secret named `HF_TOKEN`; the notebooks pick it up automatically.

## Working together

- **Pull before you start, push when you finish** (`git pull`, then commit and `git push`).
- One person edits a notebook at a time. To try a variation, copy it to a new number (e.g. `03b_...`) instead of
  editing someone else's working version.
- Never overwrite a results folder. A re-run goes in a new folder (`01_smoke_test_v1_rerun/`).
- Never commit `kaggle.json`, HF tokens, or model weights (`.gitignore` blocks the common ones).
- Parked ideas go in `vault/00 - Backlog.md`; decisions and next steps in `docs/ROADMAP.md`.
