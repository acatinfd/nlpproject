import pickle

def eval_lda(threshold, tipNum):

    result_j1 = pickle.load( open( "result_combine.p", "rb") )
    sortedSentenceList = pickle.load ( open ( "smallTestSet.p", "rb") )
    #evaluate the result by judger vs result by lda and similarity
    #truePos = 0
    trueNeg = 0
    Pos = len(result_j1)
    total = 2000
    Neg = total - Pos
    
    #get testSet full set
    smallTestSet = {}
    for sen in sortedSentenceList:
        sen_id = str(sen[0]) + str(sen[1])
        smallTestSet[sen_id] = 1
    result_sim = {}
    
    #get result_sim full set
    count = 0
    result_sim_list = pickle.load(open('simResultSorted.p', 'rb'))
    for item in result_sim_list:
            if count < tipNum:
                count += 1
                result_sim[str(item[0]) + str(item[1])] = item[3]
    
    #get result_lda full set            
    result_lda = {}
    with open("test_rst1.json") as f:
        for raw in f:
            raw = raw.replace('true', 'True').replace('false', 'False')
            b = eval(raw)
            b_id = str(b['reviewId']) + str(b['sentencesId'])
            
            if b_id in smallTestSet:
                result_lda[b_id] = b['topic']
    
    
    #Pos_lda = len(result_lda)
    #Pos_lda = 0
    Neg_lda = 0
    for res_id in result_lda:
        #if result_lda[res_id] <= threshold and res_id in result_sim:
        if result_lda[res_id] <= threshold and res_id not in result_sim:
            #Pos_lda += 1
            Neg_lda += 1
            #if res_id in result_j1:
            if res_id not in result_j1:            
                #truePos += 1
                trueNeg += 1
    
    print 'threshold: ', threshold, 'tipNum: ', tipNum
  
    precision = 0
    recall = 0
    
    #if Pos_lda > 0:
    if Neg_lda > 0:
        #precision = float(truePos*1.0/Pos_lda)
        precision = float(trueNeg*1.0/Neg_lda)
        print "precision = ", str(precision) 
    else:
        print 'Nothing at all'
    
    recall = float(trueNeg*1.0/Neg)
    #recall = float(truePos*1.0/Pos)
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
    
    
	
