import pickle

def eval_sim(tipNum):

    result_sim = {}
    
    count = 0
    result_sim_list = pickle.load(open('simResultSorted.p', 'rb'))
    for item in result_sim_list:
            if count < tipNum:
                count += 1
                result_sim[str(item[0]) + str(item[1])] = item[3]

    print "result_sim: ", len(result_sim)
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
    #sortedSentenceList = pickle.load ( open ( "smallTestSet.p", "rb") )
    #evaluate the result by judger vs result by lda
    truePos = 0
    #trueNeg = 0
    Pos = len(result_j1)
    Pos_lda = 0
        
    #Neg_lda = len(true_result_lda)
    Pos_lda = len(result_sim)
    
    for res_id in result_sim:
        #if not (res_id in result_j1):
        if res_id in result_j1:
            truePos += 1
            #trueNeg += 1
    
    total = 2000
    precision = 0
    recall = 0
    
    print 'tipNum: ', tipNum
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
    total = 2000

highPre = 0
highRec = 0
pre = 0
rec = 0
tipNum = 20
F = 0.0
tip = 0

for i in range(tipNum):
    result = eval_sim(i*100)
    #result = eval_lda()
    print "================="
    F1 = result[0]
    if F < F1:
        highPre = result[1]
        highRec = result[2]
        F = F1
        tip = i*100
        
print 'highest F:', 'F = ', F, ' precision = ', highPre, 'recall = ' , highRec, ' tipNum = ', tip