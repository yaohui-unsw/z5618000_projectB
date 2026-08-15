"""Deterministic sentiment features for the frozen Stage 6C design.

The module keeps headline text intact, isolates plain and finance-adjusted
VADER analyzers, aggregates only mapped equity news, and applies past-only
standardisation and a one-observed-trading-day lag.  It never reads returns.
"""
from __future__ import annotations

from collections.abc import Iterable
import re
from typing import Any

import numpy as np
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

from src.validation import (
    BENCHMARKS,
    EQUITY_TICKERS,
    SECTOR_DISPLAY_LABELS,
    SOURCE_SECTORS,
)


TOKEN_PATTERN_TEXT = r"(?<![A-Za-z0-9])[A-Za-z]+(?:['-][A-Za-z]+)*(?![A-Za-z0-9])"
TOKEN_PATTERN = re.compile(TOKEN_PATTERN_TEXT)
NEUTRAL_BAND = 0.05
STANDARDISATION_WINDOW = 252
MINIMUM_HISTORY = 60
MINIMUM_STD = 1e-8
ZSCORE_LIMIT = 3.0
DECISION_DATE = "2026-08-14"


# In student-approved order.  The zero values are intentional overrides.
FINANCE_LEXICON: dict[str, float] = {
    "shares": 0.0,
    "energy": 0.0,
    "alert": 0.0,
    "rally": 1.0,
    "active": 0.0,
    "beat": 1.5,
    "rebound": 0.5,
    "downgrades": -1.0,
    "asset": 0.0,
    "beats": 1.5,
    "outperform": 1.0,
    "miss": -1.0,
    "overweight": 1.0,
    "bullish": 1.5,
    "slump": -1.5,
    "misses": -1.5,
    "plunge": -1.5,
    "downgraded": -1.5,
    "tumble": -1.5,
    "underweight": -1.0,
    "plunges": -1.5,
    "underperform": -1.0,
    "layoffs": -1.0,
}

REJECTED_TERMS = frozenset({"inflow", "inflows", "outflow", "outflows"})


