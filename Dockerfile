FROM python:3.12-slim

# Set a working directory
WORKDIR /app

# Install build dependencies and cleanup apt when done
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manifest first for efficient caching
COPY requirements.txt ./

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Ensure SQLite DB data directory exists when using a mounted volume
RUN mkdir -p /app/data

# Expose the app port
EXPOSE 8000

# Default environment variables (can be overridden in compose or docker run)
# By default, store the sqlite DB under `/app/data/shortener.db` so it can be
# persisted via a bind mount at `./data` on the host.
ENV DATABASE_URL="sqlite:///./data/shortener.db" \
    REDIS_HOST=redis \
    REDIS_PORT=6379

# Copy and set entrypoint
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
