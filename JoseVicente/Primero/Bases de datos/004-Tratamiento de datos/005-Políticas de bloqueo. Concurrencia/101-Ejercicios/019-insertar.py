import sqlite3

basededatos = sqlite3.connect("empresa.db")

cursor = basededatos.cursor()

cursor.execute('''
  INSERT INTO clientes
  VALUES (
    NULL,
    'Juan',
    'Garcia Lopez',
    'juan@jocarsa.com',
    'La calle de Juan'
  );
''')

basededatos.commit()

