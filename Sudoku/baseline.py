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
symbols = [str(x)for x in range(1,10)] #fix this later
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
rows = []
columns = []
subBlocks = []
for i in range(length):
    rows +=[[]]
    columns +=[[]]
    subBlocks +=[[]]

block = 0  #keeps track of the sub-block number the code is on
blockRow = 0 #keeps track of the which number of row of sub-blocks we are on
x = gHeight - 1
for idx in range(len(myPuzzles[0])):
    row = idx // length #calculates which row the index is in
    col = idx % length #calculates which column the index is in
    rows[row] += [idx]
    columns[col] += [idx]
    
    subBlocks[block] +=[idx]
    if idx% gWidth == (gWidth-1): #if index reaches the end of a sub-block going across
        if idx % length == (length-1): #if index reaches the end of a row
            if idx // length == x: #if it reaches the end of a row of sub-blocks, update block and blockRow
                block +=1
                blockRow = block
                x+=gHeight
            else:
                block = blockRow #set the block to blockRow because we're still on the same row of sub-blocks
        else:
            block+=1
#print(subBlocks)


#rows is pzl index // side length
# column is pzl index % side length
#sub-blocks: width is starting + width, then skip sidelength elems, do it gHeight times
def isInvalid(pzl): 
    for idx in columns: #for every column
        checked = [] #reset the checked list
        for elm in idx: #for each value in that column
            if pzl[elm] in checked: # if the symbol is in checked, then the puzzle is invalid
                return True
            if pzl[elm] in symbols: #if the symbol is a symbol that can be used, add it to checked
                checked+=pzl[elm]
    for idx in rows:#for every row
        checked = []#reset the checked list
        for elm in idx:#for each value in that row
            if pzl[elm] in checked:# if the symbol is in checked, then the puzzle is invalid
                  return True
            if pzl[elm] in symbols:#if the symbol is a symbol that can be used, add it to checked
                checked+=pzl[elm]
    for idx in subBlocks:#for every sub-block
        checked = []#reset the checked list
        for elm in idx:#for each value in that sub-block
            if pzl[elm] in checked:# if the symbol is in checked, then the puzzle is invalid
                return True
            if pzl[elm] in symbols:#if the symbol is a symbol that can be used, add it to checked
                checked+=pzl[elm]
def isFilledOut(pzl):#checks if every index in puzzle has a legal symbol
    for elm in pzl: 
        if elm not in symbols:
            return False
    return True

def bF(pzl):
    #returns a solved pzl or the empty string on failure
    if isInvalid(pzl): return ""
    if isFilledOut(pzl): return pzl

    setOfChoices = symbols
    for choice in setOfChoices: #for every symbol you can use, add it to the first place needed to add a symbol
        adjPzl = [*pzl]
        adjPzl[pzl.index(".")] = choice
        subPzl = ''.join(adjPzl)
        #print(subPzl)
        pSol = bF(subPzl)
        if pSol: return pSol
    return ""
#test = [myPuzzles[5], myPuzzles[6]]
#for pzl in test:
pzlNm = 1 #keeps track of the puzzle number
for pzl in myPuzzles:


    x = time.process_time()
    solution = bF(pzl)
    cS = checkSum(solution)
    y = time.process_time() - x
    if int(y) == 0: #y may sometimes create a math domain error if it's 0 because of the log10
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
# printPuzzle(myPuzzles[0])
# print(myPuzzles[0])
# print(length, gWidth, gHeight)
#Tianhao Chen, pd. 4, 2023