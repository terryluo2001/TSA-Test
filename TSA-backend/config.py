"""
Database configuration for the To-Do List API.
Customize these settings based on your MySQL setup.
"""

import os

# MySQL Database Configuration
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '3306')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'todolist_db')

# SQLAlchemy Database URI
# Format: mysql+pymysql://username:password@host:port/database
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Disable SQLAlchemy modification tracking (not needed, saves resources)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# SQLAlchemy Echo (set to True to see SQL queries in console)
SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', 'False').lower() == 'true'
