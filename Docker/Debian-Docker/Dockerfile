####################################################################################################
## Builder image
####################################################################################################
FROM python:3.11-slim-bullseye AS builder

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt update \
  && apt install -y --no-install-recommends \
  build-essential \
  ca-certificates \
  curl

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN python -m pip install --upgrade pip setuptools
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /Kumiko

COPY /pyproject.toml /Kumiko/
COPY /poetry.lock /Kumiko/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --without=dev,test \
  && pip wheel --wheel-dir=/Kumiko/wheels -r requirements.txt

####################################################################################################
## Final image
####################################################################################################
FROM python:3.11-slim-bullseye

RUN apt update \
  && apt install -y --no-install-recommends \
  tini \
  ca-certificates \
  bash \
  netcat \
  libopus-dev \
  libffi-dev \
  libnacl-dev

WORKDIR /Kumiko
COPY /Bot/kumikobot.py /Kumiko/Bot/
COPY /Bot/kumikocore.py /Kumiko/Bot/
COPY /Bot/Cogs/ /Kumiko/Bot/Cogs
COPY /Bot/Libs/ /Kumiko/Bot/Libs/
COPY /scripts/init-db.py /Kumiko/init-db.py
COPY /scripts/seeder.py /Kumiko/seeder.py
COPY /Docker/Debian-Docker/start.sh /Kumiko/start.sh
COPY /Docker/Debian-Docker/wait-for /Kumiko/wait-for

COPY --from=builder /Kumiko/wheels /Kumiko/wheels
COPY --from=builder /Kumiko/requirements.txt /Kumiko/requirements.txt

RUN pip install --upgrade pip setuptools

RUN adduser --disabled-password --gecos "" kumiko \
  && chown -R kumiko:kumiko /Kumiko \
  && chmod +x /Kumiko/start.sh \
  && chmod +x /Kumiko/wait-for

USER kumiko

ENV PATH="${PATH}:/home/kumiko/.local/bin"

RUN pip install --user --no-index --find-links=/Kumiko/wheels -r requirements.txt

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["/Kumiko/start.sh"]

STOPSIGNAL SIGTERM

LABEL org.opencontainers.image.title="Kumiko"
LABEL org.opencontainers.image.description="A multipurpose Discord bot built with freedom and choice in mind"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/No767/Kumiko"
