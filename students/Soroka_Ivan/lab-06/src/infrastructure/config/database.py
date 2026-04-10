from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://postgres:admin@localhost:5432/helpdesk_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency для FastAPI (выдает сессию БД на каждый запрос)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()