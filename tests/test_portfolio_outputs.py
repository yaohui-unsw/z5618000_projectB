"""Real-output reconciliation tests for the authorised Stage 5A artifacts."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src import data_access
from src.etl import clean_crypto_prices, clean_equity_prices
from src.features import (
    align_crypto_returns_to_equity_calendar,
    build_equity_returns,
    build_native_crypto_returns,
    equity_trading_calendar,
)
from src.portfolio_validation import (
    FUND_RETURN_COLUMNS,
    FUND_WEIGHT_COLUMNS,
    PERFORMANCE_METRIC_COLUMNS,
    SENSITIVITY_COLUMNS,
    validate_portfolio_outputs,
)
from src.portfolios import FUND_IDS, FUND_SPECS, build_family_return_matrices


ROOT = Path(__file__).resolve().parents[1]


def _load_outputs() -> dict[str, pd.DataFrame]:
    return {
        "fund_returns": pd.read_csv(ROOT / "results/data/fund_returns.csv", parse_dates=["date"]),
        "fund_weights": pd.read_csv(ROOT / "results/data/fund_weights.csv", parse_dates=["date"]),
        "performance_metrics": pd.read_csv(ROOT / "results/tables/performance_metrics.csv", parse_dates=["start_date", "end_date"]),
        "solver_diagnostics": pd.read_csv(ROOT / "results/tables/portfolio_solver_diagnostics.csv", parse_dates=["date"]),
        "sensitivity_metrics": pd.read_csv(ROOT / "results/tables/extreme_sensitivity_metrics.csv"),
    }


def _source_matrices() -> dict[str, pd.DataFrame]:
    equity = clean_equity_prices(data_access.load_equity_prices())
    crypto = clean_crypto_prices(data_access.load_crypto_prices())
    equity_returns = build_equity_returns(equity)
    crypto_returns = build_native_crypto_returns(crypto)
    aligned = align_crypto_returns_to_equity_calendar(
        crypto_returns, equity_trading_calendar(equity)
    )
    return build_family_return_matrices(equity_returns, crypto_returns, aligned)


def _monthly_dates(matrix: pd.DataFrame, window: int) -> list[pd.Timestamp]:
    complete = matrix.loc[matrix.notna().all(axis=1)].sort_index()
    dates: list[pd.Timestamp] = []
    seen = None
    for date in complete.index[window:]:
        month = date.to_period("M")
        if month != seen:
            dates.append(pd.Timestamp(date))
            seen = month
    return dates


def test_real_outputs_pass_source_reconciliation_and_contract():
    outputs = _load_outputs()
    matrices = _source_matrices()
    report = validate_portfolio_outputs(
        **outputs, family_matrices=matrices, require_sensitivity=True
    )
    assert report.blocks == []


def test_output_schemas_ids_keys_and_substantive_row_counts():
    outputs = _load_outputs()
    returns = outputs["fund_returns"]
    weights = outputs["fund_weights"]
    metrics = outputs["performance_metrics"]
    sensitivity = outputs["sensitivity_metrics"]
    diagnostics = outputs["solver_diagnostics"]
    assert tuple(returns.columns) == FUND_RETURN_COLUMNS
    assert tuple(weights.columns) == FUND_WEIGHT_COLUMNS
    assert tuple(metrics.columns) == PERFORMANCE_METRIC_COLUMNS
    assert tuple(sensitivity.columns) == SENSITIVITY_COLUMNS
    assert tuple(metrics["fund_id"]) == FUND_IDS
    assert tuple(sensitivity["fund_id"]) == FUND_IDS
    assert not returns.duplicated(["date", "fund_id"]).any()
    assert not weights.duplicated(["date", "fund_id", "ticker"]).any()
    assert not diagnostics.duplicated(["date", "fund_id"]).any()

    matrices = _source_matrices()
    expected_returns = 0
    expected_weights = 0
    expected_diagnostics = 0
    for spec in FUND_SPECS:
        matrix = matrices[spec.family]
        complete = matrix.loc[matrix.notna().all(axis=1)]
        schedule = _monthly_dates(matrix, spec.window)
        expected_returns += len(complete.loc[complete.index >= schedule[0]])
        expected_weights += len(schedule) * len(spec.assets)
        expected_diagnostics += len(schedule)
    assert len(returns) == expected_returns
    assert len(weights) == expected_weights
    assert len(diagnostics) == expected_diagnostics
    assert len(metrics) == len(sensitivity) == 12


def test_constraints_calendars_first_live_dates_and_extreme_retention():
    outputs = _load_outputs()
    matrices = _source_matrices()
    weights = outputs["fund_weights"]
    assert weights["target_weight"].min() >= -1e-8
    assert weights["target_weight"].max() <= 0.20 + 1e-8
    sums = weights.groupby(["date", "fund_id"])["target_weight"].sum()
    np.testing.assert_allclose(sums, 1.0, rtol=0, atol=1e-8)

    metrics = outputs["performance_metrics"].set_index("fund_id")
    for spec in FUND_SPECS:
        schedule = _monthly_dates(matrices[spec.family], spec.window)
        assert pd.Timestamp(metrics.loc[spec.fund_id, "start_date"]) == schedule[0]
        assert int(metrics.loc[spec.fund_id, "annualisation"]) == spec.annualisation
    assert int(matrices["Equity"].abs().ge(0.25).sum().sum()) == 4
    assert int(matrices["Crypto"].abs().ge(0.25).sum().sum()) == 65


def test_sensitivity_is_separate_and_deltas_reconcile():
    outputs = _load_outputs()
    sensitivity = outputs["sensitivity_metrics"]
    assert np.isfinite(sensitivity.loc[:, list(SENSITIVITY_COLUMNS[3:])]).all().all()
    np.testing.assert_allclose(
        sensitivity["delta_net_annualised_return"],
        sensitivity["sensitivity_net_annualised_return"] - sensitivity["canonical_net_annualised_return"],
        rtol=0, atol=5e-12,
    )
    np.testing.assert_allclose(
        sensitivity["delta_net_sharpe_ratio"],
        sensitivity["sensitivity_net_sharpe_ratio"] - sensitivity["canonical_net_sharpe_ratio"],
        rtol=0, atol=5e-12,
    )
    np.testing.assert_allclose(
        sensitivity["delta_net_max_drawdown"],
        sensitivity["sensitivity_net_max_drawdown"] - sensitivity["canonical_net_max_drawdown"],
        rtol=0, atol=5e-12,
    )
    assert sensitivity.loc[:, [column for column in sensitivity if column.startswith("delta_")]].abs().to_numpy().max() > 0
