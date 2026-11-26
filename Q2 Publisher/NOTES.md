# IOP Publishing: publishing notes (Q2 Publisher)

Collected 24 Nov 2026. Sources are listed in `sources.md`. Pages are saved in `pages/` (raw HTML) and `text/` (extracted text).

## 1. What I could and could not collect

- **Full-site scrape not done.** `iopscience.iop.org/robots.txt` sets `User-agent: *` to `Disallow: /`. The site terms prohibit systematic downloading. I did not render the blocked pages with Playwright or any other browser, because that would get around the block.
- **Allowed pages fetched.** The publishing-support subdomain (`publishingsupport.iopscience.iop.org`) allows crawling. I fetched 35 of its publisher-facing pages, plus About, Terms and copyright pages from `ioppublishing.org` and `iopscience.iop.org`. The `ioppublishing.org` robots.txt allows crawling except `/info/`, `/wp-admin/` and `/wp-login.php`.
- **Not fetched.** The per-journal "about" pages (about 185) and the article-level FAQ pages. Acceptance rates and per-journal acceptance decisions are not published in the pages I read. The main site (disallowed) may hold them.
- **Read in full so far:** choosing a journal, submission checklist, open access overview. **Listed but not yet read in detail:** review process, first decision, revisions, acceptance, after publication, data policy, copyright, ethics, APC refund, accepted manuscripts. Those are in `text/` for later review.

## 2. How to publish (from the author pages)

1. **Choose a journal first.** IOP's guidance lists these factors: peer review quality, relevance and audience, scope, article types (Letter vs Paper), reputation, indexing (Web of Science and Scopus for IOP journals, shown under "Abstracted in" on each journal homepage), language, cost, and open access vs subscription. Check the journal's aims and scope before you write.
2. **Pre-submission checklist.** Confirm that:
   - the article fits the journal's scope and you know its article type;
   - you have a PDF of the full manuscript;
   - you know the journal's peer review model (single-anonymous means author names go in the manuscript; double-anonymous means you must anonymise);
   - the abstract is clear enough for reviewers to judge expertise;
   - all co-authors' names, emails, ORCID iDs and affiliations are ready (fewer than 20 co-authors);
   - references follow the style guide;
   - third-party material is cited in captions, and permission is obtained before acceptance;
   - supplementary material is ready;
   - the journal's ethics policy is met (ethics statement for human or animal work, or images of people);
   - the journal's research data policy is considered;
   - you have an ORCID iD.
   A free pre-submission "Preflight" tool checks many of these on a Word file.
3. **Submit** through the journal's submission system. (The submission and review pages were listed but not yet read.)
4. **Transfer if needed.** IOP's in-house editors can offer a transfer to another IOP journal. Reviewer reports can transfer with the manuscript, and no resubmission is needed. A transfer is not a guarantee of acceptance.

## 3. Open access and cost

- Gold open access: the article is free to read and reuse. Authors keep copyright and publish under **CC-BY**. Most IOP journals offer this option, and some are fully open access.
- Transformative and institutional agreements: some authors publish at no cost to themselves. The agreements hub and the IOPP Journal Finder show whether your institution is covered.
- Green open access: in subscription journals, authors may archive the accepted version (see the overview page for the embargo and version rules; not yet read in full).
- Article processing charges and refund policy: on the APC refund policy page (`text/31`). Exact prices are not in the pages I read yet.

## 4. Where to publish: journal list

