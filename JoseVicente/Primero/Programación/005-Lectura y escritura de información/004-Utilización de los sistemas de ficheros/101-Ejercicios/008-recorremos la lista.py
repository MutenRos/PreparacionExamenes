import os

carpeta = "/home/josevicente/Imágenes/Capturas de pantalla"

for directorio,carpetas,archivos in os.walk(carpeta):
  print(directorio)
  print(carpetas)
  for archivo in archivos:
    print(archivo)
  
