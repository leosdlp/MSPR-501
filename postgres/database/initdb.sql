DO $$ 
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'projet_mspr') THEN
      CREATE DATABASE projet_mspr;
   END IF;
END $$;

\c projet_mspr

CREATE TABLE disease(
   id_disease SERIAL,
   name VARCHAR(50)  NOT NULL,
   is_pandemic BOOLEAN NOT NULL,
   PRIMARY KEY(id_disease)
);

CREATE TABLE statement(
   id_statement SERIAL,
   _date DATE NOT NULL,
   confirmed INTEGER NOT NULL,
   deaths INTEGER NOT NULL,
   recovered INTEGER NOT NULL,
   active INTEGER NOT NULL,
   total_tests INTEGER,
   new_deaths INTEGER NOT NULL,
   new_cases INTEGER NOT NULL,
   new_recovered INTEGER NOT NULL,
   id_disease INTEGER NOT NULL,
   PRIMARY KEY(id_statement),
   FOREIGN KEY(id_disease) REFERENCES disease(id_disease)
);

CREATE TABLE region(
   id_region SERIAL,
   name VARCHAR(50)  NOT NULL,
   population INTEGER,
   PRIMARY KEY(id_region)
);

CREATE TABLE city(
   id_city SERIAL,
   latitude NUMERIC(14,7)   NOT NULL,
   longitude NUMERIC(14,7)   NOT NULL,
   name VARCHAR(50)  NOT NULL,
   population INTEGER,
   PRIMARY KEY(id_city)
);

CREATE TABLE continent(
   id_continent SERIAL,
   name VARCHAR(50)  NOT NULL,
   PRIMARY KEY(id_continent)
);

CREATE TABLE climat_type(
   id_climat_type SERIAL,
   name VARCHAR(50)  NOT NULL,
   description VARCHAR(50) ,
   PRIMARY KEY(id_climat_type)
);

CREATE TABLE country(
   id_country SERIAL,
   name VARCHAR(50)  NOT NULL,
   population INTEGER NOT NULL,
   pib MONEY,
   id_climat_type INTEGER NOT NULL,
   id_continent INTEGER NOT NULL,
   PRIMARY KEY(id_country),
   FOREIGN KEY(id_climat_type) REFERENCES climat_type(id_climat_type),
   FOREIGN KEY(id_continent) REFERENCES continent(id_continent)
);

CREATE TABLE weather_report(
   id_weather_report SERIAL,
   date_start DATE NOT NULL,
   date_end DATE NOT NULL,
   average_temperature NUMERIC(15,2)  ,
   average_wind_velocity NUMERIC(15,2)  ,
   humidity_level NUMERIC(15,2)  ,
   id_country INTEGER NOT NULL,
   PRIMARY KEY(id_weather_report),
   FOREIGN KEY(id_country) REFERENCES country(id_country)
);

CREATE TABLE place_statement(
   id_country INTEGER,
   id_statement INTEGER,
   id_region INTEGER,
   id_city INTEGER,
   PRIMARY KEY(id_country, id_statement, id_region, id_city),
   FOREIGN KEY(id_country) REFERENCES country(id_country),
   FOREIGN KEY(id_statement) REFERENCES statement(id_statement),
   FOREIGN KEY(id_region) REFERENCES region(id_region),
   FOREIGN KEY(id_city) REFERENCES city(id_city)
);
