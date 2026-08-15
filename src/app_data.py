"""Cached, read-only access to MAIA's precomputed canonical artifacts.

The deployed app is intentionally downstream-only.  This module resolves every
artifact relative to the Project B root, validates its public contract, and
returns defensive copies.  It never calls the protected raw-data loader and it
never writes to the project.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

import pandas as pd
import streamlit as st


PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[1]

FUND_IDS: Final[tuple[str, ...]] = (
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
ELIGIBLE_BASE_IDS: Final[tuple[str, ...]] = (
    "equity_equal_weight",
    "equity_minimum_variance",
    "equity_maximum_sharpe",
    "equity_risk_parity",
    "combined_equal_weight",
    "combined_minimum_variance",
    "combined_maximum_sharpe",
    "combined_risk_parity",
)
VARIANTS: Final[tuple[str, ...]] = (
    "plain_vader_naive",
    "finance_vader_naive",
    "evidence_aware_finance",
)
OVERLAY_IDS: Final[tuple[str, ...]] = tuple(
    f"{fund_id}__{variant}"
    for fund_id in ELIGIBLE_BASE_IDS
    for variant in VARIANTS
)
SECTOR_ORDER: Final[tuple[str, ...]] = (
    "Tech",
    "Financials",
    "Energy",
    "Consumer",
    "Industrials",
    "Healthcare",
    "Comm",
    "Materials",
    "Utilities",
    "RealEstate",
)


class ArtifactError(RuntimeError):
    """A human-readable canonical-artifact contract failure."""


@dataclass(frozen=True)
class ArtifactSpec:
    relative_path: str
    columns: tuple[str, ...]
    date_columns: tuple[str, ...]
    key_columns: tuple[str, ...]
    sort_columns: tuple[str, ...]
    expected_rows: int | None
    purpose: str


ARTIFACT_SPECS: Final[dict[str, ArtifactSpec]] = {
    "fund_returns": ArtifactSpec(
        "results/data/fund_returns.csv",
        (
            "date", "fund_id", "family", "method", "gross_return", "turnover",
            "transaction_cost", "net_return", "is_rebalance",
        ),
        ("date",),
        ("date", "fund_id"),
        ("date", "fund_id"),
        10_404,
        "Daily gross and net paths for the twelve frozen base funds.",
    ),
    "fund_weights": ArtifactSpec(
        "results/data/fund_weights.csv",
        (
            "date", "fund_id", "family", "method", "ticker", "pretrade_weight",
            "target_weight", "trade_weight", "turnover", "solver_success",
            "solver_status",
        ),
        ("date",),
        ("date", "fund_id", "ticker"),
        ("date", "fund_id", "ticker"),
        17_280,
        "Rebalance-level base-fund holdings and trade audit fields.",
    ),
    "performance_metrics": ArtifactSpec(
        "results/tables/performance_metrics.csv",
        (
            "fund_id", "family", "method", "start_date", "end_date",
            "observations", "annualisation", "transaction_cost_bps",
            "net_cumulative_return", "net_annualised_return",
            "net_annualised_volatility", "net_sharpe_ratio",
            "net_max_drawdown", "gross_cumulative_return",
            "gross_annualised_return", "gross_sharpe_ratio",
            "average_rebalance_turnover", "total_turnover", "rebalance_count",
        ),
        ("start_date", "end_date"),
        ("fund_id",),
        ("fund_id",),
        12,
        "Canonical fact-sheet metrics for every base fund.",
    ),
    "solver_diagnostics": ArtifactSpec(
        "results/tables/portfolio_solver_diagnostics.csv",
        (
            "date", "fund_id", "family", "method", "solver_success", "attempts",
            "status_code", "message", "iterations", "objective_value",
            "sum_residual", "lower_bound_violation", "upper_bound_violation",
            "covariance_repair", "minimum_eigenvalue", "retry_used",
            "near_identical_with", "near_identical_warning",
            "near_identical_explanation",
        ),
        ("date",),
        ("date", "fund_id"),
        ("date", "fund_id"),
        432,
        "Solver status, retry, and constraint evidence.",
    ),
    "extreme_sensitivity": ArtifactSpec(
        "results/tables/extreme_sensitivity_metrics.csv",
        (
            "fund_id", "family", "method",
            "canonical_net_annualised_return",
            "sensitivity_net_annualised_return", "delta_net_annualised_return",
            "canonical_net_sharpe_ratio", "sensitivity_net_sharpe_ratio",
            "delta_net_sharpe_ratio", "canonical_net_max_drawdown",
            "sensitivity_net_max_drawdown", "delta_net_max_drawdown",
        ),
        (),
        ("fund_id",),
        ("fund_id",),
        12,
        "Separately labelled +/-25% native-return robustness evidence.",
    ),
    "sector_sentiment": ArtifactSpec(
        "results/data/sector_sentiment_index.csv",
        (
            "date", "sector", "sector_display", "headline_count",
            "ticker_count_with_news", "ticker_coverage", "plain_compound",
            "finance_compound", "mean_reliability", "evidence_aware_compound",
            "plain_z", "finance_z", "evidence_aware_z",
        ),
        ("date",),
        ("date", "sector"),
        ("date", "sector"),
        10_060,
        "Complete precomputed ten-sector sentiment panel.",
    ),
    "ticker_sentiment": ArtifactSpec(
        "results/data/ticker_sentiment_daily.csv",
        (
            "date", "ticker", "sector", "headline_count", "has_news",
            "plain_score", "finance_score", "covered_headline_share",
            "nonneutral_headline_count", "directional_agreement",
            "volume_evidence", "reliability", "custom_finance_term_hit_share",
            "evidence_aware_compound", "plain_z", "finance_z",
            "evidence_aware_signal", "signal_source_date",
            "lagged_plain_signal", "lagged_finance_signal",
            "lagged_evidence_aware_signal",
        ),
        ("date", "signal_source_date"),
        ("date", "ticker"),
        ("date", "ticker"),
        50_300,
        "Complete precomputed ticker-day sentiment and lag panel.",
    ),
    "fusion_returns": ArtifactSpec(
        "results/data/fusion_returns.csv",
        (
            "date", "overlay_id", "base_fund_id", "family", "method", "variant",
            "gross_return", "turnover", "transaction_cost", "net_return",
            "is_rebalance",
        ),
        ("date",),
        ("date", "overlay_id"),
        ("date", "overlay_id"),
        18_072,
        "Daily paths for all 24 frozen sentiment overlays.",
    ),
    "fusion_weights": ArtifactSpec(
        "results/data/fusion_weights.csv",
        (
            "date", "overlay_id", "base_fund_id", "family", "method", "variant",
            "ticker", "base_target_weight", "pretrade_weight",
            "signal_source_date", "signal_value", "multiplier",
            "raw_tilted_value", "target_weight", "trade_weight", "turnover",
            "projection_success", "projection_status",
        ),
        ("date", "signal_source_date"),
        ("date", "overlay_id", "ticker"),
        ("date", "overlay_id", "ticker"),
        47_520,
        "Rebalance holdings and projection evidence for all overlays.",
    ),
    "sentiment_diagnostics": ArtifactSpec(
        "results/tables/sentiment_diagnostics.csv",
        (
            "scope", "entity", "model", "metric", "value", "numerator",
            "denominator", "start_date", "end_date", "notes",
        ),
        ("start_date", "end_date"),
        ("scope", "entity", "model", "metric"),
        ("scope", "entity", "model", "metric"),
        70,
        "Mapped-headline, coverage, reliability, and active-tilt diagnostics.",
    ),
    "finance_lexicon": ArtifactSpec(
        "results/tables/finance_lexicon.csv",
        (
            "term", "candidate_class", "vanilla_vader_value",
            "approved_finance_value", "direction", "student_decision",
            "decision_date", "rationale",
        ),
        ("decision_date",),
        ("term",),
        ("term",),
        23,
        "The 23 student-approved or edited operational finance terms.",
    ),
    "fusion_metrics": ArtifactSpec(
        "results/tables/fusion_performance_metrics.csv",
        (
            "overlay_id", "base_fund_id", "family", "method", "variant",
            "start_date", "end_date", "observations", "annualisation",
            "transaction_cost_bps", "net_cumulative_return",
            "net_annualised_return", "net_annualised_volatility",
            "net_sharpe_ratio", "net_max_drawdown", "gross_cumulative_return",
            "gross_annualised_return", "gross_sharpe_ratio",
            "average_rebalance_turnover", "total_turnover",
            "transaction_cost_drag", "rebalance_count",
        ),
        ("start_date", "end_date"),
        ("overlay_id",),
        ("overlay_id",),
        24,
        "Complete performance metrics for all 24 overlays.",
    ),
    "fusion_comparison": ArtifactSpec(
        "results/tables/fusion_comparison.csv",
        (
            "overlay_id", "base_fund_id", "family", "method", "variant",
            "delta_net_annualised_return", "delta_annualised_volatility",
            "delta_net_sharpe_ratio", "delta_net_max_drawdown",
            "delta_net_cumulative_return", "delta_average_turnover",
            "delta_total_turnover", "delta_transaction_cost_drag",
        ),
        (),
        ("overlay_id",),
        ("overlay_id",),
        24,
        "Complete overlay-minus-base comparison without selective omission.",
    ),
}


def artifact_path(name: str, *, project_root: Path = PROJECT_ROOT) -> Path:
    """Return the resolved, project-contained path for one named artifact."""
    if name not in ARTIFACT_SPECS:
        raise ArtifactError(f"Unknown MAIA artifact '{name}'.")
    root = project_root.resolve()
    path = (root / ARTIFACT_SPECS[name].relative_path).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ArtifactError(f"Artifact '{name}' resolves outside the Project B root.") from exc
    return path


def _ordered_rank(series: pd.Series, order: tuple[str, ...]) -> pd.Series:
    mapping = {value: rank for rank, value in enumerate(order)}
    fallback = len(mapping)
    return series.astype(str).map(mapping).fillna(fallback).astype("int64")


def _stable_sort(frame: pd.DataFrame, spec: ArtifactSpec) -> pd.DataFrame:
    work = frame.copy(deep=True)
    sort_columns: list[str] = []
    temporary: list[str] = []
    orders = {
        "fund_id": FUND_IDS,
        "base_fund_id": ELIGIBLE_BASE_IDS,
        "overlay_id": OVERLAY_IDS,
        "sector": SECTOR_ORDER,
    }
    for column in spec.sort_columns:
        if column in orders:
            temp = f"__maia_order_{column}"
            work[temp] = _ordered_rank(work[column], orders[column])
            sort_columns.append(temp)
            temporary.append(temp)
        else:
            sort_columns.append(column)
    if sort_columns:
        work = work.sort_values(sort_columns, kind="mergesort", na_position="last")
    return work.drop(columns=temporary).reset_index(drop=True)


def _read_and_validate(
    name: str,
    *,
    project_root: Path = PROJECT_ROOT,
) -> pd.DataFrame:
    spec = ARTIFACT_SPECS[name]
    path = artifact_path(name, project_root=project_root)
    if not path.is_file():
        raise ArtifactError(
            f"Required MAIA artifact is missing: {spec.relative_path}. "
            "Restore the precomputed result before running the app."
        )
    try:
        frame = pd.read_csv(path, na_values=["NA"], keep_default_na=True)
    except Exception as exc:  # pandas provides the underlying parse detail
        raise ArtifactError(f"Could not read {spec.relative_path}: {exc}") from exc

    observed = tuple(frame.columns)
    if observed != spec.columns:
        missing = [column for column in spec.columns if column not in frame.columns]
        raise ArtifactError(
            f"Invalid schema in {spec.relative_path}. Missing={missing}; "
            f"expected columns in frozen order={list(spec.columns)}."
        )
    if spec.expected_rows is not None and len(frame) != spec.expected_rows:
        raise ArtifactError(
            f"Invalid row count in {spec.relative_path}: {len(frame):,}; "
            f"expected {spec.expected_rows:,}."
        )
    for column in spec.date_columns:
        try:
            frame[column] = pd.to_datetime(frame[column], format="%Y-%m-%d", errors="coerce")
        except (TypeError, ValueError) as exc:
            raise ArtifactError(f"Invalid date field '{column}' in {spec.relative_path}.") from exc
        required_date = column in spec.key_columns or column in {"date", "start_date", "end_date", "decision_date"}
        if required_date and frame[column].isna().any():
            raise ArtifactError(f"Required date field '{column}' is missing or invalid in {spec.relative_path}.")
    if frame.loc[:, list(spec.key_columns)].isna().any().any():
        raise ArtifactError(f"Primary key contains missing values in {spec.relative_path}.")
    if frame.duplicated(list(spec.key_columns)).any():
        raise ArtifactError(f"Primary key is duplicated in {spec.relative_path}.")
    return _stable_sort(frame, spec)


@st.cache_data(show_spinner=False)
def _load_artifact_cached(name: str) -> pd.DataFrame:
    return _read_and_validate(name)


def load_artifact(name: str) -> pd.DataFrame:
    """Load one validated artifact and protect the cached frame from UI mutation."""
    return _load_artifact_cached(name).copy(deep=True)


def load_base_metrics() -> pd.DataFrame:
    return load_artifact("performance_metrics")


def load_fund_returns() -> pd.DataFrame:
    return load_artifact("fund_returns")


def load_fund_weights() -> pd.DataFrame:
    return load_artifact("fund_weights")


def load_implementation_evidence() -> tuple[pd.DataFrame, pd.DataFrame]:
    return load_artifact("solver_diagnostics"), load_artifact("extreme_sensitivity")


def load_sentiment_evidence() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    return (
        load_artifact("sector_sentiment"),
        load_artifact("sentiment_diagnostics"),
        load_artifact("finance_lexicon"),
    )


def load_fusion_evidence() -> tuple[pd.DataFrame, pd.DataFrame]:
    return load_artifact("fusion_metrics"), load_artifact("fusion_comparison")


def artifact_inventory() -> pd.DataFrame:
    """Return a light path/purpose inventory without reading artifact contents."""
    rows = []
    for name, spec in ARTIFACT_SPECS.items():
        path = artifact_path(name)
        rows.append(
            {
                "artifact": name,
                "relative_path": spec.relative_path,
                "purpose": spec.purpose,
                "available": path.is_file(),
            }
        )
    return pd.DataFrame(rows)


__all__ = [
    "ARTIFACT_SPECS",
    "ArtifactError",
    "ArtifactSpec",
    "FUND_IDS",
    "OVERLAY_IDS",
    "PROJECT_ROOT",
    "SECTOR_ORDER",
    "VARIANTS",
    "artifact_inventory",
    "artifact_path",
    "load_artifact",
    "load_base_metrics",
    "load_fund_returns",
    "load_fund_weights",
    "load_fusion_evidence",
    "load_implementation_evidence",
    "load_sentiment_evidence",
]
