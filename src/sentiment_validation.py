"""Machine-readable validation for frozen sentiment and fusion artifacts."""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.fusion import (
    FUSION_COMPARISON_COLUMNS,
    FUSION_PERFORMANCE_COLUMNS,
    FUSION_RETURN_COLUMNS,
    FUSION_WEIGHT_COLUMNS,
    OVERLAY_IDS,
    OVERLAY_ORDER,
    OVERLAY_SPECS,
    TILT_STRENGTH,
    VARIANTS,
)
from src.portfolios import TRANSACTION_COST_RATE, WEIGHT_CAP, performance_metrics
from src.sentiment import (
    FINANCE_LEXICON,
    FINANCE_LEXICON_COLUMNS,
    LEXICON_METADATA,
    REJECTED_TERMS,
    SECTOR_SENTIMENT_COLUMNS,
    SENTIMENT_DIAGNOSTIC_COLUMNS,
    TICKER_SENTIMENT_COLUMNS,
)
from src.validation import (
    BENCHMARKS,
    CRYPTO_TICKERS,
    EQUITY_TICKERS,
    SECTOR_DISPLAY_LABELS,
    SOURCE_SECTORS,
    ValidationReport,
)


EXPECTED_ROWS = {
    "ticker_sentiment_daily": 50_300,
    "sector_sentiment_index": 10_060,
    "finance_lexicon": 23,
    "fusion_returns": 18_072,
    "fusion_weights": 47_520,
    "fusion_performance_metrics": 24,
    "fusion_comparison": 24,
}


def _columns(frame: pd.DataFrame, expected: tuple[str, ...]) -> bool:
    return tuple(frame.columns) == expected


def _unique(frame: pd.DataFrame, columns: list[str]) -> bool:
    return set(columns).issubset(frame.columns) and not frame.duplicated(columns).any()


def _close(left: Any, right: Any, tolerance: float = 1e-10) -> bool:
    return bool(np.allclose(left, right, rtol=tolerance, atol=tolerance, equal_nan=True))


def _ordered(frame: pd.DataFrame, columns: list[str]) -> bool:
    expected = frame.sort_values(columns, kind="mergesort").reset_index(drop=True)
    return frame.reset_index(drop=True).equals(expected)


def _metric_reconciliation(
    fusion_returns: pd.DataFrame,
    metrics: pd.DataFrame,
) -> bool:
    for row in metrics.itertuples(index=False):
        subset = fusion_returns.loc[
            fusion_returns["overlay_id"].eq(row.overlay_id)
        ].sort_values("date", kind="mergesort")
        if len(subset) != row.observations:
            return False
        net = performance_metrics(subset["net_return"], int(row.annualisation))
        gross = performance_metrics(subset["gross_return"], int(row.annualisation))
        rebalances = subset.loc[subset["is_rebalance"].astype(bool)]
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
            "transaction_cost_drag": gross["cumulative_return"] - net["cumulative_return"],
        }
        if any(not np.isclose(getattr(row, key), value, rtol=1e-10, atol=1e-10) for key, value in expected.items()):
            return False
        if int(row.rebalance_count) != len(rebalances):
            return False
    return True


