sudo apt install apache2

josevicente@debianserver:~$ sudo apt install apache2
[sudo] contraseña para josevicente: 
josevicente is not in the sudoers file.

Hacemos que josevicente sea usuario con permisos
usermod -aG sudo josevicente

Lo hago directamente desde la máquina (root):


