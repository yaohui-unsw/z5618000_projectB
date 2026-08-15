"""Independent synthetic tests for the frozen portfolio specification."""
from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from src.portfolios import (
    FUND_IDS,
    FUND_SPECS,
    FundSpec,
    PortfolioBlockError,
    drift_weights,
    monthly_rebalance_dates,
    negative_sharpe_objective,
    performance_metrics,
    rolling_estimation_window,
    run_fund_backtest,
    solve_target_weights,
)


EXPECTED_FUNDS = (
    "equity_equal_weight",
    "equity_minimum_variance",
    "equity_maximum_sharpe",
    "equity_risk_parity",
    "crypto_equal_weight",
    "crypto_minimum_variance",
    "crypto_maximum_sharpe",
    "crypto_risk_parity",
    "combined_equal_weight",
    "combined_minimum_variance",
    "combined_maximum_sharpe",
    "combined_risk_parity",
)


def _diagonal_sample(scales: np.ndarray, means: np.ndarray | None = None) -> pd.DataFrame:
    number_assets = len(scales)
    values = np.zeros((2 * number_assets, number_assets), dtype="float64")
    for index, scale in enumerate(scales):
        values[2 * index, index] = scale
        values[2 * index + 1, index] = -scale
    if means is not None:
        values += means
    return pd.DataFrame(values, columns=[f"A{i}" for i in range(number_assets)])


def test_exact_fund_universe_calendars_and_order():
    assert FUND_IDS == EXPECTED_FUNDS
    assert [spec.annualisation for spec in FUND_SPECS[:4]] == [252] * 4
    assert [spec.annualisation for spec in FUND_SPECS[4:8]] == [365] * 4
    assert [spec.annualisation for spec in FUND_SPECS[8:]] == [252] * 4
    assert [spec.window for spec in FUND_SPECS[:4]] == [252] * 4
    assert [spec.window for spec in FUND_SPECS[4:8]] == [365] * 4


def test_strict_window_and_first_eligible_monthly_dates():
    dates = pd.bdate_range("2023-01-02", periods=45)
    returns = pd.DataFrame(0.001, index=dates, columns=[f"A{i}" for i in range(5)])
    schedule = monthly_rebalance_dates(returns, 10)
    assert schedule[0] == dates[10]
    assert all(date == min(d for d in dates[10:] if d.to_period("M") == date.to_period("M")) for date in schedule)
    window = rolling_estimation_window(returns, schedule[0], 10)
    assert tuple(window.index) == tuple(dates[:10])
    assert window.index.max() < schedule[0]


def test_minimum_variance_matches_independent_diagonal_solution():
    scales = np.linspace(1.0, 1.15, 10)
    sample = _diagonal_sample(scales)
    weights, diagnostic = solve_target_weights(sample, "minimum_variance", 252)
    covariance = np.cov(sample.to_numpy(), rowvar=False, ddof=1) * 252
    expected = (1.0 / np.diag(covariance))
    expected /= expected.sum()
    assert expected.max() < 0.20
    np.testing.assert_allclose(weights, expected, atol=2e-6, rtol=0)
    assert diagnostic["solver_success"] is True
    assert abs(weights.sum() - 1.0) <= 1e-8


def test_risk_parity_matches_diagonal_risk_budget_solution():
    scales = np.linspace(1.0, 1.15, 10)
    sample = _diagonal_sample(scales)
    weights, _ = solve_target_weights(sample, "risk_parity", 252)
    expected = 1.0 / scales
    expected /= expected.sum()
    np.testing.assert_allclose(weights, expected, atol=3e-6, rtol=0)


def test_maximum_sharpe_improves_controlled_objective_and_is_feasible():
    scales = np.linspace(1.0, 1.1, 10)
    means = np.linspace(0.010, 0.012, 10)
    sample = _diagonal_sample(scales, means)
    weights, _ = solve_target_weights(sample, "maximum_sharpe", 252)
    mean = sample.mean().to_numpy() * 252
    covariance = np.cov(sample.to_numpy(), rowvar=False, ddof=1) * 252
    equal = np.full(10, 0.1)
    assert negative_sharpe_objective(weights, mean, covariance) <= negative_sharpe_objective(equal, mean, covariance) + 1e-10
    assert weights.min() >= -1e-8
    assert weights.max() <= 0.20 + 1e-8
    assert abs(weights.sum() - 1.0) <= 1e-8


def test_one_retry_and_persistent_failure_block():
    sample = _diagonal_sample(np.linspace(1.0, 1.1, 10))
    calls: list[int] = []

    def retry_optimizer(fun, x0, **kwargs):
        calls.append(len(calls) + 1)
        success = len(calls) == 2
        return SimpleNamespace(
            x=np.asarray(x0), success=success, status=0 if success else 9,
            message="ok" if success else "forced first failure", nit=len(calls),
        )

    weights, diagnostic = solve_target_weights(
        sample, "minimum_variance", 252, optimizer=retry_optimizer
    )
    assert len(weights) == 10
    assert diagnostic["attempts"] == 2
    assert [attempt["initial_value"] for attempt in diagnostic["attempt_details"]] == ["equal_weight", "staggered"]

    def failing_optimizer(fun, x0, **kwargs):
        return SimpleNamespace(x=np.asarray(x0), success=False, status=9, message="forced", nit=1)

    with pytest.raises(PortfolioBlockError) as error:
        solve_target_weights(sample, "minimum_variance", 252, optimizer=failing_optimizer)
    assert len(error.value.attempts) == 2


