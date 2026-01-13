from pydantic import BaseModel
from decimal import Decimal

class PriceResponse(BaseModel):
    ticker: str
    price: Decimal
    timestamp: int

    class Config:
        from_attributes = True