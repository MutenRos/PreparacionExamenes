import os

carpeta = "/home/josevicente/Imágenes/Capturas de pantalla"

total = 0

for directorio,carpetas,archivos in os.walk(carpeta):
  print(directorio)
  print(carpetas)
  for archivo in archivos:
    ruta = os.path.join(directorio,archivo)
    try:
      estadisticas = os.stat(ruta)
      tamanio = estadisticas.st_size
      total = total + tamanio
    except:
      print("No he podido acceder al archivo")

print("el total de la carpeta en bytes es: ",total,"bytes")
print("el total de la carpeta en KB es: ",total/1024,"KB")
print("el total de la carpeta en MB es: ",total/(1024*1024),"MB")
