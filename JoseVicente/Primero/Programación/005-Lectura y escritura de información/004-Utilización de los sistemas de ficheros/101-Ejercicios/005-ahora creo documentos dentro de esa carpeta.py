import os

try:
  os.mkdir("documentos")
except:
  print("La carpeta ya existe pero no doy error fatal")
  
print("Y ahora continuamos el programa")

archivo = open("documentos/cliente.txt",'w')
archivo.close()

