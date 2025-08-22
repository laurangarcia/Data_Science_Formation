CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100),
    surname VARCHAR(100),
    email VARCHAR(100),
    age INT,
    init_date DATE
);

/* 
En la creacion de los databse, tambien le podemos poner restricciones
Restricciones: 
- NN: NOT NULL
- UQ: UNIQUE
*/
CREATE TABLE persons2(
	id int NOT NULL AUTO_INCREMENT,
    name varchar(100),
    age int,
    email varchar(50) ,
    created datetime DEFAULT CURRENT_TIMESTAMP(),
    UNIQUE(id),
    PRIMARY KEY(id),
    CHECK (age >= 18)
);

