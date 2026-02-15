import os

carpeta = "/var/www/html/dam2526/Primero/Programación"

for ruta, subdirs, archivos in os.walk(carpeta):
    print("Ruta:", ruta)
    print("Subcarpetas:", subdirs)
    print("Archivos:", archivos)
    print("-" * 40)

