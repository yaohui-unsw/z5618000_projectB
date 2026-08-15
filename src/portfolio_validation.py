"""Machine-readable validation for frozen OOS portfolio artifacts.

Validation is intentionally separate from optimisation.  The in-memory path
can reconcile fund returns, drift, turnover, costs, and calendars against the
source return matrices before any CSV is written.  The file-based command uses
the same structural and metric checks without rerunning an optimiser.
"""
from __future__ import annotations

import json
from math import sqrt
from typing import Any

import numpy as np
import pandas as pd

from src.portfolios import (
    CONSTRAINT_TOLERANCE,
    FUND_IDS,
    FUND_ORDER,
    FUND_SPECS,
    TRANSACTION_COST_RATE,
    WEIGHT_CAP,
)
from src.validation import ValidationReport


FUND_RETURN_COLUMNS = (
    "date", "fund_id", "family", "method", "gross_return", "turnover",
    "transaction_cost", "net_return", "is_rebalance",
)
FUND_WEIGHT_COLUMNS = (
    "date", "fund_id", "family", "method", "ticker", "pretrade_weight",
    "target_weight", "trade_weight", "turnover", "solver_success",
    "solver_status",
)
PERFORMANCE_METRIC_COLUMNS = (
    "fund_id", "family", "method", "start_date", "end_date", "observations",
    "annualisation", "transaction_cost_bps", "net_cumulative_return",
    "net_annualised_return", "net_annualised_volatility", "net_sharpe_ratio",
    "net_max_drawdown", "gross_cumulative_return", "gross_annualised_return",
    "gross_sharpe_ratio", "average_rebalance_turnover", "total_turnover",
    "rebalance_count",
)
SOLVER_DIAGNOSTIC_REQUIRED_COLUMNS = (
    "date", "fund_id", "family", "method", "solver_success", "attempts",
    "status_code", "message", "iterations", "objective_value",
    "sum_residual", "lower_bound_violation", "upper_bound_violation",
    "covariance_repair",
)
SENSITIVITY_COLUMNS = (
    "fund_id", "family", "method", "canonical_net_annualised_return",
    "sensitivity_net_annualised_return", "delta_net_annualised_return",
    "canonical_net_sharpe_ratio", "sensitivity_net_sharpe_ratio",
    "delta_net_sharpe_ratio", "canonical_net_max_drawdown",
    "sensitivity_net_max_drawdown", "delta_net_max_drawdown",
)


def _columns_equal(frame: pd.DataFrame, columns: tuple[str, ...]) -> bool:
    return tuple(frame.columns) == columns


def _unique_key(frame: pd.DataFrame, columns: list[str]) -> bool:
    return (
        all(column in frame for column in columns)
        and not frame.loc[:, columns].isna().any().any()
        and not frame.duplicated(columns).any()
    )


def _finite(frame: pd.DataFrame, columns: list[str]) -> bool:
    try:
        values = frame.loc[:, columns].to_numpy(dtype="float64")
    except (KeyError, TypeError, ValueError):
        return False
    return bool(np.isfinite(values).all())


def _metric_values(returns: pd.Series, annualisation: int) -> dict[str, float]:
    values = returns.to_numpy(dtype="float64")
    wealth = np.cumprod(1.0 + values)
    cumulative = float(wealth[-1] - 1.0)
    annualised = float(wealth[-1] ** (annualisation / len(values)) - 1.0)
    standard_deviation = float(np.std(values, ddof=1))
    volatility = standard_deviation * sqrt(annualisation)
    sharpe = float(np.mean(values) / standard_deviation * sqrt(annualisation))
    drawdown = wealth / np.maximum.accumulate(wealth) - 1.0
    return {
        "cumulative_return": cumulative,
        "annualised_return": annualised,
        "annualised_volatility": volatility,
        "sharpe_ratio": sharpe,
        "max_drawdown": float(drawdown.min()),
    }


def _expected_monthly_dates(matrix: pd.DataFrame, window: int) -> pd.DatetimeIndex:
    complete = matrix.loc[matrix.notna().all(axis=1)].sort_index(kind="mergesort")
    eligible = list(complete.index[window:])
    selected: list[pd.Timestamp] = []
    last_period: Any = None
    for date in eligible:
        period = pd.Timestamp(date).to_period("M")
        if period != last_period:
            selected.append(pd.Timestamp(date))
            last_period = period
    return pd.DatetimeIndex(selected, name="date")


