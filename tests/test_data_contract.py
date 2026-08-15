"""Real-data regression tests for the accepted Project B input contract."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src import data_access
from src.etl import clean_crypto_prices, clean_equity_prices, clean_news_headlines
from src.features import (
    align_crypto_returns_to_equity_calendar,
    build_combined_return_matrix,
    build_complete_headline_panel,
    build_equity_returns,
    build_mapped_headline_table,
    build_native_crypto_returns,
    equity_trading_calendar,
    map_headlines_to_equity_calendar,
)
from src.validation import (
    ALIGNED_CRYPTO_COLUMNS,
    BENCHMARKS,
    CLEAN_NEWS_COLUMNS,
    COMBINED_ASSETS,
    COVERAGE_COLUMNS,
    CRYPTO_PRICE_COLUMNS,
    CRYPTO_RETURN_COLUMNS,
    CRYPTO_TICKERS,
    EQUITY_PRICE_COLUMNS,
    EQUITY_RETURN_COLUMNS,
    EQUITY_TICKERS,
    MAPPING_COLUMNS,
    SECTOR_DISPLAY_LABELS,
    SECTOR_DISPLAY_ORDER,
    SIX_UNMAPPED,
    SOURCE_SECTORS,
    find_extreme_observations,
    validate_data_foundation,
)


@pytest.fixture(scope="session")
def foundation() -> dict[str, object]:
    raw_equity = data_access.load_equity_prices()
    raw_crypto = data_access.load_crypto_prices()
    raw_news = data_access.load_news_headlines()
    equity = clean_equity_prices(raw_equity)
    crypto = clean_crypto_prices(raw_crypto)
    news = clean_news_headlines(raw_news)
    equity_returns = build_equity_returns(equity)
    crypto_returns = build_native_crypto_returns(crypto)
    calendar = equity_trading_calendar(equity)
    aligned_crypto = align_crypto_returns_to_equity_calendar(crypto_returns, calendar)
    combined_returns = build_combined_return_matrix(equity_returns, aligned_crypto)
    full_mapping = map_headlines_to_equity_calendar(news, calendar)
    mapped_headlines = build_mapped_headline_table(full_mapping)
    coverage_panel = build_complete_headline_panel(mapped_headlines, equity)
    return locals()


def test_clean_price_contract(foundation: dict[str, object]) -> None:
    raw_equity = foundation["raw_equity"]
    raw_crypto = foundation["raw_crypto"]
    equity = foundation["equity"]
    crypto = foundation["crypto"]
    assert isinstance(raw_equity, pd.DataFrame)
    assert isinstance(raw_crypto, pd.DataFrame)
    assert isinstance(equity, pd.DataFrame)
    assert isinstance(crypto, pd.DataFrame)

    assert tuple(equity.columns) == EQUITY_PRICE_COLUMNS
    assert tuple(crypto.columns) == CRYPTO_PRICE_COLUMNS
    assert len(raw_equity) == len(equity) == 50_300
    assert len(raw_crypto) == 14_620
    assert len(crypto) == 14_610
    assert int(pd.to_datetime(raw_crypto["date"]).eq(pd.Timestamp("2024-01-01")).sum()) == 10
    assert not crypto["date"].gt(pd.Timestamp("2023-12-31")).any()
    assert (equity["date"].min(), equity["date"].max()) == (
        pd.Timestamp("2020-01-02"),
        pd.Timestamp("2023-12-29"),
    )
    assert (crypto["date"].min(), crypto["date"].max()) == (
        pd.Timestamp("2020-01-01"),
        pd.Timestamp("2023-12-31"),
    )
    assert equity["date"].nunique() == 1_006
    assert crypto["date"].nunique() == 1_461
    assert tuple(sorted(equity["ticker"].unique())) == EQUITY_TICKERS
    assert tuple(sorted(crypto["ticker"].unique())) == CRYPTO_TICKERS
    assert tuple(sorted(equity["sector"].unique())) == SOURCE_SECTORS
    assert not equity.duplicated(["ticker", "date"]).any()
    assert not crypto.duplicated(["ticker", "date"]).any()
    assert not equity.isna().any().any()
    assert not crypto.isna().any().any()
    assert str(equity["date"].dtype) == str(crypto["date"].dtype) == "datetime64[ns]"
    assert str(equity["ticker"].dtype) == str(crypto["ticker"].dtype) == "string"
    assert str(equity["sector"].dtype) == "string"
    for column in ["open", "high", "low", "close", "adjClose"]:
        assert str(equity[column].dtype) == str(crypto[column].dtype) == "float64"
    assert str(equity["volume"].dtype) == str(crypto["volume"].dtype) == "int64"


def test_news_identity_schema_and_preservation(foundation: dict[str, object]) -> None:
    raw = foundation["raw_news"]
    news = foundation["news"]
    assert isinstance(raw, pd.DataFrame)
    assert isinstance(news, pd.DataFrame)
    assert tuple(news.columns) == CLEAN_NEWS_COLUMNS
    assert len(raw) == 149_683
    assert len(news) == 146_836
    assert len(raw) - len(news) == 2_847
    assert tuple(sorted(news["ticker"].unique())) == EQUITY_TICKERS
    assert tuple(sorted(news["sector"].unique())) == SOURCE_SECTORS
    assert not news.duplicated(["ticker", "source_timestamp", "title"]).any()
    assert not news[["ticker", "source_timestamp", "title"]].isna().any().any()
    assert str(news["date"].dtype) == "datetime64[us, UTC]"
    assert str(news["source_timestamp"].dtype) == "datetime64[ns, UTC]"
    assert str(news["source_date_utc"].dtype) == "datetime64[ns]"
    assert str(news["source_row_order"].dtype) == "int64"
    for row in news.itertuples():
        assert row.title == raw.iloc[row.source_row_order]["title"]
    assert int(news["publisher"].isna().sum()) == 137_447


def test_sector_display_contract() -> None:
    assert SECTOR_DISPLAY_ORDER == (
        "Tech", "Financials", "Energy", "Consumer", "Industrials", "Healthcare",
        "Comm", "Materials", "Utilities", "RealEstate",
    )
    assert SECTOR_DISPLAY_LABELS["Comm"] == "Comm/Telecom"
    assert SECTOR_DISPLAY_LABELS["RealEstate"] == "Real Estate"
    assert set(SECTOR_DISPLAY_LABELS) == set(SOURCE_SECTORS)


def test_native_and_aligned_return_contract(foundation: dict[str, object]) -> None:
    equity_returns = foundation["equity_returns"]
    crypto_returns = foundation["crypto_returns"]
    aligned = foundation["aligned_crypto"]
    assert isinstance(equity_returns, pd.DataFrame)
    assert isinstance(crypto_returns, pd.DataFrame)
    assert isinstance(aligned, pd.DataFrame)
    assert tuple(equity_returns.columns) == EQUITY_RETURN_COLUMNS
    assert tuple(crypto_returns.columns) == CRYPTO_RETURN_COLUMNS
    assert tuple(aligned.columns) == ALIGNED_CRYPTO_COLUMNS
    assert len(equity_returns) == 50_300
    assert len(crypto_returns) == 14_610
    assert len(aligned) == 10_060
    assert int(equity_returns["return"].isna().sum()) == 50
    assert int(crypto_returns["return"].isna().sum()) == 10
    assert not aligned["return"].isna().any()
    for returns in (equity_returns, crypto_returns):
        ordered = returns.sort_values(["ticker", "date"], kind="mergesort")
        first = ordered.groupby("ticker", sort=False).head(1)
        rest = ordered.drop(index=first.index)
        assert first["return"].isna().all()
        assert rest["return"].notna().all()
    assert not aligned.duplicated(["ticker", "date"]).any()


def test_combined_return_matrix_contract(foundation: dict[str, object]) -> None:
    combined = foundation["combined_returns"]
    assert isinstance(combined, pd.DataFrame)
    assert combined.shape == (1_006, 60)
    assert combined.index.name == "date"
    assert tuple(combined.columns) == COMBINED_ASSETS
    assert combined.index.min() == pd.Timestamp("2020-01-02")
    assert combined.index.max() == pd.Timestamp("2023-12-29")
    assert combined.index.is_monotonic_increasing and combined.index.is_unique
    assert int(combined.isna().sum().sum()) == 50
    assert combined.loc[:, list(CRYPTO_TICKERS)].notna().all().all()


def test_mapping_six_records_and_coverage(foundation: dict[str, object]) -> None:
    full_mapping = foundation["full_mapping"]
    mapped = foundation["mapped_headlines"]
    panel = foundation["coverage_panel"]
    assert isinstance(full_mapping, pd.DataFrame)
    assert isinstance(mapped, pd.DataFrame)
    assert isinstance(panel, pd.DataFrame)
    assert tuple(full_mapping.columns) == CLEAN_NEWS_COLUMNS + MAPPING_COLUMNS
    assert tuple(mapped.columns) == CLEAN_NEWS_COLUMNS + MAPPING_COLUMNS
    assert tuple(panel.columns) == COVERAGE_COLUMNS
    assert len(full_mapping) == 146_836
    assert len(mapped) == 146_830
    unmapped = full_mapping.loc[
        full_mapping["map_status"].eq("unmapped_end_of_sample")
    ].sort_values("source_row_order")
    measured = tuple(
        (int(row.source_row_order), pd.Timestamp(row.source_date_utc))
        for row in unmapped.itertuples()
    )
    assert measured == SIX_UNMAPPED
    assert unmapped["ticker"].eq("AMD").all()
    assert unmapped["sector"].eq("Tech").all()
    assert unmapped["mapped_trade_date"].isna().all()
    assert len(full_mapping) == len(mapped) + len(unmapped)
    assert mapped["mapped_trade_date"].isin(foundation["calendar"]).all()
    assert mapped["mapped_trade_date"].ge(mapped["source_date_utc"]).all()
    assert mapped["mapping_day_distance"].between(0, 3).all()
    assert len(panel) == 50_300
    assert not panel.duplicated(["ticker", "date"]).any()
    assert int(panel["headline_count"].eq(0).sum()) == 12_338
    assert int(panel["headline_count"].sum()) == len(mapped)
    assert panel["has_news"].equals(panel["headline_count"].gt(0))
    assert str(panel["date"].dtype) == "datetime64[ns]"
    assert str(panel["ticker"].dtype) == str(panel["sector"].dtype) == "string"
    assert str(panel["headline_count"].dtype) == "int64"
    assert str(panel["has_news"].dtype) == "bool"
    assert not any("sentiment" in column.lower() for column in panel.columns)


def test_extreme_observations_are_retained(foundation: dict[str, object]) -> None:
    equity = foundation["equity"]
    crypto = foundation["crypto"]
    assert isinstance(equity, pd.DataFrame)
    assert isinstance(crypto, pd.DataFrame)
    equity_extremes = find_extreme_observations(equity)
    crypto_extremes = find_extreme_observations(crypto)
    assert len(equity_extremes) == 4
    assert len(crypto_extremes) == 65
    for extremes in (equity_extremes, crypto_extremes):
        assert not extremes.duplicated(["ticker", "date"]).any()
        assert np.isfinite(extremes["adjClose"]).all()
        assert extremes["adjClose"].gt(0).all()
        assert np.isfinite(extremes["previous_adjClose"]).all()
        assert extremes["previous_adjClose"].gt(0).all()
        assert np.isfinite(extremes["calculated_return"]).all()
        assert extremes["volume"].ge(0).all()
        assert extremes["previous_volume"].ge(0).all()


def test_machine_readable_validation_has_no_blocks(foundation: dict[str, object]) -> None:
    project_root = Path(__file__).resolve().parents[1]
    report = validate_data_foundation(
        project_root=project_root,
        loader_path=Path(data_access.__file__),
        raw_equity=foundation["raw_equity"],
        raw_crypto=foundation["raw_crypto"],
        raw_news=foundation["raw_news"],
        equity=foundation["equity"],
        crypto=foundation["crypto"],
        news=foundation["news"],
        equity_returns=foundation["equity_returns"],
        crypto_returns=foundation["crypto_returns"],
        aligned_crypto=foundation["aligned_crypto"],
        combined_returns=foundation["combined_returns"],
        full_mapping=foundation["full_mapping"],
        mapped_headlines=foundation["mapped_headlines"],
        coverage_panel=foundation["coverage_panel"],
    )
    payload = report.to_dict()
    assert report.ok
    assert payload["status"] == "PASS"
    assert payload["summary"]["BLOCK"] == 0
    assert payload["summary"]["WARN"] >= 1
    assert BENCHMARKS["clean_news_rows"] == 146_836
