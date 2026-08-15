"""Frozen out-of-sample portfolio engine for FINS5545 Project B.

The module implements the student-approved Stage 4B specification.  It keeps
estimation strictly before each decision date, lets holdings drift between
monthly rebalances, and never writes files.  Output persistence is owned by
``scripts/run_part_b.py`` after the separate validation layer has passed.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from math import sqrt
from typing import Any, Callable, Sequence

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from src.features import build_combined_return_matrix
from src.validation import COMBINED_ASSETS, CRYPTO_TICKERS, EQUITY_TICKERS


WEIGHT_CAP = 0.20
TRANSACTION_COST_RATE = 0.0005
CONSTRAINT_TOLERANCE = 1e-8
NEAR_IDENTICAL_TOLERANCE = 1e-6
SLSQP_OPTIONS = {"maxiter": 2000, "ftol": 1e-12, "disp": False}


class PortfolioBlockError(RuntimeError):
    """Raised when a frozen portfolio invariant or solver condition fails."""

    def __init__(self, message: str, *, attempts: list[dict[str, Any]] | None = None):
        super().__init__(message)
        self.attempts = attempts or []


@dataclass(frozen=True)
class FundSpec:
    """One prespecified family-method fund."""

    fund_id: str
    family: str
    method: str
    method_key: str
    assets: tuple[str, ...]
    annualisation: int
    window: int


def _fund_specs() -> tuple[FundSpec, ...]:
    families = (
        ("equity", "Equity", EQUITY_TICKERS, 252, 252),
        ("crypto", "Crypto", CRYPTO_TICKERS, 365, 365),
        ("combined", "Combined", COMBINED_ASSETS, 252, 252),
    )
    methods = (
        ("equal_weight", "Equal Weight"),
        ("minimum_variance", "Minimum Variance"),
        ("maximum_sharpe", "Maximum Sharpe"),
        ("risk_parity", "Risk Parity"),
    )
    return tuple(
        FundSpec(
            fund_id=f"{family_key}_{method_key}",
            family=family,
            method=method,
            method_key=method_key,
            assets=tuple(assets),
            annualisation=annualisation,
            window=window,
        )
        for family_key, family, assets, annualisation, window in families
        for method_key, method in methods
    )


FUND_SPECS = _fund_specs()
FUND_IDS = tuple(spec.fund_id for spec in FUND_SPECS)
FUND_ORDER = {fund_id: position for position, fund_id in enumerate(FUND_IDS)}


def _wide_returns(
    long_returns: pd.DataFrame, assets: Sequence[str], *, name: str
) -> pd.DataFrame:
    required = {"date", "ticker", "return"}
    missing = sorted(required.difference(long_returns.columns))
    if missing:
        raise PortfolioBlockError(f"{name} is missing required columns: {missing}")
    if long_returns.duplicated(["date", "ticker"]).any():
        raise PortfolioBlockError(f"{name} has duplicate ticker-date keys")
    wide = long_returns.pivot(index="date", columns="ticker", values="return")
    missing_assets = sorted(set(assets).difference(wide.columns))
    if missing_assets:
        raise PortfolioBlockError(f"{name} is missing assets: {missing_assets}")
    wide = wide.loc[:, list(assets)].sort_index(kind="mergesort").astype("float64")
    wide.index = pd.DatetimeIndex(pd.to_datetime(wide.index), name="date")
    if not wide.index.is_unique or not wide.index.is_monotonic_increasing:
        raise PortfolioBlockError(f"{name} dates must be unique and ascending")
    return wide


def build_family_return_matrices(
    equity_returns: pd.DataFrame,
    native_crypto_returns: pd.DataFrame,
    aligned_crypto_returns: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Build canonical family matrices without changing native return timing."""
    equity = _wide_returns(equity_returns, EQUITY_TICKERS, name="equity returns")
    crypto = _wide_returns(
        native_crypto_returns, CRYPTO_TICKERS, name="native crypto returns"
    )
    combined = build_combined_return_matrix(
        equity_returns, aligned_crypto_returns
    ).astype("float64")
    if tuple(combined.columns) != COMBINED_ASSETS:
        raise PortfolioBlockError("combined matrix asset order differs from contract")
    return {"Equity": equity, "Crypto": crypto, "Combined": combined}


