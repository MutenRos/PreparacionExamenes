1.-Desarrollado en local
2.-Subimos el código a un repositorio remoto (en la nube)
3.-Nos conectamos al servidor
4.-Desde el servidor traemos el código

De nuevo:

Tenemos un equipo de desarrollo 
Y tenemos un servidor de producción

1.-Primero creo un repositorio
2.-Me clono el repositorio en mi máquina de desarrollo (por ejemplo con GitHub Desktop para hacerlo fácil) - File->Clone repository
3.-Con mi editor/entorno favorito accedo a la carpeta
4.-Ahora creo lo que sea necesario
5.-Ahora realizo un commit + push (Desde GitHub Desktop)
6.-Ahora me conecto al servidor

josevicente@josevicenteportatil:~$ ssh josevicente@192.168.1.78

josevicente@ubuntuserver:~$ cd /var/www/html


7.-Ahora traigo la carpeta desde github.com (la nube) hasta mi servidor

josevicente@ubuntuserver:/var/www/html$ sudo git clone https://github.com/jocarsa/miweb.git

