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

def limpiaPantalla():
  print("\033[2J\033[H", end="")  # Limpiar pantalla

def ponNegrita():
  print("\u001b[1m")  # Negrita
  
def reiniciaEstilo():
  print("\u001b[0m")  # Reiniciamos estilo

def ponColor(r,b,g):
  print("\u001b[38;2;"+str(r)+";"+str(g)+";"+str(b)+"m", end="")

clientes = []

archivo = open("clientes.bin",'rb')
clientes = pickle.load(archivo)
archivo.close()

limpiaPantalla()

while True:
  limpiaPantalla()
  ponNegrita()
  ponColor(255,0,0)
  print("Agenda de clientes")
  reiniciaEstilo()
  print("Selecciona una opcion:")
  ponColor(255,0,0)
  print("1.-Insertar un cliente")
  ponColor(0,255,0)
  print("2.-Listar clientes")
  ponColor(0,0,255)
  print("3.-Actualizar clientes")
  ponColor(255,255,0)
  print("4.-Eliminar clientes")
  ponColor(0,255,255)
  print("5.-Guardar clientes")
  opcion = input("Selecciona una opcion: ")
  opcion = int(opcion)

  if opcion == 1:
    limpiaPantalla()
    print("Vamos a insertar un cliente")
    nuevocliente = Cliente()
    nuevocliente.nombre = input("Indica el nombre del cliente: ")
    nuevocliente.apellidos = input("Indica los apellidos del cliente: ")
    nuevocliente.email = input("Indica el email del cliente: ")
    clientes.append(nuevocliente) # a la lista de clientes le ponemos el nuevo cliente
  elif opcion == 2:
    limpiaPantalla()
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

