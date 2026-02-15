'''
  Micro lista de la compra v0.1
  Escoge entre dos opciones
  Puedes insertar tantos elementos como quieras
  (c) 2025 Jose Vicente Carratala
'''

while True:
  print("Escoge una opcion")
  print("1.-insertar un elemento")
  print("2.-Listar elementos")
  # Bloque para intentar convertir la opcion a entero
  try:
    opcion = int(input("Escoge tu opcion: "))
  except:
    print("No valido, asumo 2")
    opcion = 2
  if opcion == 1:
    archivo = open("listadelacompra.txt","a")
    elemento = input("Introduce el nombre del elemento: ")
    archivo.write(elemento+"\n")
    archivo.close()
  elif opcion == 2:
    archivo = open("listadelacompra.txt","r")
    lineas = archivo.readlines()
    for linea in lineas:
      print(linea)
    archivo.close()
