# Local Development Setup

## Prerequisites
- Docker and Docker Compose installed
- Python 3.10+ installed

## Quick Start

### 1. Start Database Services
```bash
# Start PostgreSQL and Redis in Docker
docker compose up -d postgres redis

# Verify services are running
docker compose ps

# Check PostgreSQL is healthy
docker compose exec postgres pg_isready -U bbgodb
```

### 2. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# The .env file is pre-configured for Docker Compose setup
# Default credentials:
# - Database: bbgodb
# - User: bbgodb
# - Password: bbgodb_dev_password
# - Host: localhost (when running scripts from host)
# - Port: 5432
```

### 3. Initialize Database Schema
```bash
# Install Python dependencies (if not already done)
pip install -e .

# Create database tables
python scripts/init_db.py
```

### 4. Verify Setup
```bash
# Connect to PostgreSQL
docker compose exec postgres psql -U bbgodb -d bbgodb

# Inside psql, verify tables:
\dt

# Expected output:
#              List of relations
#  Schema |      Name       | Type  | Owner
# --------+-----------------+-------+--------
#  public | article_chunks  | table | bbgodb
#  public | article_images  | table | bbgodb
#  public | articles        | table | bbgodb
#  public | ingestion_logs  | table | bbgodb

# Exit psql
\q
```

## Database URLs Explained

**From Host Machine (running scripts locally):**
```
DATABASE_URL=postgresql://bbgodb:bbgodb_dev_password@localhost:5432/bbgodb
```
- Host: `localhost` (Docker exposes port 5432)

**From Inside Docker (API service):**
```
DATABASE_URL=postgresql://bbgodb:bbgodb_dev_password@postgres:5432/bbgodb
```
- Host: `postgres` (Docker service name)
- This is configured in docker-compose.yml

## Common Commands

```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs -f postgres

# Reset database (WARNING: deletes all data)
python scripts/drop_db.py
python scripts/init_db.py

# Access PostgreSQL CLI
docker compose exec postgres psql -U bbgodb -d bbgodb
```

## Troubleshooting

**Connection refused:**
```bash
# Make sure PostgreSQL is running
docker compose ps postgres

# Check if port 5432 is exposed
docker compose port postgres 5432
```

**Authentication failed:**
```bash
# Verify credentials in .env match docker-compose.yml
# Default: bbgodb / bbgodb_dev_password
```

**Tables not found:**
```bash
# Run initialization script
python scripts/init_db.py
```
