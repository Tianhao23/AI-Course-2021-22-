import random
import subprocess, sys

constraints = {}
for i in range(64):
    constraints[i] = []
    n = [i - j * 8 for j in range(1, i//8 + 1)]
    s = [i + j * 8 for j in range(1, (63 - i)//8 + 1)]
    w = [i - j for j in range(1, i % 8 + 1)]
    e = [i + j for j in range(1, 8 - i % 8)]
    nw = [i - j * 9 for j in range(1, min(i % 8, i//8) + 1)]
    ne = [i - j * 7 for j in range(1, min(8 - i % 8, i//8 + 1))]
    sw = [i + j * 7 for j in range(1, min((63 - i)//8, i % 8) + 1)]
    se = [i + j * 9 for j in range(1, min((63 - i)//8 + 1, 8 - i % 8))]
    lst = [n, s, w, e, nw, ne, sw, se]
    for j in lst:
        if len(j) > 1:
            constraints[i].append(j)

filename = input()

rcount = 0
pcount = 0
default = '.' * 27 + 'OX' + '.' * 6 + 'XO' + '.' * 27

def format(board):
    for i in range(8):
        print(board[i * 8:i * 8 + 8])
    print()

def valid(board, pos, t1, t2):
    for i in constraints[pos]:
        flag = False
        for j in i:
            if board[j] == t2:
                flag = True
            elif board[j] == t1 and flag:
                return True
            else:
                break
    return False

def findpossible(board, t1, t2):
    possible = []
    for i in range(64):
        if board[i] == '.' and valid(board, i, t1, t2):
            possible.append(i)
    return possible

def randommove(board, token1, token2):
    pos = findpossible(board, token1, token2)
    if not pos:
        return -1
    rand = random.randint(0, len(pos) - 1)
    return pos[rand]

def placemove(board, pos, token1, token2):
    result = list(board)
    result[pos] = token1
    for i in constraints[pos]:
        flag = False
        change = []
        for j in i:
            if board[j] == token2:
                flag = True
                change.append(j)
            elif board[j] == token1 and flag:
                for k in change:
                    result[k] = token1
                break
            else:
                break
    return ''.join(result)

def endgame(board, token1, token2):
    one, two = 0, 0
    for i in board:
        if i == token1:
            one += 1
        elif i == token2:
            two += 1
    return one, two

def move(bd, token1, token2):
    board = str(bd)
    randmove = randommove(board, token1, token2)
    if randmove != -1:
        board = placemove(board, randmove, token1, token2)
        playermove = int(subprocess.check_output([sys.executable, filename, board, token2])[:-2])
        if playermove != -1:
            board = placemove(board, playermove, token2, token1)
    else:
        playermove = int(subprocess.check_output([sys.executable, filename, board, token2])[:-2])
        if playermove == -1:
            one, two = endgame(board, token1, token2)
            global rcount, pcount
            if one > two:
                one = 64 - two
            elif two > one:
                two = 64 - one
            rcount += one
            pcount += two
            return board, -1
        else:
            board = placemove(board, playermove, token2, token1)
    return board, 0

for k in range(50):
    token1 = 'X'
    token2 = 'O'
    puzzle = default
    while True:
        puzzle, i = move(puzzle, token1, token2)
        if i == -1:
            print(puzzle)
            break
for k in range(50):
    token1 = 'O'
    token2 = 'X'
    puzzle = default
    playermove = int(subprocess.check_output([sys.executable, filename, puzzle, token2])[:-2])
    puzzle = placemove(puzzle, playermove, token2, token1)
    while True:
        puzzle, i = move(puzzle, token1, token2)
        if i == -1:
            print(puzzle)
            break

print(rcount, pcount)