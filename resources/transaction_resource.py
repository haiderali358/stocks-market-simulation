from flask import jsonify
from common.constants import TRANSACTION_ENTERED, DATA_NOT_FOUND
from database.database import db
from models import Transactions, User, StockData
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from celery_config import process_data


class TransactionEntry(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True)
        parser.add_argument("ticker_id", type=str, required=True)
        parser.add_argument("transaction_type", type=str, required=True)
        parser.add_argument("transaction_volume", type=int, required=True)
        parser.add_argument("transaction_price", type=float, required=True)
        data = parser.parse_args()
        process_data.delay(data)
        return {"message": "Transaction is Processing"}


class TransactionsDataViewAll(Resource):
    @jwt_required()
    def get(self):
        trans = db.query(Transactions).all()
        if trans:
            tran_list = []
            for tran in trans:
                trans_data = {"user_id": tran.user_id,
                              "ticker_id": tran.ticker_id,
                              "transaction_type": tran.transaction_type,
                              "transaction_volume": tran.transaction_volume,
                              "transaction_price": tran.transaction_price,
                              "timestamp": tran.timestamp}
                tran_list.append(trans_data)
            return jsonify(tran_list)
        return {"message": DATA_NOT_FOUND}


class TransactionsDataViewSingle(Resource):
    @jwt_required()
    def get(self, user_id=None):
        trans = db.query(Transactions).filter(Transactions.user_id == user_id).first()
        if trans:
            return jsonify({"user_id": trans.user_id,
                            "ticker_id": trans.ticker_id,
                            "transaction_type": trans.transaction_type,
                            "transaction_volume": trans.transaction_volume,
                            "transaction_price": trans.transaction_price,
                            "timestamp": trans.timestamp})
        return {"message": DATA_NOT_FOUND}


class TransactionsDataViewDouble(Resource):
    @jwt_required()
    def get(self, user_id=None, start_timestamp=None, end_timestamp=None):
        trans = db.query(Transactions).filter(
            Transactions.user_id == user_id,
            Transactions.timestamp.between(start_timestamp, end_timestamp)
        ).all()
        if trans:
            return jsonify({"user_id": trans.user_id,
                            "ticker_id": trans.ticker_id,
                            "transaction_type": trans.transaction_type,
                            "transaction_volume": trans.transaction_volume,
                            "transaction_price": trans.transaction_price,
                            "timestamp": trans.timestamp})

        return {"message": DATA_NOT_FOUND}
