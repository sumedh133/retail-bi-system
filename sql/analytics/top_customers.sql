SELECT 
    c.customer_name,
    c.segment,
    c.region,
    SUM(f.revenue) AS total_spent,
    COUNT(DISTINCT f.sale_id) AS total_orders
FROM 
    fact_sales f
JOIN 
    dim_customer c ON f.customer_id = c.customer_id
GROUP BY 
    c.customer_name, c.segment, c.region
ORDER BY 
    total_spent DESC
LIMIT 10;