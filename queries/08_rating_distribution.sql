SELECT
    rating,
    COUNT(film_id) AS films,
    ROUND(100.0 * COUNT(film_id) / (SELECT COUNT(*) FROM film), 1) AS pct_films
FROM film
GROUP BY rating
ORDER BY films DESC;
