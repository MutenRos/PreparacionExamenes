import mysql.connector

# Me conecto a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="usuarioempresarial",
    password="usuarioempresarial",
    database="empresarial"
)

# Creo un cursor
cursor = conexion.cursor()

# Ejecuto un select
cursor.execute("SELECT * FROM productos")

# Pinto el resultado en pantalla
for fila in cursor.fetchall():
    print(fila)

# Cierro la conexion
cursor.close()
conexion.close()

