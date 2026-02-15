Queremos pasar el código (proyecto intermodular) desde entorno de desarollo hasta entorno de producción.

Qué hemos usado?

Python + flask + sqlite3
Cuenta nuestro entorno con esas herramientas?
La respuestas es si

Como conectamos el entorno de desarrollo con entorno de producción
Respuesta más sencilla: Filezilla

Nuestro servidor ya tiene servidor openssh

En nuestro entorno de desarrollo instalamos Filezilla Client

Configuramos nueva conexión:
Protocolo: SFTP (SSH)
Servidor: 192.168.1.151
usuario: josevicente
contraseña: TAME123$

Una vez conectado:
En la parte izquierda: tu equipo de desarrollo local
En la parte de la derecha: tu equipo remoto en produccion

Arrastrar:
De izquierda a derecha: subir archivos al servidor
De derecha a izquierda: bajar archivos del servidor

Creo directorio nuevo: /home/josevicente/paseproduccion
















