"""Frozen monthly sentiment overlays for accepted Equity and Combined funds."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from src.portfolios import (
    FUND_SPECS,
    TRANSACTION_COST_RATE,
    WEIGHT_CAP,
    FundSpec,
    drift_weights,
    performance_metrics,
)
from src.sentiment import SENTIMENT_DIAGNOSTIC_COLUMNS
from src.validation import CRYPTO_TICKERS, EQUITY_TICKERS


TILT_STRENGTH = 0.10
VARIANTS = (
    "plain_vader_naive",
    "finance_vader_naive",
    "evidence_aware_finance",
)
VARIANT_SIGNAL_COLUMNS = {
    "plain_vader_naive": "lagged_plain_signal",
    "finance_vader_naive": "lagged_finance_signal",
    "evidence_aware_finance": "lagged_evidence_aware_signal",
}

ELIGIBLE_FUND_SPECS = tuple(
    spec for spec in FUND_SPECS if spec.family in {"Equity", "Combined"}
)


@dataclass(frozen=True)
class OverlaySpec:
    overlay_id: str
    base_fund_id: str
    family: str
    method: str
    variant: str
    assets: tuple[str, ...]
    annualisation: int


OVERLAY_SPECS = tuple(
    OverlaySpec(
        overlay_id=f"{spec.fund_id}__{variant}",
        base_fund_id=spec.fund_id,
        family=spec.family,
        method=spec.method,
        variant=variant,
        assets=spec.assets,
        annualisation=spec.annualisation,
    )
    for spec in ELIGIBLE_FUND_SPECS
    for variant in VARIANTS
)
OVERLAY_IDS = tuple(spec.overlay_id for spec in OVERLAY_SPECS)
OVERLAY_ORDER = {overlay_id: position for position, overlay_id in enumerate(OVERLAY_IDS)}


FUSION_RETURN_COLUMNS = (
    "date", "overlay_id", "base_fund_id", "family", "method", "variant",
    "gross_return", "turnover", "transaction_cost", "net_return",
    "is_rebalance",
)
FUSION_WEIGHT_COLUMNS = (
    "date", "overlay_id", "base_fund_id", "family", "method", "variant",
    "ticker", "base_target_weight", "pretrade_weight", "signal_source_date",
    "signal_value", "multiplier", "raw_tilted_value", "target_weight",
    "trade_weight", "turnover", "projection_success", "projection_status",
)
FUSION_PERFORMANCE_COLUMNS = (
    "overlay_id", "base_fund_id", "family", "method", "variant", "start_date",
    "end_date", "observations", "annualisation", "transaction_cost_bps",
    "net_cumulative_return", "net_annualised_return",
    "net_annualised_volatility", "net_sharpe_ratio", "net_max_drawdown",
    "gross_cumulative_return", "gross_annualised_return", "gross_sharpe_ratio",
    "average_rebalance_turnover", "total_turnover", "transaction_cost_drag",
    "rebalance_count",
)
FUSION_COMPARISON_COLUMNS = (
    "overlay_id", "base_fund_id", "family", "method", "variant",
    "delta_net_annualised_return", "delta_annualised_volatility",
    "delta_net_sharpe_ratio", "delta_net_max_drawdown",
    "delta_net_cumulative_return", "delta_average_turnover",
    "delta_total_turnover", "delta_transaction_cost_drag",
)


class FusionBlockError(RuntimeError):
    """A frozen fusion or projection invariant failed."""


def capped_simplex_projection(
    values: np.ndarray,
    total: float = 1.0,
    cap: float = WEIGHT_CAP,
    *,
    tolerance: float = 1e-13,
) -> tuple[np.ndarray, str]:
    """Euclidean projection onto ``sum(w)=total`` and ``0<=w<=cap``."""
    vector = np.asarray(values, dtype="float64")
    if vector.ndim != 1 or not np.isfinite(vector).all():
        raise FusionBlockError("projection input must be a finite vector")
    if total < -tolerance or total > len(vector) * cap + tolerance:
        raise FusionBlockError("capped-simplex target total is infeasible")
    if total <= tolerance:
        return np.zeros_like(vector), "zero_equity_sleeve"
    if (
        np.all(vector >= -tolerance)
        and np.all(vector <= cap + tolerance)
        and abs(float(vector.sum()) - total) <= tolerance
    ):
        result = np.clip(vector, 0.0, cap)
        result *= total / result.sum()
        return result, "already_feasible"

    lower = float(np.min(vector - cap))
    upper = float(np.max(vector))
    for _ in range(200):
        midpoint = (lower + upper) / 2.0
        projected = np.clip(vector - midpoint, 0.0, cap)
        if float(projected.sum()) > total:
            lower = midpoint
        else:
            upper = midpoint
    projected = np.clip(vector - (lower + upper) / 2.0, 0.0, cap)
    residual = total - float(projected.sum())
    if abs(residual) > tolerance:
        if residual > 0:
            candidates = np.flatnonzero(projected < cap - tolerance)
        else:
            candidates = np.flatnonzero(projected > tolerance)
        for index in candidates:
            room = cap - projected[index] if residual > 0 else projected[index]
            change = np.sign(residual) * min(abs(residual), room)
            projected[index] += change
            residual -= change
            if abs(residual) <= tolerance:
                break
    if (
        not np.isfinite(projected).all()
        or abs(float(projected.sum()) - total) > 1e-10
        or float(projected.min()) < -1e-10
        or float(projected.max()) > cap + 1e-10
    ):
        raise FusionBlockError("capped-simplex projection failed validation")
    return projected, "projected_capped_simplex"


def _fund_spec(fund_id: str) -> FundSpec:
    matches = [spec for spec in ELIGIBLE_FUND_SPECS if spec.fund_id == fund_id]
    if len(matches) != 1:
        raise FusionBlockError(f"unexpected or Crypto-only base fund: {fund_id}")
    return matches[0]


def build_overlay_targets(
    base_weights: pd.DataFrame,
    ticker_sentiment: pd.DataFrame,
) -> pd.DataFrame:
    """Create all 24 projected monthly targets without rerunning optimisation."""
    required_weights = {"date", "fund_id", "ticker", "target_weight"}
    required_sentiment = {
        "date", "ticker", "signal_source_date", *VARIANT_SIGNAL_COLUMNS.values()
    }
    if not required_weights.issubset(base_weights.columns):
        raise FusionBlockError("base weights are missing required columns")
    if not required_sentiment.issubset(ticker_sentiment.columns):
        raise FusionBlockError("ticker sentiment is missing lagged signals")
    base = base_weights.copy(deep=True)
    base["date"] = pd.to_datetime(base["date"])
    signals = ticker_sentiment.loc[:, list(required_sentiment)].copy(deep=True)
    signals["date"] = pd.to_datetime(signals["date"])
    signals["signal_source_date"] = pd.to_datetime(signals["signal_source_date"])
    signal_lookup = signals.set_index(["date", "ticker"])
    rows: list[dict[str, Any]] = []

    for overlay in OVERLAY_SPECS:
        fund_spec = _fund_spec(overlay.base_fund_id)
        fund = base.loc[base["fund_id"].eq(overlay.base_fund_id)]
        if fund.empty:
            raise FusionBlockError(f"base weights missing {overlay.base_fund_id}")
        for date, group in fund.groupby("date", sort=True):
            ordered = group.set_index("ticker").reindex(list(fund_spec.assets))
            if ordered["target_weight"].isna().any():
                raise FusionBlockError("base target is incomplete or misordered")
            base_target = ordered["target_weight"].to_numpy(dtype="float64")
            equity_count = len(EQUITY_TICKERS)
            equity_tickers = list(fund_spec.assets[:equity_count])
            equity_signals = signal_lookup.reindex(
                pd.MultiIndex.from_product([[date], equity_tickers], names=["date", "ticker"])
            )
            signal_column = VARIANT_SIGNAL_COLUMNS[overlay.variant]
            signal_values = equity_signals[signal_column].to_numpy(dtype="float64")
            multipliers = np.exp(TILT_STRENGTH * np.nan_to_num(signal_values, nan=0.0))
            raw_equity = base_target[:equity_count] * multipliers

            if overlay.family == "Equity":
                sleeve_total = 1.0
            else:
                sleeve_total = float(base_target[:equity_count].sum())
            if sleeve_total > 0 and float(raw_equity.sum()) <= 0:
                raise FusionBlockError("positive equity sleeve has no raw tilted mass")
            normalised = (
                raw_equity * (sleeve_total / float(raw_equity.sum()))
                if sleeve_total > 0
                else np.zeros_like(raw_equity)
            )
            projected_equity, projection_status = capped_simplex_projection(
                normalised, total=sleeve_total, cap=WEIGHT_CAP
            )
            if overlay.family == "Equity":
                target = projected_equity
            else:
                target = np.concatenate([projected_equity, base_target[equity_count:]])
                if not np.array_equal(target[equity_count:], base_target[equity_count:]):
                    raise FusionBlockError("Combined crypto target changed during fusion")
            if abs(float(target.sum()) - 1.0) > 1e-10 or np.any(target < -1e-10) or np.any(target > WEIGHT_CAP + 1e-10):
                raise FusionBlockError("published overlay target violates constraints")

            for position, ticker in enumerate(fund_spec.assets):
                equity_asset = position < equity_count
                signal = signal_values[position] if equity_asset else np.nan
                source_date = equity_signals["signal_source_date"].iloc[position] if equity_asset else pd.NaT
                multiplier = multipliers[position] if equity_asset else 1.0
                raw_value = raw_equity[position] if equity_asset else np.nan
                rows.append(
                    {
                        "date": pd.Timestamp(date),
                        "overlay_id": overlay.overlay_id,
                        "base_fund_id": overlay.base_fund_id,
                        "family": overlay.family,
                        "method": overlay.method,
                        "variant": overlay.variant,
                        "ticker": ticker,
                        "base_target_weight": float(base_target[position]),
                        "signal_source_date": source_date,
                        "signal_value": float(signal) if np.isfinite(signal) else np.nan,
                        "multiplier": float(multiplier),
                        "raw_tilted_value": float(raw_value) if equity_asset else np.nan,
                        "target_weight": float(target[position]),
                        "projection_success": True,
                        "projection_status": projection_status,
                    }
                )
    targets = pd.DataFrame(rows)
    targets["_overlay_order"] = targets["overlay_id"].map(OVERLAY_ORDER)
    asset_order = {ticker: index for index, ticker in enumerate((*EQUITY_TICKERS, *CRYPTO_TICKERS))}
    targets["_asset_order"] = targets["ticker"].map(asset_order)
    return targets.sort_values(
        ["date", "_overlay_order", "_asset_order"], kind="mergesort"
    ).drop(columns=["_overlay_order", "_asset_order"]).reset_index(drop=True)


def _performance_row(
    returns: pd.DataFrame,
    overlay: OverlaySpec,
) -> dict[str, Any]:
    net = performance_metrics(returns["net_return"], overlay.annualisation)
    gross = performance_metrics(returns["gross_return"], overlay.annualisation)
    rebalances = returns.loc[returns["is_rebalance"]]
    cost_bearing = rebalances.iloc[1:]
    drag = gross["cumulative_return"] - net["cumulative_return"]
    return {
        "overlay_id": overlay.overlay_id,
        "base_fund_id": overlay.base_fund_id,
        "family": overlay.family,
        "method": overlay.method,
        "variant": overlay.variant,
        "start_date": pd.Timestamp(returns["date"].iloc[0]),
        "end_date": pd.Timestamp(returns["date"].iloc[-1]),
        "observations": int(len(returns)),
        "annualisation": int(overlay.annualisation),
        "transaction_cost_bps": 5.0,
        "net_cumulative_return": net["cumulative_return"],
        "net_annualised_return": net["annualised_return"],
        "net_annualised_volatility": net["annualised_volatility"],
        "net_sharpe_ratio": net["sharpe_ratio"],
        "net_max_drawdown": net["max_drawdown"],
        "gross_cumulative_return": gross["cumulative_return"],
        "gross_annualised_return": gross["annualised_return"],
        "gross_sharpe_ratio": gross["sharpe_ratio"],
        "average_rebalance_turnover": float(cost_bearing["turnover"].mean()) if len(cost_bearing) else 0.0,
        "total_turnover": float(cost_bearing["turnover"].sum()),
        "transaction_cost_drag": drag,
        "rebalance_count": int(len(rebalances)),
    }


def run_fusion_suite(
    targets: pd.DataFrame,
    family_matrices: dict[str, pd.DataFrame],
    base_returns: pd.DataFrame,
    base_performance: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Run 24 monthly overlays using accepted base dates and return mechanics."""
    base_daily = base_returns.copy(deep=True)
    base_daily["date"] = pd.to_datetime(base_daily["date"])
    return_frames: list[pd.DataFrame] = []
    weight_frames: list[pd.DataFrame] = []
    metric_rows: list[dict[str, Any]] = []

    for overlay in OVERLAY_SPECS:
        matrix = family_matrices[overlay.family].loc[:, list(overlay.assets)]
        accepted_dates = pd.DatetimeIndex(
            base_daily.loc[
                base_daily["fund_id"].eq(overlay.base_fund_id), "date"
            ].sort_values(kind="mergesort")
        )
        live = matrix.reindex(accepted_dates)
        if live.isna().any().any() or tuple(live.columns) != overlay.assets:
            raise FusionBlockError("accepted live return matrix is incomplete")
        target_frame = targets.loc[targets["overlay_id"].eq(overlay.overlay_id)]
        target_groups = {
            pd.Timestamp(date): group.set_index("ticker").reindex(list(overlay.assets))
            for date, group in target_frame.groupby("date", sort=True)
        }
        accepted_rebalances = set(
            base_daily.loc[
                base_daily["fund_id"].eq(overlay.base_fund_id)
                & base_daily["is_rebalance"].astype(bool),
                "date",
            ]
        )
        if set(target_groups) != accepted_rebalances:
            raise FusionBlockError("overlay rebalance dates differ from base fund")
        current: np.ndarray | None = None
        daily_rows: list[dict[str, Any]] = []
        holding_rows: list[dict[str, Any]] = []
        for date, asset_row in live.iterrows():
            is_rebalance = date in accepted_rebalances
            turnover = 0.0
            transaction_cost = 0.0
            if is_rebalance:
                group = target_groups[date]
                target = group["target_weight"].to_numpy(dtype="float64")
                initial = current is None
                pretrade = np.zeros(len(target), dtype="float64") if initial else current.copy()
                trade = target - pretrade
                if not initial:
                    turnover = 0.5 * float(np.abs(trade).sum())
                    transaction_cost = TRANSACTION_COST_RATE * turnover
                pre_return = target
                for ticker, target_row, pre, trade_value in zip(
                    overlay.assets, group.itertuples(), pretrade, trade, strict=True
                ):
                    holding_rows.append(
                        {
                            "date": date,
                            "overlay_id": overlay.overlay_id,
                            "base_fund_id": overlay.base_fund_id,
                            "family": overlay.family,
                            "method": overlay.method,
                            "variant": overlay.variant,
                            "ticker": ticker,
                            "base_target_weight": float(target_row.base_target_weight),
                            "pretrade_weight": float(pre),
                            "signal_source_date": target_row.signal_source_date,
                            "signal_value": float(target_row.signal_value) if pd.notna(target_row.signal_value) else np.nan,
                            "multiplier": float(target_row.multiplier),
                            "raw_tilted_value": float(target_row.raw_tilted_value) if pd.notna(target_row.raw_tilted_value) else np.nan,
                            "target_weight": float(target_row.target_weight),
                            "trade_weight": float(trade_value),
                            "turnover": turnover,
                            "projection_success": bool(target_row.projection_success),
                            "projection_status": str(target_row.projection_status),
                        }
                    )
            else:
                if current is None:
                    raise FusionBlockError("overlay live series began before inception")
                pre_return = current
            asset_returns = asset_row.to_numpy(dtype="float64")
            gross = float(pre_return @ asset_returns)
            net = (1.0 - transaction_cost) * (1.0 + gross) - 1.0
            if not np.isfinite(gross) or not np.isfinite(net) or gross <= -1.0 or net <= -1.0:
                raise FusionBlockError("overlay produced an invalid daily return")
            daily_rows.append(
                {
                    "date": date,
                    "overlay_id": overlay.overlay_id,
                    "base_fund_id": overlay.base_fund_id,
                    "family": overlay.family,
                    "method": overlay.method,
                    "variant": overlay.variant,
                    "gross_return": gross,
                    "turnover": turnover,
                    "transaction_cost": transaction_cost,
                    "net_return": net,
                    "is_rebalance": bool(is_rebalance),
                }
            )
            current = drift_weights(pre_return, asset_returns)
        overlay_returns = pd.DataFrame(daily_rows)
        overlay_weights = pd.DataFrame(holding_rows)
        return_frames.append(overlay_returns)
        weight_frames.append(overlay_weights)
        metric_rows.append(_performance_row(overlay_returns, overlay))

    returns = pd.concat(return_frames, ignore_index=True)
    weights = pd.concat(weight_frames, ignore_index=True)
    metrics = pd.DataFrame(metric_rows)
    for frame in (returns, weights, metrics):
        frame["_overlay_order"] = frame["overlay_id"].map(OVERLAY_ORDER)
    returns = returns.sort_values(["date", "_overlay_order"], kind="mergesort").drop(columns="_overlay_order").reset_index(drop=True)
    asset_order = {ticker: index for index, ticker in enumerate((*EQUITY_TICKERS, *CRYPTO_TICKERS))}
    weights["_asset_order"] = weights["ticker"].map(asset_order)
    weights = weights.sort_values(["date", "_overlay_order", "_asset_order"], kind="mergesort").drop(columns=["_overlay_order", "_asset_order"]).reset_index(drop=True)
    metrics = metrics.sort_values("_overlay_order", kind="mergesort").drop(columns="_overlay_order").reset_index(drop=True)

    base_metrics = base_performance.set_index("fund_id")
    comparisons: list[dict[str, Any]] = []
    for row in metrics.itertuples(index=False):
        base = base_metrics.loc[row.base_fund_id]
        base_drag = float(base["gross_cumulative_return"] - base["net_cumulative_return"])
        comparisons.append(
            {
                "overlay_id": row.overlay_id,
                "base_fund_id": row.base_fund_id,
                "family": row.family,
                "method": row.method,
                "variant": row.variant,
                "delta_net_annualised_return": row.net_annualised_return - float(base["net_annualised_return"]),
                "delta_annualised_volatility": row.net_annualised_volatility - float(base["net_annualised_volatility"]),
                "delta_net_sharpe_ratio": row.net_sharpe_ratio - float(base["net_sharpe_ratio"]),
                "delta_net_max_drawdown": row.net_max_drawdown - float(base["net_max_drawdown"]),
                "delta_net_cumulative_return": row.net_cumulative_return - float(base["net_cumulative_return"]),
                "delta_average_turnover": row.average_rebalance_turnover - float(base["average_rebalance_turnover"]),
                "delta_total_turnover": row.total_turnover - float(base["total_turnover"]),
                "delta_transaction_cost_drag": row.transaction_cost_drag - base_drag,
            }
        )
    comparison = pd.DataFrame(comparisons)
    return {
        "fusion_returns": returns.loc[:, list(FUSION_RETURN_COLUMNS)],
        "fusion_weights": weights.loc[:, list(FUSION_WEIGHT_COLUMNS)],
        "fusion_performance_metrics": metrics.loc[:, list(FUSION_PERFORMANCE_COLUMNS)],
        "fusion_comparison": comparison.loc[:, list(FUSION_COMPARISON_COLUMNS)],
    }


