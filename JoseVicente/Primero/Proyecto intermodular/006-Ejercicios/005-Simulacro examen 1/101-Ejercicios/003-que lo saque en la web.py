import mysql.connector
from flask import Flask

aplicacion = Flask(__name__)

conexion = mysql.connector.connect(
  host="localhost",
  user="blog2526",
  password="blog2526",
  database="blog2526"
)

@aplicacion.route("/")
def raiz():
  cursor = conexion.cursor() 
  cursor.execute("SELECT * FROM entradas_con_autores;")
  cadena = ""
  lineas = cursor.fetchall()
  for linea in lineas:
    cadena += "|"+linea[0]+"|"+linea[1]+"|"+linea[2]+"|"+linea[3]+"|"+linea[4]+"|"+linea[5]
  return cadena
  
if __name__ == "__main__":
  aplicacion.run()
