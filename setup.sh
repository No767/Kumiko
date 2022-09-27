mkdir ~/.kumiko
cd ~/.kumiko && mkdir Postgres-Docker
cd Postgres-Docker && wget -q https://raw.githubusercontent.com/No767/Kumiko/dev/Postgres-Docker/Dockerfile \
&& wget -q https://raw.githubusercontent.com/No767/Kumiko/dev/Postgres-Docker/init.sh \
&& wget -q https://raw.githubusercontent.com/No767/Kumiko/dev/Postgres-Docker/ws-data-init.sh \
&& wget -q https://raw.githubusercontent.com/No767/Kumiko/dev/Postgres-Docker/ws_data.csv
cd .. && wget -O docker-compose.yml -q https://raw.githubusercontent.com/No767/Kumiko/dev/docker-compose-example.yml \
&& wget -O .env -q https://raw.githubusercontent.com/No767/Kumiko/dev/.env-docker-example
echo "Downloaded and set up all the files needed for Kumiko!"