import asyncio
import time
from .worker import celery_app
from .services.deribit import DeribitClient
from .database import SessionLocal
from .models import PriceHistory


@celery_app.task(name="app.tasks.collect_prices")
def collect_prices():
    from .database import engine
    PriceHistory.metadata.create_all(bind=engine)
    client = DeribitClient()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    tickers = ["BTC", "ETH"]
    db = SessionLocal()

    try:
        for ticker in tickers:
            price = loop.run_until_complete(client.fetch_price(ticker))

            if price is not None:
                new_entry = PriceHistory(
                    ticker=ticker.upper(),
                    price=price,
                    timestamp=int(time.time())
                )
                db.add(new_entry)

        db.commit()
    except Exception as e:
        print(f"Error collecting prices: {e}")
        db.rollback()
    finally:
        db.close()
        loop.close()