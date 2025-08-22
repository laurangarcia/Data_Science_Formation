SELECT name, init_date FROM users WHERE age BETWEEN 20 AND 30

SELECT name, init_date AS 'Fecha de inicio de programación' FROM users WHERE age BETWEEN 20 AND 30

SELECT CONCAT(name," ", surname) FROM users


SELECT CONCAT("Nombre: ",name, "Apellidos: ", surname) FROM users