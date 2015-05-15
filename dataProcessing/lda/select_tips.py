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
    nonsense = [0]
    prob = 0
    nonsense_idx = 0
    for i in range(50):
        if nonsense[nonsense_idx] == i:
            prob += list[i]
            if nonsense_idx + 1 < len(nonsense):
                nonsense_idx = nonsense_idx + 1
    return prob


for review in reviews_cursor:
    	test_final_rst_collection.insert({
        	"reviewId": review["reviewId"],
        	"sentencesId": review["sentencesId"],
        	"topic": max_elmt(review["topic"])
    	})
