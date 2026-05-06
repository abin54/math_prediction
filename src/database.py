from sqlalchemy import create_engine, Column, Integer, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import date
import os
import pandas as pd

# Uses local sqlite file, easy for docker
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/prediction_db.sqlite")
# Ensure directory exists
os.makedirs(os.path.dirname(DATABASE_URL.replace("sqlite:///./", "./")), exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DailyValue(Base):
    __tablename__ = "daily_values"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True, nullable=False)
    value = Column(Float, nullable=False)

# Create table if it doesn't exist
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_historical_df(days: int = 800) -> pd.DataFrame:
    """Pulls the last N days from the database for feature engineering."""
    from sqlalchemy import select
    from datetime import timedelta
    
    db = SessionLocal()
    cutoff_date = date.today() - timedelta(days=days)
    stmt = select(DailyValue).where(DailyValue.date >= cutoff_date).order_by(DailyValue.date)
    results = db.execute(stmt).scalars().all()
    db.close()
    
    if not results:
        return pd.DataFrame(columns=["ds", "value"])
        
    return pd.DataFrame([{"ds": r.date, "value": r.value} for r in results])
