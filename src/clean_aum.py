from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/03_aum_by_fund_house.csv")
OUTPUT_FILE = Path("data/processed/clean_aum.csv")


def load_data():
    return pd.read_csv(RAW_FILE)


def clean_data(df):

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    invalid_dates = df["date"].isna().sum()
    df = df.dropna(subset=["date"])

    df["fund_house"] = (
        df["fund_house"]
        .str.strip()
        .str.title()
    )

    numeric_columns = [
        "aum_lakh_crore",
        "aum_crore",
        "num_schemes"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    invalid_values = (
        (df["aum_lakh_crore"] < 0) |
        (df["aum_crore"] < 0) |
        (df["num_schemes"] <= 0)
    ).sum()

    df = df[
        (df["aum_lakh_crore"] >= 0) &
        (df["aum_crore"] >= 0) &
        (df["num_schemes"] > 0)
    ]

    duplicate_records = df.duplicated().sum()
    df = df.drop_duplicates()

    summary = {
        "invalid_dates": invalid_dates,
        "invalid_values": invalid_values,
        "duplicate_records": duplicate_records,
        "final_records": len(df),
    }

    return df, summary


def save_data(df):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)


def main():

    print("=" * 70)
    print("AUM DATA CLEANING")
    print("=" * 70)

    df = load_data()

    print(f"Original Records : {len(df)}")

    clean_df, summary = clean_data(df)

    save_data(clean_df)

    print("\nCleaning Summary")
    print("-" * 70)
    print(f"Invalid Dates Removed     : {summary['invalid_dates']}")
    print(f"Invalid Values Removed    : {summary['invalid_values']}")
    print(f"Duplicate Records Removed : {summary['duplicate_records']}")
    print(f"Final Records             : {summary['final_records']}")

    print(f"\nClean dataset saved to:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()