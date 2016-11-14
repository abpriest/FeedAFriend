/*password = mealswipes*/
CREATE EXTENSION pgcrypto;

DROP DATABASE IF EXISTS feedfriend;
CREATE DATABASE feedfriend;

\c feedfriend
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id serial NOT NULL,
    username text NOT NULL,
    password text NOT NULL,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS profile;
CREATE TABLE profile (
    id serial NOT NULL,
    name varchar(20) NOT NULL,
    email varchar(15) NOT NULL,
    giverec boolean NOT NULL,
    image bytea,
    PRIMARY KEY (id),
    
    userid serial NOT NULL,
    CONSTRAINT users_userid_fk
    FOREIGN KEY (userid)
    REFERENCES users (id)
);

INSERT INTO users(username, password) VALUES('testuser', crypt('testpassword', gen_salt('bf')));
INSERT INTO profile(name, email, giverec) VALUES('test', 'test@umw.edu', true);

SELECT * FROM users WHERE password = crypt('testpassword', password) AND username = 'testuser';
