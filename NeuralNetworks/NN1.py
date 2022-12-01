import sys;args = sys.argv[1:]
w = open(args[0],"r").read().splitlines()
# Tianhao Chen, pd.4
import math
weights = [] #actual weights for each layer
xfunct = args[1]
inputs = [i for i in args[2:]]
for i in w:weights.append(i.split())
layers = [] # number of nodes for each layer
for i in weights[::-1]: 
    if not layers: layers.append(len(i))
    else: layers.append(int(len(i)) // layers[-1])
layers = layers[::-1]
nodes = [[float(i) for i in inputs]] #numbering of the nodes, adds in the input values
counter = 1
for i in layers[1:]:
    temp = []
    for j in range(i):
        temp.append(counter)
        counter+=1
    nodes.append(temp)
def transferFunction(x, method):
    if method == 'T1': return x
    if method == 'T2':
        if x >= 0: return x
        else: return 0
    if method == 'T3': return 1/(1+math.exp((-x)))
    if method == 'T4': return 2 * transferFunction(x, 'T3') -1
values = [[float(i) for i in inputs]]
#print(values)
for layer in range(len(nodes)-1):
    inputs = []
    i = 0
    for node in nodes[layer+1]:  
        temp = 0
        for idx in range(len(values[layer])):
            print(values[layer][idx])
            temp += (values[layer][idx] * float(weights[layer][i]))
            i +=1
        inputs.append(transferFunction(temp, xfunct))
    print(inputs)
    values.append(inputs)
result = []
#print(weights)
for i in range(len(values[-1])):
    result.append(values[-1][i] * float(weights[-1][i]))
print(*result)
# Tianhao Chen, pd. 4, 2023