from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


DATABASE = "sqlite:///bluestock_mf.db"

FILES = {
    "dim_fund": "data/raw/01_fund_master.csv",
    "fact_nav": "data/processed/clean_nav.csv",
    "fact_transactions": "data/processed/clean_transactions.csv",
    "fact_performance": "data/processed/clean_performance.csv",
}


def load_csv(file_path):
    return pd.read_csv(file_path)


def load_table(df, table_name, engine):
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )


def verify_table(table_name, engine):
    query = f"SELECT COUNT(*) AS rows FROM {table_name}"
    rows = pd.read_sql(query, engine)

    print(f"{table_name:<20} {rows.iloc[0, 0]} rows")


def main():

    print("=" * 70)
    print("LOADING DATA INTO SQLITE DATABASE")
    print("=" * 70)

    engine = create_engine(DATABASE)

    for table_name, file_path in FILES.items():

        path = Path(file_path)

        if not path.exists():
            print(f"File not found : {path}")
            continue

        print(f"\nLoading {path.name} ...")

        df = load_csv(path)

        load_table(df, table_name, engine)

        print(f"{len(df)} records inserted.")

    print("\n" + "=" * 70)
    print("DATABASE VERIFICATION")
    print("=" * 70)

    for table_name in FILES.keys():
        verify_table(table_name, engine)

    print("\nDatabase created successfully.")
    print("Database File : bluestock_mf.db")


if __name__ == "__main__":
    main()
    