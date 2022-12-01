import sys;args = sys.argv[1:]
# Tianhao Chen,pd.4
LIMIT_AB = 13
import time, random
#args = ['...........................OX......XO...........................', 'o']
board, play, op, move = '','','', []
gHeight, gWidth = 8, 8
length = 8
cvt= "*ABCDEFGH"
lCSets, posCon, rows, columns, bDiagonals, fDiagonals, danger, edges = [], [], [], [], [],[], {}, {}

def compute():
    global board, play, op, move, lCSets, posCon, rows, columns, bDiagonals, fDiagonals, danger, edges
    for i in args: #handles the command line
        if len(i) ==64: board = i.upper()
        elif len(i) == 1 and i in "oOxX": play = i.upper()
        else:
            if len(i) <3:
                if i[0].upper() in cvt:i = convert(i)
                move += [int(i)]
            else:
                for j in range(0,len(i)-1, 2):
                    if i[j] == '_': mv = i[j+1]
                    else: mv = i[j]+i[j+1]
                    move += [int(mv)]       
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
    danger = {9,10,11,12,13,14,17,25,33,41,49, 50,51,52,53,54, 22, 30, 38, 46}
    edges = {1,2,3,4,5,6,8,16,24,32,40,48, 15, 23,31,39,47,55, 57,58,59,60,61,62}

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
posCache = {}
def possible(pzl, toPlay, opposite): #determines possible moves
    global posCache
    possible = {} #set of possible moves
    key = (pzl, toPlay)
    if key in posCache:return posCache[key]
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
    posCache[key] = possible                          
    return possible
def makeMove(pzl, toPlay, move): #makes a move, swapping the opposite tokens with your token
    adj = list(pzl) #listify the string
    for i in move: adj[i] = toPlay
    return ''.join(adj)
def snapShot(pzl, toPlay, moves, move, opposite): #snapshot for the othello board
    if move or move == 0:print(f'{toPlay} plays to {move}')
    printBoard(addAst(pzl, moves))
    x = pzl.count('X')
    o = pzl.count('O')
    print(f'{pzl} {x}/{o}')
    if moves:
        display = set(moves.keys())
        print(f'Possible moves for {opposite}: {display}')
    print()
cacheChange = {}
def negamax(board, toPlay):
    opposite = 'O' if toPlay=='X' else 'X'
    key = (board, toPlay)
    returnVal = 0
    if key in cacheChange: return cacheChange[key]
    if board.count('.') == 0: #if no possible moves
        returnVal = board.count(toPlay) - board.count(opposite), []
    pos = possible(board, toPlay, opposite)
    if not pos:
        if possible(board, opposite, toPlay):
            val, seq = negamax(board, opposite)
            seq = seq + [-1]
            returnVal = val*-1, seq
        else: returnVal = board.count(toPlay) - board.count(opposite), []
    minVal = -1000
    sequence = []
    for mv in set(pos.keys()):
        val, seq = negamax(makeMove(board,toPlay, pos[mv]), opposite)
        if val*-1 > minVal: minVal = val*-1; sequence = seq
        if mv not in sequence: sequence = sequence + [mv] 
        returnVal = minVal, sequence
    cacheChange[key] = returnVal
    return returnVal
def alphabeta(board, toPlay, a, b):
    opposite = 'O' if toPlay=='X' else 'X'
    if board.count('.') == 0: return board.count(toPlay) - board.count(opposite), []
    if not (pos:=possible(board, toPlay, opposite)):
        if possible(board, opposite, toPlay):
            val, seq = alphabeta(board, opposite, -b, -a)
            seq = seq + [-1]
            #returnVal = val*-1, seq
            return val*-1, seq
        else:return board.count(toPlay) - board.count(opposite), []
    sequence = []
    best = a-1
    for mv in set(pos.keys()):
        val, seq = alphabeta(makeMove(board,toPlay, pos[mv]), opposite, -b, -a)
        val = val*-1
        if val < a: continue
        if val > b:
            if mv not in seq: seq = seq+[mv]
            return val, seq
        best = max(best, val)
        a = val+1
        sequence = seq
        if mv not in sequence: sequence = sequence + [mv] 
    return best, sequence

