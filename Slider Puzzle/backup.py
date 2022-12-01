import sys; args = sys.argv[1:]
myWords = open(args[0],"r").read().splitlines()
import time, math, random
from math import log10, floor
# Tianhao Chen, pd.4
steps = 0
psbeNbr = {}
mht = {}
icprg = {}
goal = myWords[0]
length = len(goal)


for lgth in range(1, math.floor(math.sqrt(length))+1): #creating the dimensions to make the puzzle as square as possible
    if length % lgth ==0:
        gHeight = lgth
        gWidth = length//lgth
for i in range(16): #generates the possible neightbors of each index
    psbeNbr[i] = []
    if i % gWidth != gWidth-1:
        psbeNbr[i] += [i+1]
    if i % gWidth != 0:
        psbeNbr[i] += [i-1]
    if 0<=i<= (length-gWidth)-1:
        psbeNbr[i] += [i+gWidth]
    if gWidth<=i <=length-1:
        psbeNbr[i] += [i-gWidth]

for e in goal: #generates the row and column number of each element in goal excluding "_"
    index = goal.index(e)
    if e != "_":
          mht[e] = [index//gHeight,index%gWidth]
for e in goal: #generates the difference in manhattan distance of each element from it's start position to it's end position
    if e!= "_":
        for i in range(16): #for each possible index that the element can go to
            for nbr in psbeNbr[i]: #find the possible neighbors that the element can go to at that index
                initialManhattan = (abs(i//gHeight - mht[e][0])) + (abs(i%gWidth - mht[e][1]))
                finalManhattan = (abs(nbr//gHeight - mht[e][0])) + (abs(nbr%gWidth - mht[e][1]))
                icprg[e, i, nbr] = finalManhattan - initialManhattan #change in manhattan distance
def neighbors(puzzle): #finding and returning the neighbors based on index
    nbrs = []
    index = puzzle.index("_")
    for i in psbeNbr[index]: #finds the index of "_" in puzzle, and finds the list of neighbors in the lookup table, adding it to nbrs list
        nbrs.append(swap(i, index, list(puzzle)))
    return nbrs
def swap(x,y,puzzle1): #swapping the "_" and its neighbor
    puzzle1[x], puzzle1[y] = puzzle1[y], puzzle1[x]
    return "".join(puzzle1)          
def printSequence(lst): 
    banded = 9
    for x in range(len(lst)//banded+1): #calculates the number of rows needed
        for i in range(gHeight): #goes through height of puzzle
            temp = []
            for j in lst[x*banded:(x+1)*banded]: #goes through count items in list to put them in one row
                temp.append(" ".join(j[i*gWidth:(i+1)*gWidth])) #joins the width of the each puzzle together
            print("  ".join(temp))  #joins the puzzles together
        print("--------------------------------------------------------------------------\n")
    print("Steps:", steps)
    b = time.time()
    c = b-a
    totalTime = round(c, 3-int(floor(log10(abs(c))))-1) #rounds the totalTime to 3 sig figs
    print("Time:",totalTime,"s")
def AStar(start, goal):
    global moves
    if start == goal: #if no moves is required
        moves = "G"
        return [start]
    if isSolvable(start, goal) == False: # if there is no solution
        moves = "X"
        return []
    pointer = manhattanLookup(start)
    openSet = {} #bucket, where the key represents the puzzle's manhattan distance
    for i in range(60):
        openSet[i] = []
    openSet[pointer]  = [(pointer, start.index("_"), start, 0, "")]
    closedSet = {}
    for e in openSet: #goes through each key in openSet
        for nde in openSet[e]: #if the key is not empty, it will go through each element in the value
            dis, index, pzl, lvl, parent = nde
            if pzl in closedSet: continue
            closedSet[pzl] = parent
            #for nbr in neighbors(pzl):
            for i in psbeNbr[index]: #produces the neighbors of puzzle without using list
                nbr = swap(i, index, list(pzl))
                if nbr == goal:
                    closedSet[nbr] = pzl
                    temp = nbr
                    output = []
                    while temp != start: #creates the path of steps to solve the puzzle
                        output.append(temp)
                        temp = closedSet[temp]
                    output.append(start) #add start to output as while loop leaves it out
                    return output[::-1] #returns output in reverse because the while loop adds from goal to start
                if nbr in closedSet: continue
                elmSwapped = nbr[index] #finds the element that was swapped with "_"
                newEst = (lvl+1) + ((dis-lvl) + icprg[elmSwapped, pzl.index(elmSwapped), nbr.index(elmSwapped)])           
                openSet[newEst].append((newEst, i, nbr, lvl+1, pzl))
def manhattanLookup(pzl):
    count = 0
    for e in pzl:
        if e !="_":
            row = pzl.index(e) // gHeight
            col = pzl.index(e) % gWidth
            count += (abs(row - mht[e][0])) + (abs(col - mht[e][1])) #uses lookuptable it row and column positions of goal elements
    return count
def manhattan(pzl, pzl1): #calculates manhattan distance
    count = 0
    for i in pzl:    
        if i != "_":
            temp = pzl.index(i)
            temp1 = pzl1.index(i)
            count+= (abs(temp//gHeight - temp1//gHeight)) + (abs(temp%gWidth - temp1%gWidth)) # calculates the shortest distance of an element between the two puzzles
    return count
def inversionCount(start, goal): #calculates the inversion count for a puzzle
    ivrsCount = 0
    for i in range(len(start)):
        for j in range(i+1, len(start)):
            if ((start.index(goal[j]) - start.index(goal[i])) <0): #if element of higher index in goal has a smaller index in start compared to another element of lower index in goal, then an inversion count occurs
                ivrsCount+=1         
    return ivrsCount
def createPath(path):
    st = ""
    for i in range(len(path)-1):
        diff = path[i+1].find("_")-path[i].find("_")#finds the change in index for "_"
        if diff>0: #if _ moved +1 index, it moved to the right. If another positive number, it moved down
            if diff == 1: 
                st+="R"
            else:
                st+="D"
        elif diff<0: #if _ moved -1 index, it moved to the left. If another negative number, it moved up
            if diff == -1:
                st+="L"
            else:
                st +="U"
    return st
def isSolvable(start, goal):
    count = inversionCount(start.replace("_",""), goal.replace("_","")) #finds the inversion count of start puzzle with respect to goal puzzle
    if gWidth % 2 == 0: #if width is even, calculate the row difference of "_", then see if its parity is the same as goal
        u = goal.index("_")//gHeight
        v = start.index("_")//gHeight
        x = count + (abs(u-v))
        return x% 2 ==0
    else: # if width is odd, just calculate if inversion count parity is same as goal
        return count % 2 == 0
#performing the process
for sltn in range(len(myWords)): #searches for the solution for every puzzle
    start = myWords[sltn]
    moves = ""
    a = time.process_time()
    solve = AStar(start, goal)
    b = time.process_time()
    c = b-a
    if len(solve) > 0: #if a solution exists
        if len(solve) != 1: #if the solution isn't just start
            moves = createPath(solve) +moves
        print(str(sltn)+":",start, "solved in",c,"secs => path:", moves)
    else: #if solution does not exist
        print(str(sltn)+":", start, " is unsolvable => path:", moves)
#Tianhao Chen, pd. 4, 2023