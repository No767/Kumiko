BOT_TOKEN ?=
PM2_PUBLIC_KEY_INGEST ?=
PM2_SECRET_KEY_INGEST ?=
DOCKER_TAG_VERSION ?=

all: run

dev-setup:
	pip install --upgrade pip setuptools wheel pipenv
	pipenv --python 3.10
	pipenv install --dev

init:
	touch Bot/.env
	echo 'TOKEN="$(BOT_TOKEN)"'  >> Bot/.env

run:
	python Bot/rinbot.py

deploy: 
	sudo docker build -t no767/rin:$(DOCKER_TAG_VERSION) --build-arg PM2_PUBLIC_KEY_INGEST=$(PM2_PUBLIC_KEY_INGEST) --build-arg PM2_SECRET_KEY_INGEST=$(PM2_SECRET_KEY_INGEST) -f ./Ubuntu-Docker/Dockerfile .