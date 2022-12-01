import sys;args = sys.argv[1:]
# Tianhao Chen, pd.4
import time
#creates the board
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
#creates a list for all the blocks
while check < len(args):
    if 'x' in args[check]:
        cons.append((int(args[check][0:args[check].index('x')]), int(args[check][args[check].index('x')+1:])))
    elif 'X' in args[check]:
        cons.append((int(args[check][0:args[check].index('X')]), int(args[check][args[check].index('X')+1:])))
    else:
        cons.append((int(args[check]), int(args[1+check])))
        check+=1
    check +=1
def printPuzzle(bSlate): #prints the board in 2-D
    i = 0
    for j in range(height):
        print(bSlate[i:i+width])
        i+=width
def impossible(): #checks if the total blocks' area is greater than the boards area
    area = width * height
    addA = 0
    for i in cons:
        addA += (i[0] * i[1])
        if addA > area:
            return True
    return False
def countHoles(): #counts the holes by subtracting area of board by total area of each block
    area = width * height
    pArea = 0
    for i in cons:
        pArea += (i[0] * i[1])
    return area-pArea
def addPuzzle(pzl, h, w): #adds a block to the board, checking to see if adding it is legal
    adj = list(pzl)
    pos = pzl.find('.')
    row = pos//width
    temp = pos
    for i in range(h):
        for j in range(w):
            if (temp//width) >= height or (temp%width)>= width or (temp//width) != row or adj[temp] == "1":
                return ''
            adj[temp] = '1'
            temp +=1
        temp +=(width-w)
        row = temp//width
    return ''.join(adj)
def sortB(possible):#sorts the blocks by area from smallest to greatest
    store = []
    for i in range(len(possible)):
        area = possible[i][0] * possible[i][1]
        store.append((area, i))
    store.sort()
    x = []
    for i in store:
        x+= [possible[int(i[1])]]
    return x
def possibles(pzl, possible): #finds all the possible blocks that can be placed
    #possible.sort(key = lambda x:x[1])
    possible = sortB(possible)
    lst = []
    for i in possible[::-1]: #list is reversed so that it's from largest to smallest
        if addPuzzle(pzl, i[0], i[1]):
            if (i[0],i[1]) not in lst:
                lst += [(i[0], i[1])]
        if (i[0],i[1]) != (i[1],i[0]):
            if addPuzzle(pzl, i[1], i[0]):
                if (i[1],i[0]) not in lst:
                    lst += [(i[1], i[0])]
    return lst
def checkHoles(pzl, used): #checks if there's empty spaces on the board. If so, there's a hole there
    while pzl.count('.') > 0:
        pos = pzl.find('.')
        used += ['1x1']
        pzl = pzl[0: pos] + 'h' + pzl[pos+1:]
    return used
def bF(bSlate, possible, used):
    global holes
    if not possible: #if all blocks are used, we're done
        used = checkHoles(bSlate, used)
        return ' '.join(used)
    
    setOfChoices = possibles(bSlate, possible)
    pos = bSlate.find('.')
    if not setOfChoices:  #if there's no possible blocks, try and add a hole there
        
        temp2 = bSlate[0:pos] + 'h' + bSlate[pos+1:]
        if temp2.count('h') > holes:
            return ''
        temp = used + ['1x1']
        return bF(temp2, possible, temp)

    for choice in setOfChoices:
        h = choice[0]
        w = choice[1]
        nSlate = addPuzzle(bSlate, h, w)
        #if nSlate == '': return ''
        blk = str(h)+"x"+str(w)
        temp = used+[blk]
        newP = [i for i in possible]
        if (h,w) in newP: #remove that block from possible blocks
            newP.remove((h,w))
        else:
            newP.remove((w,h))
        pSol = bF(nSlate, newP, temp)
        if pSol: return pSol
    if bSlate.count('h')<holes: #try a hole for the first blank if nothing else works
        nSlate = bSlate[0:pos] + 'h' + bSlate[pos+1:]
        temp = used + ['1x1']
    return bF(nSlate, possible, temp)
    #return ""
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
