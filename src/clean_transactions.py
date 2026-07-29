from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/08_investor_transactions.csv")
OUTPUT_FILE = Path("data/processed/clean_transactions.csv")


def load_data():
    return pd.read_csv(RAW_FILE)


def clean_data(df):

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce"
    )

    invalid_dates = df["transaction_date"].isna().sum()
    df = df.dropna(subset=["transaction_date"])

    df["transaction_type"] = (
        df["transaction_type"]
        .str.strip()
        .str.title()
    )

    df["kyc_status"] = (
        df["kyc_status"]
        .str.strip()
        .str.title()
    )

    df["amount_inr"] = pd.to_numeric(
        df["amount_inr"],
        errors="coerce"
    )

    invalid_amounts = (df["amount_inr"] <= 0).sum()
    df = df[df["amount_inr"] > 0]

    duplicate_records = df.duplicated().sum()
    df = df.drop_duplicates()

    summary = {
        "invalid_dates": invalid_dates,
        "invalid_amounts": invalid_amounts,
        "duplicate_records": duplicate_records,
        "final_records": len(df),
    }

    return df, summary


def save_data(df):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)


def main():

    print("=" * 70)
    print("INVESTOR TRANSACTION DATA CLEANING")
    print("=" * 70)

    df = load_data()

    print(f"Original Records : {len(df)}")

    clean_df, summary = clean_data(df)

    save_data(clean_df)

    print("\nCleaning Summary")
    print("-" * 70)
    print(f"Invalid Dates Removed     : {summary['invalid_dates']}")
    print(f"Invalid Amounts Removed   : {summary['invalid_amounts']}")
    print(f"Duplicate Records Removed : {summary['duplicate_records']}")
    print(f"Final Records             : {summary['final_records']}")

    print(f"\nClean dataset saved to:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()