import sys; args = sys.argv[1:]
# Tianhao Chen,pd.4

height = int(args[0][0:args[0].index('x')]) # height parameter for puzzle
width = int(args[0][args[0].index('x')+1:]) #width parameter for puzzle
Blocks = int(args[1]) #number of blocking squares
#dct = args[2] #for xword 2
seedstring = []
BLOCKCHAR, OPENCHAR = "#" , "-"
if len(args) > 2: seedstring += args[2:]
length = width*height
pzl = [OPENCHAR for i in range(length)]
rows, columns = [[x+width*y for x in range(width)] for y in range(height)], [[x*width + y for x in range(height)]for y in range(width)]
#pzl = OPENCHAR*(height*width)
def printBoard(pzl, rows): #prints a 2-D display of othello board
    for row in rows:
        for i in row:print(pzl[i], end = " ")
        print()
def addseedstring(vert, horiz, vh, word, pzl): #adds the seedstring into the puzzle
    if vh.upper() == 'V':
        for i in range(len(word)): pzl[columns[horiz][vert+i]] = word[i] #goes down the column starting at vert index
    else:
        for i in range(len(word)): pzl[rows[vert][horiz]+i] = word[i]#goes across the row starting at horiz index
    return pzl
def fillseedstring(pzl, seedstring): #adds every seedstring into the puzzle
    for i in seedstring:
        vh, vert, startH, number = i[0], i[1:i.index('x')], i.index('x')+ 1, '0123456789'
        if startH == len(i) - 1: horiz, word = i[startH:], '#'
        else:
            endH = startH + 2 if i[startH + 1] in number else startH +1
            horiz, word = i[startH: endH], i[endH:]
        pzl = addseedstring(int(vert), int(horiz), vh, word, pzl)
    return pzl
def makeSymmetric(pzl):#once the seedstrings are added in, add blocking squares to ensure that board is symmetic
    # for i, c in enumerate(pzl):
    #     if c == BLOCKCHAR:
    #         pzl[len] = 
    loc = []
    for i in range(len(pzl)):
        if pzl[i] == BLOCKCHAR: loc.append(i) #store the current position of each blocking square
    pzl = pzl[::-1] #rotate puzzle 180 degrees
    for i in loc: pzl[i] = BLOCKCHAR #add blocking squares to each position previously stores
    return pzl[::-1] #rotate the puzzle again

def boundaryblocks(pzl):#adds blocks that are <3 away from boundary
    for row in rows: #for every row
        prevblock = ''
        for i, c in enumerate(row):
            if prevblock != '' and pzl[c] == BLOCKCHAR and i - prevblock <4:
                for k in range(row[prevblock], row[i]): pzl[k] = BLOCKCHAR
            if pzl[c] == BLOCKCHAR: prevblock = i

            if pzl[c] == BLOCKCHAR and i < 3: #if it's less than 3 away from left border, convert all to blocking squares
                for k in range(row[0],row[i]): pzl[k] = BLOCKCHAR
            if pzl[c] == BLOCKCHAR and (len(row)-1 - i)<3: #if it's less than 3 away from right border
                for k in range(c,row[-1]+1):pzl[k] = BLOCKCHAR #this part may be uneccesary due to symmetry
    for col in columns:
        prevblock = ''
        for i,c in enumerate(col):
            if prevblock != '' and pzl[c] == BLOCKCHAR and i - prevblock <4:
                for k in range(col[prevblock], col[i], width): pzl[k] = BLOCKCHAR
            if pzl[c] == BLOCKCHAR: prevblock = i

            if pzl[c] == BLOCKCHAR and i < 3: #less than 3 from top
                for k in range(col[0],col[i], width):pzl[k] = BLOCKCHAR
            if pzl[c] == BLOCKCHAR and (len(col)-1 - i)<3: #less than 3 from bottom
                for k in range(c,col[-1]+1, width):pzl[k] = BLOCKCHAR
    # for row in rows: #for every row
    #     prevblock = ''
    #     for i, c in enumerate(row):
    #         if prevblock != '' and pzl[c] == BLOCKCHAR and i - prevblock <4:
    #             for k in range(row[prevblock], row[i]): pzl[k] = BLOCKCHAR
    #         if pzl[c] == BLOCKCHAR: prevblock = i
    return pzl

if seedstring: pzl = fillseedstring(pzl,seedstring)
pzl = makeSymmetric(pzl)
pzl = boundaryblocks(pzl)

#remainingBlocks = Blocks - str(pzl).count('#')
def addBlocks(pzl):
    letterCount = len(pzl) - pzl.count(OPENCHAR) - pzl.count(BLOCKCHAR)
    temp = [*pzl]
    for i in range(len(pzl)):
        if temp[i] == OPENCHAR:
            temp[i] = BLOCKCHAR
            temp = boundaryblocks(temp)
            temp = makeSymmetric(temp)
            if len(temp) - temp.count(OPENCHAR) - temp.count(BLOCKCHAR) !=letterCount: temp = [*pzl]
            if temp.count("#") > Blocks :temp = [*pzl]
            if temp.count("#") <= Blocks:pzl = [*temp]
            if temp.count("#") == Blocks: return pzl
    return pzl
#def addBlocks(pzl):
#     letterCount = len(pzl) - pzl.count(OPENCHAR) - pzl.count(BLOCKCHAR)
#     temp = [*pzl]
#     for i in range(len(pzl)):
#         if temp[i] == OPENCHAR:
#             temp[i] = BLOCKCHAR
#             temp = boundaryblocks(temp)
#             temp = makeSymmetric(temp)
#             if length != Blocks and temp.count(BLOCKCHAR)!=length:
#                 seenSpaces = connectedChars(temp, temp.index(OPENCHAR), set())
#                 if len(seenSpaces) != length - temp.count(BLOCKCHAR): temp = [*pzl] 
#             if len(temp) - temp.count(OPENCHAR) - temp.count(BLOCKCHAR) !=letterCount: temp = [*pzl]
#             if temp.count("#") > Blocks :temp = [*pzl]
#             if temp.count("#") <= Blocks:pzl = [*temp]
            
#             if temp.count("#") == Blocks: return pzl 
#     return pzl
pzl = addBlocks(pzl)
printBoard(''.join(pzl), rows)
# Tianhao Chen, pd. 4, 2023
#speed up: symmetric is useless
#add a block, check the symmertical location