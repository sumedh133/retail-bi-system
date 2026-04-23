import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


def get_db_uri():
    load_dotenv()

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")

    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


def test_connection():
    try:
        db_uri = get_db_uri()
        print(f"🔌 Connecting to: {db_uri}")

        engine = create_engine(db_uri)

        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Connection successful!")
            print("Result:", result.scalar())

    except Exception as e:
        print("❌ Connection failed:")
        print(str(e))


if __name__ == "__main__":
    test_connection()