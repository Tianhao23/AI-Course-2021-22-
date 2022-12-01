import sys; args = sys.argv[1:]
# Tianhao Chen, pd.4
import time, math, random
from math import log, pi, acos, sin, cos, tan, log10, floor
from tkinter import *

distance = 0



Root = Tk()
Root.title("Railroad Astar(Red is openSet, Blue is closedSet, Green is path)")
canvas = Canvas(Root, background = "black", width = 1920, height = 1080)
openSet = []
map = PhotoImage(file = "US2.png")
canvas.create_image(485,395, image = map) #use for create_Line
Root.geometry("970x790") #sets the geometry of the tkinter
canvas.pack(fill=BOTH, expand =1)

#nodes.txt file had latitude first then longitude

   
def remove(): #removes the lowest value
    global openSet
    if len(openSet) == 1: #if there's only one element, remove it
        return openSet.pop(0)
    else:
        swap(0, len(openSet)-1)#swap the smallest with the last element, so .pop() can save time
        result = openSet.pop()
        heapDown(0) #calls heapDown to sort openSet again
        return result #returns that node

def add(f, stn, g, parent):
    global openSet
    openSet.append((f, stn, g, parent)) #adds new node to openSet, then call heapUp
    heapUp(len(openSet)-1) 

def heapUp(k):
    global openSet
    parent = (k)//2 #calculates the parent index
    if openSet[k]<openSet[parent]: #if current value is less than its parent, then it needs to move up
        swap(k, parent)
        heapUp(parent)
   
def swap(x,y): #swapping the "_" and its neighbor
    global openSet
    openSet[x], openSet[y] = openSet[y], openSet[x]
  
   
def heapDown(k): #used in remove
    global openSet
    leftChild = 2*k #finds the two children index
    rightChild = 2*k+1
    check = openSet[k][0] #current value
    if  leftChild < len(openSet) -1: #checks if leftChild index is too large, meaning k has no children
        if rightChild > len(openSet): #if right child is too large index, leftChild becomes default
            newC = leftChild
        elif openSet[leftChild][0] > openSet[rightChild][0]: #checks which children is smaller, setting that as the 
            newC = rightChild
        else:
            newC = leftChild 
        if openSet[newC][0] < check: #check if there's a need to swap. If child is less than current value, then it needs to be higher up
            swap(newC, k)
            heapDown(newC)        
#set up the files
temp = open("rrNodeCity.txt", "r").read().splitlines()
cityName = {}
nameToID = {}#for taking in arguments
for line in temp: #formats the file into a dict, where each id has a value city name associated
    idx = line.index(" ")
    cityName[line[0:idx]] = line[idx+1:]
    nameToID[line[idx+1:]] = line[0:idx]
temp = open("rrEdges.txt", "r").read().split()
edges = {}
for i in range(0, len(temp), 2): #creates the neighbors for each station. File only has edge in one way, so you need to add both stations of each edge as a key to the dict
    node1 = temp[i]
    node2 = temp[i+1]
    if node1 not in edges:
        edges[node1] = []
    edges[node1] += [node2]
    if node2 not in edges:
        edges[node2] = []
    edges[node2] += [node1]

temp = open("rrNodes.txt", "r").read().splitlines()
stations = {}
for line in temp: #creating the data stored in stations
    idx = line.index(" ") #first instance of " ", separates id from latitude
    minus = line.index("-") #separates latitude from longitude
    node = line[0:idx]
    if node not in stations:
        stations[node] = [float(line[idx+1:minus-1]), float(line[minus:])]

def drawLine(canvas, lat1, long1, lat2, long2, col): #draws the lines for the tkinter
   lat1, long1, lat2, long2 = float(lat1), float(long1), float(lat2), float(long2)   
   #canvas.create_line(long1, 800-lat1, long2, 800-lat2, fill=col, width = 1)
   canvas.create_line((((float(long1))+180)*(1920/360))*2.25-560, 
   ((1080/2)-(1080*(log(tan((pi/4)+(((float(lat1))*pi/180)/2))))/(2*pi)))*3.74-1141, #decreasing value makes it go down
   (((float(long2))+180)*(1920/360))*2.25-560, ((1080/2)-(1080*(log(tan((pi/4)+(((float(lat2))*pi/180)/2))))/(2*pi)))*3.74-1141, fill=col, width=2) #used for scaling the coordinates and draws them


  
