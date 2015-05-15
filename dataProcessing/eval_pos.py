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
    result_j1 = pickle.load( open( "result_combine2.p", "rb") )
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
    precision = 0
    recall = 0
    
    print 'threshold: ', threshold    
    #if Neg_lda > 0:
    if Pos_lda > 0:
        precision = float(truePos*1.0/Pos_lda)
        print "precision = ", str(precision) 
    else:
        print 'Nothing at all'
    
    #recall = float(trueNeg*1.0/(total - Pos))
    recall = float(truePos*1.0/Pos)
    print "recall = ", str(recall)
    
    F1 = 0
    if not (recall == 0 and precision == 0):
        F1 = precision * recall * 2/(precision + recall)
    
    return (F1, precision, recall)
    
highPre = 0
highRec = 0
pre = 0
rec = 0
step = 10
F = 0.0

for i in range(step):
    result = eval_lda(i/(step*1.0))
    #result = eval_lda()
    print "================="
    F1 = result[0]
    if F < F1:
        highPre = result[1]
        highRec = result[2]
        F = F1
        threshold = i/(step*1.0)
        
print 'highest F:', 'F = ', F, ' precision = ', highPre, 'recall = ' , highRec, ' threshold = ', threshold
    
      
	