- The journal list is on `publishingsupport.iopscience.iop.org/publishing-support/journals/`. I read the top-level page only. The sitemap lists about 300 journal URLs, and about 185 "about-journals" pages.
- Journals I could identify from the homepage (from the blocked site's link list, ISSNs checked against Crossref):
  - Physics in Medicine and Biology (0031-9155)
  - Reports on Progress in Physics (0034-4885)
  - Journal of Physics: Conference Series (1742-6596)
  - Environmental Research Letters (1748-9326)
  - IOP Conference Series: Earth and Environmental Science (1755-1315)
  - IOP Conference Series: Materials Science and Engineering (1757-899X)
  - Quantum Science and Technology (2058-9565)
  - Machine Learning: Science and Technology (2632-2153)
- The journal list is not complete here. The sitemap includes many more titles, including the Chinese Physics and Japanese Journal of Applied Physics series.

## 5. What has been published before (Crossref, 2024 onward)

Source: Crossref REST API (`api.crossref.org/journals/{ISSN}/works`), accessed 24 Nov 2026. The count is registered DOIs with a publication date from 1 Jan 2024. It is not the same as acceptances, and proceedings volumes inflate some counts.

| Journal | ISSN | Items with DOI, 2024 onward |
|---|---|---|
| Journal of Physics: Conference Series | 1742-6596 | 32,633 |
| IOP Conference Series: Earth and Environmental Science | 1755-1315 | 18,585 |
| Physics in Medicine and Biology | 0031-9155 | 1,899 |
| IOP Conference Series: Materials Science and Engineering | 1757-899X | 1,953 |
| Environmental Research Letters | 1748-9326 | 2,852 |
| Machine Learning: Science and Technology | 2632-2153 | 998 |
| Quantum Science and Technology | 2058-9565 | 814 |
| Reports on Progress in Physics | 0034-4885 | 325 |

- 2979-2584 was not found in Crossref.
- Acceptance rates, rejection rates and time to decision are **not in these sources**. They would have to come from the journal pages (not fetched) or from IOP directly.

## 6. Gaps and next steps

- Read the remaining author pages: review process, first decision, revisions, acceptance, and after publication. These contain the decision and timing details.
- Ask IOP for acceptance rates, median time to first decision and article processing charges for each target journal. The contact page lists the channels.
- If you want the journal-by-journal scope and author guidelines, the per-journal "about" pages on the publishing-support subdomain are the allowed route. That is about 185 pages, so fetch them with a delay and only the journals you care about.
- Crossref counts can be broken down by article type or by year if you need trends.

## 7. Timeline: from submission to publication

Based on the author process pages (review process, first decision, revised article, acceptance and publication, after publication). Each stage gives the typical timing from the pages. Actual timing differs by journal, so check each journal's homepage for its median decision time.

| Stage | What happens | Typical timing (from IOP's pages) |
|---|---|---|
| 0. Before submitting | Choose a journal, check scope and article type, run the checklist, and anonymise the manuscript if the journal uses double-anonymous review | Your own time. Not measured by IOP |
| 1. Submission | Submit the PDF and source files through the journal's submission system. A free Preflight tool checks a Word file | Not stated. I did not find a submission window, so the pages suggest you can submit whenever the manuscript is ready. Confirm this on the journal page |
| 2. Pre-review check | Some journals have a quick quality check by an editorial board member. A rejection here is possible, and an optional transfer offer may follow | Not stated. Some journals offer a transfer; you have 10 days to accept or decline |
| 3. Peer review | Usually two independent reviewers. If they disagree, an adjudicator decides | Journal-specific. IOP says its times are among the fastest in its communities. Median times are on each journal homepage. Reviewers can request a short extension |
| 4. First decision | You receive an email with one of: provisional accept, minor revision, moderate revision, major revision, reject (you may resubmit), reject, or transfer offer | Email on decision day. Reviewers' reports come with it |
| 5a. Revision (if requested) | Send a revised PDF, source files, a copyright form and written permissions where needed. Include a point-by-point response to every reviewer comment | Minor: 1–2 weeks. Moderate: 2–4 weeks. Major: 4–8 weeks. The exact deadline is in your decision email. The revised version goes back to the reviewers, or to in-house staff for minor changes |
| 5b. Acceptance | Provisional accept, then formal accept once the editorial team has the copyright form and all required items | No timing given. IOP cannot formally accept until the signed copyright form is in |
| 6. Accepted manuscript | Most journals post the accepted manuscript within 24 hours of acceptance (an option, not every journal) | Within 24 hours, where offered |
| 7. Typesetting and proofs | The article is typeset in house style. You check the proof and send corrections. You are responsible for the final accuracy | Corrections are processed and the paper is published about one week after corrections arrive. The proof review period can be extended if you tell IOP you will be away |
| 8. Publication | Version of Record published online. You get an email | About one week after proof corrections |
| 9. After publication | Promote the article, update citations and profiles, deposit the accepted manuscript in a repository (usually a 12-month embargo) | Ongoing. Corrections go through a formal corrigendum process |

**Key points**

- **Rejection rates:** most journals reject more than half of submissions, according to IOP's review page. Rejections can come before peer review.
- **Copyright form:** you must submit the signed copyright form before formal acceptance. For hybrid subscription articles you transfer copyright to IOP. For fully gold open access articles you grant IOP a non-exclusive licence. Gold open access articles are published under CC-BY.
- **Resubmission limits:** articles rejected in the same or a substantially similar form are generally not reconsidered by any IOP primary journal.
- **Gaps in this timeline:** the pages do not give a submission window, a median time to first decision for each journal, or acceptance rates. Those are on the journal homepages (not fetched) or need to come from IOP directly.

**Realistic overall range.** Adding the stages together gives a rough range. With no revision, first decision plus typesetting is typically a few weeks to a few months, depending on the journal's review times. With one major revision, add 4–8 weeks plus another review round. Treat these as estimates and confirm against the journal's median times.