def calH(board, toPlay):
    opposite = 'O' if toPlay=='X' else 'X'
    countP = board.count(toPlay)
    countO = board.count(opposite)
    coinParity = 64*(countP-countO)/(countP+countO)
    playPos = possible(board, toPlay, opposite)
    opPos = possible(board, opposite, toPlay)
    posP = len(playPos)
    posO = len(opPos)
    if (posP+posO !=0): mobHeuristic = 64*(posP-posO)/(posP+posO)
    else: mobHeuristic = 0
    cornP, cornO = 0,0
    corner = [0, 7, 56, 63]
    for i in corner:
        if board[i] == toPlay: 
            cornP +=1
        elif board[i] == opposite: 
            cornO +=1
    if cornP+cornO !=0: corHeuristic = 64*(cornP-cornO)/(cornP+cornO)
    else: corHeuristic = 0
    cxPlay = 0
    cxOpposite = 0
    if board[0] == '.': #play if it's a cx move and if you have the corner
        if board[1] == toPlay: cxPlay +=1
        elif board[1] == opposite: cxOpposite +=1
        if board[9] == toPlay: cxPlay +=1
        elif board[9] == opposite: cxOpposite +=1
        if board[8] == toPlay: cxPlay +=1
        elif board[8] == opposite: cxOpposite +=1
    if board[7] == '.':
        if board[6] == toPlay: cxPlay +=1
        elif board[6] == opposite: cxOpposite +=1
        if board[14] == toPlay: cxPlay +=1
        elif board[14] == opposite: cxOpposite +=1
        if board[15] == toPlay: cxPlay +=1
        elif board[15] == opposite: cxOpposite +=1
    if board[56] == '.':
        if board[48] == toPlay: cxPlay +=1
        elif board[48] == opposite: cxOpposite +=1
        if board[49] == toPlay: cxPlay +=1
        elif board[49] == opposite: cxOpposite +=1
        if board[57] == toPlay: cxPlay +=1
        elif board[57] == opposite: cxOpposite +=1
    if board[63] == '.':
        if board[62] == toPlay: cxPlay +=1
        elif board[62] == opposite: cxOpposite +=1
        if board[55] == toPlay: cxPlay +=1
        elif board[55] == opposite: cxOpposite +=1
        if board[54] == toPlay: cxPlay +=1
        elif board[54] == opposite: cxOpposite +=1
    cxFinal = -12.5 * (cxPlay - cxOpposite)
    returnVal = (.2)*cxFinal + (.3)*corHeuristic + (.4) * mobHeuristic + (.1) * coinParity
    return int(returnVal)

maxMoves = 4
def midab(board, toPlay, a, b, depth):
    opposite = 'O' if toPlay=='X' else 'X'
    if depth == maxMoves: return calH(board,toPlay), []
    if not (pos:=possible(board, toPlay, opposite)):
        if possible(board, opposite, toPlay):
            val, seq = midab(board, opposite, -b, -a, depth+1)
            seq = seq + [-1]
            return val*-1, seq
        else:return calH(board,toPlay), []
    sequence = []
    best = a-1
    for mv in set(pos.keys()):
        val, seq = midab(makeMove(board,toPlay, pos[mv]), opposite, -b, -a, depth+1)
        val = val*-1
        if val < a: continue
        if val > b:
            if mv not in seq: seq = seq+[mv]
            return val, seq
        best = max(best, val)
        a = val+1
        sequence = seq
        if mv not in sequence: sequence = sequence + [mv] 
    return best, sequence
def limMob(pzl, toPlay, opposite, pos): #limit mobility, returns the move with the least number of possibilities for the opponent, eliminating cx moves from consideration
    cS = {0: {1,9,8},7:{6,14,15}, 56:{48,49,57}, 63:{62,55,54}}
    minM = 1000
    moveToPlay = -1
    for mv in pos:
        newBoard = makeMove(pzl, toPlay,pos[mv])
        temp = set(possible(newBoard, opposite, toPlay).keys())
        for i in cS: 
            if newBoard[i] != opposite:temp -= cS[i]
        if 0 in temp or 7 in temp or 56 in temp or 63 in temp: continue #look over later
        if not temp: return mv
        else:
            if (length:=len(temp)) < minM:
                minM = length
                moveToPlay = mv
    return moveToPlay
def lessTknTaken(pos):
    minTaken = 1000
    mv = -1
    for i in pos:
        if (tryM :=len(pos[i])) < minTaken:
            minTaken = tryM
            mv = i
    return mv
def bestMove(possible, toPlay, opposite, pzl): #finds the best moves
    if not possible: return -1
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

    pMove = limMob(pzl, toPlay, opposite, possible) #limited mobility, it's allowing opponent to play corner
    if pMove != -1 and pMove not in worstM: return pMove
    pMove = lessTknTaken(possible) 
    if pMove != -1 and pMove not in worstM: return pMove
    for i in edges:
        if i in possible and i not in worstM:return i
    if possibleSet: return possibleSet.pop()
    return worstM.pop() #last resort
