def operacionMatematica(operando1,operando2,operacion):
  if operacion == "suma":
    suma = operando1 + operando2;
    return suma
  elif operacion == "resta":
    resta = operando1 - operando2
    return resta
  

print(operacionMatematica(1,2,"suma"))

print(operacionMatematica(1,2))

