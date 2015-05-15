from pymongo import MongoClient
db = MongoClient("mongodb://localhost:27017/")["TESTING_REVIEWS"]
db.final.drop()