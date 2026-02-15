Abro virtualbox

Creo una maquina virtual, con:
  nombre: UbuntuServer[tunombre]
  Imagen: alimentamos la imagen ISO descargada
  Omitir instalacion desatendida
  
  Hardware:
    Memoria: 2048-4196MB RAM
    Procesadores: Rec 4
    Disco: 125GB
    
Arrancamos la maquina

Elegimos idioma y disposicion de teclado
Elijo Ubuntu server no minimizado

Acepto la configuracion de red (recordad adaptador puente antes o despues)

No quiero proxy address

Comprobamos los mirrors

Particionamos disco entero
Aceptamos la propuesta de puntos de montaje

Aceptamos que se va a borrar el disco (de la maquina virtual)

Datos de la máquina con vuestro nombre

No quiero ubuntu pro por el momento

No elijáis servidor openssh automatico en la instalacion

No quiero entornos preconfigurados

La parte de la copia de archivos en clase ha ocupado tres minutos

Antes de reiniciar, cambiar a adaptador puente para que la maquina se vea desde fuera

Tras reiniciar, primer login

Primero, actualizo paquetes
sudo apt update

Instalo paquetes de red:
sudo apt install net-tools

Quiero saber cual es mi ip:
ifconfig

192.168.1.176

Y ahora instalo openssh-server
sudo apt install openssh-server








