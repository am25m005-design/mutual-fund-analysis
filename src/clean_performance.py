from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/07_scheme_performance.csv")
OUTPUT_FILE = Path("data/processed/clean_performance.csv")


def load_data():
    return pd.read_csv(RAW_FILE)


def clean_data(df):

    numeric_columns = [
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "aum_crore",
        "expense_ratio_pct",
        "morningstar_rating"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    invalid_returns = (
        df[[
            "return_1yr_pct",
            "return_3yr_pct",
            "return_5yr_pct"
        ]]
        .isna()
        .any(axis=1)
        .sum()
    )

    df["negative_sharpe"] = df["sharpe_ratio"] < 0

    df["invalid_expense_ratio"] = (
        (df["expense_ratio_pct"] < 0.1) |
        (df["expense_ratio_pct"] > 2.5)
    )

    duplicate_records = df.duplicated().sum()
    df = df.drop_duplicates()

    summary = {
        "invalid_returns": invalid_returns,
        "negative_sharpe": int(df["negative_sharpe"].sum()),
        "invalid_expense_ratio": int(df["invalid_expense_ratio"].sum()),
        "duplicate_records": duplicate_records,
        "final_records": len(df),
    }

    return df, summary


def save_data(df):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)


def main():

    print("=" * 70)
    print("SCHEME PERFORMANCE DATA CLEANING")
    print("=" * 70)

    df = load_data()

    print(f"Original Records : {len(df)}")

    clean_df, summary = clean_data(df)

    save_data(clean_df)

    print("\nCleaning Summary")
    print("-" * 70)
    print(f"Invalid Return Values      : {summary['invalid_returns']}")
    print(f"Negative Sharpe Ratios     : {summary['negative_sharpe']}")
    print(f"Invalid Expense Ratios     : {summary['invalid_expense_ratio']}")
    print(f"Duplicate Records Removed  : {summary['duplicate_records']}")
    print(f"Final Records              : {summary['final_records']}")

    print(f"\nClean dataset saved to:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    