SELECT
    t.product_category_name_english AS category,
    COUNT(oi.order_id) AS order_count,
    ROUND(SUM(oi.price), 2) AS total_revenue,
    ROUND(AVG(oi.price), 2) AS avg_price
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN translations t ON p.product_category_name = t.product_category_name
GROUP BY category
ORDER BY order_count DESC
LIMIT 10