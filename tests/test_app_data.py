from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
import pytest

from src import app_data


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_all_artifact_paths_are_relative_existing_and_project_contained() -> None:
    root = app_data.PROJECT_ROOT.resolve()
    assert not root.is_file()
    assert len(app_data.ARTIFACT_SPECS) == 13
    for name, spec in app_data.ARTIFACT_SPECS.items():
        assert not Path(spec.relative_path).is_absolute()
        path = app_data.artifact_path(name)
        path.relative_to(root)
        assert path.is_file(), spec.relative_path


def test_every_artifact_loads_with_frozen_schema_dates_keys_and_order() -> None:
    for name, spec in app_data.ARTIFACT_SPECS.items():
        frame = app_data.load_artifact(name)
        assert tuple(frame.columns) == spec.columns
        assert len(frame) == spec.expected_rows
        assert not frame.duplicated(list(spec.key_columns)).any()
        for column in spec.date_columns:
            assert pd.api.types.is_datetime64_any_dtype(frame[column]), (name, column)
        assert frame.equals(app_data.load_artifact(name))


def test_exact_base_fund_overlay_and_operational_lexicon_universes() -> None:
    metrics = app_data.load_base_metrics()
    fusion_metrics, comparison = app_data.load_fusion_evidence()
    _, _, lexicon = app_data.load_sentiment_evidence()
    assert tuple(metrics["fund_id"]) == app_data.FUND_IDS
    assert tuple(fusion_metrics["overlay_id"]) == app_data.OVERLAY_IDS
    assert tuple(comparison["overlay_id"]) == app_data.OVERLAY_IDS
    assert len(lexicon) == 23
    assert lexicon["term"].nunique() == 23
    assert {"inflow", "inflows", "outflow", "outflows"}.isdisjoint(lexicon["term"])


def test_loaders_return_defensive_copies_and_never_modify_artifact() -> None:
    path = app_data.artifact_path("performance_metrics")
    before = _sha256(path)
    first = app_data.load_base_metrics()
    original = first.loc[0, "net_annualised_return"]
    first.loc[0, "net_annualised_return"] = 999.0
    second = app_data.load_base_metrics()
    assert second.loc[0, "net_annualised_return"] == original
    assert _sha256(path) == before


def test_missing_artifact_fails_with_named_human_readable_message(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    spec = app_data.ArtifactSpec(
        relative_path="results/data/definitely_missing.csv",
        columns=("id",),
        date_columns=(),
        key_columns=("id",),
        sort_columns=("id",),
        expected_rows=1,
        purpose="Missing-file test",
    )
    monkeypatch.setitem(app_data.ARTIFACT_SPECS, "missing_test", spec)
    with pytest.raises(app_data.ArtifactError, match="definitely_missing.csv"):
        app_data._read_and_validate("missing_test", project_root=tmp_path)
    assert not (tmp_path / spec.relative_path).exists()


def test_invalid_schema_fails_instead_of_using_placeholder(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    spec = app_data.ArtifactSpec(
        relative_path="bad.csv",
        columns=("id", "value"),
        date_columns=(),
        key_columns=("id",),
        sort_columns=("id",),
        expected_rows=1,
        purpose="Schema test",
    )
    monkeypatch.setitem(app_data.ARTIFACT_SPECS, "bad_test", spec)
    (tmp_path / "bad.csv").write_text("id\n1\n", encoding="utf-8")
    with pytest.raises(app_data.ArtifactError, match="Invalid schema"):
        app_data._read_and_validate("bad_test", project_root=tmp_path)

