-- si haces esto, TODAS las filas de la tabla users tendrán 21 como edad OJOOOOO
UPDATE users SET age = "21"

-- Siempre usar WHERE ATENCIÓNNNNNNNNNN
UPDATE users SET age = "21" WHERE user_id = 7

-- Se puede realizar más de una actualización
UPDATE users SET age = 20, init_date = "2020-02-20" WHERE user_id = 7

