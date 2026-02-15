import mysql.connector
import json

conexion = mysql.connector.connect(
  host="localhost",
  user="blog2526",
  password="blog2526",
  database="blog2526"
)

cursor = conexion.cursor(dictionary=True) 
cursor.execute("SHOW TABLES;")

tablas = cursor.fetchall()
documento = {}
for tabla in tablas:
  
  # Select * FROM cada una de las tablas
  cursor.execute("SELECT * FROM "+tabla['Tables_in_blog2526']+";")
  registros = cursor.fetchall()
  documento[tabla['Tables_in_blog2526']] = registros

documento_json = json.dumps(documento, indent=4, ensure_ascii=False)
print(documento_json)
