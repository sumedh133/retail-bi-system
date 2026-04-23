SELECT 
    d.year,
    d.month,
    SUM(f.revenue) AS total_revenue,
    SUM(f.quantity) AS total_items_sold
FROM 
    fact_sales f
JOIN 
    dim_date d ON f.date_id = d.date_id
GROUP BY 
    d.year, d.month
ORDER BY 
    d.year ASC, d.month ASC;