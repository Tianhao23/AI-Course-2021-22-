import sys;args = sys.argv[1:]
w = open(args[0],"r").read().splitlines()
# Tianhao Chen, pd.4
import math
temp = []
valid = '-.1234567890 '
for i in w:
    x = ''
    for j in i:
        if j in valid:x+=j
    temp.append(x.split())
while [] in temp: temp.remove([])
eq = args[1]
if '=' in eq:eq = eq.replace('=', '')
if '<' in eq : ineq = '<' 
else: ineq = '>'
idx = eq.find(ineq) 
radius = float(eq[idx+1:])     
r = math.sqrt(radius)
#print(r)
#print(temp)
for i in range(len(temp[0])):
    if i%2 == 0:  temp[0][i] = str(float(temp[0][i])/ r)
#print(temp)
def createstruct(weights):
    strct = [2]
    for i in weights: strct.append(int(len(i)/strct[-1]))
    #print(strct)
    strct[0] = strct[0]+1
    for i in range(1, len(strct)-1):strct[i] = strct[i] * 2
    return strct + [1]#double check structure
def output(weights, strct):
    print(f'Layer Counts: {strct}')#print the actual layer counts
    for i in weights:print(*i)
def createweights(strct, weights):
    newweights = []
    temp = []
    counter = 0
    for i in range(0, int(strct[1]/2)):
        for j in range(strct[0]):
            if j == 1: temp.append('0')
            else:
                temp.append(weights[0][counter])
                counter +=1
    counter = 0
    for i in range(int(strct[1]/2), int(strct[1])):
        for j in range(strct[0]):
            if j != 0: 
                temp.append(weights[0][counter])
                counter +=1
            else: temp.append('0')
        #print(temp)
    newweights.append(temp)
    for i in range(len(strct)-4):
        #print(i)
        temp = []
       # print(strct[i+2])
        for j in range(strct[i+2]):
           # print(j)
            for k in range(strct[i+1]):
               # print(counter)W
                if j == 0 and k == 0: 
                    counter = 0
                    temp.append(weights[i+1][counter])
                    counter+=1
                elif j < strct[i+2]/2 and k < strct[i+1]/2 :
                    temp.append(weights[i+1][counter])
                    counter+=1
                elif j == strct[i+2]/2 and k== strct[i+1]/2  :
                    counter = 0
                    temp.append(weights[i+1][counter])
                    counter+=1
                elif ((j > strct[i+2]/2 or j == strct[i+2]/2)  and k > strct[i+1]/2) or (j > strct[i+2]/2 and k == strct[i+1]/2):
                    temp.append(weights[i+1][counter])
                    counter+=1
                else:
                    temp.append('0')

        newweights.append(temp)       
        #for j in i:
        #print(strct[strct.index(i)-1])
    temp = []
    for i in range(strct[-3]):
        if ineq == '<': x = str(-float(weights[-1][0]))
        else: x = weights[-1][0]
        temp.append(x)
    newweights.append(temp)
   # x = str((1+math.exp(1))/ (2*math.exp(1)))
    if ineq == '>': x = str((1+math.exp(1))/ (2*math.exp(1)))
    else: x = '1.85914'
    newweights.append([x])
    return newweights

strct = createstruct(temp)
#print(strct)
updatedweights = createweights(strct, temp)
output(updatedweights, strct)
# Tianhao Chen, pd. 4, 2023