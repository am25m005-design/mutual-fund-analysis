"""
Task 1: Clean NAV History Dataset

This script:
1. Loads the NAV history dataset.
2. Converts the date column to datetime.
3. Sorts records by AMFI code and date.
4. Removes duplicate records.
5. Forward-fills missing NAV values.
6. Removes invalid NAV values.
7. Saves the cleaned dataset.
"""

from pathlib import Path
import pandas as pd

# -------------------------------------------------------------------
# File Paths
# -------------------------------------------------------------------

RAW_FILE = Path("data/raw/02_nav_history.csv")
OUTPUT_FILE = Path("data/processed/clean_nav.csv")


def load_data():
    """Load the raw NAV history dataset."""
    return pd.read_csv(RAW_FILE)


def clean_data(df):
    """Clean the NAV history dataset."""

    # Convert date column
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Remove rows with invalid dates
    invalid_dates = df["date"].isna().sum()
    df = df.dropna(subset=["date"])

    # Convert NAV column to numeric
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

    # Sort data
    df = df.sort_values(
        by=["amfi_code", "date"]
    ).reset_index(drop=True)

    # Remove duplicate records
    duplicate_records = df.duplicated(
        subset=["amfi_code", "date"]
    ).sum()

    df = df.drop_duplicates(
        subset=["amfi_code", "date"]
    )

    # Forward-fill missing NAV values within each scheme
    df["nav"] = (
        df.groupby("amfi_code")["nav"]
        .ffill()
    )

    # Remove invalid NAV values
    invalid_nav = (df["nav"] <= 0).sum()

    df = df[df["nav"] > 0]

    summary = {
        "invalid_dates": invalid_dates,
        "duplicate_records": duplicate_records,
        "invalid_nav": invalid_nav,
        "final_records": len(df),
    }

    return df, summary


def save_data(df):
    """Save cleaned dataset."""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)


def main():

    print("=" * 70)
    print("NAV HISTORY DATA CLEANING")
    print("=" * 70)

    df = load_data()

    print(f"Original Records : {len(df)}")

    clean_df, summary = clean_data(df)

    save_data(clean_df)

    print("\nCleaning Summary")
    print("-" * 70)
    print(f"Invalid Dates Removed     : {summary['invalid_dates']}")
    print(f"Duplicate Records Removed : {summary['duplicate_records']}")
    print(f"Invalid NAV Removed       : {summary['invalid_nav']}")
    print(f"Final Records             : {summary['final_records']}")

    print(f"\nClean dataset saved to:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()