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
  cadena = '''
  <!doctype html>
  <html>
    <head>
       <style>
          html,body{background:grey;}
          main{background:white;width:600px;margin:auto;padding:20px;}
       </style>
    </head>
    <body>
      <main>
  '''
  tuplas = cursor.fetchall()
  for tupla in tuplas:
    cadena += '''
      <article>
        <h3>'''+tupla[1]+'''</h3>
        <p>'''+tupla[2]+'''</p>
      </article>
    '''
  cadena += '''
      </main>
    </body> 
  </html>
  '''
  return cadena
    
if __name__ == "__main__":
  aplicacion.run()
