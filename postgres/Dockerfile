FROM postgres:17.2

ENV POSTGRES_DB=mspr501
ENV POSTGRES_USER=mspr501
ENV POSTGRES_PASSWORD=s5t4v5

COPY ./data/data.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
