FROM library/postgres:latest

WORKDIR /docker-entrypoint-initdb.d

COPY /Docker/Postgres-Docker/init.sh /docker-entrypoint-initdb.d/
COPY /Docker/Postgres-Docker/ws-data-init.sh /docker-entrypoint-initdb.d/
COPY /Docker/Postgres-Docker/ws_data.csv /docker-entrypoint-initdb.d/