# etl/load.py

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

from extract import extract
from transform import transform
from db_utils import get_db_uri


# -----------------------------
# LOAD FUNCTION
# -----------------------------
def load_tables(tables: dict):
    engine = create_engine(get_db_uri())

    try:
        print("🧹 Clearing old data...")

        with engine.begin() as conn:
            # Order matters because of FK constraints
            conn.execute(text("TRUNCATE TABLE fact_sales CASCADE"))
            conn.execute(text("TRUNCATE TABLE dim_customer CASCADE"))
            conn.execute(text("TRUNCATE TABLE dim_product CASCADE"))
            conn.execute(text("TRUNCATE TABLE dim_date CASCADE"))

        print("⬆️ Loading data...")

        # Insert in correct order
        tables["dim_customer"].to_sql(
            "dim_customer", engine, if_exists="append", index=False
        )

        tables["dim_product"].to_sql(
            "dim_product", engine, if_exists="append", index=False
        )

        tables["dim_date"].to_sql(
            "dim_date", engine, if_exists="append", index=False
        )

        tables["fact_sales"].to_sql(
            "fact_sales", engine, if_exists="append", index=False
        )

        print("🎉 Data loaded successfully!")

    except Exception as e:
        print("❌ Load failed:")
        print(str(e))


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def run_pipeline():
    print("🚀 Starting ETL...")

    df = extract()
    tables = transform(df)

    load_tables(tables)


if __name__ == "__main__":
    run_pipeline()