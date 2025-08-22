SELECT CONCAT("Nombre: ",name, "Apellidos: ", surname) FROM users

SELECT MAX(age), age FROM users GROUP BY age

SELECT COUNT(age), age FROM users GROUP BY age ORDER BY age ASC

SELECT COUNT(age), age FROM users GROUP BY age ORDER BY age ASC

SELECT COUNT(age), age FROM users WHERE age > 15 GROUP BY age ORDER BY age ASC