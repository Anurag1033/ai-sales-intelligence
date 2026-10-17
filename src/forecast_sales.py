
from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from statsmodels.tsa.holtwinters import ExponentialSmoothing

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT / "data" / "processed" / "sales_forecast.csv"


def main():
    load_dotenv(ROOT / ".env")

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is missing. Check your .env file.")

    engine = create_engine(db_url)

    query = """
        SELECT
            DATE(invoice_date) AS sale_date,
            SUM(sales_amount) AS daily_sales
        FROM sales
        GROUP BY DATE(invoice_date)
        ORDER BY sale_date
    """

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)

    if len(df) < 60:
        raise ValueError("Not enough daily sales history to build a forecast.")

    df["sale_date"] = pd.to_datetime(df["sale_date"])
    daily = (
        df.set_index("sale_date")["daily_sales"]
        .astype(float)
        .asfreq("D", fill_value=0)
    )

    model = ExponentialSmoothing(
        daily,
        trend="add",
        seasonal="add",
        seasonal_periods=7,
        initialization_method="estimated",
    ).fit(optimized=True)

    forecast = model.forecast(30).clip(lower=0)

    result = pd.DataFrame({
        "forecast_date": forecast.index,
        "predicted_sales_gbp": forecast.values,
    })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print("30-day sales forecast created successfully.")
    print(f"Saved to: {OUTPUT_FILE}")
    print(result.head(10).to_string(index=False))
    print(f"\nTotal predicted sales for 30 days: £{result['predicted_sales_gbp'].sum():,.2f}")


if __name__ == "__main__":
    main()
