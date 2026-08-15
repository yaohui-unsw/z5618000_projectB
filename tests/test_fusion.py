"""Independent synthetic tests for the frozen sentiment-fusion design."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.fusion import (
    ELIGIBLE_FUND_SPECS,
    OVERLAY_IDS,
    OVERLAY_SPECS,
    TILT_STRENGTH,
    VARIANTS,
    FusionBlockError,
    build_overlay_targets,
    capped_simplex_projection,
    run_fusion_suite,
)
from src.portfolios import performance_metrics
from src.validation import CRYPTO_TICKERS, EQUITY_TICKERS


def _base_weights(dates: list[pd.Timestamp]) -> pd.DataFrame:
    rows = []
    for spec in ELIGIBLE_FUND_SPECS:
        target = np.repeat(1.0 / len(spec.assets), len(spec.assets))
        for date in dates:
            for ticker, value in zip(spec.assets, target, strict=True):
                rows.append(
                    {
                        "date": date,
                        "fund_id": spec.fund_id,
                        "family": spec.family,
                        "method": spec.method,
                        "ticker": ticker,
                        "target_weight": value,
                    }
                )
    return pd.DataFrame(rows)


def _signals(dates: list[pd.Timestamp], *, active: bool = False) -> pd.DataFrame:
    rows = []
    for date in dates:
        for ticker in EQUITY_TICKERS:
            is_first = ticker == EQUITY_TICKERS[0]
            rows.append(
                {
                    "date": date,
                    "ticker": ticker,
                    "signal_source_date": date - pd.Timedelta(days=1),
                    "lagged_plain_signal": 1.0 if active and is_first else np.nan,
                    "lagged_finance_signal": 2.0 if active and is_first else np.nan,
                    "lagged_evidence_aware_signal": 0.5 if active and is_first else np.nan,
                }
            )
    return pd.DataFrame(rows)


def _base_returns(dates: pd.DatetimeIndex) -> pd.DataFrame:
    rows = []
    for spec in ELIGIBLE_FUND_SPECS:
        for position, date in enumerate(dates):
            rows.append(
                {
                    "date": date,
                    "fund_id": spec.fund_id,
                    "family": spec.family,
                    "method": spec.method,
                    "gross_return": 0.001,
                    "turnover": 0.0,
                    "transaction_cost": 0.0,
                    "net_return": 0.001,
                    "is_rebalance": position in {0, 2},
                }
            )
    return pd.DataFrame(rows)


def _base_performance() -> pd.DataFrame:
    rows = []
    for spec in ELIGIBLE_FUND_SPECS:
        rows.append(
            {
                "fund_id": spec.fund_id,
                "net_annualised_return": 0.10,
                "net_annualised_volatility": 0.20,
                "net_sharpe_ratio": 0.50,
                "net_max_drawdown": -0.10,
                "net_cumulative_return": 0.05,
                "gross_cumulative_return": 0.051,
                "average_rebalance_turnover": 0.02,
                "total_turnover": 0.70,
            }
        )
    return pd.DataFrame(rows)


def _matrices(dates: pd.DatetimeIndex) -> dict[str, pd.DataFrame]:
    equity = pd.DataFrame(0.0, index=dates, columns=EQUITY_TICKERS)
    combined = pd.DataFrame(0.0, index=dates, columns=(*EQUITY_TICKERS, *CRYPTO_TICKERS))
    equity.iloc[0, 0] = 0.10
    equity.iloc[1, 0] = 0.20
    combined.iloc[:, : len(EQUITY_TICKERS)] = equity.to_numpy()
    return {"Equity": equity, "Combined": combined}


def test_exact_overlay_enumeration_order_and_crypto_exclusion():
    assert len(OVERLAY_SPECS) == len(OVERLAY_IDS) == 24
    assert len(set(OVERLAY_IDS)) == 24
    assert all(spec.family in {"Equity", "Combined"} for spec in OVERLAY_SPECS)
    assert all("crypto_" not in overlay_id for overlay_id in OVERLAY_IDS)
    assert tuple(spec.variant for spec in OVERLAY_SPECS[:3]) == VARIANTS
    assert OVERLAY_IDS[0] == "equity_equal_weight__plain_vader_naive"
    assert OVERLAY_IDS[-1] == "combined_risk_parity__evidence_aware_finance"


def test_capped_simplex_projection_constraints_determinism_and_block():
    values = np.array([0.8, 0.1, 0.1, 0.0, 0.0])
    first, status = capped_simplex_projection(values, total=1.0, cap=0.20)
    second, second_status = capped_simplex_projection(values, total=1.0, cap=0.20)
    assert status == second_status == "projected_capped_simplex"
    np.testing.assert_array_equal(first, second)
    assert first.sum() == pytest.approx(1.0, abs=1e-12)
    assert first.min() >= 0.0 and first.max() <= 0.20 + 1e-12
    with pytest.raises(FusionBlockError):
        capped_simplex_projection(np.ones(4), total=1.0, cap=0.20)


def test_variant_signal_selection_lambda_and_missing_multiplier():
    date = pd.Timestamp("2021-01-04")
    targets = build_overlay_targets(_base_weights([date]), _signals([date], active=True))
    ticker = EQUITY_TICKERS[0]
    expected = {
        "plain_vader_naive": np.exp(TILT_STRENGTH * 1.0),
        "finance_vader_naive": np.exp(TILT_STRENGTH * 2.0),
        "evidence_aware_finance": np.exp(TILT_STRENGTH * 0.5),
    }
    for variant, multiplier in expected.items():
        row = targets.loc[
            targets["overlay_id"].eq(f"equity_equal_weight__{variant}")
            & targets["ticker"].eq(ticker)
        ].iloc[0]
        assert row.multiplier == pytest.approx(multiplier)
    missing = targets.loc[
        targets["overlay_id"].eq("equity_equal_weight__plain_vader_naive")
        & targets["ticker"].eq(EQUITY_TICKERS[1])
    ].iloc[0]
    assert pd.isna(missing.signal_value) and missing.multiplier == 1.0


def test_all_missing_reproduces_base_and_combined_sleeves_are_preserved():
    date = pd.Timestamp("2021-01-04")
    base = _base_weights([date])
    targets = build_overlay_targets(base, _signals([date]))
    for overlay in OVERLAY_SPECS:
        subset = targets.loc[targets["overlay_id"].eq(overlay.overlay_id)].set_index("ticker")
        source = base.loc[base["fund_id"].eq(overlay.base_fund_id)].set_index("ticker")
        np.testing.assert_allclose(subset.loc[list(overlay.assets), "target_weight"], source.loc[list(overlay.assets), "target_weight"], atol=1e-12)
    combined = targets.loc[targets["family"].eq("Combined")]
    assert combined.loc[combined["ticker"].isin(CRYPTO_TICKERS), "multiplier"].eq(1.0).all()
    assert combined.loc[combined["ticker"].isin(CRYPTO_TICKERS), "signal_value"].isna().all()
    assert combined.loc[combined["ticker"].isin(CRYPTO_TICKERS), "raw_tilted_value"].isna().all()


def test_monthly_only_targets_drift_inception_turnover_cost_and_metrics():
    dates = pd.DatetimeIndex([pd.Timestamp("2021-01-04"), pd.Timestamp("2021-01-05"), pd.Timestamp("2021-02-01")])
    rebalance_dates = [dates[0], dates[2]]
    targets = build_overlay_targets(_base_weights(rebalance_dates), _signals(rebalance_dates))
    artifacts = run_fusion_suite(
        targets,
        _matrices(dates),
        _base_returns(dates),
        _base_performance(),
    )
    returns = artifacts["fusion_returns"]
    weights = artifacts["fusion_weights"]
    overlay_id = "equity_equal_weight__plain_vader_naive"
    daily = returns.loc[returns["overlay_id"].eq(overlay_id)].sort_values("date")
    holdings = weights.loc[weights["overlay_id"].eq(overlay_id)]
    assert holdings["date"].nunique() == 2
    inception = daily.iloc[0]
    assert inception.turnover == 0.0 and inception.transaction_cost == 0.0
    target = np.repeat(1 / 50, 50)
    first_returns = np.zeros(50)
    first_returns[0] = 0.10
    drift_one = target * (1 + first_returns) / (1 + target @ first_returns)
    second_returns = np.zeros(50)
    second_returns[0] = 0.20
    drift_two = drift_one * (1 + second_returns) / (1 + drift_one @ second_returns)
    second_rebalance = holdings.loc[holdings["date"].eq(dates[2])].set_index("ticker").reindex(EQUITY_TICKERS)
    np.testing.assert_allclose(second_rebalance["pretrade_weight"], drift_two, atol=1e-12)
    expected_turnover = 0.5 * np.abs(target - drift_two).sum()
    assert daily.iloc[2].turnover == pytest.approx(expected_turnover)
    assert daily.iloc[2].transaction_cost == pytest.approx(0.0005 * expected_turnover)
    expected_net = (1 - 0.0005 * expected_turnover) * (1 + daily.iloc[2].gross_return) - 1
    assert daily.iloc[2].net_return == pytest.approx(expected_net)
    metrics = artifacts["fusion_performance_metrics"].set_index("overlay_id").loc[overlay_id]
    manual = performance_metrics(daily["net_return"], 252)
    assert metrics.net_annualised_return == pytest.approx(manual["annualised_return"])
    assert metrics.net_annualised_volatility == pytest.approx(manual["annualised_volatility"])
    assert metrics.net_sharpe_ratio == pytest.approx(manual["sharpe_ratio"])
    assert metrics.net_max_drawdown == pytest.approx(manual["max_drawdown"])


def test_projection_results_are_deterministic():
    date = pd.Timestamp("2021-01-04")
    base = _base_weights([date])
    signals = _signals([date], active=True)
    first = build_overlay_targets(base, signals)
    second = build_overlay_targets(base, signals)
    pd.testing.assert_frame_equal(first, second)
