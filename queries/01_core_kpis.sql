SELECT
    ROUND(SUM(amount), 2) AS total_revenue,
    COUNT(payment_id) AS total_payments,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(AVG(amount), 2) AS avg_payment
FROM payment;
