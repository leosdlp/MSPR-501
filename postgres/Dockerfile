FROM postgres:17.2

ENV POSTGRES_USER=root
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=projet_mspr

COPY ./database/initdb.sql /docker-entrypoint-initdb.d/initdb.sql

EXPOSE 5432
