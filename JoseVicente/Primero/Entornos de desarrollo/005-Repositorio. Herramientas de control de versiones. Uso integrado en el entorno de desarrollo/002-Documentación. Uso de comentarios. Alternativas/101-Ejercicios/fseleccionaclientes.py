import sqlite3
def seleccionarClientes():
    '''
    Selecciona y muestra todos los clientes de la base de datos.
    No tiene parámetros ni retorna valores.
    '''
    basededatos = sqlite3.connect('clientes.db')
    cursor = basededatos.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    print("Lista de clientes:")
    for cliente in clientes:
        print(f"ID: {cliente[0]}, Nombre: {cliente[1]}, Edad: {cliente[2]}, Email: {cliente[3]}")
