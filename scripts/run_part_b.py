"""Run authorised, reproducible Project B stages from the project root."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
import tempfile

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.validate_data_contract import build_pipeline  # noqa: E402
from src import data_access  # noqa: E402
from src.fusion import (  # noqa: E402
    build_fusion_diagnostics,
    build_overlay_targets,
    run_fusion_suite,
)
from src.portfolio_validation import (  # noqa: E402
    FUND_RETURN_COLUMNS,
    FUND_WEIGHT_COLUMNS,
    PERFORMANCE_METRIC_COLUMNS,
    SENSITIVITY_COLUMNS,
    validate_portfolio_outputs,
)
from src.portfolios import (  # noqa: E402
    build_clipped_sensitivity_matrices,
    build_extreme_sensitivity_metrics,
    build_family_return_matrices,
    run_portfolio_suite,
)
from src.sentiment import (  # noqa: E402
    build_finance_lexicon_table,
    build_sector_sentiment_index,
    build_sentiment_diagnostics,
    build_ticker_sentiment_daily,
    create_vader_analyzers,
    score_headlines,
)
from src.sentiment_validation import validate_sentiment_fusion_outputs  # noqa: E402
from src.validation import (  # noqa: E402
    find_extreme_observations,
    validate_data_foundation,
    validate_deterministic_rerun,
)


OUTPUT_PATHS = {
    "fund_returns": PROJECT_ROOT / "results" / "data" / "fund_returns.csv",
    "fund_weights": PROJECT_ROOT / "results" / "data" / "fund_weights.csv",
    "performance_metrics": PROJECT_ROOT / "results" / "tables" / "performance_metrics.csv",
    "solver_diagnostics": PROJECT_ROOT / "results" / "tables" / "portfolio_solver_diagnostics.csv",
    "sensitivity_metrics": PROJECT_ROOT / "results" / "tables" / "extreme_sensitivity_metrics.csv",
}

SENTIMENT_FUSION_OUTPUT_PATHS = {
    "sector_sentiment_index": PROJECT_ROOT / "results" / "data" / "sector_sentiment_index.csv",
    "ticker_sentiment_daily": PROJECT_ROOT / "results" / "data" / "ticker_sentiment_daily.csv",
    "fusion_returns": PROJECT_ROOT / "results" / "data" / "fusion_returns.csv",
    "fusion_weights": PROJECT_ROOT / "results" / "data" / "fusion_weights.csv",
    "sentiment_diagnostics": PROJECT_ROOT / "results" / "tables" / "sentiment_diagnostics.csv",
    "finance_lexicon": PROJECT_ROOT / "results" / "tables" / "finance_lexicon.csv",
    "fusion_performance_metrics": PROJECT_ROOT / "results" / "tables" / "fusion_performance_metrics.csv",
    "fusion_comparison": PROJECT_ROOT / "results" / "tables" / "fusion_comparison.csv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stage",
        choices=("portfolios", "sentiment-fusion"),
        required=True,
        help="Run only the explicitly authorised Project B stage.",
    )
    parser.add_argument(
        "--with-extreme-sensitivity",
        action="store_true",
        help="Run the separately labelled ±25% native-return robustness scenario.",
    )
    return parser.parse_args()


def _load_and_validate_data() -> dict[str, pd.DataFrame]:
    raw_equity = data_access.load_equity_prices()
    raw_crypto = data_access.load_crypto_prices()
    raw_news = data_access.load_news_headlines()
    first = build_pipeline(raw_equity, raw_crypto, raw_news)
    second = build_pipeline(raw_equity, raw_crypto, raw_news)
    report = validate_data_foundation(
        project_root=PROJECT_ROOT,
        loader_path=Path(data_access.__file__),
        raw_equity=raw_equity,
        raw_crypto=raw_crypto,
        raw_news=raw_news,
        **first,
    )
    report.results.append(validate_deterministic_rerun(first, second))
    if not report.ok:
        codes = ", ".join(result.code for result in report.blocks)
        raise RuntimeError(f"data-contract validation blocked portfolio execution: {codes}")
    summary = report.to_dict()["summary"]
    print(
        "Data contract gate: "
        f"PASS={summary['PASS']} WARN={summary['WARN']} BLOCK={summary['BLOCK']}"
    )
    return first


def _select_columns(artifacts: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    selected = {
        "fund_returns": artifacts["fund_returns"].loc[:, list(FUND_RETURN_COLUMNS)],
        "fund_weights": artifacts["fund_weights"].loc[:, list(FUND_WEIGHT_COLUMNS)],
        "performance_metrics": artifacts["performance_metrics"].loc[:, list(PERFORMANCE_METRIC_COLUMNS)],
        "solver_diagnostics": artifacts["solver_diagnostics"],
    }
    return selected


def _write_outputs(
    canonical: dict[str, pd.DataFrame], sensitivity: pd.DataFrame
) -> None:
    for path in OUTPUT_PATHS.values():
        if not path.parent.is_dir():
            raise RuntimeError(f"expected starter output directory is absent: {path.parent}")
    canonical["fund_returns"].to_csv(OUTPUT_PATHS["fund_returns"], index=False)
    canonical["fund_weights"].to_csv(OUTPUT_PATHS["fund_weights"], index=False)
    canonical["performance_metrics"].to_csv(
        OUTPUT_PATHS["performance_metrics"], index=False
    )
    canonical["solver_diagnostics"].to_csv(
        OUTPUT_PATHS["solver_diagnostics"], index=False
    )
    sensitivity.to_csv(OUTPUT_PATHS["sensitivity_metrics"], index=False)


def _print_retry_evidence(label: str, artifacts: dict[str, pd.DataFrame]) -> None:
    """Expose every authorised retry attempt without creating another artifact."""
    diagnostics = artifacts["solver_diagnostics"]
    holdings = artifacts["fund_weights"]
    for row in diagnostics.loc[diagnostics["retry_used"]].itertuples():
        status_value = holdings.loc[
            holdings["date"].eq(row.date)
            & holdings["fund_id"].eq(row.fund_id),
            "solver_status",
        ].iloc[0]
        attempts = json.loads(status_value)["attempt_details"]
        for attempt in attempts:
            print(
                f"{label} solver attempt: date={pd.Timestamp(row.date).date()} "
                f"fund_id={row.fund_id} attempt={attempt['attempt']} "
                f"seed={attempt['initial_value']} success={attempt['success']} "
                f"valid={attempt['valid']} status={attempt['status_code']} "
                f"iterations={attempt['iterations']} message={attempt['message']}"
            )


def _read_accepted_portfolio_outputs() -> dict[str, pd.DataFrame]:
    """Read the immutable Stage 5A files without rerunning optimisation."""
    frames = {
        "fund_returns": pd.read_csv(OUTPUT_PATHS["fund_returns"], parse_dates=["date"]),
        "fund_weights": pd.read_csv(OUTPUT_PATHS["fund_weights"], parse_dates=["date"]),
        "performance_metrics": pd.read_csv(
            OUTPUT_PATHS["performance_metrics"], parse_dates=["start_date", "end_date"]
        ),
    }
    frames["fund_returns"]["is_rebalance"] = frames["fund_returns"][
        "is_rebalance"
    ].astype(bool)
    return frames


def _safe_write_sentiment_fusion_outputs(
    artifacts: dict[str, pd.DataFrame],
) -> None:
    """Stage all eight deterministic CSVs outside the project, then replace."""
    if set(artifacts) != set(SENTIMENT_FUSION_OUTPUT_PATHS):
        raise RuntimeError("sentiment/fusion artifact set differs from the frozen eight")
    for path in SENTIMENT_FUSION_OUTPUT_PATHS.values():
        if not path.parent.is_dir():
            raise RuntimeError(f"expected starter output directory is absent: {path.parent}")
    with tempfile.TemporaryDirectory(prefix="fins5545_stage6c_") as temporary:
        staged: dict[str, Path] = {}
        for name, frame in artifacts.items():
            path = Path(temporary) / SENTIMENT_FUSION_OUTPUT_PATHS[name].name
            frame.to_csv(
                path,
                index=False,
                date_format="%Y-%m-%d",
                na_rep="NA",
                lineterminator="\n",
                float_format="%.17g",
            )
            if not path.is_file() or path.stat().st_size == 0:
                raise RuntimeError(f"failed to stage substantive output: {name}")
            staged[name] = path
        for name, destination in SENTIMENT_FUSION_OUTPUT_PATHS.items():
            os.replace(staged[name], destination)


def _file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def run_sentiment_fusion() -> int:
    """Run only the accepted Stage 6C sentiment and overlay workflow."""
    pipeline = _load_and_validate_data()
    plain, finance = create_vader_analyzers()
    vanilla_snapshot = dict(plain.lexicon)
    scored = score_headlines(
        pipeline["mapped_headlines"],
        plain_analyzer=plain,
        finance_analyzer=finance,
    )
    plain_unchanged = plain.lexicon == vanilla_snapshot
    ticker_daily = build_ticker_sentiment_daily(
        scored, pipeline["coverage_panel"], enforce_contract_counts=True
    )
    sector_index, sector_custom = build_sector_sentiment_index(
        ticker_daily, enforce_contract_counts=True
    )
    lexicon = build_finance_lexicon_table()
    diagnostics = build_sentiment_diagnostics(
        scored,
        ticker_daily,
        sector_index,
        sector_custom,
        cleaned_headline_count=len(pipeline["news"]),
        unmapped_headline_count=int(
            pipeline["full_mapping"]["map_status"].eq("unmapped_end_of_sample").sum()
        ),
    )

    accepted = _read_accepted_portfolio_outputs()
    matrices = build_family_return_matrices(
        pipeline["equity_returns"], pipeline["crypto_returns"], pipeline["aligned_crypto"]
    )
    targets = build_overlay_targets(accepted["fund_weights"], ticker_daily)
    fusion = run_fusion_suite(
        targets,
        matrices,
        accepted["fund_returns"],
        accepted["performance_metrics"],
    )
    diagnostics = pd.concat(
        [diagnostics, build_fusion_diagnostics(fusion["fusion_weights"])],
        ignore_index=True,
    ).sort_values(["scope", "entity", "model", "metric"], kind="mergesort").reset_index(drop=True)
    artifacts = {
        "sector_sentiment_index": sector_index,
        "ticker_sentiment_daily": ticker_daily,
        "fusion_returns": fusion["fusion_returns"],
        "fusion_weights": fusion["fusion_weights"],
        "sentiment_diagnostics": diagnostics,
        "finance_lexicon": lexicon,
        "fusion_performance_metrics": fusion["fusion_performance_metrics"],
        "fusion_comparison": fusion["fusion_comparison"],
    }
    report = validate_sentiment_fusion_outputs(
        **artifacts,
        base_returns=accepted["fund_returns"],
        base_weights=accepted["fund_weights"],
        base_performance=accepted["performance_metrics"],
        family_matrices=matrices,
        plain_analyzer_unchanged=plain_unchanged,
    )
    if not report.ok:
        codes = ", ".join(result.code for result in report.blocks)
        raise RuntimeError(
            f"sentiment/fusion validation blocked all eight output writes: {codes}"
        )
    _safe_write_sentiment_fusion_outputs(artifacts)
    summary = report.to_dict()["summary"]
    print(
        "Sentiment/fusion in-memory validation: "
        f"PASS={summary['PASS']} WARN={summary['WARN']} BLOCK={summary['BLOCK']}"
    )
    print(
        "Canonical counts: mapped_headlines="
        f"{len(scored)} ticker_days={len(ticker_daily)} sector_days={len(sector_index)} "
        f"overlays={fusion['fusion_performance_metrics']['overlay_id'].nunique()}"
    )
    for name, path in SENTIMENT_FUSION_OUTPUT_PATHS.items():
        print(
            f"Output {name}: rows={len(artifacts[name])} "
            f"sha256={_file_sha256(path)}"
        )
    print("SENTIMENT-FUSION STAGE STATUS: PASS")
    return 0


def run_portfolios(*, with_extreme_sensitivity: bool) -> int:
    if not with_extreme_sensitivity:
        raise RuntimeError(
            "Stage 5A requires --with-extreme-sensitivity; no partial canonical write was made"
        )
    pipeline = _load_and_validate_data()
    equity_extremes = len(find_extreme_observations(pipeline["equity"]))
    crypto_extremes = len(find_extreme_observations(pipeline["crypto"]))
    if (equity_extremes, crypto_extremes) != (4, 65):
        raise RuntimeError(
            "extreme-return benchmark differs before portfolio execution: "
            f"equity={equity_extremes}, crypto={crypto_extremes}"
        )
    print(f"Extreme-return gate: equity={equity_extremes} crypto={crypto_extremes}")

    matrices = build_family_return_matrices(
        pipeline["equity_returns"],
        pipeline["crypto_returns"],
        pipeline["aligned_crypto"],
    )
    canonical = _select_columns(run_portfolio_suite(matrices))
    clipped_matrices = build_clipped_sensitivity_matrices(matrices)
    clipped = _select_columns(run_portfolio_suite(clipped_matrices))
    sensitivity = build_extreme_sensitivity_metrics(
        canonical["performance_metrics"], clipped["performance_metrics"]
    ).loc[:, list(SENSITIVITY_COLUMNS)]

    canonical_report = validate_portfolio_outputs(
        fund_returns=canonical["fund_returns"],
        fund_weights=canonical["fund_weights"],
        performance_metrics=canonical["performance_metrics"],
        solver_diagnostics=canonical["solver_diagnostics"],
        sensitivity_metrics=sensitivity,
        family_matrices=matrices,
        require_sensitivity=True,
    )
    clipped_report = validate_portfolio_outputs(
        fund_returns=clipped["fund_returns"],
        fund_weights=clipped["fund_weights"],
        performance_metrics=clipped["performance_metrics"],
        solver_diagnostics=clipped["solver_diagnostics"],
        family_matrices=clipped_matrices,
    )
    if not canonical_report.ok or not clipped_report.ok:
        failures = canonical_report.blocks + clipped_report.blocks
        codes = ", ".join(result.code for result in failures)
        raise RuntimeError(f"portfolio validation blocked all output writes: {codes}")

    _write_outputs(canonical, sensitivity)
    first_dates = (
        canonical["performance_metrics"]
        .groupby("family", sort=False)["start_date"]
        .first()
        .dt.strftime("%Y-%m-%d")
        .to_dict()
    )
    retries = int(canonical["solver_diagnostics"]["retry_used"].sum())
    near_identical = int(
        canonical["solver_diagnostics"]["near_identical_warning"].sum()
    )
    sensitivity_retries = int(clipped["solver_diagnostics"]["retry_used"].sum())
    sensitivity_near_identical = int(
        clipped["solver_diagnostics"]["near_identical_warning"].sum()
    )
    summary = canonical_report.to_dict()["summary"]
    print(
        "Canonical portfolio validation: "
        f"PASS={summary['PASS']} WARN={summary['WARN']} BLOCK={summary['BLOCK']}"
    )
    print(f"First live dates: {first_dates}")
    print(
        "Output rows: "
        f"returns={len(canonical['fund_returns'])} "
        f"weights={len(canonical['fund_weights'])} "
        f"metrics={len(canonical['performance_metrics'])} "
        f"diagnostics={len(canonical['solver_diagnostics'])} "
        f"sensitivity={len(sensitivity)}"
    )
    print(f"Canonical solver retries={retries}; near-identical diagnostic rows={near_identical}")
    print(
        "Sensitivity solver retries="
        f"{sensitivity_retries}; near-identical diagnostic rows={sensitivity_near_identical}"
    )
    _print_retry_evidence("Canonical", canonical)
    _print_retry_evidence("Sensitivity", clipped)
    print("PORTFOLIO STAGE STATUS: PASS")
    return 0


def main() -> int:
    args = parse_args()
    if args.stage == "portfolios":
        return run_portfolios(
            with_extreme_sensitivity=args.with_extreme_sensitivity
        )
    if args.stage == "sentiment-fusion":
        return run_sentiment_fusion()
    raise RuntimeError(f"unsupported stage: {args.stage}")


if __name__ == "__main__":
    raise SystemExit(main())
