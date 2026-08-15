"""Deterministic Station 1 cleaning for the frozen Project B data contract.

The official loader caches mutable DataFrames. Every public cleaner therefore
starts from a deep copy and never writes data to disk.
"""
from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from src import data_access
from src.validation import (
    CLEAN_NEWS_COLUMNS as CONTRACT_CLEAN_NEWS_COLUMNS,
    CRYPTO_CUTOFF,
    CRYPTO_PRICE_COLUMNS as CONTRACT_CRYPTO_PRICE_COLUMNS,
    EQUITY_PRICE_COLUMNS as CONTRACT_EQUITY_PRICE_COLUMNS,
    RAW_NEWS_COLUMNS as CONTRACT_RAW_NEWS_COLUMNS,
)


EQUITY_PRICE_COLUMNS = list(CONTRACT_EQUITY_PRICE_COLUMNS)
CRYPTO_PRICE_COLUMNS = list(CONTRACT_CRYPTO_PRICE_COLUMNS)
RAW_NEWS_COLUMNS = list(CONTRACT_RAW_NEWS_COLUMNS)
CLEAN_NEWS_COLUMNS = list(CONTRACT_CLEAN_NEWS_COLUMNS)
PRICE_FLOAT_COLUMNS = ["open", "high", "low", "close", "adjClose"]


def _require_columns(frame: pd.DataFrame, required: Iterable[str], name: str) -> None:
    """Raise a deterministic error when a protected source schema is incomplete."""
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"{name} is missing required columns: {missing}")


def _naive_ns(values: pd.Series) -> pd.Series:
    """Return timestamps as timezone-naive nanosecond values."""
    parsed = pd.to_datetime(values, errors="raise")
    if isinstance(parsed.dtype, pd.DatetimeTZDtype):
        parsed = parsed.dt.tz_convert("UTC").dt.tz_localize(None)
    return parsed.astype("datetime64[ns]")


def _clean_price_panel(
    prices: pd.DataFrame,
    *,
    columns: list[str],
    name: str,
    cutoff: pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Copy, type, filter, and stably order a protected price panel."""
    _require_columns(prices, columns, name)
    clean = prices.loc[:, columns].copy(deep=True)
    clean["date"] = _naive_ns(clean["date"])
    clean["ticker"] = clean["ticker"].astype("string")
    if "sector" in clean:
        clean["sector"] = clean["sector"].astype("string")
    for column in PRICE_FLOAT_COLUMNS:
        clean[column] = pd.to_numeric(clean[column], errors="raise").astype("float64")
    clean["volume"] = pd.to_numeric(clean["volume"], errors="raise").astype("int64")
    if cutoff is not None:
        clean = clean.loc[clean["date"].le(cutoff)].copy()
    return clean.sort_values(["date", "ticker"], kind="mergesort").reset_index(drop=True)


def clean_equity_prices(prices: pd.DataFrame) -> pd.DataFrame:
    """Return the canonical clean equity-price panel without mutating ``prices``."""
    return _clean_price_panel(
        prices,
        columns=EQUITY_PRICE_COLUMNS,
        name="equity prices",
    )


def clean_crypto_prices(prices: pd.DataFrame) -> pd.DataFrame:
    """Return crypto prices through 2023-12-31 on their native daily calendar."""
    return _clean_price_panel(
        prices,
        columns=CRYPTO_PRICE_COLUMNS,
        name="crypto prices",
        cutoff=CRYPTO_CUTOFF,
    )


def clean_news_headlines(headlines: pd.DataFrame) -> pd.DataFrame:
    """Preserve exact text and deterministically remove duplicate identities.

    Identity is ``ticker + normalised UTC source timestamp + exact title``.
    The earliest zero-based source row is retained. The loaded ``date`` field is
    preserved for auditability; mapping uses the separately derived UTC date.
    """
    _require_columns(headlines, RAW_NEWS_COLUMNS, "news headlines")
    clean = headlines.loc[:, RAW_NEWS_COLUMNS].copy(deep=True)
    clean["source_row_order"] = np.arange(len(clean), dtype="int64")
    clean["source_timestamp"] = pd.to_datetime(
        clean["date"], errors="raise", utc=True
    ).astype("datetime64[ns, UTC]")
    clean["source_date_utc"] = (
        clean["source_timestamp"]
        .dt.tz_convert("UTC")
        .dt.tz_localize(None)
        .dt.normalize()
        .astype("datetime64[ns]")
    )
    for column in ["ticker", "sector", "title", "url", "publisher"]:
        clean[column] = clean[column].astype("string")

    clean = clean.sort_values("source_row_order", kind="mergesort")
    clean = clean.drop_duplicates(
        ["ticker", "source_timestamp", "title"], keep="first"
    )
    clean = clean.loc[:, CLEAN_NEWS_COLUMNS]
    return clean.sort_values(
        ["source_timestamp", "source_row_order", "ticker"], kind="mergesort"
    ).reset_index(drop=True)


def load_clean_equities() -> pd.DataFrame:
    """Load through the protected helper and return a detached clean copy."""
    return clean_equity_prices(data_access.load_equity_prices())


def load_clean_crypto() -> pd.DataFrame:
    """Load through the protected helper and return a detached clean copy."""
    return clean_crypto_prices(data_access.load_crypto_prices())


def load_clean_news() -> pd.DataFrame:
    """Load through the protected helper and return canonical cleaned headlines."""
    return clean_news_headlines(data_access.load_news_headlines())


__all__ = [
    "CLEAN_NEWS_COLUMNS",
    "CRYPTO_PRICE_COLUMNS",
    "EQUITY_PRICE_COLUMNS",
    "RAW_NEWS_COLUMNS",
    "clean_crypto_prices",
    "clean_equity_prices",
    "clean_news_headlines",
    "load_clean_crypto",
    "load_clean_equities",
    "load_clean_news",
]
