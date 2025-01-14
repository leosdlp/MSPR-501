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
   latitude NUMERIC(15,10)   NOT NULL,
   longitude NUMERIC(15,15)   NOT NULL,
   name VARCHAR(50)  NOT NULL,
   population INTEGER,
   PRIMARY KEY(id_city)
);

CREATE TABLE continent(
   id_continent SERIAL,
   name VARCHAR(50)  NOT NULL,
   PRIMARY KEY(id_continent)
);

CREATE TABLE country(
   id_country SERIAL,
   name VARCHAR(50)  NOT NULL,
   population INTEGER NOT NULL,
   id_continent INTEGER NOT NULL,
   PRIMARY KEY(id_country),
   FOREIGN KEY(id_continent) REFERENCES continent(id_continent)
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
