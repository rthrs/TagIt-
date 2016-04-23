-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2016-04-23 09:41:07.171

-- Table: Fingerprints
CREATE TABLE Fingerprints (
    hash varchar(32)  NOT NULL,
    off int  NOT NULL,
    song_id bigserial  NOT NULL,
    CONSTRAINT Fingerprints_pk PRIMARY KEY (hash,off,song_id)
);

-- Table: Songs
CREATE TABLE Songs (
    song_id SERIAL PRIMARY KEY,
    title varchar(30)  NOT NULL,
    artist varchar(30)  NOT NULL,
    album varchar(30),
    year varchar(4),
    track int
);

CREATE INDEX hash_index ON Fingerprints(hash);
