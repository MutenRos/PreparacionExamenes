from flask import Flask  
import sqlite3

aplicacion = Flask(__name__)

@aplicacion.route("/")
def raiz():
  ####################### INICIO DE LA CADENA
  cadena = ''
  ####################### CABEZA ESTATICA
  cadena += '''
  <!doctype html>
    <html lang="es">
      <head>
        <title>Tienda online</title>
        <meta charset="utf-8">
        <style>
          body,html{background:grey;font-family:sans-serif;text-align:center;}
          header,footer,main{background:white;width:600px;margin:auto;padding:20px;}
          main{display:grid;grid-template-columns:auto auto auto;gap:20px;}
          main article img{
            width:100%;height:100px;background:grey;
          }
        </style>
      </head>
      <body>
        <header>
          <h1>Tienda online</h1>
        </header>
        <main>
  '''
  #################### CUERPO DINAMICO
  conexion = sqlite3.connect("tiendaonline.db")
  conexion.row_factory = sqlite3.Row
  cursor = conexion.cursor()
  cursor.execute('SELECT * FROM productos;')
  filas = cursor.fetchall()
  for fila in filas:
    cadena += '''
          <article>
            <img src="">
            <h3>'''+fila['nombre']+'''</h3>
            <p>'''+fila['precio']+'''</p>
          </article>
         '''
  ################### PIE DE PAGINA ESTATICO
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