def _parse_solver_status(values: pd.Series) -> bool:
    try:
        payloads = [json.loads(value) for value in values.astype(str)]
    except (TypeError, ValueError, json.JSONDecodeError):
        return False
    required = {
        "solver", "solver_success", "attempts", "status_code", "message",
        "iterations", "objective_value", "sum_residual",
        "lower_bound_violation", "upper_bound_violation",
        "covariance_repair", "minimum_eigenvalue", "attempt_details",
    }
    return all(required.issubset(payload) for payload in payloads)


def _check_ordering(
    returns: pd.DataFrame, weights: pd.DataFrame, metrics: pd.DataFrame,
    diagnostics: pd.DataFrame,
) -> bool:
    spec_by_id = {spec.fund_id: spec for spec in FUND_SPECS}
    expected_returns = returns.assign(
        _fund_order=returns["fund_id"].map(FUND_ORDER)
    ).sort_values(["date", "_fund_order"], kind="mergesort").drop(columns="_fund_order")
    asset_order = {
        (spec.fund_id, ticker): position
        for spec in FUND_SPECS
        for position, ticker in enumerate(spec.assets)
    }
    expected_weights = weights.assign(
        _fund_order=weights["fund_id"].map(FUND_ORDER),
        _asset_order=[asset_order.get((row.fund_id, row.ticker), -1) for row in weights.itertuples()],
    ).sort_values(["date", "_fund_order", "_asset_order"], kind="mergesort").drop(columns=["_fund_order", "_asset_order"])
    expected_metrics = metrics.assign(
        _fund_order=metrics["fund_id"].map(FUND_ORDER)
    ).sort_values("_fund_order", kind="mergesort").drop(columns="_fund_order")
    expected_diagnostics = diagnostics.assign(
        _fund_order=diagnostics["fund_id"].map(FUND_ORDER)
    ).sort_values(["date", "_fund_order"], kind="mergesort").drop(columns="_fund_order")
    membership_ok = all(
        tuple(group["ticker"]) == spec_by_id[fund_id].assets
        for (_, fund_id), group in weights.groupby(["date", "fund_id"], sort=False)
    )
    return (
        membership_ok
        and returns.reset_index(drop=True).equals(expected_returns.reset_index(drop=True))
        and weights.reset_index(drop=True).equals(expected_weights.reset_index(drop=True))
        and metrics.reset_index(drop=True).equals(expected_metrics.reset_index(drop=True))
        and diagnostics.reset_index(drop=True).equals(expected_diagnostics.reset_index(drop=True))
    )


def _reconcile_metrics(
    returns: pd.DataFrame, metrics: pd.DataFrame, *, tolerance: float = 5e-10
) -> bool:
    metric_map = metrics.set_index("fund_id")
    for spec in FUND_SPECS:
        fund = returns.loc[returns["fund_id"].eq(spec.fund_id)].sort_values("date")
        if fund.empty or spec.fund_id not in metric_map.index:
            return False
        row = metric_map.loc[spec.fund_id]
        net = _metric_values(fund["net_return"], spec.annualisation)
        gross = _metric_values(fund["gross_return"], spec.annualisation)
        rebalances = fund.loc[fund["is_rebalance"].astype(bool)]
        cost_bearing = rebalances.iloc[1:]
        expected = {
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
        }
        if any(not np.isclose(float(row[key]), value, rtol=0, atol=tolerance) for key, value in expected.items()):
            return False
        if (
            pd.Timestamp(row["start_date"]) != pd.Timestamp(fund["date"].iloc[0])
            or pd.Timestamp(row["end_date"]) != pd.Timestamp(fund["date"].iloc[-1])
            or int(row["observations"]) != len(fund)
            or int(row["annualisation"]) != spec.annualisation
            or float(row["transaction_cost_bps"]) != 5.0
            or int(row["rebalance_count"]) != len(rebalances)
        ):
            return False
    return True


