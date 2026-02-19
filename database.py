# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base # Keeping import but updating usage if needed or just changing import
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

engine = create_engine(settings.DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependência para injetar o DB nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()