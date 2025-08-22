-- Unicamente las filas coincidentes

SELECT * FROM users
INNER JOIN dni;
JOIN dni
-- Se puede usar INNER o JOIN, son equivalentes.
-- Tenemos que especificar la condición de unión
ON users.user_id = dni.user_id;


SELECT * FROM users
JOIN companies
ON users.company_id = companies.company_id


SELECT * FROM users_languages
JOIN users ON users_languages.user_id = users.user_id
JOIN languages ON users_languages.language_id = languages.language_id


SELECT users.name, languages.name
FROM users_languages
JOIN users ON users_languages.user_id = users.user_id
JOIN languages ON users_languages.language_id = languages.language_id

