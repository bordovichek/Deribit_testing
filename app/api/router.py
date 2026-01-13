from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import PriceHistory
from ..schemas import PriceResponse

router = APIRouter()


@router.get("/all", response_model=List[PriceResponse])
def get_all_prices(ticker: str = Query(..., description="BTC or ETH"), db: Session = Depends(get_db)):
    return db.query(PriceHistory).filter(PriceHistory.ticker == ticker.upper()).all()


@router.get("/latest", response_model=PriceResponse)
def get_latest_price(ticker: str = Query(..., description="BTC or ETH"), db: Session = Depends(get_db)):
    result = db.query(PriceHistory).filter(PriceHistory.ticker == ticker.upper()) \
        .order_by(PriceHistory.timestamp.desc()).first()
    if not result:
        raise HTTPException(status_code=404, detail="Data not found")
    return result


@router.get("/filter", response_model=List[PriceResponse])
def get_prices_by_date(
        ticker: str = Query(..., description="BTC or ETH"),
        start_ts: int = Query(..., description="Start UNIX timestamp"),
        end_ts: int = Query(..., description="End UNIX timestamp"),
        db: Session = Depends(get_db)
):
    return db.query(PriceHistory).filter(
        PriceHistory.ticker == ticker.upper(),
        PriceHistory.timestamp >= start_ts,
        PriceHistory.timestamp <= end_ts
    ).all()
