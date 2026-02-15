import mysql.connector

conexion = mysql.connector.connect(
  host="localhost",
  user="blog2526",
  password="blog2526",
  database="blog2526"
)

cursor = conexion.cursor() 
cursor.execute("SHOW TABLES;")

lineas = cursor.fetchall()
print(lineas)
