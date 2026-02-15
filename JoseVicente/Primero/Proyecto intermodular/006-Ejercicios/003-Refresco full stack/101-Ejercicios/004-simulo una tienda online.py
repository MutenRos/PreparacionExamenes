from flask import Flask  

aplicacion = Flask(__name__)

@aplicacion.route("/")
def raiz():

  return '''
    <!doctype html>
    <html lang="es">
      <head>
        <title>Tienda online</title>
        <meta charset="utf-8">
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
