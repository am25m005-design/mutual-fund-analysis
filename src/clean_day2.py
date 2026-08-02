import pandas as pd
from pathlib import Path

# ==========================================
# Project Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW = BASE_DIR / "data" / "raw"
PROCESSED = BASE_DIR / "data" / "processed"

PROCESSED.mkdir(parents=True, exist_ok=True)

# ==========================================
# Files to Process
# ==========================================

datasets = {
    "01_fund_master.csv": "clean_fund_master.csv",
    "02_nav_history.csv": "clean_nav.csv",
    "03_aum_by_fund_house.csv": "clean_aum.csv",
    "04_monthly_sip_inflows.csv": "clean_sip_inflows.csv",
    "05_category_inflows.csv": "clean_category_inflows.csv",
    "06_industry_folio_count.csv": "clean_folio_count.csv",
    "07_scheme_performance.csv": "clean_performance.csv",
    "08_investor_transactions.csv": "clean_transactions.csv",
    "09_portfolio_holdings.csv": "clean_portfolio.csv",
    "10_benchmark_indices.csv": "clean_benchmark.csv",
}

# ==========================================
# Cleaning Function
# ==========================================

def clean_dataset(df, filename):

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Trim spaces
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip()

    # Convert date columns
    for col in df.columns:
        if "date" in col.lower() or "month" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Convert numeric columns
    keywords = [
        "nav", "aum", "amount", "return",
        "expense", "ratio", "holding",
        "weight", "folio", "inflow"
    ]

    for col in df.columns:
        if any(k in col.lower() for k in keywords):

            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("%", "", regex=False)
            )

            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ---------- File Specific Cleaning ----------

    if filename == "02_nav_history.csv":

        if {"amfi_code", "date", "nav"}.issubset(df.columns):
            df = df.sort_values(["amfi_code", "date"])
            df["nav"] = df.groupby("amfi_code")["nav"].ffill()
            df = df[df["nav"] > 0]

    elif filename == "03_aum_by_fund_house.csv":

        for col in df.columns:
            if "aum" in col.lower():
                df = df[df[col] >= 0]

    elif filename == "04_monthly_sip_inflows.csv":

        for col in df.columns:
            if "sip" in col.lower():
                df = df[df[col] >= 0]

    elif filename == "07_scheme_performance.csv":

        if "expense_ratio" in df.columns:
            print("\nExpense Ratio Anomalies")
            print(df[(df["expense_ratio"] < 0.1) |
                     (df["expense_ratio"] > 2.5)])

    elif filename == "08_investor_transactions.csv":

        if "amount" in df.columns:
            df = df[df["amount"] > 0]

    elif filename == "09_portfolio_holdings.csv":

        for col in df.columns:
            if "holding" in col.lower() or "weight" in col.lower():
                df = df[(df[col] >= 0) & (df[col] <= 100)]

    return df

# ==========================================
# Process All Files
# ==========================================

for raw_file, output_file in datasets.items():

    input_path = RAW / raw_file

    if not input_path.exists():
        print(f"File not found: {raw_file}")
        continue

    print("=" * 60)
    print(f"Processing {raw_file}")

    df = pd.read_csv(input_path)

    print("Original Shape :", df.shape)

    df = clean_dataset(df, raw_file)

    print("Cleaned Shape  :", df.shape)

    output_path = PROCESSED / output_file

    df.to_csv(output_path, index=False)

    print(f"Saved -> {output_path}")

print("\nAll datasets cleaned successfully!")