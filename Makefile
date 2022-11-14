all: run

dev-setup:
	poetry env use 3.10
	poetry install
	cp .env-dev-example ./Bot/.env
	cp ./docker-compose-dev.yml ./docker-compose.yml

run:
	python Bot/kumikobot.py