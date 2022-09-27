FROM library/postgres:latest

WORKDIR /docker-entrypoint-initdb.d

COPY /Postgres-Docker/init.sh /docker-entrypoint-initdb.d/
COPY /Postgres-Docker/ws-data-init.sh /docker-entrypoint-initdb.d/
COPY /Postgres-Docker/ws_data.csv /docker-entrypoint-initdb.d/