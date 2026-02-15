import argparse
from datetime import date
from dateutil.relativedelta import relativedelta

from .config import load_config
from .pipeline import run_month

def default_month() -> str:
    # previous calendar month
    first = date.today().replace(day=1)
    prev = first - relativedelta(months=1)
    return f"{prev.year:04d}-{prev.month:02d}"

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--month", default=default_month(), help="YYYY-MM (default: previous month)")
    p.add_argument("--max-candidates", type=int, default=None)
    p.add_argument("--max-accepted", type=int, default=None)
    p.add_argument("--include-borderline", action="store_true")
    p.add_argument("--no-pdf", action="store_true")
    p.add_argument("--force", action="store_true")
    args = p.parse_args()

    cfg = load_config()
    if args.max_candidates is not None:
        cfg = cfg.__class__(**{**cfg.__dict__, "max_candidates": args.max_candidates})
    if args.max_accepted is not None:
        cfg = cfg.__class__(**{**cfg.__dict__, "max_accepted": args.max_accepted})
    if args.include_borderline:
        cfg = cfg.__class__(**{**cfg.__dict__, "include_borderline": True})

    run_month(cfg, args.month, no_pdf=args.no_pdf, force=args.force)

if __name__ == "__main__":
    main()
