from flask import jsonify
from common.constants import TRANSACTION_ENTERED, DATA_NOT_FOUND
from database.database import db
from models import Transactions, User, StockData
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from celery_config import process_data
from flask_pydantic import validate
from schemas.transaction_schema import TransactionSchema


class TransactionEntry(Resource):
    @validate()
    def post(self, body: TransactionSchema):
        user_id = body.user_id
        ticker_id = body.ticker_id
        transaction_type = body.transaction_type
        transaction_volume = body.transaction_volume
        transaction_price = body.transaction_price
        timestamp = body.timestamp
        data = {
            "user_id": user_id,
            "ticker_id": ticker_id,
            "transaction_type": transaction_type,
            "transaction_volume": transaction_volume,
            "transaction_price": transaction_price,
            "timestamp": timestamp

        }
        process_data.delay(data=data)
        return {"message": "Transaction is Processing"}


class TransactionsDataViewAll(Resource):
    @jwt_required()
    def get(self):
        transactions = db.query(Transactions).all()
        transaction_list = []
        for transaction in transactions:
            transaction_data = {"user_id": transaction.user_id,
                                "ticker_id": transaction.ticker_id,
                                "transaction_type": transaction.transaction_type,
                                "transaction_volume": transaction.transaction_volume,
                                "transaction_price": transaction.transaction_price,
                                "timestamp": transaction.timestamp}
            transaction_list.append(transaction_data)
            return jsonify(transaction_list)
        if not transactions:
            return {"message": DATA_NOT_FOUND}


class TransactionsDataViewSingle(Resource):
    @jwt_required()
    def get(self, user_id=None):
        transaction = db.query(Transactions).filter(Transactions.user_id == user_id).first()
        if transaction:
            return jsonify({"user_id": transaction.user_id,
                            "ticker_id": transaction.ticker_id,
                            "transaction_type": transaction.transaction_type,
                            "transaction_volume": transaction.transaction_volume,
                            "transaction_price": transaction.transaction_price,
                            "timestamp": transaction.timestamp})
        return {"message": DATA_NOT_FOUND}


class TransactionsDataViewDouble(Resource):
    @jwt_required()
    def get(self, user_id=None, start_timestamp=None, end_timestamp=None):
        transaction = db.query(Transactions).filter(
            Transactions.user_id == user_id,
            Transactions.timestamp.between(start_timestamp, end_timestamp)
        ).all()
        if transaction:
            return jsonify({"user_id": transaction.user_id,
                            "ticker_id": transaction.ticker_id,
                            "transaction_type": transaction.transaction_type,
                            "transaction_volume": transaction.transaction_volume,
                            "transaction_price": transaction.transaction_price,
                            "timestamp": transaction.timestamp})
        return {"message": DATA_NOT_FOUND}
