FROM postgres:17.2

ENV POSTGRES_USER=root
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=mydatabase

# A changer, a therme charger le script sql de l'etl ici
COPY ./database/initdb /docker-entrypoint-initdb.d/

EXPOSE 5432
