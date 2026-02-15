Para publicar una aplicación necesitamos:

1.-Un dominio de internet
En mi caso he registrado el dominio recortabl.es
Lo he registrado en un proveedor de dominios (IONOS)
Coste de entre 6-10 euros al año

2.-HE necesitado en certificado SSL
Es el "candadito" que aparece en la URL cuando entras en el dominio
En mi caso he cogido uno basic
Coste aprox: 35 euros al año

3.-Apuntar las DNS hacia el servidor que tengo contratado
Apuntamos el registro A hacia la IP del servidor (en mi caso es: 217.160.228.9)
Al hacerlo habrá otras DNS que se desactivarán o se cambiarán

4.-Vamos configurando el servicio, y para ello:
 	1.-Nos conectamos al servidor por ssh o por ftp (filezilla) como en el examen de sistemas informáticos
 	2.-En la carpeta /var/www/html  creamos una nueva carpeta para el proyecto
 	3.-En el servidor, creamos un nuevo virtualhost para el dominio:
 	
 	<VirtualHost *:443>
		 ServerAdmin admin@jocarsa.com
		 ServerName recortabl.es
		 ServerAlias www.recortabl.es

		 DocumentRoot /var/www/html/recortabl.es/

		 SSLEngine on
		 SSLCertificateFile /etc/apache2/ssl/recortabl.es_fullchain.cer
		 SSLCertificateKeyFile /etc/apache2/ssl/recortabl.es.key

		 <Directory /var/www/html/recortabl.es/>
		     Options Indexes FollowSymLinks
		     AllowOverride All
		     Require all granted
		 </Directory>

		 ErrorLog ${APACHE_LOG_DIR}/screensaver.es-error.log
		 CustomLog ${APACHE_LOG_DIR}/screensaver.es-access.log combined
	</VirtualHost>

	No puedo activar el sitio hasta que no instale el certificado
	
	
