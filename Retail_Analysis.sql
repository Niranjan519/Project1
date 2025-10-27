
CREATE TABLE IF NOT EXISTS retail_transactions (
    "Row ID" INT,
    "Order ID" VARCHAR(50) PRIMARY KEY,
    "Order Date" DATE NOT NULL,
    "Ship Date" DATE NOT NULL,
    "Ship Mode" VARCHAR(50),
    "Customer ID" VARCHAR(50),
    "Customer Name" VARCHAR(100),
    "Segment" VARCHAR(50),
    -- ... geographical and sales people columns ...
    "Product ID" VARCHAR(50),
    "Category" VARCHAR(100),
    "Sub-Category" VARCHAR(100),
    "Product Name" VARCHAR(255),
    "Returned" VARCHAR(10), -- 'Yes' or 'No'
    "Sales" DECIMAL(10, 2) NOT NULL,
    "Quantity" INT NOT NULL,
    "Discount" DECIMAL(10, 4),
    "Profit" DECIMAL(10, 4) NOT NULL
);



-- Remove records where essential financial data is zero or missing
DELETE FROM retail_transactions
WHERE "Sales" IS NULL OR "Profit" IS NULL
   OR "Sales" <= 0 OR "Quantity" <= 0;

-- Optional: Calculate Cost of Goods Sold (COGS) for direct use
-- COGS = Sales - Profit

-- CALCULATE PROFIT MARGINS AND INVENTORY PROXY METRICS
-- Aggregates total metrics for BI dashboard consumption (Phase 2 output)

SELECT
    T."Region",
    T."Category",
    T."Sub-Category",
    -- Financial Metrics
    SUM(T."Sales") AS total_sales,
    SUM(T."Profit") AS total_profit,
    -- Profit Margin Calculation
    (SUM(T."Profit") / SUM(T."Sales")) * 100 AS profit_margin_percent,
    -- Inventory Efficiency Proxy: Average Shipping Lead Time (in days)
    -- This is a strong proxy for inventory/fulfillment delay problems
    AVG(JULIANDAY(T."Ship Date") - JULIANDAY(T."Order Date")) AS avg_shipping_lead_time_days,
    -- Seasonality Metric (Using Quarter)
    CASE
        WHEN CAST(STRFTIME('%m', T."Order Date") AS INT) BETWEEN 1 AND 3 THEN 'Q1 - Winter'
        WHEN CAST(STRFTIME('%m', T."Order Date") AS INT) BETWEEN 4 AND 6 THEN 'Q2 - Spring'
        WHEN CAST(STRFTIME('%m', T."Order Date") AS INT) BETWEEN 7 AND 9 THEN 'Q3 - Summer'
        ELSE 'Q4 - Autumn'
    END AS sales_season
FROM
    retail_transactions AS T
GROUP BY
    T."Region",
    T."Category",
    T."Sub-Category",
    sales_season
ORDER BY
    total_sales DESC;
