FROM library/postgres:latest

WORKDIR /docker-entrypoint-initdb.d

COPY /Postgres-Docker/init.sh /docker-entrypoint-initdb.d/
# COPY /WS-Data/ws_data.sql /docker-entrypoint-initdb.d/ # Deal with this later