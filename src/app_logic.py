"""Pure display and investor-journey calculations for the MAIA app.

All functions operate on already-generated canonical artifacts.  Nothing here
estimates a portfolio, scores text, changes a frozen signal, or writes output.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Mapping, Sequence

import numpy as np
import pandas as pd


CRYPTO_TICKERS = frozenset(
    {
        "ADA-USD", "BCH-USD", "BTC-USD", "EOS-USD", "ETC-USD",
        "ETH-USD", "LTC-USD", "TRX-USD", "XLM-USD", "XRP-USD",
    }
)
MANAGEMENT_FEE_RATE = 0.005
TRADING_COST_BPS = 5.0
METHOD_DESCRIPTIONS = {
    "Equal Weight": "A transparent diversified benchmark.",
    "Minimum Variance": "Seeks the lowest estimated portfolio variance using prior observations.",
    "Maximum Sharpe": "Seeks the highest estimated return per unit of risk using a zero risk-free rate.",
    "Risk Parity": "Seeks to balance portfolio risk contributions.",
}
VARIANT_LABELS = {
    "plain_vader_naive": "Plain VADER",
    "finance_vader_naive": "Finance VADER",
    "evidence_aware_finance": "Evidence-aware Finance",
}


class AppLogicError(ValueError):
    """A deterministic user-input or artifact-relationship error."""


@dataclass(frozen=True)
class AllocationValidation:
    valid: bool
    total_percent: float
    message: str


@dataclass(frozen=True)
class CalendarReconciliation:
    returns: pd.DataFrame
    start_date: pd.Timestamp
    end_date: pd.Timestamp
    annualisation: int
    calendar_label: str


def human_fund_name(family: str, method: str) -> str:
    return f"{family} — {method}"


def fund_name_map(metrics: pd.DataFrame) -> dict[str, str]:
    required = {"fund_id", "family", "method"}
    if not required.issubset(metrics.columns):
        raise AppLogicError(f"Fund metrics are missing {sorted(required - set(metrics.columns))}.")
    unique = metrics.loc[:, ["fund_id", "family", "method"]].drop_duplicates()
    if unique["fund_id"].duplicated().any():
        raise AppLogicError("A fund ID maps to more than one family or method.")
    return {
        row.fund_id: human_fund_name(row.family, row.method)
        for row in unique.itertuples(index=False)
    }


def growth_of_one(
    returns: pd.DataFrame,
    *,
    id_column: str = "fund_id",
    return_column: str = "net_return",
) -> pd.DataFrame:
    required = {"date", id_column, return_column}
    if not required.issubset(returns.columns):
        raise AppLogicError(f"Growth input is missing {sorted(required - set(returns.columns))}.")
    work = returns.loc[:, ["date", id_column, return_column]].copy(deep=True)
    work["date"] = pd.to_datetime(work["date"])
    if work.duplicated(["date", id_column]).any():
        raise AppLogicError("Growth input has duplicate date/fund keys.")
    values = work[return_column].to_numpy(dtype="float64")
    if not np.isfinite(values).all() or np.any(values <= -1.0):
        raise AppLogicError("Growth input requires finite returns greater than -100%.")
    work = work.sort_values([id_column, "date"], kind="mergesort")
    work["growth"] = work.groupby(id_column, sort=False)[return_column].transform(
        lambda series: (1.0 + series).cumprod()
    )
    return work.sort_values(["date", id_column], kind="mergesort").reset_index(drop=True)


def growth_and_drawdown(
    returns: pd.DataFrame,
    *,
    id_column: str = "fund_id",
    return_column: str = "net_return",
) -> pd.DataFrame:
    paths = growth_of_one(returns, id_column=id_column, return_column=return_column)
    paths = paths.sort_values([id_column, "date"], kind="mergesort")
    paths["drawdown"] = paths.groupby(id_column, sort=False)["growth"].transform(
        lambda series: series / series.cummax() - 1.0
    )
    return paths.sort_values(["date", id_column], kind="mergesort").reset_index(drop=True)


def latest_target_holdings(
    weights: pd.DataFrame,
    fund_id: str,
    *,
    tolerance: float = 1e-8,
) -> pd.DataFrame:
    required = {"date", "fund_id", "ticker", "target_weight", "family", "method"}
    if not required.issubset(weights.columns):
        raise AppLogicError(f"Holdings input is missing {sorted(required - set(weights.columns))}.")
    fund = weights.loc[weights["fund_id"].eq(fund_id)].copy(deep=True)
    if fund.empty:
        raise AppLogicError(f"No holdings are available for fund '{fund_id}'.")
    fund["date"] = pd.to_datetime(fund["date"])
    latest_date = fund["date"].max()
    latest = fund.loc[fund["date"].eq(latest_date)].copy(deep=True)
    if latest["ticker"].duplicated().any():
        raise AppLogicError(f"Latest holdings for '{fund_id}' contain duplicate tickers.")
    values = latest["target_weight"].to_numpy(dtype="float64")
    if not np.isfinite(values).all() or np.any(values < -tolerance) or np.any(values > 0.20 + tolerance):
        raise AppLogicError(f"Latest holdings for '{fund_id}' violate the frozen bounds.")
    if abs(float(values.sum()) - 1.0) > tolerance:
        raise AppLogicError(f"Latest target holdings for '{fund_id}' do not sum to one.")
    latest["asset_class"] = np.where(latest["ticker"].isin(CRYPTO_TICKERS), "Crypto", "Equity")
    return latest.sort_values(["target_weight", "ticker"], ascending=[False, True], kind="mergesort").reset_index(drop=True)


def current_holdings_date(holdings: pd.DataFrame) -> pd.Timestamp:
    if holdings.empty or "date" not in holdings:
        raise AppLogicError("Current holdings are unavailable.")
    dates = pd.to_datetime(holdings["date"]).dropna().unique()
    if len(dates) != 1:
        raise AppLogicError("Current holdings must have one effective rebalance date.")
    return pd.Timestamp(dates[0])


def asset_class_exposures(holdings: pd.DataFrame) -> pd.DataFrame:
    required = {"ticker", "target_weight"}
    if not required.issubset(holdings.columns):
        raise AppLogicError("Holdings do not contain ticker and target_weight.")
    work = holdings.loc[:, ["ticker", "target_weight"]].copy(deep=True)
    work["asset_class"] = np.where(work["ticker"].isin(CRYPTO_TICKERS), "Crypto", "Equity")
    exposure = work.groupby("asset_class", sort=False, observed=True)["target_weight"].sum()
    exposure = exposure.reindex(["Equity", "Crypto"], fill_value=0.0)
    return exposure.rename("target_weight").reset_index()


def validate_user_allocation(
    selected_funds: Sequence[str],
    allocations_percent: Mapping[str, float],
    *,
    step_percent: int = 5,
) -> AllocationValidation:
    funds = tuple(selected_funds)
    if len(set(funds)) != len(funds):
        return AllocationValidation(False, float("nan"), "Each selected fund must be unique.")
    if not 2 <= len(funds) <= 4:
        return AllocationValidation(False, float("nan"), "Choose between two and four base funds.")
    if set(allocations_percent) != set(funds):
        return AllocationValidation(False, float("nan"), "Every selected fund needs one allocation value.")
    values = np.array([allocations_percent[fund] for fund in funds], dtype="float64")
    if not np.isfinite(values).all() or np.any(values <= 0.0) or np.any(values > 100.0):
        return AllocationValidation(False, float(values.sum()), "Each selected fund must receive between 5% and 100%.")
    units = values / float(step_percent)
    if not np.allclose(units, np.round(units), rtol=0.0, atol=1e-9):
        return AllocationValidation(False, float(values.sum()), f"Allocations must use {step_percent}-percentage-point increments.")
    total = float(values.sum())
    if not np.isclose(total, 100.0, rtol=0.0, atol=1e-9):
        return AllocationValidation(False, total, "Total allocation must equal exactly 100%; MAIA will not normalise it silently.")
    return AllocationValidation(True, total, "Allocation is valid and totals 100%.")


def equal_split_percentages(selected_funds: Sequence[str], *, step_percent: int = 5) -> dict[str, float]:
    funds = tuple(selected_funds)
    if not 2 <= len(funds) <= 4:
        raise AppLogicError("Equal split requires between two and four funds.")
    total_units = 100 // step_percent
    base_units, remainder = divmod(total_units, len(funds))
    units = [base_units + (1 if index < remainder else 0) for index in range(len(funds))]
    return {fund: float(unit * step_percent) for fund, unit in zip(funds, units)}


def reconcile_return_calendars(
    fund_returns: pd.DataFrame,
    selected_funds: Sequence[str],
) -> CalendarReconciliation:
    required = {"date", "fund_id", "family", "net_return"}
    if not required.issubset(fund_returns.columns):
        raise AppLogicError(f"Fund returns are missing {sorted(required - set(fund_returns.columns))}.")
    funds = tuple(selected_funds)
    if not funds:
        raise AppLogicError("At least one fund is required for calendar reconciliation.")
    work = fund_returns.loc[fund_returns["fund_id"].isin(funds), list(required)].copy(deep=True)
    work["date"] = pd.to_datetime(work["date"])
    if work.empty or set(work["fund_id"].unique()) != set(funds):
        raise AppLogicError("One or more selected funds are absent from canonical returns.")
    identity = work.loc[:, ["fund_id", "family"]].drop_duplicates()
    if identity["fund_id"].duplicated().any():
        raise AppLogicError("A selected fund has inconsistent family metadata.")
    family = identity.set_index("fund_id")["family"].to_dict()
    start = max(work.loc[work["fund_id"].eq(fund), "date"].min() for fund in funds)
    end = min(work.loc[work["fund_id"].eq(fund), "date"].max() for fund in funds)
    if pd.isna(start) or pd.isna(end) or start > end:
        raise AppLogicError("Selected funds have no common historical OOS period.")

    all_crypto = all(family[fund] == "Crypto" for fund in funds)
    if all_crypto:
        date_sets = [
            set(work.loc[work["fund_id"].eq(fund), "date"])
            for fund in funds
        ]
        common = set.intersection(*date_sets)
        display_dates = pd.DatetimeIndex(sorted(date for date in common if start <= date <= end))
        annualisation = 365
        label = "Shared native Crypto calendar (weekends retained)"
    else:
        non_crypto = [fund for fund in funds if family[fund] != "Crypto"]
        date_sets = [
            set(work.loc[work["fund_id"].eq(fund), "date"])
            for fund in non_crypto
        ]
        common = set.intersection(*date_sets)
        display_dates = pd.DatetimeIndex(sorted(date for date in common if start <= date <= end))
        annualisation = 252
        label = "Shared Equity/Combined display calendar; Crypto weekend returns compounded into the next display date"
    if display_dates.empty:
        raise AppLogicError("The selected funds have an empty common display calendar.")

    reconciled = pd.DataFrame({"date": display_dates})
    for fund in funds:
        series = (
            work.loc[work["fund_id"].eq(fund), ["date", "net_return"]]
            .sort_values("date", kind="mergesort")
            .drop_duplicates("date")
        )
        values = series["net_return"].to_numpy(dtype="float64")
        if not np.isfinite(values).all() or np.any(values <= -1.0):
            raise AppLogicError(f"Fund '{fund}' has an invalid canonical return.")
        if family[fund] == "Crypto" and not all_crypto:
            interval_values: list[float] = []
            previous: pd.Timestamp | None = None
            for display_date in display_dates:
                if previous is None:
                    mask = series["date"].eq(display_date)
                else:
                    mask = series["date"].gt(previous) & series["date"].le(display_date)
                interval = series.loc[mask, "net_return"].to_numpy(dtype="float64")
                if len(interval) == 0:
                    raise AppLogicError(f"Crypto return interval is empty for '{fund}' at {display_date:%Y-%m-%d}.")
                interval_values.append(float(np.prod(1.0 + interval) - 1.0))
                previous = pd.Timestamp(display_date)
            reconciled[fund] = interval_values
        else:
            indexed = series.set_index("date")["net_return"].reindex(display_dates)
            if indexed.isna().any():
                raise AppLogicError(f"Fund '{fund}' is missing a return on the common display calendar.")
            reconciled[fund] = indexed.to_numpy(dtype="float64")
    return CalendarReconciliation(
        returns=reconciled,
        start_date=pd.Timestamp(display_dates[0]),
        end_date=pd.Timestamp(display_dates[-1]),
        annualisation=annualisation,
        calendar_label=label,
    )


def build_allocation_history(
    fund_returns: pd.DataFrame,
    selected_funds: Sequence[str],
    allocations_percent: Mapping[str, float],
    initial_capital: float,
    *,
    annual_management_fee: float = MANAGEMENT_FEE_RATE,
) -> tuple[pd.DataFrame, CalendarReconciliation]:
    validation = validate_user_allocation(selected_funds, allocations_percent)
    if not validation.valid:
        raise AppLogicError(validation.message)
    if not np.isfinite(initial_capital) or initial_capital <= 0:
        raise AppLogicError("Initial capital must be a positive finite amount.")
    if not 0 <= annual_management_fee < 1:
        raise AppLogicError("The illustrative management fee must lie in [0, 1).")

    calendar = reconcile_return_calendars(fund_returns, selected_funds)
    history = pd.DataFrame({"date": calendar.returns["date"]})
    sleeve_columns: list[str] = []
    for fund in selected_funds:
        allocation = float(allocations_percent[fund]) / 100.0
        sleeve = initial_capital * allocation * (1.0 + calendar.returns[fund]).cumprod()
        column = f"sleeve__{fund}"
        history[column] = sleeve.to_numpy(dtype="float64")
        sleeve_columns.append(column)
    history["before_management_fee"] = history[sleeve_columns].sum(axis=1)
    elapsed_days = (history["date"] - calendar.start_date).dt.days.astype("float64")
    fee_factor = (1.0 - annual_management_fee) ** (elapsed_days / 365.0)
    history["after_management_fee"] = history["before_management_fee"] * fee_factor
    history["management_fee_drag"] = history["before_management_fee"] - history["after_management_fee"]

    before_base = np.r_[initial_capital, history["before_management_fee"].to_numpy(dtype="float64")]
    after_base = np.r_[initial_capital, history["after_management_fee"].to_numpy(dtype="float64")]
    history["account_return_before_fee"] = before_base[1:] / before_base[:-1] - 1.0
    history["account_return_after_fee"] = after_base[1:] / after_base[:-1] - 1.0
    if not np.isfinite(history.select_dtypes(include=["number"]).to_numpy()).all():
        raise AppLogicError("Allocation history produced a non-finite value.")
    return history, calendar


def allocation_performance_metrics(
    history: pd.DataFrame,
    *,
    initial_capital: float,
    annualisation: int,
) -> dict[str, float]:
    required = {"after_management_fee", "before_management_fee", "account_return_after_fee"}
    if not required.issubset(history.columns) or history.empty:
        raise AppLogicError("Allocation history is incomplete.")
    returns = history["account_return_after_fee"].to_numpy(dtype="float64")
    after = history["after_management_fee"].to_numpy(dtype="float64")
    before = history["before_management_fee"].to_numpy(dtype="float64")
    if len(returns) < 2 or not np.isfinite(returns).all() or np.any(returns <= -1.0):
        raise AppLogicError("Allocation metrics require at least two finite returns above -100%.")
    deviation = float(np.std(returns, ddof=1))
    wealth_with_initial = np.r_[initial_capital, after]
    drawdown = wealth_with_initial / np.maximum.accumulate(wealth_with_initial) - 1.0
    ending = float(after[-1])
    total_return = ending / initial_capital - 1.0
    annualised_return = (ending / initial_capital) ** (annualisation / len(returns)) - 1.0
    annualised_volatility = deviation * sqrt(annualisation)
    sharpe = float(np.mean(returns) / deviation * sqrt(annualisation)) if deviation > 0 else float("nan")
    return {
        "ending_value_after_fee": ending,
        "total_return_after_fee": float(total_return),
        "annualised_return_after_fee": float(annualised_return),
        "annualised_volatility_after_fee": float(annualised_volatility),
        "sharpe_ratio_after_fee": sharpe,
        "max_drawdown_after_fee": float(drawdown.min()),
        "management_fee_drag_dollars": float(before[-1] - after[-1]),
    }


def allocation_table(
    selected_funds: Sequence[str],
    allocations_percent: Mapping[str, float],
    initial_capital: float,
    names: Mapping[str, str],
) -> pd.DataFrame:
    rows = [
        {
            "fund_id": fund,
            "fund": names[fund],
            "allocation_percent": float(allocations_percent[fund]),
            "initial_dollars": initial_capital * float(allocations_percent[fund]) / 100.0,
        }
        for fund in selected_funds
    ]
    return pd.DataFrame(rows)


def rolling_sentiment_summary(
    sector_sentiment: pd.DataFrame,
    selected_sectors: Sequence[str],
    *,
    window: int = 21,
) -> pd.DataFrame:
    required = {"date", "sector", "sector_display", "finance_compound"}
    if not required.issubset(sector_sentiment.columns):
        raise AppLogicError("Sector sentiment artifact is incomplete.")
    if window <= 0:
        raise AppLogicError("Rolling display window must be positive.")
    work = sector_sentiment.loc[sector_sentiment["sector"].isin(selected_sectors), list(required)].copy(deep=True)
    work["date"] = pd.to_datetime(work["date"])
    work = work.sort_values(["sector", "date"], kind="mergesort")
    work["rolling_21"] = work.groupby("sector", sort=False)["finance_compound"].transform(
        lambda series: series.rolling(window, min_periods=1).mean()
    )
    return work.sort_values(["date", "sector"], kind="mergesort").reset_index(drop=True)


def market_sentiment_pulse(
    sector_sentiment: pd.DataFrame,
    *,
    window: int = 21,
) -> pd.DataFrame:
    required = {"date", "sector", "finance_compound"}
    if not required.issubset(sector_sentiment.columns):
        raise AppLogicError("Sector sentiment artifact is incomplete.")
    work = sector_sentiment.loc[:, list(required)].copy(deep=True)
    work["date"] = pd.to_datetime(work["date"])
    pulse = work.groupby("date", sort=True).agg(
        finance_vader_market_tone=("finance_compound", "mean"),
        sectors_with_news=("finance_compound", "count"),
    ).reset_index()
    pulse["rolling_21"] = pulse["finance_vader_market_tone"].rolling(window, min_periods=1).mean()
    return pulse


def diagnostic_value(
    diagnostics: pd.DataFrame,
    scope: str,
    entity: str,
    model: str,
    metric: str,
) -> float:
    mask = (
        diagnostics["scope"].eq(scope)
        & diagnostics["entity"].eq(entity)
        & diagnostics["model"].eq(model)
        & diagnostics["metric"].eq(metric)
    )
    matches = diagnostics.loc[mask, "value"]
    if len(matches) != 1:
        raise AppLogicError(f"Diagnostic key {(scope, entity, model, metric)} has {len(matches)} rows.")
    return float(matches.iloc[0])


def fusion_comparison_summary(comparison: pd.DataFrame) -> dict[str, object]:
    required = {
        "overlay_id", "base_fund_id", "variant", "delta_net_annualised_return",
        "delta_net_sharpe_ratio", "delta_average_turnover",
    }
    if not required.issubset(comparison.columns):
        raise AppLogicError("Fusion comparison artifact is incomplete.")
    work = comparison.copy(deep=True)
    if len(work) != 24 or work["overlay_id"].nunique() != 24 or work["base_fund_id"].nunique() != 8:
        raise AppLogicError("Fusion comparison must retain all 24 overlays across eight bases.")
    expected_variants = set(VARIANT_LABELS)
    if set(work["variant"]) != expected_variants:
        raise AppLogicError("Fusion comparison variant coverage differs from the frozen design.")
    pivot_sharpe = work.pivot(index="base_fund_id", columns="variant", values="delta_net_sharpe_ratio")
    pivot_return = work.pivot(index="base_fund_id", columns="variant", values="delta_net_annualised_return")
    pivot_turnover = work.pivot(index="base_fund_id", columns="variant", values="delta_average_turnover")
    strongest = work.loc[work["delta_net_sharpe_ratio"].idxmax()]
    weakest = work.loc[work["delta_net_sharpe_ratio"].idxmin()]
    return {
        "plain_positive_sharpe": int((pivot_sharpe["plain_vader_naive"] > 0).sum()),
        "finance_positive_sharpe": int((pivot_sharpe["finance_vader_naive"] > 0).sum()),
        "evidence_positive_sharpe": int((pivot_sharpe["evidence_aware_finance"] > 0).sum()),
        "finance_beats_plain_sharpe": int((pivot_sharpe["finance_vader_naive"] > pivot_sharpe["plain_vader_naive"]).sum()),
        "finance_beats_plain_return": int((pivot_return["finance_vader_naive"] > pivot_return["plain_vader_naive"]).sum()),
        "evidence_lower_turnover": int((pivot_turnover["evidence_aware_finance"] < pivot_turnover["finance_vader_naive"]).sum()),
        "evidence_lower_return": int((pivot_return["evidence_aware_finance"] < pivot_return["finance_vader_naive"]).sum()),
        "evidence_lower_sharpe": int((pivot_sharpe["evidence_aware_finance"] < pivot_sharpe["finance_vader_naive"]).sum()),
        "strongest_overlay": str(strongest["overlay_id"]),
        "strongest_sharpe_delta": float(strongest["delta_net_sharpe_ratio"]),
        "weakest_overlay": str(weakest["overlay_id"]),
        "weakest_sharpe_delta": float(weakest["delta_net_sharpe_ratio"]),
    }


def complete_fusion_table(
    comparison: pd.DataFrame,
    fusion_metrics: pd.DataFrame,
    base_metrics: pd.DataFrame,
) -> pd.DataFrame:
    summary = fusion_comparison_summary(comparison)
    del summary  # validation side effect is intentional; no result is selected out
    base = base_metrics.loc[:, ["fund_id", "net_annualised_return", "net_sharpe_ratio", "average_rebalance_turnover"]].rename(
        columns={
            "fund_id": "base_fund_id",
            "net_annualised_return": "base_net_annualised_return",
            "net_sharpe_ratio": "base_net_sharpe_ratio",
            "average_rebalance_turnover": "base_average_turnover",
        }
    )
    overlay = fusion_metrics.loc[:, ["overlay_id", "net_annualised_return", "net_sharpe_ratio", "average_rebalance_turnover"]].rename(
        columns={
            "net_annualised_return": "overlay_net_annualised_return",
            "net_sharpe_ratio": "overlay_net_sharpe_ratio",
            "average_rebalance_turnover": "overlay_average_turnover",
        }
    )
    table = comparison.merge(base, on="base_fund_id", how="left", validate="many_to_one")
    table = table.merge(overlay, on="overlay_id", how="left", validate="one_to_one")
    if len(table) != 24 or table.isna().any().any():
        raise AppLogicError("Complete fusion evidence did not merge to 24 fully populated rows.")
    table["variant_display"] = table["variant"].map(VARIANT_LABELS)
    table["base_fund_display"] = table.apply(lambda row: human_fund_name(row["family"], row["method"]), axis=1)
    return table


__all__ = [
    "AllocationValidation",
    "AppLogicError",
    "CRYPTO_TICKERS",
    "CalendarReconciliation",
    "MANAGEMENT_FEE_RATE",
    "METHOD_DESCRIPTIONS",
    "TRADING_COST_BPS",
    "VARIANT_LABELS",
    "allocation_performance_metrics",
    "allocation_table",
    "asset_class_exposures",
    "build_allocation_history",
    "complete_fusion_table",
    "current_holdings_date",
    "diagnostic_value",
    "equal_split_percentages",
    "fund_name_map",
    "fusion_comparison_summary",
    "growth_and_drawdown",
    "growth_of_one",
    "human_fund_name",
    "latest_target_holdings",
    "market_sentiment_pulse",
    "reconcile_return_calendars",
    "rolling_sentiment_summary",
    "validate_user_allocation",
]
