import sys; args = sys.argv[1:]
myPuzzles = open(args[0],"r").read().splitlines()
# Tianhao Chen, pd.4
import math, time
from math import log10, floor

length = int(math.sqrt(len(myPuzzles[0])))
for i in range(1, math.floor(math.sqrt(length))+1): #creating the dimensions to make the puzzle as square as possible
        if length % i ==0:
            gHeight = i
            gWidth = length//i

symbols = {chr(x) for x in range(58-(gHeight*gWidth),58)}

def printPuzzle(pzl):
    output = ""
    x = gHeight -1
    for idx in range(len(pzl)):
        output += pzl[idx] + " "
        if idx% gWidth == (gWidth-1): #if index reaches the end of a sub-block going across
            output+= "  " #add spaces for a new sub-block
            if idx % length == (length-1):  #if index reaches the end of a row
                output+="\n" #go to next row
                if idx // length == x: #if the next row is a new sub-block
                    output+="\n" #create another line for a new sub-block
                    x+=gHeight
    print(output)
def checkSum(pzl):
    total = 0
    for elm in pzl:
        total += ord(elm) #adds up add the ascii values of each character in the puzzle 
    total -= (len(pzl) * ord(min(pzl))) # subtracts the total with the ascii value of the minimum character times the length of the puzzle
    return total
rows = [{*range(idx, idx+length)}for idx in range(0, length*length, length)]
columns = [{*range(idx,length*length, length)} for idx in range(length)]
subBlocks = []
for i in range(length):
    subBlocks += [set()]
def compute():
    for idx in range(len(myPuzzles[0])):
        row = idx // length #calculates which row the index is in
        col = idx % length #calculates which column the index is in
        block = (row//gHeight)+ (col//gWidth)* (length//gWidth) 
        subBlocks[block].add(idx)

compute()
#print(subBlocks)
lCSets = rows+ columns + subBlocks
posCon = [[csIdx for csIdx, cs in enumerate(lCSets) if idx in cs] for idx in range(length*length)]
nbrs = [(lCSets[posCon[idx][0]]|lCSets[posCon[idx][1]]|lCSets[posCon[idx][2]])-{idx} for idx in range(length*length)]
#print(lCSets)
#print(posCon)

def isInvalid(pzl,change): #isValid but with constraints
    for idx in posCon[change]: #for each value in that column
        checked = set()
        for elm in lCSets[idx]:
            if pzl[elm] in checked: # if the symbol is in checked, then the puzzle is invalid
                return True
            if pzl[elm] in symbols: #if the symbol is a symbol that can be used, add it to checked
                checked.add(pzl[elm])
def isFilledOut(pzl):#checks if every index in puzzle has a legal symbol
    for elm in pzl: 
        if elm not in symbols:
            return False
    return True
def possible(pzl, pos): #calculates the possible number of symbols you can fill in an index
    filled = set()
    for elm in nbrs[pos]:
            if pzl[elm] != '.' and pzl[elm] not in filled:
                filled.add(pzl[elm])
    return symbols - filled

def createDots(pzl): #calculates a dictonary of all the dots and possible number of symbols
    return {i:possible(pzl, i) for i in range(len(pzl)) if pzl[i] == '.' }  
    # dotD= {}
    # for i in range(len(pzl)):
    #     if pzl[i] == '.':
    #         dotD[i] = possible(pzl, i)
    #return dotD
def bDot(dots):
    if not dots:
        return -2
    #best = min(dots, key =dots.get)

    best = 0
    lowest = 20
    for i in dots:
        x = len(dots[i])
        if x < lowest:
            lowest = x
            best = i
    # print(lowest)
    if lowest== 0:
        return -1
    return best
def update(change, dots, choice):
    dot2 = {i:(dots[i] -{choice}) if i in dots and i in nbrs[change] else dots[i] for i in dots} 
    # dot2 = {i:dots[i] for i in dots}
    # changes = nbrs[change]
    # for idx in changes:
    #     if idx in dot2:
    #         dot2[idx] = dot2[idx] - {choice}
    return dot2
def bF(pzl, change, dots, choice):
    global bFnum, nChoice, maxC, pzlNm, puzl

    bFnum +=1
    #returns a solved pzl or the empty string on failure
    #change = bDot(dots, choice)
    change = bDot(dots)
    if change == -1: 
        nChoice +=1
        return ""
    if change == -2: return pzl
    if dots[change] == 0:
        nChoice +=1
    #printPuzzle(pzl)
    #if isInvalid(pzl, change): return ""
    #if isFilledOut(pzl): return pzl
    #dots = bestDot(pzl)
    if len(dots[change])>maxC:
        maxC = len(dots[change])
        puzl = (pzlNm, pzl, change, dots[change])
    #print(change)

    
    #print(dots)
    for choice in dots.pop(change): #for every symbol you can use, add it to the first place needed to add a symbol
            dot2 = update(change, dots, choice)
            #dot2 = {i:dots[i] for i in dots} 
            #dot2 = {}
            #for i in dots:
            #    dot2[i] = dots[i]
            #changes = nbrs[change]
            #dot2 = dot2[idx] - {choice} if idx in dot2 for idx in changes
            #for idx in changes:
                #if idx in dot2:
                    #dot2[idx] = dot2[idx] - {choice}
            subPzl = pzl[0:change] + choice+pzl[change+1:]
            pSol = bF(subPzl, change, dot2, choice)
            if pSol: return pSol
    return ""


pzlNm = 1 #keeps track of the puzzle number
bFnum = 0
totalDot = 0
nChoice = 0
maxC = 0
puzl = ()
test = [myPuzzles[11]]
#for pzl in test:
startTime = time.process_time()
for pzl in myPuzzles:
    #printPuzzle(pzl)
    dots = createDots(pzl)
    totalDot += len(dots)
    #print(pzl)
    #print(dots)
    x = time.process_time()
    solution = bF(pzl, 0, dots, -1)
    cS = checkSum(solution)
    y = time.process_time() - x
    if y == 0.0: #y may sometimes create a math domain error if it's 0 because of the log10
        totalTime = 0.0
    else:
        totalTime = round(y, 3-int(floor(log10(abs(y))))-1) #rounds the totalTime to 3 sig figs
    print(pzlNm, ":", pzl)
    if pzlNm <10:
        print("   ", solution, cS, str(totalTime) + "s")
    elif pzlNm<100:
        print("    ", solution,  cS, str(totalTime) + "s")
    else:
        print("     ", solution,  cS,str(totalTime) + "s")
    pzlNm+=1
end = time.process_time()-startTime
print("Number of bF calls", bFnum)
print("Total time", end)
print("Total Dots Filled:", totalDot)
print("No choices:", nChoice)
print("Max choices", maxC)
print(puzl)
printPuzzle(puzl[1])
# printPuzzle(myPuzzles[0])
# print(myPuzzles[0])
# print(length, gWidth, gHeight)
#Tianhao Chen, pd. 4, 2023