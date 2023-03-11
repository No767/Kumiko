# Database Setup

Kumiko requires PostgreSQL, and Redis to get started. 

## Setting up the `.env` files

There are two `.env` files that should be found in your project. One is in the `Bot` directory, and the other is in the root directory of the repo. But they aren't named `.env`. So when you run the `dev-setup` command in make, this will rename the dev env file to `.env`, and is found under `Bot/.env`. The other one should remain in the root directory of the repo. Rename `.env-docker-example` to `.env`. Once you set up the credentials within `Bot/.env`, make sure to copy the values to `.env` in the root directory of the repo. **Do not directly copy and paste the contents of `Bot/.env` into to the one in the root of the repo.**

## Migration

There is one last thing that needs to be done. And that is to migrate the data. Run the following command in order to do so:

```sh
prisma db push
```
