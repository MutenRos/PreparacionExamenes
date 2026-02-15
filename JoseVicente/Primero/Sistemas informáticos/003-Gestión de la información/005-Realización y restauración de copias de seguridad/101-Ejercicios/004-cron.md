// Nuestro crontab de usuario
crontab -e

// Editar el crontab del root del sistema
sudo crontab -e

// Crear copia de seguridad cada minuto

* * * * * /usr/bin/python3 /var/www/html/dam2526/Primero/Sistemas\ informáticos/003-Gestión\ de\ la\ información/005-Realización\ y\ restauración\ de\ copias\ de\ seguridad/101-Ejercicios/005-ejecutarcopia.py >> /var/log/ejecutarcopia.log 2>&1


