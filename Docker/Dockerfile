# ####################################################################################################
# ## Builder image
# ####################################################################################################
FROM python:3.11-slim-bookworm AS builder

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  curl \
  git

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /Kumiko

COPY /pyproject.toml /Kumiko/
COPY /poetry.lock /Kumiko/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --only main

####################################################################################################
## Final image
####################################################################################################
FROM python:3.11-slim-bookworm

RUN apt update \
  && apt install -y --no-install-recommends \
  tini \
  bash \
  netcat-traditional \
  libopus-dev \
  libffi-dev \
  libsodium-dev \
  git

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /Kumiko

COPY /pyproject.toml /Kumiko/
COPY /poetry.lock /Kumiko/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --only main

WORKDIR /Kumiko
COPY /Bot/kumikobot.py /Kumiko/Bot/
COPY /Bot/kumikocore.py /Kumiko/Bot/
COPY /Migrations /Kumiko/Migrations
COPY /Bot/Cogs /Kumiko/Bot/Cogs
COPY /Bot/Libs /Kumiko/Bot/Libs/
COPY /migrations-runner.py /Kumiko/migrations-runner.py
COPY /Docker/start.sh /Kumiko/start.sh
COPY /Docker/wait-for /Kumiko/wait-for

COPY --from=builder /Kumiko/requirements.txt /Kumiko/requirements.txt

RUN adduser --disabled-password --gecos "" kumiko \
  && chown -R kumiko:kumiko /Kumiko \
  && chmod +x /Kumiko/start.sh \
  && chmod +x /Kumiko/wait-for

USER kumiko

ENV PATH="${PATH}:/home/kumiko/.local/bin"

RUN pip install --user -r requirements.txt

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["/Kumiko/start.sh"]

STOPSIGNAL SIGTERM

LABEL org.opencontainers.image.title="Kumiko"
LABEL org.opencontainers.image.description="A multipurpose Discord bot built with freedom and choice in mind"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/No767/Kumiko"