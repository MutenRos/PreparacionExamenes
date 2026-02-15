import sqlite3

basededatos = sqlite3.connect("empresa.db")

cursor = basededatos.cursor()

cursor.execute('''
  UPDATE clientes
  SET direccion = 'La otra calle de Juan'
  WHERE Identificador = 2;
''')

basededatos.commit()