LEXICON_METADATA: tuple[dict[str, Any], ...] = (
    {"term": "shares", "candidate_class": "reviewed_override", "vanilla": 1.2, "decision": "ACCEPT", "rationale": "In financial headlines it is normally a neutral noun referring to equity units."},
    {"term": "energy", "candidate_class": "reviewed_override", "vanilla": 1.1, "decision": "ACCEPT", "rationale": "It normally identifies a sector, commodity theme, or name component rather than positive affect."},
    {"term": "alert", "candidate_class": "reviewed_override", "vanilla": 1.2, "decision": "ACCEPT", "rationale": "In this corpus it is mainly a publication, ETF-flow, option, or trading-alert label."},
    {"term": "rally", "candidate_class": "addition", "vanilla": np.nan, "decision": "ACCEPT", "rationale": "It normally denotes a positive market-price movement, with a conservative magnitude retained for attribution and question risk."},
    {"term": "active", "candidate_class": "reviewed_override", "vanilla": 1.7, "decision": "ACCEPT", "rationale": "Most active describes trading activity or volume rather than favourable performance."},
    {"term": "beat", "candidate_class": "addition", "vanilla": np.nan, "decision": "ACCEPT", "rationale": "An earnings, revenue, or estimate beat is materially favourable; other words can represent offsetting clauses."},
    {"term": "rebound", "candidate_class": "addition", "vanilla": np.nan, "decision": "EDIT", "rationale": "It is directionally positive, but can be prospective, temporary, or refer to another asset, so a weaker value is more defensible."},
    {"term": "downgrades", "candidate_class": "addition", "vanilla": np.nan, "decision": "EDIT", "rationale": "Rating downgrades are negative, but this plural form often appears in mixed analyst-action digests."},
    {"term": "asset", "candidate_class": "reviewed_override", "vanilla": 1.5, "decision": "ACCEPT", "rationale": "It is generally a neutral finance noun or organisation-name component."},
    {"term": "beats", "candidate_class": "addition", "vanilla": np.nan, "decision": "ACCEPT", "rationale": "It normally reports performance above expectations; mixed clauses remain visible through other headline terms."},
    {"term": "outperform", "candidate_class": "addition", "vanilla": np.nan, "decision": "EDIT", "rationale": "It is a favourable rating, but maintained ratings and simultaneous target cuts justify a more conservative magnitude."},
    {"term": "miss", "candidate_class": "reviewed_override", "vanilla": -0.6, "decision": "EDIT", "rationale": "It frequently denotes an earnings or revenue shortfall but also occurs in ordinary constructions such as miss out."},
    {"term": "overweight", "candidate_class": "reviewed_override", "vanilla": -1.5, "decision": "ACCEPT", "rationale": "In financial ratings it is positive and corrects the inappropriate negative vanilla-VADER sign."},
    {"term": "bullish", "candidate_class": "addition", "vanilla": np.nan, "decision": "ACCEPT", "rationale": "It directly expresses a positive market or analyst view, while existing VADER rules and other words retain some contextual qualification."},
    {"term": "slump", "candidate_class": "addition", "vanilla": np.nan, "decision": "ACCEPT", "rationale": "It denotes a material adverse decline in markets, demand, or activity."},
    {"term": "misses", "candidate_class": "reviewed_override", "vanilla": -0.9, "decision": "ACCEPT", "rationale": "In this finance corpus it usually reports failure to meet earnings, sales, or operating expectations."},
    {"term": "plunge", "candidate_class": "addition", "vanilla": np.nan, "decision": "ACCEPT", "rationale": "It denotes a sharp adverse decline, with the magnitude kept below extreme VADER values."},
    {"term": "downgraded", "candidate_class": "addition", "vanilla": np.nan, "decision": "ACCEPT", "rationale": "It directly reports an adverse analyst-rating reduction."},
    {"term": "tumble", "candidate_class": "addition", "vanilla": np.nan, "decision": "ACCEPT", "rationale": "It denotes a substantial negative market or operating movement."},
    {"term": "underweight", "candidate_class": "addition", "vanilla": np.nan, "decision": "ACCEPT", "rationale": "In finance it is an unfavourable relative-allocation or analyst-rating term."},
    {"term": "plunges", "candidate_class": "addition", "vanilla": np.nan, "decision": "ACCEPT", "rationale": "It is the inflected form of a sharp adverse decline."},
    {"term": "underperform", "candidate_class": "addition", "vanilla": np.nan, "decision": "EDIT", "rationale": "It is an unfavourable rating, but a symmetric conservative value with outperform reduces overstatement and maintained-rating risk."},
    {"term": "layoffs", "candidate_class": "addition", "vanilla": np.nan, "decision": "EDIT", "rationale": "Workforce reductions are generally adverse, but cost-reduction and restructuring interpretations justify a weaker value."},
)


TICKER_SENTIMENT_COLUMNS = (
    "date", "ticker", "sector", "headline_count", "has_news", "plain_score",
    "finance_score", "covered_headline_share", "nonneutral_headline_count",
    "directional_agreement", "volume_evidence", "reliability",
    "custom_finance_term_hit_share", "evidence_aware_compound", "plain_z",
    "finance_z", "evidence_aware_signal", "signal_source_date",
    "lagged_plain_signal", "lagged_finance_signal",
    "lagged_evidence_aware_signal",
)

SECTOR_SENTIMENT_COLUMNS = (
    "date", "sector", "sector_display", "headline_count",
    "ticker_count_with_news", "ticker_coverage", "plain_compound",
    "finance_compound", "mean_reliability", "evidence_aware_compound",
    "plain_z", "finance_z", "evidence_aware_z",
)

SENTIMENT_DIAGNOSTIC_COLUMNS = (
    "scope", "entity", "model", "metric", "value", "numerator",
    "denominator", "start_date", "end_date", "notes",
)

FINANCE_LEXICON_COLUMNS = (
    "term", "candidate_class", "vanilla_vader_value",
    "approved_finance_value", "direction", "student_decision",
    "decision_date", "rationale",
)


class SentimentBlockError(RuntimeError):
    """A frozen sentiment invariant failed."""


