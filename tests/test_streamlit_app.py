from __future__ import annotations

import ast
from pathlib import Path
import re

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
import pandas as pd
from streamlit.testing.v1 import AppTest

from src.app_charts import (
    FUND_SHORT_LABELS,
    FUSION_BASE_LABELS,
    METHOD_COLOURS,
    SECTOR_DISPLAY_NAMES,
    fusion_delta_chart,
    growth_chart,
    risk_return_chart,
    sector_term_exposure_chart,
)
from src.app_data import VARIANTS, load_base_metrics


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_PATH = PROJECT_ROOT / "streamlit_app.py"
APP_MODULES = (
    APP_PATH,
    PROJECT_ROOT / "src" / "app_data.py",
    PROJECT_ROOT / "src" / "app_logic.py",
    PROJECT_ROOT / "src" / "app_charts.py",
)


def _run_app() -> AppTest:
    app = AppTest.from_file(str(APP_PATH), default_timeout=45).run()
    assert not app.exception
    return app


def _rendered_text(app: AppTest) -> str:
    values: list[str] = []
    for collection_name in ("markdown", "caption", "info", "warning", "success", "error", "subheader", "metric"):
        for element in getattr(app, collection_name):
            values.append(str(getattr(element, "value", element)))
            values.append(str(getattr(element, "label", "")))
    return "\n".join(values)


def test_default_page_is_useful_and_contains_identity_disclaimer_and_all_funds() -> None:
    app = _run_app()
    text = _rendered_text(app)
    assert "MAIA" in text
    assert "Compare twelve systematic Equity, Crypto and Combined funds" in text
    assert "Historical out-of-sample illustration only" in text
    assert tuple(app.sidebar.radio[0].options) == (
        "Explore Funds", "Fund Fact Sheet", "Allocation Studio",
        "Sentiment & Innovation", "Methodology & Disclosures",
    )
    assert any(len(frame.value) == 12 for frame in app.dataframe)
    assert app.multiselect


def test_shared_header_safe_area_and_all_five_page_headers_render() -> None:
    source = APP_PATH.read_text(encoding="utf-8")
    assert re.search(
        r"\.block-container\s*\{[^}]*padding-top:\s*clamp\(4\.25rem,\s*8vh,\s*5rem\)",
        source,
        flags=re.DOTALL,
    )
    assert re.search(
        r"@media\s*\(max-width:\s*768px\)\s*\{\s*\.block-container\s*\{\s*padding-top:\s*4\.75rem;",
        source,
        flags=re.DOTALL,
    )
    assert "MAIA · Multi-Asset Investment Assistant" in source
    assert 'class="maia-kicker"' in source
    assert '[data-testid="stToolbar"]' not in source

    app = _run_app()
    for page_title in (
        "Explore Funds",
        "Fund Fact Sheet",
        "Allocation Studio",
        "Sentiment & Innovation",
        "Methodology & Disclosures",
    ):
        if app.sidebar.radio[0].value != page_title:
            app.sidebar.radio[0].set_value(page_title).run()
        assert not app.exception
        markdown_values = [str(element.value) for element in app.markdown]
        assert sum("MAIA · Multi-Asset Investment Assistant" in value for value in markdown_values) == 1
        assert any(f'class="maia-title">{page_title}</div>' in value for value in markdown_values)


def test_fact_sheet_navigation_and_fund_selection_render() -> None:
    app = _run_app()
    app.sidebar.radio[0].set_value("Fund Fact Sheet").run()
    assert not app.exception
    assert app.selectbox
    app.selectbox[0].set_value("combined_risk_parity").run()
    assert not app.exception
    text = _rendered_text(app)
    assert "Fund Fact Sheet" in text
    assert "Current target holdings" in text
    assert "How this fund works" in str(app)


def test_allocation_controls_exist_and_invalid_total_is_rejected() -> None:
    app = _run_app()
    app.sidebar.radio[0].set_value("Allocation Studio").run()
    assert not app.exception
    assert app.number_input and app.multiselect and len(app.select_slider) == 4
    app.select_slider[0].set_value(5).run()
    assert not app.exception
    text = _rendered_text(app)
    assert "Total allocation: 80%" in text
    assert "will not normalise it silently" in text


def test_sentiment_page_exposes_all_lexicon_and_fusion_evidence() -> None:
    app = _run_app()
    app.sidebar.radio[0].set_value("Sentiment & Innovation").run()
    assert not app.exception
    sizes = [len(frame.value) for frame in app.dataframe]
    assert 23 in sizes
    assert 24 in sizes
    text = _rendered_text(app)
    assert "Term exposure is not contextual accuracy" in text
    assert "No prespecified statistical significance test was conducted" in text


def test_methodology_page_is_reachable() -> None:
    app = _run_app()
    app.sidebar.radio[0].set_value("Methodology & Disclosures").run()
    assert not app.exception
    text = _rendered_text(app)
    assert "Methodology & Disclosures" in text
    assert "69 extreme returns" in text
    assert "one-observed-trading-day lag" in text


