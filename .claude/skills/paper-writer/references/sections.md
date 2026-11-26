# Section recipes

## Introduction (fit it on page one if you can)

Content, wide to narrow (the funnel):
1. Field: what everyone agrees on, with citations. Two or three sentences at most.
2. Gap: a problem with a cost. "X fails in this way, which costs Y" beats "nobody has studied X."
3. Specific question, in one sentence.
4. What you did.
5. Contributions: "We make the following contributions:" then bullets, each refutable and with a forward reference.
6. One line saying where related work is discussed in full (if it comes late).

How to write it:
- Reach the problem within a few sentences. No paragraphs of general background.
- Show the problem with a concrete example (a code fragment, one item, one data point) before describing it in general terms.
- Choose a molehill, not a mountain: hard enough to be interesting, small enough to be solved by this paper.
- Make the final "In this paper we..." paragraph specific, since skimmers decide based on it.
- Do not write a "The rest of this paper is organized as follows" paragraph. The forward references replace it. A section that no contribution points to may not belong in the paper.
- Do not repeat the abstract.

## Core technical sections

- Start with an example and the intuition. Formal definitions follow.
- Every section supplies evidence for a listed contribution: a proof, measurements, an analysis, a comparison, or a case study. The evidence should be enough to believe the claim and to reproduce it.
- Describe a dead end only when it is the obvious approach and its failure explains your design.
- Limitations can sit here when they come up naturally and the reader can follow them at this point. Otherwise put them in the discussion or related work.

## Results

- Per figure: bullets, then a paragraph. Say what was measured, what was found, n or the number of repeats, and which figure or panel shows it.
- Report nulls and negatives plainly.
- In a combined Results and Discussion section, follow each result with its meaning in the same paragraph.

## Methods

The competent-stranger test: someone in the field can repeat the work without contacting you. Cover:
- Who or what: participants and recruitment, materials and suppliers, models with versions and checkpoints, datasets with versions and splits, item counts.
- What you measured and how: instruments, metrics with exact definitions, prompts, hyperparameters, seeds, hardware.
- Analysis: statistical tests, software and versions, exclusion rules.
- What you chose not to do, and why or what you used instead.

## Discussion (four moves)

1. Restate the key finding with numbers. "This study found that..."
2. Place it in the literature: what it extends, confirms, or contradicts.
3. Limitations, named honestly: measurement, design, population (and for ML: models, languages, data, compute).
4. What comes next. Each limitation should point to the next study.

Keep "what the data shows" and "why we think it happens" in separate sentences, and label the second as interpretation.

## Related work

- Cite as you go in the introduction and the technical sections, at the points where the work would come up naturally in a whiteboard explanation. Hold detailed comparison for a section near the end, once the reader has the vocabulary. Follow the venue if it requires an early section.
- Give credit generously. Praise you believe costs nothing.
- State honestly where your approach is worse. If a reviewer finds the weakness first, it counts against you.
- Leave out no close neighbour. "The authors seem unaware of [paper] that covers 80% of this" sinks papers.
- For tool or benchmark comparisons, describe the competitor fairly and let the table show the difference.

## Conclusion

Short. Main findings and what they mean, the answer to the paper's question, and how far that answer goes. No new information. If the conclusion needs a new fact, the body is missing it. Do not copy the abstract into the past tense. Future work, if included, takes a few lines and invites others to take it up.

## Abstract

Default (six moves, about 150 to 250 words): context, what you did, main result, nuance (where it did not hold), key number, meaning and boundary.
Short (four sentences, for tight limits): the problem, why it matters, what the solution achieves, what follows.
Assemble it from sentences already in the paper: the opening of the introduction, the "what we did" paragraph, the conclusion, the headline number in the results. If a move has no source sentence, fix the paper first. Narrative abstracts (background, problem, solution) read better and, according to studies cited in one source video, are cited more. Keep jargon out.

## Title

States the finding, not the topic. "Observation of gravitational waves from a binary black hole merger," not "A study investigating..." Include the field's search keywords (check Google Scholar for the terms people use). Avoid question titles, which one source video reports are downloaded more but cited less. Humor is allowed if the finding stays visible. Do not use hype words.

## After review (rebuttals and resubmission)

- Read the reviews, then wait before responding. A session should draft calmly and assume good faith.
- For each misunderstanding, ask how to rewrite the paper so that no reviewer could misread it again, and make that edit. Then point to it in the response.
- Separate real errors (fix them), misreadings (clarify the paper), and requests for out-of-scope work (decline politely with a reason, or add a limitation).
- Every response cites the changed section or line.