def create_vader_analyzers() -> tuple[SentimentIntensityAnalyzer, SentimentIntensityAnalyzer]:
    """Return isolated vanilla and finance analyzers without mutating vanilla."""
    if set(FINANCE_LEXICON) & REJECTED_TERMS or len(FINANCE_LEXICON) != 23:
        raise SentimentBlockError("operational finance lexicon is not the frozen set")
    plain = SentimentIntensityAnalyzer()
    vanilla_snapshot = dict(plain.lexicon)
    finance = SentimentIntensityAnalyzer()
    finance.lexicon.update(FINANCE_LEXICON)
    if plain.lexicon != vanilla_snapshot:
        raise SentimentBlockError("finance analyzer creation mutated vanilla VADER")
    if any(finance.lexicon.get(term) != value for term, value in FINANCE_LEXICON.items()):
        raise SentimentBlockError("finance analyzer differs from the frozen lexicon")
    return plain, finance


def matched_tokens(title: str) -> tuple[str, ...]:
    """Return deterministic lowercase token keys without changing stored text."""
    if not isinstance(title, str):
        raise SentimentBlockError("headline title must be a non-missing string")
    return tuple(match.group(0).lower() for match in TOKEN_PATTERN.finditer(title))


def score_headlines(
    mapped_headlines: pd.DataFrame,
    *,
    plain_analyzer: SentimentIntensityAnalyzer | None = None,
    finance_analyzer: SentimentIntensityAnalyzer | None = None,
) -> pd.DataFrame:
    """Score each mapped headline separately and retain auditable identifiers."""
    required = {
        "source_row_order", "source_timestamp", "source_date_utc", "ticker",
        "sector", "title", "mapped_trade_date", "map_status",
    }
    missing = sorted(required.difference(mapped_headlines.columns))
    if missing:
        raise SentimentBlockError(f"mapped headlines missing columns: {missing}")
    if mapped_headlines["title"].isna().any():
        raise SentimentBlockError("mapped headline titles contain missing values")
    plain, finance = (
        create_vader_analyzers()
        if plain_analyzer is None or finance_analyzer is None
        else (plain_analyzer, finance_analyzer)
    )
    active_nonzero = {term for term, value in finance.lexicon.items() if value != 0}
    custom_terms = set(FINANCE_LEXICON)

    rows: list[dict[str, Any]] = []
    for row in mapped_headlines.itertuples(index=False):
        title = row.title
        tokens = set(matched_tokens(title))
        rows.append(
            {
                "source_row_order": int(row.source_row_order),
                "source_timestamp": pd.Timestamp(row.source_timestamp),
                "source_date_utc": pd.Timestamp(row.source_date_utc),
                "mapped_trade_date": pd.Timestamp(row.mapped_trade_date),
                "ticker": str(row.ticker),
                "sector": str(row.sector),
                "title": title,
                "plain_compound": float(plain.polarity_scores(title)["compound"]),
                "finance_compound": float(finance.polarity_scores(title)["compound"]),
                "covered_nonzero": bool(tokens & active_nonzero),
                "custom_term_hit": bool(tokens & custom_terms),
            }
        )
    scored = pd.DataFrame(rows)
    return scored.sort_values(
        ["mapped_trade_date", "ticker", "source_timestamp", "source_row_order"],
        kind="mergesort",
    ).reset_index(drop=True)


def _past_only_zscore(
    frame: pd.DataFrame,
    *,
    group_column: str,
    value_column: str,
    output_column: str,
) -> pd.DataFrame:
    """Calculate a past-only z-score on the previous 252 observed dates."""
    result = frame.copy(deep=True)
    result[output_column] = np.nan
    for _, indices in result.groupby(group_column, sort=False, observed=True).groups.items():
        positions = list(indices)
        series = result.loc[positions, value_column].astype("float64")
        history = series.shift(1).rolling(
            window=STANDARDISATION_WINDOW,
            min_periods=MINIMUM_HISTORY,
        )
        mean = history.mean()
        std = history.std(ddof=1)
        valid = series.notna() & std.notna() & np.isfinite(std) & std.gt(MINIMUM_STD)
        zscore = ((series - mean) / std).where(valid).clip(-ZSCORE_LIMIT, ZSCORE_LIMIT)
        result.loc[positions, output_column] = zscore.to_numpy(dtype="float64")
    return result


