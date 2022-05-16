from hashlib import new
from urllib import response
from pymongo import MongoClient
from flask import Flask, request, Response, jsonify
from bson import json_util
from bson.objectid import ObjectId
import pprint

app = Flask(__name__)

connection_string = f"mongodb://neko:123@172.16.2.97:27017"
client = MongoClient(connection_string)


collection = client.collection
user_collection = collection.user_connection
product = collection.product

#register with a new account
#check exist username and email, if not, account can create



@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    check_user = user_collection.find_one({'username': username})
    check_email = user_collection.find_one({'email': email})

    if not ( check_user or check_email) and password:
        user_collection.insert({'username': username, 'password': password,'email': email})
        response = jsonify(message='Your account have been create success!')
        response.status_code = 201
        return response
    else:
        return not_found()
    
#login, check the username and the password

@app.route('/login', methods=['GET'])
def login():
    username = request.json['username']
    password = request.json['password']

    check_user = {"$and": [
        {"username": {"$eq": username}},
        {"password": {"$eq": password}}
    ]}

    if check_user:
        response = jsonify(message='Login sucesss!')
        return response
    else:
        not_found()


#verify email
@app.route('/verifyemail', methods=['GET'])
def verifyemail():
    email = request.json['email']
    check_email = user_collection.find_one({'email': email})

    if check_email:
        response = jsonify(message='A verify email has been sent to your email address!')
        response.status_code = 200
        return response
    else:
        not_found()


@app.route('/login/product', methods=['POST'])
def createProduct():
    productName = request.json['name_product']
    productPrice = request.json['price']
    productQuantity = request.json['quantity']
    productDescription = request.json['description']

    check_production_name = product.find_one({'name_product': productName})
    if not check_production_name and productPrice and productQuantity and productDescription:
        product.insert({'name_product': productName, 'price': productPrice, 'quantity': productQuantity, 'description': productDescription})
        response = jsonify(message='Create product successful')
        response.status_code = 201
        return response
    else:
        not_found()


@app.route('/login/product/quantity', methods=['GET'])
def showQuantityAllProdcut():
    quantity = product.find({})
    response = json_util.dumps(quantity)
    return Response(response, mimetype="application/json")
    
@app.route('/login/product/update', methods=['PUT'])
def updateProduct():
    oldNameProduct = request.json({"name_product"})
    newNameProduct = request.json({"name_product"})
    productPrice = request.json("price")
    productQuantity = request.json("quantity")
    productDescription = request.json("description")
    checkProduct = product.find_one({"name_product": oldNameProduct})
    if checkProduct:
        
    else:
        not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource not found' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

