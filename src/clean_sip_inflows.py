from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/04_monthly_sip_inflows.csv")
OUTPUT_FILE = Path("data/processed/clean_sip_inflows.csv")


def load_data():
    return pd.read_csv(RAW_FILE)


def clean_data(df):

    df["month"] = pd.to_datetime(
        df["month"],
        format="%Y-%m",
        errors="coerce"
    )

    invalid_dates = df["month"].isna().sum()
    df = df.dropna(subset=["month"])

    numeric_columns = [
        "sip_inflow_crore",
        "active_sip_accounts_crore",
        "new_sip_accounts_lakh",
        "sip_aum_lakh_crore"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    invalid_values = (
        (df[numeric_columns] < 0)
        .any(axis=1)
        .sum()
    )

    df = df[
        (df[numeric_columns] >= 0)
        .all(axis=1)
    ]

    duplicate_records = df.duplicated().sum()
    df = df.drop_duplicates()

    summary = {
        "invalid_dates": invalid_dates,
        "invalid_values": invalid_values,
        "duplicate_records": duplicate_records,
        "final_records": len(df)
    }

    return df, summary


def save_data(df):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)


def main():

    print("=" * 70)
    print("MONTHLY SIP INFLOWS DATA CLEANING")
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