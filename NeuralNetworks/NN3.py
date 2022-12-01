import sys;args = sys.argv[1:]
import random, math
# Tianhao Chen, pd.4
#print(args[0])
w = args[0]
if '=' in w:w = w.replace('=', '')
if '<' in w : ineq = '<' 
else: ineq = '>'
index = args[0].find(ineq) 
radius = w[index+1:]
#print(radius)
#print(index)
def generateTrainingSets(radius, ineq):
    trainingset = {}
    for i in range(1000):
        x, y = random.uniform(-1.5,1.5), random.uniform(-1.5,1.5)
        r = x**2 + y**2
        if ineq == '<':
            if r < float(radius): trainingset[x,y] = 1
            else: trainingset[x,y] = 0
        else:
            if r > float(radius):trainingset[x,y] = 1
            else: trainingset[x,y] = 0 
    return trainingset
trainingset = generateTrainingSets(radius,ineq)
#print(trainingset)
nodes = [[0.0, 0.0, 1.0], [0.0 for i in range(5)], [0.0 for i in range(3)], [0.0],[0.0]]
weights = [[random.uniform(-1,1) for i in range(len(nodes[0])*len(nodes[1]))], [random.uniform(-1,1) for i in range(len(nodes[1])*len(nodes[2]))], [random.uniform(-1,1) for i in range(len(nodes[2])*len(nodes[3]))],[random.uniform(-1,1) for i in range(len(nodes[3])*len(nodes[4]))]]


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
def gradient(nodes, error, outputs, weights): #last layer should be different
    grads = []
    for layer in range(len(error)-1):
        gradlayer = []
        for node in error[layer]:
            for start in nodes[layer]:gradlayer.append(start*node)
        grads.append(gradlayer)
    grads.append([((float(t) - (x*w))*x) for t,x,w in zip(outputs, nodes[-2], weights[-1])])
    return grads
def backProp(result, outputs, weights, nodes):
    outErr = [(float(i) - j) for i, j in zip(outputs, result)]
    errors = calcErrs(outErr, weights, nodes, outputs)
    #print(f'error: {errors}')
    grad = gradient(nodes, errors, outputs, weights)
    #print(f'gradient: {grad}')
    grad = [[j*.1 for j in i] for i in grad]
    newweights= [[i[k]+j[k] for k in range(len(i))] for i,j in zip(weights, grad)]
    return newweights
def output(nodes, weights):
    print(f'Layer Counts: {len(nodes[0])} {len(nodes[1])} {len(nodes[2])} {len(nodes[3])} {len(nodes[4])}' )
    print(*weights, sep = '\n')
    # print(*weights[0])
    # print(*weights[1])
    # print(*weights[2])

def epoch(weights, cycles):
   # a = time.process_time()
    for j in range(cycles):
        counter = 0
        for i in trainingset: 
            inputs, outputs = i, [trainingset[i]]
            #print(inputs,outputs)
            nodes = [[float(i) for i in inputs]+[1.0],[0.0 for i in range(5)], [0.0 for i in range(3)], [0],[0]]
            nodes, result = feedforward(nodes,weights)
            nodes[-1] = [*result]

            weights = backProp(result, outputs, weights, nodes)
            outErr = [(float(i) - j) for i, j in zip(outputs, result)]
            totalerr = .5 * sum(i**2 for i in outErr)

            if totalerr <= .001 :
                counter +=1
                if counter == len(trainingset) : 
                   # b = time.process_time()
                    #if b-a <28.5: 
                        output(nodes, weights)
                        return
            if j % 1000 == 0 and j!= 0:
                if totalerr > .25:
                    weights = [[random.uniform(-1,1) for i in range(len(nodes[0])*len(nodes[1]))], [random.uniform(-1,1) for i in range(len(nodes[1])*len(nodes[2]))], [random.uniform(-1,1) for i in range(len(nodes[2])*len(nodes[3]))],[random.uniform(-1,1) for i in range(len(nodes[3])*len(nodes[4]))]]
       # b = time.process_time()
        #if b-a <28.5: 
        output(nodes, weights)
epoch(weights, 1000000)
# Tianhao Chen, pd. 4, 2023