'''
  Agenda de clientes v.0.1 por Jose Vicente Carratala
  Este programa gestiona y mantiene una base de datos de clientes
'''

import pickle

class Cliente():
  def __init__(self):
    self.nombre = ""
    self.apellidos = ""
    self.email = ""
    
clientes = []
print("\033[2J\033[H", end="")
print("Agenda de clientes")
while True:
  print("\033[2J\033[H", end="")
  print("Selecciona una opcion:")
  print("1.-Insertar un cliente")
  print("2.-Listar clientes")
  print("3.-Actualizar clientes")
  print("4.-Eliminar clientes")
  print("5.-Guardar clientes")
  opcion = input("Selecciona una opcion: ")
  opcion = int(opcion)

  if opcion == 1:
    print("\033[2J\033[H", end="")
    print("Vamos a insertar un cliente")
    nuevocliente = Cliente()
    nuevocliente.nombre = input("Indica el nombre del cliente: ")
    nuevocliente.apellidos = input("Indica los apellidos del cliente: ")
    nuevocliente.email = input("Indica el email del cliente: ")
    clientes.append(nuevocliente) # a la lista de clientes le ponemos el nuevo cliente
  elif opcion == 2:
    print("\033[2J\033[H", end="")
    print("Vamos a listar los clientes")
    print("Listado de clientes:")
    print("##############################")
    for cliente in clientes:
      print("Nombre: ",cliente.nombre)
      print("Apellidos: ",cliente.apellidos)
      print("Email: ",cliente.email)
      print("##############################")
    input("Pulsa una tecla para continuar....")
  elif opcion == 3:
    print("Vamos a actualizar los clientes")
  elif opcion == 4:
    print("Vamos a eliminar clientes")
  elif opcion == 5:
    print("Vamos a guardar los clientes")
    archivo = open("clientes.bin",'wb')
    pickle.dump(clientes, archivo)
    archivo.close()
    input("Pulsa una tecla para continuar...")

