from flask import Flask, render_template 

aplicacion = Flask(__name__)

@aplicacion.route("/")
def raiz():
  return render_template("index.html")
  
@aplicacion.route("/sobremi")
def sobremi():
  return render_template("sobremi.html")
  
@aplicacion.route("/contacto")
def contacto():
  return render_template("contacto.html")
  
if __name__ == "__main__":
  aplicacion.run()