def test_manual_weight_drift():
    weights = np.array([0.20, 0.20, 0.20, 0.20, 0.20])
    returns = np.array([0.10, 0.00, -0.05, 0.02, 0.03])
    gross = float(weights @ returns)
    expected = weights * (1 + returns) / (1 + gross)
    np.testing.assert_allclose(drift_weights(weights, returns), expected, atol=1e-14)
    assert np.isclose(expected.sum(), 1.0)


def test_initial_formation_turnover_and_drifted_rebalance_turnover():
    dates = pd.date_range("2023-01-27", periods=10, freq="D")
    values = np.tile(np.array([0.01, 0.00, -0.01, 0.02, -0.005]), (10, 1))
    matrix = pd.DataFrame(values, index=dates, columns=[f"A{i}" for i in range(5)])
    spec = FundSpec("synthetic_equal_weight", "Synthetic", "Equal Weight", "equal_weight", tuple(matrix.columns), 365, 3)
    fund_returns, weights, _, _ = run_fund_backtest(matrix, spec)
    first = fund_returns.iloc[0]
    assert bool(first["is_rebalance"])
    assert first["turnover"] == 0.0
    assert first["transaction_cost"] == 0.0
    first_holdings = weights.loc[weights["date"].eq(first["date"])]
    assert first_holdings["pretrade_weight"].eq(0).all()
    np.testing.assert_allclose(first_holdings["trade_weight"], first_holdings["target_weight"])

    second_date = fund_returns.loc[fund_returns["is_rebalance"], "date"].iloc[1]
    previous_date = fund_returns.loc[fund_returns["date"].lt(second_date), "date"].iloc[-1]
    target = np.full(5, 0.2)
    drifted = target.copy()
    for date in fund_returns.loc[(fund_returns["date"].ge(first["date"])) & (fund_returns["date"].le(previous_date)), "date"]:
        drifted = drifted * (1 + matrix.loc[date].to_numpy()) / (1 + float(drifted @ matrix.loc[date].to_numpy()))
    expected_turnover = 0.5 * np.abs(target - drifted).sum()
    observed_turnover = float(fund_returns.loc[fund_returns["date"].eq(second_date), "turnover"].iloc[0])
    assert np.isclose(observed_turnover, expected_turnover, atol=1e-14)
    expected_cost = 0.0005 * expected_turnover
    row = fund_returns.loc[fund_returns["date"].eq(second_date)].iloc[0]
    assert np.isclose(row["transaction_cost"], expected_cost, atol=1e-14)
    assert np.isclose(row["net_return"], (1 - expected_cost) * (1 + row["gross_return"]) - 1, atol=1e-14)


def test_performance_metrics_against_independent_formulas():
    returns = pd.Series([0.01, -0.02, 0.03, 0.005])
    result = performance_metrics(returns, 252)
    wealth = np.cumprod(1 + returns.to_numpy())
    std = np.std(returns.to_numpy(), ddof=1)
    assert np.isclose(result["cumulative_return"], wealth[-1] - 1)
    assert np.isclose(result["annualised_return"], wealth[-1] ** (252 / 4) - 1)
    assert np.isclose(result["annualised_volatility"], std * np.sqrt(252))
    assert np.isclose(result["sharpe_ratio"], returns.mean() / std * np.sqrt(252))
    assert np.isclose(result["max_drawdown"], np.min(wealth / np.maximum.accumulate(wealth) - 1))


def test_future_perturbation_does_not_change_earlier_targets_and_rerun_is_deterministic():
    rng = np.random.default_rng(5545)
    dates = pd.date_range("2022-01-01", periods=100, freq="D")
    matrix = pd.DataFrame(rng.normal(0.0005, 0.01, size=(100, 6)), index=dates, columns=[f"A{i}" for i in range(6)])
    spec = FundSpec("synthetic_minimum_variance", "Synthetic", "Minimum Variance", "minimum_variance", tuple(matrix.columns), 365, 20)
    first = run_fund_backtest(matrix, spec)
    repeat = run_fund_backtest(matrix.copy(deep=True), spec)
    pd.testing.assert_frame_equal(first[0], repeat[0])
    pd.testing.assert_frame_equal(first[1], repeat[1])

    cutoff = pd.Timestamp("2022-03-01")
    perturbed = matrix.copy(deep=True)
    perturbed.loc[perturbed.index > cutoff, "A0"] += 0.25
    changed = run_fund_backtest(perturbed, spec)
    original_targets = first[1].loc[first[1]["date"].le(cutoff)].reset_index(drop=True)
    changed_targets = changed[1].loc[changed[1]["date"].le(cutoff)].reset_index(drop=True)
    pd.testing.assert_frame_equal(original_targets, changed_targets)
