DROP DATABASE IF EXISTS feedfriend;
CREATE DATABASE feedfriend;

DROP ROLE IF EXISTS student;
CREATE ROLE student WITH password 'mealswipes123' LOGIN;

\c feedfriend

CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS profile;
CREATE TABLE profile (
    id serial NOT NULL,
    name varchar(20) NOT NULL,
    email varchar(15) NOT NULL,
    usertype varchar(1) NOT NULL,
    image bytea,
    PRIMARY KEY (id)
);

GRANT ALL ON profile TO student;
GRANT ALL ON profile_id_seq TO student;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id serial NOT NULL,
    username text NOT NULL,
    password text NOT NULL,
    PRIMARY KEY (id),
    
    userid serial,
    CONSTRAINT profile_id_fk
    FOREIGN KEY (userid)
    REFERENCES profile (id)

);

GRANT ALL ON users TO student;
GRANT ALL ON users_id_seq TO student;
GRANT ALL ON users_userid_seq TO student;

INSERT INTO profile(name, email, usertype) VALUES('test123', 'test123@umw.edu', 'g');
INSERT INTO users(username, password) VALUES('test123', crypt('test123', gen_salt('bf')));

INSERT INTO profile(name, email, usertype) VALUES('test111', 'test111@umw.edu', 'g');
INSERT INTO users(username, password) VALUES('test111', crypt('test111', gen_salt('bf')));