import sys;args = sys.argv[1:]
# Tianhao Chen, pd.4
import time
board, play, op, move = '','','', []
gHeight, gWidth = 8, 8
length = 8
cvt= "-ABCDEFGH"
lCSets, posCon, rows, columns, bDiagonals, fDiagonals = [], [], [], [], [],[]
N = 11
def compute():
    global board, play, op, move, lCSets, posCon, rows, columns, bDiagonals, fDiagonals
    for i in args: #handles the command line
        if len(i) ==64: board = i.upper()
        if len(i) == 1 and i in "oOxX": play = i.upper()
        else: move += [i]
    if not board: board = '.'*27+"OX......XO"+'.'*27
    if not play:
        count = 0
        for i in board:
            if i in 'OoXx':count+=1
            if count % 2 == 0: play = 'X'
            else: play = 'O'
    op = 'XO'[play=='X']
    rows = [[*range(idx, idx + length)] for idx in range(0, length*length, length)] #constraint sets
    columns = [[*range(idx, length*length, length)] for idx in range(length)]
    bDiagonals = [[] for i in range(gWidth+gHeight -1)]
    fDiagonals = [[] for i in range(gWidth+gHeight -1)]
    for i in range(gWidth):
        for j in range(gHeight):
            bDiagonals[i+j]+=[i*gWidth+j]
            fDiagonals[i-j]+=[j*gWidth+i]
    lCSets = rows + columns +fDiagonals + bDiagonals
    posCon = [[csIdx for csIdx, cs in enumerate(lCSets) if idx in cs] for idx in range(length*length)]
def convert(toMove): #converts from spreadsheet coordinates to an int from 0-63
    col = cvt.index(toMove[0].upper())
    row = int(toMove[1])
    for i in range(row-1): col += 8
    return col-1        
def printBoard(pzl): #prints a 2-D display of othello board
    output = ''
    for i in range(0,len(pzl),gHeight): #go through each index, incrementing by height
        for j in range(gWidth): #adds a row of elements, separated by a space
            output+=pzl[i+j] + ' '
        output += '\n' #new line
    print(output)
def addAst(pzl, moves): #adds asterisks for possible moves
    adj = list(pzl)
    for i in moves:adj[i] = '*'
    return ''.join(adj)
def possible(pzl, toPlay, opposite): #determines possible moves
    possible = {} #set of possible moves
    for i in range(length*length):
        if pzl[i] == '.':
            for j in posCon[i]:
                check = lCSets[j].index(i)
                if len(lCSets[j][check:]) >2 and pzl[lCSets[j][check+1]] == opposite:
                    for elm in lCSets[j][check+2:]:
                        if pzl[elm] == '.': break
                        elif pzl[elm] == toPlay:
                            if i not in possible: possible[i] = set()
                            for x in lCSets[j][check:lCSets[j].index(elm)]: possible[i].add(x)
                            break
                if check> 1 and len(lCSets[j][check::-1]) >2 and pzl[lCSets[j][check-1]] == opposite:
                    for elm in lCSets[j][check-2::-1]:
                        if pzl[elm] == '.':break
                        elif pzl[elm] == toPlay:
                            if i not in possible: possible[i] = set()
                            for x in lCSets[j][lCSets[j].index(elm)+1:check+1]: possible[i].add(x)
                            break                           
    return possible
def makeMove(pzl, toPlay, move): #makes a move, swapping the opposite tokens with your token
    adj = list(pzl) #listify the string
    for i in move: adj[i] = toPlay
    return ''.join(adj)
def snapShot(pzl, toPlay, moves, move, opposite, bestMove): #snapshot for the othello board
    if move:print(f'{toPlay} plays to {move}')
    printBoard(addAst(pzl, moves))
    x = pzl.count('X')
    o = pzl.count('O')
    print(f'{pzl} {x}/{o}')
    if moves:
        display = set(moves.keys())
        if opposite: print(f'Possible moves for {toPlay}: {display}')
        else:print(f'Possible moves for {opposite}: {display}')
    print(f'My move: {bestMove}')
