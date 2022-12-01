import sys;args = sys.argv[1:]
# Tianhao Chen, pd.4
import math
length = int(args[0])
data = {i: [0,True, True, True, True] for i in range(length)} #[reward, can go north, can go south, can go east, can go west]
rewards = [0 for i in range(length)]
numbers = '0123456789'
map = ['.' for i in range(length)]
gWidth, gHeight, reward, task = 0, 0, 12, ''
def inputs():
    global gWidth, gHeight, reward, data, task
    for input in args[1:]:
        if input in numbers:
            gWidth = int(input)
            gHeight = int(length / gWidth)
        elif input == args[1]:
            for i in range(1, math.floor(math.sqrt(length))+1): #creating the dimensions to make the puzzle as square as possible
                if length % i ==0: gHeight, gWidth = i, length//i
        else:
            if input[0] == 'R':
                if ':' in input:
                    if input[1] == ':': reward = int(input[2:])
                    else: 
                        data[int(input[1:input.index(':')])][0], rewards[int(input[1:input.index(':')])] =int(input[input.index(':')+1:]), int(input[input.index(':')+1:])
                        
                else:data[int(input[1:])][0], rewards[int(input[1:])] = reward, reward

            if input[0] == 'B':
                if 'N' in input or 'S' in input or 'E' in input or'W' in input:
                    digits = '1234567890'
                    index = 1
                    while input[index] in digits: index +=1
                    if 'N' in input:
                        data[int(input[1:index])][1] = False if data[int(input[1:index])][1] == True else True
                        if int(input[1:index])-gWidth > 0: 
                            data[int(input[1:index])-gWidth][2] = False if data[int(input[1:index])-gWidth][2] == True else True
                    if 'S' in input : 
                        data[int(input[1:index])][2] = False if data[int(input[1:index])][2] == True else True
                        if int(input[1:index])+gWidth < length:
                            data[int(input[1:index])+gWidth][1] = False if data[int(input[1:index])+gWidth][1] == True else True
                    if 'E' in input :
                        data[int(input[1:index])][3] = False if data[int(input[1:index])][3] == True else True
                        
                        if (int(input[1:index])+1) %gWidth > (int(input[1:index])) %gWidth: data[int(input[1:index])+1][4] = False if data[int(input[1:index])+1][4] == True else True
                    if 'W' in input:
                        data[int(input[1:index])][4] = False if data[int(input[1:index])][4] == True else True
                        
                        if (int(input[1:index])-1) %gWidth < (int(input[1:index])) %gWidth: data[int(input[1:index])-1][3] = False if data[int(input[1:index])-1][3] == True else True
                else:
                    for i in range(1, 5):
                        data[int(input[1:])][i] = False if data[int(input[1:])][i] == True else True
                        if i == 1:
                            if int(input[1:])-gWidth > 0: data[int(input[1:])-gWidth][2] = False if data[int(input[1:])-gWidth][2] == True else True
                        if i ==2:
                           if int(input[1:])+gWidth < length: data[int(input[1:])+gWidth][1] = False if data[int(input[1:])+gWidth][1] == True else True
                        if i == 3:
                            if (int(input[1:])+1) %gWidth > (int(input[1:])) %gWidth: data[int(input[1:])+1][4] = False if data[int(input[1:])+1][4] == True else True
                        if i == 4:
                            if (int(input[1:])-1) %gWidth < (int(input[1:])) %gWidth: data[int(input[1:])-1][3] = False if data[int(input[1:])-1][3] == True else True
            if input == 'G0': task = G0
            if input == 'G1' : task = G1

def G0(start, goal):
    global map
    dir = 'NSEW'
    if start == goal:
        return
    parseMe = [start]
    dctSeen = {start}
    while parseMe: #goes through each item in parseMe
        node = parseMe.pop(0)
        nbrs = [node+gWidth, node-gWidth, node+1, node-1]
        for i in range(len(nbrs)):
            minDis = 10000000
            idx = 0
            if data[node][i+1] == True:
                parseMe += [nbrs[i]]
                dctSeen.add(nbrs[i])
                dis = math.dist([node], nbrs[i])
                if dis < minDis: 
                    minDis = dis
                    idx = i
        
        map[nbrs[idx]] += dir[idx]
        #calculate neigbors that get closer to reward


        #for nbr in range(len(nbrs)): #gets neighbors of node
            #if nbr not in dctSeen and nbrs[nbr] <length and nbrs[nbr]%gWidth < gWidth :

                # if nbr == goal:
                #     dctSeen[nbr] = node
                #     temp = nbr
                #     output = []
                #     while temp != start: #creates the path of steps to solve the puzzle
                #         output.append(temp)
                #         temp = dctSeen[temp]
                #     output.append(start) #add start to output as while loop leaves it out
                #     steps = len(output)-1
                #     return output[::-1] #returns output in reverse because the while loop adds from goal to start
                #parseMe += [nbrs[nbr]]
                #dctSeen[nbr]=node
    return []
def G1():
    return 2
def output(map):
    output = ''
    for i in range(0,len(map),gWidth): #go through each index, incrementing by height
        for j in range(gWidth): #adds a row of elements, separated by a space
            output+=map[i+j] + ' '
        output += '\n' #new line
    print(output)
    print('======')
inputs()
print(gWidth, gHeight, data, reward)
print(rewards)
#print(rewards.index(max(rewards)))
output(map)
# Tianhao Chen, pd. 4, 2023