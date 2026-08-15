"""Lightweight, display-only charts for the MAIA Streamlit application.

The functions accept defensive data-frame copies and return Matplotlib figure
objects. They do not read files, execute models, or save figures.
"""
from __future__ import annotations

from collections.abc import Mapping

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import pandas as pd

from src.app_logic import VARIANT_LABELS


NAVY = "#102A43"
CHARCOAL = "#334E68"
TEAL = "#138A8A"
ORANGE = "#E98324"
BLUE = "#2F6BBD"
GREEN = "#4C956C"
GREY = "#7B8794"
LIGHT = "#E8EEF3"

METHOD_COLOURS = {
    "Equal Weight": GREY,
    "Minimum Variance": BLUE,
    "Maximum Sharpe": ORANGE,
    "Risk Parity": GREEN,
}
VARIANT_COLOURS = {
    "plain_vader_naive": BLUE,
    "finance_vader_naive": ORANGE,
    "evidence_aware_finance": TEAL,
}
FUND_METHOD_SUFFIXES = {
    "_equal_weight": "Equal Weight",
    "_minimum_variance": "Minimum Variance",
    "_maximum_sharpe": "Maximum Sharpe",
    "_risk_parity": "Risk Parity",
}
FUND_SHORT_LABELS = {
    "equity_equal_weight": "Eq/EW",
    "equity_minimum_variance": "Eq/MV",
    "equity_maximum_sharpe": "Eq/MS",
    "equity_risk_parity": "Eq/RP",
    "crypto_equal_weight": "Cr/EW",
    "crypto_minimum_variance": "Cr/MV",
    "crypto_maximum_sharpe": "Cr/MS",
    "crypto_risk_parity": "Cr/RP",
    "combined_equal_weight": "Comb/EW",
    "combined_minimum_variance": "Comb/MV",
    "combined_maximum_sharpe": "Comb/MS",
    "combined_risk_parity": "Comb/RP",
}
FUSION_BASE_LABELS = {
    fund_id: label
    for fund_id, label in FUND_SHORT_LABELS.items()
    if fund_id.startswith(("equity_", "combined_"))
}
RISK_RETURN_LABEL_OFFSETS = {
    "equity_equal_weight": (-42, -13),
    "equity_minimum_variance": (-44, 32),
    "equity_maximum_sharpe": (10, -14),
    "equity_risk_parity": (-43, 8),
    "crypto_equal_weight": (-42, -3),
    "crypto_minimum_variance": (-42, 10),
    "crypto_maximum_sharpe": (-42, -13),
    "crypto_risk_parity": (8, 8),
    "combined_equal_weight": (9, -10),
    "combined_minimum_variance": (-50, -13),
    "combined_maximum_sharpe": (9, 7),
    "combined_risk_parity": (9, 7),
}
SECTOR_DISPLAY_NAMES = {
    "Comm": "Comm/Telecom",
    "RealEstate": "Real Estate",
}


