from pymongo import MongoClient
from settings import Settings

reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TEST_DATABASE][
    Settings.TEST_RESULT_COLLECTION]

reviews_cursor = reviews_collection.find()
reviewsCount = reviews_cursor.count()
reviews_cursor.batch_size(1000)

test_final_rst_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TEST_DATABASE][
    "final"]

def max_elmt(list):
    nonsense = [1, 5, 6, 8, 10, 14, 15, 16, 18, 20, 24, 26, 35, 37, 39]
    prob = 0
    nonsense_idx = 0
    for i in range(50):
        if i not in nonsense:
            prob += list[i]
    return prob


for review in reviews_cursor:
    	test_final_rst_collection.insert({
        	"reviewId": review["reviewId"],
        	"sentencesId": review["sentencesId"],
        	"topic": max_elmt(review["topic"])
    	})
