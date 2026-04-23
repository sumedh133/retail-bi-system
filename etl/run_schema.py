# etl/run_schema.py

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from db_utils import get_db_uri


def run_schema():
    try:
        print("📄 Loading schema.sql...")

        with open("sql/schema.sql", "r") as f:
            schema_sql = f.read()

        engine = create_engine(get_db_uri())

        print("🚀 Applying schema...")

        with engine.connect() as conn:
            conn.execute(text(schema_sql))
            conn.commit()

        print("✅ Schema applied successfully!")

    except Exception as e:
        print("❌ Failed to apply schema:")
        print(str(e))


if __name__ == "__main__":
    run_schema()