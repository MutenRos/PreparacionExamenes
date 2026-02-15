import random
muestra = {1,2,3,4,5,6,7,8,9}

while True:
  serie = []

  for i in range(0,9):
    numero = random.randint(1,9)
    serie.append(numero)

  filtrado = set(serie)
  if filtrado == muestra:
    print("Es igual")
    break;
    
print(muestra)
print(filtrado)
print(serie)
