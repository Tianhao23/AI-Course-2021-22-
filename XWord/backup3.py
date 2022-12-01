import sys; args = sys.argv[1:]
x = open(args[0],"r").read().splitlines()
# Tianhao Chen,pd.4
args.pop(0)
height = int(args[0][0:args[0].index('x')]) # height parameter for puzzle
width = int(args[0][args[0].index('x')+1:]) #width parameter for puzzle
Blocks = int(args[1]) #number of blocking squares


seedstring = []
BLOCKCHAR, OPENCHAR = "#" , "-"
if len(args) > 2: seedstring += args[2:]
length = width*height
pzl = [OPENCHAR for i in range(length)]
rows, columns = [[x+width*y for x in range(width)] for y in range(height)], [[x*width + y for x in range(height)]for y in range(width)]
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
    return pzl
def neighbors(index): #finding and returning the neighbors based on index
    nbrs = []
    #index cases
    if index % width != width-1:nbrs.append(index+1)
    if index % width != 0:nbrs.append(index-1)
    if 0<=index<= (length-width)-1:nbrs.append(index+width)
    if width<=index <=length-1:nbrs.append(index-width)
    return nbrs

def connectedChars(pzl, idx, seen):
    nbrs = neighbors(idx) #create a list of neighbors of that index
    seen.add(idx) #add the index if it has neighbors
    for i in nbrs: # for every neighbor, if it's not a blocking square, run connectedChars again
        if pzl[i] != BLOCKCHAR and i not in seen: seen = connectedChars(pzl, i, seen)
    return seen

if seedstring: pzl = fillseedstring(pzl,seedstring)
pzl = makeSymmetric(pzl)
pzl = boundaryblocks(pzl)
def bF(pzl, index, ltrct): #update, instead of returning the puzzle, add it to a set
    if length != Blocks and pzl.count(BLOCKCHAR)!=length: #if not all non-blocking squares are connected
            seenSpaces = connectedChars(pzl, pzl.index(OPENCHAR), set())    
            if len(seenSpaces) != length - pzl.count(BLOCKCHAR): return ''           
    if len(pzl) - pzl.count(OPENCHAR) -pzl.count(BLOCKCHAR) !=ltrct: return '' # if letters were changed
    if pzl.count("#") > Blocks :return ''
    if pzl.count("#") == Blocks: return pzl 
    for i in range(index, len(pzl)): #starting from this index
        if pzl[i] == OPENCHAR: # if it's an '-'
            subpzl = [*pzl] 
            subpzl[i] = BLOCKCHAR
            subpzl = makeSymmetric(boundaryblocks(subpzl))
            pSol = bF(subpzl, i+1, ltrct) #run brute force on updated puzzle
            if pSol: return pSol
    return ""
def checkFill(seen, openSpaces, pzl):
    fill = openSpaces - seen #to fill squares is the openspaces minus the seen spaces
    answer = [*pzl] #fill in the fill set
    for i in fill: answer[i] = BLOCKCHAR
    answer= boundaryblocks(answer)
    answer = makeSymmetric(answer)
    if answer.count(BLOCKCHAR) > Blocks: #if the number of blocks is too great
        fill = seen #try the stuff to fill to be seen
        answer = [*pzl]
        for i in fill: answer[i] = BLOCKCHAR
        answer= boundaryblocks(answer)
        answer = makeSymmetric(answer)
    return answer
letterCount = len(pzl) - pzl.count(OPENCHAR) - pzl.count(BLOCKCHAR)
seenSpaces = connectedChars(pzl, pzl.index(OPENCHAR), set())
openSpaces = {i for i in range(length) if pzl[i] == OPENCHAR}
answer = checkFill(seenSpaces, openSpaces, pzl)
seenSpaces = connectedChars(answer, answer.index(OPENCHAR), set())
openSpaces = {i for i in range(length) if pzl[i] == OPENCHAR}
if seenSpaces != openSpaces: answer = checkFill(seenSpaces, openSpaces, answer)

answer = bF(answer, 0, letterCount)

