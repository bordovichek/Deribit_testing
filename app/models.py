from sqlalchemy import Column, Integer, String, Numeric, Index
from .database import Base

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, nullable=False)
    price = Column(Numeric(precision=18, scale=8), nullable=False)
    timestamp = Column(Integer, nullable=False)

    __table_args__ = (
        Index('ix_ticker_timestamp', 'ticker', 'timestamp'),
    )