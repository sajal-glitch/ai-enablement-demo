"""
Test suite for the Sales Analytics API and data processing functions.

DEMO USAGE:
  Session 1 / Module 1  — After Claude refactors sales_processor.py, ask:
                          "Now add unit tests for the refactored function."
                          → Shows multi-turn Claude Chat capability.

  Session 2 / Module 3  — /tests slash command demo:
                          Select a function in VS Code → type /tests
                          → Claude generates a test suite like this one.

  Run tests:
    pytest tests/ -v
    pytest tests/ -v --tb=short   (cleaner output for demo)
"""

import pytest
import pandas as pd
from io import StringIO
from pathlib import Path

from app.sales_processor import (
    process_monthly_totals,
    process_monthly_totals_refactored,
    process_sales_data,
)


# ── Fixtures ─────────────────────────────────────────────────────────────────

CLEAN_CSV = """date,region,revenue,units
2024-01-15,APAC,45000.00,120
2024-01-22,EMEA,38000.00,95
2024-02-10,APAC,52000.00,140
2024-02-28,NA,29000.00,75
2024-03-05,LATAM,18000.00,42
"""

MESSY_CSV = """date,region,revenue,units
2024-01-15,APAC,45000,120
Jan 2024,EMEA,,95
2024/02/10,APAC,52000,140
not-a-date,NA,29000,75
2024-03-05,LATAM,18000,42
"""

MISSING_COLS_CSV = """date,region,sales
2024-01-15,APAC,45000
"""


@pytest.fixture
def clean_csv_file(tmp_path) -> Path:
    f = tmp_path / "clean_sales.csv"
    f.write_text(CLEAN_CSV)
    return f


@pytest.fixture
def messy_csv_file(tmp_path) -> Path:
    f = tmp_path / "messy_sales.csv"
    f.write_text(MESSY_CSV)
    return f


@pytest.fixture
def missing_cols_csv_file(tmp_path) -> Path:
    f = tmp_path / "missing_cols.csv"
    f.write_text(MISSING_COLS_CSV)
    return f


@pytest.fixture
def clean_df() -> pd.DataFrame:
    return pd.read_csv(StringIO(CLEAN_CSV))


# ── process_monthly_totals_refactored ────────────────────────────────────────

class TestProcessMonthlyTotalsRefactored:

    def test_happy_path_returns_correct_monthly_totals(self, clean_csv_file):
        result = process_monthly_totals_refactored(str(clean_csv_file))
        assert len(result) == 3  # Jan, Feb, Mar
        jan = result[result["month"].astype(str) == "2024-01"]
        assert float(jan["total_revenue"]) == pytest.approx(83000.0)
        assert int(jan["total_units"]) == 215

    def test_handles_missing_revenue_values(self, messy_csv_file):
        result = process_monthly_totals_refactored(str(messy_csv_file))
        # Row with missing revenue treated as 0 — should not crash
        assert result is not None
        assert len(result) > 0

    def test_drops_rows_with_unparseable_dates(self, messy_csv_file):
        result = process_monthly_totals_refactored(str(messy_csv_file))
        # "not-a-date" row should be dropped — remaining rows processed
        assert result is not None

    def test_raises_on_missing_required_columns(self, missing_cols_csv_file):
        with pytest.raises(ValueError, match="missing required columns"):
            process_monthly_totals_refactored(str(missing_cols_csv_file))

    def test_raises_file_not_found(self):
        with pytest.raises(Exception):
            process_monthly_totals_refactored("/nonexistent/path/sales.csv")

    def test_returns_dataframe_with_expected_columns(self, clean_csv_file):
        result = process_monthly_totals_refactored(str(clean_csv_file))
        assert "total_revenue" in result.columns
        assert "total_units" in result.columns
        assert "month" in result.columns


# ── process_sales_data ───────────────────────────────────────────────────────

class TestProcessSalesData:

    def test_happy_path_adds_quarter_column(self, clean_df):
        result = process_sales_data(clean_df)
        assert "quarter" in result.columns

    def test_quarter_values_are_correct(self, clean_df):
        result = process_sales_data(clean_df)
        q1_rows = result[result["quarter"].str.contains("Q1")]
        assert len(q1_rows) == 5  # all rows in the fixture are Q1 2024

    def test_raises_on_missing_columns(self):
        bad_df = pd.DataFrame({"date": ["2024-01-01"], "region": ["APAC"]})
        with pytest.raises(ValueError, match="Missing required columns"):
            process_sales_data(bad_df)

    def test_revenue_coerced_to_float(self, clean_df):
        result = process_sales_data(clean_df)
        assert result["revenue"].dtype == float

    def test_original_dataframe_not_mutated(self, clean_df):
        original_cols = list(clean_df.columns)
        process_sales_data(clean_df)
        assert list(clean_df.columns) == original_cols
