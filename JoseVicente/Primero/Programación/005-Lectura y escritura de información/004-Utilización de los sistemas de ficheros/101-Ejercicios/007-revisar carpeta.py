import os

carpeta = "/home/josevicente/Imágenes/Capturas de pantalla"

for directorio,carpetas,archivo in os.walk(carpeta):
  print(directorio)
  print(carpetas)
  print(archivo)
  
