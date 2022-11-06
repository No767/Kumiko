####################################################################################################
## Builder image
####################################################################################################
FROM python:3.10-alpine3.16 AS builder

RUN apk add --no-cache \
  ca-certificates \
  build-base \
  curl

# Add Poetry locally
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN python -m pip install --upgrade pip setuptools
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /Kumiko

COPY /pyproject.toml /Kumiko/
COPY /poetry.lock /Kumiko/

# Create dependency wheels
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes \
  && pip wheel --wheel-dir=/Kumiko/wheels -r requirements.txt

####################################################################################################
## Final image
####################################################################################################
FROM python:3.10-alpine3.16

# Note that wget is needed for the wait-for script
RUN apk add --no-cache \
  ca-certificates \
  tini \
  bash \
  wget

# Copy anything that is needed for Kumiko
# Docker build context: '.' (root of the repo)
WORKDIR /Kumiko
COPY /Bot/kumikobot.py /Kumiko/Bot/
COPY /scripts/seeder.py /Kumiko/seeder.py
COPY /Bot/Cogs/ /Kumiko/Bot/Cogs
COPY /Bot/Libs/economy_utils/ /Kumiko/Bot/Libs/economy_utils
COPY /Bot/Libs/genshin_wish_sim_utils /Kumiko/Bot/Libs/genshin_wish_sim_utils
COPY /Bot/Libs/admin_logs_utils /Kumiko/Bot/Libs/admin_logs_utils
COPY /Bot/Libs/kumiko_ui_components /Kumiko/Bot/Libs/kumiko_ui_components
COPY /Docker/Alpine-Docker/start.sh /Kumiko/start.sh
COPY /Docker/Alpine-Docker/wait-for /Kumiko/wait-for

# Copy dependency wheels from builder stage
COPY --from=builder /Kumiko/wheels /Kumiko/wheels
COPY --from=builder /Kumiko/requirements.txt /Kumiko/requirements.txt

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools

# Add an unprivileged user and set directory permissions
RUN adduser --disabled-password --gecos "" kumiko \
  && chown -R kumiko:kumiko /Kumiko \
  && chmod +x /Kumiko/start.sh \
  && chmod +x /Kumiko/wait-for

USER kumiko

# Set up path so pip won't complain again
ENV PATH="${PATH}:/home/kumiko/.local/bin"

# Install dependencies
RUN pip install --user --no-index --find-links=/Kumiko/wheels -r requirements.txt

ENTRYPOINT ["/sbin/tini", "--"]

CMD ["/Kumiko/start.sh"]

STOPSIGNAL SIGTERM

# Image metadata
LABEL org.opencontainers.image.title="Kumiko"
LABEL org.opencontainers.image.description="A multipurpose Discord bot built with freedom and choice in mind"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/No767/Kumiko"
