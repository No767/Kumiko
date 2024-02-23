#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE ROLE kumiko WITH LOGIN PASSWORD "$KUMIKO_PASSWORD";
  CREATE DATABASE kumiko OWNER kumiko;
EOSQL

psql -v ON_ERROR_STOP=1 --username "kumiko" --dbname "kumiko" <<-EOSQL
  CREATE EXTENSION IF NOT EXISTS pg_trgm;
EOSQL
