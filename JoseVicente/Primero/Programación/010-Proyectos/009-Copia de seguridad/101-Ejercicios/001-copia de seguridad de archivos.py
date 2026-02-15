import shutil

source = "/home/josevicente/Escritorio/Escritorio/imagenes"
destination = "/var/www/html/dam2526/Primero/Programación/010-Proyectos/009-Copia de seguridad/101-Ejercicios/copia"

shutil.copytree(source, destination, dirs_exist_ok=True)

