DROP DATABASE IF EXISTS feedfriend;
CREATE DATABASE feedfriend;

DROP ROLE IF EXISTS student;
CREATE ROLE student WITH password 'mealswipes123' LOGIN;

\c feedfriend

CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS usertype;
CREATE TABLE usertype(
    id serial NOT NULL,
    userT text NOT NULL,
    PRIMARY KEY(id)
);

GRANT ALL ON usertype TO student;
GRANT ALL ON usertype_id_seq TO student;

INSERT INTO usertype(userT) VALUES('Giver'),('Receiver');

DROP TABLE IF EXISTS mealtype;
CREATE TABLE mealtype(
    id serial NOT NULL,
    meal text NOT NULL,
    PRIMARY KEY(id)
);

GRANT ALL ON mealtype TO student;
GRANT ALL ON mealtype_id_seq TO student;

INSERT INTO mealtype(meal) VALUES('Breakfast'),('Lunch'),('Dinner');

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
    email varchar(25) NOT NULL,
    usertype int NOT NULL,
    image bytea,
    PRIMARY KEY (id),
    
    userid int,
    CONSTRAINT users_id_fk
    FOREIGN KEY (userid)
    REFERENCES users (id)
);

GRANT ALL ON profile TO student;
GRANT ALL ON profile_id_seq TO student;

DROP TABLE IF EXISTS availability;
CREATE TABLE availability (
    id serial NOT NULL,
    mealtype int NOT NULL,
    starttime varchar(4),
    endtime varchar(4),
    PRIMARY KEY (id),
    
    userid int,
    CONSTRAINT users_id_fk
    FOREIGN KEY (userid)
    REFERENCES users (id)
    
);

GRANT ALL ON availability TO student;
GRANT ALL ON availability_id_seq TO student;

-- Table for Requests
DROP TABLE IF EXISTS requests;
CREATE TABLE requests (
    id serial NOT NULL,
    availability_id integer REFERENCES availability,
    requested_id integer REFERENCES users,
    PRIMARY KEY (id)
);

GRANT ALL ON requests TO student;
GRANT ALL ON requested_id_seq TO student;

INSERT INTO users(username, password) VALUES('testuser', crypt('testpassword', gen_salt('bf')));
INSERT INTO profile(name, email, usertype, userid) VALUES('testuser', 'test@umw.edu', (SELECT id FROM usertype WHERE userT = 'Giver'), (SELECT id FROM users WHERE username = 'testuser'));

INSERT INTO users(username, password) VALUES('testg', crypt('testg', gen_salt('bf')));
INSERT INTO profile(name, email, usertype, userid) VALUES('testg', 'testgiver@umw.edu', (SELECT id FROM usertype WHERE userT = 'Giver'), (SELECT id FROM users WHERE username = 'testg'));

INSERT INTO users(username, password) VALUES('testr', crypt('testr', gen_salt('bf')));
INSERT INTO profile(name, email, usertype, userid) VALUES('testr', 'testreceiver@umw.edu', (SELECT id FROM usertype WHERE userT = 'Receiver'), (SELECT id FROM users WHERE username = 'testr'));
