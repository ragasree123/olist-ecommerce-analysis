SELECT
    oi.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(oi.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS total_revenue
FROM order_items oi
JOIN sellers s ON oi.seller_id = s.seller_id
GROUP BY oi.seller_id
ORDER BY total_orders DESC
LIMIT 10