import sqlite3

basededatos = sqlite3.connect("empresa.db")

cursor = basededatos.cursor()

cursor.execute("SELECT * FROM clientes")
filas = cursor.fetchall()

for fila in filas:
  print(fila)
