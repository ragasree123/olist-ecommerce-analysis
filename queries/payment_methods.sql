SELECT
    payment_type,
    COUNT(*) AS transaction_count,
    ROUND(AVG(payment_value), 2) AS avg_payment,
    ROUND(SUM(payment_value), 2) AS total_revenue
FROM order_payments
GROUP BY payment_type
ORDER BY transaction_count DESC