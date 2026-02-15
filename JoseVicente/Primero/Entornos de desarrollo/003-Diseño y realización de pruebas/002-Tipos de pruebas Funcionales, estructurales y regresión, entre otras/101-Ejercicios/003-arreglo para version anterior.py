def operacionMatematica(operando1,operando2,operacion = None):
  if operacion == "suma":
    suma = operando1 + operando2;
    return suma
  elif operacion == "resta":
    resta = operando1 - operando2
    return resta
  
print("ejecucion 1")
print(operacionMatematica(1,2,"suma"))
print("ejecucion 2")
print(operacionMatematica(1,2,"resta"))
print("ejecucion 3")
print(operacionMatematica(1,2))

