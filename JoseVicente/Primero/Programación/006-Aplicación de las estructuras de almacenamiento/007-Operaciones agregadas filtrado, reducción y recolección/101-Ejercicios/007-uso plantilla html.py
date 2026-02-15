import random
from flask import Flask,render_template

aplicacion = Flask(__name__)

@aplicacion.route("/")
def raiz():
  return render_template("index.html")

@aplicacion.route("/api")
def api():
  muestra = {1,2,3,4,5,6,7,8,9}
  sudoku = []
  for bloque in range(1,10):
    while True:
      serie = []
      for i in range(0,9):
        numero = random.randint(1,9)
        serie.append(numero)
      filtrado = set(serie)
      if filtrado == muestra:
        break;    
    sudoku.append(serie)
    
  return str(sudoku)

if __name__ == "__main__":
  aplicacion.run()
