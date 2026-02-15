import sqlite3

basededatos = sqlite3.connect("empresa.db")

cursor = basededatos.cursor()

cursor.execute('''
  DELETE FROM clientes
  WHERE Identificador = 2;
''')

basededatos.commit()

