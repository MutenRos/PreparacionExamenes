import sqlite3
from flask import Flask
app = Flask(__name__)

@app.route('/')
def listar_productos(): 

    basededatos = sqlite3.connect('./tiendaonline.db')
    cursor = basededatos.cursor()
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
    '''
    # ahora listado de productos

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

    cadena += '''
 </section>
    </main>
    <footer>
        <p>&copy; 2024 Tienda Online de Tecnología. Todos los derechos reservados.</p>
    </footer>
</body>
</html>
    '''

    return cadena
    basededatos.close()

if __name__ == '__main__':
    app.run(debug=True)
