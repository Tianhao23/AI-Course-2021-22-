import sys; args = sys.argv[1:]
# Tianhao Chen, pd.4
prbl = int(args[0])-60

regSol = [
  r"/^(1|0(?!10))*$/", #60
  r"/^(0(?!10)|1(?!01))*$/", #61
  r"/^(0|1)([01]*\1)?$/", #62
  r"/\b((\w)(?!\w*\2\b))+\b/i", #63
  r"/(?=(\w)+\w*\1)((\w)+\w*(?!\1)\3|(\w*\1){4})\w*/i", #64
  r"/(?=(\w)+(\w*\1\w*){2})\b((\w)(?!\w*\4)|\1)+\b/i", #65
  r"/\b(?!\w*([aeiou])\w*\1)(\w*[aeiou]\w*){5}/i", #66
  r"/(?=(0|10*1)*$)^.(..)*$/", #67
  r"/^(0|(1(01*0)*10*)+)$/", #68
  r"/^1(10*1|01*(0|$))*$/" #69
  ]
if prbl < len(regSol):
  print(regSol[prbl])
#Tianhao Chen, pd. 4, 2023
