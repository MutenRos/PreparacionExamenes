ssh josevicente@192.168.1.176

sudo apt install apache2

cd /var/www/html

Cambiamos el archivo original

sudo mv index.html index_old.html

sudo nano index.html
Y dentro ponemos un hola mundo

Y comprobamos en el navegador:
http://192.168.1.176


