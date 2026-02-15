import sqlite3

def imprimeMenu():
    '''
    Muestra el menú de opciones al usuario.
    No tiene parámetros ni retorna valores.
    '''
    print("Seleccione una opción:")
    print("1. Añadir cliente")
    print("2. Ver clientes")

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

def crear_tabla():
    '''
    Crea la tabla 'clientes' en la base de datos si no existe.
    No tiene parámetros ni retorna valores.
    '''
    basededatos = sqlite3.connect('clientes.db')
    cursor = basededatos.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    ''')    
    basededatos.commit()