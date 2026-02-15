import mysql.connector
import json
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
  cursor = conexion.cursor(dictionary = True) 
  cursor.execute("SELECT * FROM entradas;")

  lineas = cursor.fetchall()
  lineas_json = json.dumps(lineas)

  return lineas_json
  
if __name__ == "__main__":
  aplicacion.run()
