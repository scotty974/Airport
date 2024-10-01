DROP DATABASE aeroport;

CREATE DATABASE aeroport;

CREATE TABLE IF NOT EXISTS Airports (
    faa VARCHAR(3) PRIMARY KEY,
    name VARCHAR(100),
    lat REAL,
    lon REAL,
    alt INTEGER,
    tz INTEGER,
    dst VARCHAR(1),
    tzone VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Airlines (
    carrier VARCHAR(2) PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Planes (
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

CREATE TABLE IF NOT EXISTS Weather (
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

CREATE TABLE IF NOT EXISTS Flights (
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