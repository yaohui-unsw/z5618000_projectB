"""Independent result auditing and report-exhibit helpers.

This module is deliberately downstream-only: it reads the frozen canonical CSV
artifacts, independently reconciles their published arithmetic where the saved
paths permit, and creates Matplotlib figures.  It never loads raw data, runs a
model, mutates an input frame, or writes a project artifact.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from math import sqrt
from pathlib import Path
from typing import Any, Iterable, Mapping

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, PercentFormatter
import numpy as np
import pandas as pd


CANONICAL_INPUTS: dict[str, str] = {
    "fund_returns": "results/data/fund_returns.csv",
    "fund_weights": "results/data/fund_weights.csv",
    "performance_metrics": "results/tables/performance_metrics.csv",
    "solver_diagnostics": "results/tables/portfolio_solver_diagnostics.csv",
    "extreme_sensitivity": "results/tables/extreme_sensitivity_metrics.csv",
    "ticker_sentiment": "results/data/ticker_sentiment_daily.csv",
    "sector_sentiment": "results/data/sector_sentiment_index.csv",
    "fusion_returns": "results/data/fusion_returns.csv",
    "fusion_weights": "results/data/fusion_weights.csv",
    "finance_lexicon": "results/tables/finance_lexicon.csv",
    "sentiment_diagnostics": "results/tables/sentiment_diagnostics.csv",
    "fusion_metrics": "results/tables/fusion_performance_metrics.csv",
    "fusion_comparison": "results/tables/fusion_comparison.csv",
}

FROZEN_SHA256: dict[str, str] = {
    "fund_returns": "7C0DB5C36F7E6CF6F054580980FA5527C812C67F9C57F47039B3B518718B6C84",
    "fund_weights": "F31A7B91A3B3CE7BE770C41597F2551913B93F6D3DDE4DCE27EC2B68E5DD53C8",
    "performance_metrics": "5719558A3D1D059137513BE0A4748BB3E1877D3956BDCFF92B095AB3B2BE2D19",
    "solver_diagnostics": "ED837EC8E7BDF0E0356267ABA372D793B33621A102B40C1B3841981CB6F1B27C",
    "extreme_sensitivity": "40E91E876813EF6F493C9C165C0D594D6DA6901FEC8B46ECA4D05F55E5BCE151",
    "ticker_sentiment": "CC9DDF834EF43B9B07240A40949716BA573A14E6ADDCD1997DFF83C125E26FCD",
    "sector_sentiment": "D7670369187E3FF6909A88F6459204284A45D07941DC395CE239D8E304E8E96E",
    "fusion_returns": "5A868D15E4D649FEDCB7BF9A0D58657F1729D6F35A2A62A2DF148622EA8CEBC5",
    "fusion_weights": "13941551A0D3D9A07290235CCEF7C8AB389D2F78EAF36D81CE661A915F485058",
    "finance_lexicon": "5E6EE31DADC6C754DD465E825FBA5F25B3BD26E5E0AA846B3A578619D444C5DB",
    "sentiment_diagnostics": "3C7842ED0F955DCA29E1E728EFD51C46AA12D4B93999DC9C72D47C436AC179B5",
    "fusion_metrics": "B75FA251E385E3709D3EC1380367D0257285D249AF742965C8FD993FCA770A07",
    "fusion_comparison": "B51DF470AEAB5932356037DF72FCF0044729C6F9F88C117E6C4B90F4922C3946",
}

SCHEMAS: dict[str, tuple[str, ...]] = {
    "fund_returns": (
        "date", "fund_id", "family", "method", "gross_return", "turnover",
        "transaction_cost", "net_return", "is_rebalance",
    ),
    "fund_weights": (
        "date", "fund_id", "family", "method", "ticker", "pretrade_weight",
        "target_weight", "trade_weight", "turnover", "solver_success", "solver_status",
    ),
    "performance_metrics": (
        "fund_id", "family", "method", "start_date", "end_date", "observations",
        "annualisation", "transaction_cost_bps", "net_cumulative_return",
        "net_annualised_return", "net_annualised_volatility", "net_sharpe_ratio",
        "net_max_drawdown", "gross_cumulative_return", "gross_annualised_return",
        "gross_sharpe_ratio", "average_rebalance_turnover", "total_turnover",
        "rebalance_count",
    ),
    "solver_diagnostics": (
        "date", "fund_id", "family", "method", "solver_success", "attempts",
        "status_code", "message", "iterations", "objective_value", "sum_residual",
        "lower_bound_violation", "upper_bound_violation", "covariance_repair",
        "minimum_eigenvalue", "retry_used", "near_identical_with",
        "near_identical_warning", "near_identical_explanation",
    ),
    "extreme_sensitivity": (
        "fund_id", "family", "method", "canonical_net_annualised_return",
        "sensitivity_net_annualised_return", "delta_net_annualised_return",
        "canonical_net_sharpe_ratio", "sensitivity_net_sharpe_ratio",
        "delta_net_sharpe_ratio", "canonical_net_max_drawdown",
        "sensitivity_net_max_drawdown", "delta_net_max_drawdown",
    ),
    "ticker_sentiment": (
        "date", "ticker", "sector", "headline_count", "has_news", "plain_score",
        "finance_score", "covered_headline_share", "nonneutral_headline_count",
        "directional_agreement", "volume_evidence", "reliability",
        "custom_finance_term_hit_share", "evidence_aware_compound", "plain_z",
        "finance_z", "evidence_aware_signal", "signal_source_date",
        "lagged_plain_signal", "lagged_finance_signal",
        "lagged_evidence_aware_signal",
    ),
    "sector_sentiment": (
        "date", "sector", "sector_display", "headline_count",
        "ticker_count_with_news", "ticker_coverage", "plain_compound",
        "finance_compound", "mean_reliability", "evidence_aware_compound",
        "plain_z", "finance_z", "evidence_aware_z",
    ),
    "fusion_returns": (
        "date", "overlay_id", "base_fund_id", "family", "method", "variant",
        "gross_return", "turnover", "transaction_cost", "net_return", "is_rebalance",
    ),
    "fusion_weights": (
        "date", "overlay_id", "base_fund_id", "family", "method", "variant",
        "ticker", "base_target_weight", "pretrade_weight", "signal_source_date",
        "signal_value", "multiplier", "raw_tilted_value", "target_weight",
        "trade_weight", "turnover", "projection_success", "projection_status",
    ),
    "finance_lexicon": (
        "term", "candidate_class", "vanilla_vader_value", "approved_finance_value",
        "direction", "student_decision", "decision_date", "rationale",
    ),
    "sentiment_diagnostics": (
        "scope", "entity", "model", "metric", "value", "numerator", "denominator",
        "start_date", "end_date", "notes",
    ),
    "fusion_metrics": (
        "overlay_id", "base_fund_id", "family", "method", "variant", "start_date",
        "end_date", "observations", "annualisation", "transaction_cost_bps",
        "net_cumulative_return", "net_annualised_return",
        "net_annualised_volatility", "net_sharpe_ratio", "net_max_drawdown",
        "gross_cumulative_return", "gross_annualised_return", "gross_sharpe_ratio",
        "average_rebalance_turnover", "total_turnover", "transaction_cost_drag",
        "rebalance_count",
    ),
    "fusion_comparison": (
        "overlay_id", "base_fund_id", "family", "method", "variant",
        "delta_net_annualised_return", "delta_annualised_volatility",
        "delta_net_sharpe_ratio", "delta_net_max_drawdown",
        "delta_net_cumulative_return", "delta_average_turnover",
        "delta_total_turnover", "delta_transaction_cost_drag",
    ),
}

EXPECTED_ROWS = {
    "fund_returns": 10_404,
    "fund_weights": 17_280,
    "performance_metrics": 12,
    "solver_diagnostics": 432,
    "extreme_sensitivity": 12,
    "ticker_sentiment": 50_300,
    "sector_sentiment": 10_060,
    "fusion_returns": 18_072,
    "fusion_weights": 47_520,
    "finance_lexicon": 23,
    "fusion_metrics": 24,
    "fusion_comparison": 24,
}

FUND_IDS = (
    "equity_equal_weight", "equity_minimum_variance", "equity_maximum_sharpe",
    "equity_risk_parity", "crypto_equal_weight", "crypto_minimum_variance",
    "crypto_maximum_sharpe", "crypto_risk_parity", "combined_equal_weight",
    "combined_minimum_variance", "combined_maximum_sharpe", "combined_risk_parity",
)
ELIGIBLE_BASE_IDS = (
    "equity_equal_weight", "equity_minimum_variance", "equity_maximum_sharpe",
    "equity_risk_parity", "combined_equal_weight", "combined_minimum_variance",
    "combined_maximum_sharpe", "combined_risk_parity",
)
VARIANTS = ("plain_vader_naive", "finance_vader_naive", "evidence_aware_finance")
OVERLAY_IDS = tuple(f"{fund}__{variant}" for fund in ELIGIBLE_BASE_IDS for variant in VARIANTS)
METHODS = ("Equal Weight", "Minimum Variance", "Maximum Sharpe", "Risk Parity")
FAMILIES = ("Equity", "Crypto", "Combined")
SECTOR_ORDER = (
    "Tech", "Financials", "Energy", "Consumer", "Industrials", "Healthcare",
    "Comm", "Materials", "Utilities", "RealEstate",
)
SECTOR_DISPLAY = {
    "Tech": "Tech", "Financials": "Financials", "Energy": "Energy",
    "Consumer": "Consumer", "Industrials": "Industrials", "Healthcare": "Healthcare",
    "Comm": "Comm/Telecom", "Materials": "Materials", "Utilities": "Utilities",
    "RealEstate": "Real Estate",
}
CRYPTO_TICKERS = {
    "ADA-USD", "BCH-USD", "BTC-USD", "EOS-USD", "ETC-USD", "ETH-USD",
    "LTC-USD", "TRX-USD", "XLM-USD", "XRP-USD",
}
OPERATIONAL_LEXICON = {
    "active": 0.0, "alert": 0.0, "asset": 0.0, "beat": 1.5,
    "beats": 1.5, "bullish": 1.5, "downgraded": -1.5, "downgrades": -1.0,
    "energy": 0.0, "layoffs": -1.0, "miss": -1.0, "misses": -1.5,
    "outperform": 1.0, "overweight": 1.0, "plunge": -1.5, "plunges": -1.5,
    "rally": 1.0, "rebound": 0.5, "shares": 0.0, "slump": -1.5,
    "tumble": -1.5, "underperform": -1.0, "underweight": -1.0,
}
REJECTED_TERMS = {"inflow", "inflows", "outflow", "outflows"}

FIGURE_FILENAMES = (
    "fund_growth_comparison.png", "combined_drawdowns.png",
    "combined_weights_over_time.png", "fund_risk_return_map.png",
    "sector_sentiment_timeseries.png", "fusion_before_after.png",
    "sentiment_innovation_diagnostics.png", "fusion_turnover_tradeoff.png",
)

METHOD_COLORS = {
    "Equal Weight": "#6B7280",
    "Minimum Variance": "#2463A6",
    "Maximum Sharpe": "#E07A24",
    "Risk Parity": "#2F855A",
}
VARIANT_COLORS = {
    "plain_vader_naive": "#3A7CA5",
    "finance_vader_naive": "#E07A24",
    "evidence_aware_finance": "#178F8F",
}
VARIANT_LABELS = {
    "plain_vader_naive": "Plain VADER",
    "finance_vader_naive": "Finance VADER",
    "evidence_aware_finance": "Evidence-aware",
}
VARIANT_MARKERS = {
    "plain_vader_naive": "o",
    "finance_vader_naive": "s",
    "evidence_aware_finance": "D",
}
FAMILY_MARKERS = {"Equity": "o", "Crypto": "^", "Combined": "s"}
INK = "#17212B"
MUTED = "#5D6B78"
GRID = "#D7DEE5"
PAPER = "#FBFCFD"


@dataclass(frozen=True)
class AuditFinding:
    code: str
    level: str
    message: str
    observed: Any = None
    expected: Any = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "level": self.level,
            "message": self.message,
            "observed": self.observed,
            "expected": self.expected,
        }


@dataclass
class AuditReport:
    findings: list[AuditFinding] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)

    def add(
        self,
        condition: bool,
        code: str,
        pass_message: str,
        block_message: str,
        *,
        observed: Any = None,
        expected: Any = None,
    ) -> None:
        self.findings.append(
            AuditFinding(
                code=code,
                level="PASS" if bool(condition) else "BLOCK",
                message=pass_message if bool(condition) else block_message,
                observed=observed,
                expected=expected,
            )
        )

    def warn(self, code: str, message: str, *, observed: Any = None) -> None:
        self.findings.append(AuditFinding(code, "WARN", message, observed=observed))

    @property
    def summary(self) -> dict[str, int]:
        return {
            level: sum(item.level == level for item in self.findings)
            for level in ("PASS", "WARN", "BLOCK")
        }

    @property
    def ok(self) -> bool:
        return self.summary["BLOCK"] == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": "PASS" if self.ok else "BLOCK",
            "summary": self.summary,
            "evidence": self.evidence,
            "findings": [item.to_dict() for item in self.findings],
        }


@dataclass(frozen=True)
class FigureMetadata:
    filename: str
    title: str
    question: str
    x_label: str
    y_label: str
    units: str
    date_range: str
    caveat: str


@dataclass
class FigureArtifact:
    figure: Figure
    metadata: FigureMetadata


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def canonical_hashes(project_root: Path) -> dict[str, str]:
    return {
        name: file_sha256(project_root / relative)
        for name, relative in CANONICAL_INPUTS.items()
    }


def load_canonical_outputs(project_root: Path) -> dict[str, pd.DataFrame]:
    """Load only the 13 frozen canonical CSVs into independent frames."""
    missing = [relative for relative in CANONICAL_INPUTS.values() if not (project_root / relative).is_file()]
    if missing:
        raise FileNotFoundError(f"missing frozen canonical output(s): {missing}")
    date_columns = {
        "fund_returns": ["date"],
        "fund_weights": ["date"],
        "performance_metrics": ["start_date", "end_date"],
        "solver_diagnostics": ["date"],
        "extreme_sensitivity": [],
        "ticker_sentiment": ["date", "signal_source_date"],
        "sector_sentiment": ["date"],
        "fusion_returns": ["date"],
        "fusion_weights": ["date", "signal_source_date"],
        "finance_lexicon": ["decision_date"],
        "sentiment_diagnostics": ["start_date", "end_date"],
        "fusion_metrics": ["start_date", "end_date"],
        "fusion_comparison": [],
    }
    return {
        name: pd.read_csv(project_root / relative, parse_dates=date_columns[name])
        for name, relative in CANONICAL_INPUTS.items()
    }


def _columns(frame: pd.DataFrame, expected: tuple[str, ...]) -> bool:
    return tuple(frame.columns) == expected


def _unique(frame: pd.DataFrame, columns: list[str]) -> bool:
    return not frame.loc[:, columns].isna().any().any() and not frame.duplicated(columns).any()


def _close(left: Any, right: Any, tolerance: float = 5e-10) -> bool:
    try:
        return bool(np.allclose(left, right, rtol=0.0, atol=tolerance, equal_nan=True))
    except (TypeError, ValueError):
        return False


def _all_finite(frame: pd.DataFrame, columns: Iterable[str], *, allow_missing: bool = False) -> bool:
    values = frame.loc[:, list(columns)].to_numpy(dtype="float64")
    return bool(np.isfinite(values[~np.isnan(values)]).all()) if allow_missing else bool(np.isfinite(values).all())


def independent_path_metrics(values: pd.Series, annualisation: int) -> dict[str, float]:
    """Recompute path metrics directly, without project model helpers."""
    returns = values.to_numpy(dtype="float64", copy=True)
    if len(returns) < 2 or not np.isfinite(returns).all() or np.any(returns <= -1.0):
        raise ValueError("return path must contain at least two finite values greater than -1")
    wealth = np.cumprod(1.0 + returns)
    deviation = float(np.std(returns, ddof=1))
    if not np.isfinite(deviation) or deviation <= 0:
        raise ValueError("return path has invalid sample standard deviation")
    drawdown = wealth / np.maximum.accumulate(wealth) - 1.0
    return {
        "cumulative_return": float(wealth[-1] - 1.0),
        "annualised_return": float(wealth[-1] ** (annualisation / len(returns)) - 1.0),
        "annualised_volatility": float(deviation * sqrt(annualisation)),
        "sharpe_ratio": float(np.mean(returns) / deviation * sqrt(annualisation)),
        "max_drawdown": float(drawdown.min()),
    }


def growth_and_drawdown(frame: pd.DataFrame, id_column: str = "fund_id") -> pd.DataFrame:
    required = {"date", id_column, "net_return"}
    if not required.issubset(frame.columns):
        raise KeyError(f"missing growth-path column(s): {sorted(required - set(frame.columns))}")
    work = frame.loc[:, ["date", id_column, "net_return"]].copy(deep=True)
    if work.duplicated(["date", id_column]).any():
        raise ValueError("duplicate growth-path key")
    if not _all_finite(work, ["net_return"]):
        raise ValueError("non-finite net return")
    work = work.sort_values([id_column, "date"], kind="mergesort")
    work["growth"] = work.groupby(id_column, sort=False)["net_return"].transform(
        lambda series: (1.0 + series).cumprod()
    )
    work["drawdown"] = work.groupby(id_column, sort=False)["growth"].transform(
        lambda series: series / series.cummax() - 1.0
    )
    return work.sort_values(["date", id_column], kind="mergesort").reset_index(drop=True)


def _diagnostic_row(
    diagnostics: pd.DataFrame, scope: str, entity: str, model: str, metric: str
) -> pd.Series:
    mask = (
        diagnostics["scope"].eq(scope)
        & diagnostics["entity"].eq(entity)
        & diagnostics["model"].eq(model)
        & diagnostics["metric"].eq(metric)
    )
    matches = diagnostics.loc[mask]
    if len(matches) != 1:
        raise ValueError(f"diagnostic key has {len(matches)} rows: {(scope, entity, model, metric)}")
    return matches.iloc[0]


def _metric_reconciliation(returns: pd.DataFrame, metrics: pd.DataFrame, id_column: str) -> tuple[bool, float]:
    max_error = 0.0
    ok = True
    for row in metrics.itertuples(index=False):
        identifier = getattr(row, id_column)
        group = returns.loc[returns[id_column].eq(identifier)].sort_values("date", kind="mergesort")
        net = independent_path_metrics(group["net_return"], int(row.annualisation))
        gross = independent_path_metrics(group["gross_return"], int(row.annualisation))
        rebalances = group.loc[group["is_rebalance"].astype(bool)]
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
            "average_rebalance_turnover": float(cost_bearing["turnover"].mean()),
            "total_turnover": float(cost_bearing["turnover"].sum()),
        }
        if hasattr(row, "transaction_cost_drag"):
            expected["transaction_cost_drag"] = gross["cumulative_return"] - net["cumulative_return"]
        for column, value in expected.items():
            error = abs(float(getattr(row, column)) - value)
            max_error = max(max_error, error)
            ok &= error <= 5e-10
        ok &= (
            len(group) == int(row.observations)
            and pd.Timestamp(group["date"].iloc[0]) == pd.Timestamp(row.start_date)
            and pd.Timestamp(group["date"].iloc[-1]) == pd.Timestamp(row.end_date)
            and len(rebalances) == int(row.rebalance_count)
        )
    return bool(ok), float(max_error)


def audit_canonical_outputs(
    frames: Mapping[str, pd.DataFrame], observed_hashes: Mapping[str, str]
) -> AuditReport:
    """Perform the Stage 7 CSV-only independent audit."""
    report = AuditReport()
    missing = sorted(set(CANONICAL_INPUTS) - set(frames))
    report.add(not missing, "input_inventory", "All 13 frozen canonical inputs are present.", "A canonical input is missing.", observed=missing, expected=[])
    if missing:
        return report

    report.add(
        dict(observed_hashes) == FROZEN_SHA256,
        "immutable_input_hashes",
        "All 13 canonical SHA-256 hashes match the frozen Stage 5A/6C evidence.",
        "At least one canonical CSV hash differs from the frozen evidence.",
        observed=dict(observed_hashes), expected=FROZEN_SHA256,
    )

    schema_ok = True
    for name, expected in SCHEMAS.items():
        condition = _columns(frames[name], expected)
        schema_ok &= condition
        report.add(condition, f"{name}_schema", f"{name} uses its frozen schema.", f"{name} schema differs from the freeze.", observed=tuple(frames[name].columns), expected=expected)
        if name in EXPECTED_ROWS:
            report.add(len(frames[name]) == EXPECTED_ROWS[name], f"{name}_rows", f"{name} has the expected row count.", f"{name} row count differs.", observed=len(frames[name]), expected=EXPECTED_ROWS[name])
    report.add(not frames["sentiment_diagnostics"].empty, "diagnostics_nonempty", "Sentiment diagnostics are non-empty.", "Sentiment diagnostics are empty.")
    if not schema_ok:
        return report

    fund_returns = frames["fund_returns"].copy(deep=True)
    fund_weights = frames["fund_weights"].copy(deep=True)
    base_metrics = frames["performance_metrics"].copy(deep=True)
    solver = frames["solver_diagnostics"].copy(deep=True)
    sensitivity = frames["extreme_sensitivity"].copy(deep=True)
    ticker = frames["ticker_sentiment"].copy(deep=True)
    sector = frames["sector_sentiment"].copy(deep=True)
    fusion_returns = frames["fusion_returns"].copy(deep=True)
    fusion_weights = frames["fusion_weights"].copy(deep=True)
    lexicon = frames["finance_lexicon"].copy(deep=True)
    diagnostics = frames["sentiment_diagnostics"].copy(deep=True)
    fusion_metrics = frames["fusion_metrics"].copy(deep=True)
    comparison = frames["fusion_comparison"].copy(deep=True)

    keys_ok = (
        _unique(fund_returns, ["date", "fund_id"])
        and _unique(fund_weights, ["date", "fund_id", "ticker"])
        and _unique(base_metrics, ["fund_id"])
        and _unique(solver, ["date", "fund_id"])
        and _unique(ticker, ["date", "ticker"])
        and _unique(sector, ["date", "sector"])
        and _unique(fusion_returns, ["date", "overlay_id"])
        and _unique(fusion_weights, ["date", "overlay_id", "ticker"])
        and _unique(lexicon, ["term"])
        and _unique(diagnostics, ["scope", "entity", "model", "metric"])
        and _unique(fusion_metrics, ["overlay_id"])
        and _unique(comparison, ["overlay_id"])
    )
    report.add(keys_ok, "unique_keys", "Every canonical primary key is complete and unique.", "A canonical primary key is missing or duplicated.")

    funds_ok = (
        tuple(base_metrics["fund_id"]) == FUND_IDS
        and set(fund_returns["fund_id"]) == set(FUND_IDS)
        and set(fund_weights["fund_id"]) == set(FUND_IDS)
        and set(solver["fund_id"]) == set(FUND_IDS)
    )
    report.add(funds_ok, "fund_universe", "All twelve frozen family-method funds are present.", "The frozen twelve-fund universe is incomplete or reordered.")

    family_expectations = {
        "Equity": (pd.Timestamp("2021-01-04"), pd.Timestamp("2023-12-29"), 753, 252),
        "Crypto": (pd.Timestamp("2021-01-01"), pd.Timestamp("2023-12-31"), 1095, 365),
        "Combined": (pd.Timestamp("2021-01-04"), pd.Timestamp("2023-12-29"), 753, 252),
    }
    calendar_ok = True
    family_dates: dict[str, pd.DatetimeIndex] = {}
    for family, (start, end, observations, annualisation) in family_expectations.items():
        ids = base_metrics.loc[base_metrics["family"].eq(family), "fund_id"]
        groups = [fund_returns.loc[fund_returns["fund_id"].eq(fund_id)].sort_values("date") for fund_id in ids]
        reference = pd.DatetimeIndex(groups[0]["date"])
        family_dates[family] = reference
        calendar_ok &= all(pd.DatetimeIndex(group["date"]).equals(reference) for group in groups)
        calendar_ok &= len(reference) == observations and reference[0] == start and reference[-1] == end
        calendar_ok &= base_metrics.loc[base_metrics["family"].eq(family), "annualisation"].eq(annualisation).all()
    calendar_ok &= family_dates["Equity"].equals(family_dates["Combined"])
    calendar_ok &= not any(date.weekday() >= 5 for date in family_dates["Equity"])
    calendar_ok &= any(date.weekday() >= 5 for date in family_dates["Crypto"])
    report.add(calendar_ok, "fund_calendars", "Family dates, live samples, and 252/365 annualisation reconcile.", "A family calendar, live boundary, observation count, or annualisation differs.")

    rebalance_ok = True
    for fund_id, group in fund_returns.groupby("fund_id", sort=False):
        ordered = group.sort_values("date", kind="mergesort")
        expected = ordered.groupby(ordered["date"].dt.to_period("M"), sort=False)["date"].min()
        actual = ordered.loc[ordered["is_rebalance"].astype(bool), "date"].reset_index(drop=True)
        rebalance_ok &= actual.equals(expected.reset_index(drop=True)) and len(actual) == 36
    report.add(rebalance_ok, "monthly_rebalance_schedule", "Every base fund rebalances on the first live date of each month.", "A base rebalance date differs from the frozen monthly schedule.")

    base_metrics_ok, base_metric_error = _metric_reconciliation(fund_returns, base_metrics, "fund_id")
    report.add(base_metrics_ok, "base_metric_reconciliation", "All twelve base metric rows independently reconcile to daily gross/net paths.", "A base metric does not reconcile to its daily return path.", observed=base_metric_error, expected="<=5e-10")

    sums = fund_weights.groupby(["date", "fund_id"], sort=False)["target_weight"].sum()
    base_min = float(fund_weights["target_weight"].min())
    base_max = float(fund_weights["target_weight"].max())
    max_sum_error = float((sums - 1.0).abs().max())
    constraints_ok = (
        _all_finite(fund_weights, ["pretrade_weight", "target_weight", "trade_weight", "turnover"])
        and base_min >= -1e-10 and base_max <= 0.20 + 1e-10 and max_sum_error <= 1e-8
        and fund_weights["solver_success"].astype(bool).all()
        and solver["solver_success"].astype(bool).all()
        and solver[["sum_residual", "lower_bound_violation", "upper_bound_violation"]].max().max() <= 1e-8
    )
    report.add(constraints_ok, "base_weight_constraints", "Base targets are finite, fully invested, long-only, capped, and solver-successful.", "A base weight or solver record violates the frozen constraints.", observed={"min": base_min, "max": base_max, "max_sum_error": max_sum_error})

    base_cost_residual = float(np.max(np.abs(fund_returns["transaction_cost"] - 0.0005 * fund_returns["turnover"])))
    base_net_residual = float(np.max(np.abs(fund_returns["net_return"] - ((1.0 - fund_returns["transaction_cost"]) * (1.0 + fund_returns["gross_return"]) - 1.0))))
    base_trade_residual = float(np.max(np.abs(fund_weights["trade_weight"] - (fund_weights["target_weight"] - fund_weights["pretrade_weight"]))))
    base_turnover_ok = True
    for (date, fund_id), group in fund_weights.groupby(["date", "fund_id"], sort=False):
        first_date = fund_returns.loc[fund_returns["fund_id"].eq(fund_id), "date"].min()
        observed = float(group["turnover"].iloc[0])
        expected = 0.0 if pd.Timestamp(date) == pd.Timestamp(first_date) else 0.5 * float(np.abs(group["trade_weight"]).sum())
        base_turnover_ok &= group["turnover"].nunique() == 1 and abs(observed - expected) <= 5e-10
    report.add(
        base_cost_residual <= 5e-12 and base_net_residual <= 5e-12 and base_trade_residual <= 5e-10 and base_turnover_ok,
        "base_turnover_costs", "Base trade weights, drifted-pretrade turnover, 5-bps costs, and gross/net arithmetic reconcile.",
        "Base turnover or transaction-cost arithmetic does not reconcile.",
        observed={"cost": base_cost_residual, "net": base_net_residual, "trade": base_trade_residual},
    )

    sensitivity_ok = (
        tuple(sensitivity["fund_id"]) == FUND_IDS
        and _close(sensitivity["delta_net_annualised_return"], sensitivity["sensitivity_net_annualised_return"] - sensitivity["canonical_net_annualised_return"])
        and _close(sensitivity["delta_net_sharpe_ratio"], sensitivity["sensitivity_net_sharpe_ratio"] - sensitivity["canonical_net_sharpe_ratio"])
        and _close(sensitivity["delta_net_max_drawdown"], sensitivity["sensitivity_net_max_drawdown"] - sensitivity["canonical_net_max_drawdown"])
    )
    report.add(sensitivity_ok, "extreme_sensitivity", "All twelve separately labelled +/-25% sensitivity rows and deltas reconcile.", "The frozen extreme-return sensitivity evidence is incomplete or arithmetically inconsistent.")

    # Sentiment population, missingness, reliability, mapping, and lag.
    no_news = ~ticker["has_news"].astype(bool)
    news = ~no_news
    sentiment_population_ok = (
        ticker["ticker"].nunique() == 50 and ticker["date"].nunique() == 1006
        and sector["sector"].nunique() == 10 and sector["date"].nunique() == 1006
        and int(no_news.sum()) == 12_338 and int(news.sum()) == 37_962
        and int(ticker["headline_count"].sum()) == 146_830
    )
    report.add(sentiment_population_ok, "sentiment_population", "Ticker/sector panels and news/no-news counts reconcile exactly.", "A sentiment population or headline-count benchmark differs.")

    mapped = _diagnostic_row(diagnostics, "headline", "all", "mapping", "mapped_headline_count")
    unmapped = _diagnostic_row(diagnostics, "headline", "all", "mapping", "unmapped_end_of_sample_count")
    mapping_ok = int(mapped.value) == 146_830 and int(unmapped.value) == 6 and int(mapped.value + unmapped.value) == 146_836
    report.add(mapping_ok, "headline_mapping", "146,836 cleaned headlines reconcile to 146,830 mapped/scored plus six endpoint exclusions.", "Cleaned, mapped, or endpoint-exclusion counts do not reconcile.")

    no_news_fields = [
        "plain_score", "finance_score", "covered_headline_share", "directional_agreement",
        "volume_evidence", "reliability", "custom_finance_term_hit_share",
        "evidence_aware_compound", "plain_z", "finance_z", "evidence_aware_signal",
    ]
    missingness_ok = ticker.loc[no_news, no_news_fields].isna().all().all()
    neutral_exists = bool((ticker["has_news"].astype(bool) & ticker["finance_score"].eq(0.0)).any())
    report.add(missingness_ok and neutral_exists, "no_news_vs_neutral", "No-news remains missing and scored-neutral news remains separately observable.", "No-news was filled or scored-neutral news is not distinguishable.")

    news_rows = ticker.loc[news]
    reliability_expected = news_rows["covered_headline_share"] * news_rows["directional_agreement"] * news_rows["volume_evidence"]
    evidence_expected = news_rows["finance_score"] * news_rows["reliability"]
    reliability_ok = (
        _close(news_rows["volume_evidence"], news_rows["headline_count"] / (news_rows["headline_count"] + 1.0))
        and _close(news_rows["reliability"], reliability_expected)
        and _close(news_rows["evidence_aware_compound"], evidence_expected)
        and all(news_rows[column].between(0.0, 1.0).all() for column in ["covered_headline_share", "directional_agreement", "volume_evidence", "reliability", "custom_finance_term_hit_share"])
    )
    report.add(reliability_ok, "reliability_reconciliation", "Reliability components, bounds, and raw evidence-aware compounds reconcile.", "A reliability component or diagnostic compound differs from the freeze.")

    lag_ok = True
    for _, group in ticker.sort_values(["ticker", "date"], kind="mergesort").groupby("ticker", sort=False):
        dates = group["date"].reset_index(drop=True)
        source = group["signal_source_date"].reset_index(drop=True)
        lag_ok &= source.equals(dates.shift(1))
        lag_ok &= _close(group["lagged_plain_signal"], group["plain_z"].shift(1))
        lag_ok &= _close(group["lagged_finance_signal"], group["finance_z"].shift(1))
        lag_ok &= _close(group["lagged_evidence_aware_signal"], (group["finance_z"] * group["reliability"]).shift(1))
    strictly_past = (ticker.loc[ticker["signal_source_date"].notna(), "signal_source_date"] < ticker.loc[ticker["signal_source_date"].notna(), "date"]).all()
    usable = int(ticker["finance_z"].notna().sum())
    lagged = int(ticker["lagged_finance_signal"].notna().sum())
    final_usable = int(ticker.sort_values("date").groupby("ticker", sort=False).tail(1)["finance_z"].notna().sum())
    boundary_ok = usable == 34_789 and lagged == 34_788 and usable - lagged == final_usable == 1
    report.add(lag_ok and strictly_past and boundary_ok, "lag_and_boundary", "Signals use only the immediate prior trading date; the 34,789/34,788 one-row difference is an end-boundary consequence.", "A lag, carry-forward, look-ahead, or boundary reconciliation failed.", observed={"usable": usable, "lagged": lagged, "final_date_usable": final_usable})

    sector_expected = news_rows.groupby(["date", "sector"], observed=True).agg(
        headline_count=("headline_count", "sum"),
        ticker_count_with_news=("ticker", "nunique"),
        plain_compound=("plain_score", "mean"),
        finance_compound=("finance_score", "mean"),
        mean_reliability=("reliability", "mean"),
        evidence_aware_compound=("evidence_aware_compound", "mean"),
    ).reset_index()
    eligible_counts = ticker.groupby("sector", observed=True)["ticker"].nunique()
    sector_expected["ticker_coverage"] = sector_expected.apply(lambda row: row.ticker_count_with_news / eligible_counts.loc[row.sector], axis=1)
    joined_sector = sector.merge(sector_expected, on=["date", "sector"], how="left", suffixes=("", "_expected"), validate="one_to_one")
    # The frozen complete panel represents a sector-day with no news using
    # zero counts/coverage and missing compounds.  Groupby has no row for that
    # state, so make the contractual zero representation explicit before the
    # comparison rather than treating absence as a numeric discrepancy.
    for column in ("headline_count_expected", "ticker_count_with_news_expected", "ticker_coverage_expected"):
        joined_sector[column] = joined_sector[column].fillna(0.0)
    sector_ok = all(
        _close(joined_sector[column], joined_sector[f"{column}_expected"])
        for column in ["headline_count", "ticker_count_with_news", "ticker_coverage", "plain_compound", "finance_compound", "mean_reliability", "evidence_aware_compound"]
    )
    sector_ok &= all(SECTOR_DISPLAY.get(row.sector) == row.sector_display for row in sector.itertuples())
    report.add(sector_ok, "sector_aggregation", "Sector scores independently equal-weight news-bearing ticker-days with accepted coverage labels.", "Sector aggregation, coverage, or display mapping does not reconcile.")

    lexicon_values = lexicon.set_index("term")["approved_finance_value"].astype(float).to_dict()
    lexicon_ok = (
        lexicon_values == OPERATIONAL_LEXICON
        and REJECTED_TERMS.isdisjoint(set(lexicon["term"]))
        and set(lexicon["student_decision"]) <= {"ACCEPT", "EDIT"}
        and pd.to_datetime(lexicon["decision_date"]).dt.strftime("%Y-%m-%d").eq("2026-08-14").all()
    )
    report.add(lexicon_ok, "operational_lexicon", "Exactly 23 student-approved values are present and all four ETF-flow terms are excluded.", "The operational lexicon differs from the frozen student decisions.")

    # Fusion coverage, signal provenance, projection, sleeves, costs, and metrics.
    overlays_ok = (
        tuple(fusion_metrics["overlay_id"]) == OVERLAY_IDS
        and set(fusion_returns["overlay_id"]) == set(OVERLAY_IDS)
        and not fusion_returns["family"].eq("Crypto").any()
        and fusion_returns.groupby("overlay_id").size().eq(753).all()
        and fusion_weights.groupby("overlay_id")["date"].nunique().eq(36).all()
    )
    report.add(overlays_ok, "overlay_universe", "All 24 overlays cover eight eligible bases and three variants; Crypto-only funds are excluded.", "Overlay coverage, dates, or Crypto exclusion differs from the freeze.")

    schedule_ok = True
    for overlay_id, group in fusion_returns.groupby("overlay_id", sort=False):
        base_id = group["base_fund_id"].iloc[0]
        base = fund_returns.loc[fund_returns["fund_id"].eq(base_id)].sort_values("date")
        ordered = group.sort_values("date")
        schedule_ok &= pd.DatetimeIndex(ordered["date"]).equals(pd.DatetimeIndex(base["date"]))
        schedule_ok &= pd.DatetimeIndex(ordered.loc[ordered["is_rebalance"].astype(bool), "date"]).equals(pd.DatetimeIndex(base.loc[base["is_rebalance"].astype(bool), "date"]))
    report.add(schedule_ok, "overlay_monthly_schedule", "Every overlay uses its base fund's exact live and monthly rebalance dates.", "An overlay changes the frozen base calendar or schedule.")

    signal_columns = {
        "plain_vader_naive": "lagged_plain_signal",
        "finance_vader_naive": "lagged_finance_signal",
        "evidence_aware_finance": "lagged_evidence_aware_signal",
    }
    equity_fusion = fusion_weights.loc[~fusion_weights["ticker"].isin(CRYPTO_TICKERS)].copy()
    signal_ok = True
    for variant, column in signal_columns.items():
        part = equity_fusion.loc[equity_fusion["variant"].eq(variant)]
        joined = part.merge(
            ticker.loc[:, ["date", "ticker", "signal_source_date", column]],
            on=["date", "ticker"], how="left", validate="many_to_one", suffixes=("", "_ticker"),
        )
        signal_ok &= _close(joined["signal_value"], joined[column])
        signal_ok &= joined["signal_source_date"].equals(joined["signal_source_date_ticker"])
        finite_signal = joined["signal_value"].notna()
        signal_ok &= _close(joined.loc[finite_signal, "multiplier"], np.exp(0.10 * joined.loc[finite_signal, "signal_value"]))
        signal_ok &= joined.loc[~finite_signal, "multiplier"].eq(1.0).all()
    report.add(signal_ok, "overlay_signal_provenance", "Every equity tilt uses the frozen lagged ticker signal with lambda 0.10 and multiplier one for missing signals.", "An overlay uses a wrong, unlagged, carried, or incorrectly scaled signal.")

    fusion_sums = fusion_weights.groupby(["date", "overlay_id"], sort=False)["target_weight"].sum()
    fusion_min = float(fusion_weights["target_weight"].min())
    fusion_max = float(fusion_weights["target_weight"].max())
    fusion_sum_error = float((fusion_sums - 1.0).abs().max())
    projection_ok = fusion_weights["projection_success"].astype(bool).all() and fusion_min >= -1e-10 and fusion_max <= 0.20 + 1e-10 and fusion_sum_error <= 1e-8
    report.add(projection_ok, "fusion_projection", "Every published overlay projection succeeds and satisfies long-only, cap, and sum constraints.", "A published overlay projection or constraint fails.", observed={"min": fusion_min, "max": fusion_max, "max_sum_error": fusion_sum_error})

    base_lookup = fund_weights.loc[:, ["date", "fund_id", "ticker", "target_weight"]]
    combined = fusion_weights.loc[fusion_weights["family"].eq("Combined")].merge(
        base_lookup,
        left_on=["date", "base_fund_id", "ticker"],
        right_on=["date", "fund_id", "ticker"],
        how="left", validate="many_to_one", suffixes=("", "_base"),
    )
    crypto = combined.loc[combined["ticker"].isin(CRYPTO_TICKERS)]
    equity = combined.loc[~combined["ticker"].isin(CRYPTO_TICKERS)]
    max_crypto_difference = float(np.max(np.abs(crypto["target_weight"] - crypto["target_weight_base"])))
    sleeve = equity.groupby(["date", "overlay_id"], sort=False).agg(overlay=("target_weight", "sum"), base=("target_weight_base", "sum"))
    max_sleeve_difference = float(np.max(np.abs(sleeve["overlay"] - sleeve["base"])))
    combined_ok = max_crypto_difference <= 5e-12 and max_sleeve_difference <= 5e-12
    report.add(combined_ok, "combined_sleeves", "Combined crypto targets remain unchanged and equity-sleeve totals are preserved.", "A Combined overlay changes a crypto target or equity-sleeve total.", observed={"crypto": max_crypto_difference, "equity_sleeve": max_sleeve_difference})

    fusion_cost_residual = float(np.max(np.abs(fusion_returns["transaction_cost"] - 0.0005 * fusion_returns["turnover"])))
    fusion_net_residual = float(np.max(np.abs(fusion_returns["net_return"] - ((1.0 - fusion_returns["transaction_cost"]) * (1.0 + fusion_returns["gross_return"]) - 1.0))))
    fusion_trade_residual = float(np.max(np.abs(fusion_weights["trade_weight"] - (fusion_weights["target_weight"] - fusion_weights["pretrade_weight"]))))
    fusion_turnover_ok = True
    for (date, overlay_id), group in fusion_weights.groupby(["date", "overlay_id"], sort=False):
        first_date = fusion_returns.loc[fusion_returns["overlay_id"].eq(overlay_id), "date"].min()
        observed = float(group["turnover"].iloc[0])
        expected = 0.0 if pd.Timestamp(date) == pd.Timestamp(first_date) else 0.5 * float(np.abs(group["trade_weight"]).sum())
        fusion_turnover_ok &= group["turnover"].nunique() == 1 and abs(observed - expected) <= 5e-10
    report.add(
        fusion_cost_residual <= 5e-12 and fusion_net_residual <= 5e-12 and fusion_trade_residual <= 5e-10 and fusion_turnover_ok,
        "fusion_turnover_costs", "Overlay turnover, trade weights, 5-bps costs, and gross/net arithmetic reconcile.",
        "Overlay turnover or transaction-cost arithmetic does not reconcile.",
        observed={"cost": fusion_cost_residual, "net": fusion_net_residual, "trade": fusion_trade_residual},
    )

    fusion_metrics_ok, fusion_metric_error = _metric_reconciliation(fusion_returns, fusion_metrics, "overlay_id")
    report.add(fusion_metrics_ok, "fusion_metric_reconciliation", "All 24 overlay metric rows independently reconcile to daily paths.", "An overlay metric does not reconcile to its daily path.", observed=fusion_metric_error, expected="<=5e-10")

    base_index = base_metrics.set_index("fund_id")
    overlay_index = fusion_metrics.set_index("overlay_id")
    delta_ok = True
    max_delta_error = 0.0
    delta_map = {
        "delta_net_annualised_return": "net_annualised_return",
        "delta_annualised_volatility": "net_annualised_volatility",
        "delta_net_sharpe_ratio": "net_sharpe_ratio",
        "delta_net_max_drawdown": "net_max_drawdown",
        "delta_net_cumulative_return": "net_cumulative_return",
        "delta_average_turnover": "average_rebalance_turnover",
        "delta_total_turnover": "total_turnover",
    }
    for row in comparison.itertuples(index=False):
        overlay = overlay_index.loc[row.overlay_id]
        base = base_index.loc[row.base_fund_id]
        for delta_column, metric_column in delta_map.items():
            error = abs(float(getattr(row, delta_column)) - (float(overlay[metric_column]) - float(base[metric_column])))
            max_delta_error = max(max_delta_error, error)
            delta_ok &= error <= 5e-10
        base_drag = float(base["gross_cumulative_return"] - base["net_cumulative_return"])
        drag_error = abs(float(row.delta_transaction_cost_drag) - (float(overlay["transaction_cost_drag"]) - base_drag))
        max_delta_error = max(max_delta_error, drag_error)
        delta_ok &= drag_error <= 5e-10
    report.add(delta_ok and tuple(comparison["overlay_id"]) == OVERLAY_IDS, "base_delta_reconciliation", "All 24 base-versus-overlay deltas independently reconcile; no result is omitted.", "A base delta is wrong or an overlay is missing.", observed=max_delta_error, expected="<=5e-10")

    paired = comparison.set_index(["base_fund_id", "variant"])
    finance_positive = int((comparison.loc[comparison["variant"].eq("finance_vader_naive"), "delta_net_sharpe_ratio"] > 0).sum())
    plain_positive = int((comparison.loc[comparison["variant"].eq("plain_vader_naive"), "delta_net_sharpe_ratio"] > 0).sum())
    evidence_positive = int((comparison.loc[comparison["variant"].eq("evidence_aware_finance"), "delta_net_sharpe_ratio"] > 0).sum())
    finance_better_sharpe = sum(
        paired.loc[(fund, "finance_vader_naive"), "delta_net_sharpe_ratio"] > paired.loc[(fund, "plain_vader_naive"), "delta_net_sharpe_ratio"]
        for fund in ELIGIBLE_BASE_IDS
    )
    finance_better_return = sum(
        paired.loc[(fund, "finance_vader_naive"), "delta_net_annualised_return"] > paired.loc[(fund, "plain_vader_naive"), "delta_net_annualised_return"]
        for fund in ELIGIBLE_BASE_IDS
    )
    evidence_lower_turnover = all(
        paired.loc[(fund, "evidence_aware_finance"), "delta_average_turnover"] < paired.loc[(fund, "finance_vader_naive"), "delta_average_turnover"]
        for fund in ELIGIBLE_BASE_IDS
    )
    evidence_lower_performance = all(
        paired.loc[(fund, "evidence_aware_finance"), "delta_net_annualised_return"] < paired.loc[(fund, "finance_vader_naive"), "delta_net_annualised_return"]
        and paired.loc[(fund, "evidence_aware_finance"), "delta_net_sharpe_ratio"] < paired.loc[(fund, "finance_vader_naive"), "delta_net_sharpe_ratio"]
        for fund in ELIGIBLE_BASE_IDS
    )
    best = comparison.loc[comparison["delta_net_annualised_return"].idxmax()]
    weakest = comparison.loc[comparison["delta_net_annualised_return"].idxmin()]
    relationships_ok = (
        (finance_positive, plain_positive, evidence_positive) == (5, 4, 4)
        and (finance_better_sharpe, finance_better_return) == (6, 7)
        and evidence_lower_turnover and evidence_lower_performance
        and best.overlay_id == "equity_maximum_sharpe__finance_vader_naive"
        and weakest.overlay_id == "equity_equal_weight__evidence_aware_finance"
        and np.isclose(best.delta_net_annualised_return, 0.0034188, atol=1e-6)
        and np.isclose(best.delta_net_sharpe_ratio, 0.0191935, atol=1e-6)
        and np.isclose(weakest.delta_net_annualised_return, -0.0011572, atol=1e-6)
        and np.isclose(weakest.delta_net_sharpe_ratio, -0.0058965, atol=1e-6)
    )
    report.add(relationships_ok, "expected_result_relationships", "All prespecified paired-result relationships and best/weakest identifiers reproduce from the frozen comparison table.", "A prespecified result direction, population, identifier, or material value differs.")

    hit = _diagnostic_row(diagnostics, "headline", "all", "finance_vader", "custom_finance_term_hit_share")
    changed = _diagnostic_row(diagnostics, "headline", "all", "plain_to_finance", "changed_score_share")
    plain_zero = _diagnostic_row(diagnostics, "headline", "all", "plain_vader", "exact_zero_rate")
    finance_zero = _diagnostic_row(diagnostics, "headline", "all", "finance_vader", "exact_zero_rate")
    plain_neutral = _diagnostic_row(diagnostics, "headline", "all", "plain_vader", "neutral_band_rate")
    finance_neutral = _diagnostic_row(diagnostics, "headline", "all", "finance_vader", "neutral_band_rate")
    sector_hits = diagnostics.loc[(diagnostics["scope"].eq("sector")) & diagnostics["metric"].eq("custom_finance_term_hit_share")].set_index("entity")["value"]
    diagnostic_rates_ok = (
        abs(hit.value - hit.numerator / hit.denominator) <= 1e-12
        and abs(changed.value - changed.numerator / changed.denominator) <= 1e-12
        and np.isclose(hit.value, 0.128053, atol=1e-6)
        and np.isclose(changed.value, 0.127760, atol=1e-6)
        and sector_hits.idxmax() == "Utilities"
        and sector_hits.nlargest(2).index.tolist() == ["Utilities", "Energy"]
    )
    report.add(diagnostic_rates_ok, "sentiment_diagnostic_rates", "Headline rates reconcile to numerators/denominators; Utilities and Energy are the two highest custom-term exposure sectors.", "A headline ratio or sector concentration relationship differs.")

    active = {
        variant: float(_diagnostic_row(diagnostics, "fusion_rebalance_equity_asset", "all", variant, "active_tilt_frequency").value)
        for variant in VARIANTS
    }
    active_ok = (
        np.isclose(active["plain_vader_naive"], 0.746667, atol=1e-6)
        and np.isclose(active["finance_vader_naive"], 0.746667, atol=1e-6)
        and np.isclose(active["evidence_aware_finance"], 0.501111, atol=1e-6)
    )
    report.add(active_ok, "active_tilt_rates", "Evidence-aware activity is about 50.11%, versus 74.67% for each naive variant.", "Active-tilt frequencies differ from the frozen diagnostics.")

    reliability_values = news_rows["reliability"].astype(float)
    report.evidence = {
        "cleaned_headlines": 146_836,
        "mapped_headlines": 146_830,
        "unmapped_headlines": 6,
        "ticker_days": 50_300,
        "sector_days": 10_060,
        "no_news_ticker_days": 12_338,
        "news_ticker_days": 37_962,
        "usable_finance_signals": usable,
        "lagged_finance_signals": lagged,
        "base_metric_max_abs_error": base_metric_error,
        "fusion_metric_max_abs_error": fusion_metric_error,
        "base_delta_max_abs_error": max_delta_error,
        "base_weight_min": base_min,
        "base_weight_max": base_max,
        "base_weight_max_sum_error": max_sum_error,
        "fusion_weight_min": fusion_min,
        "fusion_weight_max": fusion_max,
        "fusion_weight_max_sum_error": fusion_sum_error,
        "combined_max_crypto_difference": max_crypto_difference,
        "combined_max_equity_sleeve_difference": max_sleeve_difference,
        "base_cost_max_abs_error": base_cost_residual,
        "base_net_max_abs_error": base_net_residual,
        "fusion_cost_max_abs_error": fusion_cost_residual,
        "fusion_net_max_abs_error": fusion_net_residual,
        "finance_positive_sharpe_deltas": finance_positive,
        "plain_positive_sharpe_deltas": plain_positive,
        "evidence_positive_sharpe_deltas": evidence_positive,
        "finance_beats_plain_sharpe": int(finance_better_sharpe),
        "finance_beats_plain_return": int(finance_better_return),
        "evidence_lower_turnover_all_eight": bool(evidence_lower_turnover),
        "evidence_lower_return_and_sharpe_all_eight": bool(evidence_lower_performance),
        "best_overlay": best.overlay_id,
        "best_delta_return": float(best.delta_net_annualised_return),
        "best_delta_sharpe": float(best.delta_net_sharpe_ratio),
        "weakest_overlay": weakest.overlay_id,
        "weakest_delta_return": float(weakest.delta_net_annualised_return),
        "weakest_delta_sharpe": float(weakest.delta_net_sharpe_ratio),
        "custom_term_hit_share": float(hit.value),
        "changed_score_share": float(changed.value),
        "plain_exact_zero_rate": float(plain_zero.value),
        "finance_exact_zero_rate": float(finance_zero.value),
        "plain_neutral_band_rate": float(plain_neutral.value),
        "finance_neutral_band_rate": float(finance_neutral.value),
        "sector_custom_hit_shares": {str(key): float(value) for key, value in sector_hits.items()},
        "active_tilt_frequencies": active,
        "reliability": {
            "count": int(reliability_values.count()),
            "mean": float(reliability_values.mean()),
            "std": float(reliability_values.std(ddof=1)),
            "min": float(reliability_values.min()),
            "median": float(reliability_values.median()),
            "q90": float(reliability_values.quantile(0.90)),
            "max": float(reliability_values.max()),
        },
    }

    report.warn("plain_analyzer_runtime_boundary", "Plain-analyzer isolation passed the accepted Stage 7 validator, but analyzer state is not inferable from CSVs alone; the independent exhibit audit checks lexicon content and score-path evidence only.")
    report.warn("extreme_event_limit", "The +/-25% scenario reconciles mechanically, but frozen CSVs cannot economically validate the 69 underlying market moves.")
    report.warn("descriptive_inference_only", "No significance test was prespecified; all comparisons remain descriptive OOS evidence under the frozen sample and specification.")
    return report


def _style_axes(ax: plt.Axes) -> None:
    ax.set_facecolor(PAPER)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#AAB4BE")
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.7, alpha=0.65)
    ax.set_axisbelow(True)


def _header(fig: Figure, title: str, subtitle: str) -> None:
    fig.suptitle(title, x=0.055, y=0.985, ha="left", va="top", fontsize=17, fontweight="bold", color=INK)
    fig.text(0.055, 0.952, subtitle, ha="left", va="top", fontsize=9.5, color=MUTED)


def _footer(fig: Figure, text: str) -> None:
    fig.text(0.055, 0.012, text, ha="left", va="bottom", fontsize=8, color=MUTED)


def _metadata(filename: str, title: str, question: str, x: str, y: str, units: str, dates: str, caveat: str) -> FigureMetadata:
    return FigureMetadata(filename, title, question, x, y, units, dates, caveat)


def plot_fund_growth(frames: Mapping[str, pd.DataFrame]) -> FigureArtifact:
    returns = frames["fund_returns"].copy(deep=True)
    paths = growth_and_drawdown(returns)
    info = returns[["fund_id", "family", "method"]].drop_duplicates()
    paths = paths.merge(info, on="fund_id", how="left", validate="many_to_one")
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=False, constrained_layout=False)
    for ax, family in zip(axes, FAMILIES):
        _style_axes(ax)
        family_paths = paths.loc[paths["family"].eq(family)]
        for method in METHODS:
            series = family_paths.loc[family_paths["method"].eq(method)].sort_values("date")
            ax.plot(series["date"], series["growth"], color=METHOD_COLORS[method], linewidth=2.0, label=method)
        start, end = family_paths["date"].min(), family_paths["date"].max()
        lower = min(1.0, float(family_paths["growth"].min()))
        upper = max(1.0, float(family_paths["growth"].max()))
        span = upper - lower
        padding = max(0.03, span * 0.08)
        ax.set_title(f"{family}  |  {start:%d %b %Y} - {end:%d %b %Y}", loc="left", fontsize=11, color=INK, pad=8)
        ax.set_ylabel("Growth of $1", color=INK)
        ax.set_ylim(max(0.0, lower - padding), upper + padding)
        ax.axhline(1.0, color=MUTED, linewidth=1.0, linestyle="--", zorder=1)
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    axes[0].legend(frameon=False, ncol=4, loc="upper left", fontsize=8.5)
    _header(fig, "Out-of-sample fund growth", "All 12 base funds | panel-specific y-scales | net daily returns after the frozen 5 bps x one-way-turnover cost")
    _footer(fig, "Source: fund_returns.csv. Dashed $1 reference in every panel; family-specific dates retained. Historical OOS evidence, not guaranteed investor returns.")
    fig.subplots_adjust(left=0.08, right=0.98, top=0.91, bottom=0.07, hspace=0.34)
    return FigureArtifact(fig, _metadata(FIGURE_FILENAMES[0], "Out-of-sample fund growth", "How did $1 grow across every family and method?", "Live OOS date", "Growth of $1", "$", "2021-01-01/04 to 2023-12-31/29", "Net of frozen costs; historical OOS evidence only."))


def plot_combined_drawdowns(frames: Mapping[str, pd.DataFrame]) -> FigureArtifact:
    returns = frames["fund_returns"].copy(deep=True)
    combined = returns.loc[returns["family"].eq("Combined")]
    paths = growth_and_drawdown(combined).merge(combined[["fund_id", "method"]].drop_duplicates(), on="fund_id", validate="many_to_one")
    fig, ax = plt.subplots(figsize=(12, 7))
    _style_axes(ax)
    for method in METHODS:
        series = paths.loc[paths["method"].eq(method)].sort_values("date")
        ax.plot(series["date"], series["drawdown"], color=METHOD_COLORS[method], linewidth=2.0, label=method)
    ax.axhline(0, color=INK, linewidth=1.0)
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_ylabel("Drawdown from prior peak", color=INK)
    ax.set_xlabel("Live OOS date", color=INK)
    ax.set_ylim(min(-0.32, float(paths["drawdown"].min()) * 1.08), 0.015)
    ax.legend(frameon=False, ncol=2, loc="lower left")
    _header(fig, "Combined-fund drawdowns", "All four frozen Combined methods | net returns | 04 Jan 2021 - 29 Dec 2023")
    _footer(fig, "Source: fund_returns.csv. Drawdown is recomputed from compounded net wealth; zero marks the running peak.")
    fig.subplots_adjust(left=0.10, right=0.98, top=0.89, bottom=0.12)
    return FigureArtifact(fig, _metadata(FIGURE_FILENAMES[1], "Combined-fund drawdowns", "How severe and persistent were losses from prior peaks in the required Combined product?", "Live OOS date", "Drawdown", "%", "2021-01-04 to 2023-12-29", "All Combined methods retained; no ex-post winner selection."))


def combined_weight_frame(frames: Mapping[str, pd.DataFrame]) -> tuple[pd.DataFrame, tuple[str, ...]]:
    weights = frames["fund_weights"].copy(deep=True)
    combined = weights.loc[weights["family"].eq("Combined"), ["date", "fund_id", "method", "ticker", "target_weight"]]
    equities = combined.loc[~combined["ticker"].isin(CRYPTO_TICKERS)]
    ranking = equities.groupby("ticker", observed=True)["target_weight"].mean().reset_index()
    ranking = ranking.sort_values(["target_weight", "ticker"], ascending=[False, True], kind="mergesort")
    top = tuple(ranking.head(6)["ticker"])
    combined["display_asset"] = np.select(
        [combined["ticker"].isin(top), combined["ticker"].isin(CRYPTO_TICKERS)],
        [combined["ticker"], "Crypto sleeve"],
        default="Other equities",
    )
    aggregated = combined.groupby(["date", "fund_id", "method", "display_asset"], observed=True, sort=False)["target_weight"].sum().reset_index()
    return aggregated, top


def plot_combined_weights(frames: Mapping[str, pd.DataFrame]) -> FigureArtifact:
    weights, top = combined_weight_frame(frames)
    categories = list(top) + ["Crypto sleeve", "Other equities"]
    palette = ["#264653", "#2A9D8F", "#457B9D", "#8AB17D", "#E9C46A", "#F4A261", "#8D6E9F", "#CBD2D9"]
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True, sharey=True)
    for ax, method in zip(axes.flat, METHODS):
        _style_axes(ax)
        part = weights.loc[weights["method"].eq(method)].pivot(index="date", columns="display_asset", values="target_weight").fillna(0.0)
        part = part.reindex(columns=categories, fill_value=0.0)
        ax.stackplot(part.index, [part[column] for column in categories], labels=categories, colors=palette, alpha=0.92, linewidth=0)
        ax.set_title(method, loc="left", fontsize=11, color=METHOD_COLORS[method], fontweight="bold")
        ax.set_ylim(0, 1)
        ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    axes[0, 0].set_ylabel("Target weight", color=INK)
    axes[1, 0].set_ylabel("Target weight", color=INK)
    handles = [Patch(facecolor=color, label=label) for color, label in zip(palette, categories)]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.53, 0.925), ncol=5, frameon=False, fontsize=8.5)
    _header(fig, "Combined target weights through time", "Six highest-mean equity tickers across all Combined funds + Crypto sleeve + Other equities; every target weight retained")
    _footer(fig, "Source: fund_weights.csv. Crypto sleeve sums all 10 frozen crypto assets; Other equities sums the remaining 44 equities. No omission or renormalisation; each stack sums to 100%.")
    fig.subplots_adjust(left=0.08, right=0.98, top=0.84, bottom=0.08, hspace=0.22, wspace=0.12)
    artifact = FigureArtifact(fig, _metadata(FIGURE_FILENAMES[2], "Combined target weights through time", "How did the required Combined product allocate across assets under each method?", "Rebalance date", "Target weight", "%", "2021-01-04 to 2023-12-01", f"Six-equity rule is deterministic; all crypto assets form Crypto sleeve and the remaining {50-len(top)} equities form Other equities without renormalisation."))
    setattr(artifact.figure, "_fins_top_assets", top)
    setattr(artifact.figure, "_fins_display_categories", tuple(categories))
    return artifact


def plot_risk_return_map(frames: Mapping[str, pd.DataFrame]) -> FigureArtifact:
    metrics = frames["performance_metrics"].copy(deep=True)
    method_short = {"Equal Weight": "EW", "Minimum Variance": "MV", "Maximum Sharpe": "MS", "Risk Parity": "RP"}
    family_short = {"Equity": "E", "Crypto": "C", "Combined": "M"}
    offsets = {
        "equity_equal_weight": (-50, 10),
        "equity_minimum_variance": (-48, -20),
        "equity_maximum_sharpe": (10, -20),
        "equity_risk_parity": (-42, -18),
        "crypto_equal_weight": (10, -22),
        "crypto_minimum_variance": (10, -18),
        "crypto_maximum_sharpe": (10, 10),
        "crypto_risk_parity": (10, 10),
        "combined_equal_weight": (10, -18),
        "combined_minimum_variance": (10, 11),
        "combined_maximum_sharpe": (10, 10),
        "combined_risk_parity": (10, 10),
    }
    fig, ax = plt.subplots(figsize=(12, 7))
    _style_axes(ax)
    sharpes = metrics["net_sharpe_ratio"].to_numpy(dtype=float)
    sizes = 80 + 170 * (sharpes - sharpes.min()) / max(sharpes.max() - sharpes.min(), 1e-12)
    for row, size in zip(metrics.itertuples(index=False), sizes):
        ax.scatter(row.net_annualised_volatility, row.net_annualised_return, s=size, color=METHOD_COLORS[row.method], marker=FAMILY_MARKERS[row.family], edgecolor="white", linewidth=1.0, zorder=3)
        ax.annotate(
            f"{family_short[row.family]}-{method_short[row.method]}",
            (row.net_annualised_volatility, row.net_annualised_return),
            xytext=offsets[row.fund_id],
            textcoords="offset points",
            fontsize=8,
            color=INK,
            arrowprops={"arrowstyle": "-", "color": "#8A96A3", "lw": 0.65},
            bbox={"facecolor": PAPER, "edgecolor": "none", "alpha": 0.82, "pad": 0.8},
        )
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("Annualised net volatility", color=INK)
    ax.set_ylabel("Annualised net return", color=INK)
    method_handles = [Line2D([0], [0], marker="o", color="none", markerfacecolor=color, markeredgecolor="white", markersize=9, label=method) for method, color in METHOD_COLORS.items()]
    family_handles = [Line2D([0], [0], marker=marker, color=INK, linestyle="none", markerfacecolor="none", markersize=8, label=family) for family, marker in FAMILY_MARKERS.items()]
    first = ax.legend(handles=method_handles, title="Method colour", loc="upper left", frameon=False, fontsize=8, title_fontsize=8)
    ax.add_artist(first)
    ax.legend(handles=family_handles, title="Family marker", loc="upper center", frameon=False, fontsize=8, title_fontsize=8)
    _header(fig, "Base funds: risk, return, and Sharpe", "All 12 net OOS funds | marker area increases with zero-risk-free-rate Sharpe | E=Equity, C=Crypto, M=Combined")
    _footer(fig, "Source: performance_metrics.csv. Annualisation is 252 for Equity/Combined and 365 for Crypto; cross-family risk differs materially.")
    fig.subplots_adjust(left=0.10, right=0.98, top=0.89, bottom=0.12)
    return FigureArtifact(fig, _metadata(FIGURE_FILENAMES[3], "Base funds: risk, return, and Sharpe", "How do all 12 base funds compare on annualised net return, volatility, and Sharpe?", "Annualised net volatility", "Annualised net return", "% and Sharpe marker area", "2021-2023 family-specific live periods", "Calendar-specific annualisation; marker size is descriptive, not a second axis."))


def plot_sector_sentiment(frames: Mapping[str, pd.DataFrame]) -> FigureArtifact:
    sector = frames["sector_sentiment"].copy(deep=True)
    sector["rolling_21"] = sector.groupby("sector", sort=False)["finance_compound"].transform(lambda values: values.rolling(21, min_periods=1).mean())
    max_abs = float(np.nanmax(np.abs(sector["finance_compound"])))
    limit = min(1.0, max(0.5, np.ceil(max_abs * 10) / 10))
    fig, axes = plt.subplots(5, 2, figsize=(12, 14), sharex=True, sharey=True)
    for ax, raw_sector in zip(axes.flat, SECTOR_ORDER):
        _style_axes(ax)
        part = sector.loc[sector["sector"].eq(raw_sector)].sort_values("date")
        ax.plot(part["date"], part["finance_compound"], color="#9DB7C8", alpha=0.35, linewidth=0.7, label="Daily")
        ax.plot(part["date"], part["rolling_21"], color="#E07A24", linewidth=1.8, label="21-day visual mean")
        ax.axhline(0, color=INK, linewidth=0.75, alpha=0.7)
        ax.set_ylim(-limit, limit)
        ax.set_title(SECTOR_DISPLAY[raw_sector], loc="left", fontsize=10, color=INK, fontweight="bold")
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    axes[0, 0].legend(frameon=False, ncol=2, loc="upper left", fontsize=8)
    for ax in axes[:, 0]:
        ax.set_ylabel("Finance compound", color=INK)
    _header(fig, "Finance-VADER sentiment across equity sectors", "Daily equal-weight ticker sentiment and 21-trading-day rolling mean | common y-scale | 02 Jan 2020 - 29 Dec 2023")
    _footer(fig, "Source: sector_sentiment_index.csv. Smoothing is visual only and was never used for trading; no-news tickers are not scored as zero.")
    fig.subplots_adjust(left=0.08, right=0.98, top=0.93, bottom=0.06, hspace=0.28, wspace=0.10)
    return FigureArtifact(fig, _metadata(FIGURE_FILENAMES[4], "Finance-VADER sentiment across equity sectors", "How did the frozen sector sentiment index evolve across all ten sectors?", "Equity trading date", "Finance-VADER compound", "VADER compound [-1,1]", "2020-01-02 to 2023-12-29", "21-day mean is visual only; ticker no-news states are excluded from score denominators."))


def _base_labels() -> list[str]:
    labels = []
    short = {"equal_weight": "EW", "minimum_variance": "MV", "maximum_sharpe": "MS", "risk_parity": "RP"}
    for fund in ELIGIBLE_BASE_IDS:
        family, method = fund.split("_", 1)
        labels.append(f"{'Eq' if family == 'equity' else 'Comb'}\n{short[method]}")
    return labels


def plot_fusion_before_after(frames: Mapping[str, pd.DataFrame]) -> FigureArtifact:
    comparison = frames["fusion_comparison"].copy(deep=True)
    labels = _base_labels()
    x = np.arange(len(ELIGIBLE_BASE_IDS))
    width = 0.24
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    for ax in axes:
        _style_axes(ax)
        ax.axhline(0, color=INK, linewidth=1.0)
    for offset, variant in enumerate(VARIANTS):
        ordered = comparison.loc[comparison["variant"].eq(variant)].set_index("base_fund_id").reindex(ELIGIBLE_BASE_IDS)
        axes[0].bar(x + (offset - 1) * width, ordered["delta_net_annualised_return"] * 10_000, width=width, color=VARIANT_COLORS[variant], label=VARIANT_LABELS[variant])
        axes[1].bar(x + (offset - 1) * width, ordered["delta_net_sharpe_ratio"], width=width, color=VARIANT_COLORS[variant])
    axes[0].set_ylabel("Annualised-return delta (bp)", color=INK)
    axes[1].set_ylabel("Sharpe delta", color=INK)
    axes[1].set_xticks(x, labels)
    axes[1].set_xlabel("Corresponding frozen base fund", color=INK)
    axes[0].legend(frameon=False, ncol=3, loc="upper left")
    _header(fig, "Sentiment fusion: complete before-versus-after evidence", "Overlay minus corresponding frozen base | all eight eligible funds and all three prespecified variants")
    _footer(fig, "Source: fusion_comparison.csv. Negative bars are retained; comparisons are descriptive and no significance test was prespecified.")
    fig.subplots_adjust(left=0.10, right=0.98, top=0.89, bottom=0.12, hspace=0.16)
    return FigureArtifact(fig, _metadata(FIGURE_FILENAMES[5], "Sentiment fusion: complete before-versus-after evidence", "Did each frozen sentiment overlay change return and Sharpe relative to its own base?", "Base fund", "Overlay minus base", "basis points and Sharpe units", "2021-01-04 to 2023-12-29", "All 24 overlays retained; no statistical-significance claim."))


def plot_sentiment_diagnostics(frames: Mapping[str, pd.DataFrame]) -> FigureArtifact:
    diagnostics = frames["sentiment_diagnostics"].copy(deep=True)
    def value(scope: str, entity: str, model: str, metric: str) -> float:
        return float(_diagnostic_row(diagnostics, scope, entity, model, metric).value)
    rate_names = ["Exact zero", "Neutral band"]
    plain_rates = [value("headline", "all", "plain_vader", "exact_zero_rate"), value("headline", "all", "plain_vader", "neutral_band_rate")]
    finance_rates = [value("headline", "all", "finance_vader", "exact_zero_rate"), value("headline", "all", "finance_vader", "neutral_band_rate")]
    overall_names = ["Custom-term\nhit share", "Changed-score\nshare"]
    overall_values = [value("headline", "all", "finance_vader", "custom_finance_term_hit_share"), value("headline", "all", "plain_to_finance", "changed_score_share")]
    sector_hits = diagnostics.loc[(diagnostics["scope"].eq("sector")) & diagnostics["metric"].eq("custom_finance_term_hit_share")].copy()
    sector_hits = sector_hits.sort_values(["value", "entity"], ascending=[True, True], kind="mergesort")
    fig = plt.figure(figsize=(13, 8))
    grid = fig.add_gridspec(2, 2, height_ratios=[1, 1.5])
    ax_rates = fig.add_subplot(grid[0, 0])
    ax_overall = fig.add_subplot(grid[0, 1])
    ax_sector = fig.add_subplot(grid[1, :])
    for ax in (ax_rates, ax_overall, ax_sector):
        _style_axes(ax)
    x = np.arange(2)
    ax_rates.bar(x - 0.18, plain_rates, width=0.36, color="#3A7CA5", label="Plain")
    ax_rates.bar(x + 0.18, finance_rates, width=0.36, color="#E07A24", label="Finance")
    ax_rates.set_xticks(x, rate_names)
    ax_rates.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax_rates.set_ylim(0, 0.60)
    ax_rates.set_title("Headline score diagnostics", loc="left", fontsize=11, color=INK, fontweight="bold")
    ax_rates.legend(frameon=False, ncol=2, fontsize=8)
    for pos, val in zip(x - 0.18, plain_rates): ax_rates.text(pos, val + 0.012, f"{val:.1%}", ha="center", fontsize=8, color=INK)
    for pos, val in zip(x + 0.18, finance_rates): ax_rates.text(pos, val + 0.012, f"{val:.1%}", ha="center", fontsize=8, color=INK)
    ax_overall.bar(np.arange(2), overall_values, color=["#178F8F", "#E07A24"], width=0.56)
    ax_overall.set_xticks(np.arange(2), overall_names)
    ax_overall.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax_overall.set_ylim(0, 0.16)
    ax_overall.set_title("Lexicon reach", loc="left", fontsize=11, color=INK, fontweight="bold")
    for pos, val in enumerate(overall_values): ax_overall.text(pos, val + 0.004, f"{val:.2%}", ha="center", fontsize=9, color=INK)
    highlight = sector_hits["entity"].isin(["Utilities", "Energy"])
    colors = np.where(highlight, "#E07A24", "#3A7CA5")
    ax_sector.barh(sector_hits["entity"].map(SECTOR_DISPLAY), sector_hits["value"], color=colors)
    ax_sector.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax_sector.set_xlabel("Headlines containing ≥1 reviewed custom term", color=INK)
    ax_sector.set_title("Custom-term exposure by sector", loc="left", fontsize=11, color=INK, fontweight="bold")
    for y, val in enumerate(sector_hits["value"]): ax_sector.text(val + 0.004, y, f"{val:.1%}", va="center", fontsize=8, color=INK)
    ax_sector.text(0.99, 0.04, "Utilities and Energy are exposure concentrations,\nnot evidence of sentiment accuracy.", transform=ax_sector.transAxes, ha="right", va="bottom", fontsize=9, color="#9A4D12", bbox={"facecolor": "#FFF3E8", "edgecolor": "#F3C49A", "boxstyle": "round,pad=0.4"})
    _header(fig, "What the reviewed finance lexicon changes", "All 146,830 mapped headlines | exposure to reviewed terms is not contextual accuracy")
    _footer(fig, "Source: sentiment_diagnostics.csv. Exact zero and |compound| < 0.05 are distinct.\nHigher Finance zero/neutral rates partly reflect intentional neutralisation of generic finance words with inappropriate vanilla polarity; this does not imply lower information coverage.")
    fig.subplots_adjust(left=0.10, right=0.97, top=0.88, bottom=0.12, hspace=0.42, wspace=0.26)
    return FigureArtifact(fig, _metadata(FIGURE_FILENAMES[6], "What the reviewed finance lexicon changes", "How materially does the reviewed lexicon alter scoring, and where are its terms concentrated?", "Diagnostic category / sector", "Rate", "% of mapped headlines", "2020-01-02 to 2023-12-29", "Term exposure is not sentiment accuracy; two examples or high frequency do not prove contextual validity."))


def plot_fusion_turnover_tradeoff(frames: Mapping[str, pd.DataFrame]) -> FigureArtifact:
    comparison = frames["fusion_comparison"].copy(deep=True)
    fig, ax = plt.subplots(figsize=(12, 7))
    _style_axes(ax)
    ax.axhline(0, color=INK, linewidth=1.0)
    ax.axvline(0, color=INK, linewidth=1.0)
    for variant in VARIANTS:
        part = comparison.loc[comparison["variant"].eq(variant)]
        ax.scatter(part["delta_average_turnover"] * 100, part["delta_net_sharpe_ratio"], s=75, color=VARIANT_COLORS[variant], marker=VARIANT_MARKERS[variant], edgecolor="white", linewidth=0.8, label=VARIANT_LABELS[variant], zorder=3)
    strongest = comparison.loc[comparison["delta_net_sharpe_ratio"].idxmax()]
    weakest = comparison.loc[comparison["delta_net_sharpe_ratio"].idxmin()]
    display_names = {
        "equity_maximum_sharpe__finance_vader_naive": "Equity Maximum Sharpe + Finance VADER",
        "equity_equal_weight__evidence_aware_finance": "Equity Equal Weight + Evidence-aware Finance",
    }
    for row, offset in ((strongest, (8, 8)), (weakest, (8, -15))):
        name = display_names[str(row.overlay_id)]
        ax.annotate(f"{name}\nSharpe delta {row.delta_net_sharpe_ratio:+.4f}", (row.delta_average_turnover * 100, row.delta_net_sharpe_ratio), xytext=offset, textcoords="offset points", fontsize=8, color=INK, arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.7})
    evidence = comparison.loc[comparison["variant"].eq("evidence_aware_finance")]
    ax.annotate("Lower incremental turnover, but lower Sharpe\nthan naive Finance in all 8 paired comparisons.", (float((evidence["delta_average_turnover"] * 100).mean()), float(evidence["delta_net_sharpe_ratio"].mean())), xytext=(42, 15), textcoords="offset points", fontsize=9, color="#0E6868", arrowprops={"arrowstyle": "->", "color": "#178F8F", "lw": 1.0}, bbox={"facecolor": "#E8F6F5", "edgecolor": "#9ED5D1", "boxstyle": "round,pad=0.4"})
    ax.set_xlabel("Incremental average rebalance turnover vs base (percentage points)", color=INK)
    ax.set_ylabel("Change in Sharpe ratio", color=INK)
    ax.legend(frameon=False, ncol=3, loc="upper right")
    _header(fig, "Sentiment selectivity, turnover, and Sharpe", "All 24 overlays | every point is overlay minus its frozen base | zero lines retain unfavourable outcomes")
    _footer(fig, "Source: fusion_comparison.csv. This is a descriptive trade-off view, not an efficient frontier or causal estimate.")
    fig.subplots_adjust(left=0.10, right=0.98, top=0.89, bottom=0.12)
    return FigureArtifact(fig, _metadata(FIGURE_FILENAMES[7], "Sentiment selectivity, turnover, and Sharpe", "How does each sentiment variant trade off extra turnover against its Sharpe change?", "Incremental average rebalance turnover vs base", "Delta Sharpe", "percentage points and Sharpe units", "2021-01-04 to 2023-12-29", "Descriptive trade-off only; no efficient-frontier, significance, or causal claim."))


def build_figure_artifacts(frames: Mapping[str, pd.DataFrame]) -> list[FigureArtifact]:
    """Build every authorised figure deterministically in filename order."""
    with plt.rc_context({
        "font.family": "DejaVu Sans",
        "figure.facecolor": PAPER,
        "savefig.facecolor": PAPER,
        "axes.labelsize": 10,
        "axes.titlesize": 11,
        "text.color": INK,
        "axes.labelcolor": INK,
        "axes.titlecolor": INK,
        "legend.fontsize": 9,
        "path.simplify": False,
    }):
        return [
            plot_fund_growth(frames),
            plot_combined_drawdowns(frames),
            plot_combined_weights(frames),
            plot_risk_return_map(frames),
            plot_sector_sentiment(frames),
            plot_fusion_before_after(frames),
            plot_sentiment_diagnostics(frames),
            plot_fusion_turnover_tradeoff(frames),
        ]


__all__ = [
    "AuditFinding", "AuditReport", "CANONICAL_INPUTS", "FIGURE_FILENAMES",
    "FROZEN_SHA256", "FigureArtifact", "FigureMetadata", "SCHEMAS",
    "audit_canonical_outputs", "build_figure_artifacts", "canonical_hashes",
    "combined_weight_frame", "file_sha256", "growth_and_drawdown",
    "independent_path_metrics", "load_canonical_outputs",
]
