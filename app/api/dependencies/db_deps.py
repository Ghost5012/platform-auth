from typing import Generator

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from app.core.configs import app_config

# Create the SQLAlchemy engine using the database URL from the application configuration.
engine = create_engine(
    app_config.DATABASE_URL,
    # The size of the connection pool.
    pool_size=60,
    # The number of connections that can be opened beyond the pool_size.
    max_overflow=60,
    # The number of seconds to wait before giving up on getting a connection from the pool.
    pool_timeout=30,
    # The number of seconds after which a connection is automatically recycled.
    # This is important to prevent issues with stale connections (e.g., db server restart).
    pool_recycle=3600,
    # Set to True to log all SQL statements issued to the database.
    echo=False, 
)

# Create a configured "Session" class.
# This will be used to create individual database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db()->Generator:
    """
    Dependency function to get a database session.

    This function is used as a dependency in FastAPI routes to provide
    a database session for interacting with the database. It ensures that
    the session is properly closed after use.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()