def _style_axis(ax: plt.Axes, *, zero: bool = False) -> None:
    ax.set_facecolor("white")
    ax.grid(axis="y", color=LIGHT, linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#B8C4CE")
    ax.tick_params(colors=CHARCOAL, labelsize=9)
    if zero:
        ax.axhline(0.0, color=CHARCOAL, linewidth=0.9, zorder=1)


def _finish(fig: Figure, title: str, subtitle: str = "") -> Figure:
    fig.patch.set_facecolor("white")
    fig.suptitle(title, x=0.06, y=0.975, ha="left", color=NAVY, fontsize=15, fontweight="bold")
    if subtitle:
        fig.text(0.06, 0.925, subtitle, ha="left", va="top", color=CHARCOAL, fontsize=8.8, linespacing=1.3)
    subtitle_lines = subtitle.count("\n") + 1 if subtitle else 0
    top = 0.87 - max(subtitle_lines - 1, 0) * 0.035 if subtitle else 0.92
    fig.tight_layout(rect=(0.03, 0.025, 0.99, top))
    return fig


def fund_method(fund_id: str) -> str:
    """Return the frozen method for a deterministic base-fund ID."""
    for suffix, method in FUND_METHOD_SUFFIXES.items():
        if fund_id.endswith(suffix):
            return method
    raise ValueError(f"Unsupported MAIA base-fund ID '{fund_id}'.")


def risk_return_chart(metrics: pd.DataFrame) -> Figure:
    required = {"fund_id", "family", "method", "net_annualised_return", "net_annualised_volatility", "net_sharpe_ratio"}
    if not required.issubset(metrics.columns):
        raise ValueError(f"Risk-return data are missing {sorted(required - set(metrics.columns))}.")
    work = metrics.loc[:, list(required)].copy(deep=True)
    fig, ax = plt.subplots(figsize=(8.2, 5.1))
    family_markers = {"Equity": "o", "Crypto": "^", "Combined": "s"}
    for row in work.itertuples(index=False):
        ax.scatter(
            row.net_annualised_volatility * 100.0,
            row.net_annualised_return * 100.0,
            color=METHOD_COLOURS.get(row.method, GREY),
            marker=family_markers.get(row.family, "o"),
            s=52 + 20 * min(abs(float(row.net_sharpe_ratio)), 2.0),
            edgecolor="white", linewidth=0.8, zorder=3,
        )
        fund_id = str(row.fund_id)
        if fund_id not in FUND_SHORT_LABELS:
            raise ValueError(f"Unsupported MAIA base-fund ID '{fund_id}'.")
        ax.annotate(
            FUND_SHORT_LABELS[fund_id],
            (row.net_annualised_volatility * 100.0, row.net_annualised_return * 100.0),
            xytext=RISK_RETURN_LABEL_OFFSETS[fund_id], textcoords="offset points",
            fontsize=7.4, color=CHARCOAL, ha="left", va="center",
            arrowprops={"arrowstyle": "-", "color": "#9AA9B5", "linewidth": 0.55},
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.78, "pad": 0.6},
            annotation_clip=False, zorder=4,
        )
    ax.margins(x=0.10, y=0.12)
    ax.set_xlabel("Annualised net volatility (%)", color=CHARCOAL)
    ax.set_ylabel("Annualised net return (%)", color=CHARCOAL)
    _style_axis(ax, zero=True)
    return _finish(
        fig,
        "Historical risk and return",
        "All 12 frozen base funds · net of the 5-bps turnover cost\n"
        "Labels: Eq/Cr/Comb = Equity/Crypto/Combined\n"
        "Methods: EW = Equal Weight; MV = Minimum Variance; MS = Maximum Sharpe; RP = Risk Parity",
    )


def growth_chart(paths: pd.DataFrame, names: Mapping[str, str]) -> Figure:
    required = {"date", "fund_id", "growth"}
    if not required.issubset(paths.columns):
        raise ValueError("Growth paths are incomplete.")
    work = paths.loc[:, list(required)].copy(deep=True)
    work["date"] = pd.to_datetime(work["date"])
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    for fund_id, group in work.groupby("fund_id", sort=False):
        method = fund_method(str(fund_id))
        ax.plot(group["date"], group["growth"], linewidth=1.8,
                label=names.get(str(fund_id), str(fund_id)),
                color=METHOD_COLOURS[method])
    ax.axhline(1.0, color=CHARCOAL, linewidth=0.9, linestyle=":")
    ax.set_ylabel("Growth of $1 (net)", color=CHARCOAL)
    ax.set_xlabel("Date", color=CHARCOAL)
    locator = mdates.AutoDateLocator(minticks=4, maxticks=8)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    ax.legend(frameon=False, fontsize=8, ncol=2, loc="best")
    _style_axis(ax)
    return _finish(fig, "Growth of $1", "Historical out-of-sample paths · canonical net returns")


def drawdown_chart(path: pd.DataFrame, fund_name: str) -> Figure:
    if not {"date", "drawdown"}.issubset(path.columns):
        raise ValueError("Drawdown path is incomplete.")
    work = path.loc[:, ["date", "drawdown"]].copy(deep=True)
    fig, ax = plt.subplots(figsize=(8.6, 3.7))
    dates = pd.to_datetime(work["date"])
    values = work["drawdown"].to_numpy(dtype="float64") * 100.0
    ax.fill_between(dates, values, 0.0, color=TEAL, alpha=0.32)
    ax.plot(dates, values, color=TEAL, linewidth=1.4)
    ax.set_ylabel("Drawdown (%)", color=CHARCOAL)
    ax.set_xlabel("Date", color=CHARCOAL)
    _style_axis(ax, zero=True)
    return _finish(fig, "Historical drawdown", f"{fund_name} · recomputed from canonical net returns")


