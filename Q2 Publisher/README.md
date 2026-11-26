# Q2 Publisher: IOP Publishing research folder

Collected 24 Nov 2026. This folder holds the publishing information for IOP Publishing (IOPscience) that could be gathered within the site's crawling rules. Other sessions should read `data/` first. It is structured. `NOTES.md` is the human-readable narrative.

## Read order for another session

1. `data/journals.json`: journal names, ISSNs, and Crossref counts from 2024 onward.
2. `data/timeline.json`: stages from submission to publication, with typical timings.
3. `data/requirements.json`: submission checklist, journal-choice factors, open access, copyright.
4. `data/sample_titles.csv`: 26 recent article titles with DOIs, grouped by journal.
5. `data/sources.json`: where each fact came from, and the robots and terms status.
6. `data/pages_index.csv` (or `.json`): map of every saved page to its URL, raw HTML and extracted text.
7. `NOTES.md`: narrative notes with the same facts, plus gaps.

## Files

| Path | Format | Contents |
|---|---|---|
| `README.md` | Markdown | This index |
| `NOTES.md` | Markdown | Full notes: process, open access, journal list, Crossref counts, timeline |
| `sources.md` | Markdown | Source list with robots and terms status |
| `urls.txt` | Plain text, one URL per line | The 42 URLs requested. Line N matches page `P{N:02d}` |
| `data/journals.json` | JSON | `journals[]`: `title`, `issn`, `crossref_items_from_2024`, `note`, `source`, `count_type` |
| `data/sample_titles.csv` | CSV | `journal, issn, doi, title, source, sort_order` |
| `data/timeline.json` | JSON | `stages[]` with `order`, `stage`, `timing`, `notes`; `key_facts` |
| `data/requirements.json` | JSON | `submission_checklist`, `journal_choice_factors`, `open_access`, `copyright`, `tools`, `unverified` |
| `data/sources.json` | JSON | `sources[]`: `id`, `name`, `url`, `robots`, `method`, `status` |
| `data/pages_index.json` / `.csv` | JSON / CSV | `id, url, raw_html, text_file, host, fetched, http_status` |
| `pages/` | HTML | Raw HTML of 42 pages, named `NN-host_path.html` |
| `text/` | TXT | Extracted text of the same pages, named `NN-host_path.txt` |
| `raw/` | XML | Publishing-support sitemap XML files, for reference |
| `build_data.py` | Python | Rebuilds the `data/` folder from `urls.txt`, `pages/` and the values recorded in the script |

## Access rules (read before fetching anything)

- **Blocked:** `iopscience.iop.org`. Its `robots.txt` has `User-agent: *` with `Disallow: /`. Its terms prohibit systematic downloading. Do not crawl or render this host (no Playwright or other browser to get around the block).
- **Allowed:** `publishingsupport.iopscience.iop.org` (robots.txt allows everything). Use a delay of at least 2 seconds per request.
- **Allowed with restrictions:** `ioppublishing.org` (robots.txt: `Disallow: /info/`, `/wp-admin/`, `/wp-login.php`; crawl-delay 600 seconds).
- **Metadata:** Crossref REST API, `api.crossref.org`. Use a descriptive, non-personal User-Agent.

## Data gaps (not yet collected)

- Per-journal scope and author guidelines (about 185 "about-journals" pages on the allowed subdomain).
- Per-journal median time to first decision, submission windows, and acceptance rates. These are on journal homepages or must come from IOP.
- Article processing charge (APC) amounts.
- Full text of the review, decision, acceptance and data-policy pages. They are saved in `text/` but have been only partly summarised.
- Journal title for ISSN 2979-2584 (not in Crossref).

## Caveats

- Crossref counts are DOIs registered since 2024, not acceptances. Conference-series counts include proceedings and are inflated.
- Titles are sampled from Crossref metadata, the 5 most recent per journal. They show what has been published, not what was rejected.
- The `text/` files and `pages/` HTML belong to IOP. Keep them private, and do not republish them. The folder sits inside the public LostInSteering repo, so keep it out of commits unless the owner decides otherwise.
