import pickle

def eval_lda(low, high):
    result_lda = {}
    with open("test_rst_2.json") as f:
        for raw in f:
            raw = raw.replace('true', 'True').replace('false', 'False')
            b = eval(raw)
            
            #if high >= b['tip'] and b['tip'] >= low:
            if 0.7 >= b['tip'] and b['tip'] >= 0.1:
                result_lda[str(b['reviewId']) + str(b['sentencesId'])] = b['tip']
    
    result_j1 = pickle.load( open( "judger_tips_x.p", "rb") )
    sortedSentenceList = pickle.load ( open ( "smallTestSet.p", "rb") )
    #evaluate the result by judger vs result by lda
    truePos = 0
    Pos = len(result_j1)
    Pos_lda = 0
    
    for res in result_j1:
        res_id = str(res[0]) + str(res[1])
        if res_id in result_lda:
            truePos += 1
            
    for sen in sortedSentenceList:
        sen_id = str(sen[0]) + str(sen[1])
        if sen_id in result_lda:
            Pos_lda += 1
    
    print 'threshold: ', low, high
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
step = 10
for i in range(step):
    result = eval_lda(i/(step*1.0), (i + 1)/(step*1.0))
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
print 'highest precision:', preT, ':', rec, highPre
    
	
