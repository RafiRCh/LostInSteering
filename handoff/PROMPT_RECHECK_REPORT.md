# Prompt recheck report and rerun recommendation

Nov 25, 2026. Private (`handoff/` is not in git). Based on a re-read of every prompt in Runs 01 to 09 and on the existing Run 08 result files. Nothing was rerun for this report, so every statement about effect size on the results is a reading of existing numbers, not a test.

## Revision (Nov 25, after devil's-advocate review): decide with a diagnostic first

The recommendation below was written before this review and is now **conditional**. A full rerun is about 55 to 65 Kaggle hours (Qwen about 30, new families 25 to 35), and nobody has measured two things that decide whether it is needed or even feasible:

- **Feasibility of the new pool rule.** 4-option accuracy at 3B is 0.31 in Hindi and 0.35 in Bengali (chance 0.25). Requiring a correct answer in six languages and in two option orders could leave the 3B pool at a few dozen items, and 0.5B and 1.5B near zero. Llama 3.2 1B and 3B (no official Bengali support) and Gemma E2B could fail the same way. The rule also tests recall of an answer from four options, which is stricter than recognising a stated answer, and requiring two orders at accuracy near 0.4 drops items the model may know.
- **Whether the old results move at all.** At 7B and 14B the models clearly separate true from false claims, so the pool is probably much less contaminated at the scales that carry the headline.

**Diagnostic job (about 3 to 5 h, one Kaggle session), before any full rerun:**
1. For Qwen 3B, 7B fp16 and 14B nf4, score 4-option accuracy in both option orders on the existing pool items in all six languages. This gives the surviving pool size under the strict rule and a softer one (correct in at least one order).
2. On 3B or 7B, compare old and new Bengali instruction, and old and new "quite sure" line, on baseline agreement.
3. Re-score baseline, English-vector anti-steering at the headline multiplier, and the random vector on the surviving subset, to see whether the headline holds. (Whether `_cache` already holds per-item steered scores is unchecked; if it does, step 3 is nearly free.)

**Decision rule, fixed before the job runs:**
- If the headline holds on the surviving subset and the prompt changes shift baselines only slightly: keep the existing Qwen runs, report the diagnostic as a robustness appendix, and run the new families under the existing protocol.
- If the headline shrinks substantially, or the prompt changes matter, or the strict rule leaves usable pools only at 7B and 14B: do the full rerun with the corrected protocol, and restrict claims to the models that keep usable pools.
(Define "shrinks substantially" and "slightly" as numbers with the supervisor before running; I have not set them.)

The supervisor proposal should lead with this diagnostic, because it is cheaper and easier to defend than asking approval for 60 hours.

## Recommendation (original, now conditional on the diagnostic above)

**Rerun everything from the beginning under one corrected protocol. Do not just patch the prompts and carry on with the old Qwen runs.**

Reasons, in order of weight:

1. **The new families must be comparable with Qwen.** The project rule is that any new family runs the Run 08 protocol. If Llama and Gemma get corrected prompts and Qwen keeps the old ones, the cross-family comparison mixes two protocols. If Llama and Gemma keep the old prompts, they inherit the flaws below.
2. **The biggest problem is not a translation; it is how the item pool is built** (finding 1). A prompt fix alone does not repair it. Rerunning only to change wording would leave it in place.
3. **Bengali and Hindi, the languages the paper cares most about, are the ones most exposed.** Their data are the least trustworthy in the current runs.

Do not delete the old Qwen results. Keep them as the "v1 protocol" runs. If the rerun uses v2, the v1 and v2 results on the same models become a prompt-sensitivity check, which is worth a short section in a paper.

## Does it compromise the existing Qwen runs?

Partly, and unevenly. I cannot put a number on it without a test.

| Kind of result | Exposure | Why |
|---|---|---|
| Within-language steering effect, such as agreement with true claims dropping 38 to 81 points at 7B under the English vector | Low | The effect is large and measured against the same language's own baseline. A one-word wording change is unlikely to produce or erase a drop of that size. Not proven. |
| Baseline sycophancy compared across languages | Medium to high | The pressure line says "quite sure" in English and Spanish but "very/completely sure" in Chinese, Hindi, Bengali and Arabic (my reading, needs native confirmation). The data do not show a clean wording effect (Chinese has the stronger wording and the lowest baseline agreement), so I would not claim it explains the differences, only that it is an uncontrolled difference. |
| Anything for Bengali and Hindi | High | See findings 1 and 2. |
| Transfer of the English vector to other languages, and native versus English vector | Medium to high | Depends on the pool and on Bengali and Hindi data. |
| Opinion results | Medium | Opinion replies were cut at 300 characters (finding 5), and 10 of 30 cells already failed the 0.10 to 0.90 floor check. |

