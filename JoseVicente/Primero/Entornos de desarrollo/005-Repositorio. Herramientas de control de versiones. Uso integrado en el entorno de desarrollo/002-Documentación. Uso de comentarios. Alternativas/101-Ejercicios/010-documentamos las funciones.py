'''
Programa para gestionar una base de datos de clientes utilizando SQLite.
Permite insertar nuevos clientes y ver la lista de clientes existentes.
Utiliza una tabla llamada 'clientes' con los campos: id, nombre, edad y email.  
'''
import sqlite3

basededatos = sqlite3.connect('clientes.db')
cursor = basededatos.cursor()

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
    No tiene parámetros ni retorna valores.'''
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

while True:                                     # Bucle principal del programa  
    imprimeMenu()                               # Muestra el menú de opciones
    opcion = input("Opción (1/2): ")            # Solicita la opción al usuario
    if opcion == '1':                           # Si la opcion seleccionada es la 1
        insertar_cliente()                      # Llama a la función para ver los clientes
    elif opcion == '2':                         # Si la opcion seleccionada es la 2 
        seleccionarClientes()                   # Llama a la función para insertar un cliente
    else:                                       # Si la opcion no es válida
        print("Opción no válida. Por favor, seleccione 1 o 2.") #   Mensaje de error
    continuar = input("¿Desea realizar otra operación? (s/n): ")# Pregunta si desea continuar
    if continuar.lower() != 's':                # Si la respuesta no es S 
        break                                   # Sale del bucle principal

basededatos.close()


