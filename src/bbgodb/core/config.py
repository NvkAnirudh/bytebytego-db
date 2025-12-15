"""
Application configuration using Pydantic settings.
"""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Create a .env file in the project root with the following variables:
    - DATABASE_URL=postgresql://user:password@localhost:5432/bbgodb
    - WEAVIATE_URL=http://localhost:8080
    - OPENAI_API_KEY=sk-...
    - RSS_FEED_URL=https://blog.bytebytego.com/feed
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "ByteByteGo DB"
    debug: bool = Field(default=False, description="Enable debug mode")

    # Database
    database_url: str = Field(
        default="postgresql://bbgodb:bbgodb_dev_password@localhost:5432/bbgodb",
        description="PostgreSQL database URL",
    )

    # Weaviate
    weaviate_url: str = Field(
        default="http://localhost:8080",
        description="Weaviate instance URL",
    )
    weaviate_api_key: Optional[str] = Field(
        default=None,
        description="Weaviate API key (if required)",
    )

    # OpenAI
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key for embeddings and generation",
    )
    openai_embedding_model: str = Field(
        default="text-embedding-3-small",
        description="OpenAI embedding model",
    )
    openai_generation_model: str = Field(
        default="gpt-4-turbo-preview",
        description="OpenAI generation model",
    )

    # Anthropic (optional)
    anthropic_api_key: Optional[str] = Field(
        default=None,
        description="Anthropic API key (optional)",
    )

    # RSS Feed
    rss_feed_url: str = Field(
        default="https://blog.bytebytego.com/feed",
        description="ByteByteGo RSS feed URL",
    )

    # Ingestion
    max_articles_per_run: int = Field(
        default=100,
        description="Maximum articles to process per ingestion run",
    )
    chunk_size: int = Field(
        default=1000,
        description="Text chunk size in characters",
    )
    chunk_overlap: int = Field(
        default=200,
        description="Overlap between chunks in characters",
    )

    # Redis (for caching)
    redis_url: Optional[str] = Field(
        default="redis://localhost:6379/0",
        description="Redis URL for caching",
    )

    # LangSmith (for observability)
    langsmith_api_key: Optional[str] = Field(
        default=None,
        description="LangSmith API key for tracing",
    )
    langsmith_project: str = Field(
        default="bbgodb",
        description="LangSmith project name",
    )


# Global settings instance
settings = Settings()