def holdings_chart(holdings: pd.DataFrame, *, top_n: int = 10) -> Figure:
    if not {"ticker", "target_weight"}.issubset(holdings.columns):
        raise ValueError("Holdings data are incomplete.")
    work = holdings.nlargest(top_n, "target_weight").sort_values("target_weight", kind="mergesort")
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.barh(work["ticker"], work["target_weight"] * 100.0, color=TEAL)
    ax.set_xlabel("Latest target weight (%)", color=CHARCOAL)
    _style_axis(ax)
    return _finish(fig, "Largest current target holdings", f"Top {min(top_n, len(work))}; complete holdings remain in the table")


def asset_class_chart(exposure: pd.DataFrame) -> Figure:
    if not {"asset_class", "target_weight"}.issubset(exposure.columns):
        raise ValueError("Asset-class exposure is incomplete.")
    fig, ax = plt.subplots(figsize=(5.8, 3.5))
    ax.bar(exposure["asset_class"], exposure["target_weight"] * 100.0, color=[BLUE, ORANGE])
    ax.set_ylabel("Latest target exposure (%)", color=CHARCOAL)
    ax.set_ylim(0.0, 100.0)
    _style_axis(ax)
    return _finish(fig, "Equity and Crypto sleeves", "Latest frozen rebalance target")


def allocation_wealth_chart(history: pd.DataFrame) -> Figure:
    required = {"date", "before_management_fee", "after_management_fee"}
    if not required.issubset(history.columns):
        raise ValueError("Allocation history is incomplete.")
    work = history.loc[:, list(required)].copy(deep=True)
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    ax.plot(work["date"], work["before_management_fee"], color=CHARCOAL, linewidth=1.6, label="Before illustrative management fee")
    ax.plot(work["date"], work["after_management_fee"], color=ORANGE, linewidth=2.0, label="After 0.50% p.a. illustrative fee")
    ax.set_ylabel("Historical account value ($)", color=CHARCOAL)
    ax.set_xlabel("Date", color=CHARCOAL)
    ax.legend(frameon=False, fontsize=8)
    _style_axis(ax)
    return _finish(fig, "One-time fund allocation", "Fund sleeves drift with canonical net performance; no user-level rebalancing")


def market_tone_chart(pulse: pd.DataFrame) -> Figure:
    required = {"date", "finance_vader_market_tone", "rolling_21"}
    if not required.issubset(pulse.columns):
        raise ValueError("Market-tone data are incomplete.")
    work = pulse.loc[:, list(required)].copy(deep=True)
    fig, ax = plt.subplots(figsize=(8.8, 4.3))
    ax.plot(work["date"], work["finance_vader_market_tone"], color=ORANGE, linewidth=0.7, alpha=0.25, label="Daily sector mean")
    ax.plot(work["date"], work["rolling_21"], color=ORANGE, linewidth=2.0, label="21-trading-day visual mean")
    ax.set_ylabel("Finance-VADER compound (−1 to +1)", color=CHARCOAL)
    ax.set_xlabel("Date", color=CHARCOAL)
    ax.set_ylim(-1.0, 1.0)
    ax.legend(frameon=False, fontsize=8)
    _style_axis(ax, zero=True)
    return _finish(fig, "Finance-VADER market tone", "Visual smoothing only · never used for trading")


def sector_sentiment_chart(summary: pd.DataFrame) -> Figure:
    required = {"date", "sector_display", "finance_compound", "rolling_21"}
    if not required.issubset(summary.columns):
        raise ValueError("Sector-sentiment data are incomplete.")
    work = summary.loc[:, list(required)].copy(deep=True)
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    colours = plt.colormaps["tab10"](np.linspace(0.0, 1.0, max(work["sector_display"].nunique(), 1)))
    for colour, (sector, group) in zip(colours, work.groupby("sector_display", sort=False)):
        ax.plot(group["date"], group["rolling_21"], label=str(sector), color=colour, linewidth=1.6)
    ax.set_ylabel("21-day Finance-VADER mean", color=CHARCOAL)
    ax.set_xlabel("Date", color=CHARCOAL)
    ax.set_ylim(-1.0, 1.0)
    ax.legend(frameon=False, fontsize=7.5, ncol=2, loc="best")
    _style_axis(ax, zero=True)
    return _finish(fig, "Sector sentiment", "Finance-VADER · 21-trading-day mean for display only · no Crypto news input")