cacheChange = {}
def negamax(board, toPlay):
    opposite = 'O' if toPlay=='X' else 'X'
    key = (board, toPlay)
    returnVal = 0
    if key in cacheChange: return cacheChange[key]
    if board.count('.') == 0: #if no possible moves
        #return board.count(toPlay) - board.count(opposite), []
        returnVal = board.count(toPlay) - board.count(opposite), []
    pos = possible(board, toPlay, opposite)
    if not pos:
        if possible(board, opposite, toPlay):
            val, seq = negamax(board, opposite)
            seq = seq + [-1]
            returnVal = val*-1, seq
            #return val*-1, seq
        else: returnVal = board.count(toPlay) - board.count(opposite), []
            #return board.count(toPlay) - board.count(opposite), []
    minVal = -1000
    sequence = []
    for mv in set(pos.keys()):
        val, seq = negamax(makeMove(board,toPlay, pos[mv]), opposite)
        if val*-1 > minVal: minVal = val*-1; sequence = seq
        if mv not in sequence: sequence = sequence + [mv] 
        returnVal = minVal, sequence
    cacheChange[key] = returnVal
    return returnVal
    #return minVal, sequence
def limMob(pzl, toPlay, opposite, pos): #limit mobility, returns the move with the least number of possibilities for the opponent, eliminating cx moves from consideration
    cS = {0: {1,9,8},7:{6,14,15}, 56:{48,49,57}, 63:{62,55,54}}
    minM = 1000
    moveToPlay = -1
    for mv in pos:
        newBoard = makeMove(pzl, toPlay,pos[mv])
        temp = set(possible(newBoard, opposite, toPlay).keys())
        for i in cS: 
            if newBoard[i] != opposite:temp -= cS[i]
        if not temp: return mv
        else:
            if len(temp) < minM:
                minM = len(temp)
                moveToPlay = mv
    return moveToPlay
def bestMove(possible, toPlay, opposite, pzl): #finds the best moves
    worstM = set() #set of worst case scenario moves, should be considered last
    possibleSet = set(possible.keys())
    if 0 in possibleSet: return 0 #return move if it's a corner move
    if 7 in possibleSet: return 7
    if 56 in possibleSet: return 56
    if 63 in possibleSet: return 63
    if pzl[0] == toPlay: #play if it's a cx move and if you have the corner
        if 1 in possibleSet: return 1
        if 9 in possibleSet: return 9
        if 8 in possibleSet: return 8
    if pzl[7] == toPlay:
        if 6 in possibleSet: return 6
        if 14 in possibleSet: return 14
        if 15 in possibleSet: return 15
    if pzl[56] == toPlay:
        if 48 in possibleSet: return 48
        if 49 in possibleSet: return 49
        if 57 in possibleSet: return 57
    if pzl[63] == toPlay:
        if 62 in possibleSet:return 62
        if 55 in possibleSet: return 55
        if 54 in possibleSet: return 54

    if pzl[0] == '.' or pzl[0] == opposite: #avoid cx move if corner is not yours
        if 1 in possibleSet: worstM.add(1); possibleSet.discard(1)
        if 9 in possibleSet: worstM.add(9);possibleSet.discard(9)
        if 8 in possibleSet: worstM.add(8);possibleSet.discard(8)
    if pzl[7] == '.'or pzl[7] == opposite:
        if 6 in possibleSet: worstM.add(6);possibleSet.discard(6)
        if 14 in possibleSet: worstM.add(14);possibleSet.discard(14)
        if 15 in possibleSet: worstM.add(15);possibleSet.discard(15)
    if pzl[56] == '.'or pzl[56] == opposite:
        if 48 in possibleSet: worstM.add(48);possibleSet.discard(48)
        if 49 in possibleSet: worstM.add(49);possibleSet.discard(49)
        if 57 in possibleSet: worstM.add(57);possibleSet.discard(57)
    if pzl[63] == '.'or pzl[63] == opposite:
        if 62 in possibleSet:worstM.add(62);possibleSet.discard(62)
        if 55 in possibleSet: worstM.add(55);possibleSet.discard(55)
        if 54 in possibleSet: worstM.add(54);possibleSet.discard(54)
    pMove = limMob(pzl, toPlay, opposite, possible) #limited mobility
    if pMove != -1: return pMove
    if possibleSet: return possibleSet.pop()
    return worstM.pop() #last resort
def quickMove(brd, tkn):
    pos = possible(brd, tkn, 'XO'[tkn=='X'])
    return bestMove(pos, tkn, 'XO'[tkn=='X'],brd)
def main():
    global N
    a = time.process_time()
    move = quickMove(board.upper(), play)
    snapShot(board.upper(), play, possible(board.upper(), play, 'XO'[play=='X']), '','XO'[play=='X'], move)
    if board.count('.') < N: 
        val, seq = negamax(board.upper(), play)
        print(f'Min score: {val}; move sequence: {seq}')
    print()
    b = time.process_time()-a
    print(b)
    
compute()
if __name__ == '__main__': main() 
# Tianhao Chen, pd. 4, 2023