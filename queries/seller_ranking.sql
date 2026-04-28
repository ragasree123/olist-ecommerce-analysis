WITH seller_revenue AS (
    SELECT
        s.seller_id,
        s.seller_state,
        s.seller_city,
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(SUM(oi.price), 2) AS total_revenue
    FROM sellers s
    JOIN order_items oi ON s.seller_id = oi.seller_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY s.seller_id
    HAVING total_orders >= 10
)
SELECT
    seller_id,
    seller_state,
    seller_city,
    total_orders,
    total_revenue,
    ROW_NUMBER() OVER (
        PARTITION BY seller_state
        ORDER BY total_revenue DESC
    ) AS rank_in_state,
    RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS overall_rank
FROM seller_revenue
ORDER BY seller_state, rank_in_state
LIMIT 20
