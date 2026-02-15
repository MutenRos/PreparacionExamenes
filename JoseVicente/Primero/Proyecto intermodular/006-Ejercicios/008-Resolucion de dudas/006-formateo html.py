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

  tuplas = cursor.fetchall()
  for tupla in tuplas:
    print(tupla)
