"""Validate the frozen Project B input contract without writing artifacts."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src import data_access  # noqa: E402
from src.etl import (  # noqa: E402
    clean_crypto_prices,
    clean_equity_prices,
    clean_news_headlines,
)
from src.features import (  # noqa: E402
    align_crypto_returns_to_equity_calendar,
    build_combined_return_matrix,
    build_complete_headline_panel,
    build_equity_returns,
    build_mapped_headline_table,
    build_native_crypto_returns,
    equity_trading_calendar,
    map_headlines_to_equity_calendar,
)
from src.validation import (  # noqa: E402
    ValidationResult,
    validate_data_foundation,
    validate_deterministic_rerun,
)


def build_pipeline(raw_equity, raw_crypto, raw_news):
    """Run the authorised in-memory data-foundation pipeline."""
    equity = clean_equity_prices(raw_equity)
    crypto = clean_crypto_prices(raw_crypto)
    news = clean_news_headlines(raw_news)
    equity_returns = build_equity_returns(equity)
    crypto_returns = build_native_crypto_returns(crypto)
    calendar = equity_trading_calendar(equity)
    aligned_crypto = align_crypto_returns_to_equity_calendar(crypto_returns, calendar)
    combined_returns = build_combined_return_matrix(equity_returns, aligned_crypto)
    full_mapping = map_headlines_to_equity_calendar(news, calendar)
    mapped_headlines = build_mapped_headline_table(full_mapping)
    coverage_panel = build_complete_headline_panel(mapped_headlines, equity)
    return {
        "equity": equity,
        "crypto": crypto,
        "news": news,
        "equity_returns": equity_returns,
        "crypto_returns": crypto_returns,
        "aligned_crypto": aligned_crypto,
        "combined_returns": combined_returns,
        "full_mapping": full_mapping,
        "mapped_headlines": mapped_headlines,
        "coverage_panel": coverage_panel,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the complete machine-readable validation report as JSON.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        raw_equity = data_access.load_equity_prices()
        raw_crypto = data_access.load_crypto_prices()
        raw_news = data_access.load_news_headlines()
        first = build_pipeline(raw_equity, raw_crypto, raw_news)
        second = build_pipeline(raw_equity, raw_crypto, raw_news)
        report = validate_data_foundation(
            project_root=PROJECT_ROOT,
            loader_path=Path(data_access.__file__),
            raw_equity=raw_equity,
            raw_crypto=raw_crypto,
            raw_news=raw_news,
            **first,
        )
        rerun = validate_deterministic_rerun(first, second)
        report.results.append(rerun)
    except Exception as exc:  # deterministic command boundary
        failure = ValidationResult(
            code="pipeline_execution",
            level="BLOCK",
            message=f"Pipeline execution failed: {type(exc).__name__}: {exc}",
        )
        payload = {
            "status": "BLOCK",
            "summary": {"PASS": 0, "WARN": 0, "BLOCK": 1},
            "results": [failure.to_dict()],
        }
        if args.json:
            print(json.dumps(payload, indent=2, default=str))
        else:
            print("Data contract validation: PASS=0 WARN=0 BLOCK=1")
            print(f"BLOCK {failure.code}: {failure.message}")
        return 1

    payload = report.to_dict()
    if args.json:
        print(json.dumps(payload, indent=2, default=str))
    else:
        summary = payload["summary"]
        print(
            "Data contract validation: "
            f"PASS={summary['PASS']} WARN={summary['WARN']} BLOCK={summary['BLOCK']}"
        )
        for result in report.results:
            if result.level != "PASS":
                print(f"{result.level} {result.code}: {result.message}")
        print("CONTRACT STATUS: PASS" if report.ok else "CONTRACT STATUS: BLOCK")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
