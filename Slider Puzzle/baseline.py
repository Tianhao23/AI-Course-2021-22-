import sys; args = sys.argv[1:]
myWords = open(args[0],"r").read().splitlines()
import time, math, random
from math import log10, floor
# Tianhao Chen, pd.4
steps = 0
def neighbors(puzzle): #finding and returning the neighbors based on index
    nbrs = []
    index = puzzle.index("_")
    #index cases
    if index % gWidth != gWidth-1:
        nbrs.append(swap(index+1,index, puzzle))
    if index % gWidth != 0:
        nbrs.append(swap(index-1,index, puzzle))
    if 0<=index<= (length-gWidth)-1:
        nbrs.append(swap(index+gWidth,index, puzzle))
    if gWidth<=index <=length-1:
        nbrs.append(swap(index-gWidth,index, puzzle))
    return nbrs
def swap(x,y,puzzle1): #swapping the "_" and its neighbor
    temp = list(puzzle1)
    temp2 = temp[x]
    temp[x]=temp[y]
    temp[y]=temp2
    return "".join(temp)          
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
    openSet = [(manhattan(start,goal), start, 0, "")] #creates a list of tuples containing f, pzl, lvl, and parent
    closedSet = {}

    while openSet:
        openSet = sorted(openSet) #sorts the openSet, putting the puzzle with the least f in front
        dis, pzl, lvl, parent = openSet.pop(0)
        if pzl in closedSet: continue
        closedSet[pzl] = parent

        for nbr in neighbors(pzl):
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
            newEst = (lvl+1) + manhattan(nbr, goal)
            openSet.append((newEst, nbr, lvl+1, pzl))

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
    #print(ivrsCount)   #test for inversion count        
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
goal = myWords[0]
length = len(goal)

for i in range(1, math.floor(math.sqrt(length))+1): #creating the dimensions to make the puzzle as square as possible
    if length % i ==0:
        gHeight = i
        gWidth = length//i
for i in range(len(myWords)): #searches for the solution for every puzzle
    start = myWords[i]
    moves = ""
    a = time.process_time()
    solve = AStar(start, goal)
    b = time.process_time()
    c = b-a
    if len(solve) > 0: #if a solution exists
        if len(solve) != 1: #if the solution isn't just start
            moves = createPath(solve)
        print(str(i)+":",start, "solved in",c,"secs => path:", moves)
    else: #if solution does not exist
        print(str(i)+":", start, " is unsolvable => path:", moves)
    #totalTime = round(c, 3-int(floor(log10(abs(c))))-1) #rounds the totalTime to 3 sig figs
    #printSequence(solve)
#Tianhao Chen, pd. 4, 2023