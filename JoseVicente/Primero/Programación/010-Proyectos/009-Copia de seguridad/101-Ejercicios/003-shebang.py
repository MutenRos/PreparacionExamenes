#!/usr/bin/python3

import shutil
import os
from datetime import datetime

source = "/home/josevicente/Escritorio/Escritorio/imagenes"
base_destination = "/var/www/html/dam2526/Primero/Programación/010-Proyectos/009-Copia de seguridad/101-Ejercicios/copia"

# Create datetime-based folder name
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
destination = os.path.join(base_destination, timestamp)

# Create destination directory
os.makedirs(destination, exist_ok=True)

# Copy contents
shutil.copytree(source, destination, dirs_exist_ok=True)

