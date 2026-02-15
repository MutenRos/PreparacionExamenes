Segunda Forma Normal (2FN)
Artículo principal: Segunda forma normal
Dependencia funcional. Una relación está en 2FN si está en 1FN y si los atributos que no forman parte de ninguna clave dependen de forma completa de la clave principal. Es decir, que no existen dependencias parciales. Todos los atributos que no son clave principal deben depender únicamente de la clave principal.

En otras palabras, podríamos decir que la segunda forma normal está basada en el concepto de dependencia completamente funcional. Una dependencia funcional 
x
→
y
{\displaystyle x\rightarrow y} es completamente funcional si al eliminar los atributos A de X significa que la dependencia no es mantenida, esto es que 
A
∈
X
,
X
−
{
A
}
↛
Y
{\displaystyle A\in X,X-\{A\}\nrightarrow Y}. Una dependencia funcional 
x
→
y
{\displaystyle x\rightarrow y} es una dependencia parcial si hay algunos atributos 
A
∈
X
{\displaystyle A\in X} que pueden ser eliminados de X y la dependencia todavía se mantiene, esto es 
A
∈
X
,
X
−
{
A
}
→
Y
{\displaystyle A\in X,X-\{A\}\rightarrow Y}.

Por ejemplo {DNI, ID_PROYECTO} 
→
{\displaystyle \rightarrow } HORAS_TRABAJO (con el DNI de un empleado y el ID de un proyecto sabemos cuántas horas de trabajo por semana trabaja un empleado en dicho proyecto) es completamente funcional dado que ni DNI 
→
{\displaystyle \rightarrow } HORAS_TRABAJO ni ID_PROYECTO 
→
{\displaystyle \rightarrow } HORAS_TRABAJO mantienen la dependencia. Sin embargo {DNI, ID_PROYECTO} 
→
{\displaystyle \rightarrow } NOMBRE_EMPLEADO es parcialmente dependiente dado que DNI 
→
{\displaystyle \rightarrow } NOMBRE_EMPLEADO mantiene la dependencia.
