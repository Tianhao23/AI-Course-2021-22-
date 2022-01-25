import sys;args = sys.argv[1:]
# Tianhao Chen, pd.4
black = 'xX'
white = 'oO'
board, play, op, move = '','','', []
gHeight, gWidth = 8, 8
length = 8
cvt= "-ABCDEFGH"
edges, danger, lCSets, posCon, rows, columns, bDiagonals, fDiagonals = [], [], [], [], [], [], [],[]
#args = ['...ooo....xoox.xoxooooxxooooxoxxoooxooxxoooooxxx..xxxxox.xxxxxx.', 'X','49']
def compute():
    global board, play, op, move, edges, danger, lCSets, posCon, rows, columns, bDiagonals, fDiagonals
    for i in args:
        if len(i) ==64:
            board = str(args[0]).lower()
        elif i == 'X' or i == 'x':
            play = i.lower()
            op = 'o'
        elif i == 'O' or i == 'o':
            play = i.lower()
            op = 'x'
        else:
            move += [i]
    if not board:
        board = '.'*27+"ox......xo"+'.'*27
    if not play:
        count = 0
        for i in board:
            if i in black or i in white:
                count+=1
            if count % 2 == 0:
                play = 'x'
                op = 'o'
            else:
                play = 'o'
                op = 'x'
    rows = [[*range(idx, idx + length)] for idx in range(0, length*length, length)]
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

#global edges, danger, lCSets, posCon, rows, columns, bDiagonals, fDiagonals
def convert(toMove):
    col = cvt.index(toMove[0].lower())
    row = int(toMove[1])
    for i in range(row-1):
        col += 8
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
    for i in moves:
        adj[i] = '*'
    return ''.join(adj)
def possible(pzl, toPlay, opposite): #determines possible moves
    possible = set()
    for i in range(length*length):
        if pzl[i] == '.':
            for j in posCon[i]:
                #print(pzl[lCSets[j][lCSets[j].index(i)+1]])
                #print(lCSets[j][lCSets[j].index(i)+1])
                check = lCSets[j].index(i)+1
                if len(lCSets[j][check:]) >1 and pzl[lCSets[j][check]] == opposite:
                    if pzl[lCSets[j][check+1]] != toPlay or pzl[lCSets[j][check+1]].lower() != toPlay or  pzl[lCSets[j][check+1]] != toPlay.lower():
                        for elm in lCSets[j][check+1:]:
                            if pzl[elm] == '.':
                                break
                            elif pzl[elm] == toPlay or pzl[elm].lower() == toPlay or pzl[elm] == toPlay.lower():
                                possible.add(i)
                check = lCSets[j].index(i)-1
                if check> 0 and len(lCSets[j][check::-1]) >1 and (pzl[lCSets[j][check]] == opposite or pzl[lCSets[j][check]].lower() == opposite or pzl[lCSets[j][check]] == opposite.lower()):
                    if pzl[lCSets[j][check-1]] != toPlay or pzl[lCSets[j][check-1]].lower() != toPlay or pzl[lCSets[j][check-1]] != toPlay.lower():
                        for elm in lCSets[j][check-1::-1]:
                            if pzl[elm] == '.':
                                break
                            elif pzl[elm] == toPlay or  pzl[elm].lower() == toPlay or  pzl[elm] == toPlay.lower():
                                possible.add(i)               
    return possible
