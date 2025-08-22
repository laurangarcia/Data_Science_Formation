-- Insertar un nuevo usuario, no podemos insertar un nuevo elemento sin su identificador
INSERT INTO users(user_id, name, surname, email) VALUES (7, "Victor", "Alarcon", "victor.alarcon@example.com");

-- Aunque lo ideal es seleccionar su identificador, como habiamos realizazo la lase de datos incremental, de igual forma se coloca su identificador en aitomatico
INSERT INTO users(name, surname, email) VALUES ("Victor", "Alarcon", "victor.alarcon@example.com");


SELECT * FROM hello_mysql.users_languages;

INSERT INTO users_languages (user_id, language_id) VALUES (1, 1);
INSERT INTO users_languages (user_id, language_id) VALUES (1, 2);
INSERT INTO users_languages (user_id, language_id) VALUES (1, 5);
INSERT INTO users_languages (user_id, language_id) VALUES (2, 4);
INSERT INTO users_languages (user_id, language_id) VALUES (2, 3);
INSERT INTO users_languages (user_id, language_id) VALUES (3, 1);
INSERT INTO users_languages (user_id, language_id) VALUES (3, 5);
INSERT INTO users_languages (user_id, language_id) VALUES (4, 4);
INSERT INTO users_languages (user_id, language_id) VALUES (4, 3);
INSERT INTO users_languages (user_id, language_id) VALUES (5, 2);
INSERT INTO users_languages (user_id, language_id) VALUES (5, 1);
