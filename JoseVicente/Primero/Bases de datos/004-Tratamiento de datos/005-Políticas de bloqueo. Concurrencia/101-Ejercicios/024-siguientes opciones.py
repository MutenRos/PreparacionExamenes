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
tabla = ""
tablas = [0]
for fila in filas:
  print(str(contador)+"-"+fila[0])
  contador += 1
  tablas.append(fila[0])
opcion = input("Tu opción elegida: ")
tabla = tablas[int(opcion)]
print("\033[2J")  # Borrar pantalla
print("\033[0;0H", end="")
print("La tabla seleccionada es: "+tabla)
print("Selecciona una operación: ")
print("1.-Crear un registro")
print("2.-Listado de registros")
print("3.-Actualizar un registro")
print("4.-Eliminar un registro")
opcion = input("Selecciona una opcion: ")
