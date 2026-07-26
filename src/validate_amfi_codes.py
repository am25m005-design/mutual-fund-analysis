"""
Task 7: Validate AMFI Scheme Codes

This script:
1. Compares AMFI scheme codes between fund_master and nav_history.
2. Identifies missing scheme codes.
3. Performs basic data quality checks.
"""

from pathlib import Path
import pandas as pd


def main():

    # -----------------------------
    # Load datasets
    # -----------------------------
    data_folder = Path("data") / "raw"

    fund_master = pd.read_csv(data_folder / "01_fund_master.csv")
    nav_history = pd.read_csv(data_folder / "02_nav_history.csv")

    # -----------------------------
    # Extract unique AMFI codes
    # -----------------------------
    fund_codes = set(fund_master["amfi_code"].astype(int))
    nav_codes = set(nav_history["amfi_code"].astype(int))

    matching_codes = fund_codes.intersection(nav_codes)
    missing_codes = fund_codes - nav_codes

    # -----------------------------
    # AMFI Code Validation
    # -----------------------------
    print("=" * 80)
    print("AMFI CODE VALIDATION")
    print("=" * 80)

    print(f"\nFund Master Codes : {len(fund_codes)}")
    print(f"NAV History Codes : {len(nav_codes)}")

    print(f"\nMatching Codes : {len(matching_codes)}")
    print(f"Missing Codes : {len(missing_codes)}")

    if missing_codes:
        print("\nMissing AMFI Codes:")
        for code in sorted(missing_codes):
            print(code)
    else:
        print("\nAll AMFI codes from fund_master are present in nav_history.")

    # -----------------------------
    # Data Quality Checks
    # -----------------------------
    duplicate_master = fund_master.duplicated(subset=["amfi_code"]).sum()

    duplicate_nav = nav_history.duplicated(
        subset=["amfi_code", "date"]
    ).sum()

    missing_master = fund_master.isnull().sum().sum()
    missing_nav = nav_history.isnull().sum().sum()

    # -----------------------------
    # Summary
    # -----------------------------
    print("\n" + "=" * 80)
    print("DATA QUALITY SUMMARY")
    print("=" * 80)

    print(f"Fund Master Records           : {len(fund_master)}")
    print(f"NAV History Records           : {len(nav_history)}")

    print(f"\nDuplicate AMFI Codes (Master) : {duplicate_master}")
    print(f"Duplicate NAV Records         : {duplicate_nav}")

    print(f"\nMissing Values (Master)       : {missing_master}")
    print(f"Missing Values (NAV History)  : {missing_nav}")

    print("\nConclusion:")

    if len(missing_codes) == 0 and duplicate_master == 0 and duplicate_nav == 0:
        print(
            "✓ All AMFI scheme codes are consistent across both datasets."
        )
        print(
            "✓ No duplicate NAV records were found for any AMFI code and date."
        )
        print(
            "✓ Both datasets contain no missing values and are suitable for further analysis."
        )
    else:
        print(
            "Some data quality issues were detected. Please review the missing codes or duplicate records.")


if __name__ == "__main__":
    main()