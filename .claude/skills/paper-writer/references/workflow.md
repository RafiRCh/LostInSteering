# Writing workflow

## Why this order

A reader reads title, abstract, introduction, body. A writer should go nearly the other way, because the front matter promises what the body delivers. The one exception is the specification (the idea and the contribution list), which comes first and steers everything else.

## Day one: the specification

- Finish the sentence "The main idea of this paper is ___." One paper, one idea. Several unrelated ideas usually mean several papers.
- List contributions as bullets. Each one is refutable (it could turn out false or undelivered) and points to the section with its evidence.
  - Weak: "We study the properties of X."
  - Strong: "We prove that type checking for X is decidable (Section 4)." or "Method A reduces error by 12 to 30% on all five benchmarks (Section 5, Table 2)."
- Start writing before the research is finished. The draft works as a forcing function. Gaps show up as sections you cannot write, and a paragraph that keeps collecting caveats marks an idea that is not settled. Report such gaps to the person as research to-dos rather than papering over them.

## Body, from figures outward

1. **Figures.** Storyboard them: one question per figure, in the order you would show them to a colleague while telling the story out loud. If the story will not hold together, the paper is not ready; say so. Cut figures that serve no contribution and keep them for later work.
2. **Results.** For each figure, write bullets (what was measured, what was found, n, which panel), then one paragraph. Include nulls and negatives.
3. **Methods.** Written once you know which methods produced the reported results. Aim for full reproducibility.
4. **Core sections.** Present the idea the way you would at a whiteboard: an example first, then the intuition, then the formal version. A reader who stops halfway should still take something away. Do not recount the dead ends of the research unless the obvious approach fails in a way the reader must see.
5. **Discussion**, then **related work**.

## Front matter, last

6. **Introduction.** Sketched on day one as the specification, finished now.
7. **Conclusion.**
8. **Abstract**, assembled from sentences already in the paper.
9. **Title.**

## Then

Humanizer pass, evidence audit, cold-reader test, checklist. See SKILL.md steps 4 to 7.

## Space and detail

Detail goes where it explains the idea. Proofs, extra tables, and loosely related material go to an appendix or supplement, which works like a subroutine call: the reader gets the result inline and the evidence on request. Write section headings you would want to read, not only the generic ones.
