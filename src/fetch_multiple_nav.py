"""
Task 5: Fetch NAV history for multiple mutual fund schemes.

This script:
1. Downloads NAV history for five mutual funds.
2. Saves each fund's NAV history as a CSV file.
"""

from pathlib import Path
import requests
import pandas as pd

# AMFI Scheme Codes
SCHEMES = {
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841,
}

BASE_URL = "https://api.mfapi.in/mf/"


def fetch_nav(scheme_code):
    """Fetch NAV data for a mutual fund."""

    try:
        response = requests.get(f"{BASE_URL}{scheme_code}", timeout=30)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as error:
        print(f"Failed to fetch Scheme {scheme_code}")
        print(error)
        return None


def save_nav(data, filename):
    """Save NAV history to CSV."""

    output_dir = Path("data") / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    nav_df = pd.DataFrame(data["data"])

    output_file = output_dir / filename

    nav_df.to_csv(output_file, index=False)

    print(f"Saved: {output_file}")


def main():

    print("=" * 80)
    print("Fetching NAV History")
    print("=" * 80)

    successful = 0

    for fund_name, scheme_code in SCHEMES.items():

        print(f"\nFetching {fund_name}...")

        data = fetch_nav(scheme_code)

        if data is None:
            continue

        print(f"Scheme : {data['meta']['scheme_name']}")
        print(f"Latest NAV : {data['data'][0]['nav']}")
        print(f"Date : {data['data'][0]['date']}")

        save_nav(data, f"{fund_name}.csv")

        successful += 1

    print("\n" + "=" * 80)
    print(f"Successfully downloaded {successful}/{len(SCHEMES)} schemes.")
    print("=" * 80)


if __name__ == "__main__":
    main()