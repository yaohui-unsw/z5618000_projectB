"""Independently audit frozen outputs and transactionally build eight report exhibits."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.reporting import (  # noqa: E402
    FIGURE_FILENAMES,
    AuditReport,
    audit_canonical_outputs,
    build_figure_artifacts,
    canonical_hashes,
    file_sha256,
    load_canonical_outputs,
)


OUTPUT_DIR = PROJECT_ROOT / "results" / "figures"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print complete audit evidence as JSON.")
    return parser.parse_args()


def validate_png(path: Path) -> dict[str, Any]:
    """Validate format, size, DPI, and visible variation without changing a file."""
    if not path.is_file() or path.stat().st_size <= 30_000:
        raise ValueError(f"PNG is missing or too small: {path.name}")
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        width, height = image.size
        dpi = image.info.get("dpi", (0.0, 0.0))
        if image.format != "PNG":
            raise ValueError(f"unsupported figure format for {path.name}: {image.format}")
        if width < 3_000 or height < 1_800:
            raise ValueError(f"figure resolution is below the 300-DPI report minimum: {path.name} {width}x{height}")
        if min(float(dpi[0]), float(dpi[1])) < 299.0:
            raise ValueError(f"figure DPI is below 300: {path.name} {dpi}")
        thumbnail = image.convert("L").resize((160, 100))
        pixels = np.asarray(thumbnail, dtype="float64")
        if float(pixels.std()) < 4.0 or int(pixels.max() - pixels.min()) < 35:
            raise ValueError(f"figure appears blank or near-blank: {path.name}")
    return {
        "bytes": path.stat().st_size,
        "width": width,
        "height": height,
        "dpi_x": float(dpi[0]),
        "dpi_y": float(dpi[1]),
        "pixel_std": float(pixels.std()),
        "sha256": file_sha256(path),
    }


def _transactional_commit(staged: dict[str, Path]) -> None:
    """Replace the authorised set with rollback if any placement fails."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    backup_dir = next(iter(staged.values())).parent / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backups: dict[Path, Path] = {}
    placed: list[Path] = []
    try:
        for filename in FIGURE_FILENAMES:
            destination = OUTPUT_DIR / filename
            if destination.exists():
                backup = backup_dir / filename
                os.replace(destination, backup)
                backups[destination] = backup
        for filename in FIGURE_FILENAMES:
            destination = OUTPUT_DIR / filename
            os.replace(staged[filename], destination)
            placed.append(destination)
    except Exception:
        for destination in placed:
            if destination.exists():
                destination.unlink()
        for destination, backup in backups.items():
            if backup.exists():
                os.replace(backup, destination)
        raise