#printBoard(''.join(answer), rows)
#print()
def isWord(word):
    valid = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPLKJHGFDSAMNBVCXZ'
    for char in word:
        if char not in valid: return False
    return True
bucketOfWords = [[]for i in range(50)]
copy = [[]for i in range(50)]
for i in x:
    if isWord(i) and len(i) >=3:
        bucketOfWords[len(i)].append(i)
        copy[len(i)].append(i)
def grabWord(trackletters, length):
    for i in range(len(copy[length])):
        valid = True
        for k in trackletters:   
            if copy[length][i][k].lower() !=trackletters[k].lower():
                valid = False
        if valid: 
            return copy[length].pop(i)
    return copy[length].pop(0)
def findword(index, pzl):
    valid = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPLKJHGFDSAMNBVCXZ'
    col = index % width
    length = 0
    trackLetters = {}
    while col != width:
        if pzl[index+length] in valid:    
            #print(pzl[index+length])
            trackLetters[length] = pzl[index+length]
            #print(grabWord(trackLetters, length))
        if pzl[index+length] == BLOCKCHAR:
            return index, index+length, grabWord(trackLetters, length)
        col +=1
        length+=1
    return index, index +length, grabWord(trackLetters, length)
def fillWords(index, pzl):
    if pzl.count(OPENCHAR) == 0: return pzl
    for i in range(index, len(pzl)):
        if pzl[i] != BLOCKCHAR:
            start, end, word = findword(i, pzl)
            subpzl = [*pzl]
            subpzl[start:end] = [*word]
            return fillWords(end, subpzl)
    return ''
def temp(index, pzl): #find word but for inital column
    valid = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPLKJHGFDSAMNBVCXZ'
    row = index // width
    length = 0
    increment = 0
    trackLetters = {}
    while row != height:
        if pzl[index+increment] in valid:    
            trackLetters[length] = pzl[index+increment]
        if pzl[index+increment] == BLOCKCHAR:    
            return index, index+increment, grabWord(trackLetters, length)
        row +=1
        increment += width
        length+=1
    return index, index +increment, grabWord(trackLetters, length)
draft = [*answer]
for i in range(len(columns[0])): 
    if draft[columns[0][i]]!= BLOCKCHAR:
        start, end, word = temp(columns[0][i], answer)
        draft[start:end:width] = [*word]
        break

draft = fillWords(0, draft)
#algorithm for xword2
printBoard(''.join(draft), rows)
print()
def wordConstraints(pzl): #find all the places to add a word
    wordIndeces = [] 
    for row in rows: #for every row
        idx = 0 #start at index 0 for that row list
        while idx <width: #while you haven't reached the end of the row
            if (idx == 0 and pzl[row[idx]] !=BLOCKCHAR) or pzl[row[idx-1]] == BLOCKCHAR: #if your index is 0 and it's not a blocking square or the previous position is a blocking square
                temp = []
                while idx < width and pzl[row[idx]] != BLOCKCHAR: #while you havent reached the end of the row and the current position isn't a blocking square
                    temp.append(row[idx])
                    idx +=1
                if temp: wordIndeces.append(temp)
            idx +=1
    for col in columns: #same idea for columns
        idx = 0
        while idx <height:
            if (idx == 0 and pzl[col[idx]] !=BLOCKCHAR) or pzl[col[idx-1]] == BLOCKCHAR:
                temp = []
                while idx < height and pzl[col[idx]] != BLOCKCHAR:
                    temp.append(col[idx])
                    idx +=1
                if temp: wordIndeces.append(temp)
            idx +=1
    return wordIndeces
def pWords(trackLetters, length):#list of possible words for a specific place on the xword
    words = []
    for i in range(len(bucketOfWords[length])): #for every word of a certain length
        valid = True
        for k in trackLetters:   
            if bucketOfWords[length][i][k].lower() !=trackLetters[k].lower(): valid = False #if the letter of that position for a word doesn't match up on the crossword
        if valid: words.append(bucketOfWords[length][i])
    return words
