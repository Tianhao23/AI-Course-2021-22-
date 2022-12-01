import sys; args = sys.argv[1:]
c1 = [{0,1,2,6,7,8}, {2,3,4,8,9,10},{5,6,7,12,13,14}, {7,8,9,14,15,16},{9,10,11,16,17,18}, {13,14,15,19,20,21}, {15,16,17,21,22,23}]
c2 = [{0,1,2,6,7,8}, {2,3,4,8,9,10},{5,6,7,12,13,14}, {7,8,9,14,15,16},{9,10,11,16,17,18}, {13,14,15,19,20,21}, {15,16,17,21,22,23}, {0,1,2,3,4}, {5,6,7,8,9,10,11}, {12,13,14,15,16,17,18}, {19,20,21,22,23}, {12,5,6,0,1},{19,13,14,7,8,2,3},{20,21,15,16,9,10,4},{22,23,17,18,11},{3,4,10,11,18},{1,2,8,9,16,17,23},{0,6,7,14,15,21,22}, {5,12,13,19,20}]
s1 = {'1','2','3','4','5','6'}
s2 = {'1','2','3','4','5','6','7'}
def isInvalid(pzl, constraint, symbols): #isValid but with constraints
    for ct in constraint:
        checked = set()
        for idx in ct:
            if pzl[idx] in checked: # if the symbol is in checked, then the puzzle is invalid
                return True
            if pzl[idx] in symbols: #if the symbol is a symbol that can be used, add it to checked
                checked.add(pzl[idx])
def isFilledOut(pzl,symbols):#checks if every index in puzzle has a legal symbol
    for elm in pzl: 
        if elm not in symbols:
            return False
    return True
def possible(pzl, pos, constraint, symbols): #calculates the possible number of symbols you can fill in an index
    filled = set()
    for node in constraint:
            if pos in node:
                if pzl[pos] != '.' and pzl[pos] not in filled:
                    filled.add(pzl[pos])
    return symbols - filled
    #return filled
def createDots(pzl,constraint, symbols): #calculates a dictonary of all the dots and possible number of symbols
    dotD = {}
    pos = 0
    dot = pzl.find('.',pos)
    while dot !=-1:
        choices = possible(pzl, dot, constraint, symbols)
        dotD[dot] = choices #dot index as key, choices as value
        pos = dot+1
        dot = pzl.find('.',pos)    
    return dotD
def bDot(dots):
    best = 0
    lowest = 20
    for i in dots:
        x = len(dots[i])
        if x < lowest:
            lowest = x
            best = i
    return best
def bF(pzl, constraint, symbols, dots):
    if isInvalid(pzl, constraint, symbols): return ""
    if isFilledOut(pzl,symbols): return pzl
    change = bDot(dots)
    #setofChoices = symbols
    for choice in dots.pop(change): #for every symbol you can use, add it to the first place needed to add a symbol
            dot2 = {i:dots[i] for i in dots}
            for node in constraint:
                if change in node:
                    for idx in node:
                        if idx in dot2:
                            dot2[idx] = dot2[idx] - {choice}
            #change = pzl.index(".")
            subPzl = pzl[0:change] + choice+pzl[change+1:]
            pSol = bF(subPzl, constraint, symbols, dot2)
            if pSol: return pSol
    return ""
if len(args) == 2:
    
    if args[0] == "B":
        dots = createDots(args[1], c2, s2)
        solution = bF(args[1], c2, s2, dots)
    if args[1] == "B":
        dots = createDots(args[0], c2, s2)

        solution = bF(args[0], c2, s2, dots)
else:
    dots = createDots(args[0], c1, s1)
    solution = bF(args[0], c1,s1, dots)
    #print(dots)
if solution:
    print(solution)
else:
    print("No solution possible")
#print(' ',solution[0], solution[1], solution[2],solution[3],solution[4])
#print(solution[5], solution[6], solution[7],solution[8],solution[9],solution[10],solution[11])
#print(solution[12], solution[13], solution[14],solution[15],solution[16],solution[17],solution[18])
#print(' ',solution[19], solution[20], solution[21],solution[22],solution[23])