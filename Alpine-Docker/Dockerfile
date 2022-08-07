####################################################################################################
## Builder image
####################################################################################################
FROM python:3.10.6-alpine3.16 AS builder

RUN apk add --no-cache \
    ca-certificates \
    build-base 

WORKDIR /Rin

COPY /Pipfile* /Rin/

# Create dependency wheels
RUN pip install --upgrade pip wheel setuptools pipenv \
    && pipenv lock -r > requirements.txt \
    && pip wheel --wheel-dir=/Rin/wheels -r requirements.txt

####################################################################################################
## Final image
####################################################################################################
FROM python:3.10.6-alpine3.16

RUN apk add --no-cache \
    ca-certificates \
    tini \
    bash

WORKDIR /Rin

COPY /Bot/rinbot.py /Rin/Bot/
COPY /Bot/Cogs/ /Rin/Bot/Cogs

# Copy dependency wheels from builder stage
COPY --from=builder /Rin/wheels /Rin/wheels
COPY --from=builder /Rin/requirements.txt /Rin/requirements.txt

COPY /Alpine-Docker/start.sh /Rin/start.sh

RUN pip install --upgrade pip

# Add an unprivileged user and set directory permissions
RUN adduser --disabled-password --gecos "" rin \
    && chown -R rin:rin /Rin \
    && chmod +x /Rin/start.sh

USER rin

# Install dependencies
RUN pip install --user --no-index --find-links=/Rin/wheels -r requirements.txt

ENTRYPOINT ["/sbin/tini", "--"]

CMD ["/Rin/start.sh"]

STOPSIGNAL SIGTERM

# Image metadata
LABEL org.opencontainers.image.title="Rin"
LABEL org.opencontainers.image.description="Discord bot focused on obtaining data from third-party services with lighting performance in mind"
LABEL org.opencontainers.image.url="https://rinbot.live"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/No767/Rin"