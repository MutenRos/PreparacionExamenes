Una base de datos puede estar centralizada en un sistema informático (SI = ordenador / servidor)

Ventaja: Control - Desventaja: Escalabilidad

Un SI tiene una serie de límites - CPU (procesador) - RAM (memoria temporal) - Disco duro (almacén de datos)

Clásica = CPU+RAM+Disco
Hay sistemas de inteligencia artificial que SI guardar la información en GPU+RAMGPU

Que ocurre cuando una base de datos tiene tantos datos que desborda las capacidades del SI?

Tienes dos opciones:
1. O bien añades más recursos al sistema
2. Distribuyes la carga de diferentes SSII (multiples servidores que dan servicio a la misma base de datos)

Fragmentación

Guardar un espejo de la base de datos
Ganamos velocidad de acceso
No ganamos en disco duro

Guardar unos datos en un servidor, y otros datos en otro servidor

Otra forma de fragmentar: Primera mitad de una tabla en un servidor, segunda mitad de la tabla en otro servidor