def gcd(lat1,long1, lat2,long2): #used to calculate great circle distance
    #
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees

    # if (and only if) the input is strings
    # use the following conversions

    lat1  = float(lat1)
    long1  = float(long1)
    lat2  = float(lat2)
    long2 = float(long2)
    #
    R   = 3958.76 # miles = 6371 km
    #
    lat1 *= pi/180.0
    long1 *= pi/180.0
    lat2 *= pi/180.0
    long2 *= pi/180.0
    #
    # approximate great circle distance with law of cosines
    #
    return acos( sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(long2-long1) ) * R


def AStar(start, goal, Root):
    global distance, openSet
    if start == goal: #if no moves is required
        return start
    add(gcd(stations[start][0], stations[start][1], stations[goal][0], stations[goal][1]), start, 0, start) # a list of tuples containing f, pzl, g, and parent

    closedSet = {}
    counter = 0
    while openSet:
        f, stn, g, parent = remove()
        if stn in closedSet: continue
        closedSet[stn] = parent
        lat1 = (stations[parent][0]-9)/45 * 600
        long1 = (stations[parent][1]+134)/70*830
        lat2 = (stations[stn][0]-9)/45 * 600
        long2 = (stations[stn][1]+134)/70*830
        drawLine(canvas, lat1, long1, lat2, long2, "blue")

        if stn == goal:
            distance = g
            temp = stn
            output = []
            while temp != start: #creates the path of steps to solve the puzzle
                output.append(temp)
                temp = closedSet[temp]
            output.append(start) #add start to output as while loop leaves it out
            return output[::-1] #returns output in reverse because the while loop adds from goal to start
        for nbr in edges[stn]:
            if nbr in closedSet: 
                lat1 = (stations[stn][0]-9)/45 * 600
                long1 = (stations[stn][1]+134)/70*830
                lat2 = (stations[nbr][0]-9)/45 * 600
                long2 = (stations[nbr][1]+134)/70*830
                drawLine(canvas, lat2, long2, lat1, long1, "blue")
                continue
            newG =  gcd(stations[stn][0], stations[stn][1], stations[nbr][0], stations[nbr][1])
            #print(stations[nbr][0], stations[nbr][1], stations[goal][0], stations[goal][1])
            if nbr != goal:

                newEst = (g+newG) + gcd(stations[nbr][0], stations[nbr][1], stations[goal][0], stations[goal][1])
            else:
                newEst = g+newG
            add(newEst, nbr, g+newG, stn)
            nlat1 = (stations[stn][0]-9)/45 * 600
            nlong1 = (stations[stn][1]+134)/70*830
            nlat2 = (stations[nbr][0]-9)/45 * 600
            nlong2 = (stations[nbr][1]+134)/70*830
            drawLine(canvas, nlat1, nlong1, nlat2, nlong2, "red")

        counter+= 1
        if counter == 500:
            Root.update()
            counter = 0
def drawPath(path, canvas):
    for i in range(len(path)-2):
        stn1 = path[i]
        stn2 = path[i+1]
        lat1 = (stations[stn1][0])
        long1 = (stations[stn1][1])
        lat2 = (stations[stn2][0])
        long2 = (stations[stn2][1])
        drawLine(canvas, lat1, long1, lat2, long2, "Green")
        Root.update()
def createPath(path):
    output = []
    for city in path:
        if city in cityName: #uses city names if possible
            output.append(cityName[city])
        else:
            output.append(city)
    return output

if len(args) == 3: #processes various types of inputs from terminal
    start = args[0]
    if not start in nameToID and not start.isdigit():
        start += " "+ args[1]
        end = args[2]
    else:
        end = args[1] + " " +args[2]
elif len(args) == 4:
    start = args[0] + " "+args[1]
    end = args[2] + " "+args[3]
else:
    start = args[0]
    end = args[1]
if not start.isdigit():
    startId = nameToID[start]
else:
    startId = start
if not end.isdigit():
    endId = nameToID[end]
else:
    endId = end
solution = AStar(startId, endId, Root)
pathWName = createPath(solution)
length = round(distance, 7-int(floor(log10(abs(distance))))-1) #rounds the distance to 7 sig figs
drawPath(solution, canvas)
print("The path the train takes to get from", start, "to", end, "is", pathWName) #outputs for the lab
print("The train goes through", len(solution), "stations to get to the final destination")
print("The distance travelled is", length, "miles")
Root.mainloop()
# Tianhao Chen, pd. 4, 2023