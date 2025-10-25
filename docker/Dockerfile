FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS build

# Compile bytecode and enable caching
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_COMPILE_BYTECODE=1 
ENV UV_LINK_MODE=copy

# Disable Python downloads as the system Python interpreter instead
ENV UV_PYTHON_DOWNLOADS=0

# Set Tini version
# Ref: https://github.com/krallin/tini?tab=readme-ov-file#using-tini
ENV TINI_VERSION=v0.19.0

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini

WORKDIR /app/

COPY pyproject.toml uv.lock /app/

# Install dependencies through lockfile
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Add project source code
COPY ./src /app

# Install the rest (this allows for optimal caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:3.13-slim-trixie

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set up non-root user
RUN groupadd --system --gid 999 app \
 && useradd --system --gid 999 --uid 999 --no-create-home app

# Copy the app from the builder
COPY --from=build /app /app
COPY --from=build --chmod=+x /tini /tini

WORKDIR /app/

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8770

ENTRYPOINT ["/tini", "--"]

CMD ["python3", "/app/main.py"]

STOPSIGNAL SIGTERM

LABEL org.opencontainers.image.title="Kumiko"
LABEL org.opencontainers.image.description="A personal multipurpose Discord bot built with freedom and choice in mind"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/No767/Kumiko"
