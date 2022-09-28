#!/bin/bash

curl -s https://raw.githubusercontent.com/No767/Kumiko/dev/WS-Data/ws_data.csv

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE DATABASE $POSTGRES_ECO_USERS_DB;
    CREATE DATABASE $POSTGRES_WS_DB;
    CREATE DATABASE $POSTGRES_AH_DB;
    CREATE DATABASE $POSTGRES_QUESTS_DB;

    ALTER DATABASE $POSTGRES_ECO_USERS_DB OWNER TO "$POSTGRES_USER";
    ALTER DATABASE $POSTGRES_WS_DB OWNER TO "$POSTGRES_USER";
    ALTER DATABASE $POSTGRES_AH_DB OWNER TO "$POSTGRES_USER";
    ALTER DATABASE $POSTGRES_QUESTS_DB OWNER TO "$POSTGRES_USER";

	GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_ECO_USERS_DB" TO "$POSTGRES_USER";
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_WS_DB" TO "$POSTGRES_USER";
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_AH_DB" TO "$POSTGRES_USER";
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_QUESTS_DB" TO "$POSTGRES_USER";
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_WS_DB" <<-EOSQL
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

    ALTER TABLE public.ws_data OWNER TO "$POSTGRES_USER";

    \copy public.ws_data FROM './ws_data.csv' DELIMITER ',' CSV

    ALTER TABLE ONLY public.ws_data
        ADD CONSTRAINT ws_data_pkey PRIMARY KEY (uuid);
EOSQL

rm ws_data.csv

echo "Finished creating and copying data for PostgreSQL"