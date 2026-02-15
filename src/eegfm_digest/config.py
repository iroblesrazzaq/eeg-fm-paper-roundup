from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Config:
    gemini_model_triage: str
    gemini_model_summary: str
    arxiv_rate_limit_seconds: float = 2.0
    pdf_rate_limit_seconds: float = 5.0
    output_dir: str = "outputs"
    data_dir: str = "data"
    max_candidates: int = 500
    max_accepted: int = 80
    include_borderline: bool = False
    max_borderline_pdfs: int = 20
    text_head_chars: int = 80_000
    text_tail_chars: int = 20_000

def load_config() -> Config:
    triage = os.environ.get("GEMINI_MODEL_TRIAGE", "gemini-2.0-flash")
    summary = os.environ.get("GEMINI_MODEL_SUMMARY", "gemini-2.0-pro")
    return Config(gemini_model_triage=triage, gemini_model_summary=summary)
