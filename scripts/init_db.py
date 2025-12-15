#!/usr/bin/env python3
"""
Initialize the database schema.

This script creates all necessary tables in PostgreSQL.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from bbgodb.core import init_db, settings


def main():
    """Initialize database tables."""
    print(f"Initializing database at: {settings.database_url}")
    print("Creating tables...")

    try:
        init_db()
        print("Database initialized successfully!")
        print("\nCreated tables:")
        print("  - articles")
        print("  - article_images")
        print("  - article_chunks")
        print("  - ingestion_logs")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
