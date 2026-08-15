"""Synthetic edge-case tests for deterministic Stage 4A behaviour."""
from __future__ import annotations

import pandas as pd

from src.etl import clean_crypto_prices, clean_equity_prices, clean_news_headlines
from src.features import (
    align_crypto_returns_to_equity_calendar,
    build_combined_return_matrix,
    build_complete_headline_panel,
    build_mapped_headline_table,
    build_native_crypto_returns,
    daily_returns,
    map_headlines_to_equity_calendar,
)


def _price_rows(tickers: tuple[str, ...], dates: list[str], *, sector: bool) -> pd.DataFrame:
    rows = []
    for ticker_number, ticker in enumerate(tickers, start=1):
        for date_number, date in enumerate(dates, start=1):
            price = float(100 * ticker_number + date_number)
            row = {
                "ticker": ticker,
                "date": pd.Timestamp(date),
                "open": price,
                "high": price + 1.0,
                "low": price - 1.0,
                "close": price,
                "adjClose": price,
                "volume": 1000 * ticker_number + date_number,
            }
            if sector:
                row["sector"] = "Tech" if ticker_number == 1 else "Financials"
            rows.append(row)
    return pd.DataFrame(rows)


def _mapping_news() -> pd.DataFrame:
    raw = pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    "2023-06-30 12:00:00+00:00",
                    "2023-07-01 08:00:00+00:00",
                    "2023-07-04 09:00:00+00:00",
                    "2023-07-06 10:00:00+00:00",
                ],
                utc=True,
            ),
            "ticker": ["AAA"] * 4,
            "sector": ["Tech"] * 4,
            "title": ["Same day", "Weekend", "Weekday holiday", "After sample"],
            "url": ["u0", "u1", "u2", "u3"],
            "publisher": ["p0", "p1", "p2", "p3"],
        }
    )
    return clean_news_headlines(raw)


def test_crypto_return_is_native_before_equity_alignment() -> None:
    prices = pd.DataFrame(
        {
            "date": pd.to_datetime(["2023-01-06", "2023-01-08", "2023-01-09"]),
            "ticker": ["BTC-USD"] * 3,
            "adjClose": [100.0, 110.0, 121.0],
        }
    )
    native = build_native_crypto_returns(prices)
    aligned = align_crypto_returns_to_equity_calendar(
        native, pd.to_datetime(["2023-01-06", "2023-01-09"])
    )
    monday = aligned.loc[aligned["date"].eq(pd.Timestamp("2023-01-09")), "return"].item()
    assert monday == 121.0 / 110.0 - 1.0
    assert monday != 121.0 / 100.0 - 1.0


def test_same_day_weekend_holiday_endpoint_and_never_backward_mapping() -> None:
    calendar = pd.to_datetime(["2023-06-30", "2023-07-03", "2023-07-05"])
    mapping = map_headlines_to_equity_calendar(_mapping_news(), calendar)
    by_title = mapping.set_index("title")
    assert by_title.loc["Same day", "map_status"] == "same_day"
    assert by_title.loc["Same day", "mapped_trade_date"] == pd.Timestamp("2023-06-30")
    assert by_title.loc["Weekend", "map_status"] == "forward"
    assert by_title.loc["Weekend", "mapped_trade_date"] == pd.Timestamp("2023-07-03")
    assert by_title.loc["Weekend", "mapping_day_distance"] == 2
    assert by_title.loc["Weekday holiday", "map_status"] == "forward"
    assert by_title.loc["Weekday holiday", "mapped_trade_date"] == pd.Timestamp("2023-07-05")
    assert by_title.loc["Weekday holiday", "mapping_day_distance"] == 1
    assert by_title.loc["After sample", "map_status"] == "unmapped_end_of_sample"
    assert pd.isna(by_title.loc["After sample", "mapped_trade_date"])
    valid = mapping["mapped_trade_date"].notna()
    assert mapping.loc[valid, "mapped_trade_date"].ge(
        mapping.loc[valid, "source_date_utc"]
    ).all()


