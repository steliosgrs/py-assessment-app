"""
Database connection and utilities for the application.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Get database connection string from environment variables
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "appdb")

# Create SQLAlchemy engine
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# Create a session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Create a base class for declarative models
Base = declarative_base()


def get_db_session():
    """
    Get a database session.

    Returns:
        SQLAlchemy session object
    """
    db = Session()
    try:
        return db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables.
    """
    # Import models here to avoid circular imports
    from shared.models import User

    Base.metadata.create_all(bind=engine)
