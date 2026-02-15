import sqlite3
from flask import Flask  

aplicacion = Flask(__name__)

@aplicacion.route("/")
def raiz():
  # Me conecto a la base de datos
  conexion = sqlite3.connect("blog.db")
  conexion.row_factory = sqlite3.Row
  cursor = conexion.cursor()
  cursor.execute('SELECT * FROM articulos;')
  filas = cursor.fetchall()
  cadena = ""
  for fila in filas:
    diccionario = dict(fila)
    cadena += diccionario['titulo']+"<br>"
    cadena += diccionario['fecha']+"<br>"
    cadena += diccionario['texto']+"<br>"
    cadena += diccionario['imagen']+"<br>"
  # Y devuelvo el resultado
  return cadena
  
if __name__ == "__main__":
  aplicacion.run(host="127.0.0.1", port=5000,debug=True)