def build_ticker_sentiment_daily(
    scored_headlines: pd.DataFrame,
    coverage_panel: pd.DataFrame,
    *,
    enforce_contract_counts: bool = False,
) -> pd.DataFrame:
    """Create the complete 50-by-1,006 ticker-day sentiment panel."""
    coverage_required = {"date", "ticker", "sector", "headline_count", "has_news"}
    if not coverage_required.issubset(coverage_panel.columns):
        raise SentimentBlockError("coverage panel does not match the frozen schema")
    work = scored_headlines.copy(deep=True)
    work["nonneutral"] = work["finance_compound"].abs().ge(NEUTRAL_BAND)
    work["nonneutral_sign"] = np.where(
        work["nonneutral"], np.sign(work["finance_compound"]), 0.0
    )
    grouped = work.groupby(["mapped_trade_date", "ticker"], sort=False, observed=True)
    aggregates = grouped.agg(
        headline_count=("title", "size"),
        plain_score=("plain_compound", "mean"),
        finance_score=("finance_compound", "mean"),
        covered_headline_share=("covered_nonzero", "mean"),
        nonneutral_headline_count=("nonneutral", "sum"),
        signed_nonneutral=("nonneutral_sign", "sum"),
        custom_finance_term_hit_share=("custom_term_hit", "mean"),
    ).reset_index().rename(columns={"mapped_trade_date": "date"})
    aggregates["nonneutral_headline_count"] = aggregates[
        "nonneutral_headline_count"
    ].astype("int64")
    aggregates["directional_agreement"] = np.where(
        aggregates["nonneutral_headline_count"].gt(0),
        aggregates["signed_nonneutral"].abs()
        / aggregates["nonneutral_headline_count"],
        0.0,
    )
    aggregates["volume_evidence"] = aggregates["headline_count"].div(
        aggregates["headline_count"].add(1)
    )
    aggregates["reliability"] = (
        aggregates["covered_headline_share"]
        * aggregates["directional_agreement"]
        * aggregates["volume_evidence"]
    )
    aggregates["evidence_aware_compound"] = (
        aggregates["finance_score"] * aggregates["reliability"]
    )
    aggregates = aggregates.drop(columns="signed_nonneutral")

    panel = coverage_panel.loc[:, ["date", "ticker", "sector", "headline_count", "has_news"]].copy(deep=True)
    panel["date"] = pd.to_datetime(panel["date"])
    panel = panel.merge(
        aggregates,
        on=["date", "ticker"],
        how="left",
        validate="one_to_one",
        suffixes=("", "_scored"),
    )
    if not panel.loc[panel["has_news"], "headline_count_scored"].eq(
        panel.loc[panel["has_news"], "headline_count"]
    ).all():
        raise SentimentBlockError("headline aggregation does not reconcile to coverage")
    panel = panel.drop(columns="headline_count_scored")
    panel["nonneutral_headline_count"] = panel[
        "nonneutral_headline_count"
    ].fillna(0).astype("int64")
    no_news = ~panel["has_news"]
    missing_on_no_news = [
        "plain_score", "finance_score", "covered_headline_share",
        "directional_agreement", "volume_evidence", "reliability",
        "custom_finance_term_hit_share", "evidence_aware_compound",
    ]
    if not panel.loc[no_news, missing_on_no_news].isna().all().all():
        raise SentimentBlockError("no-news rows acquired fabricated sentiment values")
    for component in (
        "covered_headline_share", "directional_agreement", "volume_evidence",
        "reliability", "custom_finance_term_hit_share",
    ):
        values = panel.loc[panel["has_news"], component]
        if values.isna().any() or not values.between(0.0, 1.0).all():
            raise SentimentBlockError(f"{component} is not finite in [0,1]")

    panel = panel.sort_values(["ticker", "date"], kind="mergesort").reset_index(drop=True)
    panel = _past_only_zscore(
        panel, group_column="ticker", value_column="plain_score", output_column="plain_z"
    )
    panel = _past_only_zscore(
        panel, group_column="ticker", value_column="finance_score", output_column="finance_z"
    )
    panel["evidence_aware_signal"] = panel["finance_z"] * panel["reliability"]
    grouped_panel = panel.groupby("ticker", sort=False, observed=True)
    panel["signal_source_date"] = grouped_panel["date"].shift(1)
    panel["lagged_plain_signal"] = grouped_panel["plain_z"].shift(1)
    panel["lagged_finance_signal"] = grouped_panel["finance_z"].shift(1)
    panel["lagged_evidence_aware_signal"] = grouped_panel[
        "evidence_aware_signal"
    ].shift(1)
    panel = panel.sort_values(["date", "ticker"], kind="mergesort").reset_index(drop=True)
    panel["ticker"] = panel["ticker"].astype("string")
    panel["sector"] = panel["sector"].astype("string")
    if enforce_contract_counts and (
        len(panel) != BENCHMARKS["coverage_rows"]
        or int((~panel["has_news"]).sum()) != BENCHMARKS["no_news_rows"]
    ):
        raise SentimentBlockError("ticker sentiment panel count differs from contract")
    return panel.loc[:, list(TICKER_SENTIMENT_COLUMNS)]


