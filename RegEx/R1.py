import sys; args = sys.argv[1:]
# Tianhao Chen, pd.4
prbl = int(args[0])-30

regSol = [
  r"/^0$|^10[01]$/", #30
  r"/^[01]*$/", #31
  r"/0$/", #32
  r"/\w*[aeiou]\w*[aeiou]\w*/i", #33
  r"/^1[01]*0$|^0$/", #34
  r"/^[01]*110[01]*$/", #35
  r"/^.{2,4}$/s", #36
  r"/^\d{3} *-? *\d{2} *-? *\d{4}$/", #37
  r"/^.*?d\w*/im", #38
  r"/^[01]?$|^0[01]*0$|^1[01]*1$/" #39
  ]

if prbl < len(regSol):
  print(regSol[prbl])
#Tianhao Chen, pd. 4, 2023