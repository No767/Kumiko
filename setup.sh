curl -s -o docker-compose.yml -q https://raw.githubusercontent.com/No767/Kumiko/dev/docker-compose-example.yml \
&& curl -s -o .env -q https://raw.githubusercontent.com/No767/Kumiko/dev/.env-docker-example
echo "Downloaded and set up all the files needed for Kumiko!"
