DROP DATABASE IF EXISTS aeroport;

CREATE DATABASE aeroport;

DROP TABLE IF EXISTS flights;
DROP TABLE IF EXISTS weather;
DROP TABLE IF EXISTS planes;
DROP TABLE IF EXISTS airlines;
DROP TABLE IF EXISTS airports;

CREATE TABLE IF NOT EXISTS airports (
    faa VARCHAR(3) PRIMARY KEY,
    name VARCHAR(100),
    lat REAL,
    lon REAL,
    alt INTEGER,
    tz INTEGER,
    dst VARCHAR(1),
    tzone VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS airlines (
    carrier VARCHAR(2) PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS planes (
    tailnum VARCHAR(10) PRIMARY KEY,
    year INTEGER,
    type VARCHAR(100),
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    engines INTEGER,
    seats INTEGER,
    speed INTEGER,
    engine VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS weather (
    origin VARCHAR(3),
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    temp REAL,
    dewp REAL,
    humid REAL,
    wind_dir INTEGER,
    wind_speed REAL,
    wind_gust REAL,
    precip REAL,
    pressure REAL,
    visib REAL,
    time_hour TIMESTAMP,
    PRIMARY KEY (origin, year, month, day, hour),
    FOREIGN KEY (origin) REFERENCES Airports(faa)
);

CREATE TABLE IF NOT EXISTS flights (
    flight_id SERIAL PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    dep_time INTEGER,
    arr_time INTEGER,
    sched_dep_time INTEGER,
    sched_arr_time INTEGER,
    dep_delay INTEGER,
    arr_delay INTEGER,
    carrier VARCHAR(2),
    tailnum VARCHAR(10),
    flight INTEGER,
    origin VARCHAR(3),
    dest VARCHAR(3),
    air_time INTEGER,
    distance INTEGER,
    time_hour TIMESTAMP,
    FOREIGN KEY (carrier) REFERENCES Airlines(carrier),
    FOREIGN KEY (tailnum) REFERENCES Planes(tailnum),
    FOREIGN KEY (origin) REFERENCES Airports(faa),
    FOREIGN KEY (dest) REFERENCES Airports(faa)
);