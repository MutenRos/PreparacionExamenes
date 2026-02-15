Tres tipos principales de cardinalidad son:

1.-Relación de 1 a 1
Un elemento de una entidad corresponde a un elemento de otra entidad

1 cliente puede 1 nombre (a un elemento de una "tabla" le corresponde solo un elemento de otra "tabla")

Cuando tenemos este caso, la solución, en base a normalización de bases de datos, suele ser incorporar ese dato en la tabla (no tiene sentido tener dos tablas separadas)

2.-Relación de 1 a n

A un elemento de una tabla le corresponden n elementos de la otra tabla

Hay que tener en cuenta la direccionalidad de la cardinalidad

Un pedido solo puede tener un cliente (desde ese punto de vista es 1 a 1)
Pero un cliente puede hacer n pedidos (desde ese punto de vista es 1 a n)

Si se da este caso, esto pide tener dos tablas en la base de datos, dos entidades diferentes

3.-Relación de n a n
Quiere decir:
a n elementos de una "tabla" le corresponden n elementos de la otra "tabla"

Ejemplo:
Un estudiante puede tener n asignaturas
Una asignaturas puede tener n estudiantes

No es común, pero, como en el caso del centro de estudios, tampoco es infrecuente

Cuando se dan estos casos, se suele solucionar la cardinalidad con una tabla intermedia







