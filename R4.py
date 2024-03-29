import sys; args = sys.argv[1:]
# Tianhao Chen, pd.4
prbl = int(args[0])-60

regSol = [
  r"/^(1|0(?!10))*$/", #60
  r"/^((?!(010|101))[01])*$/", #61
  r"/^(0|1)([01]*\1)?$/", #62
  r"/\b((\w)(?!\w*\2\b))+\b/i", #63
  r"/\b\w*((\w)\w*(\w)\w*(\2\w*\3|\3\w*\2)|(\w)\w*\5\w*(\w)\w*\6)\w*/i", #64
  r"/(?=(\w)+(\w*\1\w*){2})\b((\w)(?!\w*\4)|\1)+\b/i",#65
  r"/\b(?!\w*([aeiou])\w*\1)(?=(\w*[aeiou]){5})\w*/i", #66
  r"/(?=(0|10*1)*$)^[01]([01]{2})*$/", #67
  r"/^(?!0\d)(0|1(01*0)*1)+$/", #68
  r"/^(?!(0|1(01*0)*1)+$)[01]+$/" #69
  ]
if prbl < len(regSol):
  print(regSol[prbl])
#Tianhao Chen, pd. 4, 2023
