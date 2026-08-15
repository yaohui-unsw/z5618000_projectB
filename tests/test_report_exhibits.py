"""Independent tests for the Stage 7 result audit and canonical exhibits."""
from __future__ import annotations

from hashlib import sha256
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from src.reporting import (
    CANONICAL_INPUTS,
    EXPECTED_ROWS,
    FIGURE_FILENAMES,
    FROZEN_SHA256,
    SCHEMAS,
    audit_canonical_outputs,
    build_figure_artifacts,
    canonical_hashes,
    combined_weight_frame,
    file_sha256,
    load_canonical_outputs,
    plot_combined_drawdowns,
    plot_fund_growth,
    plot_fusion_turnover_tradeoff,
    plot_sentiment_diagnostics,
)


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "results" / "figures"


def _frames():
    return load_canonical_outputs(ROOT)


def test_frozen_inputs_have_exact_hashes_schemas_rows_and_keys() -> None:
    hashes = canonical_hashes(ROOT)
    assert hashes == FROZEN_SHA256
    frames = _frames()
    for name, expected_schema in SCHEMAS.items():
        assert tuple(frames[name].columns) == expected_schema
        if name in EXPECTED_ROWS:
            assert len(frames[name]) == EXPECTED_ROWS[name]
    key_map = {
        "fund_returns": ["date", "fund_id"],
        "fund_weights": ["date", "fund_id", "ticker"],
        "performance_metrics": ["fund_id"],
        "solver_diagnostics": ["date", "fund_id"],
        "ticker_sentiment": ["date", "ticker"],
        "sector_sentiment": ["date", "sector"],
        "fusion_returns": ["date", "overlay_id"],
        "fusion_weights": ["date", "overlay_id", "ticker"],
        "finance_lexicon": ["term"],
        "sentiment_diagnostics": ["scope", "entity", "model", "metric"],
        "fusion_metrics": ["overlay_id"],
        "fusion_comparison": ["overlay_id"],
    }
    for name, key in key_map.items():
        assert not frames[name][key].isna().any().any()
        assert not frames[name].duplicated(key).any()


def test_independent_audit_reconciles_metrics_coverage_and_deltas() -> None:
    frames = _frames()
    report = audit_canonical_outputs(frames, canonical_hashes(ROOT))
    assert report.ok, [finding.to_dict() for finding in report.findings if finding.level == "BLOCK"]
    evidence = report.evidence
    assert evidence["cleaned_headlines"] == 146_836
    assert evidence["mapped_headlines"] == 146_830
    assert evidence["unmapped_headlines"] == 6
    assert evidence["ticker_days"] == 50_300
    assert evidence["sector_days"] == 10_060
    assert evidence["no_news_ticker_days"] == 12_338
    assert evidence["news_ticker_days"] == 37_962
    assert evidence["finance_positive_sharpe_deltas"] == 5
    assert evidence["plain_positive_sharpe_deltas"] == 4
    assert evidence["evidence_positive_sharpe_deltas"] == 4
    assert evidence["finance_beats_plain_sharpe"] == 6
    assert evidence["finance_beats_plain_return"] == 7
    assert evidence["evidence_lower_turnover_all_eight"]
    assert evidence["evidence_lower_return_and_sharpe_all_eight"]
    assert evidence["base_metric_max_abs_error"] <= 5e-10
    assert evidence["fusion_metric_max_abs_error"] <= 5e-10
    assert evidence["base_delta_max_abs_error"] <= 5e-10


def test_signal_source_dates_are_strictly_past_and_not_carried() -> None:
    ticker = _frames()["ticker_sentiment"].sort_values(["ticker", "date"], kind="mergesort")
    for _, group in ticker.groupby("ticker", sort=False):
        assert group["signal_source_date"].reset_index(drop=True).equals(group["date"].reset_index(drop=True).shift(1))
        np.testing.assert_allclose(group["lagged_plain_signal"], group["plain_z"].shift(1), rtol=0, atol=1e-12, equal_nan=True)
        np.testing.assert_allclose(group["lagged_finance_signal"], group["finance_z"].shift(1), rtol=0, atol=1e-12, equal_nan=True)
        np.testing.assert_allclose(
            group["lagged_evidence_aware_signal"],
            (group["finance_z"] * group["reliability"]).shift(1),
            rtol=0,
            atol=1e-12,
            equal_nan=True,
        )
    present = ticker["signal_source_date"].notna()
    assert (ticker.loc[present, "signal_source_date"] < ticker.loc[present, "date"]).all()
    assert ticker["finance_z"].notna().sum() == 34_789
    assert ticker["lagged_finance_signal"].notna().sum() == 34_788


def test_combined_display_rule_is_deterministic_and_preserves_weight() -> None:
    frames = _frames()
    first, top_first = combined_weight_frame(frames)
    second, top_second = combined_weight_frame(frames)
    assert top_first == top_second == ("MRK", "WMT", "ABBV", "PSA", "GILD", "KO")
    assert first.equals(second)
    sums = first.groupby(["date", "fund_id"], sort=False)["target_weight"].sum()
    np.testing.assert_allclose(sums, 1.0, rtol=0, atol=1e-8)
    assert set(first["display_asset"]) == {*top_first, "Crypto sleeve", "Other equities"}
    source = frames["fund_weights"].loc[frames["fund_weights"]["family"].eq("Combined")]
    crypto_tickers = {"ADA-USD", "BCH-USD", "BTC-USD", "EOS-USD", "ETC-USD", "ETH-USD", "LTC-USD", "TRX-USD", "XLM-USD", "XRP-USD"}
    expected_crypto = source.loc[source["ticker"].isin(crypto_tickers)].groupby(["date", "fund_id"])["target_weight"].sum().sort_index()
    actual_crypto = first.loc[first["display_asset"].eq("Crypto sleeve")].set_index(["date", "fund_id"])["target_weight"].sort_index()
    np.testing.assert_allclose(actual_crypto, expected_crypto, rtol=0, atol=1e-12)
    expected_other_equities = source.loc[(~source["ticker"].isin(crypto_tickers)) & (~source["ticker"].isin(top_first))].groupby(["date", "fund_id"])["target_weight"].sum().sort_index()
    actual_other_equities = first.loc[first["display_asset"].eq("Other equities")].set_index(["date", "fund_id"])["target_weight"].sort_index()
    np.testing.assert_allclose(actual_other_equities, expected_other_equities, rtol=0, atol=1e-12)


