import sqlite3

conexion = sqlite3.connect("blog.db")
conexion.row_factory = sqlite3.Row

cursor = conexion.cursor()

cursor.execute('SELECT * FROM articulos;')

filas = cursor.fetchall()

for fila in filas:
  diccionario = dict(fila)
  print(diccionario['titulo'])
  print(diccionario['fecha'])
  print(diccionario['texto'])
  print(diccionario['imagen'])
