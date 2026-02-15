# Codex: implement run_month() by wiring:
# 1) arXiv fetch -> outputs/YYYY-MM/arxiv_raw.json
# 2) triage -> outputs/YYYY-MM/triage.jsonl + DB
# 3) pdf download + extract + summarize -> outputs/YYYY-MM/papers.jsonl + DB
# 4) digest.json + docs site generation (index.html + month page)
from .config import Config

def run_month(cfg: Config, month: str, no_pdf: bool = False, force: bool = False) -> None:
    raise NotImplementedError
