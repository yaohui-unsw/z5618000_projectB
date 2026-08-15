"""Real-output contract tests for all eight canonical Stage 6C artifacts."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pandas as pd

from scripts.validate_data_contract import build_pipeline
from src import data_access
from src.fusion import OVERLAY_IDS
from src.portfolios import build_family_return_matrices
from src.sentiment import FINANCE_LEXICON, REJECTED_TERMS, create_vader_analyzers
from src.sentiment_validation import EXPECTED_ROWS, validate_sentiment_fusion_outputs


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATHS = {
    "sector_sentiment_index": ROOT / "results/data/sector_sentiment_index.csv",
    "ticker_sentiment_daily": ROOT / "results/data/ticker_sentiment_daily.csv",
    "fusion_returns": ROOT / "results/data/fusion_returns.csv",
    "fusion_weights": ROOT / "results/data/fusion_weights.csv",
    "sentiment_diagnostics": ROOT / "results/tables/sentiment_diagnostics.csv",
    "finance_lexicon": ROOT / "results/tables/finance_lexicon.csv",
    "fusion_performance_metrics": ROOT / "results/tables/fusion_performance_metrics.csv",
    "fusion_comparison": ROOT / "results/tables/fusion_comparison.csv",
}
PORTFOLIO_HASHES = {
    "results/data/fund_returns.csv": "7C0DB5C36F7E6CF6F054580980FA5527C812C67F9C57F47039B3B518718B6C84",
    "results/data/fund_weights.csv": "F31A7B91A3B3CE7BE770C41597F2551913B93F6D3DDE4DCE27EC2B68E5DD53C8",
    "results/tables/performance_metrics.csv": "5719558A3D1D059137513BE0A4748BB3E1877D3956BDCFF92B095AB3B2BE2D19",
    "results/tables/portfolio_solver_diagnostics.csv": "ED837EC8E7BDF0E0356267ABA372D793B33621A102B40C1B3841981CB6F1B27C",
    "results/tables/extreme_sensitivity_metrics.csv": "40E91E876813EF6F493C9C165C0D594D6DA6901FEC8B46ECA4D05F55E5BCE151",
}


def _hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest().upper()


def _read() -> dict[str, pd.DataFrame]:
    date_columns = {
        "sector_sentiment_index": ["date"],
        "ticker_sentiment_daily": ["date", "signal_source_date"],
        "fusion_returns": ["date"],
        "fusion_weights": ["date", "signal_source_date"],
        "sentiment_diagnostics": ["start_date", "end_date"],
        "finance_lexicon": ["decision_date"],
        "fusion_performance_metrics": ["start_date", "end_date"],
        "fusion_comparison": [],
    }
    return {
        name: pd.read_csv(path, parse_dates=date_columns[name])
        for name, path in OUTPUT_PATHS.items()
    }


def test_exact_eight_outputs_rows_keys_and_operational_lexicon():
    assert all(path.is_file() and path.stat().st_size > 0 for path in OUTPUT_PATHS.values())
    frames = _read()
    for name, expected in EXPECTED_ROWS.items():
        assert len(frames[name]) == expected
    lexicon = frames["finance_lexicon"].set_index("term")
    assert set(lexicon.index) == set(FINANCE_LEXICON)
    assert REJECTED_TERMS.isdisjoint(lexicon.index)
    for term, value in FINANCE_LEXICON.items():
        assert lexicon.loc[term, "approved_finance_value"] == value
    assert tuple(frames["fusion_performance_metrics"]["overlay_id"]) == OVERLAY_IDS
    assert set(frames["fusion_comparison"]["overlay_id"]) == set(OVERLAY_IDS)
    assert not frames["ticker_sentiment_daily"].duplicated(["date", "ticker"]).any()
    assert not frames["sector_sentiment_index"].duplicated(["date", "sector"]).any()
    assert not frames["fusion_returns"].duplicated(["date", "overlay_id"]).any()
    assert not frames["fusion_weights"].duplicated(["date", "overlay_id", "ticker"]).any()


def test_existing_portfolio_inputs_remain_byte_identical():
    for relative, expected in PORTFOLIO_HASHES.items():
        assert _hash(ROOT / relative) == expected


def test_real_outputs_pass_full_source_reconciliation():
    frames = _read()
    base_returns = pd.read_csv(ROOT / "results/data/fund_returns.csv", parse_dates=["date"])
    base_weights = pd.read_csv(ROOT / "results/data/fund_weights.csv", parse_dates=["date"])
    base_performance = pd.read_csv(ROOT / "results/tables/performance_metrics.csv", parse_dates=["start_date", "end_date"])
    pipeline = build_pipeline(
        data_access.load_equity_prices(),
        data_access.load_crypto_prices(),
        data_access.load_news_headlines(),
    )
    matrices = build_family_return_matrices(
        pipeline["equity_returns"], pipeline["crypto_returns"], pipeline["aligned_crypto"]
    )
    plain, _ = create_vader_analyzers()
    snapshot = dict(plain.lexicon)
    create_vader_analyzers()
    report = validate_sentiment_fusion_outputs(
        **frames,
        base_returns=base_returns,
        base_weights=base_weights,
        base_performance=base_performance,
        family_matrices=matrices,
        plain_analyzer_unchanged=plain.lexicon == snapshot,
    )
    assert report.ok, report.to_dict()
