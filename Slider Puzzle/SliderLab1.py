import sys; args = sys.argv[1:]
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
def bfs(start, goal):
    global steps #access and change the global variable steps
    if start == goal: #base case
        return [start]
    parseMe = [start]
    dctSeen = {start: 0}
    while parseMe: #goes through each item in parseMe
        node = parseMe.pop(0)    
        for nbr in neighbors(node): #gets neighbors of node
            if nbr not in dctSeen:
                if nbr == goal:
                    dctSeen[nbr] = node
                    temp = nbr
                    output = []
                    while temp != start: #creates the path of steps to solve the puzzle
                        output.append(temp)
                        temp = dctSeen[temp]
                    output.append(start) #add start to output as while loop leaves it out
                    steps = len(output)-1
                    return output[::-1] #returns output in reverse because the while loop adds from goal to start
                parseMe += [nbr]
                dctSeen[nbr]=node
    steps = -1
    return []
#performing the process
if args:
    start = args[0] # create the start and goal string
    try:
        goal = args[1]
    except:
        goal = "".join(sorted(start.replace("_", "")))+"_"
    length = len(start)
    a = time.time()
    for i in range(1, math.floor(math.sqrt(length))+1): #creating the dimensions to make the puzzle as square as possible
        if length % i ==0:
            gHeight = i
            gWidth = length//i
    solve = bfs(start, goal)
    printSequence(solve)
else:
    goal = "12345678_" 
    temp = ['1','2','3','4','5','6','7','8','_']
    
    x = time.time()
    solvable = 0
    totalPathLength = 0
    totalSolveTime = 0
    totalUnsolveTime = 0
    unsolvable = 0
    gWidth = 3
    gHeight = 3
    length = 9
    for i in range(500):
        temp2 = ""
        seen = set()
        while len(seen)!=9:
            i = (random.randint(0,8))
            if i not in seen:
                temp2+= temp[i]
                seen.add(i)
        start = "".join(temp2)
        startTime = time.time()
        path = bfs(start, goal)
        elapsedTime = time.time() - startTime
        if path:
            totalPathLength += (len(path)-1)
            totalSolveTime += elapsedTime 
            solvable +=1
        else:
            unsolvable += 1
            totalUnsolveTime += elapsedTime
    y = time.time() -x
    print("Total time:", y)
    print("Number of Solvable Puzzles:", solvable)
    print("Average path length:", totalPathLength/solvable)
    print("Average time for solvable puzzles:", totalSolveTime/solvable)
    print("Average time for unsolvable:", totalUnsolveTime/unsolvable)

        
