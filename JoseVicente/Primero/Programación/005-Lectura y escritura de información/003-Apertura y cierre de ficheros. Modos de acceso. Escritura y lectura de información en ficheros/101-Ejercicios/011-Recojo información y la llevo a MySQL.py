# pip install mysql-connector-python - Si estoy en Windows
# pip3 install mysql-connector-python - Si estoy en Linux o macOS


import mysql.connector

nombre = input("Introduce el nombre del cliente")
apellidos = input("Introduce los apellidos del cliente")
telefono = input("Introduce el telefono del cliente")
email = input("Introduce el email del cliente")
localidad = input("Introduce la localidad del cliente")

conexion = mysql.connector.connect(
    host="localhost",      
    user="usuarioempresarial",    
    password="usuarioempresarial",  
    database="empresarial"      
)

cursor = conexion.cursor()

cursor.execute('''
  INSERT INTO clientes
  VALUES (
    NULL,
    "'''+nombre+'''",
    "'''+apellidos+'''",
    "'''+telefono+'''",
    "'''+email+'''",
    "'''+localidad+'''"
  )
''')
conexion.commit()

cursor.close() 

conexion.close()

