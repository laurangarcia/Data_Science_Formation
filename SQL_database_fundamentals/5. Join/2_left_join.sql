-- Devuelve todas las filas de la tabla de la izquierda (users) y las filas coincidentes de la tabla de la derecha (dni)
SELECT * FROM users
LEFT JOIN dni ON users.user_id = dni.user_id;
ON users.user_id = dni.user_id;


SELECT * FROM users
LEFT JOIN dni
ON users.user_id = dni.user_id
LEFT JOIN languages 
ON users_languages.language_id = languages.language_id