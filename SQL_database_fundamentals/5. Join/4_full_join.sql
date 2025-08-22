SELECT *
FROM users
FULL JOIN dni ON users.user_id = dni.user_id
FULL OUTER JOIN languages ON users_languages.language_id = languages.language_id
