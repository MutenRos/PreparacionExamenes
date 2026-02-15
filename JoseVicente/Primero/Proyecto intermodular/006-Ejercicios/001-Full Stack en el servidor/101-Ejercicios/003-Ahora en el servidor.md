1.-Ahora arranco el servidor

2.-Inicio sesión en el servidor

josevicente@josevicenteportatil:~$ ssh josevicente@192.168.1.78
hostkeys_find_by_key_hostfile: hostkeys_foreach failed for /home/josevicente/.ssh/known_hosts: Permission denied
The authenticity of host '192.168.1.78 (192.168.1.78)' can't be established.
ED25519 key fingerprint is SHA256:01yUhdMdtJMuT0isDFihz6YGycA3tWKbt52qNN3P/3g.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Failed to add the host to the list of known hosts (/home/josevicente/.ssh/known_hosts).
josevicente@192.168.1.78's password: 
client_input_hostkeys: hostkeys_foreach failed for /home/josevicente/.ssh/known_hosts: Permission denied
Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 6.8.0-84-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of lun 06 oct 2025 14:02:23 UTC

  System load:  0.07              Processes:               152
  Usage of /:   8.2% of 60.23GB   Users logged in:         0
  Memory usage: 28%               IPv4 address for enp0s3: 192.168.1.78
  Swap usage:   0%


El mantenimiento de seguridad expandido para Applications está desactivado

Se pueden aplicar 141 actualizaciones de forma inmediata.
Para ver estas actualizaciones adicionales, ejecute: apt list --upgradable

Active ESM Apps para recibir futuras actualizaciones de seguridad adicionales.
Vea https://ubuntu.com/esm o ejecute «sudo pro status»


Last login: Mon Oct  6 12:01:31 2025 from 192.168.1.235
josevicente@ubuntuserver:~$ 

