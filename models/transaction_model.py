from datetime import datetime
from sqlalchemy import String, Column, Integer, Float, DateTime, ForeignKey, Enum

from models.base_model import BaseModel


class Transactions(BaseModel):
    __tablename__ = "transactions"
    user_id = Column(Integer, ForeignKey('user.id'))
    ticker_id = Column(Integer)
    transaction_type = Column(Enum('buy', 'sell', name='transaction_types'))
    transaction_volume = Column(Integer)
    transaction_price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