def build_fusion_diagnostics(fusion_weights: pd.DataFrame) -> pd.DataFrame:
    """Summarise missing multipliers and active tilts for all variants."""
    equity = fusion_weights.loc[fusion_weights["ticker"].isin(EQUITY_TICKERS)].copy()
    start = pd.Timestamp(fusion_weights["date"].min())
    end = pd.Timestamp(fusion_weights["date"].max())
    rows: list[dict[str, Any]] = []
    for variant in VARIANTS:
        subset = equity.loc[equity["variant"].eq(variant)]
        denominator = len(subset)
        missing = int(subset["signal_value"].isna().sum())
        active = subset["multiplier"].sub(1.0).abs().gt(1e-15)
        magnitude = subset.loc[active, "multiplier"].sub(1.0).abs()
        values = {
            "multiplier_one_due_missing_signal_rate": (missing / denominator, missing, denominator, "Missing lagged signal uses multiplier one without carry-forward."),
            "active_tilt_frequency": (int(active.sum()) / denominator, int(active.sum()), denominator, "Active means abs(multiplier-1) > 1e-15."),
            "active_tilt_mean_absolute_multiplier_change": (float(magnitude.mean()) if len(magnitude) else 0.0, np.nan, np.nan, "Conditional on an active tilt."),
            "active_tilt_max_absolute_multiplier_change": (float(magnitude.max()) if len(magnitude) else 0.0, np.nan, np.nan, "Maximum absolute multiplier change."),
        }
        for metric, (value, numerator, denominator_value, notes) in values.items():
            rows.append(
                {
                    "scope": "fusion_rebalance_equity_asset", "entity": "all",
                    "model": variant, "metric": metric, "value": value,
                    "numerator": numerator, "denominator": denominator_value,
                    "start_date": start, "end_date": end, "notes": notes,
                }
            )
    return pd.DataFrame(rows).loc[:, list(SENTIMENT_DIAGNOSTIC_COLUMNS)]


def apply_sentiment(weights: pd.DataFrame, sentiment: pd.DataFrame) -> pd.DataFrame:
    """Compatibility wrapper for the frozen monthly target construction."""
    return build_overlay_targets(weights, sentiment)


__all__ = [
    "ELIGIBLE_FUND_SPECS", "FUSION_COMPARISON_COLUMNS",
    "FUSION_PERFORMANCE_COLUMNS", "FUSION_RETURN_COLUMNS",
    "FUSION_WEIGHT_COLUMNS", "FusionBlockError", "OVERLAY_IDS",
    "OVERLAY_ORDER", "OVERLAY_SPECS", "TILT_STRENGTH", "VARIANTS",
    "VARIANT_SIGNAL_COLUMNS", "apply_sentiment", "build_fusion_diagnostics",
    "build_overlay_targets", "capped_simplex_projection", "run_fusion_suite",
]