def _reconcile_to_sources(
    returns: pd.DataFrame,
    weights: pd.DataFrame,
    family_matrices: dict[str, pd.DataFrame],
    *,
    tolerance: float = 5e-10,
) -> tuple[bool, str]:
    for spec in FUND_SPECS:
        matrix = family_matrices[spec.family].sort_index(kind="mergesort")
        complete = matrix.loc[matrix.notna().all(axis=1)]
        schedule = _expected_monthly_dates(matrix, spec.window)
        expected_live = complete.loc[complete.index >= schedule[0]]
        fund = returns.loc[returns["fund_id"].eq(spec.fund_id)].sort_values("date")
        if tuple(pd.to_datetime(fund["date"])) != tuple(expected_live.index):
            return False, f"{spec.fund_id}: live calendar differs"
        fund_weights = weights.loc[weights["fund_id"].eq(spec.fund_id)]
        current: np.ndarray | None = None
        for output in fund.itertuples():
            date = pd.Timestamp(output.date)
            expected_rebalance = date in set(schedule)
            if bool(output.is_rebalance) != expected_rebalance:
                return False, f"{spec.fund_id}: rebalance schedule differs at {date.date()}"
            if expected_rebalance:
                holding = fund_weights.loc[pd.to_datetime(fund_weights["date"]).eq(date)].set_index("ticker").reindex(spec.assets)
                if holding["target_weight"].isna().any():
                    return False, f"{spec.fund_id}: missing holdings at {date.date()}"
                target = holding["target_weight"].to_numpy(dtype="float64")
                pretrade = holding["pretrade_weight"].to_numpy(dtype="float64")
                trade = holding["trade_weight"].to_numpy(dtype="float64")
                expected_pretrade = np.zeros(len(target)) if current is None else current
                if not np.allclose(pretrade, expected_pretrade, rtol=0, atol=tolerance):
                    return False, f"{spec.fund_id}: pretrade drift differs at {date.date()}"
                if not np.allclose(trade, target - expected_pretrade, rtol=0, atol=tolerance):
                    return False, f"{spec.fund_id}: trade weights differ at {date.date()}"
                expected_turnover = 0.0 if current is None else 0.5 * float(np.abs(target - current).sum())
                pre_return = target
            else:
                if current is None:
                    return False, f"{spec.fund_id}: no current holdings"
                expected_turnover = 0.0
                pre_return = current
            asset_return = complete.loc[date, list(spec.assets)].to_numpy(dtype="float64")
            expected_gross = float(pre_return @ asset_return)
            expected_cost = TRANSACTION_COST_RATE * expected_turnover
            expected_net = (1.0 - expected_cost) * (1.0 + expected_gross) - 1.0
            observed = [output.turnover, output.transaction_cost, output.gross_return, output.net_return]
            expected = [expected_turnover, expected_cost, expected_gross, expected_net]
            if not np.allclose(observed, expected, rtol=0, atol=tolerance):
                return False, f"{spec.fund_id}: return/cost reconciliation differs at {date.date()}"
            current = pre_return * (1.0 + asset_return) / (1.0 + expected_gross)
    return True, "all source returns, drifted weights, turnover, and costs reconcile"


