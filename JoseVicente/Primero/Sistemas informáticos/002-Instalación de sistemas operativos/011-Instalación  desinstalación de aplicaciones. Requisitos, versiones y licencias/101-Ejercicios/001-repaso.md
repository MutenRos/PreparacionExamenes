1.-Iniciamos sesion en la maquina:

usuario (en mi caso) josevicente
password (en mi caso) TAME123$

ifconfig para obtener la ip
la mía 192.168.1.72

Me conecto al equipo remoto:
josevicente@josevicenteportatil:~$ ssh josevicente@192.168.1.72
hostkeys_find_by_key_hostfile: hostkeys_foreach failed for /home/josevicente/.ssh/known_hosts: Permission denied
The authenticity of host '192.168.1.72 (192.168.1.72)' can't be established.
ED25519 key fingerprint is SHA256:01yUhdMdtJMuT0isDFihz6YGycA3tWKbt52qNN3P/3g.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Failed to add the host to the list of known hosts (/home/josevicente/.ssh/known_hosts).
josevicente@192.168.1.72's password: 
client_input_hostkeys: hostkeys_foreach failed for /home/josevicente/.ssh/known_hosts: Permission denied
Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 6.8.0-84-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of lun 06 oct 2025 12:01:31 UTC

  System load:  0.16              Processes:               157
  Usage of /:   7.3% of 60.23GB   Users logged in:         1
  Memory usage: 9%                IPv4 address for enp0s3: 192.168.1.72
  Swap usage:   0%


El mantenimiento de seguridad expandido para Applications está desactivado

Se pueden aplicar 141 actualizaciones de forma inmediata.
Para ver estas actualizaciones adicionales, ejecute: apt list --upgradable

Active ESM Apps para recibir futuras actualizaciones de seguridad adicionales.
Vea https://ubuntu.com/esm o ejecute «sudo pro status»


Last login: Mon Sep 29 15:45:30 2025 from 192.168.1.73
josevicente@ubuntuserver:~$ 


Comprobamos que la semana pasada instalamos apache

En un navegador web pongo 
http://192.168.1.72

O bien en la terminal pongo
sudo service apache2 status


josevicente@ubuntuserver:~$ sudo service apache2 status
[sudo] password for josevicente: 
● apache2.service - The Apache HTTP Server
     Loaded: loaded (/usr/lib/systemd/system/apache2.service; enabled; preset: >
     Active: active (running) since Mon 2025-10-06 11:59:59 UTC; 2min 52s ago
       Docs: https://httpd.apache.org/docs/2.4/
    Process: 895 ExecStart=/usr/sbin/apachectl start (code=exited, status=0/SUC>
   Main PID: 923 (apache2)
      Tasks: 55 (limit: 2267)
     Memory: 8.0M (peak: 8.6M)
        CPU: 103ms
     CGroup: /system.slice/apache2.service
             ├─923 /usr/sbin/apache2 -k start
             ├─925 /usr/sbin/apache2 -k start
             └─926 /usr/sbin/apache2 -k start

oct 06 11:59:59 ubuntuserver systemd[1]: Starting apache2.service - The Apache >
oct 06 11:59:59 ubuntuserver apachectl[915]: AH00558: apache2: Could not reliab>
oct 06 11:59:59 ubuntuserver systemd[1]: Started apache2.service - The Apache H>
lines 1-17/17 (END)

