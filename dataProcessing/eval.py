import pickle

def eval_lda(threshold, tipNum):

    result_j1 = pickle.load( open( "result_combine2.p", "rb") )
    sortedSentenceList = pickle.load ( open ( "smallTestSet.p", "rb") )
    #evaluate the result by judger vs result by lda and similarity
    truePos = 0
    Pos = len(result_j1)
    
    smallTestSet = {}
    for sen in sortedSentenceList:
        sen_id = str(sen[0]) + str(sen[1])
        smallTestSet[sen_id] = 1
    result_sim = {}
    
    count = 0
    result_sim_list = pickle.load(open('simResultSorted.p', 'rb'))
    for item in result_sim_list:
            if count < tipNum:
                count += 1
                result_sim[str(item[0]) + str(item[1])] = item[3]
                
    result_lda = {}
    with open("new_test_rst.json") as f:
        for raw in f:
            raw = raw.replace('true', 'True').replace('false', 'False')
            b = eval(raw)
            b_id = str(b['reviewId']) + str(b['sentencesId'])
            
            if b_id in smallTestSet and (b['topic'] <= threshold or b_id not in result_sim):
                result_lda[b_id] = b['topic']
    
    Pos_lda = len(result_lda)
    
    for res_id in result_lda:
        if res_id in result_j1:
            #truePos += 1
            truePos += 1
    
    print 'threshold: ', threshold, 'tipNum: ', tipNum
  
    precision = 0
    recall = 0
    
    if Pos_lda > 0:
        precision = float(truePos*1.0/Pos_lda)
        print "precision = ", str(precision) 
    else:
        print 'Nothing at all'
    
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
tipNum = 10
F = 0.0
threhold = -1
tip = 0

for i in range(step):
    for j in range(tipNum):
        result = eval_lda(i/(step*1.0), j*100)
    
        print "================="
        F1 = result[0]
        if F < F1:
            highPre = result[1]
            highRec = result[2]
            F = F1
            threshold = i/(step*1.0)
            tip = j*100
            
print 'highest F:', 'F = ', F, ' precision = ', highPre, 'recall = ' , highRec, ' threshold = ', threshold, ' tipNum = ', tip
    
    
	
