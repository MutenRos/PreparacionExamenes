import os

columnas, filas = os.get_terminal_size()
print("\033[2J") # Borrar pantalla
texto = "jocarsa | green"
print("\033[32m") # Texto verde

centrox = round(columnas/2)
centroy = round(filas/2)
iniciox = round(centrox - len(texto)/2)
print(iniciox)
print(f"\033[{centroy};{iniciox}H", end="")
print(texto)

