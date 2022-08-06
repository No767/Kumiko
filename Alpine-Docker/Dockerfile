####################################################################################################
## Builder image
####################################################################################################
FROM python:3.10.5-alpine3.16 AS builder

# Note that some libaries require Linux Kernel C Headers
RUN apk add --no-cache \
    ca-certificates \
    build-base \
    curl \
    linux-headers 

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
FROM python:3.10.5-alpine3.16

RUN apk add --no-cache \
    ca-certificates \
    tini \
    bash

WORKDIR /Kumiko
COPY /Bot/kumikobot.py /Kumiko/Bot/
COPY /Bot/Cogs/ /Kumiko/Bot/Cogs
COPY /Bot/.env /Kumiko/Bot/
COPY /Bot/economy_utils/ /Kumiko/Bot/economy_utils
COPY /Bot/genshin_wish_sim_utils /Kumiko/Bot/genshin_wish_sim_utils
COPY /Bot/exceptions /Kumiko/Bot/exceptions

# Copy dependency wheels from builder stage
COPY --from=builder /Kumiko/wheels /Kumiko/wheels
COPY --from=builder /Kumiko/requirements.txt /Kumiko/requirements.txt

RUN pip install --upgrade pip setuptools

# Add an unprivileged user and set directory permissions
RUN adduser --disabled-password --gecos "" kumiko \
    && chown -R kumiko:kumiko /Kumiko 

USER kumiko

# Set up path so pip won't complain again
ENV PATH="${PATH}:~/.local/bin"

# Install dependencies
RUN pip install --user --no-index --find-links=/Kumiko/wheels -r requirements.txt

ENTRYPOINT ["/sbin/tini", "--"]

CMD ["python", "/Kumiko/Bot/kumikobot.py"]

STOPSIGNAL SIGTERM

# Image metadata
LABEL org.opencontainers.image.title="Kumiko"
LABEL org.opencontainers.image.description="A multipurpose Discord bot built with freedom and choice in mind"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/No767/Kumiko"