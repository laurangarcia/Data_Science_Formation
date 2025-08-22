
-- Seleccionar todos los usuarios con email nulo
SELECT * FROM users WHERE email IS NULL;

-- Seleccionar todos los usuarios con email no nulo
SELECT * FROM users WHERE email IS NOT NULL;

-- Seleccionar todos los usuarios con email no nulo y mayores de 18
SELECT * FROM users WHERE email IS NOT NULL AND age > 18;

-- Seleccionar nombre, apellido y edad (0 si es nula)
SELECT name, surname, IFNULL(age, 0) AS age FROM users;

-- Seleccionar si un valor es nulo
SELECT  ISNULL(NULL);