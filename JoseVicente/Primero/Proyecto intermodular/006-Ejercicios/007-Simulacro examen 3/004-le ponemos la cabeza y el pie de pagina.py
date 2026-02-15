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
  cadena = '''
    <!doctype html>
<html lang="es">
  <head>
    <title>El portafolio de Jose Vicente</title>
    <meta charset="utf-8">
    <style>
      body,html{background:grey;font-family:sans-serif;}
      header,main,footer{background:white;padding:20px;text-align:center;margin:auto;width:600px;}
      main{display:grid;grid-template-columns:auto auto auto;gap:20px;}
      article img{width:100%;}
    </style>
  </head>
  <body>
    <header>
      <h1>Jose Vicente Carratala</h1>
      <h2>info@jocarsa.com</h2>
    </header>
    <main>
  '''
  lineas = cursor.fetchall()
  for linea in lineas:
    cadena += '''
      <article>
        <h3>'''+linea[3]+'''</h3>
        <p>'''+linea[4]+'''</p>
        <img src="'''+linea[5]+'''">
      </article>
    
    '''
  cadena += '''
      </main>
      
    <footer>
      (c) 2025 Jose Vicente Carratala
    </footer>
  </body>
</html>
    '''
  return cadena
  
if __name__ == "__main__":
  aplicacion.run()
