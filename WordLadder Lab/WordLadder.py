import sys; args = sys.argv[1:]
myWords = open(args[0],"r").read().splitlines()
#Tianhao Chen, pd. 4, 2023
import time, random
from math import log10, floor
a = time.time()
maxDegree = 0
def makeGraph(list): #creates a graph based on a list of words
    dctGraph = {} 
    for i in list:
        dctGraph[i] = [] #puts all the words in a key with an empty list as the value
    for x in dctGraph:
        nbr = createNeighbors(x) #creates possible neighbors of word x
        for j in nbr:
            if j in dctGraph and j!= x: #if word in neighbor is in graph, then there is an edge
                dctGraph.get(x).append(j) 
    return dctGraph
def createNeighbors(word):
    nbrs = set()
    letters = "abcdefghijklmnopqrstuvwxyz" #
    for i in range(6):
        for j in range(26):
            temp = list(word)
            if temp[i]!= letters[j]:
                temp[i] = letters[j] #sets each index of word as each of the letters in the alphabet
            nbrs.add("".join(temp))
    return nbrs
def isEdge(a, b): #checks if two words are edges
    count = 0
    for i in range(len(a)):#goes through each letter to see if they match
        if a[i]!=b[i]:
            count += 1
    if count == 1: #return true only if count is 1, meaning that there is only 1 letter difference
        return True
    return False
def printOut(wrdgrph): #prints exercises 1-4
    print("Word count:", len(myWords))
    print("Edge count:", countEdge(wrdgrph))
    print("Degree list:", degreeList(wrdgrph))
    b = time.time()
    c = b-a
    totalTime = round(c, 3-int(floor(log10(abs(c))))-1) #rounds the totalTime to 3 sig figs
    print("Construction time:", str(totalTime)+"s")
def countEdge(wrdgrph): #counts the number of edges
    count = 0
    for i in wrdgrph:
        temp = wrdgrph.get(i)
        count += len(temp)
    return count//2 #divides by 2 because each edge is counted twice
def degreeList(wrdgrph): #returns a string with degrees
    global maxDegree
    result = ""
    temp = []
    for i in wrdgrph: #goes through each neighbor list and adds its length to a list
        x = wrdgrph.get(i)
        temp.append(len(x))
    maxDegree = max(temp) #finds the max degree
    for i in range(maxDegree+1): # counts the number of occurrences for each degree up to maxDegree, adds value to result
        if temp.count(i)!=0:
            result += " "+str(temp.count(i))
    return result
output = makeGraph(myWords)
printOut(output)

def secondHighestDegree(myGrph):
    x = maxDegree-1
    for i in myGrph:
        if len(myGrph.get(i)) == x: #if word is of secondHighestDegree, return it
            return i
    return ""

def makeCCs(output):
    cnctdCmpnt= []
    seen = set() #set that stores all the words that we've visited
    for i in output:
        parseMe = [i]
        dctSeen = [] #seen words for that particular connected component
        while parseMe: #goes through each item in parseMe
            node = parseMe.pop(0)    
            for nbr in output.get(node): #gets neighbors of node
                if nbr not in seen:
                    if nbr not in dctSeen: #if they are not in seen or dctSeen, add it as part of the connected component
                        parseMe += [nbr]
                        dctSeen.append(nbr)
                        seen.add(nbr)
        if set(dctSeen) not in cnctdCmpnt:
            cnctdCmpnt.append(set(dctSeen))
    return cnctdCmpnt
def findCCSizes(conComp):
    result = set()
    for i in conComp:
        result.add(len(i)) #set with all the different lengths of connected components
    return len(result)
def largestCCSize(conComp): #finds the max value of the various connected Component sizes
    result = set()
    for i in conComp: 
        result.add(len(i))
    return max(result)
def k2(conComp): #checks if a connected Component is length 2
    count = 0
    for i in conComp:
        if len(i) == 2:
            count+= 1
    return count
def k3(conComp):
    count = 0
    for i in conComp:
        if len(i) == 3: # checks if a connected component is length 3
            temp = list(i)
            edges = 0
            for j in range(len(temp)-1):#if so, checks if each word is a neighbor of every other word in the CC
                for k in range(j+1, len(temp)):
                    if isEdge(temp[j], temp[k]):
                        edges+=1    
            if edges == 3:
                count+=1
    return count
def k4(conComp):
    count = 0
    for i in conComp:
        if len(i) == 4:# checks if a connected component is length 4
            temp = list(i)
            edges = 0
            for j in range(len(temp)-1):#if so, checks if each word is a neighbor of every other word in the CC
                for k in range(j+1, len(temp)):
                    if isEdge(temp[j], temp[k]):
                        edges+=1    
            if edges == 6:
                count+=1
    return count
def nbrsOfFirst(myGrph, firstWord): #returns neighbors of the arg firstWord
    return " ".join(myGrph.get(firstWord))
def farthest(myGrph, first): #goes through all reachables from first
    parseMe = [first]
    dctSeen = {first: 0} #sets the value of the word as the level
    while parseMe: #goes through each item in parseMe
        node = parseMe.pop(0)
        for nbr in myGrph.get(node) : #gets neighbors of node
            if nbr not in dctSeen:
                parseMe += [nbr]
                dctSeen[nbr]= dctSeen.get(node)+1          
    return max(dctSeen, key=dctSeen.get) #returns the max value in the dictionary
def Path(myGrph, first, second):
    if first == second: #base case
        return [first]
    parseMe = [first]
    dctSeen = {first: 0}
    while parseMe: #goes through each item in parseMe
        node = parseMe.pop(0)    
        for nbr in myGrph.get(node): #gets neighbors of node
            if nbr not in dctSeen:
                if nbr == second:
                    dctSeen[nbr] = node
                    temp = nbr
                    output = []
                    while temp != first: #creates the path of steps to solve the puzzle
                        output.append(temp)
                        temp = dctSeen[temp]
                    output.append(first) #add start to output as while loop leaves it out
                    return " ".join(output[::-1]) #returns output in reverse because the while loop adds from goal to start
                parseMe += [nbr]
                dctSeen[nbr]=node
    return ""
if len(args)>1:
    firstWord = args[1]
    secondWord = args[2]
    contComp = makeCCs(output)
    print("Second degree word:", secondHighestDegree(output))
    print("Connected component size count:", findCCSizes(contComp))
    print("Largest component size:", largestCCSize(contComp))
    print("K2 Count:",k2(contComp))
    print("K3 Count:",k3(contComp))
    print("K4 Count:",k4(contComp))
    print("Neighbors:", nbrsOfFirst(output, firstWord))
    print("Farthest:", farthest(output, firstWord))
    print("Path:", Path(output, firstWord, secondWord))
d = time.process_time()
print(d)
#Tianhao Chen, pd. 4, 2023