def createPossibles(wordIndeces, pzl):
    letters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPLKJHGFDSAMNBVCXZ'
    possibles = []
    for word in wordIndeces: #for every possible place you can put a word
        trackLetters = {}
        for i, idx in enumerate(word):
            if pzl[idx] in letters: trackLetters[i] = pzl[idx] #store any letters that are fixed for that word
        posWords = pWords(trackLetters, len(word)) #might cause issue if trackletters is empty
        possibles.append((word, posWords))
    return possibles
def isInvalid(pos):
    for i in pos:
        if not i[1] : return True
    return False
def canFill(wordPos, pzl): #double checks if you can fill a word here
    for i in wordPos:
        if pzl[i] == OPENCHAR: return True
    return False
def minPos(pos, pzl):
    wordPos, words = '', ''
    for i in pos:
        if (not wordPos and not words):
            if canFill(i[0], pzl):
                wordPos, words = i[0], i[1]
        if len(i[1]) < len(words) and canFill(i[0], pzl):
            wordPos, words = i[0], i[1]
    return wordPos, words
intermediate = answer  
shouldPrint = False if length >=117 else True
def update(p, changed, pzl): #updates the list of possible words
    c = [(i[0], [*i[1]]) for i in p]
    #printBoard(''.join(pzl), rows)
    for idx in changed:
        #print(idx)
        letter = pzl[idx]
        for cs in posCon[idx]:
            #print(c[cs][0])
            #print(pos[cs][0])
            #print(pos[cs][0])
            x =  p[cs][0].index(idx)
            #if cs == 1: print('other' in c[cs][1], letter, x)
            #counter = 0
            y = [*p[cs][1]]
            for i in y:
                #counter+=1
                
                #print('other' in pos[1][1], letter, x)
                #if letter == 'h': print(i, letter)
                
                #if cs == 1 and i == 'other':print('its there')
                if i[x] != letter:
                    #if cs == 1 and i[1] == 't':print(i)
                    #if i == 'other':print(c[cs][0])
                    c[cs][1].remove(i)
                    #print(c ==  p)
            #if cs == 1: print(counter, len(p[cs][1]))
    return c
def x2(pzl, usedWords, pos): #update, instead of returning the puzzle, add it to a set
    global intermediate, shouldPrint
    if usedWords == None: usedWords = set()
    #pos = createPossibles(wordIndeces, pzl)
    if isInvalid(pos): return ''
    if pzl.count(OPENCHAR) == 0: return pzl
    if shouldPrint and length - pzl.count(OPENCHAR) - pzl.count(BLOCKCHAR) > length - intermediate.count(OPENCHAR) - intermediate.count(BLOCKCHAR):
        printBoard(''.join(pzl), rows)
        print()
        intermediate = pzl
    wordPos, words = minPos(pos, pzl)
    for i in words:
        if i not in usedWords:
            #print(i)
            subpzl = [*pzl]
            
            changed = []
            for idx in range(len(wordPos)):
                if subpzl[wordPos[idx]] == OPENCHAR: 
                    changed.append(wordPos[idx])
                subpzl[wordPos[idx]] = i[idx]
            newPos = update(pos, changed, subpzl)
            copyUsed = {*usedWords}
            copyUsed.add(i)
            pSol = x2(subpzl, copyUsed, newPos)
            print(pos)
            if pSol: return pSol
    return ''
wordIndeces = wordConstraints(answer)
print(wordIndeces)
posCon = [[csIdx for csIdx, cs in enumerate(wordIndeces) if idx in cs] for idx in range(length)]
print(posCon)
#print(wordIndeces)
possibles = createPossibles(wordIndeces, answer)

#print(possibles[0])
wordPos, words = minPos(possibles, pzl)
#print(words)
#print(possibles) #if there's only one option, it could be a seedstring
#printBoard(''.join(answer), rows)
answer = x2(answer, set(), possibles)
# possibles = possibles[1]
# answer[5] = 'h'
# possibles = update(possibles, [5], answer)
if answer: printBoard(''.join(answer), rows)
#print('adm' in x)
# Tianhao Chen, pd. 4, 2023