def test_static_runtime_guard_blocks_models_raw_loader_and_result_writes() -> None:
    banned_modules = {"nltk", "src.data_access", "src.portfolios", "src.sentiment", "src.fusion"}
    write_methods = {"to_csv", "to_parquet", "to_pickle", "to_excel", "write_text", "write_bytes", "savefig"}
    for path in APP_MODULES:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert banned_modules.isdisjoint(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                assert module not in banned_modules
                assert not (module == "src" and any(alias.name in {"data_access", "portfolios", "sentiment", "fusion"} for alias in node.names))
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                assert node.func.attr not in write_methods, (path, node.func.attr)
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open":
                mode = node.args[1].value if len(node.args) > 1 and isinstance(node.args[1], ast.Constant) else "r"
                assert not any(flag in str(mode) for flag in ("w", "a", "+", "x"))


def test_rendered_copy_has_no_absolute_path_or_affirmative_sales_language() -> None:
    app = _run_app()
    text = _rendered_text(app).lower()
    assert "c:\\users\\" not in text
    assert "buy now" not in text
    assert "guaranteed return" not in text
    assert "we recommend" not in text
    assert "recommended fund" not in text
    assert "best for you" not in text


def test_growth_method_colours_are_stable_across_selection_order_and_single_fund() -> None:
    selected = [
        "combined_risk_parity",
        "equity_minimum_variance",
        "crypto_maximum_sharpe",
        "equity_equal_weight",
    ]
    names = {fund: fund for fund in selected}
    rows = [
        {"date": date, "fund_id": fund, "growth": 1.0 + index * 0.01}
        for fund in selected
        for index, date in enumerate(pd.to_datetime(["2023-01-02", "2023-01-03"]))
    ]

    def observed_colours(frame: pd.DataFrame) -> dict[str, str]:
        figure = growth_chart(frame, names)
        try:
            return {
                str(line.get_label()): to_hex(line.get_color())
                for line in figure.axes[0].lines
                if str(line.get_label()) in names.values()
            }
        finally:
            plt.close(figure)

    expected = {
        "combined_risk_parity": to_hex(METHOD_COLOURS["Risk Parity"]),
        "equity_minimum_variance": to_hex(METHOD_COLOURS["Minimum Variance"]),
        "crypto_maximum_sharpe": to_hex(METHOD_COLOURS["Maximum Sharpe"]),
        "equity_equal_weight": to_hex(METHOD_COLOURS["Equal Weight"]),
    }
    frame = pd.DataFrame(rows)
    assert observed_colours(frame) == expected
    assert observed_colours(frame.iloc[::-1].reset_index(drop=True)) == expected
    assert observed_colours(frame.loc[frame["fund_id"].eq("crypto_maximum_sharpe")]) == {
        "crypto_maximum_sharpe": to_hex(METHOD_COLOURS["Maximum Sharpe"])
    }


def test_risk_return_labels_identify_all_funds_without_canvas_clipping_or_overlap() -> None:
    figure = risk_return_chart(load_base_metrics())
    try:
        figure.canvas.draw()
        renderer = figure.canvas.get_renderer()
        annotations = figure.axes[0].texts
        assert {annotation.get_text() for annotation in annotations} == set(FUND_SHORT_LABELS.values())
        boxes = [annotation.get_bbox_patch().get_window_extent(renderer) for annotation in annotations]
        canvas = figure.bbox
        for box in boxes:
            assert box.x0 >= canvas.x0 and box.x1 <= canvas.x1
            assert box.y0 >= canvas.y0 and box.y1 <= canvas.y1
        for index, first in enumerate(boxes):
            assert not any(first.overlaps(second) for second in boxes[index + 1 :])
    finally:
        plt.close(figure)


def test_fusion_delta_uses_frozen_abbreviations_and_retains_all_24_overlays() -> None:
    methods = ["Equal Weight", "Minimum Variance", "Maximum Sharpe", "Risk Parity"]
    records = []
    for base_fund_id in FUSION_BASE_LABELS:
        family = "Equity" if base_fund_id.startswith("equity_") else "Combined"
        method = methods[list(FUSION_BASE_LABELS).index(base_fund_id) % 4]
        for index, variant in enumerate(VARIANTS):
            records.append(
                {
                    "base_fund_id": base_fund_id,
                    "family": family,
                    "method": method,
                    "variant": variant,
                    "delta_net_annualised_return": [-0.002, 0.003, -0.001][index],
                    "delta_net_sharpe_ratio": [-0.01, 0.02, -0.005][index],
                }
            )
    figure = fusion_delta_chart(pd.DataFrame(records))
    try:
        observed = tuple(label.get_text() for label in figure.axes[1].get_xticklabels())
        assert observed == tuple(FUSION_BASE_LABELS.values())
        assert sum(len(axis.patches) for axis in figure.axes) == 48
        assert any("Eq = Equity; Comb = Combined" in text.get_text() for text in figure.texts)
    finally:
        plt.close(figure)


def test_sector_exposure_uses_display_only_communication_and_real_estate_names() -> None:
    raw = pd.DataFrame(
        {
            "sector": ["Comm", "RealEstate", "Utilities"],
            "hit_share": [0.10, 0.20, 0.30],
        }
    )
    figure = sector_term_exposure_chart(raw)
    try:
        labels = {label.get_text() for label in figure.axes[0].get_yticklabels()}
        assert SECTOR_DISPLAY_NAMES == {"Comm": "Comm/Telecom", "RealEstate": "Real Estate"}
        assert {"Comm/Telecom", "Real Estate", "Utilities"} == labels
        assert "Comm" not in labels and "RealEstate" not in labels
        assert raw["sector"].tolist() == ["Comm", "RealEstate", "Utilities"]
    finally:
        plt.close(figure)
