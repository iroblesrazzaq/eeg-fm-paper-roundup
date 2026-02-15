# SPEC.md

## 1) Product definition
Monthly “EEG Foundation Model” paper digest from arXiv.

Outputs per month `YYYY-MM`:
- `outputs/YYYY-MM/digest.md`
- `outputs/YYYY-MM/digest.json`
- `outputs/YYYY-MM/papers.jsonl` (one JSON summary per paper)
- `outputs/YYYY-MM/arxiv_raw.json` (raw fetched candidates)
- `data/digest.sqlite` (history + incremental state)

## 2) What “tags” mean on arXiv
arXiv does not have freeform tags like social media.
What we can filter by from arXiv:
- subject categories (primary + cross-lists), e.g. `cs.LG`, `q-bio.NC`, `eess.SP`
- text fields: title, abstract, comments, journal-ref, DOI

We will also generate our own `digest_tags` (e.g., masking, recon, adapter) during triage/summarize for organization.

## 3) Candidate retrieval

### 3.1 Categories (recall net)
Include papers whose category list intersects:
- q-bio.NC
- cs.LG
- stat.ML
- eess.SP
- cs.AI
- cs.NE (optional)

### 3.2 Query strategy (keep it simple)
Use 2 arXiv searches and union results:
- Query A: EEG/BCI terms
- Query B: foundation/pretraining terms AND EEG terms

Implementation notes:
- arXiv API returns Atom XML; parse entries.
- Use pagination: `start`, `max_results`.
- Filter *by published date* within month window:
  - `[YYYY-MM-01, next_month-01)`

### 3.3 Dedupe
- Canonical key: `arxiv_id_base` (strip version suffix `vN`)
- Store latest metadata but keep base key stable.

## 4) LLM stages (runtime behavior)

### 4.1 Triage (title+abstract only)
Goal: decide if paper should be full-text processed.

Input:
- arxiv_id, title, authors, categories, published, abstract

Output: `TriageDecision` JSON (validated)
Fields:
- `is_eeg_related` (bool)
- `is_foundation_model_related` (bool)
- `paper_type` enum
- `confidence` float 0..1
- `needs_fulltext` bool
- `reasons` list[str]
- `suggested_tags` list[str]

Rule:
- If uncertain but potentially relevant, set `needs_fulltext=true`.

### 4.2 Full-text acquisition (shortlist only)
For papers passing:
- `(is_eeg_related && is_foundation_model_related) OR needs_fulltext`

Steps:
- download PDF to `outputs/YYYY-MM/pdfs/{arxiv_id_base}.pdf`
- extract text to `outputs/YYYY-MM/text/{arxiv_id_base}.txt`
- extraction tool: `pypdf` (preferred) with fallback to `pdfminer.six`
- store extraction metadata:
  - page_count, char_count, errors

Do not block the run on extraction failure.

### 4.3 Summarization (full text when available)
Input:
- metadata + abstract + extracted text (or abstract-only if extraction failed)

Output: `PaperSummary` JSON (validated)
Required highlights:
- `one_liner`
- `unique_contribution`
- data scale fields when present (datasets, subjects, eeg_hours, channels)
- evaluation tasks/benchmarks
- open-source links if mentioned in text

Must not invent facts; use `null`/`unknown` if absent.

### 4.4 Digest rendering (deterministic)
Group papers by `paper_type`.
Create:
- Top picks (<=5) via heuristic scoring:
  - confidence + presence of concrete scale/eval + novelty phrasing length
Render Markdown cards:
- Title link
- one_liner
- **Unique contribution**
- key points
- tags
- code/weights links if any

Write digest.md + digest.json.

## 5) Persistence (SQLite)
Tables:
- papers(arxiv_id_base PK, arxiv_id_latest, title, authors_json, abstract, published, updated, categories_json, pdf_url, abs_url, extra_json)
- triage(arxiv_id_base PK, decision_json, created_at, model_id)
- summaries(arxiv_id_base PK, summary_json, created_at, model_id, had_fulltext, extraction_status)
- runs(month PK, created_at, query_json, stats_json)

## 6) CLI
`python -m eegfm_digest.run --month YYYY-MM [--max-candidates N] [--max-shortlist N] [--no-pdfs]`

## 7) Rate limiting
- arXiv API requests: sleep >= 2s between calls
- PDF downloads: sleep >= 5s between downloads

## 8) Error handling
- If LLM JSON invalid: attempt one repair prompt; else mark error + continue
- If PDF download/extraction fails: store error + summarize from abstract only

## 9) Tests
- Unit tests for parsing, date filtering, dedupe, schema validation, rendering
- Golden test: fixed summaries -> snapshot digest.md
