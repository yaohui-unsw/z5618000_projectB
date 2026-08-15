"""MAIA — Multi-Asset Investment Assistant.

This deployed surface is deliberately downstream-only: it reads validated,
precomputed Project B artifacts and performs lightweight display or allocation
arithmetic. It never loads raw data or executes an analytical model.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

st.set_page_config(
    page_title="MAIA | Multi-Asset Investment Assistant",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.app_charts import (  # noqa: E402
    allocation_wealth_chart,
    asset_class_chart,
    drawdown_chart,
    fusion_delta_chart,
    fusion_tradeoff_chart,
    growth_chart,
    holdings_chart,
    market_tone_chart,
    risk_return_chart,
    sector_sentiment_chart,
    sector_term_exposure_chart,
)
from src.app_data import (  # noqa: E402
    ArtifactError,
    FUND_IDS,
    SECTOR_ORDER,
    load_base_metrics,
    load_fund_returns,
    load_fund_weights,
    load_fusion_evidence,
    load_implementation_evidence,
    load_sentiment_evidence,
)
from src.app_logic import (  # noqa: E402
    AppLogicError,
    MANAGEMENT_FEE_RATE,
    METHOD_DESCRIPTIONS,
    allocation_performance_metrics,
    allocation_table,
    asset_class_exposures,
    build_allocation_history,
    complete_fusion_table,
    current_holdings_date,
    diagnostic_value,
    equal_split_percentages,
    fund_name_map,
    fusion_comparison_summary,
    growth_and_drawdown,
    growth_of_one,
    latest_target_holdings,
    market_sentiment_pulse,
    rolling_sentiment_summary,
    validate_user_allocation,
)


DISCLAIMER = "Historical out-of-sample illustration only. This is not a forecast, recommendation, or guarantee."
NAV_ITEMS = (
    "Explore Funds",
    "Fund Fact Sheet",
    "Allocation Studio",
    "Sentiment & Innovation",
    "Methodology & Disclosures",
)


st.markdown(
    """
    <style>
    :root { --maia-navy:#102A43; --maia-teal:#138A8A; --maia-orange:#E98324; }
    /* Shared safe area below Streamlit's fixed toolbar for every MAIA page. */
    .block-container {
        padding-top: clamp(4.25rem, 8vh, 5rem);
        padding-bottom: 3rem;
        max-width: 1280px;
    }
    @media (max-width: 768px) {
        .block-container { padding-top: 4.75rem; }
    }
    [data-testid="stSidebar"] { border-right: 1px solid #dfe7ee; }
    .maia-kicker { color:#138A8A; font-size:.78rem; font-weight:700; letter-spacing:.10em; text-transform:uppercase; }
    .maia-title { color:#102A43; font-size:2.2rem; font-weight:760; line-height:1.05; margin:.15rem 0 .2rem 0; }
    .maia-subtitle { color:#486581; font-size:1.05rem; max-width:900px; margin-bottom:.8rem; }
    .maia-disclaimer { background:#f4f7fa; border-left:4px solid #138A8A; color:#334E68; padding:.72rem .9rem; margin:.5rem 0 1.1rem 0; }
    .maia-note { color:#526879; font-size:.88rem; }
    h1, h2, h3 { color:#102A43; }
    div[data-testid="stMetric"] { background:#f7f9fb; border:1px solid #e2e8ee; padding:.75rem; border-radius:.45rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


def _header(section: str, lead: str) -> None:
    st.markdown('<div class="maia-kicker">MAIA · Multi-Asset Investment Assistant</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="maia-title">{section}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="maia-subtitle">{lead}</div>', unsafe_allow_html=True)


def _disclaimer() -> None:
    st.markdown(f'<div class="maia-disclaimer">{DISCLAIMER}</div>', unsafe_allow_html=True)


def _show_figure(figure: plt.Figure) -> None:
    st.pyplot(figure, clear_figure=True, width="stretch")
    plt.close(figure)


def _format_base_metrics(metrics: pd.DataFrame, names: dict[str, str]) -> pd.DataFrame:
    columns = [
        "fund_id", "family", "method", "start_date", "end_date",
        "net_annualised_return", "net_annualised_volatility",
        "net_sharpe_ratio", "net_max_drawdown", "average_rebalance_turnover",
    ]
    table = metrics.loc[:, columns].copy(deep=True)
    table.insert(0, "Fund", table["fund_id"].map(names))
    percent_columns = [
        "net_annualised_return", "net_annualised_volatility",
        "net_max_drawdown", "average_rebalance_turnover",
    ]
    table.loc[:, percent_columns] = table.loc[:, percent_columns] * 100.0
    return table.drop(columns="fund_id")


def render_explore_funds() -> None:
    _header(
        "Explore Funds",
        "Compare twelve systematic Equity, Crypto and Combined funds using transparent out-of-sample evidence and news-sentiment analytics.",
    )
    _disclaimer()
    metrics = load_base_metrics()
    names = fund_name_map(metrics)

    c1, c2, c3 = st.columns(3)
    c1.metric("Frozen base funds", f"{metrics['fund_id'].nunique()}")
    c2.metric("Fund families", f"{metrics['family'].nunique()}")
    c3.metric("Methods per family", f"{metrics['method'].nunique()}")
    st.caption("Primary performance uses canonical net returns after the frozen 5-bps one-way-turnover transaction cost.")

    st.subheader("Complete fund comparison")
    st.dataframe(
        _format_base_metrics(metrics, names),
        hide_index=True,
        width="stretch",
        height=470,
        column_config={
            "start_date": st.column_config.DateColumn("OOS start"),
            "end_date": st.column_config.DateColumn("OOS end"),
            "net_annualised_return": st.column_config.NumberColumn("Net ann. return", format="%.2f%%"),
            "net_annualised_volatility": st.column_config.NumberColumn("Ann. volatility", format="%.2f%%"),
            "net_sharpe_ratio": st.column_config.NumberColumn("Net Sharpe", format="%.3f"),
            "net_max_drawdown": st.column_config.NumberColumn("Max drawdown", format="%.2f%%"),
            "average_rebalance_turnover": st.column_config.NumberColumn("Avg. turnover", format="%.2f%%"),
        },
    )
    st.caption("The table always retains all 12 funds. Filters below affect only the risk-return view.")

    f1, f2 = st.columns(2)
    families = f1.multiselect("Risk-return families", ["Equity", "Crypto", "Combined"], default=["Equity", "Crypto", "Combined"])
    methods = f2.multiselect("Risk-return methods", list(METHOD_DESCRIPTIONS), default=list(METHOD_DESCRIPTIONS))
    filtered = metrics.loc[metrics["family"].isin(families) & metrics["method"].isin(methods)]
    if filtered.empty:
        st.info("Choose at least one family and method to display the risk-return map.")
    else:
        _show_figure(risk_return_chart(filtered))

    st.subheader("Compare historical growth")
    default_funds = [fund for fund in FUND_IDS if fund.startswith("combined_")]
    selected = st.multiselect(
        "Select up to four funds",
        list(FUND_IDS),
        default=default_funds,
        max_selections=4,
        format_func=lambda fund: names[fund],
    )
    if selected:
        returns = load_fund_returns()
        paths = growth_of_one(returns.loc[returns["fund_id"].isin(selected)])
        _show_figure(growth_chart(paths, names))
    else:
        st.info("Select at least one fund to draw a historical growth path.")

    with st.expander("How the four methods differ", expanded=False):
        for method, description in METHOD_DESCRIPTIONS.items():
            st.markdown(f"**{method}:** {description}")


def render_fact_sheet() -> None:
    _header("Fund Fact Sheet", "Inspect one frozen base fund, its historical risk path, and its latest target holdings.")
    _disclaimer()
    metrics = load_base_metrics()
    names = fund_name_map(metrics)
    fund_id = st.selectbox("Explore a fund", list(FUND_IDS), format_func=lambda fund: names[fund])
    row = metrics.loc[metrics["fund_id"].eq(fund_id)].iloc[0]

    st.subheader(names[fund_id])
    st.caption(f"{row['family']} family · {row['method']} method · OOS {row['start_date']:%d %b %Y} to {row['end_date']:%d %b %Y}")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Annualised net return", f"{row['net_annualised_return']:.2%}")
    k2.metric("Annualised net volatility", f"{row['net_annualised_volatility']:.2%}")
    k3.metric("Net Sharpe ratio", f"{row['net_sharpe_ratio']:.3f}")
    k4.metric("Net maximum drawdown", f"{row['net_max_drawdown']:.2%}")

    returns = load_fund_returns()
    path = growth_and_drawdown(returns.loc[returns["fund_id"].eq(fund_id)])
    st.metric("Final net growth of $1", f"${path['growth'].iloc[-1]:,.3f}")
    _show_figure(growth_chart(path, names))
    _show_figure(drawdown_chart(path, names[fund_id]))

    weights = load_fund_weights()
    latest = latest_target_holdings(weights, fund_id)
    holdings_date = current_holdings_date(latest)
    st.subheader("Current target holdings")
    st.caption(f"Latest frozen target rebalance: {holdings_date:%d %b %Y}. Current means the latest target in this historical dataset, not a live holding.")
    h1, h2 = st.columns([1.6, 1.0])
    with h1:
        _show_figure(holdings_chart(latest))
    with h2:
        st.metric("Number of holdings", f"{len(latest)}")
        st.metric("Target-weight sum", f"{latest['target_weight'].sum():.2%}")
        if row["family"] == "Combined":
            _show_figure(asset_class_chart(asset_class_exposures(latest)))
    complete = latest.loc[:, ["ticker", "asset_class", "target_weight"]].copy(deep=True)
    complete["target_weight"] = complete["target_weight"] * 100.0
    st.dataframe(
        complete,
        hide_index=True,
        width="stretch",
        height=360,
        column_config={"target_weight": st.column_config.NumberColumn("Target weight", format="%.3f%%")},
    )

    window = 365 if row["family"] == "Crypto" else 252
    st.subheader("Fund operating terms")
    details = pd.DataFrame(
        {
            "Term": ["Rebalance", "Estimation window", "Constraints", "Risk-free rate", "Trading cost", "Average turnover", "Total turnover"],
            "Frozen specification": [
                "Monthly — first observed eligible date",
                f"Rolling {window} complete strictly prior observations",
                "Long-only, fully invested, 20% per-asset cap",
                "0%",
                f"{row['transaction_cost_bps']:.0f} bps per unit of one-way turnover",
                f"{row['average_rebalance_turnover']:.2%}",
                f"{row['total_turnover']:.2f}",
            ],
        }
    )
    st.dataframe(details, hide_index=True, width="stretch")
    with st.expander("How this fund works"):
        st.write(METHOD_DESCRIPTIONS[str(row["method"])])
        st.write("Weights are estimated from strictly prior observations, applied on monthly rebalance dates, and allowed to drift with realised asset returns between rebalances.")
        st.write("The displayed evidence is historical and out of sample under the frozen design; it is not an expected-return forecast.")


def render_allocation_studio() -> None:
    _header("Allocation Studio", "Build a one-time allocation across MAIA funds and inspect a strictly historical account illustration.")
    _disclaimer()
    st.info("The canonical fund net returns already include the frozen 5-bps turnover cost. MAIA does not apply that cost twice.")
    metrics = load_base_metrics()
    names = fund_name_map(metrics)
    initial_capital = st.number_input("Initial capital ($)", min_value=1_000.0, max_value=10_000_000.0, value=10_000.0, step=1_000.0)
    defaults = [fund for fund in FUND_IDS if fund.startswith("combined_")]
    selected = st.multiselect(
        "Choose two to four base funds",
        list(FUND_IDS),
        default=defaults,
        max_selections=4,
        format_func=lambda fund: names[fund],
        key="allocation_funds",
    )
    if st.button("Equal split", width="content"):
        for fund, value in equal_split_percentages(selected).items():
            st.session_state[f"allocation_{fund}"] = int(value)

    allocations: dict[str, float] = {}
    if 2 <= len(selected) <= 4:
        default_split = equal_split_percentages(selected)
        columns = st.columns(len(selected))
        for column, fund in zip(columns, selected):
            key = f"allocation_{fund}"
            if key not in st.session_state:
                st.session_state[key] = int(default_split[fund])
            with column:
                allocations[fund] = float(st.select_slider(names[fund], options=list(range(5, 101, 5)), key=key, format_func=lambda value: f"{value}%"))

    validation = validate_user_allocation(selected, allocations) if 2 <= len(selected) <= 4 else None
    total = validation.total_percent if validation is not None else 0.0
    if validation is not None and validation.valid:
        st.success(f"Total allocation: {total:.0f}% — valid")
    else:
        message = validation.message if validation is not None else "Choose between two and four base funds."
        st.warning(f"Total allocation: {total:.0f}% — {message}")
        return

    fund_returns = load_fund_returns()
    history, calendar = build_allocation_history(fund_returns, selected, allocations, initial_capital)
    account_metrics = allocation_performance_metrics(history, initial_capital=initial_capital, annualisation=calendar.annualisation)
    st.caption(f"Common historical period: {calendar.start_date:%d %b %Y} to {calendar.end_date:%d %b %Y}. {calendar.calendar_label}.")
    _show_figure(allocation_wealth_chart(history))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ending value after fee", f"${account_metrics['ending_value_after_fee']:,.2f}")
    c2.metric("Historical total return after fee", f"{account_metrics['total_return_after_fee']:.2%}")
    c3.metric("Annualised return after fee", f"{account_metrics['annualised_return_after_fee']:.2%}")
    c4.metric("Annualised volatility after fee", f"{account_metrics['annualised_volatility_after_fee']:.2%}")
    c5, c6, c7 = st.columns(3)
    c5.metric("Sharpe ratio after fee", f"{account_metrics['sharpe_ratio_after_fee']:.3f}")
    c6.metric("Maximum drawdown after fee", f"{account_metrics['max_drawdown_after_fee']:.2%}")
    c7.metric("Illustrative fee drag", f"${account_metrics['management_fee_drag_dollars']:,.2f}")
    st.caption(f"Illustrative management fee: {MANAGEMENT_FEE_RATE:.2%} p.a., applied to account wealth by elapsed calendar time. This is separate from the canonical portfolio model.")
    st.dataframe(
        allocation_table(selected, allocations, initial_capital, names),
        hide_index=True,
        width="stretch",
        column_config={
            "allocation_percent": st.column_config.NumberColumn("Allocation", format="%.0f%%"),
            "initial_dollars": st.column_config.NumberColumn("Initial dollars", format="$%.2f"),
        },
    )
    st.markdown(f"**{DISCLAIMER}**")


def render_sentiment_innovation() -> None:
    _header("Sentiment & Innovation", "Inspect precomputed Finance-VADER evidence and all frozen base-versus-overlay comparisons without selective omission.")
    _disclaimer()
    sector, diagnostics, lexicon = load_sentiment_evidence()
    fusion_metrics, comparison = load_fusion_evidence()
    base_metrics = load_base_metrics()

    st.subheader("Market Sentiment Pulse")
    pulse = market_sentiment_pulse(sector)
    latest = pulse.iloc[-1]
    p1, p2, p3 = st.columns(3)
    p1.metric("Latest 21-day market tone", f"{latest['rolling_21']:+.3f}")
    p2.metric("Latest source date", f"{latest['date']:%d %b %Y}")
    p3.metric("Numeric scale", "−1 to +1")
    _show_figure(market_tone_chart(pulse))
    st.caption("Finance-VADER market tone is a display-only cross-sector summary. The 21-trading-day mean is visual smoothing and was never used for trading.")

    st.subheader("Sector sentiment")
    display_map = sector.loc[:, ["sector", "sector_display"]].drop_duplicates().set_index("sector")["sector_display"].to_dict()
    selected_sectors = st.multiselect("Select sectors", list(SECTOR_ORDER), default=["Tech", "Financials", "Energy"], format_func=lambda value: display_map.get(value, value))
    if selected_sectors:
        summary = rolling_sentiment_summary(sector, selected_sectors)
        _show_figure(sector_sentiment_chart(summary))
    else:
        st.info("Select at least one sector to display its precomputed Finance-VADER series.")
    st.caption("No-news observations remain missing rather than neutral. Crypto has no news sentiment input.")

    st.subheader("Student-reviewed finance lexicon")
    custom_hit = diagnostic_value(diagnostics, "headline", "all", "finance_vader", "custom_finance_term_hit_share")
    changed = diagnostic_value(diagnostics, "headline", "all", "plain_to_finance", "changed_score_share")
    plain_zero = diagnostic_value(diagnostics, "headline", "all", "plain_vader", "exact_zero_rate")
    finance_zero = diagnostic_value(diagnostics, "headline", "all", "finance_vader", "exact_zero_rate")
    plain_neutral = diagnostic_value(diagnostics, "headline", "all", "plain_vader", "neutral_band_rate")
    finance_neutral = diagnostic_value(diagnostics, "headline", "all", "finance_vader", "neutral_band_rate")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Custom-term hit share", f"{custom_hit:.2%}")
    d2.metric("Headline scores changed", f"{changed:.2%}")
    d3.metric("Plain exact zero / neutral band", f"{plain_zero:.2%} / {plain_neutral:.2%}")
    d4.metric("Finance exact zero / neutral band", f"{finance_zero:.2%} / {finance_neutral:.2%}")
    st.dataframe(
        lexicon.loc[:, ["term", "approved_finance_value", "candidate_class", "student_decision", "rationale"]],
        hide_index=True, width="stretch", height=420,
        column_config={"approved_finance_value": st.column_config.NumberColumn("Approved value", format="%+.1f")},
    )
    sector_rates = diagnostics.loc[
        diagnostics["scope"].eq("sector") & diagnostics["metric"].eq("custom_finance_term_hit_share"),
        ["entity", "value"],
    ].rename(columns={"entity": "sector", "value": "hit_share"})
    _show_figure(sector_term_exposure_chart(sector_rates))
    st.warning("Term exposure is not contextual accuracy. Higher Finance-VADER zero/neutral rates partly reflect intentional neutralisation of generic finance words with inappropriate vanilla polarity; this does not imply lower information coverage. Utilities and Energy are exposure concentrations, not proof of greater sentiment accuracy.")

    st.subheader("Fusion evidence")
    summary = fusion_comparison_summary(comparison)
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Finance Sharpe > base", f"{summary['finance_positive_sharpe']} of 8")
    a2.metric("Plain Sharpe > base", f"{summary['plain_positive_sharpe']} of 8")
    a3.metric("Evidence-aware Sharpe > base", f"{summary['evidence_positive_sharpe']} of 8")
    a4.metric("Finance Sharpe > Plain", f"{summary['finance_beats_plain_sharpe']} of 8")
    st.write(
        f"Evidence-aware Finance reduced average rebalance turnover in **{summary['evidence_lower_turnover']} of 8** paired comparisons, "
        f"but had lower annualised return in **{summary['evidence_lower_return']} of 8** and lower Sharpe in **{summary['evidence_lower_sharpe']} of 8** than naive Finance VADER."
    )
    st.caption(
        f"Strongest observed Sharpe delta: {summary['strongest_overlay']} ({summary['strongest_sharpe_delta']:+.4f}). "
        f"Weakest: {summary['weakest_overlay']} ({summary['weakest_sharpe_delta']:+.4f}). These are descriptive frozen-sample observations."
    )
    _show_figure(fusion_delta_chart(comparison))
    _show_figure(fusion_tradeoff_chart(comparison))
    complete = complete_fusion_table(comparison, fusion_metrics, base_metrics)
    display_columns = [
        "base_fund_display", "variant_display", "base_net_annualised_return",
        "overlay_net_annualised_return", "delta_net_annualised_return",
        "base_net_sharpe_ratio", "overlay_net_sharpe_ratio",
        "delta_net_sharpe_ratio", "delta_average_turnover",
    ]
    st.dataframe(complete.loc[:, display_columns], hide_index=True, width="stretch", height=520)
    st.info("All 24 overlays and every negative result are retained. No prespecified statistical significance test was conducted; these comparisons are descriptive, not causal.")


def render_methodology() -> None:
    _header("Methodology & Disclosures", "A concise account of what MAIA's historical evidence does—and does not—represent.")
    _disclaimer()
    st.subheader("Customer journey")
    st.write("MAIA is for a financially curious retail investor who wants to compare systematic multi-asset funds, inspect one fund, build a historical fund-level allocation, and understand the sentiment innovation without reading Python code.")
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(
            """
            **Portfolio foundation**

            - 12 funds: Equity, Crypto and Combined; four methods per family.
            - Rolling 252-observation windows for Equity/Combined and 365 for Crypto.
            - Monthly rebalancing using information strictly before each decision date.
            - Long-only, fully invested, 20% per-asset cap and zero risk-free rate.
            - Native seven-day Crypto returns; holdings drift between rebalances.
            - 5-bps transaction cost per unit of one-way turnover.
            """
        )
    with m2:
        st.markdown(
            """
            **Sentiment and fusion**

            - Plain VADER plus a 23-term student-reviewed finance lexicon.
            - No Crypto news; no news is different from scored-neutral news.
            - Past-only standardisation and one-observed-trading-day lag.
            - Fixed sentiment tilt strength, lambda = 0.10.
            - 24 monthly Equity/Combined overlays; no Crypto-only overlay.
            - Reliability is a coverage/agreement diagnostic, not truth or news quality.
            """
        )
    st.subheader("Important limitations")
    st.markdown(
        """
        - The 69 extreme returns remain in canonical base results; the separate ±25% scenario is robustness evidence, not corrected data.
        - Short headlines can be ambiguous, ticker attribution can be imperfect, and reviewed-term exposure is not contextual accuracy.
        - No prespecified significance test was conducted, and the frozen sample cannot establish causality or universal validity.
        - Historical out-of-sample evidence is not a forecast, personalised advice, or a guarantee.
        """
    )
    with st.expander("Implementation and robustness evidence"):
        solver, sensitivity = load_implementation_evidence()
        st.write("Solver diagnostics (all fund-rebalance records)")
        st.dataframe(
            solver.loc[:, ["date", "fund_id", "method", "solver_success", "attempts", "retry_used", "sum_residual", "upper_bound_violation"]],
            hide_index=True, width="stretch", height=300,
        )
        st.write("Separately labelled ±25% extreme-return sensitivity")
        st.dataframe(sensitivity, hide_index=True, width="stretch", height=300)
        st.caption("This evidence is bounded and historical. Large movements were retained in the canonical data, and the scenario did not replace canonical results.")
    st.caption("MAIA is a portfolio-management interface. It offers no account, bank funding, order execution, live price, or personalised-advice capability.")


with st.sidebar:
    st.markdown("## MAIA")
    st.caption("Multi-Asset Investment Assistant")
    page = st.radio("Navigate", NAV_ITEMS, index=0)
    st.divider()
    st.caption("Precomputed evidence only · no live model execution")


try:
    if page == "Explore Funds":
        render_explore_funds()
    elif page == "Fund Fact Sheet":
        render_fact_sheet()
    elif page == "Allocation Studio":
        render_allocation_studio()
    elif page == "Sentiment & Innovation":
        render_sentiment_innovation()
    else:
        render_methodology()
except (ArtifactError, AppLogicError, ValueError) as exc:
    st.error(f"MAIA cannot display this section because a validated artifact or input is unavailable: {exc}")
    st.caption("No placeholder value was substituted. Restore or verify the named precomputed artifact and retry.")
