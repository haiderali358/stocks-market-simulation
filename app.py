from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from redis import Redis
from flask_caching import Cache
from resources.transaction_resource import (
    TransactionEntry,
    TransactionsDataViewAll,
    TransactionsDataViewSingle,
    TransactionsDataViewDouble
)
from resources.user_resource import (
    UserSignUp,
    UserSignIn,
    UserData
)
from resources.stock_resource import (
    StockEntry,
    StockDataViewAll,
    StockDataSingle
)


app = Flask(__name__)
api = Api(app)
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'  # Replace with your Redis server details
cache = Cache(app)
redis_conn = Redis(host='localhost', port=6379, db=0)
app.config['JWT_SECRET_KEY'] = 'abc123'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=600)

jwt = JWTManager(app)


api.add_resource(UserSignUp, "/user/sign_up")
api.add_resource(UserSignIn, "/user/sign_in")
api.add_resource(UserData, "/user/<string:username>")
api.add_resource(StockEntry, "/stock/data")
api.add_resource(StockDataViewAll,"/stock/data/view")
api.add_resource(StockDataSingle,"/stock/data/view/<int:ticker>")
api.add_resource(TransactionEntry, "/transaction/")
api.add_resource(TransactionsDataViewAll, "/transaction/data/view")
api.add_resource(TransactionsDataViewSingle,"/transaction/data/view/<int:user_id>")
api.add_resource(TransactionsDataViewDouble, "/transaction/data/view/<int:user_id>/<string:start_timestamp>/<string:end_timestamp>")

if __name__ == "__main__":
    app.run(debug=True)
