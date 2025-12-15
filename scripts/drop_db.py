#!/usr/bin/env python3
"""
Drop all database tables.

WARNING: This will delete all data!
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from bbgodb.core import drop_db, settings


def main():
    """Drop all database tables."""
    print(f"WARNING: This will drop all tables in: {settings.database_url}")
    response = input("Are you sure you want to continue? (yes/no): ")

    if response.lower() != "yes":
        print("Aborted.")
        sys.exit(0)

    print("Dropping all tables...")

    try:
        drop_db()
        print("All tables dropped successfully!")
    except Exception as e:
        print(f"Error dropping tables: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
