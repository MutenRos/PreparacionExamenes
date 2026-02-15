Tercera Forma Normal (3FN)
Artículo principal: Tercera forma normal
La 3NF fue definida originalmente por E.F. Codd.[2]​ La tabla se encuentra en 3FN si es 2FN y si no existe ninguna dependencia funcional transitiva en los atributos que no son clave.

Un ejemplo de este concepto sería que, una dependencia funcional X 
→
{\displaystyle \rightarrow } Y en un esquema de relación R es una dependencia transitiva si hay un conjunto de atributos Z que no es un subconjunto de alguna clave de R, donde se mantiene X 
→
{\displaystyle \rightarrow } Z y Z 
→
{\displaystyle \rightarrow } Y.

Por ejemplo, la dependencia SSN 
→
{\displaystyle \rightarrow } DMGRSSN es una dependencia transitiva en EMP_DEPT de la siguiente figura. Decimos que la dependencia de DMGRSSN el atributo clave SSN es transitiva vía DNUMBER porque las dependencias SSN→DNUMBER y DNUMBER→DMGRSSN son mantenidas, y DNUMBER no es un subconjunto de la clave de EMP_DEPT. Intuitivamente, podemos ver que la dependencia de DMGRSSN sobre DNUMBER es indeseable en EMP_DEPT dado que DNUMBER no es una clave de EMP_DEPT.

Formalmente, un esquema de relación 
R
{\displaystyle R} está en 3 Forma Normal Elmasri-Navâthe,[3]​ si para toda dependencia funcional 
X
→
A
{\displaystyle X\rightarrow A}, se cumple al menos una de las siguientes condiciones:

X
{\displaystyle X} es superllave o clave.
A
{\displaystyle A} es atributo primo de 
R
{\displaystyle R}; esto es, si es miembro de alguna clave en 
R
{\displaystyle R}.
Además el esquema debe cumplir necesariamente, con las condiciones de segunda forma normal.
