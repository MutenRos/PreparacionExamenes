import mysql.connector
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
  cursor = conexion.cursor() 
  cursor.execute("SELECT * FROM entradas_con_autores;")
  cadena = '''
  <!doctype html>
  <html>
  <head>
    <style>
      *{padding:2px;margin:2px;}
      body{background:grey;font-family:sans-serif;}
      header,main,footer{width:500px;background:white;padding:20px;margin:auto;}
      article{padding-bottom:20px;border-bottom:1px solid grey;margin-bottom:20px;}
      p{font-size:11px;}
    </style>
  </head>
  <body>
  <header>
    <h1>El blog de Jose Vicente</h1>
  </header>
  <main>
  '''
  lineas = cursor.fetchall()
  for linea in lineas:
    cadena += '''
      <article>
        <h3>'''+linea[0]+'''</h3>
        <p>'''+linea[3]+''' '''+linea[4]+''' - '''+linea[5]+'''</p>
        <time>'''+linea[2]+'''</time>
        <p>'''+linea[1]+'''</p>
      </article>
    '''
  cadena += '''
  </main>
  <footer>
  </footer>
  </body>
  </html>
  '''
  return cadena
  
if __name__ == "__main__":
  aplicacion.run()
