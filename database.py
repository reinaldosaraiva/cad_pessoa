from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)