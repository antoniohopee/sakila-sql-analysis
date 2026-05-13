SELECT
    cu.customer_id,
    cu.first_name || ' ' || cu.last_name AS customer,
    cu.active,
    cu.store_id,
    COUNT(r.rental_id) AS rentals,
    ROUND(SUM(p.amount), 2) AS amount_spent
FROM customer AS cu
JOIN rental AS r
    ON r.customer_id = cu.customer_id
JOIN payment AS p
    ON p.rental_id = r.rental_id
GROUP BY
    cu.customer_id,
    cu.first_name,
    cu.last_name,
    cu.active,
    cu.store_id
ORDER BY amount_spent DESC
LIMIT 10;
