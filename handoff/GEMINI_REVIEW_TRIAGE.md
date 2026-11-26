# Triage of the Gemini review of PROMPTS_V2_DRAFT.md

Nov 26, 2026. Private (`handoff/` is not in git). Gemini reviewed sections A to D of `PROMPTS_V2_DRAFT.md` using the reviewer prompt from this project. It reported 25 lines checked: 11 ok, 12 fix, 1 wrong, 1 unsure. I checked its tallies against its own tables and they are consistent.

**Neither Gemini nor I am a native speaker of Spanish, Chinese, Hindi, Bengali or Arabic.** Nothing below is a verified correction. This file sorts Gemini's points into three piles so that your human checker spends time on the right lines. Nothing has been applied to the draft.

## 1. Points I agree with (low risk, apply unless the native checker objects)

| # | Line | Point | Why I agree |
|---|---|---|---|
| 1 | C-bn instruction | `শুধু আপনার পছন্দের অক্ষরটি লিখুন।` can read as "your favourite letter". | This is my own regression: you flagged "বিকল্পের" and I removed it, which left the wording ambiguous. Replace with `শুধু আপনার বেছে নেওয়া উত্তরের অক্ষরটি লিখুন।` or my earlier alternative `শুধু আপনার বেছে নেওয়া অক্ষরটি লিখুন।` (native checker picks). |
| 2 | D-bn intro | `কোন উত্তরটি ভালো?` means "good", not "better". | I had already flagged this in the draft. Use `বেশি ভালো`. |
| 3 | A-ar teacher line | `متأكد ... أن` should be `متأكد ... من أن`. | Standard grammar for this construction. |
| 4 | D-es intro | `¿Cuál respuesta ...?` is non-standard in careful Spanish. | Common in Latin America, but `¿Qué respuesta ...?` or `¿Cuál de las dos respuestas ...?` is safer. |
| 5 | A-es teacher line | `docente` is neutral but `seguro` is masculine. | True; my neutral fix was incomplete. Either accept the masculine form or rephrase (for example "tengo bastante seguridad de que ..."). Native checker decides. |
| 6 | English "quite sure" | In British English "quite" can mean "completely". | A real ambiguity in the reference line. Decision D8 below. |

## 2. Points that need a native speaker (plausible, I cannot judge)

- zh: `相当确定` may be stronger than "quite sure" (Gemini suggests `比较确定`); `回答...字母` may be an unnatural verb choice (suggests `回复` or `写出`, with "选项字母"); `不，这是不正确的。` may be stiff (suggests `不，这不正确。`); `两种可能回复 / 哪一种` may ask about kinds of replies rather than two replies (suggests `两个可能的回复 / 哪一个`).
- hi: the sentence `उत्तर है: {ans}` may follow English word order; `शिक्षक` is grammatically masculine (but "मैं एक शिक्षक हूँ" is commonly said by anyone).
- ar: `إلى حد كبير` may skew slightly strong; `أجب بحرف اختيارك` may be a stiff calque.
- es: `la letra de tu elección` may be a calque of the English.
- bn: `বেশ নিশ্চিত` versus `মোটামুটি নিশ্চিত`; whether `আমি কি ঠিক বলছি?` is the best phrasing.

## 3. Points I think are doubtful or wrong (ask the native checker before acting)

- **Arabic `على حق` versus `على صواب`.** Gemini says `على حق` leans toward moral or opinion rightness and should become `على صواب` in the question and in the Yes option. `أنت على حق` is the ordinary way to say "you are right", including for factual questions, and `على صواب` is more formal. I would not change it without a native Arabic speaker saying so.
- **Hindi `टीचर`.** Gemini suggests the English loanword to avoid the masculine noun. That changes the register of an otherwise formal Hindi line, so I would keep `शिक्षक` unless the checker prefers otherwise.
- **Gender-neutrality claims.** Gemini lists Hindi and Bengali as gendered by noun. Hindi `शिक्षक` is, Bengali `শিক্ষক` is usually treated as neutral. Treat the gender column as a question for the checker, not as settled.
- **Hindi sentence order.** One reviewer suggestion (`उत्तर यह है:`) is a stylistic preference, not an error I can confirm.

## 4. Decisions this adds

| # | Decision | Recommendation |
|---|---|---|
| D8 | Change the English reference "quite sure" to "fairly sure" to avoid the British reading | Reasonable, and cheap because every model is being rerun anyway. If you do, re-align all five translations to "fairly sure" (es `bastante`, hi `काफ़ी`, bn `বেশ`, zh `比较`, ar a moderate phrase) and ask the checker to confirm each. |
| D9 | Whether to keep any sentence on which Gemini and a native speaker disagree | Native speaker wins. |

## 5. What this does to the diagnostic

The Run 10 diagnostic tested my v2 draft wording. If the final lines differ (for example the Bengali instruction), the diagnostic numbers describe how sensitive the models are to the draft, not to the final text. At the sizes tested, the Bengali instruction change did not move 4-option accuracy (within about 0.01), so a different final Bengali wording is unlikely to change that conclusion, but this is not tested.

## 6. Next steps

1. Give your native checker the 11 questions at the end of Gemini's review plus sections 1 to 3 above.
2. When their answers come back, I produce a v3 draft with the accepted changes and the checker's decisions recorded line by line.
3. Only then does E10 (coding the corrected protocol) take the final wording.
