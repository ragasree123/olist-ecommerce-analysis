run_sql("""
-- CTE 1 — calculate total spend per customer
WITH customer_spend AS (
    SELECT
        c.customer_unique_id,
        c.customer_state,
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(SUM(oi.price), 2) AS total_spend,
        ROUND(AVG(oi.price), 2) AS avg_order_value,
        MIN(o.order_purchase_timestamp) AS first_order,
        MAX(o.order_purchase_timestamp) AS last_order
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),

-- CTE 2 — segment customers by spend level
customer_segments AS (
    SELECT
        customer_unique_id,
        customer_state,
        total_orders,
        total_spend,
        avg_order_value,
        CASE
            WHEN total_spend >= 500 THEN 'High Value'
            WHEN total_spend >= 200 THEN 'Mid Value'
            WHEN total_spend >= 100 THEN 'Standard'
            ELSE 'Low Value'
        END AS spend_segment
    FROM customer_spend
)

-- Final query — summarise each segment
SELECT
    spend_segment,
    COUNT(*) AS customer_count,
    ROUND(AVG(total_spend), 2) AS avg_spend,
    ROUND(AVG(total_orders), 2) AS avg_orders,
    ROUND(SUM(total_spend), 2) AS total_segment_revenue,
    ROUND(
        SUM(total_spend) * 100.0 /
        SUM(SUM(total_spend)) OVER (),
        1
    ) AS revenue_pct
FROM customer_segments
GROUP BY spend_segment
ORDER BY avg_spend DESC
""")