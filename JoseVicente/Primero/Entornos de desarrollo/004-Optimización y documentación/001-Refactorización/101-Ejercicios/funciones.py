################## DEFINICION DE FUNCIONES #######################################3

def imprimeBienvenida():
  print("Programa agenda v0.1 por Jose Vicente Carratala")
  
def muestraMenu():
  print("Selecciona una opcion:")
  print("1.-Insertar clientes")
  print("2.-Listar clientes")
  print("3.-Actualizar clientes")
  print("4.-Eliminar clientes")

def insertarCliente():
  global clientes
  nombre = input("Dime el nuevo nombre del cliente: ")
  clientes += nombre+","
  
def listadoClientes():
  global clientes
  print("Tus clientes son: ")
  print(clientes)
  
def actualizaClientes():
  global clientes
  print("Tus clientes son:")
  print(clientes)
  print("Quienes quieres que sean?")
  clientes = input("Introduce los nuevos clientes")
  
def borraClientes():
  global clientes
  clientes = ""
  print("Tus clientes han sido borrados")
