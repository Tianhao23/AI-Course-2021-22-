import sys;args = sys.argv[1:]
w = open(args[0],"r").read().splitlines()
# Tianhao Chen, pd.4
import random, math, time
values = w[0].split()
temp = values.index('=>')
inputs = values[0:temp]
#print(inputs)
outputs = values[temp+1:]
nodes = [[float(i) for i in inputs]+[1.0]]

if len(outputs) == 2: nodes.append([0.0 for i in range(3)]);nodes.append([0.0 for i in range(len(outputs))]);nodes.append([0.0 for i in range(len(outputs))])
else: nodes.append([0.0 for i in range(2)]);nodes.append([0.0 for i in range(len(outputs))]);nodes.append([0.0 for i in range(len(outputs))])
weights = [[random.uniform(-1,1) for i in range(len(nodes[0])*len(nodes[1]))]]
weights.append([random.uniform(-1,1) for i in range(len(nodes[-2])*len(nodes[-3]))]);weights.append([random.uniform(-1,1) for i in range(len(outputs))])#;weights.append([random.uniform(-1,1)  for i in range(len(outputs))])
#weights.append([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]);weights.append([2.0, 2.0]);weights.append([3.0])#;weights.append([.1])
#weights.append([1 for i in range(len(nodes[0])*2)]);weights.append([1 for i in range(2*len(nodes[-1]))]);weights.append([1 for i in range(len(outputs))])#;weights.append([random.uniform(-1,1)  for i in range(len(outputs))])
#weights = [[2.38289451722523, 2.0388304292006136, 1.3046592772124055, 1.5443617992755128, 1.6485179578295495, 2.934783435399877], [3.3299713656690066, 4.26688364998776], [3.6573730144103997]]
#weights =  [[-0.3383313638478169, -0.6348920118403429, 0.5868726017213988, 0.9670129869352289], [-0.6700928419360326, -0.3585999060403795], [-0.3773728974939812]]
def transferFunction(x):
    return 1/(1+math.exp((-x)))
def feedforward(nodes, weights):
    for layer in range(len(nodes)-2):
        inputs = []
        i = 0
        for node in nodes[layer+1]:  
            temp = 0
            for idx in range(len(nodes[layer])):
                temp += (nodes[layer][idx] * float(weights[layer][i]))
                i +=1
            inputs.append(transferFunction(temp))
        nodes[layer+1] = [*inputs]
    result = []
    for i in range(len(nodes[-2])):
        result.append(nodes[-2][i] * float(weights[-1][i]))
    return nodes, result
def hadamard(v1, v2):
    return [(i*j) for i,j in zip(v1,v2)]
def dotProd(v1, v2):
    return sum(hadamard(v1, v2))
def deriv(x):
    return x*(1-x)

def calcErrs(outErr, weights, nodes, outputs):
    errors = [outErr]
    temp = []
    for i in range(len(nodes[-2])):
        err = (float(outputs[i]) -nodes[-1][i]) * weights[-1][i] *deriv(nodes[-2][i])
        temp.append(err)
    errors.append(temp)
    for i in range(2, len(nodes)-1):
        temp = []
        for j in range(len(nodes[-i -1])): 
            err = deriv(nodes[-i-1][j]) * dotProd(errors[-1], [weights[-i][k] for k in range(j, len(weights[-i]), len(nodes[-i-1]))])
            temp.append(err)
        errors.append(temp)
    return errors[::-1]
    #from the second to last node going backwards:
        #for each node in that layer:
            #calc the error of that layer, which is the dot product of the deriv of node * 
            # dot product of layer+1 errors and list[weights of node index, +number of errors in +1 layer]
            #add to a list
        #add list to errors list  
def gradient(nodes, error, outputs, weights): #last layer should be different
    grads = []
    for layer in range(len(error)-1):
        gradlayer = []
        for node in error[layer]:
            for start in nodes[layer]:gradlayer.append(start*node)
        grads.append(gradlayer)
    grads.append([((float(t) - (x*w))*x) for t,x,w in zip(outputs, nodes[-2], weights[-1])])
    return grads
    #for each error starting on layer+1:
        #for each node in layer-1
            #calc negative graident by node*error
            #add to a list
        #add list to a list of list
def backProp(result, outputs, weights, nodes):
    outErr = [(float(i) - j) for i, j in zip(outputs, result)]
    errors = calcErrs(outErr, weights, nodes, outputs)
    #print(f'error: {errors}')
    grad = gradient(nodes, errors, outputs, weights)
    #print(f'gradient: {grad}')
    grad = [[j*.4 for j in i] for i in grad]
    newweights= [[i[k]+j[k] for k in range(len(i))] for i,j in zip(weights, grad)]
    return newweights
def output(nodes, weights):
    print(f'Layer Counts: {len(nodes[0])} {len(nodes[1])} {len(nodes[2])} {len(nodes[3])}' )
    #print(*weights, sep = '\n')
    print(*weights[0])
    print(*weights[1])
    print(*weights[2])

def epoch(weights, cycles):
    a = time.process_time()
    for j in range(cycles):
        counter = 0
        for i in w: 
            values = i.split()
            temp = values.index('=>')
            inputs = values[0:temp]
            outputs = values[temp+1:]
            nodes = [[float(i) for i in inputs]+[1.0]]

            if len(outputs) == 2: nodes.append([0.0 for i in range(3)]);nodes.append([0.0 for i in range(len(outputs))]);nodes.append([0.0 for i in range(len(outputs))])
            else: nodes.append([0.0 for i in range(2)]);nodes.append([0.0 for i in range(len(outputs))]);nodes.append([0.0 for i in range(len(outputs))])
            nodes, result = feedforward(nodes,weights)
            nodes[-1] = [*result]

            weights = backProp(result, outputs, weights, nodes)
            outErr = [(float(i) - j) for i, j in zip(outputs, result)]
            totalerr = .5 * sum(i**2 for i in outErr)
            #totalerr = .5 * (i**2 for i in error)
            if totalerr < .001 :
                counter +=1
                if counter == len(w) : 
                    b = time.process_time()
                    if b-a <28.5: 
                        output(nodes, weights)
                        return
            if j % 1000 == 0 and j!= 0:
                if totalerr > .25:
                    weights = [[random.uniform(-1,1) for i in range(len(nodes[0])*len(nodes[1]))]]
                    weights.append([random.uniform(-1,1) for i in range(len(nodes[-2])*len(nodes[-3]))]);weights.append([random.uniform(-1,1) for i in range(len(outputs))])#;weights.append([random.uniform(-1,1)  for i in range(len(outputs))])
        b = time.process_time()
        if b-a <28.5: 
            output(nodes, weights)
epoch(weights, 1000000)
# print(f'input {inputs}')
# print(f'outputs {outputs}')
# print(f'orginal weights {weights}')
# nodes, result = feedforward(nodes,weights)
# nodes[-1] = [*result]
# #print(nodes)
# weights = backProp(result, outputs, weights, nodes)
# output(nodes, weights)

#update weights by multiplying the gradient by a factor of 0.01 to .1, then adding elements to corresponding weight index
# Tianhao Chen, pd. 4, 2023