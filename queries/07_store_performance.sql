SELECT
    s.store_id,
    a.address || ', ' || ci.city || ', ' || co.country AS store_location,
    st.first_name || ' ' || st.last_name AS manager,
    COUNT(p.payment_id) AS payments,
    ROUND(SUM(p.amount), 2) AS revenue
FROM store AS s
JOIN address AS a
    ON a.address_id = s.address_id
JOIN city AS ci
    ON ci.city_id = a.city_id
JOIN country AS co
    ON co.country_id = ci.country_id
JOIN staff AS st
    ON st.staff_id = s.manager_staff_id
JOIN payment AS p
    ON p.staff_id = st.staff_id
GROUP BY s.store_id, store_location, manager
ORDER BY revenue DESC;
