# etl/extract.py

import pandas as pd
from pathlib import Path


DATA_PATH = Path("data/raw/train.csv")


def extract():
    """
    Extract raw data from CSV.
    Returns:
        pd.DataFrame
    """
    print("📥 Extracting data...")

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"File not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    print(f"✅ Loaded dataset with {len(df)} rows and {len(df.columns)} columns.")
    return df


if __name__ == "__main__":
    df = extract()
    print(df.head())