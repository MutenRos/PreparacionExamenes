from flask import Flask  

aplicacion = Flask(__name__)

@aplicacion.route("/")
def raiz():
  return "Esta es la página principal"
  
@aplicacion.route("/sobremi")
def sobremi():
  return "Esta es la página sobre mi"
  
@aplicacion.route("/contacto")
def contacto():
  return "Esta es la página de contacto"

if __name__ == "__main__":
  aplicacion.run()
