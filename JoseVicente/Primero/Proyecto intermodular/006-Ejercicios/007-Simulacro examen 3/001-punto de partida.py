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
  
  return "Hola que tal"
  
if __name__ == "__main__":
  aplicacion.run()
