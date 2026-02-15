from flask import Flask  
import sqlite3

aplicacion = Flask(__name__)

@aplicacion.route("/")
def raiz():
  # BLOQUE SQLITE
  conexion = sqlite3.connect("tiendaonline.db")
  conexion.row_factory = sqlite3.Row
  cursor = conexion.cursor()
  cursor.execute('SELECT * FROM productos;')
  filas = cursor.fetchall()
  for fila in filas:
    print(fila)
  # BLOQUE FLASK
  return '''
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
          <article>
            <img src="">
            <h3>Articulo</h3>
            <p>5.54€</p>
          </article>
          <article>
            <img src="">
            <h3>Articulo</h3>
            <p>5.54€</p>
          </article>
          <article>
            <img src="">
            <h3>Articulo</h3>
            <p>5.54€</p>
          </article>
          <article>
            <img src="">
            <h3>Articulo</h3>
            <p>5.54€</p>
          </article>
          <article>
            <img src="">
            <h3>Articulo</h3>
            <p>5.54€</p>
          </article>
          <article>
            <img src="">
            <h3>Articulo</h3>
            <p>5.54€</p>
          </article>
          <article>
            <img src="">
            <h3>Articulo</h3>
            <p>5.54€</p>
          </article>
          <article>
            <img src="">
            <h3>Articulo</h3>
            <p>5.54€</p>
          </article>
          <article>
            <img src="">
            <h3>Articulo</h3>
            <p>5.54€</p>
          </article>
          <article>
            <img src="">
            <h3>Articulo</h3>
            <p>5.54€</p>
          </article>
          <article>
            <img src="">
            <h3>Articulo</h3>
            <p>5.54€</p>
          </article>
        </main>
        <footer>
        </footer>
      </body>
    </html>
  '''
  
if __name__ == "__main__":
  aplicacion.run()
