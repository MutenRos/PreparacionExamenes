def creaDivision(dividendo,divisor):
  return dividendo/divisor;
  
try:
  for divid in range(-100,100):
    for divis in range(-100,100):
      print(creaDivision(divid,divis))
except:
  print("No ha aguantado")
