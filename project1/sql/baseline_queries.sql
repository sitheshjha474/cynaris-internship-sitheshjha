-- Total revenue
SELECT
    SUM(net_revenue) AS total_revenue
FROM sales_cleaned;


-- Total units sold
SELECT
    SUM(units) AS total_units
FROM sales_cleaned;


-- Number of transactions
SELECT
    COUNT(DISTINCT transaction_id) AS transactions
FROM sales_cleaned;


-- Revenue by city
SELECT
    city,
    SUM(net_revenue) AS revenue
FROM sales_cleaned
GROUP BY city
ORDER BY revenue DESC;


-- Revenue by channel
SELECT
    channel,
    SUM(net_revenue) AS revenue
FROM sales_cleaned
GROUP BY channel
ORDER BY revenue DESC;


-- Revenue by category
SELECT
    category,
    SUM(net_revenue) AS revenue
FROM sales_cleaned
GROUP BY category
ORDER BY revenue DESC;


-- Return rate
SELECT
    AVG(return_flag) * 100 AS return_rate
FROM sales_cleaned;


-- Customer churn
SELECT
    AVG(churned) * 100 AS churn_rate
FROM customers_cleaned;


-- Product inventory
SELECT
    product_id,
    name,
    stock_units,
    avg_monthly_sales,
    stock_units / NULLIF(avg_monthly_sales, 0)
        AS estimated_months_of_stock
FROM products_cleaned
ORDER BY estimated_months_of_stock;