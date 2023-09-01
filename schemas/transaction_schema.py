from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TransactionSchema(BaseModel):
    user_id: int
    ticker_id: int
    transaction_type: Optional[str]
    transaction_volume: int
    transaction_price: float
    timestamp: Optional[datetime]