def _source_sector_sort(frame: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    result = frame.copy(deep=True)
    result["_sector_order"] = pd.Categorical(
        result["sector"], categories=list(SOURCE_SECTORS), ordered=True
    ).codes
    result = result.sort_values(
        [*columns, "_sector_order"], kind="mergesort"
    ).drop(columns="_sector_order")
    return result.reset_index(drop=True)


def build_sector_sentiment_index(
    ticker_daily: pd.DataFrame,
    *,
    enforce_contract_counts: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Aggregate ticker days equally within sector and return custom-hit evidence."""
    required = set(TICKER_SENTIMENT_COLUMNS)
    if not required.issubset(ticker_daily.columns):
        raise SentimentBlockError("ticker sentiment input does not match frozen schema")
    sector_sizes = (
        ticker_daily.loc[:, ["ticker", "sector"]]
        .drop_duplicates()
        .groupby("sector", observed=True)["ticker"]
        .nunique()
    )
    base = ticker_daily.groupby(["date", "sector"], sort=False, observed=True).agg(
        headline_count=("headline_count", "sum"),
        ticker_count_with_news=("has_news", "sum"),
    ).reset_index()
    base["headline_count"] = base["headline_count"].astype("int64")
    base["ticker_count_with_news"] = base["ticker_count_with_news"].astype("int64")
    base["ticker_coverage"] = base["ticker_count_with_news"].div(
        base["sector"].map(sector_sizes)
    )
    news = ticker_daily.loc[ticker_daily["has_news"]].copy(deep=True)
    means = news.groupby(["date", "sector"], sort=False, observed=True).agg(
        plain_compound=("plain_score", "mean"),
        finance_compound=("finance_score", "mean"),
        mean_reliability=("reliability", "mean"),
        evidence_aware_compound=("evidence_aware_compound", "mean"),
    ).reset_index()
    sector = base.merge(means, on=["date", "sector"], how="left", validate="one_to_one")
    sector["sector_display"] = sector["sector"].map(SECTOR_DISPLAY_LABELS).astype("string")
    sector = sector.sort_values(["sector", "date"], kind="mergesort").reset_index(drop=True)
    for value_column, output_column in (
        ("plain_compound", "plain_z"),
        ("finance_compound", "finance_z"),
        ("evidence_aware_compound", "evidence_aware_z"),
    ):
        sector = _past_only_zscore(
            sector,
            group_column="sector",
            value_column=value_column,
            output_column=output_column,
        )
    sector = _source_sector_sort(sector, ["date"])
    sector["sector"] = sector["sector"].astype("string")
    if enforce_contract_counts and len(sector) != BENCHMARKS["equity_dates"] * len(SOURCE_SECTORS):
        raise SentimentBlockError("sector sentiment panel count differs from contract")

    custom = news.assign(
        custom_hit_headlines=(
            news["custom_finance_term_hit_share"] * news["headline_count"]
        )
    ).groupby(["date", "sector"], sort=False, observed=True).agg(
        custom_hit_headlines=("custom_hit_headlines", "sum"),
        headlines=("headline_count", "sum"),
    ).reset_index()
    custom["custom_finance_term_hit_share"] = custom[
        "custom_hit_headlines"
    ].div(custom["headlines"])
    custom = _source_sector_sort(custom, ["date"])
    return sector.loc[:, list(SECTOR_SENTIMENT_COLUMNS)], custom


def sector_sentiment_index(scores: pd.DataFrame) -> pd.DataFrame:
    """Compatibility wrapper returning only the required sector index."""
    sector, _ = build_sector_sentiment_index(scores)
    return sector


def build_finance_lexicon_table() -> pd.DataFrame:
    """Return the exact 23-entry student-approved operational lexicon."""
    rows = []
    for metadata in LEXICON_METADATA:
        term = metadata["term"]
        value = FINANCE_LEXICON[term]
        rows.append(
            {
                "term": term,
                "candidate_class": metadata["candidate_class"],
                "vanilla_vader_value": metadata["vanilla"],
                "approved_finance_value": value,
                "direction": "positive" if value > 0 else "negative" if value < 0 else "neutral",
                "student_decision": metadata["decision"],
                "decision_date": pd.Timestamp(DECISION_DATE),
                "rationale": metadata["rationale"],
            }
        )
    result = pd.DataFrame(rows).sort_values("term", kind="mergesort").reset_index(drop=True)
    return result.loc[:, list(FINANCE_LEXICON_COLUMNS)]


def _distribution_rows(
    values: pd.Series,
    *,
    scope: str,
    entity: str,
    model: str,
    metric_prefix: str,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    notes: str,
) -> list[dict[str, Any]]:
    clean = pd.Series(values, dtype="float64").dropna()
    statistics = {
        "count": float(len(clean)),
        "mean": float(clean.mean()) if len(clean) else np.nan,
        "std": float(clean.std(ddof=1)) if len(clean) > 1 else np.nan,
        "min": float(clean.min()) if len(clean) else np.nan,
        "q25": float(clean.quantile(0.25)) if len(clean) else np.nan,
        "median": float(clean.median()) if len(clean) else np.nan,
        "q75": float(clean.quantile(0.75)) if len(clean) else np.nan,
        "q90": float(clean.quantile(0.90)) if len(clean) else np.nan,
        "q95": float(clean.quantile(0.95)) if len(clean) else np.nan,
        "max": float(clean.max()) if len(clean) else np.nan,
    }
    return [
        {
            "scope": scope, "entity": entity, "model": model,
            "metric": f"{metric_prefix}_{name}", "value": value,
            "numerator": float(len(clean)) if name == "count" else np.nan,
            "denominator": np.nan, "start_date": start_date, "end_date": end_date,
            "notes": notes,
        }
        for name, value in statistics.items()
    ]


def build_sentiment_diagnostics(
    scored_headlines: pd.DataFrame,
    ticker_daily: pd.DataFrame,
    sector_index: pd.DataFrame,
    sector_custom_daily: pd.DataFrame,
    *,
    cleaned_headline_count: int = 146_836,
    unmapped_headline_count: int = 6,
) -> pd.DataFrame:
    """Build auditable sentiment diagnostics with explicit rate denominators."""
    start = pd.Timestamp(ticker_daily["date"].min())
    end = pd.Timestamp(ticker_daily["date"].max())
    rows: list[dict[str, Any]] = []

    def add(
        scope: str, entity: str, model: str, metric: str, value: float,
        numerator: float = np.nan, denominator: float = np.nan, notes: str = "",
    ) -> None:
        rows.append(
            {
                "scope": scope, "entity": entity, "model": model,
                "metric": metric, "value": float(value),
                "numerator": float(numerator), "denominator": float(denominator),
                "start_date": start, "end_date": end, "notes": notes,
            }
        )

    mapped = len(scored_headlines)
    add("headline", "all", "mapping", "mapped_headline_count", mapped, mapped, cleaned_headline_count, "Only mapped records enter trading-day sentiment.")
    add("headline", "all", "mapping", "unmapped_end_of_sample_count", unmapped_headline_count, unmapped_headline_count, cleaned_headline_count, "Six accepted endpoint records remain excluded from trading uses.")
    for model, column in (("plain_vader", "plain_compound"), ("finance_vader", "finance_compound")):
        values = scored_headlines[column]
        exact = int(values.eq(0.0).sum())
        neutral = int(values.abs().lt(NEUTRAL_BAND).sum())
        add("headline", "all", model, "exact_zero_rate", exact / mapped, exact, mapped, "Exact zero differs from the neutral band.")
        add("headline", "all", model, "neutral_band_rate", neutral / mapped, neutral, mapped, "Neutral band is abs(compound) < 0.05.")
    covered = int(scored_headlines["covered_nonzero"].sum())
    custom = int(scored_headlines["custom_term_hit"].sum())
    changed = int((scored_headlines["plain_compound"] - scored_headlines["finance_compound"]).abs().gt(1e-15).sum())
    add("headline", "all", "finance_vader", "nonzero_active_lexicon_coverage", covered / mapped, covered, mapped, "Zero-valued approved overrides do not count as non-zero coverage.")
    add("headline", "all", "finance_vader", "custom_finance_term_hit_share", custom / mapped, custom, mapped, "All 23 approved terms count, including zero-valued overrides.")
    add("headline", "all", "plain_to_finance", "changed_score_share", changed / mapped, changed, mapped, "A changed score is an absolute difference greater than 1e-15.")

    total_days = len(ticker_daily)
    news_days = int(ticker_daily["has_news"].sum())
    no_news_days = total_days - news_days
    add("ticker_day", "all", "coverage", "news_day_share", news_days / total_days, news_days, total_days, "News-bearing ticker-days only.")
    add("ticker_day", "all", "coverage", "no_news_day_share", no_news_days / total_days, no_news_days, total_days, "No-news remains missing information.")
    rows.extend(_distribution_rows(ticker_daily["reliability"], scope="ticker_day", entity="all", model="evidence_aware_finance", metric_prefix="reliability", start_date=start, end_date=end, notes="Reliability is descriptive evidence strength, not truth."))
    rows.extend(_distribution_rows(ticker_daily["directional_agreement"], scope="ticker_day", entity="all", model="evidence_aware_finance", metric_prefix="directional_agreement", start_date=start, end_date=end, notes="Agreement excludes finance-neutral headlines."))
    rows.extend(_distribution_rows(ticker_daily["volume_evidence"], scope="ticker_day", entity="all", model="evidence_aware_finance", metric_prefix="volume_evidence", start_date=start, end_date=end, notes="Headline volume is not information quality."))
    for model, z_column, lag_column in (
        ("plain_vader", "plain_z", "lagged_plain_signal"),
        ("finance_vader", "finance_z", "lagged_finance_signal"),
        ("evidence_aware_finance", "evidence_aware_signal", "lagged_evidence_aware_signal"),
    ):
        usable = int(ticker_daily[z_column].notna().sum())
        lagged = int(ticker_daily[lag_column].notna().sum())
        add("ticker_day", "all", model, "usable_signal_rate", usable / total_days, usable, total_days, "Past-only history and current news are both required.")
        add("ticker_day", "all", model, "lagged_signal_availability", lagged / total_days, lagged, total_days, "Only the immediately previous observed trading date is eligible.")

    sector_days = len(sector_index)
    sector_news = int(sector_index["ticker_count_with_news"].gt(0).sum())
    add("sector_day", "all", "coverage", "news_day_share", sector_news / sector_days, sector_news, sector_days, "Sector dates with at least one news-bearing ticker.")
    for sector in SOURCE_SECTORS:
        subset = sector_custom_daily.loc[sector_custom_daily["sector"].eq(sector)]
        numerator = float(subset["custom_hit_headlines"].sum())
        denominator = float(subset["headlines"].sum())
        value = numerator / denominator if denominator else np.nan
        add("sector", sector, "finance_vader", "custom_finance_term_hit_share", value, numerator, denominator, "Stored here rather than widening sector_sentiment_index.csv.")
    result = pd.DataFrame(rows).loc[:, list(SENTIMENT_DIAGNOSTIC_COLUMNS)]
    if result.duplicated(["scope", "entity", "model", "metric"]).any():
        raise SentimentBlockError("sentiment diagnostics contain duplicate keys")
    return result.sort_values(["scope", "entity", "model", "metric"], kind="mergesort").reset_index(drop=True)


__all__ = [
    "DECISION_DATE", "FINANCE_LEXICON", "FINANCE_LEXICON_COLUMNS",
    "LEXICON_METADATA", "MINIMUM_HISTORY", "MINIMUM_STD", "NEUTRAL_BAND",
    "REJECTED_TERMS", "SECTOR_SENTIMENT_COLUMNS", "SENTIMENT_DIAGNOSTIC_COLUMNS",
    "STANDARDISATION_WINDOW", "SentimentBlockError", "TICKER_SENTIMENT_COLUMNS",
    "TOKEN_PATTERN_TEXT", "build_finance_lexicon_table",
    "build_sector_sentiment_index", "build_sentiment_diagnostics",
    "build_ticker_sentiment_daily", "create_vader_analyzers", "matched_tokens",
    "score_headlines", "sector_sentiment_index",
]
