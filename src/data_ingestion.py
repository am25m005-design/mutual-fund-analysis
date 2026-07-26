import os
import pandas as pd

DATA_FOLDER = "data/raw"

# Check if the folder exists
if not os.path.exists(DATA_FOLDER):
    print(f"Error: Folder '{DATA_FOLDER}' not found.")
    exit()

csv_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]

print(f"Found {len(csv_files)} CSV files\n")

for file in csv_files:
    path = os.path.join(DATA_FOLDER, file)

    try:
        df = pd.read_csv(path)

        print("=" * 60)
        print(f"File: {file}")
        print("=" * 60)
        print("Shape:", df.shape)

        print("\nData Types:")
        print(df.dtypes)

        print("\nFirst 5 Rows:")
        print(df.head())

        print()

    except Exception as e:
        print(f"Error reading {file}: {e}")

print("Finished loading all datasets.")