def sector_term_exposure_chart(sector_rates: pd.DataFrame) -> Figure:
    if not {"sector", "hit_share"}.issubset(sector_rates.columns):
        raise ValueError("Sector term-exposure data are incomplete.")
    work = sector_rates.sort_values("hit_share", kind="mergesort")
    work["sector_display"] = work["sector"].map(SECTOR_DISPLAY_NAMES).fillna(work["sector"])
    fig, ax = plt.subplots(figsize=(7.8, 4.6))
    colours = [ORANGE if value in {"Utilities", "Energy"} else TEAL for value in work["sector"]]
    ax.barh(work["sector_display"], work["hit_share"] * 100.0, color=colours)
    ax.set_xlabel("Headlines with ≥1 reviewed finance term (%)", color=CHARCOAL)
    _style_axis(ax)
    return _finish(fig, "Reviewed-term exposure by sector", "Exposure is not contextual accuracy; Utilities and Energy are concentration risks")


def fusion_delta_chart(comparison: pd.DataFrame) -> Figure:
    required = {"base_fund_id", "family", "method", "variant", "delta_net_annualised_return", "delta_net_sharpe_ratio"}
    if not required.issubset(comparison.columns):
        raise ValueError("Fusion comparison data are incomplete.")
    work = comparison.loc[:, list(required)].copy(deep=True)
    bases = list(dict.fromkeys(work["base_fund_id"].astype(str)))
    variants = list(VARIANT_LABELS)
    x = np.arange(len(bases), dtype="float64")
    width = 0.24
    fig, axes = plt.subplots(2, 1, figsize=(10.0, 7.0), sharex=True)
    for index, variant in enumerate(variants):
        ordered = work.loc[work["variant"].eq(variant)].set_index("base_fund_id").reindex(bases)
        offset = (index - 1) * width
        axes[0].bar(x + offset, ordered["delta_net_annualised_return"] * 10_000.0, width, color=VARIANT_COLOURS[variant], label=VARIANT_LABELS[variant])
        axes[1].bar(x + offset, ordered["delta_net_sharpe_ratio"], width, color=VARIANT_COLOURS[variant])
    unsupported = [fund for fund in bases if fund not in FUSION_BASE_LABELS]
    if unsupported:
        raise ValueError(f"Unsupported fusion base-fund IDs: {unsupported}.")
    labels = [FUSION_BASE_LABELS[fund] for fund in bases]
    axes[0].set_ylabel("Annualised-return delta (bp)", color=CHARCOAL)
    axes[1].set_ylabel("Sharpe delta", color=CHARCOAL)
    axes[1].set_xticks(x, labels, rotation=0, fontsize=7.2)
    axes[0].legend(frameon=False, fontsize=8, ncol=3)
    for ax in axes:
        _style_axis(ax, zero=True)
    return _finish(
        fig,
        "Sentiment overlays versus frozen base funds",
        "All 24 overlays retained · delta = overlay minus corresponding base\n"
        "Eq = Equity; Comb = Combined; EW/MV/MS/RP = Equal Weight/Minimum Variance/Maximum Sharpe/Risk Parity",
    )


def fusion_tradeoff_chart(comparison: pd.DataFrame) -> Figure:
    required = {"base_fund_id", "variant", "delta_average_turnover", "delta_net_sharpe_ratio"}
    if not required.issubset(comparison.columns):
        raise ValueError("Fusion trade-off data are incomplete.")
    work = comparison.loc[:, list(required)].copy(deep=True)
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    for variant, group in work.groupby("variant", sort=False):
        ax.scatter(group["delta_average_turnover"] * 100.0, group["delta_net_sharpe_ratio"], color=VARIANT_COLOURS[variant], label=VARIANT_LABELS[variant], s=56, alpha=0.9)
    ax.set_xlabel("Incremental average rebalance turnover vs base (percentage points)", color=CHARCOAL)
    ax.set_ylabel("Sharpe delta vs base", color=CHARCOAL)
    ax.legend(frameon=False, fontsize=8)
    ax.axvline(0.0, color=CHARCOAL, linewidth=0.9)
    _style_axis(ax, zero=True)
    return _finish(fig, "Turnover and Sharpe trade-off", "Descriptive frozen-sample evidence; no significance test was prespecified")


__all__ = [
    "FUND_SHORT_LABELS", "FUSION_BASE_LABELS", "METHOD_COLOURS", "NAVY",
    "ORANGE", "RISK_RETURN_LABEL_OFFSETS", "SECTOR_DISPLAY_NAMES", "TEAL",
    "VARIANT_COLOURS",
    "allocation_wealth_chart", "asset_class_chart", "drawdown_chart",
    "fund_method", "fusion_delta_chart", "fusion_tradeoff_chart", "growth_chart",
    "holdings_chart", "market_tone_chart", "risk_return_chart",
    "sector_sentiment_chart", "sector_term_exposure_chart",
]
