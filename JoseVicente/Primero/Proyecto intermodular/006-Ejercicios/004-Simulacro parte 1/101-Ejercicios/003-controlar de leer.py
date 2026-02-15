import sqlite3

basededatos = sqlite3.connect('./tiendaonline.db')
cursor = basededatos.cursor()

# ahora listado de productos

cursor.execute("SELECT * FROM productos")
productos = cursor.fetchall()

for producto in productos:
    print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Imagen: {producto[3]}, Precio: {producto[4]}")    


basededatos.close()

