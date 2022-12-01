import re
i = '"Lanyon, you remember your vows: what follows is under the seal of our profession.'
s = re.findall(r'"[^"]+\.', i)
print(s)
print(i[-1])






# cacheChan ={}
# def change(amt, coinList):
#     key = (amt, *coinList)
#     if key in cacheChan: return cacheChan[key]
#     if amt <= 0: return amt ==0 
#     elif not coinList: return 0
#     else: 
#         val = change(amt-coinList[0], coinList) + change(amt, coinList[1:])
#     cacheChan[key] = val
#     return val
# print(change(10000, [100,50,25,10,5,1]))

# def alphabeta(brd,tkn,a, b):
#     if no possible for token:
#         if no pos for enemy:
#             return score
#         ab = recurse with alphabeta
#         return right thing
#     best = a-1
#     for v in possible moves for tkn:
#         ab = alphabeta(makemove(),-b,-a)
#         score = -ab[0]
#         if score < a: continue
#         if score > b: return [score]
#         update best
#         a = score+1
#     return best