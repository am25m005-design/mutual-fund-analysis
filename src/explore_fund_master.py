"""
Task 6: Explore Fund Master Dataset

This script:
1. Loads the fund master dataset.
2. Prints basic information.
3. Displays unique fund houses, categories,
   sub-categories, and risk grades.
"""

from pathlib import Path
import pandas as pd


def main():

    file_path = Path("data") / "raw" / "01_fund_master.csv"

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("Fund master file not found.")
        return

    print("=" * 80)
    print("FUND MASTER DATASET")
    print("=" * 80)

    print(f"\nNumber of Records : {len(df)}")
    print(f"Number of Columns : {len(df.columns)}")

    print("\nColumns:")
    print(df.columns.tolist())

    # --------- Find matching column names ---------

    fund_house_col = next((c for c in df.columns if "house" in c.lower()), None)
    category_col = next((c for c in df.columns if "category" in c.lower() and "sub" not in c.lower()), None)
    subcategory_col = next((c for c in df.columns if "sub" in c.lower() and "category" in c.lower()), None)
    risk_col = next((c for c in df.columns if "risk" in c.lower()), None)
    scheme_code_col = next((c for c in df.columns if "code" in c.lower()), None)

    if fund_house_col:
        print("\nUnique Fund Houses:")
        print(df[fund_house_col].dropna().sort_values().unique())

    if category_col:
        print("\nUnique Categories:")
        print(df[category_col].dropna().sort_values().unique())

    if subcategory_col:
        print("\nUnique Sub-Categories:")
        print(df[subcategory_col].dropna().sort_values().unique())

    if risk_col:
        print("\nUnique Risk Grades:")
        print(df[risk_col].dropna().sort_values().unique())

    if scheme_code_col:
        print("\nAMFI Scheme Code Summary")
        print(df[scheme_code_col].describe())


if __name__ == "__main__":
    main()