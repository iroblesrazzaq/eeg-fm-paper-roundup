# AGENTS.md
# Repository instructions for Codex (development-time), NOT runtime LLM “agents”.

## Project goal
Implement a monthly pipeline that:
1) queries arXiv for candidate EEG foundation-model-ish papers,
2) triages candidates with an LLM using title+abstract,
3) fetches PDFs only for triaged-in papers,
4) extracts text deterministically,
5) summarizes and writes a monthly digest (Markdown + JSON),
6) stores state in SQLite for incremental runs.

## Operating rules
- Prefer simple, testable Python over clever abstractions.
- Keep network access minimal:
  - arXiv API calls are allowed.
  - PDF downloads only for shortlisted papers.
- Do not hardcode secrets. Read API keys from environment variables.
- Every LLM call must return strict JSON validated by a schema.
- If anything fails (PDF extraction, JSON parse), log and continue; never crash the whole run.

## Dev environment
- Python: 3.11+
- Package manager: uv (preferred) or pip
- Main entrypoint: `python -m eegfm_digest.run --month YYYY-MM`

## Setup commands
- Create venv + install:
  - `python -m venv .venv && source .venv/bin/activate`
  - `pip install -e .`
- Run tests:
  - `pytest -q`
- Format/lint (if configured):
  - `ruff check .`
  - `ruff format .`

## Repository layout (expected)
- `src/eegfm_digest/` — library code
- `src/eegfm_digest/run.py` — CLI pipeline runner
- `prompts/` — prompt templates (triage, summarize, repair)
- `schemas/` — JSON schemas (triage.json, summary.json, digest.json)
- `tests/` — unit + golden tests
- `data/` — sqlite db
- `outputs/YYYY-MM/` — run artifacts

## Implementation priorities
1) Correct arXiv fetching + month filtering + dedupe by base arXiv id.
2) Robust JSON-schema validation for LLM outputs.
3) Staged PDF download/extraction with caching.
4) Deterministic digest rendering.

## Testing expectations
- Unit tests for:
  - arXiv Atom parsing
  - month window boundaries
  - dedupe/version handling
  - schema validation failure paths
- Golden test:
  - render digest from a fixed fixture set of summaries and compare to snapshot.

## Git hygiene
- Do not commit large PDFs by default. Store extracted text + metadata.
- Commit `outputs/YYYY-MM/digest.md` and `digest.json`.
- Use `.gitignore` for `outputs/**/pdfs/` unless explicitly requested.

## Notes
- arXiv API: `export.arxiv.org/api/query` (Atom).
- Rate limit politely (sleep between requests).
