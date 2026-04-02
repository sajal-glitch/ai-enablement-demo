"""
Exploratory Data Analysis (EDA) Script
========================================
DEMO USAGE — Session 2 / Module 3 (Agent Skills & Slash Commands):

This script is the TARGET for the /eda custom slash command demo.

WHAT TO SHOW:
  1. Open Claude Code in terminal from the project root.
  2. Run: /eda data/sales_sample.csv
  3. Claude will automatically run a standardised EDA:
       - Data types and shape
       - Missing value counts
       - Distribution summary (describe())
       - Correlation matrix for numeric columns
       - Identifies outliers
       - Produces a summary report

The /eda command definition lives in: .claude/commands/eda.md

This file shows what the EDA output LOOKS LIKE so participants
understand what the skill is automating.

ALSO: run this script manually before the demo to show the "before" state:
  python app/eda.py data/sales_sample.csv
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path


def run_eda(filepath: str) -> None:
    """
    Run a standardised EDA on a CSV file and print a structured report.

    This is the function the /eda slash command automates.
    """
    path = Path(filepath)
    if not path.exists():
        print(f"[ERROR] File not found: {filepath}")
        sys.exit(1)

    df = pd.read_csv(filepath)

    print("=" * 60)
    print(f"EDA REPORT: {path.name}")
    print("=" * 60)

    # ── Shape ────────────────────────────────────────────────────
    print(f"\n[SHAPE]  {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")

    # ── Data Types ───────────────────────────────────────────────
    print("\n[DATA TYPES]")
    print(df.dtypes.to_string())

    # ── Missing Values ───────────────────────────────────────────
    print("\n[MISSING VALUES]")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_report = pd.DataFrame({"count": missing, "pct": missing_pct})
    missing_report = missing_report[missing_report["count"] > 0]
    if missing_report.empty:
        print("  No missing values found.")
    else:
        print(missing_report.to_string())

    # ── Numeric Summary ──────────────────────────────────────────
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print("\n[NUMERIC SUMMARY]")
        print(df[numeric_cols].describe().round(2).to_string())

    # ── Outlier Detection (IQR method) ───────────────────────────
    print("\n[OUTLIERS — IQR method]")
    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        outliers = df[(df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)]
        if len(outliers) > 0:
            print(f"  {col}: {len(outliers)} outliers detected")

    # ── Categorical Columns ──────────────────────────────────────
    cat_cols = df.select_dtypes(include=["object"]).columns
    if len(cat_cols) > 0:
        print("\n[CATEGORICAL COLUMNS — value counts]")
        for col in cat_cols:
            if df[col].nunique() <= 10:
                print(f"\n  {col}:")
                print(df[col].value_counts().to_string(header=False))

    # ── Correlations ─────────────────────────────────────────────
    if len(numeric_cols) > 1:
        print("\n[CORRELATIONS]")
        print(df[numeric_cols].corr().round(3).to_string())

    print("\n" + "=" * 60)
    print("EDA COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "data/sales_sample.csv"
    run_eda(filepath)
