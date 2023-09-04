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
from schemas.user_schema import UserSignUpSchema, UserSignInSchema, UserDataViewSchema
from flask_pydantic import validate


redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


def hash_password(password):
    return sha256.hash(password)


def verify_password(password, hashed_password):
    return sha256.verify(password, hashed_password)


class UserSignUp(Resource):
    @validate()
    def post(self, body: UserSignUpSchema):
        username = body.username
        password = body.password
        balance = body.balance
        hashed_password = hash_password(password)
        user = User(username=username, password=hashed_password, balance=balance)
        db.add(user)
        db.commit()
        return {"message": USER_REGISTERED}


class UserSignIn(Resource):
    @validate()
    def post(self, body: UserSignInSchema):
        username = body.username
        password = body.password
        balance = body.balance
        user = db.query(User).filter(User.username == username).first()
        if user and verify_password(password, user.password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
        return jsonify({'message': USER_SIGN_IN_FAILED}), 401


class UserData(Resource):
    @jwt_required()
    def get(self, username):
        cached_data = redis_conn.get(username)
        if cached_data:
            return jsonify(json.loads(cached_data))
        user = db.query(User).filter(User.username == username).first()
        if user:
            user_data = {"id": user.id, "username": user.username, "balance": user.balance}
            redis_conn.setex(username, 3600, json.dumps(user_data))
            return user_data
        return {"message": USER_NOT_FOUND}, 404
