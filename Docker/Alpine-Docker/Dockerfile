####################################################################################################
## Builder image
####################################################################################################
FROM python:3.11-alpine3.16 AS builder

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

RUN curl https://sh.rustup.rs -sSf | sh -s -- --profile minimal --default-toolchain stable -y
ENV PATH="${PATH}:/root/.cargo/bin"

WORKDIR /Kumiko

COPY /pyproject.toml /Kumiko/
COPY /poetry.lock /Kumiko/

# Create dependency wheels
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes \
  && pip wheel --wheel-dir=/Kumiko/wheels -r requirements.txt

####################################################################################################
## Final image
####################################################################################################
FROM python:3.11-alpine3.16

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
COPY /Bot/kumikocore.py /Kumiko/Bot/
COPY /scripts/seeder.py /Kumiko/seeder.py
COPY /scripts/seeder-v2.py /Kumiko/seeder-v2.py
COPY /Bot/Cogs/ /Kumiko/Bot/Cogs
COPY /Bot/Libs/ /Kumiko/Bot/Libs/
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
