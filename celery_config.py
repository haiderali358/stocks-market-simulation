from celery import Celery
import time

celery = Celery(
    'celery_app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)


@celery.task
def process_data(data):
    transactions = Transactions(user_id=data['user_id'],
                                ticker_id=data['ticker_id'],
                                transaction_type=data['transaction_type'],
                                transaction_volume=data['transaction_volume'],
                                transaction_price=data['transaction_price'])
    user = db.query(User).filter(User.id == transactions.user_id).first()
    ticker_value = db.query(StockData).filter(StockData.ticker == transactions.ticker_id).first()
    if transactions.transaction_type == "buy":
        if user.balance >= transactions.transaction_price:
            user.balance -= transactions.transaction_price
        else:
            return {"message": NO_BALANCE}, 400
        if ticker_value.volume:
            ticker_value.volume -= trans.transaction_volume
        else:
            return {"message": EMPTY_STOCK}, 400
    elif transactions.transaction_type == "sell":
        user.balance += transactions.transaction_price
        ticker_value.volume += transactions.transaction_volume
    db.add(transactions)
    db.commit()
