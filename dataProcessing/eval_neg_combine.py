import pickle

def eval_lda(threshold, tipNum):

    result_j1 = pickle.load( open( "result_combine23.p", "rb") )
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
    with open("new_test_rst.json") as f:
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
        if result_lda[res_id] >= threshold or res_id not in result_sim:
            #Pos_lda += 1
            Neg_lda += 1
            #if res_id in result_j1:
            if res_id not in result_j1:            
                #truePos += 1
                trueNeg += 1
    
    #print 'threshold: ', threshold, 'tipNum: ', tipNum
  
    precision = 0
    recall = 0
    
    #if Pos_lda > 0:
    if Neg_lda > 0:
        #precision = float(truePos*1.0/Pos_lda)
        precision = float(trueNeg*1.0/Neg_lda)
        #print "precision = ", str(precision) 
    #else:
        #print 'Nothing at all'
    
    recall = float(trueNeg*1.0/Neg)
    #recall = float(truePos*1.0/Pos)
    #print "recall = ", str(recall)
    
    F1 = 0
    if not (recall == 0 and precision == 0):
        F1 = precision * recall * 2/(precision + recall)
    #print "F1 = ", F1
    return (F1, precision, recall) 

highPre = 0
highRec = 0
pre = 0
rec = 0
step = 20
tipNum = 20
F = 0.0
threhold = -1
tip = 0

i = 0
while i < 500:
    result = eval_lda(0.15, i)
    F1 = result[0]
    if F < F1:
        highPre = result[1]
        highRec = result[2]
        F = F1
        threshold = i
    print ",".join([str(w) for w in result] + [str(i)])
    i += 30    
print 'highest F:', 'F = ', F, ' precision = ', highPre, 'recall = ' , highRec, ' threshold = ', threshold

"""  
for i in range(step):
    for j in range(tipNum):
        if j >= tipNum*0.8:
            continue
        result = eval_lda(i/(step*1.0), j*100)
    
        #print "================="
        F1 = result[0]
        if F < F1:
            highPre = result[1]
            highRec = result[2]
            F = F1
            threshold = i/(step*1.0)
            tip = j*100
        print ",".join([str(w) for w in result] + [str(i/(step*1.0)), str(j*100)])

        
print 'highest F:', 'F = ', F, ' precision = ', highPre, 'recall = ' , highRec, ' threshold = ', threshold, ' tipNum = ', tip

i = 0.0
while i < 0.5:
    i += 0.05
    for j in range(tipNum):
        if j >= tipNum*0.8:
            continue
        result = eval_lda(i/(step*1.0), j*50)
    
        print "================="
        F1 = result[0]
        if F < F1:
            highPre = result[1]
            highRec = result[2]
            F = F1
            threshold = i/(step*1.0)
            tip = j*100
            
print 'highest F:', 'F = ', F, ' precision = ', highPre, 'recall = ' , highRec, ' threshold = ', threshold, ' tipNum = ', tip
"""   
	
