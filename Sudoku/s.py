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
    #block = 0  #keeps track of the sub-block number the code is on
    #blockRow = 0 #keeps track of the which number of row of sub-blocks we are on
    #x = gHeight - 1
    for idx in range(len(myPuzzles[0])):
        row = idx // length #calculates which row the index is in
        col = idx % length #calculates which column the index is in
        block = (row//gHeight)+ (col//gWidth)* (length//gWidth) 
        subBlocks[block].add(idx)

compute()
#print(subBlocks)
lCSets = [{*range(idx, idx+length)}for idx in range(0, length*length, length)]+ [{*range(idx,length*length, length)} for idx in range(length)] + subBlocks
posCon = [[csIdx for csIdx, cs in enumerate(lCSets) if idx in cs] for idx in range(length*length)]
nbrs = [(lCSets[posCon[idx][0]]|lCSets[posCon[idx][1]]|lCSets[posCon[idx][2]])-{idx} for idx in range(length*length)]
#print(nbrs)
#print(lCSets)
#print(posCon)
def isInvalidR(pzl, r, c, b): #isValid but with constraints
    checked = set() #reset the checked list
    for elm in columns[c]: #for each value in that column
        if pzl[elm] in checked: # if the symbol is in checked, then the puzzle is invalid
            return True
        if pzl[elm] in symbols: #if the symbol is a symbol that can be used, add it to checked
            checked.add(pzl[elm])
    checked = set()#reset the checked list
    for elm in rows[r]:#for each value in that row
        
        if pzl[elm] in checked:# if the symbol is in checked, then the puzzle is invalid
            return True
        if pzl[elm] in symbols:#if the symbol is a symbol that can be used, add it to checked
            checked.add(pzl[elm])
    checked = set()#reset the checked list
    for elm in subBlocks[b]:#for each value in that sub-block
        if pzl[elm] in checked:# if the symbol is in checked, then the puzzle is invalid
            return True
        if pzl[elm] in symbols:#if the symbol is a symbol that can be used, add it to checked
            checked.add(pzl[elm])

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
    return len(symbols) - len(filled), symbols-filled
    #return symbols - filled
def used(pzl, pos): #calculates the symbols already used
    filled = set()
    for elm in nbrs[pos]:
            if pzl[elm] != '.' and pzl[elm] not in filled:
                filled.add(pzl[elm])
    return filled
def bestDot(pzl): #calculates a dictonary of all the dots and possible number of symbols
    dotD = {}
    dotD2 = {}
    pos = 0
    dot = pzl.find('.',pos)
    #if dot == -1:
        #dotD = -1
    while dot !=-1:
        choices, choices2 = possible(pzl, dot)
        dotD[dot] = choices #dot index as key, number of choices as value
        dotD2[dot] = choices2
        pos = dot+1
        dot = pzl.find('.',pos)
    #if dotD != -1:
        #valid = dotD[min(dotD, key =dotD.get)]
        #if valid == 0:
            #dotD = 0
    return dotD, dotD2
    
# def update(dots, change): #updates the dictonary for the dots
#     changes = [posCon[change]]
#     for nbr in changes:
#         for idx in nbr:
#             if idx in dots:
#                 dots[idx] -= 1
#     return dots
def bF(pzl,change):
    #returns a solved pzl or the empty string on failure
    #if isInvalidR(pzl, r,c,b): return ""
    if isInvalid(pzl, change): return ""
    if isFilledOut(pzl): return pzl
    
    dots, dots2 = bestDot(pzl)
    #if dots == 0: return ""
    #if dots == -1: return pzl
    change = min(dots, key =dots.get)
    setOfChoices = dots2[change]
    
   
    #u = used(pzl, change)
    #del dots[change]
    #dots = update(dots, change)
    for choice in setOfChoices: #for every symbol you can use, add it to the first place needed to add a symbol
        subPzl = pzl[0:change] + choice+pzl[change+1:]
        #row = change // length #calculates which row the index is in
        #col = change % length #calculates which column the index is in
        #block = (row//gHeight)+(col//gWidth)* (length//gWidth) 
        #print(subPzl)
        pSol = bF(subPzl, change)
        if pSol: return pSol
    return ""


pzlNm = 1 #keeps track of the puzzle number
test = [myPuzzles[10]]
#for pzl in test:
for pzl in myPuzzles:
    #printPuzzle(pzl)
    #dots = bestDot(pzl)
    x = time.process_time()
    solution = bF(pzl, 0)
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
print(time.process_time())
# printPuzzle(myPuzzles[0])
# print(myPuzzles[0])
# print(length, gWidth, gHeight)
#Tianhao Chen, pd. 4, 2023