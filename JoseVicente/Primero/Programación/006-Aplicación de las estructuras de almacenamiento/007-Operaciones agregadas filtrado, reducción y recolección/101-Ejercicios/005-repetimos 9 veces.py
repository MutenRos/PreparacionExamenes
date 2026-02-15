import random
muestra = {1,2,3,4,5,6,7,8,9}

sudoku = []

for bloque in range(1,10):
  while True:
    serie = []
    for i in range(0,9):
      numero = random.randint(1,9)
      serie.append(numero)
    filtrado = set(serie)
    if filtrado == muestra:
      break;    
  sudoku.append(serie)
  
print(sudoku)
