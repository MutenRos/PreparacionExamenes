import sqlite3
def insertar_cliente():
    '''
    Inserta un nuevo cliente en la base de datos.
    Solicita al usuario el nombre, edad y email del cliente.
    No retorna valores.
    '''
    basededatos = sqlite3.connect('clientes.db')
    cursor = basededatos.cursor()
    nombre = input("Nombre: ")
    edad = int(input("Edad: "))
    email = input("Email: ")
    
    cursor.execute('''
    INSERT INTO clientes (nombre, edad, email)
    VALUES (?, ?, ?)
    ''', (nombre, edad, email))
    basededatos.commit()
    print("Cliente añadido exitosamente.")
