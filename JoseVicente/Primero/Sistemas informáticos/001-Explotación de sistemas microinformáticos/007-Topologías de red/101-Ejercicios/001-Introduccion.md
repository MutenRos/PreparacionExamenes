# Red de estrella / copo de nieve

Se utiliza para representar elementos muy complejos en redes de area grande

# Esto es posible gracias al sistema TCP/IP

Le asigna una dirección (algo así como un número de teléfono) a cada dispositivo conectado a internet

IPv4 (x.x.x.x) cada x va desde 0 a 255
4 billones de dispositivos conectados a internet

IPv6 (y.y.y.y.y.y.y.y) donde cada y va desde 0 a 
340,282,366,920,938,463,463,374,607,431,768,211,456

# Ejemplo eval

Tengo un equipo de desarrollo, que tiene dos IA en local

Tengo un servidor remoto, que simplemente muestra actividades a los alumnos, y recoge sus respuestas

Generar actividades: desarrollo -> servidor remoto
Descargar actividades: desarrollo <- servidor remoto
Corrijo en local con IA
Subo las evaluaciones al servidor: desarrollo -> servidor remoto


Tiempo de descarga de una web

Ejemplo 2:
mediumseagreen, cada vez que lo cargas, descarga 109KB = 109.000 bytes = 800.000 bits
En una red como la mia que ahora mismo tiene una tasa de 117 Mb/s 
Regla de 3: Si 117.000.000 = 1 segundo, 800.000 = X?
La aplicación va a tardar en transferirse 0,006837607 segundos al ordenador del usuario

Probablemente el criterio primario de un programa no es la red, pero si que es un factor de evaluación de desempeño


IMPORTANTE:

A un servidor nunca o practicamente nunca se le pone una conexion inhalambrica
Debería estar con cable, y debería estar lo más cerca posible del nodo de red

Los dispositivos de cliente final, en 2025, la mayoría están con Wifi - 5G
3G hasta 2 Mbps, 
4G hasta 300 Mbps (o incluso 1 Gbps en condiciones ideales),
 y 5G alcanza teóricamente 10 Gbps y más allá
 
 
Distancia	Pérdida FSPL (3.5 GHz)	RSRP típico (con EIRP ~62 dBm)	Capacidad estimada	Velocidad en MB/s
1 km	~103 dB	−41 dBm (excelente)	~100%	1250 MB/s
2 km	~109 dB	−47 dBm (muy buena)	~90%	1125 MB/s
5 km	~117 dB	−55 dBm (buena)	~70%	875 MB/s
10 km	~123 dB	−61 dBm (aceptable)	~40%	500 MB/s

Topologías:

Bus: Hay un cable central (médula espinal) y los nodos se conectan a ese cable

Estrella: Hay un nodo central, y los nodos se conectan a ese nodo

Mixta: Puede combinar varios de ellos

Anillo: los nodos están conectados uno a uno como vecinos

Doble Anillo: doble conexión entre vecinos

Arbol:
Conexión jerárquica

Malla:
Conexiones punto a punto (equipos interconectados entre si)
Totalmente conexa: Todo el mundo tiene conexión con todso










