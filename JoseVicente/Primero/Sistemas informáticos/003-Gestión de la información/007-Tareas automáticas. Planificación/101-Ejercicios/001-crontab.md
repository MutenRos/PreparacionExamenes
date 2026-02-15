crontab -e

m h  dom mon dow   command

minute - 0 = cada minuto 0 de cada hora
h = hora del día
dom = day of month 
mon = month
dow = day of week

0 * * * * /usr/bin/python3 /var/www/html/generadorapuntesv3/apuntes.py "/var/www/html/interfacesweb" >/dev/null 2>&1

* * * * * /usr/bin/python3 "/var/www/html/dam2526/Primero/Sistemas informáticos/003-Gestión de la información/007-Tareas automáticas. Planificación/101-Ejercicios/002-escribir.py" >/dev/null 2>&1

