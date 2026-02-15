import sqlite3

print("\033[2J")  # Borrar pantalla
print("\033[0;0H", end="")
print("Programa de gestión")
print("Selecciona una entidad:")

basededatos = sqlite3.connect("empresa.db")
cursor = basededatos.cursor()
cursor.execute('''
  SELECT name 
  FROM sqlite_master 
  WHERE type='table'
  ORDER BY name;
  ''')
contador = 1
filas = cursor.fetchall()
for fila in filas:
  print(str(contador)+"-"+fila[0])
  contador += 1
opcion = input("Tu opción elegida: ")
