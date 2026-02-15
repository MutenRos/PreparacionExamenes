import mysql.connector

conexion = mysql.connector.connect(
  host="localhost",
  user="portafolio",
  password="portafolio",
  database="portafolio"
)

cursor = conexion.cursor()

peticion = cursor.execute("SELECT * FROM piezas;")

tuplas = cursor.fetchall()
for tupla in tuplas:
  print(tupla)
