import sqlite3

basededatos = sqlite3.connect('clientes.db')
cursor = basededatos.cursor()

def imprimeMenu():
    print("Seleccione una opción:")
    print("1. Añadir cliente")
    print("2. Ver clientes")

def insertar_cliente():
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
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    print("Lista de clientes:")
    for cliente in clientes:
        print(f"ID: {cliente[0]}, Nombre: {cliente[1]}, Edad: {cliente[2]}, Email: {cliente[3]}")

def crear_tabla():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    ''')    
    basededatos.commit()

print("Bienvenido al sistema de gestión de clientes.")

while True:
    imprimeMenu()
    opcion = input("Opción (1/2): ")
    if opcion == '1':
        insertar_cliente()
    elif opcion == '2':
        seleccionarClientes()
    else:
        print("Opción no válida. Por favor, seleccione 1 o 2.")
    continuar = input("¿Desea realizar otra operación? (s/n): ")
    if continuar.lower() != 's':
        break   

basededatos.close()


