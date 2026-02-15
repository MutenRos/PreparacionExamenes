import shutil

source_folder = "/etc/apache2"
destination_folder = "/home/josevicente/backups/apache2"

shutil.copytree(source_folder, destination_folder)

