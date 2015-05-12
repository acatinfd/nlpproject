from pymongo import MongoClient
from settings import Settings

client = MongoClient(Settings.MONGO_CONNECTION_STRING)
client.drop_database(Settings.REVIEWS_DATABASE)
client.drop_database(Settings.TAGS_DATABASE)