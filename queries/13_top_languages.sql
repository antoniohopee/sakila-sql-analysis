SELECT
    TRIM(l.name) AS language,
    COUNT(DISTINCT f.film_id) AS films,
    COUNT(r.rental_id) AS rentals,
    ROUND(COALESCE(SUM(p.amount), 0), 2) AS revenue
FROM language AS l
LEFT JOIN film AS f
    ON f.language_id = l.language_id
LEFT JOIN inventory AS i
    ON i.film_id = f.film_id
LEFT JOIN rental AS r
    ON r.inventory_id = i.inventory_id
LEFT JOIN payment AS p
    ON p.rental_id = r.rental_id
GROUP BY l.language_id, l.name
ORDER BY revenue DESC;
