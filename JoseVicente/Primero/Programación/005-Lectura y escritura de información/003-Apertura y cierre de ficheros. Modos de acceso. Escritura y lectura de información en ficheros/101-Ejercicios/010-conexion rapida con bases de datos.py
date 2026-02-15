# pip install mysql-connector-python - Si estoy en Windows
# pip3 install mysql-connector-python - Si estoy en Linux o macOS

# Primero importo el conector
import mysql.connector
# Ahora establezco una conexión con un usuario con permisos
conexion = mysql.connector.connect(
    host="localhost",       # or IP of your MySQL server
    user="usuarioempresarial",      # replace with your MySQL user
    password="usuarioempresarial",  # replace with your MySQL password
    database="empresarial"       # replace with your database name
)
# Creo un cursor para pedir cosas
cursor = conexion.cursor()
# En el el cursor, ejecuto una petición
cursor.execute("SELECT * FROM clientes")
# Obtengo los resultados de la petición
resultados = cursor.fetchall()
# Como hay muchos resultados, voy uno a uno
for fila in resultados:
    print(fila)
# Cierro el cursor
cursor.close() 
# Cierro la conexion
conexion.close()

