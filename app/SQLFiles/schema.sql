CREATE TABLE artist (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE,
    hometown VARCHAR(64),
    bio VARCHAR(256) UNIQUE,
);

CREATE TABLE event (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64),
    date VARCHAR(64),
    price INTEGER,
    artistID INTEGER,
    FOREIGN KEY (artistID) REFERENCES artist(id),
    FOREIGN KEY (venueID) REFERENCES venue(id),
);

CREATE TABLE venue (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) UNIQUE,
    location VARCHAR(128),
);
