# pip install flask

from flask import Flask             

aplicacion = Flask(__name__)

@aplicacion.route("/")
def raiz():
  cadena = '''
  <style>
    body{background:grey;}
    h1{color:white;text-align:center;}
    article{background:white;padding:20px;margin:auto;width:500px;}
  </style>
  <h1>El blog Python de Jose Vicente</h1>
  '''
  articulos = [
    "Primer artículo",
    "Segundo artículo",
    "Tercer artículo",
    "Cuarto artículo",
    "..."
  ]
  for articulo in articulos:
    cadena += '''<article>
      <h2>'''+articulo+'''</h2>
      <p>Este será el contenido del artículo</p>
    </article>'''
  return cadena
  
if __name__ == "__main__":
  aplicacion.run(host="192.168.1.235", port=8080,debug=True)
