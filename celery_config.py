from celery import Celery
# from app import app
import time

celery = Celery(
    'celery_app',
    broker='redis://localhost:6379/0',  # Replace with your Redis URL
    backend='redis://localhost:6379/0',  # Replace with your Redis URL
)

# Optional: Load Celery configuration from Flask app's config
# celery.conf.update(app.config)

@celery.task
def process_data(data):
    trans = Transactions(user_id=data['user_id'],
                         ticker_id=data['ticker_id'],
                         transaction_type=data['transaction_type'],
                         transaction_volume=data['transaction_volume'],
                         transaction_price=data['transaction_price'])
    user = db.query(User).filter(User.id == trans.user_id).first()
    tic = db.query(StockData).filter(StockData.ticker == trans.ticker_id).first()
    if trans.transaction_type == "buy":
        if user.balance >= trans.transaction_price:
            user.balance -= trans.transaction_price
        else:
            return {"message": "Insufficient balance for buying"}, 400
        if tic.volume is not None:
            tic.volume -= trans.transaction_volume
        else:
            return {"message": "Stock is not available"}, 400
    elif trans.transaction_type == "sell":
        user.balance += trans.transaction_price
        tic.volume += trans.transaction_volume
    result = process_data.delay(trans)
    db.add(trans)
    db.commit()
