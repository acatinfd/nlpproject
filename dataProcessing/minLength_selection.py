"""
sample call:
    minLength_selection(sentence_list, 30, 20)
    
method: 
    select sentences based on the length of sentence, getting the shortest sentences that are not shorter than "minLen"
    
input: 
    sentence_list: a list that contains all sentences from test_set, each item is a tuple with (review_id, sentence_id, sentence)
    tipNum: total number in test_set that should be recognized as tips
    minLen: minimum length of returned sentences

output:
    return a list of tuples containing (review_id, sentence_id, sentence), the size of the list is "tipNum" (or smaller than that if limited by the size of test_set)
"""

def minLength_selection(sentence_list, tipNum, minLen):
    sortedReviews = sorted(sentence_list, key = lambda p: len(p[2]))
    
    minLengthSentences = []
    k = 0
    total = len(sortedReviews)
    
    while len(minLengthSentences) < tipNum:
        if k >= total:
            break

        while k < total and len(sortedReviews[k][2]) < minLen:
            k += 1
        
        if k < total:
            minLengthSentences.append(sortedReviews[k])
            #print (len(sortedReviews[k][2]), sortedReviews[k][2])
            k += 1
            
    return minLengthSentences


