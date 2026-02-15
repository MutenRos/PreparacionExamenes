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
    cadena += '''
      <article>
        <h3>'''+linea[3]+'''</h3>
        <p>'''+linea[4]+'''</p>
        <img src="'''+linea[5]+'''">
      </article>
    
    '''
  return cadena
  
if __name__ == "__main__":
  aplicacion.run()
