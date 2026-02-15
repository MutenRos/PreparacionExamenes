Tipos de redes y como nos afectan como programadores

Fundamentalmente trabajamos con dos tipos de redes:
Redes cableadas

Usando el protocolo Ethernet

Cat5 = 100Mb/segundo
Cat5e = 1000Mb/segundo
Cat6 = 1000Mb/segundo
Cat6b = 10000Mb/segundo
Cat7 = 10000Mb/segundo

Un bit es la unidad mínima de información en un sistema informático
Un bit es un interruptor, es un encendido o apagado, es un 1 o 0
La informática actual se basa en el sistema binario

Si una red Cat6 transmite 1000Mb / segundo
1000Mb = 1000 x 1.000.000 = 1.000.000.000 mil millones
Eso quiere decir que cada segundo que pasa se pueden transmitir hasta mil millones de piezas de información

Ejemplo:
1 byte = 8 bit
persona.xml = 207 bytes = 1656 bits
Por regla de tres: 1.000.000.000 es a 1 como 1656 es a X
Tardamos 0,000001656 segundos en enviar un archivo xml
O bien en un segundo podríamos transferir teóricamente 603864,734299517 XML

Ejemplo:
1 imagen de Ubuntu:4,8GB = 4.800.000.000 bytes x 8 = 38.400.000.000
En una red que transmite 1.000.000.000 de bits en un segundo, un archivo de 38.4 tarda 38.4 segundos en transferirse

Componentes de una red informática

Nuestro ordenador tiene una tarjeta de red (a veces tiene varias - Cable+Wifi)
Nos conectamos a un router con un cable
Y luego tenemos el router
Del router sale un cable que suele ser de fibra óptica
Eso va a un nodo de un centro de red que está en la calle
Eso va a un nodo de zona
De ahi a un nodo regional
De ahi a  un nodo nacional

Un factor limitante es el ancho de banda contratado al proveedor
A dia de hoy, ejemplo Movistar:
300MBps
600MBps
1000MBps

Averiguar velocidad de red en Ubuntu:
ethtool eth0 | grep Speed - esto es para red de cable

Windows

Abre el Administrador de tareas → pestaña Rendimiento → Ethernet.
Ahí aparece la velocidad de enlace (por ejemplo, 100 Mbps, 1 Gbps, 2.5 Gbps, etc.).

O en Panel de control → Centro de redes → Cambiar configuración del adaptador → Estado.

macOS

En Preferencias del Sistema → Red → Avanzado → Hardware aparece la velocidad de enlace.

En terminal:

josevicente@josevicenteportatil:~$ iwconfig
lo        no wireless extensions.

enp55s0   no wireless extensions.

wlo1      IEEE 802.11  ESSID:"MOVISTAR_E9A4"  
          Mode:Managed  Frequency:5.18 GHz  Access Point: 46:48:B9:F3:E9:AD   
          Bit Rate=117 Mb/s   Tx-Power=22 dBm   
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:on
          Link Quality=34/70  Signal level=-76 dBm  
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:0  Invalid misc:16134   Missed beacon:0



Redes inhalámbricas:

La velocidad de red es bastante inferior que con redes cableadas
Debemos medir la velocidad que necesitamos con respecto a la velocidad que nos llega

Diferencia entre MB y Mb

Un ejemplo es el programa eval.jocarsa.com










