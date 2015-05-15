class Settings:
    def __init__(self):
        pass

    DATASET_TRAIN_FILE = 'reviews_data.json'
    MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
    REVIEWS_DATABASE = "Dataset_Challenge_Reviews"
    TAGS_DATABASE = "Tags"
    REVIEWS_COLLECTION = "Reviews"
    CORPUS_COLLECTION = "Corpus"

    TEST_DATABASE = "TESTING_REVIEWS" #TODO
    TEST_RESULT_COLLECTION = "TEST_RESULTS"
