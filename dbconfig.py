from itsdangerous import json
from pymongo import MongoClient
from flask import Flask, request, Response, jsonify
from bson import json_util
from bson.objectid import ObjectId
from flask_swagger_ui import get_swaggerui_blueprint



app = Flask(__name__)

#connection_string = f"mongodb://neko:123@172.16.2.97:27017"
connection_string = f"mongodb://neko:123@192.168.32.114:27017"
client = MongoClient(connection_string)


collection = client.collection
user_collection = collection.user_connection
product = collection.product


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app-name': "RESTFUL API PYTHON MONGODB"
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)


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

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    """
    check_user = {"$and": [
        {"username": {"$eq": username}},
        {"password": {"$eq": password}}
    ]}
"""
    check_user = user_collection.find({'username': username, "password": password})
    response_2 = json_util.dumps(check_user)
    if response_2:
    #    response = jsonify(message='Login sucesss!')
     #   response.status_code = 200
        return Response(response_2, mimetype="application/json")
    else:
        return not_found()

   # return Response(response, mimetype="application/json")

#verify email
@app.route('/verifyemail', methods=['GET'])
def verifyemail():
    email = request.args.get("email")
    check_email = user_collection.find({'email': email})
    response = json_util.dumps(check_email)
    """
    if check_email:
        response = jsonify(message='A verify email has been sent to your email address!')
        response.status_code = 200
        return response
    else:
        return not_found()
        """
    return Response(response, mimetype="application/json")


@app.route('/product', methods=['POST'])
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
        return not_found()


@app.route('/product/quantity', methods=['GET'])
def showQuantityAllProdcut():
    quantity = product.find({})
    response = json_util.dumps(quantity)
    return Response(response, mimetype="application/json")
    
@app.route('/product/update/<id>', methods=['PUT'])
def updateProduct(id):
    checkProductID = product.find_one({"_id": ObjectId(id)})
    productName = request.json["name_product"]
    productPrice = request.json["price"]
    productQuantity = request.json["quantity"]
    productDescription = request.json["description"]
    if checkProductID:
        product.update_one({'_id': ObjectId(id)}, {'$set': {'name_product': productName, 'price': productPrice, 'quantity': productQuantity, 'description': productDescription}})
        response = jsonify(message='User ' + id + ' Update successfully')
        response.status_code = 200
        return response
    else:
        return not_found()

@app.route('/product/delete/<id>', methods=['DELETE'])
def deleteProduct(id):
    checkProductID = product.find_one({"_id": ObjectId(id)})
    if checkProductID:
        product.delete_one({'_id': ObjectId(id)})
        response = jsonify(message='User ' + id + ' has been deleted!')
        return response
    else:
        return not_found()
"""
@app.route('/order/<id>', methods=['POST', 'GET'])
def order(id):
    checkProductID = product.find_one({"_id": ObjectId(id)}) #just for checking data
    cursor = 
    
    
    if checkProductID:
        product.update_one({'_id': ObjectId}, {'$set': {"quantity": afterBuy}})
        response = jsonify(message='order success!')
        response.status_code = 201
        return response
    else:
        not_found()
"""
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource not found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

