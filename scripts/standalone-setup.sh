#!/bin/bash

curl -s -o ws_data.csv https://raw.githubusercontent.com/No767/Kumiko/dev/Postgres-Docker/ws_data.csv

set -e

PGPASSWORD="$POSTGRES_PASSWORD" psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USERNAME" --dbname "$POSTGRES_DB" --host="$POSTGRES_IP" <<-EOSQL
	CREATE DATABASE $POSTGRES_ECO_USERS_DB;
    CREATE DATABASE $POSTGRES_WS_DB;
    CREATE DATABASE $POSTGRES_AH_DB;
    CREATE DATABASE $POSTGRES_QUESTS_DB;

    ALTER DATABASE $POSTGRES_ECO_USERS_DB OWNER TO "$POSTGRES_USERNAME";
    ALTER DATABASE $POSTGRES_WS_DB OWNER TO "$POSTGRES_USERNAME";
    ALTER DATABASE $POSTGRES_AH_DB OWNER TO "$POSTGRES_USERNAME";
    ALTER DATABASE $POSTGRES_QUESTS_DB OWNER TO "$POSTGRES_USERNAME";

	GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_ECO_USERS_DB" TO "$POSTGRES_USERNAME";
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_WS_DB" TO "$POSTGRES_USERNAME";
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_AH_DB" TO "$POSTGRES_USERNAME";
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_QUESTS_DB" TO "$POSTGRES_USERNAME";
EOSQL


PGPASSWORD="$POSTGRES_PASSWORD" psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USERNAME" --dbname "$POSTGRES_WS_DB" --host="$POSTGRES_IP"  <<-EOSQL
    SET statement_timeout = 0;
    SET lock_timeout = 0;
    SET idle_in_transaction_session_timeout = 0;
    SET client_encoding = 'UTF8';
    SET standard_conforming_strings = on;
    SELECT pg_catalog.set_config('search_path', '', false);
    SET check_function_bodies = false;
    SET xmloption = content;
    SET client_min_messages = warning;
    SET row_security = off;

    SET default_tablespace = '';

    SET default_table_access_method = heap;

    CREATE TABLE public.ws_data (
        uuid character varying NOT NULL,
        event_name character varying,
        name character varying,
        description text,
        star_rank integer,
        type character varying
    );

    ALTER TABLE public.ws_data OWNER TO "$POSTGRES_USERNAME";

    \copy public.ws_data FROM './ws_data.csv' DELIMITER ',' CSV

    ALTER TABLE ONLY public.ws_data
        ADD CONSTRAINT ws_data_pkey PRIMARY KEY (uuid);
EOSQL

rm *.csv || rm. *.csv.*

echo "Finished creating and copying data for PostgreSQL"