FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy project files
COPY pyproject.toml .
COPY uv.lock .
COPY README.md .

# Copy application code (needed for editable install)
COPY src/ src/

# Install Python dependencies with uv
RUN uv sync --frozen --no-dev

# Expose port
EXPOSE 8000

# Default command
CMD ["uv", "run", "python", "-m", "bbgodb.cli", "serve"]
