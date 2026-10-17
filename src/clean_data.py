from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "raw" / "Online Retail.xlsx"
OUTPUT_FILE = ROOT / "data" / "processed" / "sales_clean.csv"

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {INPUT_FILE}")

    df = pd.read_excel(INPUT_FILE)
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]

    print("Rows before cleaning:", len(df))

    df = df.drop_duplicates()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

    df = df.dropna(
        subset=["InvoiceNo", "StockCode", "InvoiceDate", "Quantity", "UnitPrice"]
    )

    df["InvoiceNo"] = df["InvoiceNo"].astype(str).str.strip()
    df = df[~df["InvoiceNo"].str.upper().str.startswith("C")]
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] >= 0)]

    df["SalesAmount"] = df["Quantity"] * df["UnitPrice"]
    df["CustomerID"] = df["CustomerID"].astype("Int64").astype("string")
    df["CustomerID"] = df["CustomerID"].fillna("Unknown")

    df["InvoiceDate"] = df["InvoiceDate"].dt.strftime("%Y-%m-%d %H:%M:%S")

    columns = [
        "InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "UnitPrice", "CustomerID", "Country", "SalesAmount"
    ]

    df = df[columns]
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print("Rows after cleaning:", len(df))
    print("Saved cleaned file to:", OUTPUT_FILE)
    print("Total sales (GBP):", round(df["SalesAmount"].sum(), 2))


if __name__ == "__main__":
    main()