#!/usr/bin/env python3

import shutil
import os
import datetime

source_folder = "/etc/apache2"
backup_root = "/home/josevicente/backups/apache2"

# Crear nombre de carpeta con fecha y hora: YYYY-MM-DD-HH-MM-SS
timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
destination_folder = os.path.join(backup_root, timestamp)

# Asegurar que existe la carpeta raíz de backups
os.makedirs(backup_root, exist_ok=True)

# Copiar el árbol, copiando symlinks como symlinks e ignorando los que estén rotos
shutil.copytree(
    source_folder,
    destination_folder,
    symlinks=True,
    ignore_dangling_symlinks=True
)

print("Copia completada en:", destination_folder)

