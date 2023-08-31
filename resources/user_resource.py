import redis
import json
from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import create_access_token, create_refresh_token
from common.constants import USER_REGISTERED, USER_SIGN_IN_FAILED, USER_NOT_FOUND
from database.database import db
from models.user_model import User
from flask import jsonify
from flask_jwt_extended import jwt_required


redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)



def hash_password(password):
    return sha256.hash(password)


def verify_password(password, hashed_password):
    return sha256.verify(password, hashed_password)


plain_password = "mysecretpassword"
hashed_password = hash_password(plain_password)

if verify_password(plain_password, hashed_password):
    print("Password is correct")
else:
    print("Password is incorrect")


class UserSignUp(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        parser.add_argument("balance", type=float, required=True)
        data = parser.parse_args()
        hashed_password = hash_password(data['password'])
        user = User(username=data['username'], password=hashed_password, balance=data['balance'])
        db.add(user)
        db.commit()
        return {"message": USER_REGISTERED}

class UserSignIn(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        data = parser.parse_args()
        user = db.query(User).filter(User.username == data['username']).first()
        if user and verify_password(data['password'], user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
        else:
            return jsonify({'message': USER_SIGN_IN_FAILED}), 401


class UserData(Resource):
    @jwt_required()
    def get(self, username=None):
        cached_data = redis_conn.get(username)
        if cached_data:
            return jsonify(json.loads(cached_data))
        user = db.query(User).filter(User.username == username).first()
        if user:
            user_data = {"id": user.id, "username": user.username, "balance": user.balance}
            redis_conn.setex(username, 3600, json.dumps(user_data))
            return user_data
        return {"message": USER_NOT_FOUND}, 404
