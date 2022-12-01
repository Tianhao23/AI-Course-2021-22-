import sys; args = sys.argv[1:]
# Tianhao Chen, pd.4
prbl = int(args[0])-50

regSol = [
  r"/(\w)+\w*\1\w*/i", #50
  r"/(\w)+(\w*\1){3}\w*/i", #51
  r"/^(0|1)([01]*\1)?$/", #52
  r"/(?=\w*cat)\b\w{6}\b/i", #53
  r"/(?=\w*bri)(?=\w*ing)\b\w{5,9}\b/i", #54
  r"/(?!\w*cat)\b\w{6}\b/i",#55
  r"/\b((\w)(?!\w*\2))+\b/i", #56
  r"/^((?!10011)[01])*$/", #57
  r"/\w*([aeiou])(?!\1)[aeiou]\w*/i", #58
  r"/^((?!1.1)[01])*$/" #59
  ]
if prbl < len(regSol):
  print(regSol[prbl])
#Tianhao Chen, pd. 4, 2023