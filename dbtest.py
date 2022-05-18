from pymongo import MongoClient
from bson.objectid import ObjectId
connection_string = "mongodb://neko:123@172.16.2.97:27017"
client = MongoClient(connection_string)
collection = client.collection
user_collection = collection.user_connection
product = collection.product

price = product.find_one({"_id": ObjectId("6281fa15e6414aa81e0c7c89")}, {"price"})
print(price["price"])