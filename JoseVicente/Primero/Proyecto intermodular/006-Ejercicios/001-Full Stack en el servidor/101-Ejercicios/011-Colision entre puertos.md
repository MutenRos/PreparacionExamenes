josevicente@ubuntuserver:~$ python3 010-escuchamos\ en\ el\ puerto\ 80.py 
 * Serving Flask app '010-escuchamos en el puerto 80'
 * Debug mode: on
Permission denied
josevicente@ubuntuserver:~$ 

Averiguar cual es el estado de apache:

josevicente@ubuntuserver:~$ sudo service apache2 status
● apache2.service - The Apache HTTP Server
     Loaded: loaded (/usr/lib/systemd/system/apache2.service; enabled; preset: >
     Active: active (running) since Mon 2025-10-06 14:01:39 UTC; 23min ago
       Docs: https://httpd.apache.org/docs/2.4/
    Process: 941 ExecStart=/usr/sbin/apachectl start (code=exited, status=0/SUC>
    Process: 2116 ExecReload=/usr/sbin/apachectl graceful (code=exited, status=>
   Main PID: 970 (apache2)
      Tasks: 55 (limit: 2267)
     Memory: 8.0M (peak: 10.4M)
        CPU: 225ms
     CGroup: /system.slice/apache2.service
             ├─ 970 /usr/sbin/apache2 -k start
             ├─2120 /usr/sbin/apache2 -k start
             └─2121 /usr/sbin/apache2 -k start

oct 06 14:01:38 ubuntuserver systemd[1]: Starting apache2.service - The Apache >
oct 06 14:01:39 ubuntuserver apachectl[961]: AH00558: apache2: Could not reliab>
oct 06 14:01:39 ubuntuserver systemd[1]: Started apache2.service - The Apache H>
oct 06 14:12:46 ubuntuserver systemd[1]: Reloading apache2.service - The Apache>
oct 06 14:12:46 ubuntuserver apachectl[2119]: AH00558: apache2: Could not relia>
oct 06 14:12:46 ubuntuserver systemd[1]: Reloaded apache2.service - The Apache >
lines 1-21/21 (END)


Pero podemos parar apache
josevicente@ubuntuserver:~$ sudo service apache2 stop
josevicente@ubuntuserver:~$ 

Liberar puerto 80
josevicente@ubuntuserver:~$ python3 010-escuchamos\ en\ el\ puerto\ 80.py 
 * Serving Flask app '010-escuchamos en el puerto 80'
 * Debug mode: on
Permission denied
josevicente@ubuntuserver:~$ 





