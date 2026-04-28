run_sql("""
WITH monthly_rev AS (
    SELECT
        STRFTIME('%Y-%m', order_purchase_timestamp) AS month,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(SUM(price), 2) AS total_revenue
    FROM orders
    JOIN order_items USING (order_id)
    WHERE order_status = 'delivered'
    GROUP BY month
    ORDER BY month
)
SELECT
    month,
    total_orders,
    total_revenue,
    LAG(total_revenue) OVER (
        ORDER BY month
    ) AS prev_month_revenue,
    ROUND(
        (total_revenue - LAG(total_revenue) OVER (
            ORDER BY month)
        ) * 100.0 /
        LAG(total_revenue) OVER (ORDER BY month),
        1
    ) AS mom_growth_pct,
    ROUND(SUM(total_revenue) OVER (
        ORDER BY month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS running_total
FROM monthly_rev
""")