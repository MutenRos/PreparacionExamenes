- DEJO la máquina virtual (servidor) encendida

y EN EL CLIENTE (tu propio ordenador)
1.-Abre un terminal
2.-Escribe ssh josevicente@192.168.1.114

ssh = comando de conexion remota
josevicente = usuario
@ direccion
192.168.1.114 = IP del servidor donde te conectas

Quieres aceptar la clave de conexión? yes

josevicente@josevicenteportatil:~$ ssh josevicente@192.168.1.114
hostkeys_find_by_key_hostfile: hostkeys_foreach failed for /home/josevicente/.ssh/known_hosts: Permission denied
The authenticity of host '192.168.1.114 (192.168.1.114)' can't be established.
ED25519 key fingerprint is SHA256:01yUhdMdtJMuT0isDFihz6YGycA3tWKbt52qNN3P/3g.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Failed to add the host to the list of known hosts (/home/josevicente/.ssh/known_hosts).
josevicente@192.168.1.114's password: 
client_input_hostkeys: hostkeys_foreach failed for /home/josevicente/.ssh/known_hosts: Permission denied
Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 6.8.0-84-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of lun 29 sep 2025 15:45:30 UTC

  System load:  0.0               Processes:               150
  Usage of /:   7.3% of 60.23GB   Users logged in:         1
  Memory usage: 11%               IPv4 address for enp0s3: 192.168.1.114
  Swap usage:   0%


El mantenimiento de seguridad expandido para Applications está desactivado

Se pueden aplicar 141 actualizaciones de forma inmediata.
Para ver estas actualizaciones adicionales, ejecute: apt list --upgradable

Active ESM Apps para recibir futuras actualizaciones de seguridad adicionales.
Vea https://ubuntu.com/esm o ejecute «sudo pro status»


josevicente@ubuntuserver:~$ 

