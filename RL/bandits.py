#import sys;args = sys.argv[1:]
# Tianhao Chen, pd.4
import math
arms = {}
def argmax(arms, testNum):
    avgs = []
    for i in arms:
        avg = arms[i][0]/arms[i][1]
       # print(testNum)
        #ucb = avg + math.sqrt(2*math.log(testNum)/arms[i][1])
        avgs.append(avg)
   # print(avgs)
    #print(avgs)

    return avgs.index(max(avgs))
def bandit(testNum, armIdx, pullVal):
    global arms
  # Bandit pull maximizer; if testNum ...
    if testNum == 0: 
        arms = {i: [4,1] for i in range(armIdx)}
       # return 0
    elif testNum > 0:
        arms[armIdx] = [arms[armIdx][0]+pullVal, arms[armIdx][1]+1]
    arm = argmax(arms, testNum)
    #print(arm)
    return arm
    
# bandit(0,10,0)
# bandit(1, 0,10)
# bandit(1,2,20)
  # ==0 => new bandit initialization; armIdx contains the
  #         number of arms (10); pullVal not used
  # > 0 => testNum contains the pull number (from 1 to 999)
  #        armIdx has the index of the arm that was requested
  #            to be pulled in the prior call
  #        pullVal has the value that resulted from the pull
  # The return val is always the idx of the next
  #     arm to pull in [0,# of arms)
# Tianhao Chen, pd. 4, 2023