import mysql.connector
import json

conexion = mysql.connector.connect(
  host="localhost",
  user="blog2526",
  password="blog2526",
  database="blog2526"
)

cursor = conexion.cursor(dictionary = True) 
cursor.execute("SELECT * FROM entradas;")

lineas = cursor.fetchall()
lineas_json = json.dumps(lineas)

print(lineas_json)
