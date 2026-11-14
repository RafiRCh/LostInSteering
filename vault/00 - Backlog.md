---
tags: [backlog]
created: 2026-11-14
updated: 2026-11-14
---

# 00 - Backlog

Project: cross-lingual transfer of sycophancy steering vectors (see `docs/proposal/proposal_v1.pdf`, smoke test in `notebooks/01_smoke_test_v1.ipynb`, results in `results/01_smoke_test_v1/`).

Parked; not in the current scope.

## Hindi → Bengali vector transfer (sibling-language transfer)

**Idea:** Instead of only asking "does an English vector work in Bengali?", ask "does a Hindi vector work in Bengali (and vice versa) better than the English one does?" Hindi and Bengali are both Indo-Aryan languages with a lot of Sanskrit-derived vocabulary, so a vector built from one might carry over to the other more cleanly.

**Caveat on the premise:** they are related, not "almost the same". They use different scripts (Devanagari vs Bengali), so the model sees completely different tokens, and grammar and everyday vocabulary differ enough that speakers of one don't automatically understand the other. That makes the test interesting: if Hindi still beats English for Bengali, the relationship is being carried at the meaning level, not by shared tokens.

**Why it might matter:** Bengali has far less training data than Hindi. If a Hindi vector steers Bengali well, then for a low-resource language you could borrow the vector from a better-resourced sibling instead of building one from scratch.

**Early hint (smoke test v1, Qwen2.5-7B, 2026-11-14):** Hindi and Bengali vectors had similar, lower cosine similarity to the English vector (about 0.6–0.7 at layers 18–21) than Spanish and Chinese (about 0.9). We did not measure Hindi vs Bengali directly; the vectors were not saved.

**How to test (cheap, reuses the v2 pipeline):**
- Save the per-language vectors in the notebook (`torch.save(VECS, ...)`).
- Compute Hindi–Bengali cosine per layer; compare with English–Bengali.
- Steer Bengali prompts with the Hindi vector; compare steerability with the English and native Bengali vectors. Do the reverse (Bengali vector on Hindi).
- Control: a non-sibling source of similar resource level (e.g. Arabic vector on Bengali), so "sibling" is tested against "just another non-English language".
- Optional: also try the Hindi vector on Marathi, Gujarati or Nepali (Nepali also uses Devanagari) to separate "same script" from "same language family".

**Do this after** v2 gives a reliable signal (native vectors clearly beating random). With v1's weak, noisy vectors the comparison would be meaningless.
