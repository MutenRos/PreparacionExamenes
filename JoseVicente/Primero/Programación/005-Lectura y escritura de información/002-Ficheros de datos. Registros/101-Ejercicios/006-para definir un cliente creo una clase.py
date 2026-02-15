'''
  Agenda de clientes v.0.1 por Jose Vicente Carratala
  Este programa gestiona y mantiene una base de datos de clientes
'''

class Cliente():
  def __init__(self):
    self.nombre = ""
    self.apellidos = ""
    self.email = ""

print("Agenda de clientes")

print("Selecciona una opcion:")
print("1.-Insertar un cliente")
print("2.-Listar clientes")
print("3.-Actualizar clientes")
print("4.-Eliminar clientes")
opcion = input("Selecciona una opcion")
opcion = int(opcion)

if opcion == 1:
  print("Vamos a insertar un cliente")
elif opcion == 2:
  print("Vamos a listar los clientes")
elif opcion == 3:
  print("Vamos a actualizar los clientes")
elif opcion == 4:
  print("Vamos a eliminar clientes")

