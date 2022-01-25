import sys;args = sys.argv[1:]
#args = ['xxxxxxo.xxxxxo..xxooooooxoxxooooxoxxooooxxxoxoooxxo.oxooxooooooo', 'x']
#args = ['xxxxxxo.xxxoxo.oxxxxooooxoxxoox.xxoxxxxxxxxxoxxoxxxxxxx.xxxxxxx.', 'o']
# Tianhao Chen, pd.4
import time
board, play, op, move = '','','', []
gHeight, gWidth = 8, 8
length = 8
cvt= "-ABCDEFGH"
edges, danger, lCSets, posCon, rows, columns, bDiagonals, fDiagonals, center = {}, {}, [], [], [], [], [],[], {}
N = 11
def compute():
    global board, play, op, move, edges, danger, lCSets, posCon, rows, columns, bDiagonals, fDiagonals, center     
    for i in args: #handles the command line
        if len(i) ==64: board = i.upper()
        if len(i) == 1 and i in "oOxX":
            play = i.upper()
        else: move += [i]
    if not board:
        board = '.'*27+"OX......XO"+'.'*27
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
    edges = {1,2,3,4,5,6,8,16,24,32,40,48, 15, 23,31,39,47,55, 57,58,59,60,61,62}
    danger = {9,10,11,12,13,14,17,25,33,41,49, 50,51,52,53,54, 22, 30, 38, 46}
    lCSets = rows + columns +fDiagonals + bDiagonals
    posCon = [[csIdx for csIdx, cs in enumerate(lCSets) if idx in cs] for idx in range(length*length)]
    center = {18, 19, 20, 21, 26, 27, 28, 29, 34, 35, 36, 37, 42, 43, 44, 45}
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
    possible = set() #set of possible moves
    for cS in lCSets: #for each constraint set
        for idx in range(len(cS)): #for each index in the constraint set 
            if idx < len(cS)-1 and (pzl[cS[idx]] == '.' or pzl[cS[idx]] == toPlay.upper()) and pzl[cS[idx+1]] == opposite.upper(): #if its at least 2 away, a '.' or your token, and its neighbor is the opponent token
                marker = toPlay.upper() if pzl[cS[idx]] == '.' else '.' #store what to end on
                for elm in cS[idx+1:]: 
                    if pzl[elm] == marker: #if it runs into a marker
                        if marker == toPlay.upper():possible.add(cS[idx]) #determine what the marker is and add a position index to possible accordingly
                        else: possible.add(elm)
                    if pzl[elm] != opposite.upper():break #if it's not an enemy token, then it's not a possible move               
    return possible
def makeMove(pzl, toPlay, opposite, move): #makes a move, swapping the opposite tokens with your token
    adj = list(pzl) #listify the string
    adj[move] = toPlay.upper() #convert that position to your token
    if move >= 0: #valid move
        for i in posCon[move]: #indeces of the constraint sets that the move is in
            traverse = [lCSets[i], lCSets[i][::-1]] #forward and backward
            for j in traverse:
                start = j.index(move)+1
                if start < len(j)-1 and adj[j[start]] == opposite.upper(): #if index is at least two away from the end and an enemy token
                    for elm in j[start:]: #check if it's valid to move
                        if adj[elm] == '.':break
                        elif adj[elm] == toPlay.upper(): #if valid, convert all tokens from start to elm into your token
                            for x in j[start: j.index(elm)]: adj[x] = toPlay.upper()
                            break
    return ''.join(adj)
def countP(pzl, tok): #counts the number of a token
    count = 0
    for i in pzl: 
        if i == tok or i.upper() == tok: count+=1
    return count
def snapShot(pzl, toPlay, moves, move, opposite, bestMove): #snapshot for the othello board
    if move:print(f'{toPlay} plays to {move}')
    printBoard(addAst(pzl, moves))
    x = countP(pzl,'X')
    o = countP(pzl,'O')
    print(f'{pzl} {x}/{o}')
    if moves:
        if opposite: print(f'Possible moves for {toPlay}: {moves}')
        else:print(f'Possible moves for {opposite}: {moves}')
    print(f'My move: {bestMove}')
