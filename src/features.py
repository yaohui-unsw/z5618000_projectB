"""Pure, deterministic Station 2 features for the frozen input contract.

Sentiment scoring and tradable-signal lagging are deliberately absent. This
module calculates native-calendar returns and assembles auditable headline
coverage only.
"""
from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np
import pandas as pd

from src.validation import (
    ALIGNED_CRYPTO_COLUMNS,
    CLEAN_NEWS_COLUMNS,
    COMBINED_ASSETS,
    COVERAGE_COLUMNS,
    CRYPTO_RETURN_COLUMNS,
    CRYPTO_TICKERS,
    EQUITY_RETURN_COLUMNS,
    EQUITY_TICKERS,
    MAPPING_COLUMNS,
)


def _require_columns(frame: pd.DataFrame, required: Iterable[str], name: str) -> None:
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"{name} is missing required columns: {missing}")


def _normalise_dates(values: pd.Series | pd.Index) -> pd.Series:
    parsed = pd.Series(pd.to_datetime(values, errors="raise"), copy=False)
    if isinstance(parsed.dtype, pd.DatetimeTZDtype):
        parsed = parsed.dt.tz_convert("UTC").dt.tz_localize(None)
    return parsed.astype("datetime64[ns]")


def equity_trading_calendar(equity_prices: pd.DataFrame) -> pd.DatetimeIndex:
    """Return the unique observed equity dates in ascending order."""
    _require_columns(equity_prices, ["date"], "equity prices")
    dates = _normalise_dates(equity_prices["date"])
    return pd.DatetimeIndex(dates.drop_duplicates().sort_values(), name="date")


def daily_returns(prices: pd.DataFrame, price_col: str = "adjClose") -> pd.DataFrame:
    """Calculate simple decimal returns per ticker on the supplied native rows.

    No fill is performed. Calculation temporarily sorts by ticker and date;
    output is returned to the canonical date-then-ticker order.
    """
    _require_columns(prices, ["date", "ticker", price_col], "prices")
    work = prices.copy(deep=True)
    work["date"] = _normalise_dates(work["date"]).to_numpy()
    work = work.sort_values(["ticker", "date"], kind="mergesort").reset_index(
        drop=True
    )
    values = pd.to_numeric(work[price_col], errors="raise").astype("float64")
    work[price_col] = values
    previous = work.groupby("ticker", sort=False, observed=True)[price_col].shift(1)
    work["return"] = values.div(previous).sub(1.0).astype("float64")
    columns = ["date", "ticker"]
    if "sector" in work.columns:
        columns.append("sector")
    columns.extend([price_col, "return"])
    return work.loc[:, columns].sort_values(
        ["date", "ticker"], kind="mergesort"
    ).reset_index(drop=True)


def build_equity_returns(equity_prices: pd.DataFrame) -> pd.DataFrame:
    """Return the contracted long equity-return panel."""
    result = daily_returns(equity_prices, "adjClose")
    return result.loc[:, list(EQUITY_RETURN_COLUMNS)]


def build_native_crypto_returns(crypto_prices: pd.DataFrame) -> pd.DataFrame:
    """Calculate crypto returns before any equity-calendar restriction."""
    result = daily_returns(crypto_prices, "adjClose")
    return result.loc[:, list(CRYPTO_RETURN_COLUMNS)]


def align_crypto_returns_to_equity_calendar(
    native_crypto_returns: pd.DataFrame,
    equity_calendar: Sequence[pd.Timestamp] | pd.DatetimeIndex,
) -> pd.DataFrame:
    """Select already-calculated native crypto returns onto equity dates."""
    _require_columns(
        native_crypto_returns, CRYPTO_RETURN_COLUMNS, "native crypto returns"
    )
    aligned = native_crypto_returns.copy(deep=True)
    aligned["date"] = _normalise_dates(aligned["date"]).to_numpy()
    calendar = pd.DatetimeIndex(pd.to_datetime(equity_calendar)).sort_values().unique()
    aligned = aligned.loc[aligned["date"].isin(calendar), list(ALIGNED_CRYPTO_COLUMNS)]
    return aligned.sort_values(["date", "ticker"], kind="mergesort").reset_index(
        drop=True
    )


