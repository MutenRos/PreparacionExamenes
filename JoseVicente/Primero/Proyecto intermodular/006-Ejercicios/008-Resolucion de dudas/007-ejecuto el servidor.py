import mysql.connector
from flask import Flask

conexion = mysql.connector.connect(
  host="localhost",
  user="portafolio",
  password="portafolio",
  database="portafolio"
)

cursor = conexion.cursor()

aplicacion = Flask(__name__)

@aplicacion.route("/")
def raiz():
  peticion = cursor.execute("SELECT * FROM piezas;")
  cadena = ""
  tuplas = cursor.fetchall()
  for tupla in tuplas:
    cadena += str(tupla)
  return cadena
    
if __name__ == "__main__":
  aplicacion.run()
