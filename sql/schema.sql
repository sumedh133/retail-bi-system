-- Drop tables if they exist to ensure a clean slate during testing
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_date;

-- 1. Create Dimension Tables
CREATE TABLE dim_customer (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(255),
    segment VARCHAR(100),
    region VARCHAR(100)
);

CREATE TABLE dim_product (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    sub_category VARCHAR(100)
);

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY, 
    date DATE,
    month INT,
    year INT,
    quarter INT
);

-- 2. Create the Fact Table
CREATE TABLE fact_sales (
    sale_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) REFERENCES dim_customer(customer_id),
    product_id VARCHAR(50) REFERENCES dim_product(product_id),
    date_id INT REFERENCES dim_date(date_id),
    quantity INT,
    revenue DECIMAL(10, 2)
);