def main() -> int:
    args = parse_args()
    if Path.cwd().resolve() != PROJECT_ROOT.resolve():
        print("Report exhibit audit: PASS=0 WARN=0 BLOCK=1")
        print(f"BLOCK workspace_guard: cwd={Path.cwd().resolve()} expected={PROJECT_ROOT.resolve()}")
        return 1

    try:
        source_hashes = canonical_hashes(PROJECT_ROOT)
        frames = load_canonical_outputs(PROJECT_ROOT)
        report = audit_canonical_outputs(frames, source_hashes)
    except Exception as exc:
        report = AuditReport()
        report.add(False, "audit_execution", "", f"Audit execution failed: {type(exc).__name__}: {exc}")
        frames = {}

    if not report.ok:
        payload = report.to_dict()
        if args.json:
            print(json.dumps(payload, indent=2, default=str))
        else:
            summary = report.summary
            print(f"Report exhibit audit: PASS={summary['PASS']} WARN={summary['WARN']} BLOCK={summary['BLOCK']}")
            for finding in report.findings:
                if finding.level != "PASS":
                    print(f"{finding.level} {finding.code}: {finding.message}")
            print("REPORT EXHIBIT STATUS: BLOCK")
        return 1

    existing_hashes = {
        filename: file_sha256(OUTPUT_DIR / filename)
        for filename in FIGURE_FILENAMES
        if (OUTPUT_DIR / filename).is_file()
    }
    staged_info: dict[str, dict[str, Any]] = {}
    stage_root: Path | None = None
    artifacts = []
    try:
        stage_root = Path(tempfile.mkdtemp(prefix="fins5545_stage7_exhibits_"))
        try:
            stage_root.resolve().relative_to(PROJECT_ROOT.resolve())
            raise RuntimeError("staging directory resolved inside Project B")
        except ValueError:
            pass
        artifacts = build_figure_artifacts(frames)
        filenames = tuple(artifact.metadata.filename for artifact in artifacts)
        if filenames != FIGURE_FILENAMES:
            raise ValueError(f"figure set/order differs: {filenames}")
        staged: dict[str, Path] = {}
        for artifact in artifacts:
            destination = stage_root / artifact.metadata.filename
            artifact.figure.savefig(
                destination,
                dpi=300,
                facecolor="#FBFCFD",
                edgecolor="none",
                metadata={
                    "Software": "FINS5545 Project B Stage 7",
                    "Title": artifact.metadata.title,
                    "Description": artifact.metadata.question,
                },
            )
            plt.close(artifact.figure)
            staged[artifact.metadata.filename] = destination
            staged_info[artifact.metadata.filename] = validate_png(destination)
        report.add(
            set(staged) == set(FIGURE_FILENAMES),
            "staged_figure_set",
            "All eight authorised PNGs were staged outside Project B.",
            "The staged figure set is incomplete or unexpected.",
        )
        report.add(
            all(info["width"] >= 3_000 and info["height"] >= 1_800 and min(info["dpi_x"], info["dpi_y"]) >= 299 for info in staged_info.values()),
            "staged_figure_quality",
            "All staged figures are valid, substantive, and report-resolution PNGs.",
            "A staged figure failed visual-file QA.",
        )
        if existing_hashes:
            rebuilt_hashes = {name: info["sha256"] for name, info in staged_info.items()}
            if existing_hashes == rebuilt_hashes:
                report.add(
                    True,
                    "deterministic_rebuild",
                    "The unchanged rebuild reproduces all eight existing figure hashes.",
                    "",
                    observed=rebuilt_hashes,
                    expected=existing_hashes,
                )
            else:
                report.warn(
                    "visual_revision_hash_change",
                    "The current reporting-code render differs from an existing Stage 7 PNG; the transactional replacement is disclosed and an immediate unchanged rebuild is required to establish determinism.",
                    observed={
                        "before": existing_hashes,
                        "staged": rebuilt_hashes,
                    },
                )
        if not report.ok:
            raise RuntimeError("staged audit produced a BLOCK")
        _transactional_commit(staged)
    except Exception as exc:
        for artifact in artifacts:
            plt.close(artifact.figure)
        report.add(False, "figure_generation", "", f"Figure generation/commit failed: {type(exc).__name__}: {exc}")
    finally:
        if stage_root is not None:
            shutil.rmtree(stage_root, ignore_errors=True)

    if report.ok:
        final_info = {filename: validate_png(OUTPUT_DIR / filename) for filename in FIGURE_FILENAMES}
        report.evidence["figure_files"] = final_info
        report.add(
            {name: info["sha256"] for name, info in final_info.items()} == {name: info["sha256"] for name, info in staged_info.items()},
            "committed_figure_hashes",
            "All eight committed PNG hashes equal their validated staged hashes.",
            "A committed figure differs from its validated staged image.",
        )

    payload = report.to_dict()
    if args.json:
        print(json.dumps(payload, indent=2, default=str))
    else:
        summary = report.summary
        print(f"Report exhibit audit: PASS={summary['PASS']} WARN={summary['WARN']} BLOCK={summary['BLOCK']}")
        for finding in report.findings:
            if finding.level != "PASS":
                print(f"{finding.level} {finding.code}: {finding.message}")
        if report.ok:
            evidence = report.evidence
            print(
                "Headline reconciliation: "
                f"cleaned={evidence['cleaned_headlines']} mapped={evidence['mapped_headlines']} "
                f"unmapped={evidence['unmapped_headlines']}"
            )
            print(
                "Paired Sharpe improvements: "
                f"plain={evidence['plain_positive_sharpe_deltas']}/8 "
                f"finance={evidence['finance_positive_sharpe_deltas']}/8 "
                f"evidence-aware={evidence['evidence_positive_sharpe_deltas']}/8"
            )
            print(f"Best base-relative overlay: {evidence['best_overlay']}")
            print(f"Weakest base-relative overlay: {evidence['weakest_overlay']}")
            for filename in FIGURE_FILENAMES:
                info = evidence["figure_files"][filename]
                print(f"FIGURE {filename} rows=NA pixels={info['width']}x{info['height']} bytes={info['bytes']} sha256={info['sha256']}")
        print(f"REPORT EXHIBIT STATUS: {'PASS' if report.ok else 'BLOCK'}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
