import sys; args = sys.argv[1:]
import random, time
from o import possible, makeMove, bestMove
def show2D(brd, tkn, mv, findMovesFunc):
    # Display a snapshot:
    # Move played, 2D board, 1D board w. score, psbl moves
    # brd is a string, tkn just moved to mv
    # findMovesFunc()
    prev = tkn
    next = 'XO'[tkn=="X"]
    psblMv = findMovesFunc(brd, next, prev) # Possible moves
    if not psblMv: # If one side must pass
        psblMv = findMovesFunc(brd, (next:=tkn), 'XO'[tkn=="X"])
    brdL = [*brd] # Listify brd to show asterisks
    for m in psblMv: brdL[m] = "*"
    brdL[mv] = brdL[mv].upper() # Show most recent move
    b2 = "".join(brdL)
    print(f"'{tkn}' played to {mv}")
    print("\n".join([b2[rs:rs+8] for rs in range(0,len(b2),8)]))
    print(f"\n{brd} {brd.count('X')}/{brd.count('O')}")
    if psblMv: # If game not over, show possible moves
        print(f"Possible moves for '{next}': {sorted([*psblMv])}\n") 

def playGame(findBestMove, findMoves, makeMove, token):
    # plays a game between findBestMove and Random
    # findMove(brd, tkn)
    # findBestMove(brd, tkn, psblMoves)
    # makeMove(brd, tkn, mv, psblMoves)
    brd = '.'*27+'OX......XO'+'.'*27 # Starting board
    tknToPlay = 'X'
    transcript = [] # Transcript of the game
    while True:
        
        if not (moves:=findMoves(brd, tknToPlay, 'XO'[tknToPlay=="X"])):
            tknToPlay = 'XO'[tknToPlay=='X'] # Swap players if pass
            if not (moves:=findMoves(brd, tknToPlay, 'XO'[tknToPlay=='X'])): break
            transcript.append(-1) # Note the pass
        if tknToPlay != token: # if it's Random's turn:
            transcript.append(random.choice([*moves]))
            brd = makeMove(brd, tknToPlay, 'XO'[tknToPlay=="X"], int(transcript[-1]))
            #show2D(brd, tknToPlay, int(transcript[-1]), findMoves)
        else: # else it's Our turn
            transcript.append(findBestMove(moves, tknToPlay,'XO'[tknToPlay=="X"], brd))
            brd = makeMove(brd,  tknToPlay, 'XO'[tknToPlay=="X"], int(transcript[-1]))
            #show2D(brd, tknToPlay, int(transcript[-1]), findMoves)
        brd = brd.upper() # Just in case
        tknToPlay = 'XO'[tknToPlay=='X'] # Switch to other side
 # Game is over:
    tknCt = brd.count(token)
    #enemy = len(brd) - tknCt - brd.count('.')
    return tknCt/64
    #print(f"\nScore: Me as {token=}: {tknCt} vs Enemy: {enemy}\n")
    #xscript = [f"_{mv}"[-2:] for mv in transcript]
    #print(f"Game transcript: {''.join(xscript)}")
a = time.process_time()
print("Win Percentage:" + str(sum([playGame(bestMove, possible, makeMove, args[0].upper())for i in range(500)])/500*100)+"%")
b = time.process_time() - a
print(f'Process Time: {b}')
#playGame(bestMove, possible, makeMove, args[0].upper())