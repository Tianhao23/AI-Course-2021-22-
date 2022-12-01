import sys;args = sys.argv[1:]
myPuzzles = open(args[0], "r").read().splitlines()
# Tianhao Chen, pd.4
import math, time
from math import log10, floor

length = int(math.sqrt(len(myPuzzles[0])))
for i in range(1,
               math.floor(math.sqrt(length)) + 1):  # creating the dimensions to make the puzzle as square as possible
    if length % i == 0:
        gHeight = i
        gWidth = length // i

symbols = {chr(x) for x in range(58 - (gHeight * gWidth), 58)}


def printPuzzle(pzl):
    output = ""
    x = gHeight - 1
    for idx in range(len(pzl)):
        output += pzl[idx] + " "
        if idx % gWidth == (gWidth - 1):  # if index reaches the end of a sub-block going across
            output += "  "  # add spaces for a new sub-block
            if idx % length == (length - 1):  # if index reaches the end of a row
                output += "\n"  # go to next row
                if idx // length == x:  # if the next row is a new sub-block
                    output += "\n"  # create another line for a new sub-block
                    x += gHeight
    print(output)


def checkSum(pzl):
    total = 0
    for elm in pzl:
        total += ord(elm)  # adds up add the ascii values of each character in the puzzle
    total -= (len(pzl) * ord(
        min(pzl)))  # subtracts the total with the ascii value of the minimum character times the length of the puzzle
    return total


rows = [{*range(idx, idx + length)} for idx in range(0, length * length, length)]
columns = [{*range(idx, length * length, length)} for idx in range(length)]
subBlocks = []
for i in range(length):
    subBlocks += [set()]


def compute():
    for idx in range(len(myPuzzles[0])):
        row = idx // length  # calculates which row the index is in
        col = idx % length  # calculates which column the index is in
        block = (row // gHeight) + (col // gWidth) * (length // gWidth)
        subBlocks[block].add(idx)


compute()
lCSets = rows + columns + subBlocks
posCon = [[csIdx for csIdx, cs in enumerate(lCSets) if idx in cs] for idx in range(length * length)]
nbrs = [(lCSets[posCon[idx][0]] | lCSets[posCon[idx][1]] | lCSets[posCon[idx][2]]) - {idx} for idx in
        range(length * length)]
nbrs2 = [(lCSets[posCon[idx][0]] | lCSets[posCon[idx][1]] | lCSets[posCon[idx][2]]) for idx in
        range(length * length)]
print(posCon)        
def bestSyb(dots): #part h
    btS = []
    for n in nbrs2: #for every neighbors
        dct = {s: set() for s in symbols} #create a dct for each symbol
        for idx in n: #for each index
            if idx in dots: #if it's a dot
                for x in dots[idx]: #check that dot's indeces, and add it
                    dct[x].add(idx)
        btS+=[(len(dct[s]), dct[s],s)  for s in dct if dct[s]] #add if that symbol has positions
    return min(btS)
def isInvalid(pzl, change):  # isValid but with constraints
    for idx in posCon[change]:  # for each value in that column
        checked = set()
        for elm in lCSets[idx]:
            if pzl[elm] in checked:  # if the symbol is in checked, then the puzzle is invalid
                return True
            if pzl[elm] in symbols:  # if the symbol is a symbol that can be used, add it to checked
                checked.add(pzl[elm])


def isFilledOut(pzl):  # checks if every index in puzzle has a legal symbol
    for elm in pzl:
        if elm not in symbols:
            return False
    return True


def possible(pzl, pos):  # calculates the possible number of symbols you can fill in an index
    return symbols - {pzl[elm] for elm in nbrs[pos] if pzl[elm] != '.'}


def bDot(dots):
    best = 0
    lowest = 20
    for i in dots:
        x = len(dots[i]) #length of number of choices
        if x < lowest:
            lowest = x
            best = i
    return best


def bF(pzl, dots):
    global bFnum
    bFnum +=1
    change = bDot(dots) #best dot position
    if not dots: return pzl
    setOfChoices = dots[change] #number of symbols
    num = len(setOfChoices)
    if num >=3: #if number of choices is 3 or more
        n, pos, sym = bestSyb(dots) #do best symbol
        for p in pos:
            dot2 = {i: (dots[i] - {sym}) if i in dots and i in nbrs[p] else dots[i] for i in dots if i!= p}
            subPzl = pzl[0:p] + sym + pzl[p + 1:]
            pSol = bF(subPzl, dot2)
            if pSol: return pSol
    else:
        for choice in setOfChoices:  # for every symbol you can use, add it to the first place needed to add a symbol
            dot2 = {i:(dots[i] -{choice}) if i in dots and i in nbrs[change] else dots[i] for i in dots if i!=change} 
            subPzl = pzl[0:change] + choice + pzl[change + 1:]
            pSol = bF(subPzl, dot2)
            if pSol: return pSol
    return ""


pzlNm = 1  # keeps track of the puzzle number
bFnum = 0
startTime = time.process_time()
for pzl in myPuzzles:
    dots = {i: possible(pzl, i) for i in range(len(pzl)) if pzl[i] == '.'}
    x = time.process_time()
    solution = bF(pzl, dots)
    cS = checkSum(solution)
    y = time.process_time() - x
    if y == 0.0:  # y may sometimes create a math domain error if it's 0 because of the log10
        totalTime = 0.0
    else:
        totalTime = round(y, 3 - int(floor(log10(abs(y)))) - 1)  # rounds the totalTime to 3 sig figs
    print(pzlNm, ":", pzl)
    if pzlNm < 10:
        print("   ", solution, cS, str(totalTime) + "s")
    elif pzlNm < 100:
        print("    ", solution, cS, str(totalTime) + "s")
    else:
        print("     ", solution, cS, str(totalTime) + "s")
    pzlNm += 1
end = time.process_time() - startTime
print("Number of bF calls", bFnum)
print("Total time", end)
# Tianhao Chen, pd. 4, 2023