import pickle
import nltk
all_business = pickle.load( open( "saveBusiness.p", "rb" ) )

for business in all_business.values():
    for key in business['reviews']:
        review = nltk.sent_tokenize(key['text'].lower())
        
        
        	