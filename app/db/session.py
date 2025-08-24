from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import make_url

from app.core.config import settings

# Configure engine with appropriate SSL settings for Neon PostgreSQL
connect_args = {}
url = settings.SQLALCHEMY_DATABASE_URI

# If using Neon PostgreSQL, ensure SSL settings are properly configured
if 'neon.tech' in str(url):
    connect_args = {
        "sslmode": "require",
        "connect_timeout": 10
    }

engine = create_engine(
    url, 
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=300,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