## Findings, most serious first

**1. The "known item" probe does not measure knowledge.** In `notebooks/src/08_unified_scale_run.py` (the probe at lines 649 to 651), an item counts as known when the model prefers "(A) Yes, you are right" while the teacher states the true answer. That measures agreement with a true claim. A model that says "yes" to everything passes. The plan file already notes this: Qwen 0.5B passed 604 of 608 Bengali items. The item pool for every run is the set of items "known" in all six languages, so yes-biased languages let in items the model does not know.
Evidence in the result files, with a correction (Nov 25, after review): the 4-option accuracies in `capability_mmlu.csv` (7B fp16: 0.71 English, 0.40 Bengali, 0.42 Hindi) are computed on items that are NOT in the pool (the code takes `valid_ids` not in `POOL`, line 1043). They show how weak the model is in Hindi and Bengali in general. They are not direct evidence that the pool holds unknown items. Direct evidence is weaker and mostly at small scale: at 1.5B, baseline agreement with false claims on the pool is 0.99 in Hindi, 0.94 in Bengali and 0.97 in Arabic, which looks like agreeing with everything. At 7B and 14B the models separate true from false claims clearly (agree_true 0.97 to 0.99 in Hindi and Bengali against agree_wrong 0.50 to 0.64 at 7B), so pool contamination is probably much smaller there. Whether the pool actually holds unknown items has not been measured. A second, separate concern: the pool is selected on agreement with true claims, which is also the headline outcome, so the size of the reported drop in agreement may be inflated by the selection. The random-vector control suggests the effect itself is real.
*Fix to decide:* build the pool from the 4-option exam question (model picks the right letter), possibly also requiring the right answer under both letter orders. This is a protocol change.

**2. Bengali answer-letter instruction uses "বিকল্পের"** (flagged by you). The line is appended to every Bengali item in every run and also to the 4-option accuracy prompt. v2 replaces it. I cannot say how much it lowered Bengali accuracy. A quick check: score Bengali 4-option accuracy on the same items with the old and new instruction (a small Qwen job, an hour or two).

**3. "Quite sure" intensity mismatch** in Chinese, Hindi, Bengali and Arabic, as described in `PROMPTS_V2_DRAFT.md`. Needs native confirmation.

**4. Gendered "teacher"** in Spanish and Arabic. Spanish has a neutral fix ("docente"). Arabic needs the checker's advice.

**5. Opinion replies cut to 300 characters.** 750 of 900 replies in the first 150 items are longer, so most are trimmed. The cut is at a sentence boundary when one exists after the halfway point, otherwise mid-text. Whether the cut changes the meaning of the reply has not been checked.

**6. Smaller points.**
- The yes and no options are not symmetric in English (yes talks about the person, no talks about the claim). Kept as is in v2.
- Register differs across languages (Spanish informal "tú", Hindi and Bengali formal). Kept as is.
- Persona prompts are English only and the six pairs mix "agreeable versus honest" with "agreeable versus skeptical". Persona is a null result, so this matters little.
- The opinion statements and exam questions are external datasets. I cannot repair them, only flag items.

## What I did not check

- I am not a native speaker of any of the five non-English languages. All v2 translations and back-translations are my drafts.
- I have not run a test of the old versus the new prompts. The exposure table is a reading of existing numbers.
- I have not compared how much the opinion truncation changes the replies' meaning.

## Cost of the rerun

From the Run 08 timings in `handoff/PLAN.md`: about 2 h at 1.5B, 5 h at 3B, 7.5 to 8 h at 7B, 10.8 h at 14B nf4, plus 0.5B and the 7B nf4 run. Roughly 30 h for all of Qwen, about one week of free Kaggle quota, and the Llama and Gemma lineup is another 25 to 35 h. To save time without weakening the paper:
- Drop the 0.5B run or keep it as a sanity anchor only. Its honesty is under 0.03 in every language, so it carries no information on steering.
- Skip the 7B nf4 run unless you want a quantization claim.
- Run 1.5B, 3B and 7B first. Run 14B last.

## Suggested order

1. A native speaker (or your checker) goes through `PROMPTS_V2_DRAFT.md` and the two item spreadsheets.
2. Decide the protocol changes: pool definition (finding 1), reply cut (finding 5), intensity wording (finding 3).
3. Apply them to `notebooks/src/08_unified_scale_run.py`, regenerate notebooks, and run the smoke preset.
4. Optional small test: old versus new Bengali instruction and teacher line on Qwen 1.5B or 3B, to measure what the fixes change.
5. Rerun Qwen (1.5B, 3B, 7B, then 14B), then the Llama and Gemma screening and full runs under the same protocol.

All of this stays paused until the supervisor approves the proposal.
