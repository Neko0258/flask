from pymongo import MongoClient

connection_string = "mongodb://neko:123@172.16.2.97:27017"
client = MongoClient(connection_string)
collection = client.collection
user_collection = collection.user_connection


people = user_collection.remove()
for person in people:
    print(str("done"))

