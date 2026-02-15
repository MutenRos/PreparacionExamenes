import random
from flask import Flask, render_template, jsonify

aplicacion = Flask(__name__)


def generar_sudoku():
    # grid[row][col]
    grid = [[0 for _ in range(9)] for _ in range(9)]

    def es_valido(fila, columna, numero):
        # Comprobar fila
        if numero in grid[fila]:
            return False

        # Comprobar columna
        for f in range(9):
            if grid[f][columna] == numero:
                return False

        # Comprobar subcuadrante 3x3
        inicio_fila = (fila // 3) * 3
        inicio_columna = (columna // 3) * 3
        for f in range(inicio_fila, inicio_fila + 3):
            for c in range(inicio_columna, inicio_columna + 3):
                if grid[f][c] == numero:
                    return False

        return True

    def resolver(celda=0):
        # Si hemos rellenado las 81 celdas, ya está completo
        if celda == 81:
            return True

        fila = celda // 9
        columna = celda % 9

        numeros = list(range(1, 10))
        random.shuffle(numeros)

        for n in numeros:
            if es_valido(fila, columna, n):
                grid[fila][columna] = n
                if resolver(celda + 1):
                    return True
                # backtracking
                grid[fila][columna] = 0

        return False

    resolver()
    return grid


@aplicacion.route("/")
def raiz():
    return render_template("index2.html")


@aplicacion.route("/api")
def api():
    # sudoku es una matriz 9x9 con números del 1 al 9
    sudoku = generar_sudoku()
    # devolvemos JSON para que respuesta.json() funcione
    return jsonify(sudoku)


if __name__ == "__main__":
    aplicacion.run(debug=True)

