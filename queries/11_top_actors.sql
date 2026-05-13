SELECT
    a.actor_id,
    a.first_name || ' ' || a.last_name AS actor,
    COUNT(DISTINCT fa.film_id) AS films,
    COUNT(r.rental_id) AS rentals,
    ROUND(SUM(p.amount), 2) AS revenue
FROM actor AS a
JOIN film_actor AS fa
    ON fa.actor_id = a.actor_id
JOIN film AS f
    ON f.film_id = fa.film_id
JOIN inventory AS i
    ON i.film_id = f.film_id
JOIN rental AS r
    ON r.inventory_id = i.inventory_id
JOIN payment AS p
    ON p.rental_id = r.rental_id
GROUP BY a.actor_id, a.first_name, a.last_name
ORDER BY rentals DESC, revenue DESC
LIMIT 10;
