
from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / "data" / "processed" / "sales_clean.csv"


def main():
    load_dotenv(ROOT / ".env")

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError(
            "DATABASE_URL is missing. Check your .env file."
        )

    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"Cleaned CSV not found: {CSV_FILE}"
        )

    print("Reading cleaned sales data...")
    df = pd.read_csv(
        CSV_FILE,
        dtype={
            "InvoiceNo": str,
            "StockCode": str,
            "CustomerID": str,
        },
    )

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    )

    df = df.rename(columns={
        "InvoiceNo": "invoice_no",
        "StockCode": "stock_code",
        "Description": "description",
        "Quantity": "quantity",
        "InvoiceDate": "invoice_date",
        "UnitPrice": "unit_price",
        "CustomerID": "customer_id",
        "Country": "country",
        "SalesAmount": "sales_amount",
    })

    engine = create_engine(db_url)

    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS sales (
                invoice_no TEXT,
                stock_code TEXT,
                description TEXT,
                quantity INTEGER,
                invoice_date TIMESTAMP,
                unit_price NUMERIC(12, 2),
                customer_id TEXT,
                country TEXT,
                sales_amount NUMERIC(14, 2)
            )
        """))

        conn.execute(text("TRUNCATE TABLE sales"))

    df.to_sql(
        "sales",
        engine,
        if_exists="append",
        index=False,
        chunksize=1000,
        method="multi",
    )

    print(f"Successfully loaded {len(df):,} rows into PostgreSQL.")


if __name__ == "__main__":
    main()
