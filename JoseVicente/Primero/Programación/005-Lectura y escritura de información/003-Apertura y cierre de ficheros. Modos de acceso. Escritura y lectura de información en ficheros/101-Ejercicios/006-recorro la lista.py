archivo = open("clientes.txt","r")
lineas = archivo.readlines()
for linea in lineas:
  print(linea)
archivo.close()
