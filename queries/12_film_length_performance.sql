SELECT
    f.title AS film,
    f.length AS length_minutes,
    COUNT(r.rental_id) AS rentals,
    ROUND(SUM(p.amount), 2) AS revenue
FROM film AS f
JOIN inventory AS i
    ON i.film_id = f.film_id
JOIN rental AS r
    ON r.inventory_id = i.inventory_id
JOIN payment AS p
    ON p.rental_id = r.rental_id
GROUP BY f.film_id, f.title, f.length
ORDER BY rentals DESC, revenue DESC
LIMIT 10;
