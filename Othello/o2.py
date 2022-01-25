import sys;args = sys.argv[1:]
# Tianhao Chen, pd.4
import math
black = 'xX'
white = 'oO'
board, play, op, move = '','','', ''
gHeight, gWidth = 8, 8
length = 8
cvt= "-ABCDEFGH"
#args = ['...ooo....xoox.xoxooooxxooooxoxxoooxooxxoooooxxx..xxxxox.xxxxxx.', 'X','49']
def compute():
    global board, play, op, move
    for i in args:
        if len(i) ==64:
            board = str(args[0]).upper()
        elif i == 'X' or i == 'x':
            play = i.upper()
            op = 'O'
        elif i == 'O' or i == 'o':
            play = i.upper()
            op = 'X'
        else:
            move = i
    if not board:
        board = '.'*27+"OX......XO"+'.'*27
    if not play:
        count = 0
        for i in board:
            if i in black or i in white:
                count+=1
            if count % 2 == 0:
                play = 'X'
                op = 'O'
            else:
                play = 'O'
                op = 'X'
def convert(toMove):
    col = cvt.index(toMove[0].upper())
    #print(col)
    row = int(toMove[1])
    #print(row)
    for i in range(row-1):
        col += 8
        #print(col)
    return col-1        
rows = [[*range(idx, idx + length)] for idx in range(0, length*length, length)]
columns = [[*range(idx, length*length, length)] for idx in range(length)]
bDiagonals = [[] for i in range(gWidth+gHeight -1)]
fDiagonals = [[] for i in range(gWidth+gHeight -1)]
for i in range(gWidth):
    for j in range(gHeight):
        bDiagonals[i+j]+=[i*gWidth+j]
        fDiagonals[i-j]+=[j*gWidth+i]
# print(bDiagonals)
# print(fDiagonals)

lCSets = rows + columns +fDiagonals + bDiagonals
#print(lCSets)
posCon = [[csIdx for csIdx, cs in enumerate(lCSets) if idx in cs] for idx in range(length*length)]
#print(posCon)
#nbrs = [list(set(lCSets[posCon[idx][0]]+lCSets[posCon[idx][1]]+lCSets[posCon[idx][2]]+lCSets[posCon[idx][3]]) - {idx} )for idx in
        #range(length*length)]
#print(nbrs)
def printBoard(pzl): #prints a 2-D display of othello board
    output = ''
    for i in range(0,len(pzl),gHeight): #go through each index, incrementing by height
        for j in range(gWidth): #adds a row of elements, separated by a space
            output+=pzl[i+j] + ' '
        output += '\n' #new line
    print(output)
def addAst(pzl, moves): #adds asterisks for possible moves
    adj = list(pzl)
    for i in moves:
        adj[i] = '*'
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
        # for cS in lCSets: #for each constraint set
    #     for idx in range(len(cS)): #for each index in the constraint set 
    #         if idx < len(cS)-1 and (pzl[cS[idx]] == '.' or pzl[cS[idx]] == toPlay) and pzl[cS[idx+1]] == opposite: #if its at least 2 away, a '.' or your token, and its neighbor is the opponent token
    #             marker = toPlay if pzl[cS[idx]] == '.' else '.' #store what to end on
    #             #change = set()
    #             for elm in cS[idx+1:]:
    #                 #change.add(elm)
    #                 if pzl[elm] == marker: #if it runs into a marker
    #                     if marker == toPlay:
    #                         if cS[idx] not in possible: possible[cS[idx]] = set()
    #                         #possible[cS[idx]] = possible[cS[idx]]|change
    #                         for i in cS[idx:cS.index(elm)]: possible[cS[idx]].add(i) #determine what the marker is and add a position index to possible accordingly
    #                     else: 
    #                         if elm not in possible: possible[elm] = set()
    #                         #possible[elm] = possible[elm]|change
    #                         for i in cS[idx+1:cS.index(elm)+1]: possible[elm].add(i)
    #                 if pzl[elm] != opposite:break #if it's not an enemy token, then it's not a possible move   
def makeMove(pzl, toPlay, opposite, move): #makes a move, swapping the opposite tokens with your token
    adj = list(pzl) #listify the string
    adj[move] = toPlay #convert that position to your token
    if move >= 0: #valid move
        for i in posCon[move]: #indeces of the constraint sets that the move is in
            traverse = [lCSets[i], lCSets[i][::-1]] #forward and backward
            for j in traverse:
                start = j.index(move)+1
                if start < len(j)-1 and adj[j[start]] == opposite: #if index is at least two away from the end and an enemy token
                    change = []
                    valid = False
                    for elm in j[start:]: #check if it's valid to move
                        change.append(elm)
                        if adj[elm] == '.':
                            break
                        elif adj[elm] == toPlay: #if valid, convert all tokens from start to elm into your token
                            
                            valid = True
                            break
                    if valid:
                        for i in change:
                                adj[i] = toPlay
                        
    return ''.join(adj)
