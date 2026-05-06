from sqlalchemy import create_engine, Column, Integer, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import date, timedelta
import pandas as pd
from sqlalchemy import select
from src.config import settings
import os

# Ensure the data directory exists for the sqlite file
data_dir = os.path.dirname(settings.database_url.replace("sqlite:///./", "./"))
if data_dir and data_dir != ".":
    os.makedirs(data_dir, exist_ok=True)

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DailyValue(Base):
    __tablename__ = "daily_values"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True, nullable=False)
    value = Column(Float, nullable=False)

Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_historical_df(days: int = 1000) -> pd.DataFrame:
    db = SessionLocal()
    cutoff_date = date.today() - timedelta(days=days)
    stmt = select(DailyValue).where(DailyValue.date >= cutoff_date).order_by(DailyValue.date)
    results = db.execute(stmt).scalars().all()
    db.close()
    if not results:
        return pd.DataFrame(columns=["ds", "value"])
    return pd.DataFrame([{"ds": r.date, "value": r.value} for r in results])
