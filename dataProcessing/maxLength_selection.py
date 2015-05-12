"""
sample call:
    maxLength_selection(sentence_list, 10)
    
method: 
    select sentences based on the length of sentence, longer is better
    
input: 
    sentence_list: a list that contains all sentences from test_set, each item is a tuple with (review_id, sentence_id, sentence)
    tipNum: total number in test_set that should be recognized as tips

output:
    return a list of tuples containing (review_id, sentence_id, sentence), the size of the list is "tipNum"
"""

def maxLength_selection(sentence_list, tipNum):
    sortedReviews = sorted(sentence_list, key = lambda p: len(p[2]))
    totalLen = len(sortedReviews)
    
    maxLengthSentences = []
    for i in range(tipNum):
        if i < totalLen:
            maxLengthSentences.append(sortedReviews[totalLen - i - 1])
            #print (len(sortedReviews[totalLen - i - 1][2]), sortedReviews[totalLen - i - 1][2])
        i += 1
    
    return maxLengthSentences


    