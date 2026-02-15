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
  cadena = '''
  <!doctype html>
  <html>
    <head>
      <title>Blog de Jose Vicente</title>
      <style>
        body{background:lightgray;font-family:sans-serif;}
        header,main,footer{width:600px;background:white;margin:auto;padding:20px;}
        main{display:grid;grid-template-columns: auto auto auto;gap:20px;}
        article img{width:100%;}
      </style>
      
    </head>
    <body>
      <header>
        <h1>El blog de Jose Vicente</h1>
      </header>
      <main>
  '''
  for fila in filas:
    diccionario = dict(fila)
    cadena += '<article>'
    cadena += '<h3>'+diccionario['titulo']+"</h3>"
    cadena += '<time>'+diccionario['fecha']+"</time>"
    cadena += '<p>'+diccionario['texto']+"</p>"
    cadena += '<img src="static/'+diccionario['imagen']+'" alt="Imagen de blog">'
    cadena += '</article>'
  # Y devuelvo el resultado
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
  aplicacion.run(host="127.0.0.1", port=5000,debug=True)


