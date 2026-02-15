def creaDivision(dividendo,divisor):
  try:
    dividendo = float(dividendo)
    divisor = float(divisor)
    if divisor != 0:
      return dividendo/divisor;
    else:
      return "infinidad"
  except:
    return 0
  
  
print(creaDivision(4,"a"))
