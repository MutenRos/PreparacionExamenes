import sqlite3

conexion = sqlite3.connect("blog.db")

cursor = conexion.cursor()

cursor.execute('SELECT * FROM articulos;')

filas = cursor.fetchall()

for fila in filas:
  print(fila)
