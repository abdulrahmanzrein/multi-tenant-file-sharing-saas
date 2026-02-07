from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# The engine is the connection to your database
# pool_pre_ping=True checks if a connection is still alive before using it
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# SessionLocal is a factory — call SessionLocal() to get a new database session
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