def test_exact_title_identity_earliest_row_and_text_preservation() -> None:
    timestamp = pd.Timestamp("2023-05-01 12:30:00", tz="UTC")
    titles = [
        "Profit Beats!  ",
        "Profit Beats!  ",
        "profit Beats!  ",
        "Profit Beats?  ",
        " Profit Beats!  ",
    ]
    raw = pd.DataFrame(
        {
            "date": [timestamp] * len(titles),
            "ticker": ["AAA"] * len(titles),
            "sector": ["Tech"] * len(titles),
            "title": titles,
            "url": [f"u{i}" for i in range(len(titles))],
            "publisher": [None] * len(titles),
        }
    )
    clean = clean_news_headlines(raw)
    assert len(clean) == 4
    retained = clean.set_index("title")["source_row_order"].to_dict()
    assert retained["Profit Beats!  "] == 0
    assert set(clean["title"]) == set(titles)
    assert "profit Beats!  " in set(clean["title"])
    assert "Profit Beats?  " in set(clean["title"])
    assert " Profit Beats!  " in set(clean["title"])


def test_no_news_is_explicit_without_a_neutral_score() -> None:
    equity = _price_rows(
        ("AAA", "BBB"), ["2023-06-30", "2023-07-03", "2023-07-05"], sector=True
    )
    mapped = build_mapped_headline_table(
        map_headlines_to_equity_calendar(
            _mapping_news(), pd.to_datetime(["2023-06-30", "2023-07-03", "2023-07-05"])
        )
    )
    panel = build_complete_headline_panel(
        mapped, equity, ticker_order=("AAA", "BBB")
    )
    assert len(panel) == 6
    no_news = panel.loc[~panel["has_news"]]
    assert len(no_news) == 3
    assert no_news["headline_count"].eq(0).all()
    assert not any(
        token in column.lower() for column in panel.columns for token in ("sentiment", "score")
    )


def test_deterministic_order_and_rerun_equality() -> None:
    raw_equity = _price_rows(
        ("BBB", "AAA"), ["2023-07-05", "2023-06-30", "2023-07-03"], sector=True
    ).sample(frac=1.0, random_state=7)
    first = clean_equity_prices(raw_equity)
    second = clean_equity_prices(raw_equity)
    pd.testing.assert_frame_equal(first, second, check_dtype=True)
    expected_keys = first[["date", "ticker"]].sort_values(
        ["date", "ticker"], kind="mergesort"
    ).reset_index(drop=True)
    pd.testing.assert_frame_equal(first[["date", "ticker"]], expected_keys)
    first_returns = daily_returns(first)
    second_returns = daily_returns(second)
    pd.testing.assert_frame_equal(first_returns, second_returns, check_dtype=True)

    crypto = pd.DataFrame(
        {
            "date": pd.to_datetime(["2023-06-30", "2023-07-03"] * 2),
            "ticker": ["X", "X", "Y", "Y"],
            "adjClose": [10.0, 11.0, 20.0, 18.0],
        }
    )
    crypto_returns = build_native_crypto_returns(crypto)
    aligned = align_crypto_returns_to_equity_calendar(
        crypto_returns, pd.to_datetime(["2023-06-30", "2023-07-03"])
    )
    matrix = build_combined_return_matrix(
        first_returns,
        aligned,
        equity_order=("AAA", "BBB"),
        crypto_order=("X", "Y"),
    )
    assert tuple(matrix.columns) == ("AAA", "BBB", "X", "Y")
    assert matrix.index.is_monotonic_increasing


def test_cleaners_and_features_do_not_mutate_source_frames() -> None:
    raw_equity = _price_rows(("AAA",), ["2023-01-02", "2023-01-03"], sector=True)
    raw_crypto = _price_rows(
        ("BTC-USD",), ["2023-12-31", "2024-01-01"], sector=False
    )
    raw_news = pd.DataFrame(
        {
            "date": pd.to_datetime(["2023-01-02 12:00:00+00:00"]),
            "ticker": ["AAA"],
            "sector": ["Tech"],
            "title": ["  CASE & punctuation!  "],
            "url": ["u"],
            "publisher": [None],
        }
    )
    snapshots = [frame.copy(deep=True) for frame in (raw_equity, raw_crypto, raw_news)]
    equity = clean_equity_prices(raw_equity)
    clean_crypto_prices(raw_crypto)
    clean_news_headlines(raw_news)
    daily_returns(equity)
    for actual, expected in zip((raw_equity, raw_crypto, raw_news), snapshots, strict=True):
        pd.testing.assert_frame_equal(actual, expected, check_dtype=True)
