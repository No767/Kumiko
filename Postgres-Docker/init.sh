#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
	CREATE DATABASE $POSTGRES_KUMIKO_DB;
    ALTER DATABASE $POSTGRES_KUMIKO_DB OWNER TO "$POSTGRES_USER";
	GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_KUMIKO_DB" TO "$POSTGRES_USER";
EOSQL