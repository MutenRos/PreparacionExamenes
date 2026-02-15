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
  cursor.execute("SELECT * FROM portafolio;")
  cadena = ""
  lineas = cursor.fetchall()
  for linea in lineas:
    cadena += "|"+str(linea[0])+"|"+str(linea[1])+"|"+str(linea[2])+"|"+str(linea[3])+"|"+str(linea[4])+"|"+str(linea[5])+"<br>"
  return cadena
  
if __name__ == "__main__":
  aplicacion.run()