def build_combined_return_matrix(
    equity_returns: pd.DataFrame,
    aligned_crypto_returns: pd.DataFrame,
    *,
    equity_order: Sequence[str] = EQUITY_TICKERS,
    crypto_order: Sequence[str] = CRYPTO_TICKERS,
) -> pd.DataFrame:
    """Build the equity-calendar matrix in explicit equity-then-crypto order."""
    _require_columns(equity_returns, ["date", "ticker", "return"], "equity returns")
    _require_columns(
        aligned_crypto_returns,
        ["date", "ticker", "return"],
        "aligned crypto returns",
    )
    equity_wide = equity_returns.pivot(index="date", columns="ticker", values="return")
    crypto_wide = aligned_crypto_returns.pivot(
        index="date", columns="ticker", values="return"
    )
    requested_equity = list(equity_order)
    requested_crypto = list(crypto_order)
    missing_equity = sorted(set(requested_equity).difference(equity_wide.columns))
    missing_crypto = sorted(set(requested_crypto).difference(crypto_wide.columns))
    if missing_equity or missing_crypto:
        raise ValueError(
            "Cannot build combined matrix; missing ordered assets: "
            f"equity={missing_equity}, crypto={missing_crypto}"
        )
    combined = pd.concat(
        [equity_wide.loc[:, requested_equity], crypto_wide.loc[:, requested_crypto]],
        axis=1,
    ).sort_index(kind="mergesort")
    combined.index = pd.DatetimeIndex(combined.index, name="date")
    combined.columns = requested_equity + requested_crypto
    return combined.astype("float64")


def map_headlines_to_equity_calendar(
    cleaned_headlines: pd.DataFrame,
    equity_calendar: Sequence[pd.Timestamp] | pd.DatetimeIndex,
) -> pd.DataFrame:
    """Map each headline to the same or next observed equity trading date."""
    _require_columns(cleaned_headlines, CLEAN_NEWS_COLUMNS, "cleaned headlines")
    mapped = cleaned_headlines.loc[:, list(CLEAN_NEWS_COLUMNS)].copy(deep=True)
    mapped["source_date_utc"] = _normalise_dates(mapped["source_date_utc"]).to_numpy()
    calendar = pd.DatetimeIndex(pd.to_datetime(equity_calendar)).sort_values().unique()
    if calendar.empty:
        raise ValueError("equity calendar must contain at least one observed date")
    if calendar.has_duplicates:
        raise ValueError("equity calendar must be unique")

    source_values = mapped["source_date_utc"].to_numpy(dtype="datetime64[ns]")
    positions = calendar.searchsorted(source_values, side="left")
    valid = positions < len(calendar)
    mapped_values = np.full(len(mapped), np.datetime64("NaT"), dtype="datetime64[ns]")
    mapped_values[valid] = calendar.to_numpy(dtype="datetime64[ns]")[positions[valid]]
    mapped["mapped_trade_date"] = pd.Series(mapped_values, index=mapped.index)

    status = np.full(len(mapped), "unmapped_end_of_sample", dtype=object)
    same_day = valid & (mapped_values == source_values)
    status[valid] = "forward"
    status[same_day] = "same_day"
    mapped["map_status"] = pd.Series(status, index=mapped.index, dtype="string")
    mapped["mapping_day_distance"] = (
        mapped["mapped_trade_date"].sub(mapped["source_date_utc"]).dt.days.astype("Int64")
    )
    mapped = mapped.loc[:, list(CLEAN_NEWS_COLUMNS + MAPPING_COLUMNS)]
    return mapped.sort_values(
        [
            "mapped_trade_date",
            "ticker",
            "source_timestamp",
            "source_row_order",
        ],
        kind="mergesort",
        na_position="last",
    ).reset_index(drop=True)


