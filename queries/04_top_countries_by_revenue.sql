SELECT
    co.country,
    COUNT(r.rental_id) AS rentals,
    ROUND(SUM(p.amount), 2) AS revenue,
    COUNT(DISTINCT cu.customer_id) AS unique_customers
FROM country AS co
JOIN city AS ci
    ON ci.country_id = co.country_id
JOIN address AS a
    ON a.city_id = ci.city_id
JOIN customer AS cu
    ON cu.address_id = a.address_id
JOIN rental AS r
    ON r.customer_id = cu.customer_id
JOIN payment AS p
    ON p.rental_id = r.rental_id
GROUP BY co.country_id, co.country
ORDER BY revenue DESC
LIMIT 10;
