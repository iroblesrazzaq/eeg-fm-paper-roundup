# EEG FM Digest

Monthly arXiv-based digest for EEG Foundation Model papers:
1) Stage 1: keyword retrieval (title+abstract) within relevant arXiv categories
2) Stage 2: Gemini triage on abstract
3) Stage 3: PDF download + text extraction + Gemini deep summary
4) Publish: static site in /docs with one page per month

## Setup
```bash
pip install -e ".[dev]"
export GEMINI_API_KEY="..."
export GEMINI_MODEL_TRIAGE="gemini-flash-lite-lastest"
export GEMINI_MODEL_SUMMARY="gemini-3-flash-preview"
