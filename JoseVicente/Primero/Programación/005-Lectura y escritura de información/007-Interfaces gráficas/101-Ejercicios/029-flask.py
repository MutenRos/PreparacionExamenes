from flask import Flask  

aplicacion = Flask(__name__)

@aplicacion.route("/")
def raiz():
  cadena = '''
    <style>
      input{
        border:2px solid blue;
        padding:5px;
        box-shadow:0px 2px 4px rgba(0,0,0,0.3) inset;
        border-radius:100px;
        text-align:center;
        text-shadow:0px 2px 2px rgba(0,0,0,0.3);
      }
    </style>
    <input type="text">
  '''
  return cadena
  
if __name__ == "__main__":
  aplicacion.run(host="127.0.0.1", port=5000,debug=True)
