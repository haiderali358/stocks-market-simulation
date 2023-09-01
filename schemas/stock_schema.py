from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StockSchema(BaseModel):
    ticker: int
    open_price: float
    close_price: float
    high: float
    low: float
    volume: int
    timestamp: Optional[datetime]
