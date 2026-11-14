# Knowledge probe: results notes

**Run:** 2026-11-11 to 2026-11-14 on Kaggle (2× T4), notebook `notebooks/02_knowledge_probe.ipynb`, Kaggle kernel `rafirahmanchowdhury/lostinsteering`. Runtime ~32 min.

**Models evaluated:**
1. `Qwen/Qwen2.5-7B-Instruct`
2. `mistralai/Mistral-7B-Instruct-v0.3`
3. `microsoft/Phi-3.5-mini-instruct`

Across 6 languages: English (`en`), Spanish (`es`), Chinese (`zh`), Hindi (`hi`), Bengali (`bn`), Arabic (`ar`).

**Verdict printed by notebook:** **`Qwen2.5-7B-Instruct` is USABLE for steering v2** (`usable_for_v2: True`).

---

## Key Findings

### 1. Global-MMLU-Lite Exam Questions (300 questions per language)
* **Qwen2.5-7B-Instruct** is the strongest multilingual model across the board:
  - English: 77.3%
  - Spanish: 70.7%
  - Chinese: 68.7%
  - Arabic: 62.0%
  - Hindi: 48.0%
  - Bengali: 44.3% (weakest language, still well above 25% random baseline)
  - **Known in all 6 languages:** **74 questions**
* **Mistral-7B-Instruct-v0.3** struggles heavily on non-European scripts:
  - Hindi: 24.7% (random chance level)
  - Bengali: 24.7% (random chance level)
  - Known in all 6 languages: only 21 questions
* **Phi-3.5-mini-instruct** (3.8B):
  - Bengali: 28.0%
  - Known in all 6 languages: only 22 questions

### 2. Arithmetic Capability
* All three models failed to achieve ≥ 80% accuracy across all 6 languages at all three tested difficulty levels (`usable_arith_level: none`).
* This confirms the observation from smoke test v1: arithmetic errors measure confusion rather than sycophancy. Fact-based MMLU questions where the model demonstrably knows the answer in all 6 languages must be used instead.

### 3. Sycophancy on Known Items
* Tested on the items each model answered correctly across **all 6 languages**:
  - **Qwen2.5-7B-Instruct:** Mean `agree_wrong` = 32.9% (max 49.5%), mean `honesty_gap` = 44.7%. It exhibits significant sycophancy when pressured with a wrong answer, but retains enough honesty gap to be steered effectively.
  - **Mistral-7B-Instruct-v0.3:** Severe sycophancy / yes-man behavior (`agree_wrong` = 82.0%), narrow honesty gap (13.0%).
  - **Phi-3.5-mini-instruct:** High `agree_wrong` (51.3%), honesty gap (21.9%).

---

## Decision for Steering v2

* **Model chosen:** `Qwen/Qwen2.5-7B-Instruct`.
* **Clean item pool:** 74 parallel questions saved in `known_all_langs__Qwen2.5-7B-Instruct.json`.
* Steering v2 will construct vectors and measure sycophancy transfer strictly using this validated item pool.

---

## Files

| File | Contents |
|---|---|
| `model_choice_summary.csv` | Summary metrics and usability verdict per model |
| `mmlu_accuracy.csv`, `mmlu_accuracy.png` | Global-MMLU-Lite accuracy by language and model |
| `sycophancy_on_known_items.csv`, `sycophancy_on_known_items.png` | Sycophancy (`agree_wrong`) and honesty gap on verified known items |
| `arithmetic_accuracy.csv` | Arithmetic accuracy across difficulty levels and languages |
| `known_all_langs__Qwen2.5-7B-Instruct.json` | 74 question IDs known in all 6 languages by Qwen2.5 |
| `known_all_langs__Mistral-7B-Instruct-v0.3.json` | 21 question IDs known in all 6 languages by Mistral |
| `known_all_langs__Phi-3.5-mini-instruct.json` | 22 question IDs known in all 6 languages by Phi-3.5 |
| `kaggle_run.log` | Complete Kaggle run log |
| `kernel-metadata.json` | Kaggle kernel configuration metadata |
