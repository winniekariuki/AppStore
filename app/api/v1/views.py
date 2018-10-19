from flask import make_response, request, jsonify
from flask import Flask
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


products = []
sale_records = []
users = []
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        user_data = None
        if 'access_token' in request.headers:
             token = request.headers['access_token']

        if not token:
            return make_response(jsonify({
                "message": "Login!!"
                }), 401)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            for user in users:
                if user['username'] == data['username']:
                    user_data = user
        except:
            return jsonify({"message": "Invalid Token!"}), 401

        return f(user_data, *args, **kwargs)
    return decorator


class UserAccount(Resource):
    def get(self):
        return make_response(jsonify({
            "Status": "Ok",
            "Message": "Success",
            "UserAccount": users
            }), 200)

    def post(self):
        id = len(users) + 1
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        role = data["role"]

        item = {
                'id': id,
                'username': username,
                'password': password,
                'role': role

        }

        users.append(item)
        return make_response(jsonify({
                    "Status": "Ok",
                    "Message": "Post Success",
                    "UserAccount": users
                }), 201)


