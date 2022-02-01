import sys; args = sys.argv[1:]
# Tianhao Chen, pd.4
prbl = int(args[0])-60

regSol = [
  r"/^((?!010)[01])*$/", #60
  r"/^((?!(010|101))[01])*$/", #61
  r"/^(0|1)([01]*\1)?$/", #62
  r"/\b(?=\w*(\w))(?!\w*\1\w+)\w*/i", #63
  r"/\b\w*((\w)\w*(\w)\w*(\2\w*\3|\3\w*\2)|(\w)\w*\5\w*(\w)\w*\6)\w*/i", #64
  r"/\b((\w)*(?!\w*\2)(\w)*(?=\w*\4{3,})(\w)*(?!\w*\6))+/",#65
  r"/\b(?=\w*a)(?=\w*e)(?=\w*i)(?=\w*o)(?=\w*u)(?!\w*([aeiou])\w*\1)\w*/i", #66
  r"/^((?=)(?=)$/", #67
  r"//", #68
  r"//" #69
  ]
if prbl < len(regSol):
  print(regSol[prbl])
#Tianhao Chen, pd. 4, 2023
