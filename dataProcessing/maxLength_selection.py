"""
input: 
    reviews_list: a list that contains all reviews from test_set, each review is a dictionary
    tipNum: total number in test_set that should be recognized as tips
"""

def maxLength_selection(reviews_list, tipNum):
    sortedReviews = sorted(reviews_list, key = len(attrgetter('text')))
    