def validate_portfolio_outputs(
    *,
    fund_returns: pd.DataFrame,
    fund_weights: pd.DataFrame,
    performance_metrics: pd.DataFrame,
    solver_diagnostics: pd.DataFrame,
    sensitivity_metrics: pd.DataFrame | None = None,
    family_matrices: dict[str, pd.DataFrame] | None = None,
    require_sensitivity: bool = False,
) -> ValidationReport:
    """Validate canonical artifacts; pass matrices for the pre-write audit."""
    report = ValidationReport()
    returns = fund_returns.copy(deep=True)
    weights = fund_weights.copy(deep=True)
    metrics = performance_metrics.copy(deep=True)
    diagnostics = solver_diagnostics.copy(deep=True)
    for frame in (returns, weights, diagnostics):
        if "date" in frame:
            frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    for column in ("start_date", "end_date"):
        if column in metrics:
            metrics[column] = pd.to_datetime(metrics[column], errors="coerce")

    report.add(
        _columns_equal(returns, FUND_RETURN_COLUMNS),
        "fund_return_schema",
        "Fund-return columns exactly match the frozen schema.",
        "Fund-return columns differ from the frozen schema.",
        observed=tuple(returns.columns), expected=FUND_RETURN_COLUMNS,
    )
    report.add(
        _columns_equal(weights, FUND_WEIGHT_COLUMNS),
        "fund_weight_schema",
        "Fund-weight columns exactly match the frozen schema.",
        "Fund-weight columns differ from the frozen schema.",
        observed=tuple(weights.columns), expected=FUND_WEIGHT_COLUMNS,
    )
    report.add(
        _columns_equal(metrics, PERFORMANCE_METRIC_COLUMNS),
        "performance_schema",
        "Performance columns exactly match the frozen schema.",
        "Performance columns differ from the frozen schema.",
        observed=tuple(metrics.columns), expected=PERFORMANCE_METRIC_COLUMNS,
    )
    report.add(
        set(SOLVER_DIAGNOSTIC_REQUIRED_COLUMNS).issubset(diagnostics.columns),
        "solver_diagnostic_schema",
        "Solver diagnostics contain every required field.",
        "Solver diagnostics omit a required field.",
    )

    ids_ok = (
        set(returns["fund_id"].unique()) == set(FUND_IDS)
        and set(weights["fund_id"].unique()) == set(FUND_IDS)
        and tuple(metrics["fund_id"]) == FUND_IDS
        and set(diagnostics["fund_id"].unique()) == set(FUND_IDS)
    )
    report.add(
        ids_ok, "twelve_funds", "All twelve frozen funds are present in order.",
        "Fund membership or order differs from the frozen twelve.",
    )
    report.add(
        _unique_key(returns, ["date", "fund_id"])
        and _unique_key(weights, ["date", "fund_id", "ticker"])
        and _unique_key(metrics, ["fund_id"])
        and _unique_key(diagnostics, ["date", "fund_id"]),
        "portfolio_keys", "All output keys are complete and unique.",
        "An output key is missing or duplicated.",
    )

    numeric_return_columns = ["gross_return", "turnover", "transaction_cost", "net_return"]
    numeric_weight_columns = ["pretrade_weight", "target_weight", "trade_weight", "turnover"]
    numeric_metric_columns = [column for column in PERFORMANCE_METRIC_COLUMNS if column not in {"fund_id", "family", "method", "start_date", "end_date"}]
    report.add(
        len(returns) > 0 and len(weights) > 0 and len(metrics) == 12
        and _finite(returns, numeric_return_columns)
        and _finite(weights, numeric_weight_columns)
        and _finite(metrics, numeric_metric_columns)
        and returns["gross_return"].gt(-1).all()
        and returns["net_return"].gt(-1).all(),
        "substantive_finite_outputs", "Outputs are substantive, finite, and have valid returns.",
        "An output is empty, non-finite, placeholder-like, or has return <= -1.",
    )

    target_sums = weights.groupby(["date", "fund_id"], sort=False)["target_weight"].sum()
    bounds_ok = (
        weights["target_weight"].ge(-CONSTRAINT_TOLERANCE).all()
        and weights["target_weight"].le(WEIGHT_CAP + CONSTRAINT_TOLERANCE).all()
        and np.allclose(target_sums.to_numpy(), 1.0, rtol=0, atol=CONSTRAINT_TOLERANCE)
    )
    report.add(
        bounds_ok, "weight_constraints", "All targets are long-only, capped, and fully invested.",
        "At least one target breaches the frozen constraints.",
        observed=(float(weights["target_weight"].min()), float(weights["target_weight"].max()), float((target_sums - 1).abs().max())),
        expected=(0.0, WEIGHT_CAP, CONSTRAINT_TOLERANCE),
    )

    initial_ok = True
    for fund_id, group in returns.groupby("fund_id", sort=False):
        first = group.sort_values("date").iloc[0]
        initial_weights = weights.loc[
            weights["fund_id"].eq(fund_id)
            & pd.to_datetime(weights["date"]).eq(pd.Timestamp(first["date"]))
        ]
        initial_ok &= (
            bool(first["is_rebalance"])
            and float(first["turnover"]) == 0.0
            and float(first["transaction_cost"]) == 0.0
            and initial_weights["pretrade_weight"].eq(0).all()
            and np.allclose(initial_weights["trade_weight"], initial_weights["target_weight"], rtol=0, atol=1e-12)
        )
    non_rebalance = returns.loc[~returns["is_rebalance"].astype(bool)]
    report.add(
        initial_ok
        and non_rebalance["turnover"].eq(0).all()
        and non_rebalance["transaction_cost"].eq(0).all()
        and np.allclose(
            returns["net_return"],
            (1.0 - returns["transaction_cost"]) * (1.0 + returns["gross_return"]) - 1.0,
            rtol=0, atol=5e-12,
        ),
        "turnover_cost_rules", "Initial formation, rebalance-only turnover, and 5-bps costs reconcile.",
        "Turnover timing, initial formation, or cost arithmetic differs from the frozen rules.",
    )

    report.add(
        diagnostics["solver_success"].astype(bool).all()
        and weights["solver_success"].astype(bool).all()
        and _finite(diagnostics, [
            "attempts", "status_code", "iterations", "objective_value",
            "sum_residual", "lower_bound_violation", "upper_bound_violation",
            "covariance_repair",
        ])
        and diagnostics["sum_residual"].le(CONSTRAINT_TOLERANCE).all()
        and diagnostics["lower_bound_violation"].le(CONSTRAINT_TOLERANCE).all()
        and diagnostics["upper_bound_violation"].le(CONSTRAINT_TOLERANCE).all()
        and _parse_solver_status(weights["solver_status"]),
        "solver_diagnostics", "Every solver/non-solver status is successful, feasible, and parseable.",
        "A solver status is unsuccessful, infeasible, non-finite, or unparseable.",
    )

    report.add(
        _reconcile_metrics(returns, metrics),
        "performance_reconciliation", "All performance metrics independently reconcile to fund returns.",
        "At least one performance metric does not independently reconcile.",
    )
    report.add(
        _check_ordering(returns, weights, metrics, diagnostics),
        "deterministic_order", "All outputs use frozen deterministic ordering.",
        "At least one output differs from the frozen order.",
    )

    if family_matrices is not None:
        source_ok, source_message = _reconcile_to_sources(returns, weights, family_matrices)
        report.add(
            source_ok, "source_return_reconciliation",
            "Fund returns, drift, turnover, costs, calendars, and first-live rules reconcile to source matrices.",
            f"Source reconciliation failed: {source_message}", observed=source_message,
        )
        equity_extremes = int(family_matrices["Equity"].abs().ge(0.25).sum().sum())
        crypto_extremes = int(family_matrices["Crypto"].abs().ge(0.25).sum().sum())
        report.add(
            (equity_extremes, crypto_extremes) == (4, 65),
            "canonical_extreme_retention", "Canonical matrices retain all 4 equity and 65 crypto extremes.",
            "Canonical extreme counts differ from the frozen 4/65 benchmark.",
            observed=(equity_extremes, crypto_extremes), expected=(4, 65),
        )

    if "near_identical_warning" in diagnostics:
        near_count = int(diagnostics["near_identical_warning"].astype(bool).sum())
        if near_count:
            report.warn(
                "near_identical_methods",
                "Valid near-identical target vectors were retained; diagnostics identify the affected methods for review.",
                observed=near_count,
            )
        else:
            report.add(True, "near_identical_methods", "No target pairs met the frozen near-identical threshold.", "")

    if sensitivity_metrics is None:
        report.add(
            not require_sensitivity,
            "extreme_sensitivity_output",
            "Sensitivity output is not required for this validation call.",
            "The authorised extreme-return sensitivity output is missing.",
        )
    else:
        sensitivity = sensitivity_metrics.copy(deep=True)
        delta_ok = (
            np.allclose(
                sensitivity["delta_net_annualised_return"],
                sensitivity["sensitivity_net_annualised_return"] - sensitivity["canonical_net_annualised_return"],
                rtol=0, atol=5e-12,
            )
            and np.allclose(
                sensitivity["delta_net_sharpe_ratio"],
                sensitivity["sensitivity_net_sharpe_ratio"] - sensitivity["canonical_net_sharpe_ratio"],
                rtol=0, atol=5e-12,
            )
            and np.allclose(
                sensitivity["delta_net_max_drawdown"],
                sensitivity["sensitivity_net_max_drawdown"] - sensitivity["canonical_net_max_drawdown"],
                rtol=0, atol=5e-12,
            )
        )
        report.add(
            _columns_equal(sensitivity, SENSITIVITY_COLUMNS)
            and tuple(sensitivity["fund_id"]) == FUND_IDS
            and _finite(sensitivity, list(SENSITIVITY_COLUMNS[3:]))
            and delta_ok,
            "extreme_sensitivity_output", "All twelve separately labelled sensitivity comparisons reconcile.",
            "Sensitivity schema, fund coverage, values, or deltas differ from the frozen scenario.",
        )
    return report


__all__ = [
    "FUND_RETURN_COLUMNS",
    "FUND_WEIGHT_COLUMNS",
    "PERFORMANCE_METRIC_COLUMNS",
    "SENSITIVITY_COLUMNS",
    "SOLVER_DIAGNOSTIC_REQUIRED_COLUMNS",
    "validate_portfolio_outputs",
]
