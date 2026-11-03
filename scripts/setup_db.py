"""
Initial database setup script.
Creates the PostgreSQL database if it doesn't exist,
then runs all migrations.

Usage: python scripts/setup_db.py
"""

import subprocess
import sys
import os

def main():
    print("=" * 60)
    print("SiteBlitz Lead Intelligence OS — Database Setup")
    print("=" * 60)

    # Check if PostgreSQL is reachable
    try:
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password="postgres",
            database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Create database if it doesn't exist
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='siteblitz_leads'")
        if not cursor.fetchone():
            print("📦 Creating database 'siteblitz_leads'...")
            cursor.execute("CREATE DATABASE siteblitz_leads")
            print("✅ Database created")
        else:
            print("✅ Database 'siteblitz_leads' already exists")

        cursor.close()
        conn.close()

    except ImportError:
        print("❌ psycopg2 not installed. Run: pip install psycopg2-binary")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to PostgreSQL: {e}")
        print("\nMake sure PostgreSQL is running:")
        print("  Option 1: docker-compose up db -d")
        print("  Option 2: Install PostgreSQL locally")
        sys.exit(1)

    # Run Alembic migrations
    print("\n🔄 Running database migrations...")
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print("✅ Migrations complete")
        print(result.stdout)
    else:
        print("❌ Migration failed:")
        print(result.stderr)
        sys.exit(1)

    print("\n🎉 Database setup complete!")
    print("Start the API: uvicorn backend.app.main:app --reload")

if __name__ == "__main__":
    main()
