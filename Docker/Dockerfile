####################################################################################################
## Final image
####################################################################################################
FROM python:3.12-slim-bookworm

RUN apt update \
  && apt install -y --no-install-recommends \
  tini \
  bash \
  netcat-traditional \
  libffi-dev \
  libnacl-dev \
  git \
  gcc \
  libc6-dev \
  && apt-get clean

WORKDIR /Kumiko
COPY /Bot/ /Kumiko/Bot/
COPY /Docker/start.sh /Kumiko/start.sh
COPY /Docker/wait-for /Kumiko/wait-for
COPY /requirements.txt /Kumiko/requirements.txt

RUN adduser --disabled-password --gecos "" kumiko \
  && chown -R kumiko:kumiko /Kumiko \
  && chmod +x /Kumiko/start.sh \
  && chmod +x /Kumiko/wait-for

USER kumiko

ENV PATH="${PATH}:${HOME}/.local/bin"

RUN pip install --user -r requirements.txt

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["/Kumiko/start.sh"]

STOPSIGNAL SIGTERM

LABEL org.opencontainers.image.title="Kumiko"
LABEL org.opencontainers.image.description="A multipurpose Discord bot built with freedom and choice in mind"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/No767/Kumiko"