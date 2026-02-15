"""
Proyecto: Tienda Online de Tecnología
Autor: José Vicente Carratalá Sanchis
Fecha: 2025
Versión: 1.0
Framework: Flask
Base de datos: SQLite

Descripción general:
--------------------
Este proyecto implementa una tienda online básica de productos tecnológicos utilizando
el framework Flask (Python) y una base de datos SQLite. La aplicación web muestra un
listado dinámico de productos obtenidos directamente desde la base de datos y genera
una página HTML con diseño responsivo para simular el frontend de una tienda real.

Características principales:
----------------------------
- Conexión automática a la base de datos SQLite 'tiendaonline.db'.
- Obtención de los registros almacenados en la tabla 'productos'.
- Renderizado dinámico de cada producto con su nombre, descripción, imagen y precio.
- Estructura HTML con estilo CSS embebido para ofrecer una experiencia visual moderna.
- Diseño adaptable con cabecera, menú de navegación, listado de productos y pie de página.
- Interfaz sencilla con botones de "Añadir al carrito" (sin funcionalidad aún implementada).

Estructura esperada de la tabla 'productos':
--------------------------------------------
| id (INTEGER PRIMARY KEY) | nombre (TEXT) | descripcion (TEXT) | imagen (TEXT) | precio (REAL) |

Ejemplo de registro:
--------------------
(1, 'Portátil Lenovo IdeaPad', 'Portátil con procesador Ryzen 5 y 16GB RAM', 'lenovo.jpg', 799.99)

Rutas disponibles:
------------------
/        → Página principal con el listado de productos.

Modo de uso:
------------
1. Asegúrate de tener instalado Flask y SQLite3 en tu entorno de Python.
2. Crea la base de datos 'tiendaonline.db' con una tabla 'productos' y algunos registros.
3. Guarda este archivo como 'app.py' o 'tienda.py'.
4. Ejecuta el servidor con:
       python app.py
5. Abre tu navegador en http://127.0.0.1:5000/ para ver la tienda online.

Notas:
------
- Este proyecto sirve como ejemplo didáctico de integración entre Flask y SQLite.
- El carrito de compras y la gestión de usuarios pueden añadirse en versiones posteriores.
"""

import sqlite3                                  # Importamos el módulo sqlite3 para manejar la base de datos SQLite
from flask import Flask                         # Importamos Flask para crear la aplicación web
app = Flask(__name__)                           # Creamos una instancia de la aplicación Flask

@app.route('/')                                 # Definimos la ruta principal de la aplicación
def listar_productos():                         # Función para listar los productos de la tienda online

    basededatos = sqlite3.connect('./tiendaonline.db')  # Conectamos a la base de datos SQLite llamada 'tiendaonline.db'
    cursor = basededatos.cursor()               # Creamos un cursor para ejecutar consultas SQL
    cadena = '''
    <!-- Maqueta visual del front de una tienda online -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tienda Online de Tecnología</title>
   <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        header {
            background-color: #333;
            color: #fff;
            padding: 10px 0;
            text-align: center;
        }
        nav ul {
            list-style: none;
            padding: 0;
        }
        nav ul li {
            display: inline;
            margin: 0 15px;
        }
        nav ul li a {
            color: #fff;
            text-decoration: none;
        }
        .product-list {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            padding: 20px;
        }
        .product-item {
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin: 15px;
            padding: 15px;
            width: 250px;
            text-align: center;
        }
        .product-item img {
            max-width: 100%;
            height: auto;
        }
        .product-item h2 {
            font-size: 1.2em;
            margin: 10px 0;
        }
        .product-item p {
            font-size: 0.9em;
            color: #555;
        }
        .price {
            font-size: 1.1em;
            color: #e91e63;
            margin: 10px 0;
            display: block;
        }
        button {
            background-color: #28a745;
            color: #fff;
            border: none;
            padding: 10px 15px;
            cursor: pointer;
            border-radius: 5px;
        }
        button:hover {
            background-color: #218838;
        }
        footer {
            background-color: #333;
            color: #fff;
            text-align: center;
            padding: 10px 0;
            position: fixed;
            width: 100%;
            bottom: 0;
        }   
   </style>
</head>
<body>
    <header>
        <h1>Tienda Online de Tecnología</h1>
        <nav>
            <ul>
                <li><a href="#">Inicio</a></li>
                <li><a href="#">Productos</a></li>
                <li><a href="#">Ofertas</a></li>
                <li><a href="#">Contacto</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <section class="product-list">
    '''                                             # cadena inicial del HTML de la página web

    # ahora listado de productos ########################################

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    for producto in productos:
        cadena += '''
        <div class="product-item">
            <img src="/static/img/''' + producto[3] + '''" alt="''' + producto[1] + '''">
            <h2>''' + producto[1] + '''</h2>
            <p>''' + producto[2] + '''</p>
            <span class="price">$''' + str(producto[4]) + '''</span>
            <button>Añadir al carrito</button>
        </div>
        '''
    # ahora listado de productos ########################################

    cadena += '''
 </section>
    </main>
    <footer>
        <p>&copy; 2024 Tienda Online de Tecnología. Todos los derechos reservados.</p>
    </footer>
</body>
</html>
    '''                                                         # cadena final del HTML de la página web

    return cadena                                               # Devolvemos la cadena HTML completa como respuesta a la solicitud web
    basededatos.close()                                         # Cerramos la conexión a la base de datos

if __name__ == '__main__':                                      # Si este archivo se ejecuta directamente
    app.run(debug=True)                                         # Ejecutamos la aplicación Flask en modo de depuración
