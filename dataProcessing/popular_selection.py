"""
sample call:
    popular_selection(test_set, 40, 20)
    
method: 
    select sentences based on the popularity of a sentence, getting the top most popular sentences that have the highest score (sum of votes)
    
input: 
    sentence_list: a list that contains all sentences from test_set, each item is a tuple with (review_id, sentence_id, sentence)
    tipNum: total number in test_set that should be recognized as tips
    minLen: minimum length of returned sentences

output:
    return a list of tuples containing (review_id, sentence_id, sentence), the size of the list is "tipNum" (or smaller than that if limited by the size of test_set)
"""
import nltk

def reviewScore(review):
    return review['votes']['funny'] + review['votes']['useful'] + review['votes']['cool']

def popular_selection(test_set, tipNum, minLen):
    scoredReviews = []
    
    for business in test_set:
        for review in business['reviews']:
            sentences = nltk.sent_tokenize(review['text'].lower())
            score = reviewScore(review)
            
            k = 0
            for sentence in sentences:
                scoredReviews.append((review['review_id'], k, score, sentence))
                k += 1
    
    popularTips = []
    sortedReviews = sorted(scoredReviews, key = lambda p: p[2])
    total = len(sortedReviews)
    
    i = 0
    while len(popularTips) < tipNum:
        if i >= total:
            break
            
        sentence = sortedReviews[total - 1 - i]
        
        if len(sentence[3]) >= minLen:
            popularTips.append((sentence[0], sentence[1], sentence[3]) )
            #print (sentence[2], sentence[3])
        
        i += 1
        
    return popularTips

