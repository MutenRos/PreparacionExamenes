sudo apt install apache2
sudo = el super usuario va a hacer algo
apt = el gestor de paquetes
install = voy a instalar algo
apache2 es el servidor de paginas web por defecto en Linux

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


josevicente@ubuntuserver:~$ sudo apt install apache2
[sudo] password for josevicente: 
Leyendo lista de paquetes... Hecho
Creando árbol de dependencias... Hecho
Leyendo la información de estado... Hecho
Se instalarán los siguientes paquetes adicionales:
  apache2-bin apache2-data apache2-utils libapr1t64 libaprutil1-dbd-sqlite3
  libaprutil1-ldap libaprutil1t64 liblua5.4-0 ssl-cert
Paquetes sugeridos:
  apache2-doc apache2-suexec-pristine | apache2-suexec-custom www-browser
Se instalarán los siguientes paquetes NUEVOS:
  apache2 apache2-bin apache2-data apache2-utils libapr1t64
  libaprutil1-dbd-sqlite3 libaprutil1-ldap libaprutil1t64 liblua5.4-0 ssl-cert
0 actualizados, 10 nuevos se instalarán, 0 para eliminar y 135 no actualizados.
Se necesita descargar 2.086 kB de archivos.
Se utilizarán 8.090 kB de espacio de disco adicional después de esta operación.
¿Desea continuar? [S/n] S
Des:1 http://es.archive.ubuntu.com/ubuntu noble-updates/main amd64 libapr1t64 amd64 1.7.2-3.1ubuntu0.1 [108 kB]
Des:2 http://es.archive.ubuntu.com/ubuntu noble/main amd64 libaprutil1t64 amd64 1.6.3-1.1ubuntu7 [91,9 kB]
Des:3 http://es.archive.ubuntu.com/ubuntu noble/main amd64 libaprutil1-dbd-sqlite3 amd64 1.6.3-1.1ubuntu7 [11,2 kB]
Des:4 http://es.archive.ubuntu.com/ubuntu noble/main amd64 libaprutil1-ldap amd64 1.6.3-1.1ubuntu7 [9.116 B]
Des:5 http://es.archive.ubuntu.com/ubuntu noble/main amd64 liblua5.4-0 amd64 5.4.6-3build2 [166 kB]
Des:6 http://es.archive.ubuntu.com/ubuntu noble-updates/main amd64 apache2-bin amd64 2.4.58-1ubuntu8.8 [1.331 kB]
Des:7 http://es.archive.ubuntu.com/ubuntu noble-updates/main amd64 apache2-data all 2.4.58-1ubuntu8.8 [163 kB]
Des:8 http://es.archive.ubuntu.com/ubuntu noble-updates/main amd64 apache2-utils amd64 2.4.58-1ubuntu8.8 [97,7 kB]
Des:9 http://es.archive.ubuntu.com/ubuntu noble-updates/main amd64 apache2 amd64 2.4.58-1ubuntu8.8 [90,2 kB]
Des:10 http://es.archive.ubuntu.com/ubuntu noble/main amd64 ssl-cert all 1.1.2ubuntu1 [17,8 kB]
Descargados 2.086 kB en 1s (1.620 kB/s)
Preconfigurando paquetes ...
Seleccionando el paquete libapr1t64:amd64 previamente no seleccionado.
(Leyendo la base de datos ... 84252 ficheros o directorios instalados actualment
e.)
Preparando para desempaquetar .../0-libapr1t64_1.7.2-3.1ubuntu0.1_amd64.deb ...
Desempaquetando libapr1t64:amd64 (1.7.2-3.1ubuntu0.1) ...
Seleccionando el paquete libaprutil1t64:amd64 previamente no seleccionado.
Preparando para desempaquetar .../1-libaprutil1t64_1.6.3-1.1ubuntu7_amd64.deb ..
.
Desempaquetando libaprutil1t64:amd64 (1.6.3-1.1ubuntu7) ...
Seleccionando el paquete libaprutil1-dbd-sqlite3:amd64 previamente no selecciona
do.
Preparando para desempaquetar .../2-libaprutil1-dbd-sqlite3_1.6.3-1.1ubuntu7_amd
64.deb ...
Desempaquetando libaprutil1-dbd-sqlite3:amd64 (1.6.3-1.1ubuntu7) ...
Seleccionando el paquete libaprutil1-ldap:amd64 previamente no seleccionado.
Preparando para desempaquetar .../3-libaprutil1-ldap_1.6.3-1.1ubuntu7_amd64.deb 
...
Desempaquetando libaprutil1-ldap:amd64 (1.6.3-1.1ubuntu7) ...
Seleccionando el paquete liblua5.4-0:amd64 previamente no seleccionado.
Preparando para desempaquetar .../4-liblua5.4-0_5.4.6-3build2_amd64.deb ...
Desempaquetando liblua5.4-0:amd64 (5.4.6-3build2) ...
Seleccionando el paquete apache2-bin previamente no seleccionado.
Preparando para desempaquetar .../5-apache2-bin_2.4.58-1ubuntu8.8_amd64.deb ...
Desempaquetando apache2-bin (2.4.58-1ubuntu8.8) ...
Seleccionando el paquete apache2-data previamente no seleccionado.
Preparando para desempaquetar .../6-apache2-data_2.4.58-1ubuntu8.8_all.deb ...
Desempaquetando apache2-data (2.4.58-1ubuntu8.8) ...
Seleccionando el paquete apache2-utils previamente no seleccionado.
Preparando para desempaquetar .../7-apache2-utils_2.4.58-1ubuntu8.8_amd64.deb ..
.
Desempaquetando apache2-utils (2.4.58-1ubuntu8.8) ...
Seleccionando el paquete apache2 previamente no seleccionado.
Preparando para desempaquetar .../8-apache2_2.4.58-1ubuntu8.8_amd64.deb ...
Desempaquetando apache2 (2.4.58-1ubuntu8.8) ...
Seleccionando el paquete ssl-cert previamente no seleccionado.
Preparando para desempaquetar .../9-ssl-cert_1.1.2ubuntu1_all.deb ...
Desempaquetando ssl-cert (1.1.2ubuntu1) ...
Configurando ssl-cert (1.1.2ubuntu1) ...
Created symlink /etc/systemd/system/multi-user.target.wants/ssl-cert.service → /
usr/lib/systemd/system/ssl-cert.service.
Configurando libapr1t64:amd64 (1.7.2-3.1ubuntu0.1) ...
Configurando liblua5.4-0:amd64 (5.4.6-3build2) ...
Configurando apache2-data (2.4.58-1ubuntu8.8) ...
Configurando libaprutil1t64:amd64 (1.6.3-1.1ubuntu7) ...
Configurando libaprutil1-ldap:amd64 (1.6.3-1.1ubuntu7) ...
Configurando libaprutil1-dbd-sqlite3:amd64 (1.6.3-1.1ubuntu7) ...
Configurando apache2-utils (2.4.58-1ubuntu8.8) ...
Configurando apache2-bin (2.4.58-1ubuntu8.8) ...
Configurando apache2 (2.4.58-1ubuntu8.8) ...
Enabling module mpm_event.
Enabling module authz_core.
Enabling module authz_host.
Enabling module authn_core.
Enabling module auth_basic.
Enabling module access_compat.
Enabling module authn_file.
Enabling module authz_user.
Enabling module alias.
Enabling module dir.
Enabling module autoindex.
Enabling module env.
Enabling module mime.
Enabling module negotiation.
Enabling module setenvif.
Enabling module filter.
Enabling module deflate.
Enabling module status.
Enabling module reqtimeout.
Enabling conf charset.
Enabling conf localized-error-pages.
Enabling conf other-vhosts-access-log.
Enabling conf security.
Enabling conf serve-cgi-bin.
Enabling site 000-default.
Created symlink /etc/systemd/system/multi-user.target.wants/apache2.service → /u
sr/lib/systemd/system/apache2.service.
Created symlink /etc/systemd/system/multi-user.target.wants/apache-htcacheclean.
service → /usr/lib/systemd/system/apache-htcacheclean.service.
Procesando disparadores para ufw (0.36.2-6) ...
Procesando disparadores para man-db (2.12.0-4build2) ...
Procesando disparadores para libc-bin (2.39-0ubuntu8.6) ...
Scanning processes...                                                           
Scanning linux images...                                                        

Running kernel seems to be up-to-date.

No services need to be restarted.

No containers need to be restarted.

No user sessions are running outdated binaries.

No VM guests are running outdated hypervisor (qemu) binaries on this host.
josevicente@ubuntuserver:~$ 

