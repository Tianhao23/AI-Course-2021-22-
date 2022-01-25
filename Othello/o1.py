import sys;args = sys.argv[1:]
# Tianhao Chen, pd.4
import math
black = 'xX'
white = 'oO'
board, play, op = '','',''
gHeight, gWidth = 8, 8
length = 8
#args = ['ooooooo.ooooooo.oxxoxoxxoxoxoxxxooxoxxxxoxoxxxxxooxxxxxxxxxxxxxx', 'o']
def compute():
    global board, play, op
    if not args:
        board = '.'*27+"OX......XO"+'.'*27
        play = 'X'
        op = 'O'
    else:
        if len(args[0]) !=64:
            play = str(args[0])
            if play in black:
                op = 'O'
            else:
                op = 'X'
            board = '.'*27+"OX......XO"+'.'*27
        else:
            board = str(args[0])
            if len(args) == 2:
                play = str(args[1]).upper()
                if play in black:
                    op = 'O'
                else:
                    op = 'X'
            else:
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
    pzl = pzl.upper()
    toPlay = toPlay.upper()
    opposite = opposite.upper()
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

                    

    # for i in range(length*length):
    #     if pzl[i] == '.':
    #         for j in posCon[i]:
    #             check = lCSets[j].index(i)+1
    #             if len(lCSets[j][check:]) >1 and (pzl[lCSets[j][check]] == opposite or pzl[lCSets[j][check]].lower() == opposite or pzl[lCSets[j][check]] == opposite.lower()):
    #                 if pzl[lCSets[j][check+1]] != toPlay or pzl[lCSets[j][check+1]].lower() != toPlay or  pzl[lCSets[j][check+1]] != toPlay.lower():
    #                     for elm in lCSets[j][check+1:]:
    #                         if pzl[elm] == '.':
    #                             break
    #                         elif pzl[elm] == toPlay or pzl[elm].lower() == toPlay or pzl[elm] == toPlay.lower():
    #                             possible.add(i)
    #             check = lCSets[j].index(i)-1
    #             if check> 0 and len(lCSets[j][check::-1]) >1 and (pzl[lCSets[j][check]] == opposite or pzl[lCSets[j][check]].lower() == opposite or pzl[lCSets[j][check]] == opposite.lower()):
    #                 if pzl[lCSets[j][check-1]] != toPlay or pzl[lCSets[j][check-1]].lower() != toPlay or pzl[lCSets[j][check-1]] != toPlay.lower():
    #                     for elm in lCSets[j][check-1::-1]:
    #                         if pzl[elm] == '.':
    #                             break
    #                         elif pzl[elm] == toPlay or  pzl[elm].lower() == toPlay or  pzl[elm] == toPlay.lower():
    #                             possible.add(i)               
    return possible
#printBoard(board)
compute()
pos = possible(board.upper(), play, op)
#print(lCSets[4])
#print(pos)
#print(board,play, op)
print(play)
if pos:
    printBoard(addAst(board, set(pos.keys())))
    print(f'Possible moves for {play}: {set(pos.keys())}')
else:
    printBoard(board)
    print("No moves possible")

# Tianhao Chen, pd. 4, 2023