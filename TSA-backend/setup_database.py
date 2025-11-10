"""
Database setup script for the To-Do List API.
This script creates the database and tables if they don't exist.
"""

import pymysql
import sys
import config

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host=config.DB_HOST,
            port=int(config.DB_PORT),
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )

        cursor = connection.cursor()

        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME}")
        print(f"✓ Database '{config.DB_NAME}' created successfully (or already exists)")

        # Use the database
        cursor.execute(f"USE {config.DB_NAME}")

        cursor.close()
        connection.close()

        return True

    except pymysql.Error as e:
        print(f"✗ Error creating database: {e}")
        return False


def create_tables():
    """Create tables using SQLAlchemy"""
    try:
        from app import app, db

        with app.app_context():
            db.create_all()
            print("✓ Tables created successfully")

        return True

    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False


def verify_setup():
    """Verify the database setup"""
    try:
        connection = pymysql.connect(
            host=config.DB_HOST,
            port=int(config.DB_PORT),
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )

        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print("\n✓ Database verification successful!")
        print(f"  Database: {config.DB_NAME}")
        print(f"  Tables: {', '.join([table[0] for table in tables])}")

        cursor.close()
        connection.close()

        return True

    except pymysql.Error as e:
        print(f"✗ Error verifying setup: {e}")
        return False


def main():
    """Main setup function"""
    print("=" * 60)
    print("To-Do List API - Database Setup")
    print("=" * 60)
    print(f"\nDatabase Configuration:")
    print(f"  Host: {config.DB_HOST}")
    print(f"  Port: {config.DB_PORT}")
    print(f"  User: {config.DB_USER}")
    print(f"  Database: {config.DB_NAME}")
    print("\n" + "=" * 60)

    # Step 1: Create database
    print("\n[Step 1/3] Creating database...")
    if not create_database():
        print("\n✗ Setup failed at database creation")
        sys.exit(1)

    # Step 2: Create tables
    print("\n[Step 2/3] Creating tables...")
    if not create_tables():
        print("\n✗ Setup failed at table creation")
        sys.exit(1)

    # Step 3: Verify setup
    print("\n[Step 3/3] Verifying setup...")
    if not verify_setup():
        print("\n✗ Setup verification failed")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("✓ Database setup completed successfully!")
    print("=" * 60)
    print("\nYou can now run the application:")
    print("  python app.py")
    print("\n")


if __name__ == "__main__":
    main()
