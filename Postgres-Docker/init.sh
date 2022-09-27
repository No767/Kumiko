#!/bin/bash

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