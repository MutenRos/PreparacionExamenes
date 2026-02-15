import os

carpeta = "documentos"

try:
  os.mkdir(carpeta)
except:
  print("La carpeta ya existe pero no doy error fatal")
  
print("Y ahora continuamos el programa")

archivo = open(carpeta+"/cliente.txt",'w')
archivo.close()

