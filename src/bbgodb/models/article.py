"""
Article model for storing ByteByteGo article metadata.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Article(Base):
    """
    Represents a ByteByteGo article with its metadata.

    This table stores the core article information extracted from the RSS feed.
    The actual content chunks and embeddings are stored separately in Weaviate.
    """

    __tablename__ = "articles"

    # Primary identifiers
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(512), unique=True, nullable=False, index=True)
    guid = Column(String(512), unique=True, nullable=False)

    # Article metadata
    title = Column(String(512), nullable=False)
    description = Column(Text, nullable=True)
    author = Column(String(256), nullable=True)

    # Content
    html_content = Column(Text, nullable=False)
    raw_text = Column(Text, nullable=True)

    # Featured image
    featured_image_url = Column(String(1024), nullable=True)

    # Timestamps
    published_date = Column(DateTime, nullable=False)
    fetched_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_updated = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Processing status
    is_processed = Column(Boolean, default=False, nullable=False)
    is_chunked = Column(Boolean, default=False, nullable=False)
    is_embedded = Column(Boolean, default=False, nullable=False)

    # Processing metadata - stores processing history, errors, etc.
    processing_metadata = Column(JSONB, nullable=True)

    # Statistics
    content_length = Column(Integer, nullable=True)
    chunk_count = Column(Integer, default=0, nullable=False)
    image_count = Column(Integer, default=0, nullable=False)

    # Indexes for common queries
    __table_args__ = (
        Index('idx_published_date', 'published_date'),
        Index('idx_is_processed', 'is_processed'),
        Index('idx_is_embedded', 'is_embedded'),
    )

    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title}', published={self.published_date})>"


class ArticleImage(Base):
    """
    Stores image metadata extracted from articles.

    Images are stored separately to enable image-based search and retrieval.
    The actual image embeddings are stored in Weaviate.
    """

    __tablename__ = "article_images"

    # Primary identifiers
    id = Column(Integer, primary_key=True, autoincrement=True)
    article_url = Column(String(512), nullable=False, index=True)

    # Image metadata
    image_url = Column(String(1024), nullable=False)
    alt_text = Column(Text, nullable=True)
    caption = Column(Text, nullable=True)

    # Image properties
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    file_size = Column(Integer, nullable=True)

    # Position in article
    position_index = Column(Integer, nullable=False)

    # Processing status
    is_embedded = Column(Boolean, default=False, nullable=False)

    # Timestamps
    extracted_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Additional metadata (e.g., download path, processing errors)
    metadata = Column(JSONB, nullable=True)

    __table_args__ = (
        Index('idx_article_images_url', 'article_url'),
        Index('idx_image_embedded', 'is_embedded'),
    )

    def __repr__(self):
        return f"<ArticleImage(id={self.id}, article_url='{self.article_url}', position={self.position_index})>"


class ArticleChunk(Base):
    """
    Stores text chunks created from articles for embedding and retrieval.

    This table maintains the mapping between Weaviate chunks and source articles,
    enabling citation and source attribution.
    """

    __tablename__ = "article_chunks"

    # Primary identifiers
    id = Column(Integer, primary_key=True, autoincrement=True)
    article_url = Column(String(512), nullable=False, index=True)

    # Chunk identifiers
    chunk_id = Column(String(256), unique=True, nullable=False, index=True)
    weaviate_id = Column(String(256), unique=True, nullable=True, index=True)

    # Chunk content
    text_content = Column(Text, nullable=False)

    # Chunk metadata
    chunk_index = Column(Integer, nullable=False)
    chunk_size = Column(Integer, nullable=False)

    # Position in article
    start_position = Column(Integer, nullable=True)
    end_position = Column(Integer, nullable=True)

    # Processing status
    is_embedded = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Additional metadata (e.g., section headers, context)
    metadata = Column(JSONB, nullable=True)

    __table_args__ = (
        Index('idx_chunk_article_url', 'article_url'),
        Index('idx_chunk_embedded', 'is_embedded'),
    )

    def __repr__(self):
        return f"<ArticleChunk(id={self.id}, article_url='{self.article_url}', chunk_index={self.chunk_index})>"


class IngestionLog(Base):
    """
    Logs all ingestion runs for monitoring and debugging.

    Tracks when the RSS feed was synced, what was ingested, and any errors.
    """

    __tablename__ = "ingestion_logs"

    # Primary identifiers
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Run metadata
    run_id = Column(String(256), unique=True, nullable=False, index=True)
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Ingestion statistics
    articles_found = Column(Integer, default=0, nullable=False)
    articles_new = Column(Integer, default=0, nullable=False)
    articles_updated = Column(Integer, default=0, nullable=False)
    articles_failed = Column(Integer, default=0, nullable=False)

    # Status
    status = Column(String(50), nullable=False)  # running, completed, failed, partial

    # Error tracking
    error_message = Column(Text, nullable=True)

    # Additional details
    details = Column(JSONB, nullable=True)

    __table_args__ = (
        Index('idx_run_started_at', 'started_at'),
        Index('idx_run_status', 'status'),
    )

    def __repr__(self):
        return f"<IngestionLog(run_id='{self.run_id}', status='{self.status}', started={self.started_at})>"
