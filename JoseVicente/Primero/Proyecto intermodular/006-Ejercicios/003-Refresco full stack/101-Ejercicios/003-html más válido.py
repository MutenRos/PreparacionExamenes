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
        <h1>Tienda online</h1>
      </body>
    </html>
  '''
  
if __name__ == "__main__":
  aplicacion.run()
