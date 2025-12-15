# Database Schema Documentation

## Overview

The bbgodb system uses PostgreSQL for metadata storage and Weaviate for vector embeddings. This document describes the PostgreSQL schema used to track articles, chunks, images, and ingestion logs.

## Tables

### 1. articles

Stores core metadata for ByteByteGo articles ingested from the RSS feed.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| url | VARCHAR(512) | Unique article URL from RSS feed |
| guid | VARCHAR(512) | Unique GUID from RSS feed |
| title | VARCHAR(512) | Article title |
| description | TEXT | Short description/excerpt |
| author | VARCHAR(256) | Article author |
| html_content | TEXT | Full HTML content from RSS |
| raw_text | TEXT | Extracted plain text content |
| featured_image_url | VARCHAR(1024) | URL of featured/cover image |
| published_date | TIMESTAMP | Original publication date |
| fetched_date | TIMESTAMP | When article was fetched |
| last_updated | TIMESTAMP | Last update timestamp |
| is_processed | BOOLEAN | Whether article has been processed |
| is_chunked | BOOLEAN | Whether article has been chunked |
| is_embedded | BOOLEAN | Whether embeddings are generated |
| processing_metadata | JSONB | Processing history, errors, stats |
| content_length | INTEGER | Character count of content |
| chunk_count | INTEGER | Number of chunks created |
| image_count | INTEGER | Number of images extracted |

**Indexes:**
- `url` (unique)
- `guid` (unique)
- `published_date`
- `is_processed`
- `is_embedded`

### 2. article_images

Stores metadata for images extracted from articles.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| article_url | VARCHAR(512) | Reference to parent article URL |
| image_url | VARCHAR(1024) | Image URL |
| alt_text | TEXT | Alt text from HTML |
| caption | TEXT | Caption if available |
| width | INTEGER | Image width in pixels |
| height | INTEGER | Image height in pixels |
| file_size | INTEGER | File size in bytes |
| position_index | INTEGER | Position within article |
| is_embedded | BOOLEAN | Whether image embedding is generated |
| extracted_date | TIMESTAMP | When image was extracted |
| metadata | JSONB | Additional metadata (download path, etc.) |

**Indexes:**
- `article_url`
- `is_embedded`

### 3. article_chunks

Stores text chunks created from articles and their mapping to Weaviate.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| article_url | VARCHAR(512) | Reference to parent article URL |
| chunk_id | VARCHAR(256) | Unique chunk identifier |
| weaviate_id | VARCHAR(256) | ID in Weaviate vector DB |
| text_content | TEXT | Chunk text content |
| chunk_index | INTEGER | Sequential index within article |
| chunk_size | INTEGER | Character count |
| start_position | INTEGER | Start position in original text |
| end_position | INTEGER | End position in original text |
| is_embedded | BOOLEAN | Whether chunk is embedded in Weaviate |
| created_date | TIMESTAMP | When chunk was created |
| metadata | JSONB | Additional metadata (section headers, etc.) |

**Indexes:**
- `chunk_id` (unique)
- `weaviate_id` (unique)
- `article_url`
- `is_embedded`

### 4. ingestion_logs

Tracks ingestion runs for monitoring and debugging.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| run_id | VARCHAR(256) | Unique run identifier |
| started_at | TIMESTAMP | Run start time |
| completed_at | TIMESTAMP | Run completion time |
| articles_found | INTEGER | Total articles in RSS feed |
| articles_new | INTEGER | New articles ingested |
| articles_updated | INTEGER | Updated articles |
| articles_failed | INTEGER | Failed articles |
| status | VARCHAR(50) | Status: running, completed, failed, partial |
| error_message | TEXT | Error details if failed |
| details | JSONB | Additional run details |

**Indexes:**
- `run_id` (unique)
- `started_at`
- `status`

## Relationships

```
articles (1) ───< (N) article_images
         (1) ───< (N) article_chunks
```

- One article can have multiple images
- One article can have multiple chunks
- Relationships are maintained via `article_url` foreign key

## Data Flow

1. **RSS Ingestion**: Articles fetched from RSS feed → stored in `articles` table
2. **Content Processing**: HTML parsed → `raw_text` extracted
3. **Image Extraction**: Images found → stored in `article_images`
4. **Chunking**: Text split into chunks → stored in `article_chunks`
5. **Embedding**: Chunks embedded → stored in Weaviate, `weaviate_id` updated
6. **Status Tracking**: Flags (`is_processed`, `is_chunked`, `is_embedded`) updated

## Usage Examples

### Check ingestion status
```sql
SELECT
    COUNT(*) as total_articles,
    SUM(CASE WHEN is_processed THEN 1 ELSE 0 END) as processed,
    SUM(CASE WHEN is_embedded THEN 1 ELSE 0 END) as embedded
FROM articles;
```

### Get recent articles
```sql
SELECT url, title, published_date, is_embedded
FROM articles
ORDER BY published_date DESC
LIMIT 10;
```

### Find articles needing processing
```sql
SELECT url, title, fetched_date
FROM articles
WHERE is_processed = FALSE
ORDER BY fetched_date ASC;
```

### Get ingestion statistics
```sql
SELECT
    run_id,
    started_at,
    articles_new,
    articles_updated,
    status
FROM ingestion_logs
ORDER BY started_at DESC
LIMIT 5;
```

## Setup Instructions

### 1. Install PostgreSQL
```bash
# macOS
brew install postgresql@14
brew services start postgresql@14

# Ubuntu/Debian
sudo apt-get install postgresql-14
sudo systemctl start postgresql
```

### 2. Create Database
```bash
createdb bbgodb
```

### 3. Set Environment Variables
```bash
cp .env.example .env
# Edit .env and set DATABASE_URL
```

### 4. Initialize Schema
```bash
python scripts/init_db.py
```

### 5. Verify Tables
```bash
psql bbgodb -c "\dt"
```

## Maintenance

### Backup Database
```bash
pg_dump bbgodb > backup_$(date +%Y%m%d).sql
```

### Restore Database
```bash
psql bbgodb < backup_20231215.sql
```

### Reset Database (WARNING: deletes all data)
```bash
python scripts/drop_db.py
python scripts/init_db.py
```

## Performance Considerations

1. **Indexes**: All frequently queried columns are indexed
2. **JSONB**: Used for flexible metadata storage with GIN indexes
3. **Chunking**: Separate table for better query performance
4. **Connection Pooling**: Configured in `database.py` (pool_size=5, max_overflow=10)

## Future Enhancements

- [ ] Add alembic migrations for schema versioning
- [ ] Add materialized views for analytics
- [ ] Add partitioning for large tables
- [ ] Add foreign key constraints with cascade deletes
