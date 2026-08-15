"""Machine-readable validation for the frozen Project B input contract.

This module centralises the accepted universe, schemas, boundaries, benchmark
counts, and validation outcomes. It validates data already held in memory and
never writes artifacts.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Literal

import numpy as np
import pandas as pd


Level = Literal["PASS", "WARN", "BLOCK"]

PROJECT_DIRECTORY_NAME = "z5618000_projectB"
PROTECTED_LOADER_SHA256 = (
    "928887403C34407C99B02984CB0600CBCF2CB9F88D7404D8E81A4B40E778B710"
)

CRYPTO_CUTOFF = pd.Timestamp("2023-12-31")
EQUITY_START = pd.Timestamp("2020-01-02")
EQUITY_END = pd.Timestamp("2023-12-29")
CRYPTO_START = pd.Timestamp("2020-01-01")
CRYPTO_END = CRYPTO_CUTOFF

EQUITY_TICKERS = (
    "ABBV", "ABT", "ADBE", "AEP", "AMD", "AMGN", "AMT", "BA", "CAT",
    "CCI", "CMCSA", "COP", "CVX", "D", "DD", "DIS", "DOW", "DUK",
    "EA", "GE", "GILD", "GS", "INTC", "KO", "MMM", "MRK", "MS",
    "NEE", "NEM", "NKE", "NUE", "NVDA", "O", "OXY", "PLD", "PSA",
    "QCOM", "SBUX", "SHW", "SLB", "SO", "T", "TMUS", "TTWO", "UPS",
    "USB", "V", "WFC", "WMT", "XOM",
)
CRYPTO_TICKERS = (
    "ADA-USD", "BCH-USD", "BTC-USD", "EOS-USD", "ETC-USD", "ETH-USD",
    "LTC-USD", "TRX-USD", "XLM-USD", "XRP-USD",
)
COMBINED_ASSETS = EQUITY_TICKERS + CRYPTO_TICKERS

SOURCE_SECTORS = (
    "Comm", "Consumer", "Energy", "Financials", "Healthcare", "Industrials",
    "Materials", "RealEstate", "Tech", "Utilities",
)
SECTOR_DISPLAY_ORDER = (
    "Tech", "Financials", "Energy", "Consumer", "Industrials", "Healthcare",
    "Comm", "Materials", "Utilities", "RealEstate",
)
SECTOR_DISPLAY_LABELS = {
    "Tech": "Tech",
    "Financials": "Financials",
    "Energy": "Energy",
    "Consumer": "Consumer",
    "Industrials": "Industrials",
    "Healthcare": "Healthcare",
    "Comm": "Comm/Telecom",
    "Materials": "Materials",
    "Utilities": "Utilities",
    "RealEstate": "Real Estate",
}

EQUITY_PRICE_COLUMNS = (
    "ticker", "date", "open", "high", "low", "close", "adjClose", "volume",
    "sector",
)
CRYPTO_PRICE_COLUMNS = (
    "ticker", "date", "open", "high", "low", "close", "adjClose", "volume",
)
RAW_NEWS_COLUMNS = ("date", "ticker", "sector", "title", "url", "publisher")
CLEAN_NEWS_COLUMNS = RAW_NEWS_COLUMNS + (
    "source_row_order", "source_timestamp", "source_date_utc",
)
EQUITY_RETURN_COLUMNS = ("date", "ticker", "sector", "adjClose", "return")
CRYPTO_RETURN_COLUMNS = ("date", "ticker", "adjClose", "return")
ALIGNED_CRYPTO_COLUMNS = ("date", "ticker", "return")
MAPPING_COLUMNS = ("map_status", "mapped_trade_date", "mapping_day_distance")
COVERAGE_COLUMNS = ("date", "ticker", "sector", "headline_count", "has_news")

BENCHMARKS = {
    "raw_equity_rows": 50_300,
    "clean_equity_rows": 50_300,
    "equity_tickers": 50,
    "equity_sectors": 10,
    "equity_dates": 1_006,
    "raw_crypto_rows": 14_620,
    "crypto_cutoff_rows_removed": 10,
    "clean_crypto_rows": 14_610,
    "crypto_tickers": 10,
    "crypto_native_dates": 1_461,
    "raw_news_rows": 149_683,
    "news_duplicates_removed": 2_847,
    "clean_news_rows": 146_836,
    "mapped_headlines": 146_830,
    "unmapped_headlines": 6,
    "coverage_rows": 50_300,
    "no_news_rows": 12_338,
    "aligned_crypto_rows": 10_060,
    "combined_rows": 1_006,
    "combined_assets": 60,
    "equity_first_missing_returns": 50,
    "crypto_first_missing_returns": 10,
    "missing_publishers": 137_447,
    "equity_extremes": 4,
    "crypto_extremes": 65,
}

SIX_UNMAPPED = (
    (14659, pd.Timestamp("2023-12-30")),
    (14660, pd.Timestamp("2023-12-30")),
    (14661, pd.Timestamp("2023-12-30")),
    (14662, pd.Timestamp("2023-12-31")),
    (14663, pd.Timestamp("2023-12-31")),
    (14664, pd.Timestamp("2023-12-31")),
)


@dataclass(frozen=True)
class ValidationResult:
    """One deterministic contract finding."""

    code: str
    level: Level
    message: str
    observed: Any = None
    expected: Any = None

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        for key in ("observed", "expected"):
            item = value[key]
            if isinstance(item, (pd.Timestamp, np.datetime64)):
                value[key] = str(item)
            elif isinstance(item, tuple):
                value[key] = list(item)
        return value


class ContractViolation(RuntimeError):
    """Raised when requested for a report containing one or more BLOCKs."""


class ValidationReport:
    """Ordered, machine-readable collection of contract findings."""

    def __init__(self) -> None:
        self.results: list[ValidationResult] = []

    def add(
        self,
        condition: bool,
        code: str,
        pass_message: str,
        fail_message: str,
        *,
        observed: Any = None,
        expected: Any = None,
        failure_level: Literal["WARN", "BLOCK"] = "BLOCK",
    ) -> None:
        self.results.append(
            ValidationResult(
                code=code,
                level="PASS" if bool(condition) else failure_level,
                message=pass_message if bool(condition) else fail_message,
                observed=observed,
                expected=expected,
            )
        )

    def warn(
        self, code: str, message: str, *, observed: Any = None, expected: Any = None
    ) -> None:
        self.results.append(ValidationResult(code, "WARN", message, observed, expected))

    @property
    def blocks(self) -> list[ValidationResult]:
        return [result for result in self.results if result.level == "BLOCK"]

    @property
    def warnings(self) -> list[ValidationResult]:
        return [result for result in self.results if result.level == "WARN"]

    @property
    def passes(self) -> list[ValidationResult]:
        return [result for result in self.results if result.level == "PASS"]

    @property
    def ok(self) -> bool:
        return not self.blocks

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": "PASS" if self.ok else "BLOCK",
            "summary": {
                "PASS": len(self.passes),
                "WARN": len(self.warnings),
                "BLOCK": len(self.blocks),
            },
            "results": [result.to_dict() for result in self.results],
        }

    def raise_for_blocks(self) -> None:
        if self.blocks:
            codes = ", ".join(result.code for result in self.blocks)
            raise ContractViolation(f"Data contract validation blocked: {codes}")


def _columns_are(frame: pd.DataFrame, expected: tuple[str, ...]) -> bool:
    return tuple(frame.columns) == expected


def _dtypes_are(frame: pd.DataFrame, expected: dict[str, str]) -> bool:
    return all(column in frame and str(frame[column].dtype) == dtype for column, dtype in expected.items())


def _ordered_by(frame: pd.DataFrame, columns: list[str]) -> bool:
    expected = frame.sort_values(columns, kind="mergesort", na_position="last")
    return frame.reset_index(drop=True).equals(expected.reset_index(drop=True))


def _unique_non_null_key(frame: pd.DataFrame, columns: list[str]) -> bool:
    return not frame.loc[:, columns].isna().any().any() and not frame.duplicated(columns).any()


def _date_bounds(frame: pd.DataFrame) -> tuple[pd.Timestamp, pd.Timestamp]:
    return pd.Timestamp(frame["date"].min()), pd.Timestamp(frame["date"].max())


def sha256_file(path: Path) -> str:
    """Hash a local file without changing it."""
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def find_extreme_observations(
    prices: pd.DataFrame, *, threshold: float = 0.25
) -> pd.DataFrame:
    """Return internally auditable native-calendar price movements.

    The function does not fill, remove, or alter an observation.
    """
    required = {"ticker", "date", "adjClose"}
    missing = sorted(required.difference(prices.columns))
    if missing:
        raise ValueError(f"prices missing extreme-review columns: {missing}")
    audit = prices.copy(deep=True).sort_values(
        ["ticker", "date"], kind="mergesort"
    )
    grouped = audit.groupby("ticker", sort=False, observed=True)
    audit["previous_date"] = grouped["date"].shift(1)
    audit["previous_adjClose"] = grouped["adjClose"].shift(1)
    if "volume" in audit:
        audit["previous_volume"] = grouped["volume"].shift(1)
    audit["calculated_return"] = audit["adjClose"].div(
        audit["previous_adjClose"]
    ).sub(1.0)
    selected = audit.loc[audit["calculated_return"].abs().ge(threshold)].copy()
    return selected.sort_values(["date", "ticker"], kind="mergesort").reset_index(
        drop=True
    )


def _validate_extremes(
    report: ValidationReport,
    prices: pd.DataFrame,
    expected_count: int,
    prefix: str,
) -> None:
    extremes = find_extreme_observations(prices)
    report.add(
        len(extremes) == expected_count,
        f"{prefix}_extreme_count",
        f"Retained all {expected_count} contracted extreme observations.",
        "Extreme-observation count differs from the frozen benchmark.",
        observed=len(extremes),
        expected=expected_count,
    )
    current = pd.to_numeric(extremes["adjClose"], errors="coerce")
    previous = pd.to_numeric(extremes["previous_adjClose"], errors="coerce")
    returns = pd.to_numeric(extremes["calculated_return"], errors="coerce")
    consistency = (
        np.isfinite(current).all()
        and current.gt(0).all()
        and np.isfinite(previous).all()
        and previous.gt(0).all()
        and np.isfinite(returns).all()
        and extremes["previous_date"].notna().all()
        and not extremes.duplicated(["ticker", "date"]).any()
    )
    if "volume" in extremes:
        volume = pd.to_numeric(extremes["volume"], errors="coerce")
        previous_volume = pd.to_numeric(extremes["previous_volume"], errors="coerce")
        consistency = bool(
            consistency
            and np.isfinite(volume).all()
            and volume.ge(0).all()
            and np.isfinite(previous_volume).all()
            and previous_volume.ge(0).all()
        )
    report.add(
        consistency,
        f"{prefix}_extreme_internal_consistency",
        "Retained extremes have valid observed predecessor rows and finite source values.",
        "At least one retained extreme failed the bounded internal-consistency checks.",
        observed=len(extremes),
        expected=expected_count,
    )
    if len(extremes):
        report.warn(
            f"{prefix}_extremes_retained",
            "Extreme returns are retained unchanged and require later, separately labelled sensitivity evidence.",
            observed=len(extremes),
            expected=expected_count,
        )


def validate_data_foundation(
    *,
    project_root: Path,
    loader_path: Path,
    raw_equity: pd.DataFrame,
    raw_crypto: pd.DataFrame,
    raw_news: pd.DataFrame,
    equity: pd.DataFrame,
    crypto: pd.DataFrame,
    news: pd.DataFrame,
    equity_returns: pd.DataFrame,
    crypto_returns: pd.DataFrame,
    aligned_crypto: pd.DataFrame,
    combined_returns: pd.DataFrame,
    full_mapping: pd.DataFrame,
    mapped_headlines: pd.DataFrame,
    coverage_panel: pd.DataFrame,
) -> ValidationReport:
    """Validate the complete in-memory Stage 4A pipeline against the contract."""
    report = ValidationReport()

    root = project_root.resolve()
    loader = loader_path.resolve()
    report.add(
        root.name == PROJECT_DIRECTORY_NAME,
        "workspace_root",
        "Project directory name matches the frozen Project B root.",
        "Execution is outside the frozen Project B root.",
        observed=root.name,
        expected=PROJECT_DIRECTORY_NAME,
    )
    report.add(
        loader == root / "src" / "data_access.py",
        "protected_loader_path",
        "Data loaded through the protected local src/data_access.py path.",
        "Loader path is not the protected Project B helper.",
        observed=str(loader),
        expected="<project root>/src/data_access.py",
    )
    loader_hash = sha256_file(loader) if loader.is_file() else None
    report.add(
        loader_hash == PROTECTED_LOADER_SHA256,
        "protected_loader_hash",
        "Protected loader hash matches the frozen contract.",
        "Protected loader hash differs from the frozen contract.",
        observed=loader_hash,
        expected=PROTECTED_LOADER_SHA256,
    )

    schemas = (
        ("equity_schema", equity, EQUITY_PRICE_COLUMNS),
        ("crypto_schema", crypto, CRYPTO_PRICE_COLUMNS),
        ("news_schema", news, CLEAN_NEWS_COLUMNS),
        ("equity_return_schema", equity_returns, EQUITY_RETURN_COLUMNS),
        ("crypto_return_schema", crypto_returns, CRYPTO_RETURN_COLUMNS),
        ("aligned_crypto_schema", aligned_crypto, ALIGNED_CRYPTO_COLUMNS),
        ("full_mapping_schema", full_mapping, CLEAN_NEWS_COLUMNS + MAPPING_COLUMNS),
        ("mapped_headline_schema", mapped_headlines, CLEAN_NEWS_COLUMNS + MAPPING_COLUMNS),
        ("coverage_schema", coverage_panel, COVERAGE_COLUMNS),
    )
    for code, frame, expected in schemas:
        report.add(
            _columns_are(frame, expected),
            code,
            "Columns and column order match the frozen schema.",
            "Columns or column order differ from the frozen schema.",
            observed=tuple(frame.columns),
            expected=expected,
        )

    dtype_checks = (
        (
            "equity_dtypes",
            equity,
            {
                "ticker": "string", "date": "datetime64[ns]", "open": "float64",
                "high": "float64", "low": "float64", "close": "float64",
                "adjClose": "float64", "volume": "int64", "sector": "string",
            },
        ),
        (
            "crypto_dtypes",
            crypto,
            {
                "ticker": "string", "date": "datetime64[ns]", "open": "float64",
                "high": "float64", "low": "float64", "close": "float64",
                "adjClose": "float64", "volume": "int64",
            },
        ),
        (
            "news_dtypes",
            news,
            {
                "date": "datetime64[us, UTC]", "ticker": "string", "sector": "string",
                "title": "string", "url": "string", "publisher": "string",
                "source_row_order": "int64", "source_timestamp": "datetime64[ns, UTC]",
                "source_date_utc": "datetime64[ns]",
            },
        ),
        (
            "equity_return_dtypes",
            equity_returns,
            {
                "date": "datetime64[ns]", "ticker": "string", "sector": "string",
                "adjClose": "float64", "return": "float64",
            },
        ),
        (
            "crypto_return_dtypes",
            crypto_returns,
            {
                "date": "datetime64[ns]", "ticker": "string", "adjClose": "float64",
                "return": "float64",
            },
        ),
        (
            "aligned_crypto_dtypes",
            aligned_crypto,
            {"date": "datetime64[ns]", "ticker": "string", "return": "float64"},
        ),
        (
            "full_mapping_dtypes",
            full_mapping,
            {
                "map_status": "string", "mapped_trade_date": "datetime64[ns]",
                "mapping_day_distance": "Int64",
            },
        ),
        (
            "mapped_headline_dtypes",
            mapped_headlines,
            {
                "map_status": "string", "mapped_trade_date": "datetime64[ns]",
                "mapping_day_distance": "int64",
            },
        ),
        (
            "coverage_dtypes",
            coverage_panel,
            {
                "date": "datetime64[ns]", "ticker": "string", "sector": "string",
                "headline_count": "int64", "has_news": "bool",
            },
        ),
    )
    for code, frame, expected in dtype_checks:
        observed = {column: str(frame[column].dtype) for column in expected if column in frame}
        report.add(
            _dtypes_are(frame, expected),
            code,
            "Contracted semantic dtypes are present.",
            "At least one contracted dtype is absent or changed.",
            observed=observed,
            expected=expected,
        )

    required_non_null = (
        ("equity_required_missingness", equity, EQUITY_PRICE_COLUMNS),
        ("crypto_required_missingness", crypto, CRYPTO_PRICE_COLUMNS),
        (
            "news_required_missingness",
            news,
            tuple(column for column in CLEAN_NEWS_COLUMNS if column != "publisher"),
        ),
        ("aligned_crypto_required_missingness", aligned_crypto, ALIGNED_CRYPTO_COLUMNS),
        (
            "mapped_headline_required_missingness",
            mapped_headlines,
            tuple(column for column in CLEAN_NEWS_COLUMNS if column != "publisher")
            + MAPPING_COLUMNS,
        ),
        ("coverage_required_missingness", coverage_panel, COVERAGE_COLUMNS),
    )
    for code, frame, required in required_non_null:
        missing_count = int(frame.loc[:, list(required)].isna().sum().sum())
        report.add(
            missing_count == 0,
            code,
            "Required fields contain no missing values.",
            "At least one required field is missing.",
            observed=missing_count,
            expected=0,
        )

    row_checks = (
        ("raw_equity_rows", len(raw_equity)),
        ("clean_equity_rows", len(equity)),
        ("raw_crypto_rows", len(raw_crypto)),
        ("clean_crypto_rows", len(crypto)),
        ("raw_news_rows", len(raw_news)),
        ("clean_news_rows", len(news)),
        ("mapped_headlines", len(mapped_headlines)),
        ("coverage_rows", len(coverage_panel)),
        ("aligned_crypto_rows", len(aligned_crypto)),
        ("combined_rows", len(combined_returns)),
    )
    for key, observed in row_checks:
        report.add(
            observed == BENCHMARKS[key],
            key,
            f"{key} matches the frozen benchmark.",
            f"{key} differs from the frozen benchmark.",
            observed=observed,
            expected=BENCHMARKS[key],
        )

    removed_cutoff = int(pd.to_datetime(raw_crypto["date"]).gt(CRYPTO_CUTOFF).sum())
    removed_duplicates = len(raw_news) - len(news)
    report.add(
        removed_cutoff == BENCHMARKS["crypto_cutoff_rows_removed"],
        "crypto_cutoff_removal",
        "The cutoff removes exactly the ten 2024-01-01 rows.",
        "The crypto cutoff removal count differs from the contract.",
        observed=removed_cutoff,
        expected=BENCHMARKS["crypto_cutoff_rows_removed"],
    )
    report.add(
        removed_duplicates == BENCHMARKS["news_duplicates_removed"],
        "news_duplicate_removal",
        "Deterministic news deduplication removed the contracted identities.",
        "News duplicate removal differs from the contract.",
        observed=removed_duplicates,
        expected=BENCHMARKS["news_duplicates_removed"],
    )

    for code, frame in (
        ("equity_price_key", equity),
        ("crypto_price_key", crypto),
        ("equity_return_key", equity_returns),
        ("crypto_return_key", crypto_returns),
        ("aligned_crypto_key", aligned_crypto),
        ("coverage_key", coverage_panel),
    ):
        report.add(
            _unique_non_null_key(frame, ["date", "ticker"]),
            code,
            "Ticker-date key is complete and unique.",
            "Ticker-date key is null or duplicated.",
        )
    report.add(
        _unique_non_null_key(news, ["ticker", "source_timestamp", "title"]),
        "clean_news_key",
        "Clean-news identity is complete and unique.",
        "Clean-news identity is null or duplicated.",
    )

    for code, frame in (("equity", equity), ("crypto", crypto)):
        values = pd.to_numeric(frame["adjClose"], errors="coerce")
        report.add(
            np.isfinite(values).all() and values.gt(0).all(),
            f"{code}_adjclose",
            "All adjusted closes are finite and strictly positive.",
            "Adjusted close contains a non-finite or non-positive value.",
        )
        volume = pd.to_numeric(frame["volume"], errors="coerce")
        report.add(
            np.isfinite(volume).all() and volume.ge(0).all(),
            f"{code}_volume",
            "All volumes are finite and non-negative.",
            "Volume contains a non-finite or negative value.",
        )

    membership_checks = (
        ("equity_tickers", tuple(sorted(equity["ticker"].unique())), EQUITY_TICKERS),
        ("crypto_tickers", tuple(sorted(crypto["ticker"].unique())), CRYPTO_TICKERS),
        ("equity_sectors", tuple(sorted(equity["sector"].unique())), SOURCE_SECTORS),
        ("news_tickers", tuple(sorted(news["ticker"].unique())), EQUITY_TICKERS),
        ("news_sectors", tuple(sorted(news["sector"].unique())), SOURCE_SECTORS),
    )
    for code, observed, expected in membership_checks:
        report.add(
            observed == expected,
            code,
            "Membership matches the frozen contract.",
            "Membership differs from the frozen contract.",
            observed=observed,
            expected=expected,
        )

    report.add(
        _date_bounds(equity) == (EQUITY_START, EQUITY_END)
        and equity["date"].nunique() == BENCHMARKS["equity_dates"],
        "equity_boundaries",
        "Equity dates match the frozen range and count.",
        "Equity date boundaries or count differ from the contract.",
        observed=(*_date_bounds(equity), equity["date"].nunique()),
        expected=(EQUITY_START, EQUITY_END, BENCHMARKS["equity_dates"]),
    )
    report.add(
        _date_bounds(crypto) == (CRYPTO_START, CRYPTO_END)
        and crypto["date"].nunique() == BENCHMARKS["crypto_native_dates"]
        and not crypto["date"].gt(CRYPTO_CUTOFF).any(),
        "crypto_boundaries",
        "Crypto dates match the native-calendar range, count, and cutoff.",
        "Crypto date boundaries, count, or cutoff differ from the contract.",
        observed=(*_date_bounds(crypto), crypto["date"].nunique()),
        expected=(CRYPTO_START, CRYPTO_END, BENCHMARKS["crypto_native_dates"]),
    )

    title_preserved = news.apply(
        lambda row: raw_news.iloc[int(row["source_row_order"])]["title"] == row["title"],
        axis=1,
    ).all()
    report.add(
        title_preserved,
        "title_preservation",
        "Every retained title exactly matches its protected source row.",
        "At least one retained title was mutated.",
    )
    earliest = (
        raw_news.assign(
            source_row_order=np.arange(len(raw_news), dtype="int64"),
            source_timestamp=pd.to_datetime(raw_news["date"], utc=True).astype(
                "datetime64[ns, UTC]"
            ),
        )
        .groupby(["ticker", "source_timestamp", "title"], sort=False, dropna=False)[
            "source_row_order"
        ]
        .min()
    )
    clean_identity = news.set_index(["ticker", "source_timestamp", "title"])[
        "source_row_order"
    ]
    report.add(
        clean_identity.sort_index().equals(earliest.sort_index()),
        "earliest_duplicate_retention",
        "Every duplicate identity retained its smallest source row order.",
        "Duplicate retention did not consistently keep the earliest source row.",
    )

    missing_publisher = int(news["publisher"].isna().sum())
    report.add(
        missing_publisher == BENCHMARKS["missing_publishers"],
        "missing_publisher_count",
        "Missing-publisher count matches the frozen benchmark and rows were retained.",
        "Missing-publisher count differs from the frozen benchmark.",
        observed=missing_publisher,
        expected=BENCHMARKS["missing_publishers"],
    )
    if missing_publisher:
        report.warn(
            "missing_publishers_retained",
            "Missing publisher is allowed and does not remove a headline.",
            observed=missing_publisher,
        )

    equity_missing = int(equity_returns["return"].isna().sum())
    crypto_missing = int(crypto_returns["return"].isna().sum())
    aligned_missing = int(aligned_crypto["return"].isna().sum())
    report.add(
        equity_missing == BENCHMARKS["equity_first_missing_returns"],
        "equity_return_missingness",
        "Equity returns contain one legitimate first missing value per ticker.",
        "Equity-return missingness differs from the contract.",
        observed=equity_missing,
        expected=BENCHMARKS["equity_first_missing_returns"],
    )
    report.add(
        crypto_missing == BENCHMARKS["crypto_first_missing_returns"],
        "crypto_return_missingness",
        "Native crypto returns contain one legitimate first missing value per ticker.",
        "Native crypto-return missingness differs from the contract.",
        observed=crypto_missing,
        expected=BENCHMARKS["crypto_first_missing_returns"],
    )
    report.add(
        aligned_missing == 0,
        "aligned_crypto_missingness",
        "Aligned crypto returns have no missing values.",
        "Aligned crypto returns contain missing values.",
        observed=aligned_missing,
        expected=0,
    )
    report.warn(
        "legitimate_first_returns",
        "First native return per ticker remains missing; no fill was applied.",
        observed=equity_missing + crypto_missing,
        expected=60,
    )

    matrix_ok = (
        tuple(combined_returns.columns) == COMBINED_ASSETS
        and combined_returns.index.name == "date"
        and combined_returns.index.is_monotonic_increasing
        and combined_returns.index.is_unique
        and combined_returns.shape
        == (BENCHMARKS["combined_rows"], BENCHMARKS["combined_assets"])
        and int(combined_returns.isna().sum().sum())
        == BENCHMARKS["equity_first_missing_returns"]
    )
    report.add(
        matrix_ok,
        "combined_matrix",
        "Combined matrix has the frozen date index, asset order, shape, and missingness.",
        "Combined matrix structure, order, or missingness differs from the contract.",
        observed=(combined_returns.shape, int(combined_returns.isna().sum().sum())),
        expected=((1006, 60), 50),
    )

    calendar = pd.Index(equity["date"].drop_duplicates().sort_values())
    mapped = full_mapping["mapped_trade_date"].dropna()
    source_dates = full_mapping.loc[mapped.index, "source_date_utc"]
    mapping_ok = (
        mapped.isin(calendar).all()
        and mapped.ge(source_dates).all()
        and full_mapping["map_status"].isin(
            ["same_day", "forward", "unmapped_end_of_sample"]
        ).all()
        and full_mapping.loc[
            full_mapping["map_status"].eq("unmapped_end_of_sample"),
            "mapped_trade_date",
        ].isna().all()
    )
    report.add(
        mapping_ok,
        "mapping_direction_calendar",
        "Headline mapping is same-day/forward, on-calendar, and explicit at the endpoint.",
        "A headline mapped backward, off-calendar, or has an invalid endpoint status.",
    )
    distance = full_mapping.loc[mapped.index, "mapping_day_distance"]
    report.add(
        distance.notna().all()
        and distance.ge(0).all()
        and distance.le(3).all()
        and full_mapping.loc[
            full_mapping["map_status"].eq("same_day"), "mapping_day_distance"
        ].eq(0).all(),
        "mapping_distance",
        "Mapped headline distances are non-negative, bounded, and consistent with status.",
        "Mapping distance is missing, negative, out of range, or inconsistent with status.",
    )

    unmapped = full_mapping.loc[
        full_mapping["map_status"].eq("unmapped_end_of_sample")
    ].sort_values("source_row_order")
    measured_six = tuple(
        (int(row.source_row_order), pd.Timestamp(row.source_date_utc))
        for row in unmapped.itertuples()
    )
    six_ok = (
        measured_six == SIX_UNMAPPED
        and len(news) == len(mapped_headlines) + len(unmapped)
        and unmapped["ticker"].eq("AMD").all()
        and unmapped["sector"].eq("Tech").all()
    )
    report.add(
        six_ok,
        "six_unmapped_reconciliation",
        "The exact six AMD endpoint records reconcile cleaned and mapped headlines.",
        "The six-record identity or cleaned-to-mapped reconciliation failed.",
        observed=measured_six,
        expected=SIX_UNMAPPED,
    )

    no_news = int(coverage_panel["headline_count"].eq(0).sum())
    coverage_ok = (
        no_news == BENCHMARKS["no_news_rows"]
        and coverage_panel["has_news"].equals(coverage_panel["headline_count"].gt(0))
        and int(coverage_panel["headline_count"].sum()) == len(mapped_headlines)
        and not any("sentiment" in str(column).lower() for column in coverage_panel.columns)
    )
    report.add(
        coverage_ok,
        "coverage_reconciliation",
        "Coverage distinguishes no news without fabricating sentiment and reconciles counts.",
        "Coverage counts, has-news flags, or no-news semantics differ from the contract.",
        observed=(no_news, int(coverage_panel["headline_count"].sum())),
        expected=(BENCHMARKS["no_news_rows"], BENCHMARKS["mapped_headlines"]),
    )
    if no_news:
        report.warn(
            "no_news_rows_retained",
            "No-news ticker-days remain explicit missing-information states.",
            observed=no_news,
            expected=BENCHMARKS["no_news_rows"],
        )

    ordering_checks = (
        ("equity_order", equity, ["date", "ticker"]),
        ("crypto_order", crypto, ["date", "ticker"]),
        ("news_order", news, ["source_timestamp", "source_row_order", "ticker"]),
        ("equity_return_order", equity_returns, ["date", "ticker"]),
        ("crypto_return_order", crypto_returns, ["date", "ticker"]),
        ("aligned_crypto_order", aligned_crypto, ["date", "ticker"]),
        (
            "full_mapping_order",
            full_mapping,
            ["mapped_trade_date", "ticker", "source_timestamp", "source_row_order"],
        ),
        (
            "mapped_headline_order",
            mapped_headlines,
            ["mapped_trade_date", "ticker", "source_timestamp", "source_row_order"],
        ),
        ("coverage_order", coverage_panel, ["date", "ticker"]),
    )
    for code, frame, columns in ordering_checks:
        report.add(
            _ordered_by(frame, columns),
            code,
            "Canonical output ordering is deterministic.",
            "Canonical output ordering differs from the frozen rule.",
        )

    _validate_extremes(
        report, equity, BENCHMARKS["equity_extremes"], "equity"
    )
    _validate_extremes(
        report, crypto, BENCHMARKS["crypto_extremes"], "crypto"
    )
    report.warn(
        "sentiment_lag_deferred",
        "Sentiment-score neutrality and decision-date lag validation are deferred until an authorised sentiment stage; Stage 4A creates no score.",
    )
    return report


def validate_deterministic_rerun(
    first: dict[str, pd.DataFrame], second: dict[str, pd.DataFrame]
) -> ValidationResult:
    """Compare controlled in-memory pipeline reruns, including dtypes and order."""
    if tuple(first) != tuple(second):
        return ValidationResult(
            "deterministic_rerun",
            "BLOCK",
            "Controlled rerun returned a different set or order of artifacts.",
            tuple(second),
            tuple(first),
        )
    for name in first:
        try:
            pd.testing.assert_frame_equal(
                first[name], second[name], check_dtype=True, check_like=False
            )
        except AssertionError as exc:
            return ValidationResult(
                "deterministic_rerun",
                "BLOCK",
                f"Controlled rerun differed for {name}: {str(exc).splitlines()[0]}",
            )
    return ValidationResult(
        "deterministic_rerun",
        "PASS",
        "Controlled rerun reproduced schemas, dtypes, order, missingness, and values.",
    )


__all__ = [
    "ALIGNED_CRYPTO_COLUMNS",
    "BENCHMARKS",
    "CLEAN_NEWS_COLUMNS",
    "COMBINED_ASSETS",
    "COVERAGE_COLUMNS",
    "CRYPTO_CUTOFF",
    "CRYPTO_PRICE_COLUMNS",
    "CRYPTO_RETURN_COLUMNS",
    "CRYPTO_TICKERS",
    "EQUITY_PRICE_COLUMNS",
    "EQUITY_RETURN_COLUMNS",
    "EQUITY_TICKERS",
    "MAPPING_COLUMNS",
    "RAW_NEWS_COLUMNS",
    "SECTOR_DISPLAY_LABELS",
    "SECTOR_DISPLAY_ORDER",
    "SIX_UNMAPPED",
    "SOURCE_SECTORS",
    "ContractViolation",
    "ValidationReport",
    "ValidationResult",
    "find_extreme_observations",
    "validate_data_foundation",
    "validate_deterministic_rerun",
]
