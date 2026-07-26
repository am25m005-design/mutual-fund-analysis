"""
Task 4: Fetch live NAV data from mfapi.in API

This script:
1. Fetches mutual fund NAV history.
2. Parses the JSON response.
3. Saves the NAV history as a CSV file.
"""

from pathlib import Path
import requests
import pandas as pd
print("Script started...")

SCHEME_CODE = "125497"

API_URL = f"https://api.mfapi.in/mf/{SCHEME_CODE}"


def fetch_nav():
    """Fetch NAV data from mfapi.in"""

    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        print(f"Request Failed: {error}")
        return None


def save_nav_history(data):
    """Save NAV history as CSV"""

    output_dir = Path("data") / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    nav_df = pd.DataFrame(data["data"])

    output_file = output_dir / f"nav_{SCHEME_CODE}.csv"

    nav_df.to_csv(output_file, index=False)

    print(f"\nNAV history saved to:\n{output_file}")


def main():

    data = fetch_nav()

    if data is None:
        return

    print("=" * 60)
    print("Scheme Information")
    print("=" * 60)

    print(f"Scheme Name : {data['meta']['scheme_name']}")
    print(f"Fund House  : {data['meta']['fund_house']}")
    print(f"Scheme Type : {data['meta']['scheme_type']}")
    print(f"Scheme Category : {data['meta']['scheme_category']}")

    print("\nLatest NAV")
    print("-" * 60)

    latest = data["data"][0]

    print(f"Date : {latest['date']}")
    print(f"NAV  : {latest['nav']}")

    save_nav_history(data)


if __name__ == "__main__":
    main()