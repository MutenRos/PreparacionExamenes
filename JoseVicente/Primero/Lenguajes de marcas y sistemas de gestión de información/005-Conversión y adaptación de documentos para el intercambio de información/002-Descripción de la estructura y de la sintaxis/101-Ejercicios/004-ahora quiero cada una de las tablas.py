import mysql.connector

conexion = mysql.connector.connect(
  host="localhost",
  user="blog2526",
  password="blog2526",
  database="blog2526"
)

cursor = conexion.cursor() 
cursor.execute("SHOW TABLES;")

tablas = cursor.fetchall()
documento = {}
for tabla in tablas:
  
  # Select * FROM cada una de las tablas
  cursor.execute("SELECT * FROM "+tabla[0]+";")
  registros = cursor.fetchall()
  documento[tabla[0]] = registros

print(documento)
