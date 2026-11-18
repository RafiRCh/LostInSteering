# How to run notebook 08 on Kaggle (step by step)

You will run `notebooks/08_unified_scale_run.ipynb` on free Kaggle GPUs and send the results back. There are two runs: **`notebook_1`** (models 1.5B, 3B, 7B; roughly 7-10 hours, may need one resume) and **`notebook_2`** (14B; roughly 9-11 hours). Do each as its own Kaggle notebook, ideally on two different accounts at the same time. Start them and leave them.

The notebook was written but never run on a GPU. If it crashes, copy the **last 40 lines of the log** and send them; do not try to fix the code yourself. Anything it already finished is saved and will not be redone.

## 1. One-time setup (about 10 minutes)

1. Make a Kaggle account at kaggle.com and **verify your phone number** (Settings > Phone verification). Without it you cannot use the GPU or the Internet in notebooks.
2. Make a free Hugging Face account at huggingface.co. Go to Settings > Access Tokens > **Create new token**, type **Read**, name it `kaggle`. Copy the token (starts with `hf_`). **Never post it in chat, in a notebook or on GitHub.**

## 2. Open the notebook

1. Download the notebook from GitHub: open `https://github.com/RafiRCh/LostInSteering`, go to `notebooks/08_unified_scale_run.ipynb`, click the download icon (**Download raw file**).
2. On Kaggle: **Create > New Notebook**, then **File > Import Notebook**, and choose the file you downloaded.

## 3. Settings (right-hand panel, "Session options")

1. **Accelerator: GPU T4 x2.** (It must be two GPUs, not one.)
2. **Internet: On.**
3. **Persistence:** leave the default.
4. Add the token: top menu **Add-ons > Secrets > Add secret**. Label: `HF_TOKEN`. Value: your `hf_...` token. Then switch on **Attached** next to it. Without this the notebook stops on purpose at the start with "No Hugging Face token found". That is intended, because downloads without a token are slow.

## 4. Choose the preset

In the first code cell group, find the line:

```python
PRESET = "notebook_1"
```

Use `"notebook_1"` for the first run and `"notebook_2"` for the second. Change nothing else.

## 5. Start it

Click **Save Version > Save & Run All (Commit)**. Choose "Save & Run All", then Save. Leave the tab alone; you can close the browser. The run happens on Kaggle's servers.

To watch it: open the notebook's **Versions** tab, click the running version, and look at the **Logs**. Early in the log you should see:

- `HF token: ACTIVE and valid` (if not, check step 3.4)
- `FLOOR CHECK ...` lines for each language. This is the first sign that the experiment works. **Send these lines to the team as soon as they appear.**

## 6. If it stops before finishing (this is normal for long runs)

The notebook stops itself cleanly at about 11 hours so the results are saved. It also saves everything as it goes.

1. When the version finishes (or fails), open it and go to the **Output** tab. Check that a folder `run08_<preset>` exists. Click **New Dataset** to turn the output into a dataset (name it e.g. `run08-small-part1`).
2. Make a new copy of the notebook (same settings, same `PRESET`), and under **Input > Add Input** attach that dataset.
3. Click Save & Run All again. The log will say `Resumed: copied N cached files`, and the notebook will skip everything already done.

Repeat until the log ends with `DONE`.

## 7. Send the results back

When the log ends with `DONE`:

1. Open the version's **Output** tab and click **Download All** (a zip).
2. Send the zip to the team (Drive link or similar). If it is very large, delete the `vectors.pt` files and the `_cache` folders from the zip first; they are not needed for the paper.
3. The files we need are in `run08_<preset>/<model>/`: `diagnostics.json`, all `*.csv`, and the `*.png` figures.

## Troubleshooting

| What you see | What to do |
|---|---|
| `No Hugging Face token found` | Redo step 3.4 (secret named exactly `HF_TOKEN`, **Attached** switched on) |
| `HF token check failed` | The token is wrong or expired. Make a new Read token and update the secret |
| `CUDA out of memory` repeated | Normal; the notebook halves its batch size by itself. Only worry if it fails completely |
| Notebook shows GPU count 1 | Session options is on a single GPU. Switch to **GPU T4 x2** and run again |
| Run failed with a Python error | Send the last 40 lines of the log. Re-running with the same dataset attached (step 6) continues from where it was |
| Stuck for more than 2 hours with no new log line | Normal during the long 14B stages (each language can take 20+ minutes). Wait unless Kaggle shows the session ended |

Kaggle gives about 30 GPU hours per week per account, so do not run more than one of the two runs per account per week.