def build_mapped_headline_table(full_mapping: pd.DataFrame) -> pd.DataFrame:
    """Select the tradable same-day/forward mapping records."""
    _require_columns(
        full_mapping, CLEAN_NEWS_COLUMNS + MAPPING_COLUMNS, "full headline mapping"
    )
    selected = full_mapping.loc[
        full_mapping["map_status"].isin(["same_day", "forward"])
    ].copy(deep=True)
    selected["mapping_day_distance"] = selected["mapping_day_distance"].astype("int64")
    return selected.loc[:, list(CLEAN_NEWS_COLUMNS + MAPPING_COLUMNS)].sort_values(
        [
            "mapped_trade_date",
            "ticker",
            "source_timestamp",
            "source_row_order",
        ],
        kind="mergesort",
    ).reset_index(drop=True)


def build_complete_headline_panel(
    mapped_headlines: pd.DataFrame,
    equity_prices: pd.DataFrame,
    *,
    ticker_order: Sequence[str] = EQUITY_TICKERS,
) -> pd.DataFrame:
    """Create the complete ticker-trading-day coverage grid without scores."""
    _require_columns(
        mapped_headlines, ["mapped_trade_date", "ticker"], "mapped headlines"
    )
    _require_columns(equity_prices, ["date", "ticker", "sector"], "equity prices")
    calendar = equity_trading_calendar(equity_prices)
    tickers = list(ticker_order)
    sector_pairs = equity_prices.loc[:, ["ticker", "sector"]].drop_duplicates()
    if sector_pairs.duplicated("ticker").any():
        raise ValueError("equity ticker maps to more than one source sector")
    sector_map = sector_pairs.set_index("ticker")["sector"]
    missing_tickers = sorted(set(tickers).difference(sector_map.index))
    if missing_tickers:
        raise ValueError(f"coverage grid has no sector for tickers: {missing_tickers}")

    grid = pd.MultiIndex.from_product(
        [calendar, tickers], names=["date", "ticker"]
    ).to_frame(index=False)
    grid["ticker"] = grid["ticker"].astype("string")
    grid["sector"] = grid["ticker"].map(sector_map).astype("string")
    counts = (
        mapped_headlines.groupby(
            ["mapped_trade_date", "ticker"], sort=False, observed=True
        )
        .size()
        .rename("headline_count")
        .reset_index()
        .rename(columns={"mapped_trade_date": "date"})
    )
    panel = grid.merge(counts, on=["date", "ticker"], how="left", validate="one_to_one")
    panel["headline_count"] = panel["headline_count"].fillna(0).astype("int64")
    panel["has_news"] = panel["headline_count"].gt(0).astype("bool")
    return panel.loc[:, list(COVERAGE_COLUMNS)].sort_values(
        ["date", "ticker"], kind="mergesort"
    ).reset_index(drop=True)


def assemble_headline_panel(
    headlines: pd.DataFrame,
    equity_prices: pd.DataFrame,
    *,
    ticker_order: Sequence[str] = EQUITY_TICKERS,
) -> pd.DataFrame:
    """Map cleaned headlines and return the complete no-score coverage panel."""
    mapping = map_headlines_to_equity_calendar(
        headlines, equity_trading_calendar(equity_prices)
    )
    mapped = build_mapped_headline_table(mapping)
    return build_complete_headline_panel(
        mapped, equity_prices, ticker_order=ticker_order
    )


__all__ = [
    "align_crypto_returns_to_equity_calendar",
    "assemble_headline_panel",
    "build_combined_return_matrix",
    "build_complete_headline_panel",
    "build_equity_returns",
    "build_mapped_headline_table",
    "build_native_crypto_returns",
    "daily_returns",
    "equity_trading_calendar",
    "map_headlines_to_equity_calendar",
]
