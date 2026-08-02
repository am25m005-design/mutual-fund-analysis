from pathlib import Path
import sqlite3

import pandas as pd
from sqlalchemy import create_engine

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE = BASE_DIR / "database" / "bluestock_mf.db"

SCHEMA = BASE_DIR / "sql" / "schema.sql"

PROCESSED = BASE_DIR / "data" / "processed"

# ==========================================================
# DATABASE
# ==========================================================

DATABASE.parent.mkdir(exist_ok=True)

engine = create_engine(f"sqlite:///{DATABASE}")

# ==========================================================
# CREATE DATABASE
# ==========================================================

print("=" * 70)
print("CREATING SQLITE DATABASE")
print("=" * 70)

with sqlite3.connect(DATABASE) as conn:

    with open(SCHEMA, "r", encoding="utf-8") as f:

        conn.executescript(f.read())

print("Schema Created Successfully.\n")

# ==========================================================
# FILES
# ==========================================================

FILES = {

    "fund_master":
        PROCESSED / "clean_fund_master.csv",

    "nav_history":
        PROCESSED / "clean_nav.csv",

    "investor_transactions":
        PROCESSED / "clean_transactions.csv",

    "scheme_performance":
        PROCESSED / "clean_performance.csv",

    "aum_history":
        PROCESSED / "clean_aum.csv"

}

# ==========================================================
# LOAD TABLE
# ==========================================================


def load_table(table_name, csv_path):

    if not csv_path.exists():

        print(f"{csv_path.name} NOT FOUND")

        return

    df = pd.read_csv(csv_path)

    df.to_sql(

        table_name,

        engine,

        if_exists="append",

        index=False

    )

    print(f"{table_name:<25} {len(df):>8} rows loaded")


# ==========================================================
# LOAD ALL TABLES
# ==========================================================

print("=" * 70)
print("LOADING TABLES")
print("=" * 70)

for table, file in FILES.items():

    load_table(table, file)

print()

# ==========================================================
# VERIFY
# ==========================================================

print("=" * 70)
print("VERIFY TABLES")
print("=" * 70)

with sqlite3.connect(DATABASE) as conn:

    cursor = conn.cursor()

    for table in FILES.keys():

        cursor.execute(f"SELECT COUNT(*) FROM {table}")

        rows = cursor.fetchone()[0]

        print(f"{table:<25} {rows}")

print()

print("=" * 70)
print("DATABASE CREATED SUCCESSFULLY")
print("=" * 70)

print(f"\nDatabase Location:\n{DATABASE}")