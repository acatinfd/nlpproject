import pickle
import math

def currentProcess(last, total):
    if last >= total:
        print "Congratulations! You have finished all the sentences!"
        anw = input('Press any key to leave: ')
        return
    
    percentage = math.ceil(float(last)/total*100)
    print (str(last) + ' sentences! You have finished ' + str(percentage) + '% of all the sentences!')
    
def judge(lastPoint, stopPoint, sortedSentenceList, judger_tips):  
      
    print ('Please finish the following 30 sentences before you take a break.')
    print ('For each sentence, enter \'y\' if it is a tip, enter \'n\' elsewise.')
    
    k = lastPoint
    while k < stopPoint:
        isTip = raw_input((str(k) + ':' + sortedSentenceList[k][2] + '\n'))
        while not (isTip in ['y', 'Y', 'N', 'n']):
            isTip = raw_input('Invalid input. Try again.\n')
        
        
        if isTip in ['Y', 'y']:
            judger_tips.append((sortedSentenceList[k]))
        k += 1
    
    pickle.dump (judger_tips, open ( "judger_tips.p", "wb") )
    pickle.dump (stopPoint, open ( "judgerCheckPoint.p", "wb") )
    
def judger_selection():
    #pre-setup
    sortedSentenceList1 = pickle.load ( open ( "judgerTestSet.p", "rb") )
    sortedSentenceList = sortedSentenceList1[:2000]
    
    total = len(sortedSentenceList)
    if total == 0:
        print ('Error: empty file')
        return
    
    lastPoint = pickle.load( open ("judgerCheckPoint.p", "rb") )
    k = 30
    stopPoint = min(lastPoint + k, total)
    while lastPoint < total:
        judger_tips = pickle.load ( open ( "judger_tips.p", "rb") )
        judge(lastPoint, stopPoint, sortedSentenceList, judger_tips)
        currentProcess(stopPoint, total)
        
        toContinue = raw_input('Continue? enter \'y\' to continue, enter \'n\' elsewise \n')
        while not (toContinue in ['y', 'Y', 'N', 'n']):
            toContinue = raw_input('Invalid input. Try again.\n')
            
        if toContinue in ['Y', 'y']:
            lastPoint = stopPoint
            stopPoint = min(lastPoint + k, total)
        else:
            break

if __name__ == "__main__":
    judger_selection()