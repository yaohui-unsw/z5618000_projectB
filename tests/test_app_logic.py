from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.app_data import ELIGIBLE_BASE_IDS, VARIANTS
from src.app_logic import (
    AppLogicError,
    allocation_performance_metrics,
    build_allocation_history,
    complete_fusion_table,
    current_holdings_date,
    equal_split_percentages,
    fusion_comparison_summary,
    growth_and_drawdown,
    growth_of_one,
    latest_target_holdings,
    reconcile_return_calendars,
    rolling_sentiment_summary,
    validate_user_allocation,
)


def _return_rows(fund_id: str, family: str, dates: list[str], returns: list[float]) -> list[dict[str, object]]:
    return [
        {"date": date, "fund_id": fund_id, "family": family, "net_return": value}
        for date, value in zip(dates, returns)
    ]


def test_growth_of_one_and_drawdown_use_independent_manual_formulas() -> None:
    frame = pd.DataFrame(_return_rows("fund", "Equity", ["2023-01-02", "2023-01-03", "2023-01-04"], [0.10, -0.20, 0.05]))
    growth = growth_of_one(frame)
    expected = np.array([1.10, 1.10 * 0.80, 1.10 * 0.80 * 1.05])
    np.testing.assert_allclose(growth["growth"], expected)
    paths = growth_and_drawdown(frame)
    manual_dd = expected / np.maximum.accumulate(expected) - 1.0
    np.testing.assert_allclose(paths["drawdown"], manual_dd)


def test_latest_holdings_use_latest_targets_sum_to_one_and_report_date() -> None:
    rows = []
    for date, weights in [("2023-11-01", [0.6, 0.4]), ("2023-12-01", [0.55, 0.45])]:
        for ticker, weight in zip(["AAPL", "BTC-USD"], weights):
            rows.append({"date": date, "fund_id": "combined", "family": "Combined", "method": "Equal Weight", "ticker": ticker, "target_weight": weight})
    latest = latest_target_holdings(pd.DataFrame(rows), "combined", tolerance=1.0)
    assert current_holdings_date(latest) == pd.Timestamp("2023-12-01")
    assert latest["target_weight"].sum() == pytest.approx(1.0)
    assert set(latest["asset_class"]) == {"Equity", "Crypto"}


def test_allocation_gate_uses_five_point_steps_and_never_normalises() -> None:
    funds = ["a", "b", "c"]
    assert equal_split_percentages(funds) == {"a": 35.0, "b": 35.0, "c": 30.0}
    valid = validate_user_allocation(funds, {"a": 35, "b": 35, "c": 30})
    assert valid.valid and valid.total_percent == 100
    invalid_total = validate_user_allocation(funds, {"a": 30, "b": 30, "c": 30})
    assert not invalid_total.valid and invalid_total.total_percent == 90
    assert "will not normalise" in invalid_total.message
    assert not validate_user_allocation(["a", "b"], {"a": 52, "b": 48}).valid


def test_mixed_calendar_compounds_crypto_weekend_returns() -> None:
    rows = _return_rows("equity", "Equity", ["2023-01-06", "2023-01-09"], [0.0, 0.0])
    rows += _return_rows("crypto", "Crypto", ["2023-01-06", "2023-01-07", "2023-01-08", "2023-01-09"], [0.01, 0.02, 0.03, 0.04])
    calendar = reconcile_return_calendars(pd.DataFrame(rows), ["equity", "crypto"])
    assert calendar.annualisation == 252
    assert list(calendar.returns["date"]) == [pd.Timestamp("2023-01-06"), pd.Timestamp("2023-01-09")]
    assert calendar.returns.loc[0, "crypto"] == pytest.approx(0.01)
    assert calendar.returns.loc[1, "crypto"] == pytest.approx((1.02 * 1.03 * 1.04) - 1.0)


def test_all_crypto_selection_uses_native_calendar_and_365() -> None:
    dates = ["2023-01-06", "2023-01-07", "2023-01-08"]
    rows = _return_rows("c1", "Crypto", dates, [0.01, 0.02, 0.03])
    rows += _return_rows("c2", "Crypto", dates, [-0.01, 0.00, 0.01])
    calendar = reconcile_return_calendars(pd.DataFrame(rows), ["c1", "c2"])
    assert calendar.annualisation == 365
    assert len(calendar.returns) == 3
    np.testing.assert_allclose(calendar.returns["c1"], [0.01, 0.02, 0.03])