def build_clipped_sensitivity_matrices(
    family_matrices: dict[str, pd.DataFrame],
    *, lower: float = -0.25,
    upper: float = 0.25,
) -> dict[str, pd.DataFrame]:
    """Clip native returns before assembling the Combined robustness matrix."""
    equity = family_matrices["Equity"].clip(lower=lower, upper=upper)
    crypto = family_matrices["Crypto"].clip(lower=lower, upper=upper)
    selected_crypto = crypto.reindex(equity.index)
    if selected_crypto.isna().any().any():
        raise PortfolioBlockError(
            "native crypto sensitivity returns do not cover the equity calendar"
        )
    combined = pd.concat(
        [equity.loc[:, list(EQUITY_TICKERS)], selected_crypto.loc[:, list(CRYPTO_TICKERS)]],
        axis=1,
    )
    combined.columns = list(COMBINED_ASSETS)
    return {
        "Equity": equity.astype("float64"),
        "Crypto": crypto.astype("float64"),
        "Combined": combined.astype("float64"),
    }


def complete_return_rows(returns: pd.DataFrame) -> pd.DataFrame:
    """Select complete rows without filling or pairwise deletion."""
    if not isinstance(returns.index, pd.DatetimeIndex):
        raise PortfolioBlockError("return matrix must use a DatetimeIndex")
    ordered = returns.sort_index(kind="mergesort")
    complete = ordered.loc[ordered.notna().all(axis=1)].copy()
    values = complete.to_numpy(dtype="float64")
    if not np.isfinite(values).all():
        raise PortfolioBlockError("complete return matrix contains non-finite values")
    return complete


def monthly_rebalance_dates(
    returns: pd.DataFrame, window: int
) -> pd.DatetimeIndex:
    """Return the first observed eligible date in each calendar month."""
    complete = complete_return_rows(returns)
    if window <= 1 or len(complete) <= window:
        raise PortfolioBlockError("insufficient complete rows for frozen rolling window")
    eligible = complete.index[window:]
    first = pd.Series(eligible, index=eligible.to_period("M")).groupby(level=0).first()
    return pd.DatetimeIndex(first.to_numpy(), name="date")


def rolling_estimation_window(
    complete_returns: pd.DataFrame, decision_date: pd.Timestamp, window: int
) -> pd.DataFrame:
    """Return exactly ``window`` complete observations strictly before ``t``."""
    decision = pd.Timestamp(decision_date)
    estimation = complete_returns.loc[complete_returns.index < decision].tail(window)
    if len(estimation) != window:
        raise PortfolioBlockError(
            f"decision {decision.date()} has {len(estimation)} prior rows; expected {window}"
        )
    if estimation.index.max() >= decision or estimation.isna().any().any():
        raise PortfolioBlockError("estimation window violates completeness or strict timing")
    return estimation


def repair_covariance(covariance: np.ndarray) -> tuple[np.ndarray, float, float]:
    """Apply only the frozen deterministic numerical eigenvalue repair."""
    sigma = np.asarray(covariance, dtype="float64")
    sigma = (sigma + sigma.T) / 2.0
    if not np.isfinite(sigma).all() or sigma.ndim != 2 or sigma.shape[0] != sigma.shape[1]:
        raise PortfolioBlockError("covariance matrix is not finite and square")
    eigenvalues = np.linalg.eigvalsh(sigma)
    minimum = float(eigenvalues.min())
    scale = max(float(np.trace(sigma) / sigma.shape[0]), 1e-12)
    epsilon = 1e-10 * scale
    ridge = max(0.0, epsilon - minimum)
    if ridge:
        sigma = sigma + ridge * np.eye(sigma.shape[0], dtype="float64")
    return sigma, minimum, float(ridge)


