SELECT
    c.name AS category,
    COUNT(r.rental_id) AS rentals,
    ROUND(SUM(p.amount), 2) AS revenue
FROM category AS c
JOIN film_category AS fc
    ON fc.category_id = c.category_id
JOIN film AS f
    ON f.film_id = fc.film_id
JOIN inventory AS i
    ON i.film_id = f.film_id
JOIN rental AS r
    ON r.inventory_id = i.inventory_id
JOIN payment AS p
    ON p.rental_id = r.rental_id
GROUP BY c.category_id, c.name
ORDER BY revenue DESC;
