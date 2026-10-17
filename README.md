# AI-Powered Sales Analytics & Forecasting

A data analytics project that uses Python, PostgreSQL, and Power BI to clean retail sales data, analyze business performance, and forecast future sales.

## Project Overview

This project transforms historical retail transaction data into useful business insights through data cleaning, SQL analysis, sales forecasting, and an interactive Power BI dashboard.

## Technologies Used

- **Python** — data cleaning and forecasting
- **Pandas** — data manipulation
- **PostgreSQL** — data storage and SQL analysis
- **Power BI** — interactive dashboard and visualization
- **Statsmodels** — time-series forecasting
- **Git and GitHub** — version control

## Key Features

- Cleaned and processed retail transaction data.
- Loaded sales records into PostgreSQL.
- Analyzed revenue, invoices, customers, products, and countries.
- Created a 30-day sales forecast using Exponential Smoothing.
- Built a Power BI dashboard with KPI cards, sales trends, product rankings, country comparisons, and forecast visualization.

## Key Results

| Metric | Result |
|---|---:|
| Original records | 541,909 |
| Processed records | 526,052 |
| Total sales | £10,642,110.80 |
| Distinct invoices | 20,726 |
| Unique customers | 4,340 |
| Distinct products | 3,941 |
| Average order value | £513.47 |

*Results are based on the historical dataset used in this project.*

## Project Structure

```text
ai-sales-intelligence/
├── data/
│   └── processed/
│       └── sales_forecast.csv
├── sql/
│   └── analysis_queries.sql
├── src/
│   ├── clean_data.py
│   ├── forecast_sales.py
│   └── load_postgres.py
├── .gitignore
├── abc.pbix
└── requirements.txt
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Anurag1033/ai-sales-intelligence.git
cd ai-sales-intelligence
```

### 2. Create a Python environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