def estimate_annualised_moments(
    estimation_returns: pd.DataFrame, annualisation: int
) -> tuple[np.ndarray, np.ndarray, float, float]:
    """Estimate frozen arithmetic mean and sample covariance on complete rows."""
    if estimation_returns.isna().any().any():
        raise PortfolioBlockError("pairwise covariance is prohibited")
    values = estimation_returns.to_numpy(dtype="float64")
    if not np.isfinite(values).all():
        raise PortfolioBlockError("estimation window contains non-finite values")
    mean = values.mean(axis=0) * annualisation
    covariance = np.cov(values, rowvar=False, ddof=1) * annualisation
    repaired, minimum, ridge = repair_covariance(covariance)
    if not np.isfinite(mean).all():
        raise PortfolioBlockError("annualised mean contains non-finite values")
    return mean, repaired, minimum, ridge


def minimum_variance_objective(weights: np.ndarray, covariance: np.ndarray) -> float:
    return float(weights @ covariance @ weights)


def minimum_variance_gradient(weights: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    return 2.0 * covariance @ weights


def negative_sharpe_objective(
    weights: np.ndarray, mean: np.ndarray, covariance: np.ndarray
) -> float:
    variance = float(weights @ covariance @ weights)
    if not np.isfinite(variance) or variance <= 0:
        return float("inf")
    return float(-(weights @ mean) / sqrt(variance))


def negative_sharpe_gradient(
    weights: np.ndarray, mean: np.ndarray, covariance: np.ndarray
) -> np.ndarray:
    sigma_w = covariance @ weights
    variance = float(weights @ sigma_w)
    if not np.isfinite(variance) or variance <= 0:
        return np.zeros_like(weights)
    portfolio_mean = float(weights @ mean)
    return -(mean / sqrt(variance) - portfolio_mean * sigma_w / variance ** 1.5)


def risk_parity_objective(weights: np.ndarray, covariance: np.ndarray) -> float:
    sigma_w = covariance @ weights
    variance = float(weights @ sigma_w)
    if not np.isfinite(variance) or variance <= 0:
        return float("inf")
    contributions = weights * sigma_w / variance
    differences = contributions - 1.0 / len(weights)
    return float(differences @ differences)


def risk_parity_gradient(weights: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    sigma_w = covariance @ weights
    variance = float(weights @ sigma_w)
    if not np.isfinite(variance) or variance <= 0:
        return np.zeros_like(weights)
    raw = weights * sigma_w
    normalised = raw / variance
    differences = normalised - 1.0 / len(weights)
    raw_jacobian = np.diag(sigma_w) + np.diag(weights) @ covariance
    normalised_jacobian = (
        raw_jacobian * variance - raw[:, None] * (2.0 * sigma_w)[None, :]
    ) / variance**2
    return 2.0 * differences @ normalised_jacobian


def _staggered_seed(number_assets: int) -> np.ndarray:
    if number_assets == 1:
        return np.ones(1, dtype="float64")
    indices = np.arange(number_assets, dtype="float64")
    raw = 1.0 + 0.01 * (2.0 * indices - (number_assets - 1)) / (number_assets - 1)
    return raw / raw.sum()


def _constraint_residuals(weights: np.ndarray) -> tuple[float, float, float]:
    sum_residual = abs(float(weights.sum()) - 1.0)
    lower = max(0.0, float(-weights.min()))
    upper = max(0.0, float(weights.max() - WEIGHT_CAP))
    return sum_residual, lower, upper


def solve_target_weights(
    estimation_returns: pd.DataFrame,
    method: str,
    annualisation: int,
    *,
    optimizer: Callable[..., Any] | None = None,
) -> tuple[np.ndarray, dict[str, Any]]:
    """Solve one frozen target vector, with at most one prespecified retry."""
    number_assets = estimation_returns.shape[1]
    if number_assets * WEIGHT_CAP < 1.0 - CONSTRAINT_TOLERANCE:
        raise PortfolioBlockError("the frozen 20% cap is infeasible for this universe")
    equal = np.full(number_assets, 1.0 / number_assets, dtype="float64")
    if method == "equal_weight":
        diagnostic = {
            "solver": "none",
            "solver_success": True,
            "attempts": 0,
            "status_code": 0,
            "message": "deterministic_equal_weight",
            "iterations": 0,
            "objective_value": 0.0,
            "sum_residual": abs(float(equal.sum()) - 1.0),
            "lower_bound_violation": 0.0,
            "upper_bound_violation": max(0.0, float(equal.max() - WEIGHT_CAP)),
            "covariance_repair": 0.0,
            "minimum_eigenvalue": 0.0,
            "attempt_details": [],
        }
        return equal, diagnostic

    mean, covariance, minimum_eigenvalue, ridge = estimate_annualised_moments(
        estimation_returns, annualisation
    )
    if method == "minimum_variance":
        objective = lambda w: minimum_variance_objective(w, covariance)
        gradient = lambda w: minimum_variance_gradient(w, covariance)
    elif method == "maximum_sharpe":
        objective = lambda w: negative_sharpe_objective(w, mean, covariance)
        gradient = lambda w: negative_sharpe_gradient(w, mean, covariance)
    elif method == "risk_parity":
        objective = lambda w: risk_parity_objective(w, covariance)
        gradient = lambda w: risk_parity_gradient(w, covariance)
    else:
        raise ValueError(f"unknown frozen portfolio method: {method}")

    solver = minimize if optimizer is None else optimizer
    constraints = ({"type": "eq", "fun": lambda w: float(w.sum() - 1.0), "jac": lambda w: np.ones_like(w)},)
    bounds = tuple((0.0, WEIGHT_CAP) for _ in range(number_assets))
    attempts: list[dict[str, Any]] = []
    final_weights: np.ndarray | None = None
    final_result: Any = None

    for attempt_number, (seed_name, seed) in enumerate(
        (("equal_weight", equal), ("staggered", _staggered_seed(number_assets))),
        start=1,
    ):
        try:
            result = solver(
                objective,
                seed.copy(),
                jac=gradient,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options=SLSQP_OPTIONS.copy(),
            )
            candidate = np.asarray(result.x, dtype="float64")
            value = float(objective(candidate))
            sum_residual, lower, upper = _constraint_residuals(candidate)
            valid = (
                bool(result.success)
                and candidate.shape == (number_assets,)
                and np.isfinite(candidate).all()
                and np.isfinite(value)
                and sum_residual <= CONSTRAINT_TOLERANCE
                and lower <= CONSTRAINT_TOLERANCE
                and upper <= CONSTRAINT_TOLERANCE
            )
            detail = {
                "attempt": attempt_number,
                "initial_value": seed_name,
                "success": bool(result.success),
                "valid": bool(valid),
                "status_code": int(getattr(result, "status", -1)),
                "message": str(getattr(result, "message", "")),
                "iterations": int(getattr(result, "nit", 0)),
                "objective_value": value,
                "sum_residual": sum_residual,
                "lower_bound_violation": lower,
                "upper_bound_violation": upper,
            }
        except Exception as exc:
            result = None
            candidate = np.full(number_assets, np.nan)
            valid = False
            detail = {
                "attempt": attempt_number,
                "initial_value": seed_name,
                "success": False,
                "valid": False,
                "status_code": -1,
                "message": f"{type(exc).__name__}: {exc}",
                "iterations": 0,
                "objective_value": None,
                "sum_residual": None,
                "lower_bound_violation": None,
                "upper_bound_violation": None,
            }
        attempts.append(detail)
        if valid:
            final_weights = candidate
            final_result = result
            break

    if final_weights is None or final_result is None:
        raise PortfolioBlockError(
            f"{method} failed both authorised SLSQP attempts", attempts=attempts
        )

    sum_residual, lower, upper = _constraint_residuals(final_weights)
    diagnostic = {
        "solver": "SLSQP",
        "solver_success": True,
        "attempts": len(attempts),
        "status_code": int(final_result.status),
        "message": str(final_result.message),
        "iterations": int(final_result.nit),
        "objective_value": float(objective(final_weights)),
        "sum_residual": sum_residual,
        "lower_bound_violation": lower,
        "upper_bound_violation": upper,
        "covariance_repair": ridge,
        "minimum_eigenvalue": minimum_eigenvalue,
        "attempt_details": attempts,
    }
    return final_weights, diagnostic


def drift_weights(weights: np.ndarray, asset_returns: np.ndarray) -> np.ndarray:
    """Apply one day of holdings drift using the frozen gross-return rule."""
    weights = np.asarray(weights, dtype="float64")
    asset_returns = np.asarray(asset_returns, dtype="float64")
    gross_return = float(weights @ asset_returns)
    if not np.isfinite(gross_return) or gross_return <= -1.0:
        raise PortfolioBlockError("portfolio gross return is non-finite or <= -1")
    drifted = weights * (1.0 + asset_returns) / (1.0 + gross_return)
    if not np.isfinite(drifted).all() or abs(float(drifted.sum()) - 1.0) > 1e-8:
        raise PortfolioBlockError("post-return holdings drift is invalid")
    return drifted


def performance_metrics(
    daily_returns: pd.Series, periods_per_year: int = 252
) -> dict[str, float]:
    """Calculate the frozen geometric, volatility, Sharpe, and drawdown metrics."""
    values = pd.Series(daily_returns, dtype="float64").dropna()
    if len(values) < 2 or not np.isfinite(values).all() or values.le(-1.0).any():
        raise PortfolioBlockError("performance series is insufficient or invalid")
    wealth = (1.0 + values).cumprod()
    if not np.isfinite(wealth).all() or wealth.iloc[-1] <= 0:
        raise PortfolioBlockError("compounded wealth is non-positive or non-finite")
    cumulative = float(wealth.iloc[-1] - 1.0)
    annualised_return = float(wealth.iloc[-1] ** (periods_per_year / len(values)) - 1.0)
    daily_std = float(values.std(ddof=1))
    if not np.isfinite(daily_std) or daily_std <= 0:
        raise PortfolioBlockError("performance volatility is zero or non-finite")
    annualised_volatility = daily_std * sqrt(periods_per_year)
    sharpe = float(values.mean() / daily_std * sqrt(periods_per_year))
    drawdown = wealth.div(wealth.cummax()).sub(1.0)
    maximum_drawdown = float(drawdown.min())
    metrics = {
        "cumulative_return": cumulative,
        "annualised_return": annualised_return,
        "annualised_volatility": annualised_volatility,
        "sharpe_ratio": sharpe,
        "max_drawdown": maximum_drawdown,
    }
    if not np.isfinite(list(metrics.values())).all():
        raise PortfolioBlockError("performance calculation produced a non-finite metric")
    return metrics


def _performance_row(fund_returns: pd.DataFrame, spec: FundSpec) -> dict[str, Any]:
    net = performance_metrics(fund_returns["net_return"], spec.annualisation)
    gross = performance_metrics(fund_returns["gross_return"], spec.annualisation)
    rebalances = fund_returns.loc[fund_returns["is_rebalance"]]
    cost_bearing = rebalances.iloc[1:]
    return {
        "fund_id": spec.fund_id,
        "family": spec.family,
        "method": spec.method,
        "start_date": pd.Timestamp(fund_returns["date"].iloc[0]),
        "end_date": pd.Timestamp(fund_returns["date"].iloc[-1]),
        "observations": int(len(fund_returns)),
        "annualisation": int(spec.annualisation),
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
        "rebalance_count": int(len(rebalances)),
    }


def run_fund_backtest(
    returns: pd.DataFrame,
    spec: FundSpec,
    *,
    optimizer: Callable[..., Any] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any], pd.DataFrame]:
    """Run one fully prespecified walk-forward fund in memory."""
    if tuple(returns.columns) != spec.assets:
        raise PortfolioBlockError(f"{spec.fund_id} asset order differs from its frozen order")
    complete = complete_return_rows(returns)
    rebalances = monthly_rebalance_dates(complete, spec.window)
    live = complete.loc[complete.index >= rebalances[0]]
    rebalance_set = set(rebalances)
    current_weights: np.ndarray | None = None
    return_rows: list[dict[str, Any]] = []
    weight_rows: list[dict[str, Any]] = []
    diagnostic_rows: list[dict[str, Any]] = []

    for date, row in live.iterrows():
        is_rebalance = date in rebalance_set
        turnover = 0.0
        transaction_cost = 0.0
        if is_rebalance:
            estimation = rolling_estimation_window(complete, date, spec.window)
            target, diagnostic = solve_target_weights(
                estimation,
                spec.method_key,
                spec.annualisation,
                optimizer=optimizer,
            )
            initial = current_weights is None
            pretrade = np.zeros(len(target), dtype="float64") if initial else current_weights.copy()
            trade = target - pretrade
            if not initial:
                turnover = 0.5 * float(np.abs(trade).sum())
                transaction_cost = TRANSACTION_COST_RATE * turnover
            pre_return = target
            status_json = json.dumps(diagnostic, sort_keys=True, separators=(",", ":"))
            for ticker, pre, target_value, trade_value in zip(
                spec.assets, pretrade, target, trade, strict=True
            ):
                weight_rows.append(
                    {
                        "date": date,
                        "fund_id": spec.fund_id,
                        "family": spec.family,
                        "method": spec.method,
                        "ticker": ticker,
                        "pretrade_weight": float(pre),
                        "target_weight": float(target_value),
                        "trade_weight": float(trade_value),
                        "turnover": turnover,
                        "solver_success": bool(diagnostic["solver_success"]),
                        "solver_status": status_json,
                    }
                )
            diagnostic_rows.append(
                {
                    "date": date,
                    "fund_id": spec.fund_id,
                    "family": spec.family,
                    "method": spec.method,
                    "solver_success": bool(diagnostic["solver_success"]),
                    "attempts": int(diagnostic["attempts"]),
                    "status_code": int(diagnostic["status_code"]),
                    "message": str(diagnostic["message"]),
                    "iterations": int(diagnostic["iterations"]),
                    "objective_value": float(diagnostic["objective_value"]),
                    "sum_residual": float(diagnostic["sum_residual"]),
                    "lower_bound_violation": float(diagnostic["lower_bound_violation"]),
                    "upper_bound_violation": float(diagnostic["upper_bound_violation"]),
                    "covariance_repair": float(diagnostic["covariance_repair"]),
                    "minimum_eigenvalue": float(diagnostic["minimum_eigenvalue"]),
                    "retry_used": bool(diagnostic["attempts"] > 1),
                }
            )
        else:
            if current_weights is None:
                raise PortfolioBlockError("live series began without an initial rebalance")
            pre_return = current_weights

        asset_returns = row.to_numpy(dtype="float64")
        gross_return = float(pre_return @ asset_returns)
        if not np.isfinite(gross_return) or gross_return <= -1.0:
            raise PortfolioBlockError(f"invalid gross return for {spec.fund_id} on {date}")
        net_return = (1.0 - transaction_cost) * (1.0 + gross_return) - 1.0
        if not np.isfinite(net_return) or net_return <= -1.0:
            raise PortfolioBlockError(f"invalid net return for {spec.fund_id} on {date}")
        return_rows.append(
            {
                "date": date,
                "fund_id": spec.fund_id,
                "family": spec.family,
                "method": spec.method,
                "gross_return": gross_return,
                "turnover": turnover,
                "transaction_cost": transaction_cost,
                "net_return": net_return,
                "is_rebalance": bool(is_rebalance),
            }
        )
        current_weights = drift_weights(pre_return, asset_returns)

    fund_returns = pd.DataFrame(return_rows)
    weights = pd.DataFrame(weight_rows)
    diagnostics = pd.DataFrame(diagnostic_rows)
    return fund_returns, weights, _performance_row(fund_returns, spec), diagnostics


def _sort_outputs(
    returns: pd.DataFrame, weights: pd.DataFrame, diagnostics: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    for frame in (returns, weights, diagnostics):
        frame["_fund_order"] = frame["fund_id"].map(FUND_ORDER)
    returns = returns.sort_values(["date", "_fund_order"], kind="mergesort").drop(columns="_fund_order").reset_index(drop=True)
    weights["_asset_order"] = weights.groupby("fund_id", sort=False).cumcount() % weights.groupby("fund_id", sort=False)["ticker"].transform("nunique")
    weights = weights.sort_values(["date", "_fund_order", "_asset_order"], kind="mergesort").drop(columns=["_fund_order", "_asset_order"]).reset_index(drop=True)
    diagnostics = diagnostics.sort_values(["date", "_fund_order"], kind="mergesort").drop(columns="_fund_order").reset_index(drop=True)
    return returns, weights, diagnostics


def _annotate_near_identical(
    weights: pd.DataFrame, diagnostics: pd.DataFrame
) -> pd.DataFrame:
    warnings: dict[tuple[pd.Timestamp, str], list[str]] = {}
    for (date, family), group in weights.groupby(["date", "family"], sort=False):
        pivots = {
            fund_id: sub.set_index("ticker")["target_weight"]
            for fund_id, sub in group.groupby("fund_id", sort=False)
        }
        ids = list(pivots)
        for left_position, left in enumerate(ids):
            for right in ids[left_position + 1 :]:
                difference = float((pivots[left] - pivots[right]).abs().max())
                if difference <= NEAR_IDENTICAL_TOLERANCE:
                    warnings.setdefault((pd.Timestamp(date), left), []).append(right)
                    warnings.setdefault((pd.Timestamp(date), right), []).append(left)
    result = diagnostics.copy()
    result["near_identical_with"] = [
        ";".join(warnings.get((pd.Timestamp(row.date), row.fund_id), []))
        for row in result.itertuples()
    ]
    result["near_identical_warning"] = result["near_identical_with"].ne("")
    result["near_identical_explanation"] = np.where(
        result["near_identical_warning"],
        "Valid target equivalence under the same data and constraints; retain outputs and review objectives, binding bounds, and mathematical equivalence.",
        "",
    )
    return result


def run_portfolio_suite(
    family_matrices: dict[str, pd.DataFrame],
    *,
    optimizer: Callable[..., Any] | None = None,
) -> dict[str, pd.DataFrame]:
    """Run all twelve funds and return deterministic in-memory artifacts."""
    return_frames: list[pd.DataFrame] = []
    weight_frames: list[pd.DataFrame] = []
    metric_rows: list[dict[str, Any]] = []
    diagnostic_frames: list[pd.DataFrame] = []
    for spec in FUND_SPECS:
        fund_returns, weights, metrics, diagnostics = run_fund_backtest(
            family_matrices[spec.family], spec, optimizer=optimizer
        )
        return_frames.append(fund_returns)
        weight_frames.append(weights)
        metric_rows.append(metrics)
        diagnostic_frames.append(diagnostics)
    returns, weights, diagnostics = _sort_outputs(
        pd.concat(return_frames, ignore_index=True),
        pd.concat(weight_frames, ignore_index=True),
        pd.concat(diagnostic_frames, ignore_index=True),
    )
    diagnostics = _annotate_near_identical(weights, diagnostics)
    metrics = pd.DataFrame(metric_rows)
    metrics["_fund_order"] = metrics["fund_id"].map(FUND_ORDER)
    metrics = metrics.sort_values("_fund_order", kind="mergesort").drop(columns="_fund_order").reset_index(drop=True)
    return {
        "fund_returns": returns,
        "fund_weights": weights,
        "performance_metrics": metrics,
        "solver_diagnostics": diagnostics,
    }


def build_extreme_sensitivity_metrics(
    canonical_metrics: pd.DataFrame, sensitivity_metrics: pd.DataFrame
) -> pd.DataFrame:
    """Compare all twelve robustness rows without replacing canonical results."""
    selected = ["fund_id", "family", "method", "net_annualised_return", "net_sharpe_ratio", "net_max_drawdown"]
    canonical = canonical_metrics.loc[:, selected].rename(
        columns={
            "net_annualised_return": "canonical_net_annualised_return",
            "net_sharpe_ratio": "canonical_net_sharpe_ratio",
            "net_max_drawdown": "canonical_net_max_drawdown",
        }
    )
    sensitivity = sensitivity_metrics.loc[:, ["fund_id", "net_annualised_return", "net_sharpe_ratio", "net_max_drawdown"]].rename(
        columns={
            "net_annualised_return": "sensitivity_net_annualised_return",
            "net_sharpe_ratio": "sensitivity_net_sharpe_ratio",
            "net_max_drawdown": "sensitivity_net_max_drawdown",
        }
    )
    comparison = canonical.merge(sensitivity, on="fund_id", validate="one_to_one")
    comparison["delta_net_annualised_return"] = comparison["sensitivity_net_annualised_return"] - comparison["canonical_net_annualised_return"]
    comparison["delta_net_sharpe_ratio"] = comparison["sensitivity_net_sharpe_ratio"] - comparison["canonical_net_sharpe_ratio"]
    comparison["delta_net_max_drawdown"] = comparison["sensitivity_net_max_drawdown"] - comparison["canonical_net_max_drawdown"]
    columns = [
        "fund_id", "family", "method",
        "canonical_net_annualised_return", "sensitivity_net_annualised_return", "delta_net_annualised_return",
        "canonical_net_sharpe_ratio", "sensitivity_net_sharpe_ratio", "delta_net_sharpe_ratio",
        "canonical_net_max_drawdown", "sensitivity_net_max_drawdown", "delta_net_max_drawdown",
    ]
    comparison["_fund_order"] = comparison["fund_id"].map(FUND_ORDER)
    return comparison.sort_values("_fund_order", kind="mergesort").drop(columns="_fund_order").loc[:, columns].reset_index(drop=True)


def oos_backtest(
    returns: pd.DataFrame,
    method: str = "minimum_variance",
    *,
    family: str = "Equity",
    annualisation: int = 252,
    window: int = 252,
) -> dict[str, pd.DataFrame]:
    """Public single-fund compatibility wrapper around the frozen engine."""
    method_labels = {
        "equal_weight": "Equal Weight",
        "minimum_variance": "Minimum Variance",
        "min_variance": "Minimum Variance",
        "maximum_sharpe": "Maximum Sharpe",
        "max_sharpe": "Maximum Sharpe",
        "risk_parity": "Risk Parity",
    }
    key_alias = {"min_variance": "minimum_variance", "max_sharpe": "maximum_sharpe"}
    method_key = key_alias.get(method, method)
    if method_key not in method_labels:
        raise ValueError(f"unknown method: {method}")
    spec = FundSpec(
        fund_id=f"{family.lower()}_{method_key}",
        family=family,
        method=method_labels[method_key],
        method_key=method_key,
        assets=tuple(returns.columns),
        annualisation=annualisation,
        window=window,
    )
    fund_returns, weights, metrics, diagnostics = run_fund_backtest(returns, spec)
    return {
        "fund_returns": fund_returns,
        "fund_weights": weights,
        "performance_metrics": pd.DataFrame([metrics]),
        "solver_diagnostics": diagnostics,
    }


__all__ = [
    "CONSTRAINT_TOLERANCE",
    "FUND_IDS",
    "FUND_ORDER",
    "FUND_SPECS",
    "FundSpec",
    "NEAR_IDENTICAL_TOLERANCE",
    "PortfolioBlockError",
    "SLSQP_OPTIONS",
    "TRANSACTION_COST_RATE",
    "WEIGHT_CAP",
    "build_clipped_sensitivity_matrices",
    "build_extreme_sensitivity_metrics",
    "build_family_return_matrices",
    "complete_return_rows",
    "drift_weights",
    "estimate_annualised_moments",
    "minimum_variance_objective",
    "monthly_rebalance_dates",
    "negative_sharpe_objective",
    "oos_backtest",
    "performance_metrics",
    "repair_covariance",
    "risk_parity_objective",
    "rolling_estimation_window",
    "run_fund_backtest",
    "run_portfolio_suite",
    "solve_target_weights",
]
