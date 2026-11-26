import json, os, csv

TODAY = "2026-11-24"
os.makedirs("data", exist_ok=True)

urls = [u.strip() for u in open("urls.txt", encoding="utf-8") if u.strip()]
pages = sorted(os.listdir("pages"))
index = []
for f in pages:
    n = int(f[:2])
    url = urls[n - 1]
    index.append({
        "id": f"P{n:02d}",
        "url": url,
        "raw_html": f"pages/{f}",
        "text_file": f"text/{f[:-5]}.txt",
        "host": url.split("/")[2],
        "fetched": TODAY,
        "http_status": 200,
    })
json.dump(index, open("data/pages_index.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
with open("data/pages_index.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(index[0].keys()))
    w.writeheader()
    w.writerows(index)

journals = [
    {"title": "Physics in Medicine and Biology", "issn": "0031-9155", "crossref_items_from_2024": 1899},
    {"title": "Reports on Progress in Physics", "issn": "0034-4885", "crossref_items_from_2024": 325},
    {"title": "Journal of Physics: Conference Series", "issn": "1742-6596", "crossref_items_from_2024": 32633,
     "note": "includes proceedings; inflates count"},
    {"title": "Environmental Research Letters", "issn": "1748-9326", "crossref_items_from_2024": 2852},
    {"title": "IOP Conference Series: Earth and Environmental Science", "issn": "1755-1315",
     "crossref_items_from_2024": 18585, "note": "includes proceedings; inflates count"},
    {"title": "IOP Conference Series: Materials Science and Engineering", "issn": "1757-899X",
     "crossref_items_from_2024": 1953, "note": "includes proceedings; inflates count"},
    {"title": "Quantum Science and Technology", "issn": "2058-9565", "crossref_items_from_2024": 814},
    {"title": "Machine Learning: Science and Technology", "issn": "2632-2153", "crossref_items_from_2024": 998},
    {"title": None, "issn": "2979-2584", "crossref_items_from_2024": None,
     "note": "not found in Crossref; title unknown; listed on the blocked homepage only"},
]
for j in journals:
    j["source"] = "Crossref REST API, accessed " + TODAY
    j["count_type"] = "registered DOIs published from 2024-01-01; not acceptances"
json.dump({"generated": TODAY, "prefix": "10.1088", "publisher": "IOP Publishing", "journals": journals},
          open("data/journals.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

samples = [
    ("Physics in Medicine and Biology", "0031-9155", "10.1088/1361-6560/aebc06", "Artificial intelligence-enabled detection of vascular perfusion defects on ventilation/perfusion (V/Q) scintigraphy for pulmonary embolism"),
    ("Physics in Medicine and Biology", "0031-9155", "10.1088/1361-6560/aec05f", "Dynamic range modulation via integrated universal range shifter and ridge filter: enabling simplified delivery for FLASH-enabled IMPT"),
    ("Physics in Medicine and Biology", "0031-9155", "10.1088/1361-6560/aebfed", "Artificial intelligence for cerebrovascular digital subtraction angiography: methods, evidence, and challenges"),
    ("Physics in Medicine and Biology", "0031-9155", "10.1088/1361-6560/aebf1f", "Review of radiobiological dose rate effects at the edge between conventional and FLASH"),
    ("Physics in Medicine and Biology", "0031-9155", "10.1088/1361-6560/aec081", "Phantom-based evaluation of a novel tomographic ultra-fast molecular breast imaging prototype"),
    ("Reports on Progress in Physics", "0034-4885", "10.1088/1361-6633/aec305", "Twistronics for photonics and phononics"),
    ("Reports on Progress in Physics", "0034-4885", "10.1088/1361-6633/aec02b", "Forces at the scale of the cell"),
    ("Reports on Progress in Physics", "0034-4885", "10.1088/1361-6633/aeb158", "Black hole equations of state and response functions"),
    ("Reports on Progress in Physics", "0034-4885", "10.1088/1361-6633/aeb89e", "Review on physics of Higgs R2 inflation"),
    ("Reports on Progress in Physics", "0034-4885", "10.1088/1361-6633/aebb5f", "Force-decomposition mechanotyping reveals capillary and bulk-viscoelastic regimes in phase-separated condensates"),
    ("Environmental Research Letters", "1748-9326", "10.1088/1748-9326/aebbd6", "Local leakage effects of establishing protected areas in multi-use forests"),
    ("Environmental Research Letters", "1748-9326", "10.1088/1748-9326/aec169", "Carbon cycle feedback dependence on imposed land-use forcing"),
    ("Environmental Research Letters", "1748-9326", "10.1088/1748-9326/aeb9fa", "How government spending relates to eco-social outcomes: a global comparative analysis from 2005 to 2019"),
    ("Environmental Research Letters", "1748-9326", "10.1088/1748-9326/aec57c", "Climate Change Exacerbated the Record-Breaking 2022 and 2025 Fire Weather Episodes in Spain"),
    ("Environmental Research Letters", "1748-9326", "10.1088/1748-9326/aec57d", "A Southern Australian SST Footprint-Related Emergent Constraint Indicates Overestimated Future Summer Precipitation Increase in Southwest China"),
    ("Quantum Science and Technology", "2058-9565", "10.1088/2058-9565/aebfc0", "An iterative Ising decoder for quantum error correction codes"),
    ("Machine Learning: Science and Technology", "2632-2153", "10.1088/2632-2153/aec2a3", "Machine-learned syndrome post-selection for reliable quantum error correction"),
    ("Machine Learning: Science and Technology", "2632-2153", "10.1088/2632-2153/aebff5", "Mitigating numerical stiffness in least-squares formulations of elliptic PDEs for physics-informed neural networks"),
    ("Machine Learning: Science and Technology", "2632-2153", "10.1088/2632-2153/aec061", "Lightweight separation-based multi-event perception for distributed acoustic sensing"),
    ("Machine Learning: Science and Technology", "2632-2153", "10.1088/2632-2153/aec5b9", "Articulating assumptions in AI-generated scientific analyses through task decomposition"),
    ("Machine Learning: Science and Technology", "2632-2153", "10.1088/2632-2153/aec062", "Probabilistic physics-informed neural solvers for Woods-Saxon parameter identification: a coupled forward-inverse approach"),
    ("IOP Conference Series: Materials Science and Engineering", "1757-899X", "10.1088/1757-899x/1351/1/012001", "Experimental research on the flow on a curvilinear slope with applicability to sea waves"),
    ("IOP Conference Series: Materials Science and Engineering", "1757-899X", "10.1088/1757-899x/1351/1/012019", "Barriers and Enablers of Green Logistics in Indian Ports"),
    ("IOP Conference Series: Materials Science and Engineering", "1757-899X", "10.1088/1757-899x/1351/1/012002", "Behavioural Organisation of Vessel Movements in Multi-Layer Corridors"),
    ("IOP Conference Series: Materials Science and Engineering", "1757-899X", "10.1088/1757-899x/1351/1/012007", "Navigating Towards Zero Emissions: Decarbonization Pathways in Maritime Transport"),
    ("IOP Conference Series: Materials Science and Engineering", "1757-899X", "10.1088/1757-899x/1351/1/012011", "Transas NTPro5000 Simulator for Ship Behaviour in Variable Conditions"),
]
with open("data/sample_titles.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["journal", "issn", "doi", "title", "source", "sort_order"])
    for i, (j, s, d, t) in enumerate(samples, 1):
        w.writerow([j, s, d, t, "Crossref REST API, 5 most recent per journal, accessed " + TODAY, i])

timeline = {
    "generated": TODAY,
    "source_pages": ["P06", "P07", "P08", "P09", "P10"],
    "note": "Timings are IOP's stated typical values. Journal-specific median decision times are on journal homepages (not fetched).",
    "stages": [
        {"order": 0, "stage": "Before submitting", "timing": "self-paced", "notes": "choose journal, check scope, run checklist, anonymise if double-anonymous"},
        {"order": 1, "stage": "Submission", "timing": "not stated; no window found", "notes": "confirm on journal page; Preflight tool for Word files"},
        {"order": 2, "stage": "Pre-review quality check", "timing": "not stated", "notes": "possible rejection or transfer offer; 10 days to accept or decline a transfer"},
        {"order": 3, "stage": "Peer review", "timing": "journal-specific median (on homepage)", "notes": "usually two reviewers; adjudicator if they disagree; extensions possible"},
        {"order": 4, "stage": "First decision", "timing": "email on decision", "notes": "provisional accept, minor/moderate/major revision, reject (resubmit possible), reject, transfer offer"},
        {"order": "5a", "stage": "Revision", "timing": {"minor": "1-2 weeks", "moderate": "2-4 weeks", "major": "4-8 weeks"}, "notes": "point-by-point response; copyright form and permissions required"},
        {"order": "5b", "stage": "Formal acceptance", "timing": "not stated", "notes": "requires signed copyright form"},
        {"order": 6, "stage": "Accepted manuscript online", "timing": "within 24 hours (most journals, optional)", "notes": ""},
        {"order": 7, "stage": "Proofs", "timing": "published about 1 week after corrections arrive", "notes": "author responsible for accuracy"},
        {"order": 8, "stage": "Version of Record published", "timing": "about 1 week after proof corrections", "notes": ""},
        {"order": 9, "stage": "After publication", "timing": "ongoing", "notes": "repository deposit usually after 12-month embargo; corrigendum process"},
    ],
    "key_facts": {
        "rejection_rate": "most journals typically above 50% (IOP review page)",
        "resubmission": "article rejected in same or substantially similar form generally not reconsidered by IOP primary journals",
    },
}
json.dump(timeline, open("data/timeline.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

reqs = {
    "generated": TODAY,
    "source_pages": ["P02", "P03", "P25", "P30", "P08"],
    "submission_checklist": [
        "fits aims and scope", "article type known", "full PDF prepared",
        "peer review model known (single vs double anonymous)", "clear abstract",
        "co-author details and ORCID iDs (if fewer than 20 co-authors)", "references per style guide",
        "third-party material cited; permissions before acceptance", "supplementary material ready",
        "ethics statement and journal ethics policy met", "research data policy considered", "ORCID iD",
    ],
    "journal_choice_factors": [
        "peer review quality", "relevance and audience", "scope", "article types (Letter vs Paper)",
        "reputation", "indexing (Web of Science, Scopus; 'Abstracted in' on journal page)", "language",
        "cost (APCs, colour figures)", "open access vs subscription",
    ],
    "open_access": {
        "gold": "CC-BY; authors keep copyright",
        "green": "accepted version archivable in subscription journals (rules on overview page, not fully read)",
        "transformative_agreements": "hub on publishingsupport; IOPP Journal Finder checks eligibility",
    },
    "copyright": {
        "hybrid_subscription": "author transfers copyright to IOP",
        "fully_gold_oa": "author grants non-exclusive licence to IOP",
        "effect": "only from acceptance date",
    },
    "tools": ["Preflight (pre-submission, Word files)", "IOPP Journal Finder", "transfer service"],
    "unverified": ["APC amounts", "submission window", "journal scope pages (not fetched)"],
}
json.dump(reqs, open("data/requirements.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

sources = [
    {"id": "S1", "name": "IOP publishing-support pages (author, reviewer, OA, policies)",
     "url": "https://publishingsupport.iopscience.iop.org/", "robots": "allows all (Disallow empty for *)",
     "method": "polite fetch, 2s delay", "status": "used"},
    {"id": "S2", "name": "IOP legal and about pages", "url": "https://ioppublishing.org/",
     "robots": "allows except /info/, /wp-admin/, /wp-login.php; crawl-delay 600s",
     "method": "polite fetch", "status": "used"},
    {"id": "S3", "name": "IOPscience About and Terms", "url": "https://iopscience.iop.org/page/aboutiopscience",
     "robots": "Disallow / for generic crawlers", "method": "two pages read, not crawled; terms prohibit systematic downloading",
     "status": "read only"},
    {"id": "S4", "name": "Crossref REST API", "url": "https://api.crossref.org/", "robots": "public metadata API",
     "method": "counts and 5 most recent titles per journal", "status": "used"},
]
json.dump({"generated": TODAY, "sources": sources}, open("data/sources.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

print("ok", len(index), len(journals), len(samples))