def quickMove(brd, tkn):
    pos = possible(brd, tkn, 'XO'[tkn=='X'])
    return bestMove(pos, tkn, 'XO'[tkn=='X'],brd)
def runGames():
    global board
    myTkn = "X" #your token
    mytknCnt, ttltkn = 0,0
    worstGame1 = ()#score, your token, game number, transcript
    worstGame2 =  () #score, your token, game number, transcript
    scores = []
    for i in range(1,101):
        transcript = []
        curTkn = 'X' #token to play
        while True:
            if not (pos := possible(board, curTkn, 'XO'[curTkn=='X'])):
                curTkn = 'XO'[curTkn=='X']
                if not (pos := possible(board, curTkn, 'XO'[curTkn=='X'])):break
                transcript.append(-1)
            if curTkn != myTkn: #opponent's turn
                mv = random.choice([*pos.keys()])
                
                #mv = quickMove(board, curTkn)
                #if board.count('.') < LIMIT_AB: 
                #     val, seq = alphabeta(board, curTkn, -64, 64)
                #     mv = seq[-1]
                transcript.append(mv)
                board = makeMove(board, curTkn, pos[mv])
            else:#our turn
                mv = quickMove(board, myTkn) #changed
                if board.count('.') < LIMIT_AB: val, seq = alphabeta(board, curTkn, -1000, 1000)
                else: val, seq = midab(board.upper(), curTkn, -64,64, 0)    
                mv = seq[-1]
                transcript.append(mv)
                board = makeMove(board, curTkn, pos[mv])
            curTkn = 'XO'[curTkn=='X']
        transcript = [f"_{mv}"[-2:] for mv in transcript]
        tkncnt = board.count(myTkn)
        mytknCnt += tkncnt
        ttltkn += (64-board.count('.'))
        score = tkncnt - board.count('XO'[myTkn=='X'])
        check = str(score)
        if (length:= len(check)) ==1: check = '  '+check
        if length == 2: check = ' '+check
        scores.append(check)
        if len(scores) == 10:
            print(scores[0],scores[1],scores[2],scores[3],scores[4],scores[5],scores[6],scores[7],scores[8],scores[9])
            scores = []
        if not worstGame1:worstGame1 = (score, myTkn, i, transcript)
        elif not worstGame2:worstGame2 = (score, myTkn, i, transcript)
        elif score < worstGame2[0]:
            if score < worstGame1[0]:
                if worstGame1[0] > worstGame2[0]:worstGame1 = worstGame2
            worstGame2 = (score, myTkn, i, transcript)
        elif score < worstGame1[0]:
            if worstGame1[0] > worstGame2[0]:worstGame1 = worstGame2
            worstGame2 = (score, myTkn, i, transcript)
        myTkn = 'XO'[myTkn=='X']
        board = '.'*27+"OX......XO"+'.'*27
    print()
    print(f'My tokens: {mytknCnt}; Total tokens: {ttltkn}')
    print(f'Score: {round((mytknCnt/ttltkn)*100, 1)}%')
    print(f'NM/AB LIMIT: {LIMIT_AB}')
    print(f'Game {worstGame1[2]} as {worstGame1[1]} => {worstGame1[0]}:')
    print(''.join(worstGame1[3]))
    print(f'Game {worstGame2[2]} as {worstGame2[1]} => {worstGame2[0]}:')
    print(''.join(worstGame2[3]))
def main():
    global LIMIT_AB, move, board, play, op
    a = time.process_time()
    if args:
        if move: snapShot(board, play, possible(board, play, 'XO'[play=='X']), '',play)
        for mv in move:
            if mv<0: continue
            pos = possible(board, play, op)
            if not pos or mv not in pos:
                temp = play
                play = op
                op = temp
            board = makeMove(board, play,  pos[mv])
            newPos = possible(board, op, play)
            if not newPos:
                newPos = possible(board, play, op)
                snapShot(board, play, newPos, mv, play)
            else:
                snapShot(board, play, newPos, mv, op)
                temp = play
                play = op
                op = temp
        if not possible(board, play, op):play = op
        if not move: snapShot(board, play, possible(board, play, 'XO'[play=='X']), '',play)
        move = quickMove(board, play)
        print(f'My move: {move}')

        if board.count('.') < LIMIT_AB: val, seq = alphabeta(board.upper(), play, -64, 64)
        else: val, seq = midab(board.upper(), play, -1000,1000, 0)
        print(f'Min score: {val}; move sequence: {seq}')
    else:runGames()
    b = round(time.process_time()-a,1)
    print(f'Elasped time: {b}s') 
compute()
if __name__ == '__main__': main() 
# Tianhao Chen, pd. 4, 2023