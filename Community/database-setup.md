# Database Setup

Kumiko requires PostgreSQL, MongoDB and Redis to get started. 

## Setting up the `.env` files

There are two `.env` files that should be found in your project. One is in the `Bot` directory, and the other is in the root directory of the repo. But they aren't named `.env`. So when you run the `dev-setup` command in make, this will rename the dev env file to `.env`, and is found under `Bot/.env`. The other one should remain in the root directory of the repo. Rename `.env-docker-example` to `.env`. Once you set up the credentials within `Bot/.env`, make sure to copy the values to `.env` in the root directory of the repo. **Do not directly copy and paste the contents of `Bot/.env` into to the one in the root of the repo.**

> **Note**
> When you get to the variables that refer to the host, this is referring to the host machine of where the servers for the databases are being ran. If you are running them locally using Docker Compose, use your IPv4 address as the host. 

## PostgreSQL Setup

Kumiko's Economy requires PostgreSQL first. The easiest way to do so is to use PostgreSQL on Docker. You can find instructions on how to do this [here](https://hub.docker.com/_/postgres). When making the password, please don't include anything with `@` in it. Asyncpg will complain about it and not connect to the database. Next look at the `.env` file now in your `Bot` directory. Edit the values for the PostgreSQL section, and make sure to keep the `Postgres_Username` and `Postgres_Kumiko_Database` with the same values. This is not needed, but good practice to do so. 


## MongoDB Setup

Kumiko's Economy (specifically the marketplace) relies on MongoDB to deal with the database storage. And the easiest way to deal with that is to use MongoDB on Docker (Image can be found [here](https://hub.docker.com/_/mongo)). When making the password, please don't include anything with `@` in it. Beanie may also start complaining about special characters and then refuses to connect because of it (also blame MongoDB for that as well). Next look at the `.env` file now in your `Bot` directory. Edit the values for the MongoDB section., and save the file

## Redis Setup

Kumiko also relies on Redis for parts of the Auction House, and for general caching. And you guessed it, the easiest way to run Redis is on Docker. You can find the image [here](https://hub.docker.com/_/redis). Look at the `.env` file now in your `Bot` directory. Edit the values for the Redis section, and save the file

## Docker Compose 

Now you have the values edited and ready to go, you'll need to fire up the Docker Compose stack. If you ran the command `make dev-setup`, there is a part where it copies `docker-compose-dev.yml` to `docker-compose.yml`. This is done for your convenience. You can fire up the Docker Compose stack just like this:

```sh
sudo docker compose up -d
```
## Last Minute Setup

There is 1 last thing that needs to be done before you can start working on Kumiko. Make sure to run the PostgreSQL seeder scripts. You'll need to run `postgres-init.py` and `seeder-v2.py`. These can be found within your `script` directory. Here's an example of how to run them:

```bash
poetry run python scripts/postgres-init.py
poetry run python scripts/seeder-v2.py
```
