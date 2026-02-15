Primero iniciamos sesion

Lo primero que tenemos que hacer es habilitar el acceso remoto al servidor

Con el paquete OpenSSH-server

Nos permite conectarnos remotamente desde otra máquina:

EN EL SERVIDOR:
sudo apt install openssh-server
sudo = su + do
su = super user 
do = hacer
sudo = el super usuario va a hacer algo

apt = es el sistema de instalación por paquetes de Debian/Ubuntu
install = es la operación que voy a hacer
openssh-server es el nombre del paquete que voy a instalar

Ahora por ultimo quiero saber la ip de mi servidor

Para averiguar la ip:
ifconfig 

Para usar ifconfig, tengo que instalar net-tools
sudo apt install net-tools

Ahora si, averiguamos la IP:
ifconfig

HORRRORRRRRRRR: En Virtualbox la NAT está activada por defecto
La NAT no nos va a dar sino problemas
Vamos a desactivar la NAT

Como?

1.-Apagamos Ubuntu
sudo shutdown

2.-En VirtualBox entro en configuración

En red, vemos que por defecto está NAT
Lo cambiamos a "adaptador puente"

3.-Volvemos a arrancar Ubuntu

Al ejecutar ifconfig, 192.168.1.114


