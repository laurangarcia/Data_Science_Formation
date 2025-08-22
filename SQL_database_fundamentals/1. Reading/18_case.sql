SELECT *, 
CASE
	WHEN age > 18 THEN 'Es mayor de edad'
    WHEN age = 18 THEN 'Acabo de cumplir 18 años'
    ELSE 'Es menor de edad'
END AS '¿Es menor de edad?'
FROM users;


SELECT *, 
CASE
	WHEN age < 17 THEN True
    ELSE False
END AS '¿Es mayor de edad?'
FROM users;