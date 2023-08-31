from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime

from models.base_model import BaseModel


class StockData(BaseModel):
    __tablename__ = "stock_data"
    ticker = Column(Integer, unique=True)
    open_price = Column(Float)
    close_price = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
