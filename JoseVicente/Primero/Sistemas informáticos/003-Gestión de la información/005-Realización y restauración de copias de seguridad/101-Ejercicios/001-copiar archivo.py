import shutil

source = "/etc/apache2/apache2.conf"
destination_folder = "/home/josevicente/backups"

shutil.copy(source, destination_folder)

