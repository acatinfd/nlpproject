"""
sample call:
    random_selection(sentence_list, 10)
    
method: 
    randomly select sentences 
    
input: 
    sentence_list: a list that contains all sentences from test_set, each item is a tuple with (review_id, sentence_id, sentence)
    tipNum: total number in test_set that should be recognized as tips

output:
    return a list of tuples containing (review_id, sentence_id, sentence), the size of the list is "tipNum" (or smaller than that if limited by the size of test_set)
"""

import random
def random_selection(sentence_list, tipNum):
    total = min(len(sentence_list), tipNum)
    
    return random.sample(sentence_list, total)

