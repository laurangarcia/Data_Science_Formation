-- Relacion 1:1
CREATE TABLE dni(
	dni_id int auto_increment PRIMARY KEY,
    dni_number int NOT NULL,
    user_id int,  
    UNIQUE(dni_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);


-- Relacion 1:N
CREATE TABLE orders(
	order_id int auto_increment PRIMARY KEY,
    order_date date NOT NULL,
    user_id int,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

ALTER TABLE users
ADD CONSTRAINT fk_companies
FOREIGN KEY(company_id) REFERENCES companies(company_id)

-- Relacion N:M

CREATE TABLE languages(
	language_id int AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Tenemos que crear esa tabla intermedia

CREATE TABLE users_languages(
	user_language_id int AUTO_INCREMENT PRIMARY KEY,
	user_id int,
	language_id int,
	FOREIGN KEY(user_id) REFERENCES users(user_id),
	FOREIGN KEY(language_id) REFERENCES languages(language_id)
    UNIQUE (user_id, language_id)
);
