Consiste en pasar una aplicación desde mi servidor local hasta el servidor real en producción.

Lo primero que hay que hacer es asegurar que el dominio está operativo.

Nosotros hemos aprendido a usar Apache2
Apache nos sirve para servir UNA web

En estas próximas semanas os voy a mostrar el concepto de virtualhost

MEdiante los virtualhosts, podéis tener, en un servidor, no una, sino tantas webs como queráis.

Un virtuahost requiere:
1.-El dominio al que atiende
2.-La carpeta donde está la web que corresponde a ese dominio
3.-Donde están los archivos de certificado SSL
4.-Configuración adicional

Importante: Para que una web se vea, los certificados tienen que estar correctamente instalados.

La parte importante de hoy: 
Copiar y pegar los archivos desde el ordenador de desarrollo hasta el servidor real
Se puede hacer con Filezilla

Error:
Fatal error: Uncaught Error: Call to undefined function imap_open() in /var/www/html/blogmail/index.php:179 Stack trace: #0 {main} thrown in /var/www/html/blogmail/index.php on line 179

No tengo la función imap open en mi servidor
Por suerte tengo contratado un VPS, con lo cual puedo acceder al servidor e instalar lo que me haga falta

Solucion:
sudo apt install php-imap

