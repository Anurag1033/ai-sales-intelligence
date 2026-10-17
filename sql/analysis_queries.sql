
-- 1. Overall sales KPIs
SELECT
    ROUND(SUM(sales_amount), 2) AS total_sales_gbp,
    COUNT(DISTINCT invoice_no) AS total_invoices,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT stock_code) AS unique_products
FROM sales;

-- 2. Monthly sales trend
SELECT
    DATE_TRUNC('month', invoice_date)::date AS month,
    ROUND(SUM(sales_amount), 2) AS monthly_sales_gbp,
    COUNT(DISTINCT invoice_no) AS total_invoices
FROM sales
GROUP BY 1
ORDER BY 1;

-- 3. Top 10 products by sales value
SELECT
    stock_code,
    MAX(description) AS product_name,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales_amount), 2) AS total_sales_gbp
FROM sales
GROUP BY stock_code
ORDER BY SUM(sales_amount) DESC
LIMIT 10;

-- 4. Top 10 countries by sales
SELECT
    country,
    COUNT(DISTINCT invoice_no) AS total_invoices,
    ROUND(SUM(sales_amount), 2) AS total_sales_gbp,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM sales
GROUP BY country
ORDER BY SUM(sales_amount) DESC
LIMIT 10;

-- 5. Average order value
SELECT
    ROUND(
        SUM(sales_amount) / COUNT(DISTINCT invoice_no),
        2
    ) AS average_order_value_gbp
FROM sales;

-- 6. Best-performing month
SELECT
    DATE_TRUNC('month', invoice_date)::date AS month,
    ROUND(SUM(sales_amount), 2) AS monthly_sales_gbp
FROM sales
GROUP BY 1
ORDER BY SUM(sales_amount) DESC
LIMIT 1;
