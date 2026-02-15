# pip install flask

from flask import Flask             

aplicacion = Flask(__name__)

@aplicacion.route("/")
def raiz():
  return "<h1>Esto es HTML desde Flask</h1>"
  
if __name__ == "__main__":
  aplicacion.run(host="192.168.1.78", port=8080,debug=True)
