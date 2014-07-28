#####
# again, make sure to start by specifing the database
#####
USE zzzRST;

## simplest possible query
SELECT * FROM users_personal;

## joining tables is the magic of rdbms 
#SELECT * FROM users_work AS w JOIN users_personal AS p WHERE w.user_id = p.user_id;

## select specific fields and use aliases ('AS' is implied)
#SELECT first_name first, last_name last FROM users_work w JOIN users_personal p WHERE w.user_id = p.user_id;

## multiple join clauses  
#SELECT first_name first, last_name last FROM users_work w JOIN users_personal p WHERE w.user_id = p.user_id AND w.department="data science" OR p.fav_dino LIKE "%ciro%";

## grouping 
#SELECT department, COUNT(*) total FROM users_personal p INNER JOIN users_work w WHERE p.user_id=w.user_id GROUP BY department; 

