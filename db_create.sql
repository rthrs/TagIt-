-- Created by Vertabelo (http://vertabelo.com)

-- tables
-- Table: Albums
CREATE TABLE Albums (
    album_id bigserial  NOT NULL,
    artist varchar(30)  NOT NULL,
    album varchar(30)  NULL,
    year varchar(4)  NOT NULL,
    img_path varchar(60)  NULL,
    genre int  NOT NULL,
    CONSTRAINT Albums_pk PRIMARY KEY (album_id)
);

-- Table: Fingerprints
CREATE TABLE Fingerprints (
    hash bit(32)  NOT NULL,
    "offset" int  NOT NULL,
    song_id bigserial  NOT NULL,
    CONSTRAINT Fingerprints_pk PRIMARY KEY (hash,"offset",song_id)
);

-- Table: Songs
CREATE TABLE Songs (
    song_id bigserial  NOT NULL,
    title varchar(30)  NOT NULL,
    album_id bigserial  NOT NULL,
    track int  NOT NULL,
    CONSTRAINT Songs_pk PRIMARY KEY (song_id)
);

-- foreign keys
-- Reference: Fingerprints_Songs (table: Fingerprints)
ALTER TABLE Fingerprints ADD CONSTRAINT Fingerprints_Songs 
    FOREIGN KEY (song_id)
    REFERENCES Songs (song_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Songs_Albums (table: Songs)
ALTER TABLE Songs ADD CONSTRAINT Songs_Albums 
    FOREIGN KEY (album_id)
    REFERENCES Albums (album_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

