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
class LoginUsers(Resource):
    def post(self):
        # print(users)
        data = request.get_json()
        username = data["username"]
        password = data["password"]


        if not data or not username or not password:
            return make_response(jsonify({
                                         'Status': 'Failed',
                                         'Message': "Login!!"
                                         }), 400)

        for user in users:
            if user['username'] == username and user['password'] == password:
                token = jwt.encode({'username': user['username'],
                                    'exp': datetime.datetime.utcnow() +
                                    datetime.timedelta(minutes=30)},
                                    app.config['SECRET_KEY'])
                return make_response(jsonify({
                                             'token': token.decode('UTF-8')
                                             }), 200)

        return make_response(jsonify({
                'Status': 'Failed',
                'Message': "No such user found"
                }), 404)
class Products(Resource):
    @token_required
    def post(user_data,self):
        if user_data == "Admin":
           return make_response(jsonify({
                "message":"Not authorized"
                }) ,401)

        id = len(products) + 1
        data = request.get_json()
        name = data["name"]
        model_no = data["model_no"]
        price = data["price"]

        item = {
                'id': id,
                'name': name,
                'model_no': model_no,
                'price': price
        }

        products.append(item)
        return make_response(jsonify({
                    "Status": "Ok",
                    "Message": "Post Success",
                    "MyProducts": products
                }), 201)
    def get(self):
        return make_response(jsonify({

            "Status": "Ok",
            "Message": "Success",
            "MyProducts": products

            }), 200) 
class SingleProduct(Resource):
        def get(self, productID):

            for product in products:
                if product["id"] == int(productID):
                    return make_response(jsonify({
                        "Status": "Ok",
                        "Message": "Success",
                        "MyProducts": product

                        }), 200)                     
class SaleRecords(Resource):
        @token_required   
        def post(user_data,self):

        if user_data["role"] != "storeattendant":
           return make_response(jsonify({
                "message":"Not authorized"
                }) ,401)       
        data=request.get_json()
        for product in products:
            if product['id'] == data["id"]:
                sale = {
                        'sale_id':len(sale_records)+1,
                        'sale':product,
                        'StoreAttendant_id':user_data["id"]
                        
                        }
                sale_records.append(sale)
            return make_response(jsonify({
                                    "Status":"Created",
                                    "Message":"Post Success",
                                    "MySaleRecords":sale_records
                                }),201)