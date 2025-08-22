SELECT name, dni_number FROM dni
RIGHT JOIN users
ON users.user_id = dni.user_id


