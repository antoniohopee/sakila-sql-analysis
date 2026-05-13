SELECT
    f.film_id,
    f.title AS film,
    ROUND(SUM(p.amount), 2) AS revenue,
    COUNT(r.rental_id) AS rentals,
    COUNT(DISTINCT i.inventory_id) AS inventory_copies
FROM film AS f
JOIN inventory AS i
    ON i.film_id = f.film_id
JOIN rental AS r
    ON r.inventory_id = i.inventory_id
JOIN payment AS p
    ON p.rental_id = r.rental_id
GROUP BY f.film_id, f.title
ORDER BY revenue DESC
LIMIT 10;
