import pickle

def eval_lda(threshold):
    len_id = 22
    result_lda = {}
    with open("new_test_rst.json") as f:
        for raw in f:
            raw = raw.replace('true', 'True').replace('false', 'False')
            b = eval(raw)
            
            #if high >= b['tip'] and b['tip'] >= low:
            #if 0.7 >= b['tip'] and b['tip'] >= 0.1:
            if b['topic'] >= threshold:
                result_lda[str(b['reviewId']) + str(b['sentencesId'])] = b['topic']
    
    result_j1 = pickle.load( open( "result_combine.p", "rb") )
    sortedSentenceList = pickle.load ( open ( "smallTestSet.p", "rb") )
    #evaluate the result by judger vs result by lda
    truePos = 0
    
    result_reviewPack = {}
    
    for res_id in result_j1:
        if not (res_id[:len_id] in result_reviewPack):
            result_reviewPack[res_id[:len_id]] = 1
            
    Pos = len(result_reviewPack)
    
    print 'all business = ', Pos
    
    Pos_lda = 0
    
    for res_id in result_lda:
        if res_id[:len_id] in result_reviewPack:
            if result_reviewPack[res_id[:len_id]] == 1:
                truePos += 1
            result_reviewPack[res_id[:len_id]] += 1
            
    
    testSetReviewPack = {}
    for sen in sortedSentenceList:
        testSetReviewPack[sen[0]] = 1
    
    for res in result_lda:
        if res[:len_id] in testSetReviewPack:      
            Pos_lda += 1
    
    print 'threshold: ', threshold
    if Pos_lda > 0:
        print "precision = ", str(float(truePos*1.0/Pos_lda) ) 
    else:
        print 'Nothing at all'
    
    print "recall = ", str(float(truePos*1.0/Pos) ) 
    if Pos_lda > 0:
        return (truePos*1.0/Pos_lda, truePos*1.0/Pos)
    else:
        return (0, truePos*1.0/Pos)

highPre = 0
highRec = 0
pre = 0
rec = 0
step = 20
for i in range(step):
    result = eval_lda(i/(step*1.0))
    #result = eval_lda()
    print "================="
    if result[0] > highPre:
        highPre = result[0]
        rec = result[1]
        preT = i/(step*1.0)
    if result[1] > highRec:
        highRec = result[1]
        pre = result[0]
        recT = i/(step*1.0)

print 'highest recall:', recT, ':', pre, highRec
print 'highest precision:', preT, ':', highPre, rec
    
	
