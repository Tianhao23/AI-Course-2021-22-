#takes the tack that whoever's turn it is wants positive #s
#applies when symmertric with respect to 0, if swap x and os, reevaluate, should be the negative
#evaluates with respect to the token whose move it is
#use in the endgame

# def negamax(board, toPlay):
#     opposite = 'O' if toPlay=='X' else 'X'
#     if countP(board.upper(), '.') == 0 or ((not possible(board.upper(), toPlay, opposite))and (not possible(board.upper(), opposite, toPlay))):
#         diff = countP(board, toPlay) - countP(board, opposite)
#         return {diff:'yes'}
#     if not possible(board.upper(), toPlay, opposite) and possible(board.upper(), opposite, toPlay):
#         #append -1
#         return negamax(board.upper(), opposite)
#     res = {i:set()for i in range(-64,65)}
#     for mv in possible(board.upper(), toPlay, opposite):
#         nm = negamax(makeMove(board.upper(),toPlay, opposite, mv), opposite)
#         for i in nm:
#             if nm[i]:
#                 mvCategory = i
#                 for j in nm[i]:res[mvCategory].add(j)
#                 break
#         res[mvCategory].add(mv)          
#     return res
#othello 5
#keep othello4
#run if number of positions is less than 11
#determine a minimum score and an option move sequence to guarantee it
#output the word score: followed by a series of moves in reverse[::-1]
#score given from the point of view of the token given