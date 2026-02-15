def creaDivision(dividendo,divisor):
  '''
    Esta función realiza una división
    Entradas: el divisor y el dividendo
    Salidas: El resultado como número
    Notas: La función realiza validación de número e infinidad
  '''
  try:
    dividendo = float(dividendo)
    divisor = float(divisor)
    if divisor != 0:
      return dividendo/divisor;
    else:
      return "infinidad"
  except:
    return 0