def makeMove(pzl, toPlay, opposite, move):
    adj = list(pzl)
    if move >= 0:
        for j in posCon[move]:
            check = lCSets[j].index(move)+1
            if len(lCSets[j][check:]) >1 and pzl[lCSets[j][check]] == opposite:
                #print(lCSets[j][check+1:])
                filled = False
                for elm in lCSets[j][check+1:]:
                    if pzl[elm] == '.':break
                    elif pzl[elm] == toPlay or pzl[elm].lower() == toPlay or pzl[elm] == toPlay.lower():
                        # print(lCSets[j].index(move))
                        # print(lCSets[j])
                        # print(elm)
                        filled = True
                        for x in lCSets[j][lCSets[j].index(move):lCSets[j].index(elm)+1]:
                            adj[x] = toPlay
                        if filled: break
            check = lCSets[j].index(move)-1
            if check > 0 and len(lCSets[j][check::-1]) >1 and pzl[lCSets[j][check]] == opposite:
                filled = False
                #print(lCSets[j][check-1::-1])
                for elm in lCSets[j][check-1::-1]:
                    if pzl[elm] == '.':break
                    elif pzl[elm] == toPlay or pzl[elm].lower() == toPlay or pzl[elm] == toPlay.lower():
                        # print(lCSets[j].index(move))
                        # print(lCSets[j])
                        # print(elm)
                        filled = True
                        for x in lCSets[j][lCSets[j].index(elm):lCSets[j].index(move)+1]:
                            adj[x] = toPlay
                        if filled: break
    return ''.join(adj)

def countP(pzl, tok):
    count = 0
    for i in pzl:
        if i == tok or i.lower() == tok:
            count+=1
    return count
def snapShot(pzl, toPlay, moves, move, opposite, bestM):
    if move:
        print(f'{toPlay} plays to {move}')
    printBoard(addAst(pzl, moves))
    x = countP(pzl,'x')
    o = countP(pzl,'o')
    print(f'{pzl} {x}/{o}')
    if moves:
        if opposite:
            print(f'Possible moves for {opposite}: {moves}')
        else:
            print(f'Possible moves for {toPlay}: {moves}')
    print(bestM)
    print()
def bestMove(possible, toPlay, opposite, pzl):
        global edges
        if not possible: #for moderator
            return -1
        worstM = set()
        if 0 in possible: return '0'
        if 7 in possible: return '7'
        if 56 in possible: return '56'
        if 63 in possible: return '63'
        if pzl[0] == toPlay:
            if 1 in possible: return '1'
            if 9 in possible: return '9'
            if 8 in possible: return '8'
        if pzl[7] == toPlay:
            if 6 in possible: return '6'
            if 14 in possible: return '14'
            if 15 in possible: return '15'
        if pzl[56] == toPlay:
            if 48 in possible: return '48'
            if 49 in possible: return '49'
            if 57 in possible: return '57'
        if pzl[63] == toPlay:
            if 62 in possible:return '62'
            if 55 in possible: return '55'
            if 54 in possible: return '54'

        if pzl[0] == '.':
            if 1 in possible: worstM.add('1'); possible.discard(1)
            if 9 in possible: worstM.add('9');possible.discard(9)
            if 8 in possible: worstM.add('8');possible.discard(8)
        if pzl[7] == '.':
            if 6 in possible: worstM.add('6');possible.discard(6)
            if 14 in possible: worstM.add('14');possible.discard(14)
            if 15 in possible: worstM.add('15');possible.discard(15)
        if pzl[56] == '.':
            if 48 in possible: worstM.add('48');possible.discard(48)
            if 49 in possible: worstM.add('49');possible.discard(49)
            if 57 in possible: worstM.add('57');possible.discard(57)
        if pzl[63] == '.':
            if 62 in possible:worstM.add('62');possible.discard(62)
            if 55 in possible: worstM.add('55');possible.discard(55)
            if 54 in possible: worstM.add('54');possible.discard(54)
        for i in edges:
            if i in possible:
                return str(i)
        # for i in danger:
        #     if i in possible:
        #         worstM.add(str(i))
        #         possible.discard(i)
                
        
        if possible:
            return possible.pop()
        return worstM.pop()
def quickMove(brd, tkn):
    pos = possible(brd.lower(), tkn, 'xo'[tkn.lower()=='x'])
    move = bestMove(pos, tkn, 'xo'[tkn.lower()=='x'], brd.lower())
    #snapShot(board, play, pos, '','', move)
    return int(move)
def main():
    print(quickMove(board, play))

compute()
if __name__ == '__main__': main() 
# Tianhao Chen, pd. 4, 2023