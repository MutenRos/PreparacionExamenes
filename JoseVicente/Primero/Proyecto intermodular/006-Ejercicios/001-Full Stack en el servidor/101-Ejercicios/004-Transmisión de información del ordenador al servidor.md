1.-Instalamos Filezilla client en tu ordenador

https://filezilla-project.org/

Descargamos el client:
https://filezilla-project.org/download.php?type=client

Lo descargáis para el sistema de desarrollo en el que estéis trabajando (previsiblemente Windows)

Filezilla:
Arriba están los datos de conexion
A la izquierda está TU ordenador
A la derecha está el servidor remoto

Gestor de sitios: crear una nueva conexión

Nuevo sitio: Le ponéis un nombre descriptivo

Protocolo: SFTP por SSH
Servidor: vuestra IP (en mi caso 192.168.1.78)
Modo de acceso: normal
usuario: vuestro usuario (en mi caso josevicente)
contraseña: vuestra contraseña

Confiar en la clave? si

Arrastro desde la ventana de la izquierda a la derecha para subir cosas al servidor

Cuando quiera descargar, arrastraré cosas desde la derecha hacia la izquierda

Compruebo si esta:
josevicente@ubuntuserver:~$ ls
'002-crear una aplicación de prueba en el servidor.py'







