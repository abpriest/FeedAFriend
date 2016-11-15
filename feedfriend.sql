/*password = mealswipes*/
CREATE EXTENSION pgcrypto;

DROP DATABASE IF EXISTS feedfriend;
CREATE DATABASE feedfriend;

DROP ROLE IF EXISTS student;
CREATE ROLE student WITH password 'mealswipes123' LOGIN;

\c feedfriend
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id serial NOT NULL,
    username text NOT NULL,
    password text NOT NULL,
    PRIMARY KEY (id)
);

GRANT ALL ON users TO student;
GRANT ALL ON users_id_seq TO student;

DROP TABLE IF EXISTS profile;
CREATE TABLE profile (
    id serial NOT NULL,
    name varchar(20) NOT NULL,
    email varchar(15) NOT NULL,
    usertype varchar(1) NOT NULL,
    image bytea,
    PRIMARY KEY (id),
    
    userid serial NOT NULL,
    CONSTRAINT users_userid_fkq
    FOREIGN KEY (userid)
    REFERENCES users (id)
);

GRANT ALL ON profile TO student;
GRANT ALL ON profile_id_seq TO student;
GRANT ALL ON profile_userid_seq TO student;


INSERT INTO users(username, password) VALUES('testuser', 'testpassword');
INSERT INTO profile(name, email, usertype, userid) VALUES('test', 'test@umw.edu', 'g', (SELECT id FROM users WHERE password = 'testpassword' AND username = 'testuser'));

SELECT * FROM users WHERE password = crypt('testpassword', password) AND username = 'testuser';
