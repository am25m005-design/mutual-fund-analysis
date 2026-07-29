import pandas as pd
from sqlalchemy import create_engine

# 1. Create connection engine
engine = create_engine("sqlite:///bluestock_mf.db")

# 2. Map cleaned CSV files to target database tables
csv_to_table = {
    "data/processed/clean_fund_master.csv": "dim_fund",
    "data/processed/clean_nav_history.csv": "fact_nav",
    "data/processed/clean_investor_transactions.csv": "fact_transactions",
    "data/processed/clean_scheme_performance.csv": "fact_performance",
    "data/processed/clean_portfolio_holdings.csv": "fact_portfolio",
    "data/processed/clean_aum_by_fund_house.csv": "fact_aum",
    "data/processed/clean_monthly_sip_inflows.csv": "fact_sip_industry",
}

# 3. Load each file into SQLite
for csv_file, table_name in csv_to_table.items():
    df = pd.read_csv(csv_file)
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into {table_name}")

print("\nDatabase load complete!")