import sys; args = sys.argv[1:]
# Tianhao Chen, pd.4
prbl = int(args[0])-40

regSol = [
  r"/^[ox.]{64}$/i", #40
  r"/^[ox]*\.[ox]*$/i", #41
  r"/^(x+o*)?\.|\.(o*x+)?$/i", #42
  r"/^.(..)*$/s", #43
  r"/^(1?0|11)([01]{2})*$/", #44
  r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i", #45
  r"/^(1?0)*1*$/", #46
  r"/^\b[bc]*a?[bc]*$/", #47
  r"/^(b|c|a[bc]*a)+$/", #48
  r"/^((2|1[20]*1)0*)+$/" #49

  ]
if prbl < len(regSol):
  print(regSol[prbl])
#Tianhao Chen, pd. 4, 2023