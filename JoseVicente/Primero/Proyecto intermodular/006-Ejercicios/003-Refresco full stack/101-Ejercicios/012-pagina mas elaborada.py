from flask import Flask  

aplicacion = Flask(__name__)

cabeza = '<!doctype html><html><head></head><body><header><h1>La web de Jose Vicente</h1></header><main>'
pie = '</main></body></html>'
@aplicacion.route("/")
def raiz():
  return cabeza+"Esta es la página principal"+pie
  
@aplicacion.route("/sobremi")
def sobremi():
  return cabeza+"Esta es la página sobre mi"+pie
  
@aplicacion.route("/contacto")
def contacto():
  return cabeza+"Esta es la página de contacto"+pie

if __name__ == "__main__":
  aplicacion.run()
