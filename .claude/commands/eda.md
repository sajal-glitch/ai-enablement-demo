# /eda — Exploratory Data Analysis Command

Run a standardised EDA on a CSV file and produce a structured report.

## Instructions

When this command is triggered with a CSV filepath:

1. Read the CSV file using pandas
2. Report the following in order:
   - **Shape**: rows × columns, column names
   - **Data types**: dtype for each column
   - **Missing values**: count and % per column (skip if none)
   - **Numeric summary**: describe() for all numeric columns
   - **Outliers**: IQR method — flag columns with >0 outliers
   - **Categorical breakdown**: value_counts() for columns with ≤10 unique values
   - **Correlations**: correlation matrix for numeric columns
3. End with a **Key Observations** section: 3–5 bullet points summarising
   the most important findings (data quality issues, skewed distributions,
   strong correlations, outliers to investigate)
4. Suggest **Next Steps**: 2–3 recommended preprocessing or feature engineering
   actions based on what you observed

## Output format

Plain text with clear section headers. Use emoji icons for each section
(📐 Shape, 🔤 Types, ❓ Missing, 📊 Summary, ⚠️ Outliers, 🏷️ Categories,
🔗 Correlations, 💡 Key Observations, 👉 Next Steps).

## Usage

```
/eda data/sales_sample.csv
/eda path/to/any_dataset.csv
```

## Notes

- This command does NOT modify the CSV file
- All analysis is read-only
- If the file has more than 1M rows, sample 100k rows and note this
