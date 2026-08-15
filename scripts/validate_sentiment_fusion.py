"""Validate precomputed Stage 6C sentiment and fusion outputs without rerunning models."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.validate_data_contract import build_pipeline  # noqa: E402
from src import data_access  # noqa: E402
from src.portfolios import build_family_return_matrices  # noqa: E402
from src.sentiment import create_vader_analyzers  # noqa: E402
from src.sentiment_validation import validate_sentiment_fusion_outputs  # noqa: E402
from src.validation import ValidationResult  # noqa: E402


PATHS = {
    "sector_sentiment_index": PROJECT_ROOT / "results/data/sector_sentiment_index.csv",
    "ticker_sentiment_daily": PROJECT_ROOT / "results/data/ticker_sentiment_daily.csv",
    "fusion_returns": PROJECT_ROOT / "results/data/fusion_returns.csv",
    "fusion_weights": PROJECT_ROOT / "results/data/fusion_weights.csv",
    "sentiment_diagnostics": PROJECT_ROOT / "results/tables/sentiment_diagnostics.csv",
    "finance_lexicon": PROJECT_ROOT / "results/tables/finance_lexicon.csv",
    "fusion_performance_metrics": PROJECT_ROOT / "results/tables/fusion_performance_metrics.csv",
    "fusion_comparison": PROJECT_ROOT / "results/tables/fusion_comparison.csv",
    "base_returns": PROJECT_ROOT / "results/data/fund_returns.csv",
    "base_weights": PROJECT_ROOT / "results/data/fund_weights.csv",
    "base_performance": PROJECT_ROOT / "results/tables/performance_metrics.csv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print the complete validation report as JSON.")
    return parser.parse_args()


def _read_outputs() -> dict[str, pd.DataFrame]:
    date_columns = {
        "sector_sentiment_index": ["date"],
        "ticker_sentiment_daily": ["date", "signal_source_date"],
        "fusion_returns": ["date"],
        "fusion_weights": ["date", "signal_source_date"],
        "sentiment_diagnostics": ["start_date", "end_date"],
        "finance_lexicon": ["decision_date"],
        "fusion_performance_metrics": ["start_date", "end_date"],
        "fusion_comparison": [],
        "base_returns": ["date"],
        "base_weights": ["date"],
        "base_performance": ["start_date", "end_date"],
    }
    frames = {
        name: pd.read_csv(path, parse_dates=date_columns[name])
        for name, path in PATHS.items()
    }
    for frame_name, column in (
        ("ticker_sentiment_daily", "has_news"),
        ("fusion_returns", "is_rebalance"),
        ("fusion_weights", "projection_success"),
        ("base_returns", "is_rebalance"),
    ):
        frames[frame_name][column] = frames[frame_name][column].astype(bool)
    return frames


def main() -> int:
    args = parse_args()
    try:
        frames = _read_outputs()
        raw_equity = data_access.load_equity_prices()
        raw_crypto = data_access.load_crypto_prices()
        raw_news = data_access.load_news_headlines()
        pipeline = build_pipeline(raw_equity, raw_crypto, raw_news)
        matrices = build_family_return_matrices(
            pipeline["equity_returns"], pipeline["crypto_returns"], pipeline["aligned_crypto"]
        )
        plain, _ = create_vader_analyzers()
        snapshot = dict(plain.lexicon)
        create_vader_analyzers()
        plain_unchanged = plain.lexicon == snapshot
        report = validate_sentiment_fusion_outputs(
            sector_sentiment_index=frames["sector_sentiment_index"],
            ticker_sentiment_daily=frames["ticker_sentiment_daily"],
            fusion_returns=frames["fusion_returns"],
            fusion_weights=frames["fusion_weights"],
            sentiment_diagnostics=frames["sentiment_diagnostics"],
            finance_lexicon=frames["finance_lexicon"],
            fusion_performance_metrics=frames["fusion_performance_metrics"],
            fusion_comparison=frames["fusion_comparison"],
            base_returns=frames["base_returns"],
            base_weights=frames["base_weights"],
            base_performance=frames["base_performance"],
            family_matrices=matrices,
            plain_analyzer_unchanged=plain_unchanged,
        )
    except Exception as exc:
        failure = ValidationResult(
            code="sentiment_fusion_validation_execution",
            level="BLOCK",
            message=f"Validation execution failed: {type(exc).__name__}: {exc}",
        )
        payload = {
            "status": "BLOCK",
            "summary": {"PASS": 0, "WARN": 0, "BLOCK": 1},
            "results": [failure.to_dict()],
        }
        if args.json:
            print(json.dumps(payload, indent=2, default=str))
        else:
            print("Sentiment/fusion output validation: PASS=0 WARN=0 BLOCK=1")
            print(f"BLOCK {failure.code}: {failure.message}")
        return 1

    payload = report.to_dict()
    if args.json:
        print(json.dumps(payload, indent=2, default=str))
    else:
        summary = payload["summary"]
        print(
            "Sentiment/fusion output validation: "
            f"PASS={summary['PASS']} WARN={summary['WARN']} BLOCK={summary['BLOCK']}"
        )
        for result in report.results:
            if result.level != "PASS":
                print(f"{result.level} {result.code}: {result.message}")
        print(f"SENTIMENT/FUSION OUTPUT STATUS: {'PASS' if report.ok else 'BLOCK'}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
