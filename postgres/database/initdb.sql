DO $$ 
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'projet_mspr') THEN
      CREATE DATABASE projet_mspr;
   END IF;
END $$;

\c projet_mspr

CREATE TABLE IF NOT EXISTS mytable (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO mytable (name) VALUES ('John Doe');
INSERT INTO mytable (name) VALUES ('Jane Smith');
INSERT INTO mytable (name) VALUES ('Alice Johnson');
