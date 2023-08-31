import json
from datetime import datetime
from flask import jsonify
from common.constants import DATA_ENTERED, DATA_NOT_FOUND
from database.database import db
from models.stock_data_model import StockData
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
import redis

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


class StockEntry(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("ticker", type=int, required=True)
        parser.add_argument("open_price", type=float, required=True)
        parser.add_argument("close_price", type=float, required=True)
        parser.add_argument("high", type=float, required=True)
        parser.add_argument("low", type=float, required=True)
        parser.add_argument("volume", type=int, required=True)
        parser.add_argument("timestamp", type=datetime, required=False)
        data = parser.parse_args()
        print(data)
        stock = StockData(ticker=data['ticker'], open_price=data['open_price'], close_price=data['close_price'],
                          high=data['high'], low=data['low'], volume=data['volume'])
        db.add(stock)
        db.commit()
        return {"message": DATA_ENTERED}


class StockDataViewAll(Resource):
    @jwt_required()
    def get(self):
        cached_data = redis_conn.get('stock_data_cache')
        if cached_data:
            return jsonify(json.loads(cached_data))

        stocks = db.query(StockData).all()
        if stocks:
            stock_list = []
            for stock in stocks:
                stock_data = {
                    "ticker": stock.ticker,
                    "open_price": stock.open_price,
                    "close_price": stock.close_price,
                    "high": stock.high,
                    "low": stock.low,
                    "volume": stock.volume,
                    "timestamp": str(stock.timestamp)
                }
                stock_list.append(stock_data)

            # Cache stock data in Redis
            redis_conn.setex('stock_data_cache', 3600, json.dumps(stock_list))

            return jsonify(stock_list)

        return {"message": DATA_NOT_FOUND}


class StockDataSingle(Resource):
    @jwt_required()
    def get(self, ticker=None):
        cached_data = redis_conn.get(ticker)
        if cached_data:
            return jsonify(json.loads(cached_data))
        stock = db.query(StockData).filter(StockData.ticker==ticker).first()
        if stock:
            return jsonify({"ticker": stock.ticker,"open_price": stock.open_price, "close_price": stock.close_price,
                               "high": stock.high, "low": stock.low, "volume": stock.volume, "timestamp": stock.timestamp})
        redis_conn.setex(ticker, 3600, json.dumps(stock))
        return {"message": DATA_NOT_FOUND}

