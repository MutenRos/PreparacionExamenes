'''
Programa para gestionar una base de datos de clientes utilizando SQLite.
Permite insertar nuevos clientes y ver la lista de clientes existentes.
Utiliza una tabla llamada 'clientes' con los campos: id, nombre, edad y email.  
'''
from funcionesbasededatos import imprimeMenu, insertar_cliente, seleccionarClientes, crear_tabla

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




