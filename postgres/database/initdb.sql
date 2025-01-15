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

-- Jeux de données

INSERT INTO disease (name, is_pandemic) VALUES
('COVID-19', TRUE),
('Grippe', FALSE),
('Ebola', TRUE),
('Varicelle', FALSE);

INSERT INTO statement (_date, confirmed, deaths, recovered, active, total_tests, new_deaths, new_cases, new_recovered, id_disease) VALUES
('2025-01-01', 1000000, 50000, 900000, 50000, 5000000, 1000, 5000, 7000, 1),
('2025-01-02', 1005000, 50500, 905000, 50000, 5050000, 1500, 6000, 7500, 2),
('2025-01-03', 500000, 3000, 450000, 50000, 1000000, 200, 2000, 2500, 3),
('2025-01-04', 200000, 1000, 190000, 9000, 2000000, 100, 1000, 1500, 4);

INSERT INTO region (name, population) VALUES
('Europe', 741400000),
('Afrique', 1340000000),
('Amérique du Nord', 579024000);

INSERT INTO city (latitude, longitude, name, population) VALUES
(48.8566, 2.3522, 'Paris', 2148327),
(34.0522, -118.2437, 'Los Angeles', 3979576),
(40.7128, -74.0060, 'New York', 8419600);

INSERT INTO continent (name) VALUES
('Europe'),
('Afrique'),
('Amérique du Nord'),
('Asie'),
('Océanie');

INSERT INTO climat_type (name, description) VALUES
('Tropical', 'Chaud et humide, avec des pluies abondantes'),
('Tempéré', 'Saisons distinctes, étés modérés et hivers froids'),
('Désertique', 'Climat sec avec peu de pluie'),
('Polaire', 'Très froid, peu de végétation');

INSERT INTO country (name, population, pib, id_climat_type, id_continent) VALUES
('France', 67390000, 2700000000000, 2, 1),
('USA', 331000000, 23000000000000, 2, 3),
('Chine', 1393400000, 14000000000000, 1, 4),
('Brésil', 211000000, 2200000000000, 1, 2);

INSERT INTO weather_report (date_start, date_end, average_temperature, average_wind_velocity, humidity_level, id_country) VALUES
('2025-01-01', '2025-01-02', 15.5, 10.2, 60.0, 1),
('2025-01-02', '2025-01-03', 22.0, 12.5, 50.0, 2),
('2025-01-03', '2025-01-04', 18.0, 5.0, 70.0, 3),
('2025-01-04', '2025-01-05', 30.0, 8.0, 40.0, 4);

INSERT INTO place_statement (id_country, id_statement, id_region, id_city) VALUES
(1, 1, 1, 1),
(2, 2, 2, 2),
(3, 3, 3, 3),
(4, 4, 2, 2);