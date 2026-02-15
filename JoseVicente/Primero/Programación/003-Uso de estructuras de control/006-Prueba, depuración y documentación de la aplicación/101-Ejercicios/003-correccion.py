def creaDivision(dividendo,divisor):
  if divisor != 0:
    return dividendo/divisor;
  else:
    return "infinidad"
  
try:
  for divid in range(-100,100):
    for divis in range(-100,100):
      print(creaDivision(divid,divis))
  print("Ha pasado la prueba")
except:
  print("No ha aguantado")
