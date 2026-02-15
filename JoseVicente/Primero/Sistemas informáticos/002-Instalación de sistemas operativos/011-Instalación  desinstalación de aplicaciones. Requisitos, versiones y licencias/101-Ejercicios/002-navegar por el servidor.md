cd = change directory

cd /var/www/html

Navegar hasta la raiz:

cd /

Listar archivos y carpetas:

josevicente@ubuntuserver:/$ ls
bin                home               mnt   sbin.usr-is-merged  usr
bin.usr-is-merged  lib                opt   snap                var
boot               lib64              proc  srv
cdrom              lib.usr-is-merged  root  swap.img
dev                lost+found         run   sys
etc                media              sbin  tmp
josevicente@ubuntuserver:/$ 

Listado con detalles:
josevicente@ubuntuserver:/$ ls -l
total 2097236
lrwxrwxrwx   1 root root          7 abr 22  2024 bin -> usr/bin
drwxr-xr-x   2 root root       4096 feb 26  2024 bin.usr-is-merged
drwxr-xr-x   4 root root       4096 sep 29 15:32 boot
dr-xr-xr-x   2 root root       4096 ago 27  2024 cdrom
drwxr-xr-x  20 root root       4100 oct  6 11:59 dev
drwxr-xr-x 109 root root       4096 sep 29 15:48 etc
drwxr-xr-x   3 root root       4096 sep 29 15:33 home
lrwxrwxrwx   1 root root          7 abr 22  2024 lib -> usr/lib
lrwxrwxrwx   1 root root          9 abr 22  2024 lib64 -> usr/lib64
drwxr-xr-x   2 root root       4096 feb 26  2024 lib.usr-is-merged
drwx------   2 root root      16384 sep 29 15:27 lost+found
drwxr-xr-x   2 root root       4096 ago 27  2024 media
drwxr-xr-x   2 root root       4096 ago 27  2024 mnt
drwxr-xr-x   2 root root       4096 ago 27  2024 opt
dr-xr-xr-x 218 root root          0 oct  6 11:59 proc
drwx------   3 root root       4096 oct  6 12:03 root
drwxr-xr-x  28 root root        840 oct  6 12:01 run
lrwxrwxrwx   1 root root          8 abr 22  2024 sbin -> usr/sbin
drwxr-xr-x   2 root root       4096 abr  3  2024 sbin.usr-is-merged
drwxr-xr-x   2 root root       4096 sep 29 15:33 snap
drwxr-xr-x   2 root root       4096 ago 27  2024 srv
-rw-------   1 root root 2147483648 sep 29 15:29 swap.img
dr-xr-xr-x  13 root root          0 oct  6 11:59 sys
drwxrwxrwt  13 root root       4096 oct  6 12:00 tmp
drwxr-xr-x  12 root root       4096 ago 27  2024 usr
drwxr-xr-x  14 root root       4096 sep 29 15:48 var
josevicente@ubuntuserver:/$ 

Entrar en var

cd /var

Listado de var:

josevicente@ubuntuserver:/var$ ls -l
total 48
drwxr-xr-x  2 root root   4096 oct  1 18:24 backups
drwxr-xr-x 17 root root   4096 oct  1 18:29 cache
drwxrwsrwt  2 root root   4096 ago 27  2024 crash
drwxr-xr-x 45 root root   4096 oct  1 18:29 lib
drwxrwsr-x  2 root staff  4096 abr 22  2024 local
lrwxrwxrwx  1 root root      9 ago 27  2024 lock -> /run/lock
drwxrwxr-x 11 root syslog 4096 oct  6 11:59 log
drwxrwsr-x  2 root mail   4096 ago 27  2024 mail
drwxr-xr-x  2 root root   4096 ago 27  2024 opt
lrwxrwxrwx  1 root root      4 ago 27  2024 run -> /run
drwxr-xr-x  2 root root   4096 ago 20  2024 snap
drwxr-xr-x  4 root root   4096 ago 27  2024 spool
drwxrwxrwt  8 root root   4096 oct  6 12:00 tmp
drwxr-xr-x  3 root root   4096 sep 29 15:48 www
josevicente@ubuntuserver:/var$ 

cd www

josevicente@ubuntuserver:/var/www$ ls -l
total 4
drwxr-xr-x 2 root root 4096 sep 29 15:48 html
josevicente@ubuntuserver:/var/www$ 

josevicente@ubuntuserver:/var/www$ cd html
josevicente@ubuntuserver:/var/www/html$ ls
index.html
josevicente@ubuntuserver:/var/www/html$ 


Es la página web por defecto de apache2









