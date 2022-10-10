BOT_TOKEN ?=
DOCKER_TAG_VERSION ?=

all: run

dev-setup:
	poetry env use 3.10
	poetry install

init:
	touch Bot/.env
	echo 'TOKEN="$(BOT_TOKEN)"'  >> Bot/.env

run:
	python Bot/kumikobot.py