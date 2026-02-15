import os

columnas, filas = os.get_terminal_size()
print("\033[2J") # Borrar pantalla
texto = "jocarsa | green"
print("\033[32m") # Texto verde

centrox = round(columnas/2)
centroy = round(filas/2)
iniciox = round(centrox - len(texto)/2)
print(f"\033[{centroy};{iniciox}H", end="")
print(texto)
input()

print("\033[2J") # Borrar pantalla
print(f"\033[4;4H","➕ 1.-Listar clientes")
print(f"\033[5;4H","👁️‍🗨️ 2.-Listado de clientes")
print(f"\033[6;4H","🖋 3.-Editar un cliente")
print(f"\033[7;4H","❌ 4.-Eliminar un cliente")
