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

opcion = input("Elige tu opcion: ")
opcion = int(opcion)

clientes = ""

if opcion == 1:
  nombre = input("Dime el nuevo nombre del cliente")
  clientes += nombre+","
elif opcion == 2:
  print("Tus clientes son: ")
  print(clientes)
elif opcion == 3:
  pass
elif opcion == 4:
  pass
  
  
