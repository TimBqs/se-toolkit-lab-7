# Bot Dockerfile - uses uv and pyproject.toml exclusively
FROM python:3.14-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy bot project files
COPY bot/pyproject.toml ./

# Install dependencies using uv (no lock file, will resolve fresh)
RUN uv sync --no-dev

# Copy bot source code
COPY bot/ ./bot/

# Copy env file for local development (Docker uses env vars from compose)
COPY .env.bot.secret .env.bot.secret

# Run the bot from /app directory where .env.bot.secret exists
CMD ["uv", "run", "bot.py"]
