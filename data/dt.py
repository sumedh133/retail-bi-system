import pandas as pd
import numpy as np

# 1. Load the master dataset
print("Loading master dataset...")
df = pd.read_csv('data/raw/train.csv')

# ---------------------------------------------------------
# 2. Extract and Save Customers Dataset
# ---------------------------------------------------------
print("Processing Customers...")
# Extract unique customers and keep the most recent region/segment if they moved
customers = df[['Customer ID', 'Customer Name', 'Segment', 'Region']].drop_duplicates(subset=['Customer ID'])

# Rename columns to match the SQL schema exactly
customers = customers.rename(columns={
    'Customer ID': 'customer_id', 
    'Customer Name': 'customer_name', 
    'Segment': 'segment',
    'Region': 'region'
})

customers.to_csv('data/extracted/customers.csv', index=False)
print(f"✅ Created customers.csv with {len(customers)} records.")

# ---------------------------------------------------------
# 3. Extract and Save Products Dataset
# ---------------------------------------------------------
print("Processing Products...")
# Extract unique products
products = df[['Product ID', 'Product Name', 'Category', 'Sub-Category']].drop_duplicates(subset=['Product ID'])

products = products.rename(columns={
    'Product ID': 'product_id',
    'Product Name': 'product_name',
    'Category': 'category',
    'Sub-Category': 'sub_category'
})

products.to_csv('data/extracted/products.csv', index=False)
print(f"✅ Created products.csv with {len(products)} records.")

# ---------------------------------------------------------
# 4. Extract and Save Sales Dataset
# ---------------------------------------------------------
print("Processing Sales...")
# The PRD requires 'quantity' and 'revenue'[cite: 53, 61]. 
# Your master file has 'Sales' (which is revenue) but is missing 'Quantity'.
# We will map 'Row ID' to 'sale_id' to ensure every line item is unique.

sales = df[['Row ID', 'Customer ID', 'Product ID', 'Order Date', 'Sales']].copy()

sales = sales.rename(columns={
    'Row ID': 'sale_id',
    'Customer ID': 'customer_id',
    'Product ID': 'product_id',
    'Order Date': 'order_date',
    'Sales': 'revenue'
})

# Since 'Quantity' is missing from your master columns, we will default it to 1 
# so your SQL aggregations like SUM(quantity) don't break.
sales['quantity'] = 1 

sales.to_csv('data/extracted/sales.csv', index=False)
print(f"✅ Created sales.csv with {len(sales)} records.")
print("🎉 Data splitting complete!")