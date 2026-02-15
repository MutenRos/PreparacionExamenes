'''
  Programa agenda v0.1
  Jose Vicente Carratala
'''

print("Programa agenda v0.1 por Jose Vicente Carratala")

print("Selecciona una opcion:")
print("1.-Insertar clientes")
print("2.-Listar clientes")
print("3.-Actualizar clientes")
print("4.-Eliminar clientes")

clientes = ""

while True:
  opcion = input("Elige tu opcion: ")
  opcion = int(opcion)
  
  if opcion == 1:
    nombre = input("Dime el nuevo nombre del cliente: ")
    clientes += nombre+","
  elif opcion == 2:
    print("Tus clientes son: ")
    print(clientes)
  elif opcion == 3:
    print("Tus clientes son:")
    print(clientes)
    print("Quienes quieres que sean?")
    clientes = input("Introduce los nuevos clientes")
  elif opcion == 4:
    clientes = ""
    print("Tus clientes han sido borrados")
  
  
