import sys; args = sys.argv[1:]
# Tianhao Chen, pd.4
prbl = int(args[0])-70

regSol = [
  r"/^(?=.*a)(?=.*e)(?=.*i)(?=.*o)[a-z]*u\w*$/m", #70
  r"/^([^\WaeiouA-Z]*[aeiou]){5}[^\Waeiou]*$/m", #71
  r"/^(?=.*[^\Waeiou\s]w[^aeiou]{2})[a-z]*$/m", #72
  r"/^aa?$|^(?=([a-z])(.)(\w)).*\3\2\1$/m", #73
  r"/^[ac-su-z]*(bt|tb)[ac-su-z]*$/m", #74
  r"/^([a-z])*\1\w*$/m", #75
  r"/(.)(\w*\1){5}\w*$/m", #76
  r"/((.)\2){3}\w*$/m", #77
  r"/([^\Waeiou][aeiou]*){13}/m", #78
  r"/^(([a-z])(?!.*\2.*\2))*$/m" #79
  ]
if prbl < len(regSol):
  print(regSol[prbl])
#Tianhao Chen, pd. 4, 2023