"""
Task 3: Load all CSV datasets using pandas.

This script:
1. Reads all CSV files from the data/raw directory.
2. Displays dataset information.
3. Stores each dataset in a dictionary for future use.
"""
from pathlib import Path
import pandas as pd


def inspect_dataset(df):
    """Print basic data quality checks."""

    print(f"Shape : {df.shape}")

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nMissing Values:")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.sum() > 0 else "No missing values.")

    print(f"\nDuplicate Rows : {df.duplicated().sum()}")

    duplicate_cols = df.columns[df.columns.duplicated()].tolist()
    if duplicate_cols:
        print(f"Duplicate Columns : {duplicate_cols}")
    else:
        print("Duplicate Columns : None")


def main():

    data_folder = Path("data") / "raw"

    csv_files = sorted(data_folder.glob("*.csv"))

    print(f"\nFound {len(csv_files)} CSV files.\n")

    for file in csv_files:

        print("=" * 80)
        print(f"Dataset : {file.name}")
        print("=" * 80)

        try:
            df = pd.read_csv(file)

            inspect_dataset(df)

        except Exception as e:
            print(f"Error reading {file.name}")
            print(e)

        print("\n")


if __name__ == "__main__":
    main() 