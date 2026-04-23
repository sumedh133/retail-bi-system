# etl/transform.py

import pandas as pd


# -----------------------------
# 1. Customers
# -----------------------------
def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    print("👥 Transforming customers...")

    customers = df[['Customer ID', 'Customer Name', 'Segment', 'Region']].drop_duplicates(
        subset=['Customer ID']
    )

    customers = customers.rename(columns={
        'Customer ID': 'customer_id',
        'Customer Name': 'customer_name',
        'Segment': 'segment',
        'Region': 'region'
    })

    print(f"✅ Customers: {len(customers)} records")
    return customers


# -----------------------------
# 2. Products
# -----------------------------
def transform_products(df: pd.DataFrame) -> pd.DataFrame:
    print("📦 Transforming products...")

    products = df[['Product ID', 'Product Name', 'Category', 'Sub-Category']].drop_duplicates(
        subset=['Product ID']
    )

    products = products.rename(columns={
        'Product ID': 'product_id',
        'Product Name': 'product_name',
        'Category': 'category',
        'Sub-Category': 'sub_category'
    })

    print(f"✅ Products: {len(products)} records")
    return products


# -----------------------------
# 3. Date Dimension
# -----------------------------
def transform_date(df: pd.DataFrame) -> pd.DataFrame:
    print("📅 Transforming date dimension...")

    temp = df[['Order Date']].copy()
    temp['Order Date'] = pd.to_datetime(temp['Order Date'], dayfirst=True)

    dim_date = temp.drop_duplicates()

    dim_date['date_id'] = dim_date['Order Date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['date'] = dim_date['Order Date']
    dim_date['month'] = dim_date['Order Date'].dt.month
    dim_date['year'] = dim_date['Order Date'].dt.year
    dim_date['quarter'] = dim_date['Order Date'].dt.quarter

    dim_date = dim_date[['date_id', 'date', 'month', 'year', 'quarter']]

    print(f"✅ Dates: {len(dim_date)} records")
    return dim_date


# -----------------------------
# 4. Sales (Fact Table)
# -----------------------------
def transform_sales(df: pd.DataFrame) -> pd.DataFrame:
    print("💰 Transforming sales...")

    sales = df[['Row ID', 'Customer ID', 'Product ID', 'Order Date', 'Sales']].copy()

    sales['Order Date'] = pd.to_datetime(sales['Order Date'], dayfirst=True)

    sales = sales.rename(columns={
        'Row ID': 'sale_id',
        'Customer ID': 'customer_id',
        'Product ID': 'product_id',
        'Order Date': 'order_date',
        'Sales': 'revenue'
    })

    # Create date_id (FK)
    sales['date_id'] = sales['order_date'].dt.strftime('%Y%m%d').astype(int)

    # Temporary quantity (since dataset doesn't have it)
    sales['quantity'] = 1

    sales = sales[['sale_id', 'customer_id', 'product_id', 'date_id', 'quantity', 'revenue']]

    print(f"✅ Sales: {len(sales)} records")
    return sales


# -----------------------------
# 5. Master Transform Function
# -----------------------------
def transform(df: pd.DataFrame) -> dict:
    """
    Runs full transformation pipeline.
    Returns:
        dict of DataFrames
    """
    return {
        "dim_customer": transform_customers(df),
        "dim_product": transform_products(df),
        "dim_date": transform_date(df),
        "fact_sales": transform_sales(df)
    }


# -----------------------------
# Run standalone
# -----------------------------
if __name__ == "__main__":
    from extract import extract

    df = extract()
    tables = transform(df)

    for name, table in tables.items():
        print(f"\n{name} preview:")
        print(table.head())