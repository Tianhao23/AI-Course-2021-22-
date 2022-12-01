import sys;args = sys.argv[1:]
# Tianhao Chen, pd.4
#args = ['15x15', '9x4', '6x11', '10x5', '4x7', '5x5', '3x6']
import math, time
from math import log10, floor
if 'x' in args[0]:
    height = int(args[0][0:args[0].index('x')])
    width = int(args[0][args[0].index('x')+1:])
    check = 1
elif 'X' in args[0]:
    height = int(args[0][0:args[0].index('X')])
    width = int(args[0][args[0].index('X')+1:])
    check = 1
else:
    height = int(args[0])
    width = int(args[1])
    check = 2
cons = []
while check < len(args):
    if 'x' in args[check]:
        cons.append((int(args[check][0:args[check].index('x')]), int(args[check][args[check].index('x')+1:])))
    elif 'X' in args[check]:
        cons.append((int(args[check][0:args[check].index('X')]), int(args[check][args[check].index('X')+1:])))
    else:
        cons.append((int(args[check]), int(args[1+check])))
        check+=1
    check +=1
def printPuzzle(bSlate):
    i = 0
    for j in range(height):
        print(bSlate[i:i+width])
        i+=width
def impossible():
    area = width * height
    addA = 0
    for i in cons:
        addA += (i[0] * i[1])
        if addA > area:
            return True
    return False
def countHoles():
    area = width * height
    pArea = 0
    for i in cons:
        pArea += (i[0] * i[1])
    return area-pArea
def addPuzzle(pzl, h, w):
    adj = list(pzl)
    #printPuzzle(pzl)
    #print(w, h)
    #print(adj)
    pos = pzl.find('.')
    row = pos//width
    temp = pos
    for i in range(h):
        for j in range(w):
            if (temp//width) >= height or (temp%width)>= width or (temp//width) != row or adj[temp] == "1":
                return ''
            #print(adj)
            #input()
            adj[temp] = '1'
            temp +=1
        temp +=(width-w)
        row = temp//width
    return ''.join(adj)
def sortB(possible):
    store = []
    for i in range(len(possible)):
        area = possible[i][0] * possible[i][1]
        store.append((area, i))
    store.sort()
    x = []
    for i in store:
        x+= [possible[int(i[1])]]
    return x
def possibles(pzl, possible):
    possible.sort(key = lambda x:x[1])
    #possible = sortB(possible)
    lst = []
    for i in possible[::-1]:
        #if addPuzzle(pzl, i[0], i[1]):
        lst += [(i[0], i[1])]
        if (i[0],i[1]) != (i[1],i[0]):
            #if addPuzzle(pzl, i[1], i[0]):
            lst += [(i[1], i[0])]
    return lst
def psb(pzl, h, w):
    pos = pzl.find('.')
    row = pos//width + h
    col = pos%width + w
    if row >height:
        return False
    if col > width:
        return False
    for i in range(w):        
        if pzl[pos+i] == '1':
            return False
    return True
def checkHoles(pzl, used):
    while pzl.count('.') > 0:
        pos = pzl.find('.')
        used += ['1x1']
        pzl = pzl[0: pos] + 'h' + pzl[pos+1:]
    return used
def bF(bSlate, possible, used):
    global holes
    # printPuzzle(bSlate)
    # print(used)
    # print(possible)
    # input()
    if not possible:
        #printPuzzle(bSlate)
        used = checkHoles(bSlate, used)
        return ' '.join(used)
    
    setOfChoices = possibles(bSlate, possible)
    pos = bSlate.find('.')
    #for every possible:
    #if 
    # if not setOfChoices:        
    #     temp2 = bSlate[0:pos] + 'h' + bSlate[pos+1:]
    #     if temp2.count('h') > holes:
    #         return ''
    #     temp = used + ['1x1']
    #     return bF(temp2, possible, temp)

    for choice in setOfChoices:
        h = choice[0]
        w = choice[1]
        nSlate = addPuzzle(bSlate, h, w)
        if nSlate == '':
            temp2 = bSlate[0:pos] + 'h' + bSlate[pos+1:]
            if temp2.count('h') > holes:
                return ''
            temp = used + ['1x1']
            return bF(temp2, possible, temp)
        blk = str(h)+"x"+str(w)
        temp = used+[blk]
        newP = [i for i in possible]
        if (h,w) in newP:
            newP.remove((h,w))
        else:
            newP.remove((w,h))
        pSol = bF(nSlate, newP, temp)
        if pSol: return pSol
    return ""
a = time.process_time()
if impossible():
    print("No solution")
else:
    holes = countHoles()
    bSlate = "." * (width * height)
    used = []
    possible = [i for i in cons]
    solution = bF(bSlate, possible, used)
    if solution:
        print("Decomposition:", solution)
    else:
        print("No solution")
b = time.process_time()-a
print(b)
# Tianhao Chen, pd. 4, 2023
