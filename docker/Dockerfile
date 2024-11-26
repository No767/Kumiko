FROM python:3.13-slim-bookworm

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  bash \
  gcc \
  git \
  libc6-dev \
  netcat-traditional \
  tini \
  && apt-get clean

WORKDIR /kumiko
COPY bot/ /kumiko/bot/
COPY /docker/start.sh /kumiko/start.sh
COPY /docker/wait-for /kumiko/wait-for
COPY /requirements.txt /kumiko/requirements.txt

RUN adduser --disabled-password --gecos "" kumiko \
  && chown -R kumiko:kumiko /kumiko \
  && chmod +x /kumiko/start.sh \
  && chmod +x /kumiko/wait-for

USER kumiko

ENV PATH="${PATH}:/home/kumiko/.local/bin"

RUN pip install --user -r requirements.txt

EXPOSE 8770

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["/kumiko/start.sh"]

STOPSIGNAL SIGTERM

LABEL org.opencontainers.image.title="Kumiko"
LABEL org.opencontainers.image.description="A personal multipurpose discord bot built with freedom and choice in mind"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/No767/Kumiko"