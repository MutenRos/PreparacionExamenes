import os
import time

carpeta = "/var/www/html/dam2526"
# 📂
total = 0

for directorio,carpetas,archivos in os.walk(carpeta):

  profundidad = directorio.replace(carpeta, "").count(os.sep)
  sangria = "│   " * profundidad
  print(sangria,"📂",directorio)
  for archivo in archivos:
    ruta = os.path.join(directorio,archivo)
    try:
      estadisticas = os.stat(ruta)
      tamanio = estadisticas.st_size
      total = total + tamanio
      fecha = time.strftime('%y-%m-%d-%H:%m:%s',time.localtime(estadisticas.st_mtime))
      print(sangria," 📃",archivo)
      
    except:
      print("No he podido acceder al archivo")

print("el total de la carpeta en bytes es: ",total,"bytes")
print("el total de la carpeta en KB es: ",total/1024,"KB")
print("el total de la carpeta en MB es: ",total/(1024*1024),"MB")
