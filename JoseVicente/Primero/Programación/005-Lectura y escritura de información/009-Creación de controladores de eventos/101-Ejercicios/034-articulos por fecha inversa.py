from flask import Flask 
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="blogexamen",
    password="Blogexamen123$",
    database="blogexamen"
)

cursor = conexion.cursor() 

aplicacion = Flask(__name__)

@aplicacion.route("/")
def raiz():
  cadena = '''
    <!doctype html>
    <html>
      <head>
        <title>El blog de Jose Vicente</title>
        <style>
          *{padding:0px;margin:0px;}
          body,html{background:grey;font-family:sans-serif;}
          header,main,footer{background:white;padding:50px;width:600px;margin:auto;}
          main{display:flex;flex-direction:column;gap:50px;}
        </style>  
      </head>
      <body>
        <header>
          <h1>El blog de Jose Vicente</h1>
        </header>
        <main>'''
  cursor.execute("SELECT * FROM posts_completos ORDER BY fecha DESC;")
  filas = cursor.fetchall()
  for fila in filas:
    cadena += '''
          <article>
            <h3>'''+fila[0]+'''</h3>
            <time>'''+fila[1]+'''</time>
            <p>'''+fila[3]+''' '''+fila[4]+'''</p>
            <p>'''+fila[2]+'''</p>
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
