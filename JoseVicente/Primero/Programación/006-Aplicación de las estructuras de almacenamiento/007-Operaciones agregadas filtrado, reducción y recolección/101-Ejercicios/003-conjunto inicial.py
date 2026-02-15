import random
muestra = {1,2,3,4,5,6,7,8,9}

serie = []

for i in range(0,9):
  numero = random.randint(1,9)
  serie.append(numero)

filtrado = set(serie)
print(muestra)
print(filtrado)
print(serie)

if filtrado == muestra:
  print("Es igual")
else:
  print("No es igual")
