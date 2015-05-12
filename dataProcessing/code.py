import pickle

#get business
all_business = {}
with open("yelp_academic_dataset_business.json") as f:
    for raw in f:
        raw = raw.replace('true', 'True').replace('false', 'False')
        b = eval(raw)
        if 'Restaurants' in b['categories']:
            all_business[b['business_id']] = b
            all_business[b['business_id']]['tips'] = []
            all_business[b['business_id']]['reviews'] = []
len(all_business)

#get tips for business
with open("yelp_academic_dataset_tip.json") as f:
    count = 0
    for data in f:
        data = data.replace('\n','')
        t = eval(data)
        if t['business_id'] in all_business:
            count = count + 1
            tip = t['text']
            all_business[t['business_id']]['tips'].append(tip)
count    

#get reviews for business
with open("yelp_academic_dataset_review.json") as f:
    reviewCount = 0
    for data in f:
        data = data.replace('\n','')
        review = eval(data)
        if review['business_id'] in all_business:
            reviewCount = reviewCount + 1
            all_business[review['business_id']]['reviews'].append(review)
reviewCount

#save data
pickle.dump( all_business, open( "saveBusiness.p", "wb") )

"""
How to load data:
----------------
import pickle
all_business = pickle.load( open( "saveBusiness.p", "rb" ) )

-------How to get reviews from all_business---------
for business in all_business.values():
    for key in business['reviews']:
        review = key['text']
----------------------------------

********************Test Set*************************
----------load test set----------------
import pickle
test_set = pickle.load( open( "saveReviewTestSet.p", "rb" ) )

----------get review from test set--------------
for business in test_set:
    for review in business['reviews']:
        review_id = review['review_id']
        business_id = review['business_id']
        review_sentences = review['text']

***************** get Rated Reviews (1 star or 5 stars) *******************
----------load data----------------
import pickle
ratedReviews = pickle.load( open( "saveRatedReviews.p", "rb" ) )

----------count 1 star reviews --------------
count = 0
for key in ratedReviews:
    if ratedReviews[key] == 1:
        count += 1

print ("1 stars: ", count)

"""