def validate_sentiment_fusion_outputs(
    *,
    sector_sentiment_index: pd.DataFrame,
    ticker_sentiment_daily: pd.DataFrame,
    fusion_returns: pd.DataFrame,
    fusion_weights: pd.DataFrame,
    sentiment_diagnostics: pd.DataFrame,
    finance_lexicon: pd.DataFrame,
    fusion_performance_metrics: pd.DataFrame,
    fusion_comparison: pd.DataFrame,
    base_returns: pd.DataFrame,
    base_weights: pd.DataFrame,
    base_performance: pd.DataFrame,
    family_matrices: dict[str, pd.DataFrame] | None = None,
    plain_analyzer_unchanged: bool = True,
) -> ValidationReport:
    """Validate all eight canonical outputs and accepted immutable inputs."""
    report = ValidationReport()
    artifacts = {
        "ticker_sentiment_daily": (ticker_sentiment_daily, TICKER_SENTIMENT_COLUMNS),
        "sector_sentiment_index": (sector_sentiment_index, SECTOR_SENTIMENT_COLUMNS),
        "finance_lexicon": (finance_lexicon, FINANCE_LEXICON_COLUMNS),
        "fusion_returns": (fusion_returns, FUSION_RETURN_COLUMNS),
        "fusion_weights": (fusion_weights, FUSION_WEIGHT_COLUMNS),
        "fusion_performance_metrics": (fusion_performance_metrics, FUSION_PERFORMANCE_COLUMNS),
        "fusion_comparison": (fusion_comparison, FUSION_COMPARISON_COLUMNS),
        "sentiment_diagnostics": (sentiment_diagnostics, SENTIMENT_DIAGNOSTIC_COLUMNS),
    }
    schemas_ok = True
    for name, (frame, expected_columns) in artifacts.items():
        condition = _columns(frame, expected_columns)
        schemas_ok &= condition
        report.add(condition, f"{name}_schema", f"{name} has the frozen schema.", f"{name} schema differs from the frozen contract.", observed=tuple(frame.columns), expected=expected_columns)
        if name in EXPECTED_ROWS:
            report.add(len(frame) == EXPECTED_ROWS[name], f"{name}_rows", f"{name} has the required row count.", f"{name} row count differs from the contract.", observed=len(frame), expected=EXPECTED_ROWS[name])
    report.add(not sentiment_diagnostics.empty, "sentiment_diagnostics_nonempty", "Sentiment diagnostics are substantive.", "Sentiment diagnostics are empty.")
    if not schemas_ok:
        return report

    # Lexicon isolation and provenance.
    expected_metadata = {row["term"]: row for row in LEXICON_METADATA}
    lexicon_values = finance_lexicon.set_index("term")["approved_finance_value"].to_dict()
    report.add(set(lexicon_values) == set(FINANCE_LEXICON), "lexicon_term_set", "Exactly 23 approved terms are operational.", "Operational term set differs from the freeze.")
    report.add(all(np.isclose(lexicon_values.get(term, np.nan), value) for term, value in FINANCE_LEXICON.items()), "lexicon_values", "All operational values match the freeze.", "An operational value differs from the freeze.")
    report.add(REJECTED_TERMS.isdisjoint(finance_lexicon["term"]), "lexicon_rejections", "All four ETF-flow terms are absent.", "A rejected ETF-flow term is operational.")
    classes_ok = all(row.candidate_class == expected_metadata[row.term]["candidate_class"] for row in finance_lexicon.itertuples())
    decisions_ok = all(row.student_decision == expected_metadata[row.term]["decision"] for row in finance_lexicon.itertuples())
    increments_ok = all(abs(float(value) * 2 - round(float(value) * 2)) <= 1e-12 for value in finance_lexicon["approved_finance_value"])
    report.add(classes_ok and decisions_ok, "lexicon_provenance", "Candidate classes and student decisions are preserved.", "Lexicon provenance differs from the accepted review.")
    report.add(increments_ok, "lexicon_increments", "All values use 0.5 increments.", "A value is not on a 0.5 increment.")
    report.add(plain_analyzer_unchanged, "plain_analyzer_isolation", "Vanilla analyzer remained unchanged.", "Finance analyzer creation mutated vanilla VADER.")

    # Keys, panels, mapping reconciliation and order.
    report.add(_unique(ticker_sentiment_daily, ["date", "ticker"]), "ticker_key", "Ticker-day keys are unique.", "Ticker-day keys are duplicated.")
    report.add(_unique(sector_sentiment_index, ["date", "sector"]), "sector_key", "Sector-day keys are unique.", "Sector-day keys are duplicated.")
    report.add(_unique(fusion_returns, ["date", "overlay_id"]), "fusion_return_key", "Fusion return keys are unique.", "Fusion return keys are duplicated.")
    report.add(_unique(fusion_weights, ["date", "overlay_id", "ticker"]), "fusion_weight_key", "Fusion weight keys are unique.", "Fusion weight keys are duplicated.")
    report.add(_unique(finance_lexicon, ["term"]), "finance_lexicon_key", "Finance terms are unique.", "Finance terms are duplicated.")
    report.add(_unique(fusion_performance_metrics, ["overlay_id"]), "fusion_metric_key", "Performance keys are unique.", "Performance keys are duplicated.")
    report.add(_unique(fusion_comparison, ["overlay_id"]), "fusion_comparison_key", "Comparison keys are unique.", "Comparison keys are duplicated.")
    report.add(_unique(sentiment_diagnostics, ["scope", "entity", "model", "metric"]), "diagnostic_key", "Diagnostic keys are unique.", "Diagnostic keys are duplicated.")

    tickers = tuple(sorted(ticker_sentiment_daily["ticker"].astype(str).unique()))
    sectors = tuple(sorted(ticker_sentiment_daily["sector"].astype(str).unique()))
    dates = pd.DatetimeIndex(pd.to_datetime(ticker_sentiment_daily["date"]).unique()).sort_values()
    report.add(tickers == EQUITY_TICKERS, "ticker_membership", "Ticker membership matches the frozen 50.", "Ticker membership differs from the contract.")
    report.add(sectors == SOURCE_SECTORS, "sector_membership", "Raw-sector membership matches the frozen ten.", "Sector membership differs from the contract.")
    report.add(len(dates) == BENCHMARKS["equity_dates"], "sentiment_dates", "All 1,006 equity dates are present.", "Sentiment dates differ from the contract.")
    no_news = ~ticker_sentiment_daily["has_news"].astype(bool)
    report.add(int(no_news.sum()) == BENCHMARKS["no_news_rows"], "no_news_count", "Exactly 12,338 no-news ticker-days remain.", "No-news count differs from the contract.")
    missing_fields = ["plain_score", "finance_score", "covered_headline_share", "directional_agreement", "volume_evidence", "reliability", "custom_finance_term_hit_share", "evidence_aware_compound", "plain_z", "finance_z", "evidence_aware_signal"]
    report.add(ticker_sentiment_daily.loc[no_news, missing_fields].isna().all().all(), "no_news_missingness", "No-news remains missing rather than neutral.", "A no-news row contains fabricated sentiment.")
    report.add(bool((ticker_sentiment_daily["has_news"].astype(bool) & ticker_sentiment_daily["finance_score"].eq(0.0)).any()), "scored_neutral_distinction", "Scored-neutral news is distinguishable from no news.", "No scored-neutral news state is observable.")

    diagnostics_lookup = sentiment_diagnostics.set_index(["scope", "entity", "model", "metric"])["value"]
    mapped_key = ("headline", "all", "mapping", "mapped_headline_count")
    unmapped_key = ("headline", "all", "mapping", "unmapped_end_of_sample_count")
    report.add(mapped_key in diagnostics_lookup.index and np.isclose(diagnostics_lookup.loc[mapped_key], BENCHMARKS["mapped_headlines"]), "mapped_headline_reconciliation", "Diagnostics reconcile 146,830 mapped headlines.", "Mapped-headline diagnostics do not reconcile.")
    report.add(unmapped_key in diagnostics_lookup.index and np.isclose(diagnostics_lookup.loc[unmapped_key], BENCHMARKS["unmapped_headlines"]), "unmapped_headline_reconciliation", "Six endpoint exclusions remain disclosed.", "Unmapped-headline diagnostics do not reconcile.")
    report.add("custom_finance_term_hit_share" not in sector_sentiment_index.columns and ((sentiment_diagnostics["scope"].eq("sector")) & (sentiment_diagnostics["metric"].eq("custom_finance_term_hit_share"))).sum() == 10, "sector_schema_resolution", "Sector custom-hit diagnostics are stored only in diagnostics.", "Sector custom-hit schema resolution is inconsistent.")

    # Reliability, standardisation, lag, and sector equal weighting.
    news = ticker_sentiment_daily.loc[~no_news]
    reliability_expected = news["covered_headline_share"] * news["directional_agreement"] * news["volume_evidence"]
    volume_expected = news["headline_count"] / (news["headline_count"] + 1.0)
    report.add(_close(news["reliability"], reliability_expected) and _close(news["volume_evidence"], volume_expected), "reliability_formula", "Reliability and volume evidence reconcile.", "Reliability formula does not reconcile.")
    bounded = all(news[column].between(0.0, 1.0).all() for column in ["covered_headline_share", "directional_agreement", "volume_evidence", "reliability", "custom_finance_term_hit_share"])
    report.add(bounded, "reliability_bounds", "All evidence components are in [0,1].", "An evidence component is out of bounds.")
    ticker_z_values = ticker_sentiment_daily[["plain_z", "finance_z"]].to_numpy(dtype="float64").ravel()
    ticker_z_values = ticker_z_values[np.isfinite(ticker_z_values)]
    sector_z_values = sector_sentiment_index[["plain_z", "finance_z", "evidence_aware_z"]].to_numpy(dtype="float64").ravel()
    sector_z_values = sector_z_values[np.isfinite(sector_z_values)]
    zscore_bounds_ok = (
        len(ticker_z_values) > 0
        and len(sector_z_values) > 0
        and np.all((ticker_z_values >= -3.0) & (ticker_z_values <= 3.0))
        and np.all((sector_z_values >= -3.0) & (sector_z_values <= 3.0))
    )
    report.add(zscore_bounds_ok, "zscore_bounds", "All published z-scores obey clipping bounds.", "A published z-score is out of bounds.")
    lag_ok = True
    ticker_sorted = ticker_sentiment_daily.sort_values(["ticker", "date"], kind="mergesort")
    for _, group in ticker_sorted.groupby("ticker", sort=False):
        expected_source = pd.to_datetime(group["date"]).shift(1)
        lag_ok &= pd.to_datetime(group["signal_source_date"]).reset_index(drop=True).equals(expected_source.reset_index(drop=True))
        lag_ok &= _close(group["lagged_plain_signal"], group["plain_z"].shift(1))
        lag_ok &= _close(group["lagged_finance_signal"], group["finance_z"].shift(1))
        expected_evidence = (group["finance_z"] * group["reliability"]).shift(1)
        lag_ok &= _close(group["lagged_evidence_aware_signal"], expected_evidence)
    report.add(lag_ok, "trading_lag", "Signals use exactly the immediately prior observed date.", "A signal uses same-day, future, or carried-forward information.")

    sector_check = ticker_sentiment_daily.loc[ticker_sentiment_daily["has_news"].astype(bool)].groupby(["date", "sector"], observed=True).agg(
        plain_compound=("plain_score", "mean"), finance_compound=("finance_score", "mean"),
        mean_reliability=("reliability", "mean"), evidence_aware_compound=("evidence_aware_compound", "mean"),
    ).reset_index()
    published_sector = sector_sentiment_index.merge(sector_check, on=["date", "sector"], how="left", suffixes=("", "_expected"), validate="one_to_one")
    sector_equal = all(_close(published_sector[column], published_sector[f"{column}_expected"]) for column in ["plain_compound", "finance_compound", "mean_reliability", "evidence_aware_compound"])
    display_ok = all(SECTOR_DISPLAY_LABELS[str(row.sector)] == str(row.sector_display) for row in sector_sentiment_index.itertuples())
    report.add(sector_equal and display_ok, "sector_aggregation", "Sector scores equal-weight news-bearing tickers with accepted labels.", "Sector aggregation or mapping differs from the freeze.")

    # Overlay coverage, timing, constraints, projection, and costs.
    report.add(tuple(fusion_performance_metrics["overlay_id"]) == OVERLAY_IDS, "overlay_order", "All 24 overlays use deterministic order.", "Overlay coverage or order differs from the freeze.")
    report.add(set(fusion_returns["overlay_id"]) == set(OVERLAY_IDS) and not fusion_returns["family"].eq("Crypto").any(), "overlay_coverage", "Exactly 24 Equity/Combined overlays are reported.", "Overlay universe is incomplete or includes Crypto-only funds.")
    report.add(set(fusion_returns["variant"]) == set(VARIANTS), "variant_coverage", "All three frozen variants are present.", "Fusion variant coverage differs from the freeze.")
    expected_observations = fusion_returns.groupby("overlay_id").size()
    expected_rebalances = fusion_weights.groupby("overlay_id")["date"].nunique()
    report.add(expected_observations.eq(753).all() and expected_rebalances.eq(36).all(), "fusion_grain_counts", "Every overlay has 753 dates and 36 rebalances.", "Overlay date or rebalance counts differ from the freeze.")
    base_returns_work = base_returns.copy(deep=True)
    base_returns_work["date"] = pd.to_datetime(base_returns_work["date"])
    timing_ok = True
    for overlay in OVERLAY_SPECS:
        overlay_dates = pd.DatetimeIndex(fusion_returns.loc[fusion_returns["overlay_id"].eq(overlay.overlay_id), "date"])
        base_dates = pd.DatetimeIndex(base_returns_work.loc[base_returns_work["fund_id"].eq(overlay.base_fund_id), "date"])
        overlay_rebalances = set(pd.to_datetime(fusion_weights.loc[fusion_weights["overlay_id"].eq(overlay.overlay_id), "date"]))
        base_rebalances = set(base_dates[base_returns_work.loc[base_returns_work["fund_id"].eq(overlay.base_fund_id), "is_rebalance"].astype(bool).to_numpy()])
        timing_ok &= overlay_dates.equals(base_dates) and overlay_rebalances == base_rebalances
    report.add(timing_ok, "monthly_schedule", "Overlay dates and monthly rebalances equal their base funds.", "An overlay changed the accepted schedule.")

    grouped_weights = fusion_weights.groupby(["date", "overlay_id"], sort=False)
    sum_ok = grouped_weights["target_weight"].sum().sub(1.0).abs().le(1e-9).all()
    bounds_ok = fusion_weights["target_weight"].between(-1e-10, WEIGHT_CAP + 1e-10).all()
    projection_ok = fusion_weights["projection_success"].astype(bool).all()
    report.add(sum_ok and bounds_ok and projection_ok, "projection_constraints", "Every projected target is feasible and successful.", "A projected target violates constraints or failed.")
    multiplier_ok = _close(
        fusion_weights.loc[fusion_weights["signal_value"].notna(), "multiplier"],
        np.exp(TILT_STRENGTH * fusion_weights.loc[fusion_weights["signal_value"].notna(), "signal_value"]),
    ) and fusion_weights.loc[fusion_weights["signal_value"].isna(), "multiplier"].eq(1.0).all()
    report.add(multiplier_ok, "fixed_tilt", "Lambda is fixed at 0.10 and missing signals use multiplier one.", "Published multipliers differ from the frozen rule.")

    combined = fusion_weights.loc[fusion_weights["family"].eq("Combined")]
    base_weight_lookup = base_weights.copy(deep=True)
    base_weight_lookup["date"] = pd.to_datetime(base_weight_lookup["date"])
    compare = combined.merge(
        base_weight_lookup.loc[:, ["date", "fund_id", "ticker", "target_weight"]],
        left_on=["date", "base_fund_id", "ticker"],
        right_on=["date", "fund_id", "ticker"], how="left", validate="many_to_one",
        suffixes=("", "_base"),
    )
    crypto_compare = compare.loc[compare["ticker"].isin(CRYPTO_TICKERS)]
    crypto_unchanged = _close(crypto_compare["target_weight"], crypto_compare["target_weight_base"])
    sleeves = compare.loc[compare["ticker"].isin(EQUITY_TICKERS)].groupby(["date", "overlay_id"], sort=False).agg(overlay=("target_weight", "sum"), base=("target_weight_base", "sum"))
    report.add(crypto_unchanged and _close(sleeves["overlay"], sleeves["base"]), "combined_sleeves", "Combined crypto weights and equity-sleeve totals are preserved.", "A Combined overlay changed crypto weights or sleeve total.")

    returns_cost_ok = _close(fusion_returns["transaction_cost"], TRANSACTION_COST_RATE * fusion_returns["turnover"]) and _close(
        fusion_returns["net_return"],
        (1.0 - fusion_returns["transaction_cost"]) * (1.0 + fusion_returns["gross_return"]) - 1.0,
    )
    non_rebalance_zero = fusion_returns.loc[~fusion_returns["is_rebalance"].astype(bool), ["turnover", "transaction_cost"]].eq(0.0).all().all()
    weight_turnover = grouped_weights.agg(turnover=("turnover", "first"), calculated=("trade_weight", lambda x: 0.5 * float(np.abs(x).sum()))).reset_index()
    initial_dates = fusion_returns.groupby("overlay_id", sort=False)["date"].min()
    initial_mask = weight_turnover.apply(lambda row: pd.Timestamp(row.date) == pd.Timestamp(initial_dates.loc[row.overlay_id]), axis=1)
    turnover_ok = weight_turnover.loc[initial_mask, "turnover"].eq(0.0).all() and _close(weight_turnover.loc[~initial_mask, "turnover"], weight_turnover.loc[~initial_mask, "calculated"])
    report.add(returns_cost_ok and non_rebalance_zero and turnover_ok, "turnover_cost_arithmetic", "Turnover, 5-bps cost, and gross/net arithmetic reconcile.", "Turnover or transaction-cost arithmetic does not reconcile.")

    if family_matrices is not None:
        source_ok = True
        for overlay in OVERLAY_SPECS:
            sub_returns = fusion_returns.loc[fusion_returns["overlay_id"].eq(overlay.overlay_id)].sort_values("date", kind="mergesort")
            sub_weights = fusion_weights.loc[fusion_weights["overlay_id"].eq(overlay.overlay_id)]
            current: np.ndarray | None = None
            for row in sub_returns.itertuples(index=False):
                date = pd.Timestamp(row.date)
                asset_returns = family_matrices[overlay.family].loc[date, list(overlay.assets)].to_numpy(dtype="float64")
                if bool(row.is_rebalance):
                    group = sub_weights.loc[pd.to_datetime(sub_weights["date"]).eq(date)].set_index("ticker").reindex(list(overlay.assets))
                    target = group["target_weight"].to_numpy(dtype="float64")
                    pretrade = np.zeros(len(target)) if current is None else current
                    source_ok &= _close(group["pretrade_weight"], pretrade)
                    pre_return = target
                else:
                    if current is None:
                        source_ok = False
                        break
                    pre_return = current
                source_ok &= np.isclose(float(pre_return @ asset_returns), row.gross_return, rtol=1e-10, atol=1e-10)
                gross = float(pre_return @ asset_returns)
                current = pre_return * (1.0 + asset_returns) / (1.0 + gross)
        report.add(source_ok, "drift_source_reconciliation", "Daily drift and gross returns reconcile to source asset returns.", "Daily drift or source-return reconciliation failed.")

    report.add(_metric_reconciliation(fusion_returns, fusion_performance_metrics), "performance_reconciliation", "All 24 performance rows independently reconcile.", "A performance row does not reconcile.")
    base_index = base_performance.set_index("fund_id")
    metric_index = fusion_performance_metrics.set_index("overlay_id")
    comparison_ok = True
    for row in fusion_comparison.itertuples(index=False):
        overlay = metric_index.loc[row.overlay_id]
        base = base_index.loc[row.base_fund_id]
        base_drag = float(base["gross_cumulative_return"] - base["net_cumulative_return"])
        expected = {
            "delta_net_annualised_return": overlay["net_annualised_return"] - base["net_annualised_return"],
            "delta_annualised_volatility": overlay["net_annualised_volatility"] - base["net_annualised_volatility"],
            "delta_net_sharpe_ratio": overlay["net_sharpe_ratio"] - base["net_sharpe_ratio"],
            "delta_net_max_drawdown": overlay["net_max_drawdown"] - base["net_max_drawdown"],
            "delta_net_cumulative_return": overlay["net_cumulative_return"] - base["net_cumulative_return"],
            "delta_average_turnover": overlay["average_rebalance_turnover"] - base["average_rebalance_turnover"],
            "delta_total_turnover": overlay["total_turnover"] - base["total_turnover"],
            "delta_transaction_cost_drag": overlay["transaction_cost_drag"] - base_drag,
        }
        comparison_ok &= all(np.isclose(getattr(row, key), value, rtol=1e-10, atol=1e-10) for key, value in expected.items())
    report.add(comparison_ok and set(fusion_comparison["overlay_id"]) == set(OVERLAY_IDS), "base_comparison", "All 24 deltas reconcile to immutable base metrics.", "A base-comparison delta or overlay is missing.")

    # Disclosed limitations are warnings rather than deletion rules.
    report.warn("lexicon_context_limit", "Lexicon coverage does not prove contextual accuracy; all weak results remain reportable.")
    report.warn("evidence_reliability_limit", "Directional agreement, volume, and coverage are evidence diagnostics rather than truth or causality.")
    return report


__all__ = ["EXPECTED_ROWS", "validate_sentiment_fusion_outputs"]