def negamax(board, toPlay):
    opposite = 'O' if toPlay=='X' else 'X'
    if countP(board.upper(), '.') == 0 or ((not possible(board.upper(), toPlay, opposite))and (not possible(board.upper(), opposite, toPlay))):
        diff = countP(board, toPlay) - countP(board, opposite)
        return diff, []
    if not possible(board.upper(), toPlay, opposite) and possible(board.upper(), opposite, toPlay):
        val, seq = negamax(board.upper(), opposite)
        seq.append(-1)
        return val*-1, seq
    minVal = -1000
    sequence = []
    for mv in possible(board.upper(), toPlay, opposite):
        val, seq = negamax(makeMove(board.upper(),toPlay, opposite, mv), opposite)
        if val*-1 > minVal: minVal = val*-1; sequence = seq
        if mv not in sequence: sequence.append(mv) 
    return minVal, sequence
def limMob(pzl, toPlay, opposite, pos): #limit mobility, returns the move with the least number of possibilities for the opponent, eliminating cx moves from consideration
    cS = {0: {1,9,8},7:{6,14,15}, 56:{48,49,57}, 63:{62,55,54}}
    minM = 1000
    moveToPlay = -1
    for mv in pos:
        newBoard = makeMove(pzl.upper(), toPlay, opposite, mv)
        temp = set(possible(newBoard.upper(), opposite, toPlay))
        for i in cS: 
            if newBoard[i] != opposite:temp -= cS[i]
        #temp = set(possible(newBoard.upper(), opposite, toPlay)) - {1,9,8,6,14,15,48,49,57,62,55,54}
        if not temp:
            return mv
        else:
            if len(temp) < minM:
                minM = len(temp)
                moveToPlay = mv
    return moveToPlay
def bestMove(possible, toPlay, opposite, pzl): #finds the best moves
    worstM = set() #set of worst case scenario moves, should be considered last
    if 0 in possible: return 0 #return move if it's a corner move
    if 7 in possible: return 7
    if 56 in possible: return 56
    if 63 in possible: return 63
    if pzl[0] == toPlay: #play if it's a cx move and if you have the corner
        if 1 in possible: return 1
        if 9 in possible: return 9
        if 8 in possible: return 8
    if pzl[7] == toPlay:
        if 6 in possible: return 6
        if 14 in possible: return 14
        if 15 in possible: return 15
    if pzl[56] == toPlay:
        if 48 in possible: return 48
        if 49 in possible: return 49
        if 57 in possible: return 57
    if pzl[63] == toPlay:
        if 62 in possible:return 62
        if 55 in possible: return 55
        if 54 in possible: return 54

    if pzl[0] == '.' or pzl[0] == opposite: #avoid cx move if corner is not yours
        if 1 in possible: worstM.add(1); possible.discard(1)
        if 9 in possible: worstM.add(9);possible.discard(9)
        if 8 in possible: worstM.add(8);possible.discard(8)
    if pzl[7] == '.'or pzl[7] == opposite:
        if 6 in possible: worstM.add(6);possible.discard(6)
        if 14 in possible: worstM.add(14);possible.discard(14)
        if 15 in possible: worstM.add(15);possible.discard(15)
    if pzl[56] == '.'or pzl[56] == opposite:
        if 48 in possible: worstM.add(48);possible.discard(48)
        if 49 in possible: worstM.add(49);possible.discard(49)
        if 57 in possible: worstM.add(57);possible.discard(57)
    if pzl[63] == '.'or pzl[63] == opposite:
        if 62 in possible:worstM.add(62);possible.discard(62)
        if 55 in possible: worstM.add(55);possible.discard(55)
        if 54 in possible: worstM.add(54);possible.discard(54)
    # for i in edges:
    #     if i in possible:        
    #         return i
    pMove = limMob(pzl, toPlay, opposite, possible) #limited mobility
    if pMove != -1: return pMove
    
    # for i in danger:
    #     if i in possible:
    #         worstM.add(str(i))
    #         possible.discard(i)
    
    if possible: 
        return possible.pop()
    return worstM.pop() #last resort
def quickMove(brd, tkn):
    tkn = tkn.upper()
    pos = possible(brd.upper(), tkn, 'XO'[tkn=='X'])
    return bestMove(pos, tkn, 'XO'[tkn=='X'], brd.upper())
def main():
    global N
    a = time.process_time()
    move = quickMove(board.upper(), play)
    snapShot(board.upper(), play, possible(board.upper(), play, 'XO'[play=='X']), '','XO'[play=='X'], move)
    if countP(board,'.') < N: 
        val, seq = negamax(board.upper(), play)
        print(f'Min score: {val}; move sequence: {seq}')
    print()
    b = time.process_time()-a
    print(b)
compute()
if __name__ == '__main__': main() 
# Tianhao Chen, pd. 4, 2023