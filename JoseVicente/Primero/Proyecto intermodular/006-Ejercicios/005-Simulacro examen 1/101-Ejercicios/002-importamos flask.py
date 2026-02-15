import mysql.connector
from flask import Flask

aplicacion = Flask(__name__)

conexion = mysql.connector.connect(
  host="localhost",
  user="blog2526",
  password="blog2526",
  database="blog2526"
)

cursor = conexion.cursor()

cursor.execute("SELECT * FROM entradas_con_autores;")
lineas = cursor.fetchall()
for linea in lineas:
  print("|",linea[0],"|",linea[1],"|",linea[2],"|",linea[3],"|",linea[4],"|",linea[5])
  
@aplicacion.route("/")
def raiz():
  return "Hola mundo"
  
if __name__ == "__main__":
  aplicacion.run()
