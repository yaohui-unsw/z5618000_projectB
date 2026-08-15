"""Independent synthetic tests for the frozen sentiment design."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.sentiment import (
    FINANCE_LEXICON,
    MINIMUM_HISTORY,
    REJECTED_TERMS,
    TICKER_SENTIMENT_COLUMNS,
    TOKEN_PATTERN_TEXT,
    build_sector_sentiment_index,
    build_ticker_sentiment_daily,
    create_vader_analyzers,
    matched_tokens,
    score_headlines,
)


def _mapped(titles: list[str]) -> pd.DataFrame:
    dates = pd.date_range("2020-01-02", periods=len(titles), freq="D")
    return pd.DataFrame(
        {
            "date": dates.tz_localize("UTC"),
            "ticker": ["AAA"] * len(titles),
            "sector": ["Tech"] * len(titles),
            "title": titles,
            "url": ["u"] * len(titles),
            "publisher": [pd.NA] * len(titles),
            "source_row_order": range(len(titles)),
            "source_timestamp": dates.tz_localize("UTC"),
            "source_date_utc": dates,
            "map_status": ["same_day"] * len(titles),
            "mapped_trade_date": dates,
            "mapping_day_distance": [0] * len(titles),
        }
    )


def _coverage(dates: pd.DatetimeIndex, tickers: tuple[str, ...], counts: dict[tuple[pd.Timestamp, str], int]) -> pd.DataFrame:
    rows = []
    for date in dates:
        for ticker in tickers:
            count = counts.get((pd.Timestamp(date), ticker), 0)
            rows.append(
                {
                    "date": pd.Timestamp(date),
                    "ticker": ticker,
                    "sector": "Tech",
                    "headline_count": count,
                    "has_news": bool(count),
                }
            )
    return pd.DataFrame(rows)


def _scored_row(date: str | pd.Timestamp, ticker: str, row_id: int, finance: float, *, plain: float | None = None, covered: bool = True, custom: bool = False) -> dict[str, object]:
    timestamp = pd.Timestamp(date)
    return {
        "source_row_order": row_id,
        "source_timestamp": timestamp.tz_localize("UTC") if timestamp.tzinfo is None else timestamp,
        "source_date_utc": timestamp.normalize(),
        "mapped_trade_date": timestamp.normalize().tz_localize(None),
        "ticker": ticker,
        "sector": "Tech",
        "title": f"Headline {row_id}",
        "plain_compound": finance if plain is None else plain,
        "finance_compound": finance,
        "covered_nonzero": covered,
        "custom_term_hit": custom,
    }


def test_plain_vader_isolation_exact_lexicon_and_zero_overrides():
    plain, finance = create_vader_analyzers()
    snapshot = dict(plain.lexicon)
    _, second_finance = create_vader_analyzers()
    assert plain.lexicon == snapshot
    assert len(FINANCE_LEXICON) == 23
    assert REJECTED_TERMS.isdisjoint(FINANCE_LEXICON)
    assert all(finance.lexicon[term] == value for term, value in FINANCE_LEXICON.items())
    assert all(second_finance.lexicon[term] == value for term, value in FINANCE_LEXICON.items())
    assert finance.lexicon["shares"] == finance.lexicon["energy"] == 0.0
    title = "Shares rally!"
    assert plain.polarity_scores(title) == create_vader_analyzers()[0].polarity_scores(title)


def test_title_preservation_separate_scoring_and_deterministic_tokens():
    titles = ["  Shares RALLY!!!  ", "Don't underperform -- again?"]
    source = _mapped(titles)
    scored = score_headlines(source)
    assert scored["title"].tolist() == titles
    assert scored["source_row_order"].tolist() == [0, 1]
    assert matched_tokens(titles[0]) == ("shares", "rally")
    assert matched_tokens(titles[1]) == ("don't", "underperform", "again")
    assert TOKEN_PATTERN_TEXT == r"(?<![A-Za-z0-9])[A-Za-z]+(?:['-][A-Za-z]+)*(?![A-Za-z0-9])"
    plain, finance = create_vader_analyzers()
    assert scored.loc[0, "plain_compound"] == plain.polarity_scores(titles[0])["compound"]
    assert scored.loc[0, "finance_compound"] == finance.polarity_scores(titles[0])["compound"]


def test_nonzero_coverage_custom_hit_and_reliability_manual_example():
    date = pd.Timestamp("2020-01-02")
    scored = pd.DataFrame(
        [
            _scored_row(date, "AAA", 1, 0.5, covered=True, custom=True),
            _scored_row(date, "AAA", 2, 0.6, covered=True, custom=False),
            _scored_row(date, "AAA", 3, 0.0, covered=False, custom=True),
        ]
    )
    dates = pd.DatetimeIndex([date, pd.Timestamp("2020-01-03")])
    panel = build_ticker_sentiment_daily(scored, _coverage(dates, ("AAA",), {(date, "AAA"): 3}))
    news = panel.iloc[0]
    assert news.covered_headline_share == pytest.approx(2 / 3)
    assert news.custom_finance_term_hit_share == pytest.approx(2 / 3)
    assert news.nonneutral_headline_count == 2
    assert news.directional_agreement == 1.0
    assert news.volume_evidence == 0.75
    assert news.reliability == pytest.approx(0.5)
    assert news.evidence_aware_compound == pytest.approx(news.finance_score * 0.5)
    no_news = panel.iloc[1]
    assert not no_news.has_news and no_news.headline_count == 0
    assert no_news.nonneutral_headline_count == 0
    missing_sentiment_fields = [
        "plain_score", "finance_score", "covered_headline_share",
        "directional_agreement", "volume_evidence", "reliability",
        "custom_finance_term_hit_share", "evidence_aware_compound",
        "plain_z", "finance_z", "evidence_aware_signal",
    ]
    assert no_news[missing_sentiment_fields].isna().all()


def test_m_zero_scored_neutral_is_not_no_news():
    date = pd.Timestamp("2020-01-02")
    scored = pd.DataFrame([_scored_row(date, "AAA", 1, 0.0, covered=False, custom=True)])
    panel = build_ticker_sentiment_daily(scored, _coverage(pd.DatetimeIndex([date]), ("AAA",), {(date, "AAA"): 1}))
    row = panel.iloc[0]
    assert row.has_news and row.finance_score == 0.0
    assert row.directional_agreement == 0.0 and row.reliability == 0.0


def test_sector_equal_weights_news_tickers_not_headlines_and_no_news_behavior():
    date = pd.Timestamp("2020-01-02")
    next_date = pd.Timestamp("2020-01-03")
    scored = pd.DataFrame(
        [
            _scored_row(date, "AAA", 1, 1.0),
            _scored_row(date, "AAA", 2, 1.0),
            _scored_row(date, "AAA", 3, 1.0),
            _scored_row(date, "BBB", 4, -1.0),
        ]
    )
    coverage = _coverage(pd.DatetimeIndex([date, next_date]), ("AAA", "BBB"), {(date, "AAA"): 3, (date, "BBB"): 1})
    ticker = build_ticker_sentiment_daily(scored, coverage)
    sector, custom = build_sector_sentiment_index(ticker)
    first = sector.loc[sector["date"].eq(date)].iloc[0]
    assert first.finance_compound == pytest.approx(0.0)
    assert first.headline_count == 4 and first.ticker_count_with_news == 2
    second = sector.loc[sector["date"].eq(next_date)].iloc[0]
    assert second.ticker_count_with_news == 0 and second.ticker_coverage == 0.0
    assert pd.isna(second.finance_compound) and pd.isna(second.mean_reliability)
    assert custom["headlines"].sum() == 4


def test_past_only_window_ddof_minimum_clipping_lag_and_no_carry():
    dates = pd.bdate_range("2020-01-02", periods=64)
    rows = []
    counts = {}
    for index, date in enumerate(dates):
        if index == 61:  # explicit no-news date after the first usable score
            continue
        value = float((index % 7) - 3) / 10.0
        rows.append(_scored_row(date, "AAA", index, value))
        counts[(pd.Timestamp(date), "AAA")] = 1
    panel = build_ticker_sentiment_daily(pd.DataFrame(rows), _coverage(dates, ("AAA",), counts))
    sixty = panel.loc[panel["date"].eq(dates[60])].iloc[0]
    history = np.array([float((index % 7) - 3) / 10.0 for index in range(MINIMUM_HISTORY)])
    expected = (float((60 % 7) - 3) / 10.0 - history.mean()) / history.std(ddof=1)
    assert sixty.finance_z == pytest.approx(np.clip(expected, -3.0, 3.0))
    assert panel.loc[panel["date"].lt(dates[60]), "finance_z"].isna().all()
    no_news = panel.loc[panel["date"].eq(dates[61])].iloc[0]
    after_no_news = panel.loc[panel["date"].eq(dates[62])].iloc[0]
    assert pd.isna(no_news.finance_z)
    assert after_no_news.signal_source_date == dates[61]
    assert pd.isna(after_no_news.lagged_finance_signal)


def test_next_observed_date_lag_weekend_holiday_and_future_perturbation():
    dates = pd.DatetimeIndex([pd.Timestamp("2020-07-02"), pd.Timestamp("2020-07-06"), pd.Timestamp("2020-07-07")])
    scored = pd.DataFrame([_scored_row(date, "AAA", index, 0.1 + index) for index, date in enumerate(dates)])
    counts = {(date, "AAA"): 1 for date in dates}
    first = build_ticker_sentiment_daily(scored, _coverage(dates, ("AAA",), counts))
    assert first.loc[first["date"].eq(pd.Timestamp("2020-07-06")), "signal_source_date"].iloc[0] == pd.Timestamp("2020-07-02")
    altered = scored.copy(deep=True)
    altered.loc[altered["mapped_trade_date"].eq(dates[-1]), "finance_compound"] = -0.9
    second = build_ticker_sentiment_daily(altered, _coverage(dates, ("AAA",), counts))
    pd.testing.assert_frame_equal(
        first.loc[first["date"].lt(dates[-1])].reset_index(drop=True),
        second.loc[second["date"].lt(dates[-1])].reset_index(drop=True),
    )


def test_zero_and_near_zero_dispersion_leave_z_missing():
    dates = pd.bdate_range("2020-01-02", periods=62)
    rows = [_scored_row(date, "AAA", index, 0.2 + index * 1e-12) for index, date in enumerate(dates)]
    panel = build_ticker_sentiment_daily(pd.DataFrame(rows), _coverage(dates, ("AAA",), {(date, "AAA"): 1 for date in dates}))
    assert panel["finance_z"].isna().all()
