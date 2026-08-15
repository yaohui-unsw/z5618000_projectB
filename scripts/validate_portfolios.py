"""Validate precomputed frozen portfolio outputs without rerunning optimisation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.portfolio_validation import validate_portfolio_outputs  # noqa: E402
from src.validation import ValidationReport, ValidationResult  # noqa: E402


PATHS = {
    "fund_returns": PROJECT_ROOT / "results" / "data" / "fund_returns.csv",
    "fund_weights": PROJECT_ROOT / "results" / "data" / "fund_weights.csv",
    "performance_metrics": PROJECT_ROOT / "results" / "tables" / "performance_metrics.csv",
    "solver_diagnostics": PROJECT_ROOT / "results" / "tables" / "portfolio_solver_diagnostics.csv",
    "sensitivity_metrics": PROJECT_ROOT / "results" / "tables" / "extreme_sensitivity_metrics.csv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    return parser.parse_args()


def _load_outputs() -> dict[str, pd.DataFrame]:
    missing = [str(path.relative_to(PROJECT_ROOT)) for path in PATHS.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing portfolio outputs: {missing}")
    return {
        "fund_returns": pd.read_csv(PATHS["fund_returns"], parse_dates=["date"]),
        "fund_weights": pd.read_csv(PATHS["fund_weights"], parse_dates=["date"]),
        "performance_metrics": pd.read_csv(
            PATHS["performance_metrics"], parse_dates=["start_date", "end_date"]
        ),
        "solver_diagnostics": pd.read_csv(
            PATHS["solver_diagnostics"], parse_dates=["date"]
        ),
        "sensitivity_metrics": pd.read_csv(PATHS["sensitivity_metrics"]),
    }


def main() -> int:
    args = parse_args()
    try:
        outputs = _load_outputs()
        report = validate_portfolio_outputs(
            **outputs,
            require_sensitivity=True,
        )
    except Exception as exc:
        report = ValidationReport()
        report.results.append(
            ValidationResult(
                code="portfolio_output_loading",
                level="BLOCK",
                message=f"Portfolio output validation failed: {type(exc).__name__}: {exc}",
            )
        )

    payload = report.to_dict()
    if args.json:
        print(json.dumps(payload, indent=2, default=str))
    else:
        summary = payload["summary"]
        print(
            "Portfolio output validation: "
            f"PASS={summary['PASS']} WARN={summary['WARN']} BLOCK={summary['BLOCK']}"
        )
        for result in report.results:
            if result.level != "PASS":
                print(f"{result.level} {result.code}: {result.message}")
        print("PORTFOLIO OUTPUT STATUS: PASS" if report.ok else "PORTFOLIO OUTPUT STATUS: BLOCK")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