def test_one_time_sleeves_drift_and_canonical_net_cost_is_not_applied_twice() -> None:
    dates = ["2023-01-02", "2023-01-03"]
    rows = _return_rows("a", "Equity", dates, [0.10, 0.00])
    rows += _return_rows("b", "Equity", dates, [0.00, 0.10])
    history, _ = build_allocation_history(pd.DataFrame(rows), ["a", "b"], {"a": 50, "b": 50}, 10_000, annual_management_fee=0.0)
    np.testing.assert_allclose(history["sleeve__a"], [5_500, 5_500])
    np.testing.assert_allclose(history["sleeve__b"], [5_000, 5_500])
    np.testing.assert_allclose(history["before_management_fee"], [10_500, 11_000])
    assert history.iloc[-1]["sleeve__a"] == history.iloc[-1]["sleeve__b"]


def test_exact_management_fee_formula_and_before_after_wealth() -> None:
    dates = ["2020-01-01", "2020-12-31"]
    rows = _return_rows("a", "Equity", dates, [0.0, 0.0])
    rows += _return_rows("b", "Equity", dates, [0.0, 0.0])
    history, calendar = build_allocation_history(pd.DataFrame(rows), ["a", "b"], {"a": 50, "b": 50}, 10_000)
    assert history.loc[0, "after_management_fee"] == pytest.approx(10_000)
    assert history.loc[1, "after_management_fee"] == pytest.approx(10_000 * (1 - 0.005) ** (365 / 365))
    assert np.all(history["after_management_fee"] <= history["before_management_fee"])
    metrics = allocation_performance_metrics(history, initial_capital=10_000, annualisation=calendar.annualisation)
    assert metrics["ending_value_after_fee"] == pytest.approx(9_950)
    assert metrics["management_fee_drag_dollars"] == pytest.approx(50)


def test_invalid_allocation_is_rejected_before_history() -> None:
    rows = _return_rows("a", "Equity", ["2023-01-02", "2023-01-03"], [0.0, 0.0])
    rows += _return_rows("b", "Equity", ["2023-01-02", "2023-01-03"], [0.0, 0.0])
    with pytest.raises(AppLogicError, match="will not normalise"):
        build_allocation_history(pd.DataFrame(rows), ["a", "b"], {"a": 40, "b": 40}, 10_000)


def test_rolling_sentiment_mean_is_display_only_and_deterministic() -> None:
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime(["2023-01-02", "2023-01-03", "2023-01-04"]),
            "sector": ["Tech"] * 3,
            "sector_display": ["Information Technology"] * 3,
            "finance_compound": [0.1, np.nan, 0.3],
        }
    )
    result = rolling_sentiment_summary(frame, ["Tech"], window=2)
    np.testing.assert_allclose(result["rolling_21"].to_numpy(), [0.1, 0.1, 0.3], equal_nan=True)
    assert frame.columns.tolist() == ["date", "sector", "sector_display", "finance_compound"]


def _fusion_frames() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    methods = ["Equal Weight", "Minimum Variance", "Maximum Sharpe", "Risk Parity"] * 2
    families = ["Equity"] * 4 + ["Combined"] * 4
    comparison_rows = []
    metric_rows = []
    base_rows = []
    for base, family, method in zip(ELIGIBLE_BASE_IDS, families, methods):
        base_rows.append({"fund_id": base, "net_annualised_return": 0.05, "net_sharpe_ratio": 0.5, "average_rebalance_turnover": 0.10})
        for index, variant in enumerate(VARIANTS):
            delta = [-0.01, 0.02, -0.005][index]
            overlay = f"{base}__{variant}"
            comparison_rows.append({
                "overlay_id": overlay, "base_fund_id": base, "family": family,
                "method": method, "variant": variant,
                "delta_net_annualised_return": delta,
                "delta_annualised_volatility": 0.0,
                "delta_net_sharpe_ratio": delta,
                "delta_net_max_drawdown": 0.0,
                "delta_net_cumulative_return": delta,
                "delta_average_turnover": [0.01, 0.02, 0.005][index],
                "delta_total_turnover": 0.0,
                "delta_transaction_cost_drag": 0.0,
            })
            metric_rows.append({
                "overlay_id": overlay,
                "net_annualised_return": 0.05 + delta,
                "net_sharpe_ratio": 0.5 + delta,
                "average_rebalance_turnover": 0.10 + [0.01, 0.02, 0.005][index],
            })
    return pd.DataFrame(comparison_rows), pd.DataFrame(metric_rows), pd.DataFrame(base_rows)


def test_complete_fusion_summary_retains_all_positive_and_negative_rows() -> None:
    comparison, fusion_metrics, base_metrics = _fusion_frames()
    summary = fusion_comparison_summary(comparison)
    assert summary["finance_positive_sharpe"] == 8
    assert summary["plain_positive_sharpe"] == 0
    table = complete_fusion_table(comparison, fusion_metrics, base_metrics)
    assert len(table) == 24
    assert (table["delta_net_sharpe_ratio"] > 0).any()
    assert (table["delta_net_sharpe_ratio"] < 0).any()

