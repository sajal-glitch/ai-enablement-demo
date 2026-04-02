"""
Sales Data Processor
=====================
This module is the DEMO TARGET for Session 1 / Module 1 — Claude Chat demo.

WHAT TO DO IN THE DEMO:
  1. Show this file to participants. Point out that process_monthly_totals()
     breaks on missing values and inconsistent date formats.
  2. Open claude.ai in the browser.
  3. Paste the function below and use this prompt:

     "I have a Python function that reads a CSV of sales data and computes
     monthly totals. The function breaks if a row has missing values or the
     date column has inconsistent formats. Here is the current code: [paste].
     Refactor this to handle missing values gracefully, normalize date formats,
     and add type hints. Explain your reasoning for each change."

  4. Show the GOOD prompt vs BAD prompt contrast:
     BAD:  "fix this code"
     GOOD: the full prompt above with context + constraints + output format

  5. After Claude refactors it, follow up:
     "Now add unit tests for the refactored function."
     → This demonstrates multi-turn capability.

ALSO USED FOR:
  - Guided Practice (Session 1 / Module 1): participants ask Claude Code to
    add a docstring to process_monthly_totals()
  - CLAUDE.md exercise (Session 2 / Module 2): participants read this file
    to understand code conventions
"""

import pandas as pd


# ─────────────────────────────────────────────────────────────────────────────
# BROKEN VERSION — show this first in the demo
# Issues:
#   1. No type hints
#   2. Crashes on NaN values in revenue/units columns
#   3. Crashes on inconsistent date formats (e.g. "Jan 2024" vs "2024-01-15")
#   4. No docstring
#   5. No error handling
# ─────────────────────────────────────────────────────────────────────────────

def process_monthly_totals(filepath):
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('month').agg({'revenue': 'sum', 'units': 'sum'})
    return monthly


# ─────────────────────────────────────────────────────────────────────────────
# REFERENCE: what Claude should produce after the demo prompt
# Shown AFTER the demo — participants see the before/after quality gap.
# ─────────────────────────────────────────────────────────────────────────────

def process_monthly_totals_refactored(filepath: str) -> pd.DataFrame:
    """
    Read a sales CSV and compute monthly revenue and unit totals.

    Handles missing values and inconsistent date formats gracefully.

    Args:
        filepath: Path to the CSV file. Expected columns: date, region,
                  revenue, units.

    Returns:
        DataFrame indexed by month (Period[M]) with columns:
        total_revenue (float) and total_units (int).

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If required columns are missing from the CSV.
    """
    required_columns = {"date", "revenue", "units"}

    df = pd.read_csv(filepath)

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    invalid_dates = df["date"].isna().sum()
    if invalid_dates > 0:
        print(f"Warning: {invalid_dates} rows had unparseable dates and will be dropped.")
    df = df.dropna(subset=["date"])

    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0.0)
    df["units"] = pd.to_numeric(df["units"], errors="coerce").fillna(0).astype(int)

    df["month"] = df["date"].dt.to_period("M")

    monthly = (
        df.groupby("month")
        .agg(total_revenue=("revenue", "sum"), total_units=("units", "sum"))
        .reset_index()
    )
    return monthly


def process_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process a sales DataFrame: validate schema, parse dates, add quarter column.

    This is the function from the Prompt Engineering 'Good Prompt' example
    (Session 1 / Module 3).

    Args:
        df: DataFrame with columns [date, region, revenue, units].

    Returns:
        Processed DataFrame with an additional 'quarter' column.

    Raises:
        ValueError: If required columns are missing.
    """
    required = {"date", "region", "revenue", "units"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0.0)
    df["units"] = pd.to_numeric(df["units"], errors="coerce").fillna(0).astype(int)
    df["quarter"] = df["date"].dt.to_period("Q").astype(str)

    return df
