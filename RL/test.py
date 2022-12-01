from numpy.random import normal; from bandits import *

def tester():
    res = []
    for i in range(1000): #change to 1000
        #bandits = [1.1071544640292001, 0.468551827636032, -0.01004318502824047, -0.10019229749786938, -0.8742857162807697, -0.88739592858834, 0.32881541924439317, 1.2520979596213484, 0.46352799871698, 0.22510933688694837]
        bandits = [k for k in normal(0, 1, 10)]
       # print(bandits)
        reward = 0
        armpl = bandit(0, 10, None)
        for k in range(1, 1001):
            reward += (val:=normal(bandits[armpl], 1))
            armpl = bandit(k, armpl, val)
        res.append(reward/k)
        if not (i+1) % 10: print(round(sum(res[i-9:i+1])/10, 2), end=" ")
        if not (i+1) % 100: print()
    print(f"SCORE: {sum(res)/(len(res)/1000)}") 

if __name__ == "__main__": tester()