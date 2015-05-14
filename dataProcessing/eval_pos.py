import pickle

def eval_lda(threshold):

    result_lda = {}
    with open("test_rst1.json") as f:
        for raw in f:
            raw = raw.replace('true', 'True').replace('false', 'False')
            b = eval(raw)
            
            #if high >= b['tip'] and b['tip'] >= low:
            #if 0.7 >= b['tip'] and b['tip'] >= 0.1:
            if b['topic'] >= threshold:
                result_lda[str(b['reviewId']) + str(b['sentencesId'])] = b['topic']

    """
    #version 0.4
    result_lda = {}
    with open("test_rst_0.4.json") as f:
        for raw in f:
            b = eval(raw)
            result_lda[str(b['reviewId']) + str(b['sentencesId'])] = 1
    
    #version 0.4
    """
    result_j1 = pickle.load( open( "result_combine.p", "rb") )
    sortedSentenceList = pickle.load ( open ( "smallTestSet.p", "rb") )
    #evaluate the result by judger vs result by lda
    truePos = 0
    #trueNeg = 0
    Pos = len(result_j1)
    Pos_lda = 0
    
    smallTestSet = {}
    for sen in sortedSentenceList:
        sen_id = str(sen[0]) + str(sen[1])
        smallTestSet[sen_id] = 1
        
    true_result_lda = {}
    for res in result_lda:
        if res in smallTestSet:
            true_result_lda[res] = 1
    
    #Neg_lda = len(true_result_lda)
    Pos_lda = len(true_result_lda)
    
    for res_id in true_result_lda:
        #if not (res_id in result_j1):
        if res_id in result_j1:
            truePos += 1
            #trueNeg += 1
            
    total = 2000
    print 'threshold: ', threshold
    #if Neg_lda > 0:
    if Pos_lda > 0:
        #print "precision = ", str(float(trueNeg*1.0/Neg_lda) ) 
        print "precision = ", str(float(truePos*1.0/Pos_lda) ) 
    else:
        print 'Nothing at all'
    
    #print "recall = ", str(float(trueNeg*1.0/(total - Pos)) ) 
    print "recall = ", str(float(truePos*1.0/Pos) ) 
    if Pos_lda > 0:
    #if Neg_lda > 0:
        return (truePos*1.0/Pos_lda, truePos*1.0/Pos)
        #return (trueNeg*1.0/Neg_lda, trueNeg*1.0/(total - Pos))
    else:
        #return (0, trueNeg*1.0/(total - Pos))
        return (0, truePos*1.0/Pos)

highPre = 0
highRec = 0
pre = 0
rec = 0
step = 10

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
    
	
