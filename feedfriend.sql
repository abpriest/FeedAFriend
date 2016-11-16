/*password = mealswipes*/


DROP DATABASE IF EXISTS feedfriend;
CREATE DATABASE feedfriend;

DROP ROLE IF EXISTS student;
CREATE ROLE student WITH password 'mealswipes123' LOGIN;

\c feedfriend

CREATE EXTENSION pgcrypto;

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


INSERT INTO users(username, password) VALUES('testuser', crypt('testpassword',gen_salt('bf')));
INSERT INTO profile(name, email, usertype, userid) VALUES('test', 'test@umw.edu', 'g', (SELECT id FROM users WHERE password = crypt('testpassword',password) AND username = 'testuser'));

SELECT * FROM users WHERE password = crypt('testpassword', password) AND username = 'testuser';

INSERT INTO users(username, password) VALUES('test123', crypt('test123', gen_salt('bf')));
INSERT INTO profile(name, email, usertype, userid) VALUES('test123', 'test123@umw.edu', 'g', (SELECT id FROM users WHERE password = 'testpassword' AND username = 'testuser'));
