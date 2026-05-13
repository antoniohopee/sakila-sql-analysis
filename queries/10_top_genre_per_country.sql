WITH country_category_rentals AS (
    SELECT
        co.country,
        c.name AS category,
        COUNT(r.rental_id) AS rentals,
        ROUND(SUM(p.amount), 2) AS revenue,
        ROW_NUMBER() OVER (
            PARTITION BY co.country
            ORDER BY COUNT(r.rental_id) DESC, SUM(p.amount) DESC
        ) AS category_rank
    FROM country AS co
    JOIN city AS ci
        ON ci.country_id = co.country_id
    JOIN address AS a
        ON a.city_id = ci.city_id
    JOIN customer AS cu
        ON cu.address_id = a.address_id
    JOIN rental AS r
        ON r.customer_id = cu.customer_id
    JOIN inventory AS i
        ON i.inventory_id = r.inventory_id
    JOIN film_category AS fc
        ON fc.film_id = i.film_id
    JOIN category AS c
        ON c.category_id = fc.category_id
    JOIN payment AS p
        ON p.rental_id = r.rental_id
    GROUP BY co.country_id, co.country, c.category_id, c.name
)
SELECT
    country,
    category AS top_category,
    rentals,
    revenue
FROM country_category_rentals
WHERE category_rank = 1
ORDER BY country;
