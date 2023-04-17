-- Which alcoholic drinks can be mixed with lemon and whiskey?
WITH alcoholic_cte AS (
    SELECT *
    FROM alcoholic
    WHERE alcohol = "alcoholic"
)
SELECT i.ingredient_name, 
       GROUP_CONCAT(dr.drink_name) AS list_of_drinks, 
       COUNT(dr.drink_name) AS count_of_drinks
FROM alcoholic_cte a
LEFT JOIN drinks dr ON a.id = dr.alcoholic_id
LEFT JOIN drink_recipe d_r ON dr.id = d_r.drink_id
LEFT JOIN ingredients i ON d_r.ingredient_id = i.id
WHERE i.ingredient_name IN ("lemon", "whiskey")
GROUP BY i.ingredient_name;

-- Which drink(s) can be mixed with just 15g of Sambuca?
/* 
The following show no results when the filter is for "sambuca" with "15g", 
the query has been modified to get back all drinks with sambuca, 
please include the commented out portion at the end of this query with the relevant filter for more strict results 
*/

SELECT dr.id, 
       dr.drink_name, 
       i.ingredient_name, 
       m.measure_quantity
FROM ingredients i
LEFT JOIN drink_recipe d_r ON i.id = d_r.ingredient_id 
LEFT JOIN measures m ON d_r.measure_id = m.id
LEFT JOIN drinks dr ON d_r.drink_id = dr.id
WHERE LOWER(i.ingredient_name) = "sambuca";
-- AND m.measure_quantity LIKE "%1 oz%"; 


-- Which drink has the most ingredients?
SELECT dr.drink_name, 
       d_r.drink_id, 
       COUNT(d_r.ingredient_id) AS ingredient_count 
FROM drink_recipe d_r
JOIN drinks dr ON d_r.drink_id = dr.id  
GROUP BY drink_id
ORDER BY ingredient_count DESC
LIMIT 1;
