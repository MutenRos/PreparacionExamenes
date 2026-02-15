import mysql.connector
from flask import Flask

aplicacion = Flask(__name__)

conexion = mysql.connector.connect(
  host="localhost",
  user="portafolio",
  password="portafolio",
  database="portafolio"
)

@aplicacion.route("/")
def raiz():
  cursor = conexion.cursor() 
  cursor.execute("SELECT * FROM piezas_con_autores;")
  cadena = ""
  lineas = cursor.fetchall()
  for linea in lineas:
    cadena += linea[0]+linea[1]+linea[2]+"<br>"
  return cadena
  
if __name__ == "__main__":
  aplicacion.run()
