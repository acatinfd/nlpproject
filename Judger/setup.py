import pickle
checkPoint = 0
pickle.dump (checkPoint, open ( "judgerCheckPoint.p", "wb") )

judger_tips = []
pickle.dump (judger_tips, open ( "judger_tips.p", "wb") )