def test_visual_correction_contracts_are_explicit_and_data_preserving() -> None:
    frames = _frames()
    growth = plot_fund_growth(frames)
    diagnostics = plot_sentiment_diagnostics(frames)
    tradeoff = plot_fusion_turnover_tradeoff(frames)
    try:
        growth_subtitle = " ".join(text.get_text() for text in growth.figure.texts)
        assert "panel-specific y-scales" in growth_subtitle
        assert len(growth.figure.axes) == 3
        assert len({tuple(round(value, 8) for value in ax.get_ylim()) for ax in growth.figure.axes}) == 3
        for ax in growth.figure.axes:
            assert ax.get_ylim()[0] < 1 < ax.get_ylim()[1]
            assert any(len(line.get_ydata()) == 2 and np.allclose(line.get_ydata(), [1.0, 1.0]) for line in ax.lines)

        diagnostic_text = " ".join(text.get_text() for text in diagnostics.figure.texts)
        diagnostic_axes_text = " ".join(
            [ax.get_xlabel() for ax in diagnostics.figure.axes]
            + [text.get_text() for ax in diagnostics.figure.axes for text in ax.texts]
        )
        assert "exposure to reviewed terms is not contextual accuracy" in diagnostic_text
        assert "≥1 reviewed custom term" in diagnostic_axes_text
        assert "intentional neutralisation" in diagnostic_text
        assert "does not imply lower information coverage" in diagnostic_text

        assert tradeoff.figure.axes[0].get_xlabel() == "Incremental average rebalance turnover vs base (percentage points)"
        tradeoff_text = " ".join(text.get_text() for text in tradeoff.figure.axes[0].texts)
        assert "Equity Maximum Sharpe + Finance VADER" in tradeoff_text
        assert "Sharpe delta +0.0192" in tradeoff_text
        assert "Equity Equal Weight + Evidence-aware Finance" in tradeoff_text
        assert "Sharpe delta -0.0059" in tradeoff_text
        assert "Lower incremental turnover, but lower Sharpe" in tradeoff_text
        assert "all 8 paired comparisons" in tradeoff_text
        assert "equity_maximum_sharpe__finance_vader_naive" not in tradeoff_text
    finally:
        plt.close(growth.figure)
        plt.close(diagnostics.figure)
        plt.close(tradeoff.figure)


def test_eight_pngs_are_substantive_300_dpi_and_metadata_bearing() -> None:
    assert all((FIGURE_DIR / filename).is_file() for filename in FIGURE_FILENAMES)
    for filename in FIGURE_FILENAMES:
        path = FIGURE_DIR / filename
        assert path.stat().st_size > 30_000
        with Image.open(path) as image:
            assert image.format == "PNG"
            assert image.width >= 3_000
            assert image.height >= 1_800
            dpi = image.info.get("dpi", (0, 0))
            assert min(dpi) >= 299
            assert image.info.get("Title")
            assert image.info.get("Description")
            pixels = np.asarray(image.convert("L").resize((160, 100)), dtype=float)
            assert pixels.std() >= 4.0
            assert pixels.max() - pixels.min() >= 35


def test_reporting_functions_supply_title_axis_unit_and_caveat_metadata_without_mutation() -> None:
    before_hashes = canonical_hashes(ROOT)
    frames = _frames()
    snapshots = {name: frame.copy(deep=True) for name, frame in frames.items()}
    artifacts = build_figure_artifacts(frames)
    try:
        assert tuple(artifact.metadata.filename for artifact in artifacts) == FIGURE_FILENAMES
        for artifact in artifacts:
            metadata = artifact.metadata
            assert metadata.title
            assert metadata.question
            assert metadata.x_label
            assert metadata.y_label
            assert metadata.units
            assert metadata.date_range
            assert metadata.caveat
            assert artifact.figure._suptitle is not None
            assert artifact.figure._suptitle.get_text() == metadata.title
    finally:
        for artifact in artifacts:
            plt.close(artifact.figure)
    for name, frame in frames.items():
        assert frame.equals(snapshots[name])
    assert canonical_hashes(ROOT) == before_hashes == FROZEN_SHA256


def test_representative_render_is_byte_deterministic() -> None:
    frames = _frames()

    def render() -> str:
        artifact = plot_combined_drawdowns(frames)
        stream = BytesIO()
        try:
            artifact.figure.savefig(
                stream,
                format="png",
                dpi=300,
                facecolor="#FBFCFD",
                edgecolor="none",
                metadata={
                    "Software": "FINS5545 Project B Stage 7",
                    "Title": artifact.metadata.title,
                    "Description": artifact.metadata.question,
                },
            )
        finally:
            plt.close(artifact.figure)
        return sha256(stream.getvalue()).hexdigest()

    assert render() == render()


def test_no_canonical_csv_was_modified_by_exhibit_generation() -> None:
    assert canonical_hashes(ROOT) == FROZEN_SHA256
    for name, relative in CANONICAL_INPUTS.items():
        assert file_sha256(ROOT / relative) == FROZEN_SHA256[name]