# def possible(pzl, toPlay, opposite): #determines possible moves
#     possible = set()
#     for i in range(length*length):
#         if pzl[i] == '.':
#             for j in posCon[i]:
#                 #print(pzl[lCSets[j][lCSets[j].index(i)+1]])
#                 #print(lCSets[j][lCSets[j].index(i)+1])
#                 check = lCSets[j].index(i)+1
#                 if len(lCSets[j][check:]) >1 and pzl[lCSets[j][check]] == opposite:
#                     if pzl[lCSets[j][check+1]] != toPlay or pzl[lCSets[j][check+1]].lower() != toPlay or  pzl[lCSets[j][check+1]] != toPlay.lower():
#                         for elm in lCSets[j][check+1:]:
#                             if pzl[elm] == '.':
#                                 break
#                             elif pzl[elm] == toPlay or pzl[elm].lower() == toPlay or pzl[elm] == toPlay.lower():
#                                 possible.add(i)
#                 check = lCSets[j].index(i)-1
#                 if check> 0 and len(lCSets[j][check::-1]) >1 and (pzl[lCSets[j][check]] == opposite or pzl[lCSets[j][check]].lower() == opposite or pzl[lCSets[j][check]] == opposite.lower()):
#                     if pzl[lCSets[j][check-1]] != toPlay or pzl[lCSets[j][check-1]].lower() != toPlay or pzl[lCSets[j][check-1]] != toPlay.lower():
#                         for elm in lCSets[j][check-1::-1]:
#                             if pzl[elm] == '.':
#                                 break
#                             elif pzl[elm] == toPlay or  pzl[elm].lower() == toPlay or  pzl[elm] == toPlay.lower():
#                                 possible.add(i)               
#     return possible
# def makeMove(pzl, toPlay, opposite, move):
#     adj = list(pzl)                            
#     if move >= 0:
#         for j in posCon[move]:
#             check = lCSets[j].index(move)+1
#             if len(lCSets[j][check:]) >1 and pzl[lCSets[j][check]] == opposite:
#                 #print(lCSets[j][check+1:])
#                 filled = False
#                 for elm in lCSets[j][check+1:]:
#                     if pzl[elm] == '.':break
#                     elif pzl[elm] == toPlay or pzl[elm].lower() == toPlay or pzl[elm] == toPlay.lower():
#                         # print(lCSets[j].index(move))
#                         # print(lCSets[j])
#                         # print(elm)
#                         filled = True
#                         for x in lCSets[j][lCSets[j].index(move):lCSets[j].index(elm)+1]:
#                             adj[x] = toPlay
#                             #break
#                         if filled: break
#             check = lCSets[j].index(move)-1
#             if check > 0 and len(lCSets[j][check::-1]) >1 and pzl[lCSets[j][check]] == opposite:
#                 filled = False
#                 #print(lCSets[j][check-1::-1])
#                 for elm in lCSets[j][check-1::-1]:
#                     if pzl[elm] == '.':break
#                     elif pzl[elm] == toPlay or pzl[elm].lower() == toPlay or pzl[elm] == toPlay.lower():
#                         # print(lCSets[j].index(move))
#                         # print(lCSets[j])
#                         # print(elm)
#                         filled = True
#                         for x in lCSets[j][lCSets[j].index(elm):lCSets[j].index(move)+1]:
#                             adj[x] = toPlay
#                             #break
#                         if filled: break
#     return ''.join(adj)

def countP(pzl, tok):
    count = 0
    for i in pzl:
        if i == tok or i.upper() == tok:
            count+=1
    return count
def snapShot(pzl, toPlay, moves, move, opposite):
    if move:
        print(f'{toPlay} plays to {move}')
    printBoard(addAst(pzl, moves))
    #print()
    x = countP(pzl,'X')
    o = countP(pzl,'O')
    #print()
    print(f'{pzl} {x}/{o}')
    if moves:
        print(f'Possible moves for {opposite}: {moves}')
    else:
        print("No moves possible")
    print()

#printBoard(board)
compute()
#print(lCSets[4])
#print(pos)
#print(board,play, op)
#print(play)
pos = possible(board.upper(), play, op)

snapShot(board, play, pos, '',op)
if move:
    if move[0].upper() in cvt:
        x = convert(move)
        move = x
    else:
        x = int(move)

    if pos:
        nBoard = makeMove(board.upper(), play, op, x)
        newPos = possible(nBoard.upper(), op, play)
        if not newPos:
            newPos = possible(nBoard.upper(), play, op)
        snapShot(nBoard, play, newPos, move, op)

    #printBoard(addAst(board, pos))
    #print(f'Possible moves for {play}: {pos}')
    else:
        temp = play
        play = op
        op = temp
        pos = possible(board.upper(), play, op)
        nBoard = makeMove(board.upper(), play, op, x)
        snapShot(nBoard, play, pos-{x}, move)


# Tianhao Chen, pd. 4, 2023