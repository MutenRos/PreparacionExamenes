import os

columnas, filas = os.get_terminal_size()
print(columnas)
print(filas)
  
print("\033[16;18H", end="")
print("Hola mundo", end="")
