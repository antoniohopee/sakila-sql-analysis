SELECT
    strftime('%Y-%m', payment_date) AS month,
    ROUND(SUM(amount), 2) AS revenue,
    COUNT(payment_id) AS payments,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(AVG(amount), 2) AS avg_payment
FROM payment
GROUP BY strftime('%Y-%m', payment_date)
ORDER BY month;
