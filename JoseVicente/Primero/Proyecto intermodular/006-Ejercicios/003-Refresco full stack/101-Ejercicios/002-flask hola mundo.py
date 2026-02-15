from flask import Flask  

aplicacion = Flask(__name__)

@aplicacion.route("/")
def raiz():

  return "Hola mundo"
  
if __name__ == "__main__":
  aplicacion.run()
