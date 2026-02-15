# Bases de datos

**Author:** Jose Vicente Carratala Sanchis

## Table of contents

- [Almacenamiento de la información](#almacenamiento-de-la-informacion)
  - [Ficheros (planos, indexados, acceso directo, entre otros)](#ficheros-planos-indexados-acceso-directo-entre-otros)
  - [Bases de datos. Conceptos, usos y tipos según el modelo de datos, la ubicación de la información](#bases-de-datos-conceptos-usos-y-tipos-segun-el-modelo-de-datos-la-ubicacion-de-la-informacion)
  - [Sistemas gestores de base de datos Funciones, componentes y tipos](#sistemas-gestores-de-base-de-datos-funciones-componentes-y-tipos)
  - [Bases de datos centralizadas y bases de datos distribuidas. Técnicas de fragmentación](#bases-de-datos-centralizadas-y-bases-de-datos-distribuidas-tecnicas-de-fragmentacion)
  - [Legislación sobre protección de datos](#legislacion-sobre-proteccion-de-datos)
  - [Big Data introducción, análisis de datos, inteligencia de negocios](#big-data-introduccion-analisis-de-datos-inteligencia-de-negocios)
  - [Ejercicio de final de unidad](#ejercicio-de-final-de-unidad)
- [Bases de datos relacionales](#bases-de-datos-relacionales)
  - [Modelo de datos](#modelo-de-datos)
  - [Terminología del modelo relacional](#terminologia-del-modelo-relacional)
  - [Tipos de datos](#tipos-de-datos)
  - [Claves primarias](#claves-primarias)
  - [Restricciones de validación](#restricciones-de-validacion)
  - [Índices. Características](#indices-caracteristicas)
  - [El valor NULL](#el-valor-null)
  - [Claves ajenas](#claves-ajenas)
  - [Vistas](#vistas)
  - [Usuarios. Privilegios](#usuarios-privilegios)
  - [Lenguaje de descripción de datos (DDL)](#lenguaje-de-descripcion-de-datos-ddl)
  - [Lenguaje de control de datos (DCL)](#lenguaje-de-control-de-datos-dcl)
  - [Ejercicio de final de unidad](#ejercicio-de-final-de-unidad-1)
- [Realización de consultas](#realizacion-de-consultas)
  - [Proyección, selección y ordenación de registros](#proyeccion-seleccion-y-ordenacion-de-registros)
  - [Operadores. Operadores de comparación. Operadores lógicos](#operadores-operadores-de-comparacion-operadores-logicos)
  - [Consultas de resumen](#consultas-de-resumen)
  - [Agrupamiento de registros](#agrupamiento-de-registros)
  - [Composiciones internas](#composiciones-internas)
  - [Composiciones externas](#composiciones-externas)
  - [Subconsultas](#subconsultas)
  - [Combinación de múltiples selecciones](#combinacion-de-multiples-selecciones)
  - [Optimización de consultas](#optimizacion-de-consultas)
  - [Ejercicio de final de unidad](#ejercicio-de-final-de-unidad-2)
- [Tratamiento de datos](#tratamiento-de-datos)
  - [Inserción, borrado y modificación de registros](#insercion-borrado-y-modificacion-de-registros)
  - [Integridad referencial](#integridad-referencial)
  - [Subconsultas y composiciones en órdenes de edición](#subconsultas-y-composiciones-en-ordenes-de-edicion)
  - [Transacciones](#transacciones)
  - [Políticas de bloqueo. Concurrencia](#politicas-de-bloqueo-concurrencia)
  - [Simulacro examen](#simulacro-examen)
  - [Simulacro de examen 2](#simulacro-de-examen-2)
  - [Ejercicio de final de unidad](#ejercicio-de-final-de-unidad-3)
  - [Examen final](#examen-final)
- [Programación de bases de datos](#programacion-de-bases-de-datos)
  - [Introducción. Lenguaje de programación](#introduccion-lenguaje-de-programacion)
  - [Variables del sistema y variables de usuario](#variables-del-sistema-y-variables-de-usuario)
  - [Funciones](#funciones)
  - [Estructuras de control de flujo](#estructuras-de-control-de-flujo)
  - [Procedimientos almacenados. Funciones de usuario](#procedimientos-almacenados-funciones-de-usuario)
  - [Eventos y disparadores](#eventos-y-disparadores)
  - [Excepciones](#excepciones)
  - [Cursores](#cursores)
- [Interpretación de Diagramas EntidadRelación](#interpretacion-de-diagramas-entidadrelacion)
  - [El modelo ER. Entidades y relaciones. Cardinalidades. Debilidad](#el-modelo-er-entidades-y-relaciones-cardinalidades-debilidad)
  - [El modelo ER ampliado. Generalización y especialización. Agregación](#el-modelo-er-ampliado-generalizacion-y-especializacion-agregacion)
  - [Paso del diagrama ER al modelo relacional](#paso-del-diagrama-er-al-modelo-relacional)
  - [Restricciones semánticas del modelo relacional](#restricciones-semanticas-del-modelo-relacional)
  - [Normalización de modelos relacionales](#normalizacion-de-modelos-relacionales)
  - [Ejercicios](#ejercicios)
  - [Criterios de evaluación](#criterios-de-evaluacion)
  - [Resumen](#resumen)
- [Uso de bases de datos no relacionales](#uso-de-bases-de-datos-no-relacionales)
  - [Características de las bases de datos no relacionales](#caracteristicas-de-las-bases-de-datos-no-relacionales)
  - [Tipos de bases de datos no relacionales](#tipos-de-bases-de-datos-no-relacionales)
  - [Elementos de las bases de datos no relacionales](#elementos-de-las-bases-de-datos-no-relacionales)
  - [Sistemas gestores de bases de datos no relacionales](#sistemas-gestores-de-bases-de-datos-no-relacionales)
  - [Herramientas de los sistemas gestores de bases de datos no relacionales para la gestión de la información almacenada](#herramientas-de-los-sistemas-gestores-de-bases-de-datos-no-relacionales-para-la-gestion-de-la-informacion-almacenada)
- [Proyectos](#proyectos)
  - [proyecto tienda online](#proyecto-tienda-online)
  - [IA para dietetica](#ia-para-dietetica)
- [Actividad libre de final de evaluación - La milla extra](#actividad-libre-de-final-de-evaluacion-la-milla-extra)
  - [La Milla Extra - Primera evaluación](#la-milla-extra-primera-evaluacion)
- [Actividades de final de unidad segundo trimestre](#actividades-de-final-de-unidad-segundo-trimestre)
  - [Proyecto tienda online](#proyecto-tienda-online-1)
  - [Proyecto IA para dietética](#proyecto-ia-para-dietetica)
  - [Proyecto scrapear web](#proyecto-scrapear-web)

---

<a id="almacenamiento-de-la-informacion"></a>
# Almacenamiento de la información

<a id="ficheros-planos-indexados-acceso-directo-entre-otros"></a>
## Ficheros (planos, indexados, acceso directo, entre otros)

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/001-Almacenamiento%20de%20la%20informaci%C3%B3n/001-Ficheros%20%28planos%2C%20indexados%2C%20acceso%20directo%2C%20entre%20otros%29)

### Introducción a los ejercicios

Esta carpeta contiene una serie de ejercicios que te permitirán explorar diferentes tipos de archivos y formatos utilizados para almacenar información, como ficheros de texto plano, CSV (Comma Separated Values), JSON (JavaScript Object Notation) y XML (eXtensible Markup Language). Los ejercicios se centran en cómo los datos pueden ser estructurados y representados en cada formato, destacando las ventajas y limitaciones de cada uno. A través de estos ejercicios, practicarás la lectura, comprensión y manipulación de datos en diferentes contextos, desarrollando habilidades esenciales para el manejo de bases de datos y la creación de sistemas de información más complejos.

### archivos de texto plano
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código no es realmente un bloque de código en el sentido convencional, sino más bien texto plano. En contexto, parece ser el contenido de un archivo de texto llamado "002-archivos de texto plano.txt". Este tipo de archivos almacenan texto sin formato y son muy comunes para guardar información como notas o ejemplos sencillos en cursos educativos.

Lo que ves es simplemente una línea con dos oraciones: "Hola esto es una prueba" y "y este es un documento", ambas separadas por un salto de línea. En la práctica, este archivo podría servir para enseñar cómo leer o manipular archivos de texto en diferentes lenguajes de programación, mostrando cómo acceder a datos simples almacenados en formato de texto puro.

Es importante entender estos archivos porque forman una base fundamental en el manejo de información y son un punto de partida perfecto antes de pasar a formatos más complejos como CSV, JSON o XML.

`002-archivos de texto plano.txt`

```
Hola esto es una prueba y este es un documento
```

### clientes
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es un archivo CSV (Coma Separated Values), que es una forma sencilla y común de almacenar información en formato de texto plano. En este caso, el archivo se llama `003-clientes.csv` y contiene datos básicos sobre clientes, como su nombre, apellidos y teléfono.

El primer renglón del archivo indica las columnas o campos que cada entrada del cliente va a tener: "nombre", "apellidos" y "telefono". Esto ayuda a entender la estructura de los datos que siguen. A continuación, tenemos tres líneas con información específica de clientes. Por ejemplo, la segunda línea indica que el nombre es "Juan", los apellidos son "Garcia Lopez" y el teléfono es 5432534.

Este tipo de archivo CSV es importante porque permite almacenar datos en un formato que es fácilmente legible por humanos y también muy sencillo para procesar con programas de computadora. Es especialmente útil cuando necesitas compartir o importar información entre diferentes aplicaciones, ya que prácticamente cualquier programa puede leer archivos CSV sin problemas.

`003-clientes.csv`

```
nombre,apellidos,telefono
Juan,Garcia Lopez,5432534
Jorge,Martinez,5432534
Jose,Lopez,523534
```

### clientes
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código es un archivo JSON que almacena información sobre varios clientes. En concreto, el archivo contiene una lista de objetos, donde cada objeto representa a un cliente diferente. Cada uno de estos objetos tiene tres propiedades: 'nombre', 'apellidos' y 'telefono'. Por ejemplo, el primer cliente en la lista se llama Juan y tiene los apellidos 'xxx' y un número telefónico también especificado como 'xxx'. Este formato es útil porque permite almacenar y organizar datos estructurados de manera clara y fácilmente accesible. JSON (JavaScript Object Notation) es popular debido a su simplicidad y porque es fácil de leer tanto para humanos como para máquinas, lo que facilita el intercambio de información entre diferentes sistemas o aplicaciones web.

`004-clientes.json`

```json
[
  {
    "nombre":"Juan",
    "apellidos":"xxx",
    "telefono":"xxx"
  },
  {
    "nombre":"Jorge",
    "apellidos":"xxx",
    "telefono":"xxx"
  },
  {
    "nombre":"Jaime",
    "apellidos":"xxx",
    "telefono":"xxx"
  },
  {
    "nombre":"Jose",
    "apellidos":"xxx",
    "telefono":"xxx"
  },
]
```

### clientes anidades
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es un archivo JSON que almacena información sobre varios clientes. Cada cliente está representado como un objeto dentro de una lista (denominada array en programación), lo que significa que puedes tener múltiples registros de clientes almacenados en este formato. Cada objeto dentro del array contiene tres propiedades: "nombre", "apellidos" y "telefono". En tu caso, los valores reales para los campos "apellidos" y "telefono" están marcados con el texto "xxx", lo que probablemente indica un valor de prueba o falta de datos específicos. 

Es importante destacar que esta estructura JSON permite la organización anidada de datos, es decir, puedes tener datos complejos como relaciones entre clientes y otros detalles almacenados en un formato fácil de leer y utilizar tanto para humanos como para máquinas. En entornos de programación y bases de datos, este tipo de archivo JSON facilita operaciones de lectura, escritura y manipulación de información sobre los clientes.

`005-clientes anidades.json`

```json
[
  {
    "nombre":"Juan",
    "apellidos":"xxx",
    "telefono","xxx"
  },
  {
    "nombre":"Jorge",
    "apellidos":"xxx",
    "telefono","xxx"
  },
  {
    "nombre":"Jaime",
    "apellidos":"xxx",
    "telefono","xxx"
  },
  {
    "nombre":"Jose",
    "apellidos":"xxx",
    "telefono","xxx"
  },
]
```

### clientes anidados
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es una lista JSON que contiene información sobre varios clientes. Cada cliente está representado como un objeto JSON con tres propiedades: `nombre`, `apellidos` y `telefono`. En la versión anterior, todos los clientes tenían solo un número de teléfono especificado como una cadena única. Sin embargo, en este archivo actualizado, se ha modificado el formato del campo `telefono` para algunos clientes.

En particular, el cliente "Juan" ahora tiene su número de teléfono representado como una lista que contiene tres elementos: `"xxx"`, `"yyyy"` y `"zzzz"`. Esto permite almacenar múltiples números de teléfono para un mismo cliente en lugar de solo uno. Los demás clientes siguen teniendo su número de teléfono como una sola cadena, similar a la versión anterior.

**ÚLTIMO PÁRRAFO:**
La principal diferencia entre este archivo y el previo es que ahora "Juan" tiene múltiples números telefónicos almacenados en una lista dentro del campo `telefono`, lo cual permite mayor flexibilidad al gestionar varios contactos de teléfono para un mismo cliente.

`005-clientes anidados.json`

```json
[
  {
    "nombre":"Juan",
    "apellidos":"xxx",
    "telefono":["xxx","yyyy","zzzz"]
  },
  {
    "nombre":"Jorge",
    "apellidos":"xxx",
    "telefono":"xxx"
  },
  {
    "nombre":"Jaime",
    "apellidos":"xxx",
    "telefono":"xxx"
  },
  {
    "nombre":"Jose",
    "apellidos":"xxx",
    "telefono":"xxx"
  },
]
```

### clientes
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código está escrito en XML y representa información sobre personas, incluyendo sus nombres, apellidos y teléfonos. La estructura principal del archivo es un elemento `<personas>` que contiene varios elementos `<persona>`, cada uno representando a una persona individual.

Cada elemento `<persona>` incluye subelementos específicos para el nombre (`<nombre>`), los apellidos (`<apellidos>`), y los teléfonos de la persona. En algunos casos, como con Juan, se usa un bloque separado llamado `<telefonos>`, que a su vez contiene múltiples elementos `<telefono>` para listar varios números telefónicos. Otros casos simplemente tienen el elemento `<telefono>` directamente dentro del `<persona>` sin la estructura adicional de `<telefonos>`.

Esta forma de organizar los datos es útil cuando necesitas representar información jerárquica y permitir variaciones en cómo se presenta cierta información, como tener múltiples teléfonos para una persona pero no ser obligatorio. Es importante para entender cómo estructurar datos complejos en archivos XML cuando trabajas con bases de datos o sistemas que manejan grandes cantidades de información personalizada.

`006-clientes.xml`

```xml
<personas>
  <persona>
    <nombre>Juan</nombre>
    <apellidos>xxx</apellidos>
    <telefonos>
      <telefono>xxx</telefono>
      <telefono>yyyy</telefono>
      <telefono>zzzz</telefono>
    </telefonos>
  </persona>
  <persona>
    <nombre>Jorge</nombre>
    <apellidos>xxx</apellidos>
    <telefono>xxx</telefono>
  </persona>
  <persona>
    <nombre>Jaime</nombre>
    <apellidos>xxx</apellidos>
    <telefono>xxx</telefono>
  </persona>
  <persona>
    <nombre>Jose</nombre>
    <apellidos>xxx</apellidos>
    <telefono>xxx</telefono>
  </persona>
</personas>
```

### Actividades propuestas

### Actividad 1: Comparación de Formatos de Archivos
**Descripción:** Los estudiantes deben identificar las diferencias entre los archivos de texto plano, CSV y JSON/XML. Se les pedirá que escriban una breve descripción sobre cada formato destacando sus ventajas y desventajas.

**Objetivo:** Aprender a distinguir entre diferentes formatos de archivo y entender su utilidad en el almacenamiento de datos.

### Actividad 2: Conversión de Archivos CSV a JSON
**Descripción:** Los estudiantes deben convertir un archivo .csv (003-clientes.csv) a formato JSON utilizando un script simple o herramienta online. La salida debe ser similar al archivo proporcionado (004-clientes.json).

**Objetivo:** Familiarizarse con la estructura básica de archivos JSON y aprender a manipular datos entre diferentes formatos.

### Actividad 3: Lectura de Archivos XML
**Descripción:** Se les pide que lean el contenido del archivo .xml (006-clientes.xml) e imprimir todos los números telefónicos de cada persona en la consola. 

**Objetivo:** Aprender a manipular archivos XML y extraer información específica.

### Actividad 4: Agregar Nuevos Datos a Archivos JSON
**Descripción:** Los estudiantes deben agregar un nuevo cliente (con nombre, apellidos y teléfono) al archivo .json existente (004-clientes.json).

**Objetivo:** Aprender cómo manipular archivos JSON para añadir nuevos datos.

### Actividad 5: Modificación de Datos en Archivos XML
**Descripción:** Se les pide que modifiquen el número telefónico de un cliente específico dentro del archivo .xml (006-clientes.xml).

**Objetivo:** Familiarizarse con la edición de datos en archivos XML.

### Actividad 6: Conversión Entre Formatos
**Descripción:** Los estudiantes deben escribir un script que permita convertir el archivo .csv a formato XML y viceversa, utilizando como base los ejemplos proporcionados (003-clientes.csv y 006-clientes.xml).

**Objetivo:** Aprender a manipular datos entre diferentes formatos de archivos.

### Actividad 7: Estructura JSON Anidada
**Descripción:** Los estudiantes deben crear un archivo .json que tenga una estructura anidada (similar al formato del archivo 005-clientes anidados.json) donde los números telefónicos estén almacenados en arrays dentro de cada objeto cliente.

**Objetivo:** Aprender a manejar datos complejos y estructuras anidadas en JSON.

### Actividad 8: Consulta Básica con XML
**Descripción:** Los estudiantes deben escribir un script que permita buscar el nombre de una persona dado su número telefónico en el archivo .xml (006-clientes.xml).

**Objetivo:** Familiarizarse con la consulta y manipulación de datos complejos en archivos XML.

### Actividad 9: Combinar Datos JSON
**Descripción:** Se les pide que combinen los dos archivos .json proporcionados (004-clientes.json y 005-clientes anidados.json) en un solo archivo, resolviendo cualquier conflicto de datos si es necesario.

**Objetivo:** Aprender a trabajar con conjuntos de datos múltiples y manejar posibles inconsistencias.

### Actividad 10: Visualización de Datos CSV
**Descripción:** Los estudiantes deben crear una pequeña aplicación que lea un archivo .csv (similar al ejemplo del archivo 003-clientes.csv) e imprima sus contenidos en la consola con formato estructurado, como columnas.

**Objetivo:** Familiarizarse con la manipulación y visualización de datos tabulares.


<a id="bases-de-datos-conceptos-usos-y-tipos-segun-el-modelo-de-datos-la-ubicacion-de-la-informacion"></a>
## Bases de datos. Conceptos, usos y tipos según el modelo de datos, la ubicación de la información

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/001-Almacenamiento%20de%20la%20informaci%C3%B3n/002-Bases%20de%20datos.%20Conceptos%2C%20usos%20y%20tipos%20seg%C3%BAn%20el%20modelo%20de%20datos%2C%20la%20ubicaci%C3%B3n%20de%20la%20informaci%C3%B3n)


<a id="sistemas-gestores-de-base-de-datos-funciones-componentes-y-tipos"></a>
## Sistemas gestores de base de datos Funciones, componentes y tipos

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/001-Almacenamiento%20de%20la%20informaci%C3%B3n/003-Sistemas%20gestores%20de%20base%20de%20datos%20Funciones%2C%20componentes%20y%20tipos)


<a id="bases-de-datos-centralizadas-y-bases-de-datos-distribuidas-tecnicas-de-fragmentacion"></a>
## Bases de datos centralizadas y bases de datos distribuidas. Técnicas de fragmentación

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/001-Almacenamiento%20de%20la%20informaci%C3%B3n/004-Bases%20de%20datos%20centralizadas%20y%20bases%20de%20datos%20distribuidas.%20T%C3%A9cnicas%20de%20fragmentaci%C3%B3n)

### Introducción a los ejercicios

Este conjunto de ejercicios se enfoca en entender las diferencias entre bases de datos centralizadas y distribuidas, así como las técnicas de fragmentación que permiten manejar grandes volúmenes de información. Los estudiantes aprenderán sobre los límites y ventajas de almacenar datos en un solo sistema informático y cómo la distribución de datos a múltiples servidores puede mejorar el rendimiento y escalabilidad de una base de datos. Además, se practicarán conceptos clave como la replicación de datos y la fragmentación horizontal y vertical para optimizar el acceso y almacenamiento de información en entornos empresariales complejos.

### Actividades propuestas

### Actividad 1: Ventajas y Desventajas de las Bases de Datos Centralizadas
**Descripción:** Los estudiantes deben listar al menos tres ventajas y desventajas de utilizar bases de datos centralizadas. Se espera que identifiquen problemas relacionados con la escalabilidad y el control.

### Actividad 2: Identificación del Hardware Crítico en Sistemas Informáticos
**Descripción:** Los estudiantes deben describir cómo los componentes básicos de un sistema informático (CPU, RAM, disco duro) afectan al rendimiento de una base de datos centralizada. Se espera que comprendan la importancia de cada componente.

### Actividad 3: Análisis de Fragmentación de Datos
**Descripción:** Los estudiantes deben explicar qué es y cómo funciona la fragmentación en bases de datos distribuidas. También deberán señalar las principales ventajas y desventajas en términos de velocidad y almacenamiento.

### Actividad 4: Desarrollo de Escenarios Prácticos
**Descripción:** Los estudiantes deben diseñar un escenario práctico donde una base de datos centralizada supera sus límites y se opta por la distribución. Se espera que describan cómo sería la implementación en términos generales.

### Actividad 5: Explicación de Espejo de Base de Datos
**Descripción:** Los estudiantes deben explicar qué significa guardar un espejo (copia) de una base de datos y cuáles son sus beneficios. Se espera que indiquen cómo afecta a la velocidad de acceso pero no al almacenamiento total.

### Actividad 6: Distribución de Datos entre Servidores
**Descripción:** Los estudiantes deben detallar un ejemplo práctico donde una tabla de base de datos se fragmenta y distribuye entre dos o más servidores. Se espera que describan cómo afecta la gestión de transacciones.

### Actividad 7: Comparación entre GPU y RAM Tradicional en IA
**Descripción:** Los estudiantes deben comparar el uso de GPUs para almacenamiento con respecto al uso tradicional de RAM en sistemas de inteligencia artificial, destacando ventajas e inconvenientes. Se espera que entiendan la importancia del hardware específico.

### Actividad 8: Evaluación de Casos Prácticos
**Descripción:** Los estudiantes deben evaluar diferentes escenarios donde se ha optado por una distribución de datos en servidores múltiples y determinar si es más beneficioso que mantener todo centralizado. Se espera que usen los conceptos aprendidos para tomar decisiones informadas.

### Actividad 9: Creación de Presentaciones
**Descripción:** Los estudiantes deben crear una breve presentación (de 5-7 diapositivas) sobre las bases de datos distribuidas y la fragmentación, incluyendo ventajas y desventajas. Se espera que demuestren su comprensión del tema.

### Actividad 10: Resolución de Problemas
**Descripción:** Los estudiantes deben resolver un problema práctico donde una base de datos se encuentra en riesgo debido a la sobrecarga de datos. Deben proponer soluciones basadas en los conceptos aprendidos sobre fragmentación y distribución de datos.


<a id="legislacion-sobre-proteccion-de-datos"></a>
## Legislación sobre protección de datos

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/001-Almacenamiento%20de%20la%20informaci%C3%B3n/005-Legislaci%C3%B3n%20sobre%20protecci%C3%B3n%20de%20datos)

### Introducción a los ejercicios

Este conjunto de ejercicios está centrado en la comprensión y aplicación de la legislación sobre protección de datos, fundamental para cualquier profesional que maneje información personal. Se abordan aspectos clave como el Reglamento General de Protección de Datos (RGPD) y la Ley Orgánica de Protección de Datos de Carácter Personal (LOPD), incluyendo sus modificaciones más recientes. Los estudiantes aprenderán sobre los derechos de los ciudadanos en relación a su información personal, así como las obligaciones que tienen las empresas y entidades encargadas del tratamiento de esos datos. Este tema es crucial para garantizar la privacidad y seguridad de la información en el ámbito profesional.

### Actividades propuestas

1. **Actividad: Desarrollo de un Resumen de Legislación sobre Protección de Datos**
   - **Descripción:** Los estudiantes deben resumir en sus propias palabras las principales normativas mencionadas (LOPD, LOPDGDD y RGPD) que afectan al almacenamiento y tratamiento de datos personales. Se espera que identifiquen los derechos de los usuarios y las obligaciones de las empresas según estas leyes.

2. **Actividad: Identificación de Responsabilidades Empresariales**
   - **Descripción:** Los alumnos deben listar y describir brevemente las principales responsabilidades empresariales derivadas del RGPD y LOPDGDD, enfocándose en cómo estas obligaciones impactan la gestión diaria de datos personales.

3. **Actividad: Creación de un Manual Simplificado**
   - **Descripción:** Los estudiantes tienen que crear un manual simplificado para empleados sobre el cumplimiento de las leyes de protección de datos (RGPD y LOPDGDD), incluyendo consejos prácticos y procedimientos recomendados.

4. **Actividad: Casos Prácticos de Violación de Datos**
   - **Descripción:** Los alumnos deben investigar y presentar ejemplos recientes de violaciones de datos y cómo estas situaciones podrían haberse evitado siguiendo las regulaciones mencionadas en el material proporcionado.

5. **Actividad: Análisis Comparativo LOPD vs RGPD**
   - **Descripción:** Se requiere a los estudiantes que hagan un análisis comparativo de la Ley Orgánica de Protección de Datos (LOPD) y el Reglamento General de Protección de Datos (RGPD), destacando las principales diferencias en términos de derechos del usuario y obligaciones empresariales.

6. **Actividad: Trabajo en Grupo sobre Derechos de Usuarios**
   - **Descripción:** Los estudiantes deben trabajar en grupos para investigar e informar sobre los derechos individuales que el RGPD otorga a los usuarios, cómo estos pueden ejercerlos y las implicaciones legales para las empresas.

7. **Actividad: Propuesta de Políticas Internas**
   - **Descripción:** Los alumnos deben diseñar propuestas detalladas para políticas internas basadas en el RGPD y LOPDGDD, que incluyan procedimientos de protección de datos, gestión del consentimiento y la eliminación de datos.

8. **Actividad: Ejercicios de Identificación de Datos Personales**
   - **Descripción:** Se propone a los estudiantes realizar ejercicios prácticos para identificar qué tipo de información se considera personal en el contexto del RGPD, incluyendo casos difusos o menos obvios.


<a id="big-data-introduccion-analisis-de-datos-inteligencia-de-negocios"></a>
## Big Data introducción, análisis de datos, inteligencia de negocios

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/001-Almacenamiento%20de%20la%20informaci%C3%B3n/006-Big%20Data%20introducci%C3%B3n%2C%20an%C3%A1lisis%20de%20datos%2C%20inteligencia%20de%20negocios)

### Introducción a los ejercicios

Este conjunto de ejercicios se enfoca en introducir los conceptos fundamentales del Big Data y cómo este impacta tanto la programación como la gestión de bases de datos. Los estudiantes aprenderán sobre el análisis de grandes volúmenes de información, sus desafíos técnicos y beneficios estratégicos para las empresas. El objetivo es familiarizar a los alumnos con la interrelación entre la Inteligencia Artificial y el Big Data, destacando la importancia de ambos campos en la toma de decisiones empresariales basadas en datos analíticos.

### Actividades propuestas

### Actividad 1: Introducción a Big Data
**Descripción:** Los estudiantes deben investigar y documentar ejemplos reales de cómo las empresas utilizan grandes cantidades de datos para mejorar sus operaciones. Se espera que comprendan la importancia del análisis de Big Data en el mundo empresarial.

### Actividad 2: Resumen Breve sobre IA y Big Data
**Descripción:** Los estudiantes deben elaborar un breve resumen sobre cómo la inteligencia artificial (IA) se integra con Big Data para mejorar el procesamiento y análisis de datos masivos. La actividad busca que comprendan las interconexiones entre ambos campos.

### Actividad 3: Caso de Estudio
**Descripción:** Los estudiantes deben analizar un caso de estudio real donde una empresa ha utilizado Big Data para tomar decisiones estratégicas. Se espera que identifiquen qué tipo de datos recopiló la empresa y cómo los utilizó para mejorar sus operaciones.

### Actividad 4: Ejercicio Práctico de Registro de Datos
**Descripción:** Los estudiantes deben diseñar un sistema simple para registrar comportamientos digitales, como clics en un sitio web o transacciones en una tienda online. La actividad busca que comprendan la importancia del registro y recopilación adecuada de datos.

### Actividad 5: Análisis de Datos Simples
**Descripción:** Los estudiantes deben realizar un análisis sencillo sobre un conjunto pequeño de datos proporcionado (por ejemplo, ventas diarias) para extraer patrones o información valiosa. Se espera que aprendan cómo se puede obtener valor a partir del análisis de datos.

### Actividad 6: Problemas y Retos en Big Data
**Descripción:** Los estudiantes deben identificar problemas y retos asociados con el manejo y procesamiento de grandes cantidades de datos, incluyendo aspectos técnicos (como potencia de proceso) y económicos. La actividad busca que comprendan las complejidades involucradas en Big Data.

### Actividad 7: Integración IA-Big Data
**Descripción:** Los estudiantes deben explorar cómo la integración entre inteligencia artificial y datos masivos puede mejorar el análisis predictivo de grandes conjuntos de información. Se espera que vean ejemplos prácticos donde esta combinación ofrece ventajas significativas.

### Actividad 8: Aplicaciones Empresariales
**Descripción:** Los estudiantes deben investigar y presentar cómo diversas industrias (retail, fintech, salud, etc.) usan Big Data para mejorar sus operaciones. La actividad busca que comprendan la amplia gama de aplicaciones prácticas del Big Data en el mundo real.

Estas actividades buscan preparar a los estudiantes para entender y trabajar con grandes conjuntos de datos, integrando conceptos clave como IA y estrategias empresariales basadas en análisis de datos.


<a id="ejercicio-de-final-de-unidad"></a>
## Ejercicio de final de unidad

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/001-Almacenamiento%20de%20la%20informaci%C3%B3n/101-Ejercicio%20de%20final%20de%20unidad)

### Introducción a los ejercicios

Esta carpeta contiene un conjunto de ejercicios diseñado para estudiantes del primer curso de DAM (Desarrollo de Aplicaciones Multiplataforma) que se centran en la unidad sobre el almacenamiento de información. El objetivo principal es consolidar los conocimientos adquiridos a lo largo de esta unidad, aplicandolos a través de un ejercicio práctico que combina el manejo de bases de datos con la representación y manipulación de la información en diferentes formatos. Los estudiantes practicarán habilidades como la creación, consulta y modificación de registros en una base de datos, así como la interpretación y almacenamiento efectivo de datos estructurados y no estructurados.

### Actividades propuestas

Dado que la carpeta proporcionada incluye un archivo markdown llamado "ejercicio.md", es probable que este contenga ejercicios relacionados con el almacenamiento de información y bases de datos. A partir de esta inferencia, aquí presento una lista de actividades adecuadas para estudiantes de Formación Profesional:

1. **Análisis de Casos de Uso**
   - Descripción: Los alumnos deben identificar y describir los casos de uso relacionados con el almacenamiento de información en un sistema basado en las instrucciones dadas. Se espera que entiendan cómo la interacción del usuario se traduce en acciones específicas sobre la base de datos.

2. **Diseño de Tablas Relacionales**
   - Descripción: En esta actividad, los estudiantes deben diseñar esquemas de tablas relacionalmente consistentes basándose en el contenido proporcionado en "ejercicio.md". Se espera que comprendan cómo estructurar y relacionar datos para un sistema eficiente.

3. **Escribir Consultas SQL Básicas**
   - Descripción: Los alumnos deben escribir consultas SQL simples, como SELECT, INSERT INTO, UPDATE y DELETE basándose en el contexto del almacenamiento de información dado en la carpeta. Se espera que aprendan a manipular datos en una base de datos.

4. **Resolución de Problemas de Errores SQL**
   - Descripción: Los estudiantes deben identificar y corregir errores comunes en sentencias SQL proporcionadas, mejorando así su habilidad para depurar código relacionado con bases de datos.

5. **Modelado Entidades-Relaciones (ER)**
   - Descripción: Se les pide a los alumnos que creen diagramas ER basados en el almacenamiento y la estructura de información proporcionada, mejorando así su comprensión del diseño lógico de bases de datos.

6. **Optimización de Consultas SQL**
   - Descripción: Los estudiantes deben examinar las consultas propuestas y sugerir métodos para mejorar su rendimiento o eficiencia. Se espera que aprendan a optimizar el acceso y manipulación de datos en una base de datos.

7. **Implementación de Contraints (Restricciones)**
   - Descripción: Los alumnos deben implementar restricciones de integridad en las tablas de la base de datos para garantizar la consistencia del almacenamiento de información, aprendiendo así cómo proteger los datos contra errores.

8. **Documentación del Modelo de Base de Datos**
   - Descripción: Se les solicita a los estudiantes que documenten el modelo de base de datos creado, describiendo su estructura y relaciones entre tablas. Esta actividad mejora sus habilidades en la comunicación técnica y la documentación de proyectos.

Estas actividades están diseñadas para fortalecer los conocimientos básicos de bases de datos y programación relacionados con el almacenamiento eficiente e inteligente de información, adaptándose al nivel y perfil académico del estudiantado de ciclos formativos.



<a id="bases-de-datos-relacionales"></a>
# Bases de datos relacionales

<a id="modelo-de-datos"></a>
## Modelo de datos

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/002-Bases%20de%20datos%20relacionales/001-Modelo%20de%20datos)

### Introducción a los ejercicios

Este conjunto de ejercicios se enfoca en la comprensión y aplicación del modelo de datos en bases de datos relacionales, particularmente centrado en entidades como Clientes, Productos y Pedidos. Los estudiantes aprenderán a identificar y definir atributos para cada entidad, así como a entender las relaciones entre ellas, principalmente a través de claves foráneas (FK) que vinculan pedidos con clientes y productos. Esta práctica es fundamental para desarrollar habilidades en la estructuración lógica de datos, lo cual es crucial en el desarrollo de sistemas de gestión de bases de datos eficientes.

### Actividades propuestas

### Actividad 1: Creación del Esquema Relacional

**Descripción:** Los estudiantes deben diseñar y crear un esquema relacional basado en la información proporcionada sobre Clientes, Productos y Pedidos. Se espera que identifiquen las relaciones entre estas entidades (por ejemplo, una relación de muchos a uno entre Pedidos y Clientes) y definan correctamente los tipos de datos para cada campo.

### Actividad 2: Consultas Básicas

**Descripción:** Los estudiantes deben escribir consultas SQL básicas que seleccionen información específica del esquema relacional creado en la actividad anterior. Esto incluirá cómo extraer detalles individuales como el nombre y teléfono de un cliente o los productos disponibles con su precio.

### Actividad 3: Consultas JOIN

**Descripción:** Los estudiantes deben aprender a escribir consultas que utilicen JOIN para combinar información entre diferentes tablas, por ejemplo, obtener detalles de un pedido junto con la información del cliente asociado al pedido y de los productos incluidos en el pedido.

### Actividad 4: Consultas Agregadas

**Descripción:** Los estudiantes deben crear consultas que utilicen funciones agregadas como SUM para calcular el total de todos los pedidos, AVG para obtener el precio promedio de los productos, o COUNT para contar cuántos clientes tienen pedidos activos.

### Actividad 5: Insertar Datos

**Descripción:** Se les pide a los estudiantes que inserten datos nuevos en las tablas creadas utilizando INSERT INTO. Deben asegurarse de respetar las relaciones entre las entidades y mantener la integridad de los datos, como establecer referencias correctas entre Cliente y Pedido.

### Actividad 6: Actualizar Datos

**Descripción:** Los estudiantes deben practicar cómo actualizar información existente en sus tablas utilizando UPDATE. Esto incluirá cambios en detalles del cliente, ajustes de precios en productos, o actualizaciones en la fecha o total de los pedidos.

### Actividad 7: Eliminar Datos

**Descripción:** Se les enseñará a los estudiantes cómo utilizar DELETE para eliminar registros de las tablas de forma segura. Esto también abordará el manejo adecuado de relaciones entre tablas, por ejemplo, asegurarse de no dejar orfandades en Pedidos si se elimina un Cliente.

### Actividad 8: Crear Procedimientos Almacenados

**Descripción:** Los estudiantes deben aprender a crear y utilizar procedimientos almacenados para realizar tareas comunes como insertar nuevos pedidos automáticamente con los datos necesarios o calcular impuestos en función del subtotal de cada pedido.

### Actividad 9: Trabajando con Transacciones

**Descripción:** A través de ejemplos prácticos, los estudiantes aprenderán cómo utilizar transacciones para garantizar la integridad y consistencia en operaciones que involucran múltiples consultas o cambios en diferentes tablas, como completar un pedido completo.

### Actividad 10: Manejo de Errores

**Descripción:** Los estudiantes deben escribir scripts básicos que manejen errores comunes al interactuar con la base de datos. Esto incluirá capturar excepciones y proporcionar respuestas útiles cuando se producen problemas como intentos fallidos de inserción debido a restricciones de clave foránea o limitaciones de tipos de datos.


<a id="terminologia-del-modelo-relacional"></a>
## Terminología del modelo relacional

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/002-Bases%20de%20datos%20relacionales/002-Terminolog%C3%ADa%20del%20modelo%20relacional)

### Introducción a los ejercicios

En esta carpeta de ejercicios se aborda la introducción al modelo relacional en bases de datos y se practican conceptos fundamentales como la creación de una base de datos y la definición de tablas con sus respectivas columnas y tipos de datos. Los estudiantes aprenderán a utilizar SQL para estructurar bases de datos empresariales, incluyendo cómo crear una nueva base de datos llamada "empresarial" y dos tablas importantes: "clientes" e "productos". Este conjunto de ejercicios es ideal para fortalecer las habilidades básicas en la gestión de información con SQL y entender la terminología específica del modelo relacional.

### crear base de datos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL sirve para crear y seleccionar una base de datos en un sistema de gestión de bases de datos relacional. En la primera línea, `CREATE DATABASE empresarial;`, el código crea una nueva base de datos llamada "empresarial". Es importante tener cuidado al nombrar las bases de datos porque deben ser únicas dentro del servidor.

La segunda línea, `USE empresarial;`, selecciona o establece la base de datos recién creada como la base de datos actual en la que se realizarán las operaciones siguientes. Esto significa que cualquier comando SQL adicional después de esta línea será ejecutado sobre la base de datos "empresarial".

Esta secuencia es fundamental cuando comienzas a trabajar con una nueva base de datos, ya que primero necesitas crearla y luego seleccionarla antes de poder agregar tablas, registros o realizar consultas en ella.

`002-crear base de datos.sql`

```sql
CREATE DATABASE empresarial;

USE empresarial;
```

### crear tabla de clientes
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL sirve para crear una tabla llamada "clientes" en la base de datos "empresarial". La tabla contiene cinco columnas: `Identificador`, `nombre`, `apellidos`, `telefono` y `email`. Cada columna tiene un tipo de dato específico que determina qué tipo de información puede almacenar. Por ejemplo, `Identificador` es de tipo INT (número entero) y se utiliza para identificar únicamente a cada cliente en la tabla. Las columnas `nombre`, `apellidos`, `telefono` y `email` son de tipo VARCHAR, lo que significa que pueden contener texto de longitud variable, con límites predefinidos para evitar datos demasiado largos.

La declaración ENGINE = InnoDB especifica el motor de base de datos que manejará cómo se almacenan los datos en esta tabla. InnoDB es un motor muy utilizado porque ofrece características avanzadas como transacciones y controles de integridad referencial, lo cual es crucial para bases de datos empresariales o relacionales más complejas.

Este código es importante porque establece la estructura básica para almacenar información sobre clientes en una base de datos, proporcionando un marco sólido que permite futuras consultas y manipulaciones de datos.

`003-crear tabla de clientes.sql`

```sql
CREATE TABLE `empresarial`.`clientes` (
  `Identificador` INT NOT NULL , 
  `nombre` VARCHAR(50) NOT NULL , 
  `apellidos` VARCHAR(100) NOT NULL , 
  `telefono` VARCHAR(50) NOT NULL , 
  `email` VARCHAR(100) NOT NULL 
) ENGINE = InnoDB;
```

### productos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL crea una nueva tabla en una base de datos llamada `empresarial`. La tabla se llama `productos` y está diseñada para almacenar información sobre diferentes productos. Cada fila de la tabla representa un producto específico, y cada columna almacena detalles como el identificador del producto (único para cada artículo), su nombre, descripción, precio y peso.

La estructura de la tabla incluye cinco columnas:
1. `Identificador`: Es un número entero (`INT`) que sirve como clave única para cada registro.
2. `nombre`: Un campo de texto variable con una longitud máxima de 50 caracteres (`VARCHAR(50)`) que almacena el nombre del producto.
3. `descripcion`: Utiliza el tipo de dato `TEXT`, lo cual significa que puede almacenar textos largos sin un límite estricto, permitiendo descripciones detalladas de los productos.
4. `precio` y `peso`: Ambas son columnas con el tipo de dato `DOUBLE(10,2)`, indicando que almacenan números decimales para representar cantidades como precios (por ejemplo, 9.99€) o pesos (como 5.34 kg). La precisión total es de diez dígitos con dos dígitos después del punto decimal.

El uso de `InnoDB` como motor de base de datos es importante porque este tipo de motor soporta transacciones y relaciones entre tablas, lo que facilita la gestión de bases de datos relacionales más complejas.

`004-productos.sql`

```sql
CREATE TABLE `empresarial`.`productos` (
  `Identificador` INT NOT NULL , 
  `nombre` VARCHAR(50) NOT NULL , 
  `descripcion` TEXT NOT NULL , 
  `precio` DOUBLE(10,2) NOT NULL , 
  `peso` DOUBLE(10,2) NOT NULL 
) ENGINE = InnoDB;
```

### Actividades propuestas

### Actividad 1: Creación de una Base de Datos

**Descripción:** Diseñar y crear una base de datos llamada "escuela" utilizando SQL. El objetivo es que los alumnos entiendan la estructura básica para establecer una nueva base de datos.

---

### Actividad 2: Definición de Tablas en Bases de Datos Relacionales

**Descripción:** Los estudiantes deben crear dos tablas, “alumnos” y “materias”, utilizando comandos SQL. Esta actividad permitirá a los alumnos familiarizarse con el proceso de definir esquemas de tabla.

---

### Actividad 3: Crear un Esquema Relacional

**Descripción:** Proporciona una descripción breve del contenido que la base de datos debe almacenar (por ejemplo, información sobre empleados y proyectos). Los estudiantes deben crear tablas y campos adecuados para este esquema.

---

### Actividad 4: Claves Primarias en SQL

**Descripción:** Explicar a los estudiantes cómo definir claves primarias en una tabla SQL y por qué son importantes. Los alumnos tendrán que implementar un campo de clave principal en al menos dos tablas distintas de la base de datos.

---

### Actividad 5: Tipos de Datos SQL

**Descripción:** Estudiar y aplicar diferentes tipos de datos SQL (INT, VARCHAR, TEXT) a campos específicos dentro del esquema relacional. Los alumnos deben justificar sus elecciones para cada tipo de dato en relación con los datos que almacenará la tabla.

---

### Actividad 6: Consultas Básicas en SQL

**Descripción:** Realizar consultas SELECT simples y compuestas desde las tablas creadas (como seleccionar todos los registros, seleccionar columnas específicas) para familiarizarse con cómo recuperar información de una base de datos relacional.

---

### Actividad 7: Relaciones entre Tablas

**Descripción:** Introducir la creación de relaciones entre tablas mediante claves foráneas. Los alumnos deben crear una relación entre las tablas "alumnos" y "materias".

---

### Actividad 8: Resolución de Problemas en SQL

**Descripción:** Proporcionar un conjunto de problemas relacionados con errores comunes al trabajar con SQL, como la falta de claves únicas o consultas incorrectamente formateadas. Los estudiantes deben identificar y corregir estos errores.

---

### Actividad 9: Documentación del Diseño

**Descripción:** Escribir documentación detallada que explique el diseño de las bases de datos creadas, incluyendo diagramas ER (Entity-Relationship) simples si es posible. Esto ayuda a los estudiantes a comprender la importancia de mantener registros claros y precisos en proyectos de desarrollo.

---

### Actividad 10: Aplicación del Modelo Relacional

**Descripción:** Integrar todas las habilidades aprendidas para crear una pequeña base de datos relacionada con un área relevante, como administración escolar o gestión de inventario. Esto permitirá a los estudiantes aplicar lo que han aprendido en un contexto práctico.

---

Cada actividad está diseñada para reforzar los conceptos clave del modelo relacional y la creación de bases de datos relacionales utilizando SQL, con el fin de preparar a los estudiantes para proyectos más complejos.


<a id="tipos-de-datos"></a>
## Tipos de datos

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/002-Bases%20de%20datos%20relacionales/003-Tipos%20de%20datos)

### Introducción a los ejercicios

Esta carpeta contiene ejercicios destinados a familiarizarte con los tipos de datos fundamentales y avanzados en bases de datos relacionales, específicamente enfocándose en MySQL. Los ejercicios te ayudarán a comprender la diferencia entre tipos de datos numéricos, cadenas, fechas y otros formatos especializados como JSON o BLOBs. A través de estos ejercicios, aprenderás a seleccionar el tipo adecuado para cada columna en función del contenido que almacenará y los requerimientos del sistema, lo cual es crucial para la eficiencia y efectividad de tus bases de datos.

### Actividades propuestas

### Actividades Propuestas:

1. **Identificación de Tipos de Datos**
   - Descripción: Los estudiantes deben identificar y clasificar diferentes tipos de datos presentes en un conjunto de variables proporcionadas. Se espera que aprendan a distinguir entre tipos numéricos, cadenas de texto, fechas y otros.

2. **Creación de Esquemas Básicos**
   - Descripción: Los estudiantes deben crear esquemas básicos para una base de datos simple utilizando los tipos de datos proporcionados en el archivo de ejercicios. Se espera que aprendan a definir tablas con columnas y sus respectivos atributos.

3. **Comparación entre Tipos de Datos**
   - Descripción: Los estudiantes deben comparar las diferencias entre diferentes tipos de datos numéricos (Tinyint, Smallint, Int, etc.) y explicar cuándo sería apropiado usar cada uno en una base de datos real. Se espera que comprendan la relevancia del tamaño y el rango de valores.

4. **Definición de Campos Textuales**
   - Descripción: Los estudiantes deben definir campos textuales adecuados para almacenar diferentes tipos de información, como descripciones largas o comentarios cortos. Se espera que aprendan a seleccionar entre Tinytext, Text y LongText basándose en la longitud del contenido.

5. **Uso de Enumeradores**
   - Descripción: Los estudiantes deben crear un ejemplo práctico usando enumeradores para limitar las entradas posibles en una columna de base de datos. Se espera que aprendan a aplicar restricciones de entrada utilizando esta herramienta útil.

6. **Tipos de Datos Temporales**
   - Descripción: Los estudiantes deben identificar cuándo sería apropiado usar tipos de datos temporales como Date, Time y DateTime en una base de datos real. Se espera que aprendan a manejar fechas y horas de manera efectiva.

7. **Creación de Tablas Complejas**
   - Descripción: Los estudiantes deben crear tablas más complejas incorporando múltiples tipos de datos, incluyendo numéricos, cadenas largas, temporales y booleanos. Se espera que aprendan a diseñar esquemas para bases de datos más realistas.

8. **Manipulación de JSON**
   - Descripción: Los estudiantes deben trabajar con un ejemplo simple donde utilicen tipos de datos JSON en MySQL para almacenar e ingresar datos estructurados. Se espera que comprendan la capacidad y flexibilidad de este tipo de datos.

9. **Implementación de BLOBs**
   - Descripción: Los estudiantes deben implementar campos de tipo Blob para guardar archivos binarios dentro de una base de datos, demostrando cómo se podría utilizar en aplicaciones reales. Se espera que comprendan la utilidad de almacenar y recuperar archivos desde bases de datos.

10. **Optimización del Diseño de Tablas**
    - Descripción: Los estudiantes deben revisar un diseño de tabla propuesto y sugerir mejoras basándose en los tipos de datos disponibles, como reducir el tamaño de columnas innecesariamente grandes o mejorar la eficiencia de ciertos campos. Se espera que aprendan a optimizar esquemas para rendimiento óptimo.

Estas actividades buscan que los estudiantes comprendan y apliquen los distintos tipos de datos disponibles en bases de datos relacionales, así como su importancia en el diseño de sistemas de gestión de información.


<a id="claves-primarias"></a>
## Claves primarias

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/002-Bases%20de%20datos%20relacionales/004-Claves%20primarias)

### Introducción a los ejercicios

En esta carpeta, se exploran los conceptos fundamentales sobre claves primarias en bases de datos relacionales. Los ejercicios te ayudarán a comprender qué es una clave primaria y cómo implementarla en tablas específicas utilizando lenguaje SQL. A través de estos ejercicios, desarrollarás habilidades para definir y modificar campos de identificación única en las tablas "clientes" y "productos", asegurando que cada registro tenga un valor numérico autoincremental que lo identifica inequívocamente.

### altero tabla
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL se utiliza para modificar la estructura de una tabla llamada `clientes` en una base de datos denominada `empresarial`. 

Primero, el fragmento añade una clave primaria a la tabla `clientes`, que es un campo único y no nulo que sirve para identificar de manera única cada registro en esta tabla. La columna elegida como clave primaria se llama `Identificador`.

Seguidamente, modifica la columna `Identificador` para asegurarse de que sea del tipo INT (número entero), que no acepte valores nulos (`NOT NULL`) y automáticamente incremente su valor para cada nuevo registro insertado en la tabla (`AUTO_INCREMENT`). Esto significa que cada vez que se añada un nuevo cliente, el sistema asignará automáticamente a este cliente un número de identificador único e incremental.

Estas modificaciones son esenciales para garantizar que cada cliente tenga una forma única y consistente de ser identificado dentro del sistema.

`002-altero tabla.sql`

```sql
ALTER TABLE `empresarial`.`clientes`
  ADD PRIMARY KEY (`Identificador`);
  
  ALTER TABLE clientes
  MODIFY COLUMN Identificador INT NOT NULL AUTO_INCREMENT;
```

### altero tabla de productos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para modificar una tabla llamada `productos` en la base de datos `empresarial`. En primer lugar, añade una clave primaria a la tabla. Una clave primaria es un campo o conjunto de campos que únicamente identifica cada fila en una tabla de forma única y no puede contener valores nulos.

La primera línea del código, `ALTER TABLE \`empresarial\`.\`productos\` ADD PRIMARY KEY (\`Identificador\`)`, añade la columna `Identificador` como clave primaria. Esto significa que todos los valores en esta columna deben ser únicos y no pueden estar vacíos (NULL).

La segunda línea del código, `ALTER TABLE productos MODIFY COLUMN Identificador INT NOT NULL AUTO_INCREMENT;`, cambia la definición de la columna `Identificador`. Aquí se especifica que:

1. La columna es del tipo de dato `INT` (número entero).
2. Los valores en esta columna no pueden ser nulos (`NOT NULL`), lo cual es un requisito para una clave primaria.
3. El atributo `AUTO_INCREMENT` indica que el sistema automáticamente incrementará este valor cada vez que se inserta un nuevo registro, garantizando así la unicidad de los identificadores.

Este código es importante porque ayuda a asegurar la integridad de la base de datos al crear una columna única y obligatoria para identificar sin ambigüedad cada producto en la tabla.

`003-altero tabla de productos.sql`

```sql
ALTER TABLE `empresarial`.`productos`
  ADD PRIMARY KEY (`Identificador`);
  
  ALTER TABLE productos
  MODIFY COLUMN Identificador INT NOT NULL AUTO_INCREMENT;
```

### Actividades propuestas

### Actividades Propuestas

1. **Creación de Tabla con Clave Primaria**
   - Los estudiantes deben crear una tabla nueva en una base de datos y añadirle un campo clave primario (`Identificador`) que sea numérico, autoincremental y único para cada registro.
   - Se pretende que entiendan cómo se define e implementa la clave primaria al diseñar una estructura de base de datos.

2. **Modificar Tabla Existente**
   - Los estudiantes deben modificar una tabla existente en la base de datos empresarial, añadiendo un campo clave primario (`Identificador`) similar a lo que ya se ha visto para las tablas `clientes` y `productos`.
   - Se espera que aprendan a alterar esquemas de base de datos existentes.

3. **Descripción de Claves Primarias**
   - Los estudiantes deben describir en un documento markdown cómo funciona la clave primaria en una tabla, incluyendo su propósito principal e importancia para el manejo eficiente de la información.
   - El objetivo es que comprendan y puedan explicar conceptos fundamentales sobre las claves primarias.

4. **Ejecución de Comandos SQL**
   - Los estudiantes deben ejecutar los comandos SQL proporcionados en el archivo `002-altero tabla.sql` y luego confirmar visualmente (mediante una consulta SELECT) que la clave primaria ha sido añadida correctamente a la tabla.
   - Se busca consolidar sus habilidades prácticas con SQL.

5. **Análisis Comparativo**
   - Los estudiantes deben analizar tanto el archivo `002-altero tabla.sql` como `003-altero tabla de productos.sql`, identificando similitudes y diferencias entre los comandos utilizados para añadir una clave primaria a las tablas `clientes` y `productos`.
   - El objetivo es mejorar la capacidad de análisis y comprensión del lenguaje SQL.

6. **Desarrollo de Scenarios**
   - Los estudiantes deben crear un escenario práctico (en markdown) donde se describa cómo una clave primaria podría ser útil en un sistema de gestión empresarial, incluyendo ejemplos concretos y casos de uso.
   - Se pretende que apliquen sus conocimientos a situaciones reales del mundo laboral.

7. **Creación de Consultas**
   - Los estudiantes deben crear consultas SQL simples para recuperar información de las tablas `clientes` y `productos`, utilizando la clave primaria (`Identificador`) como criterio principal.
   - Se busca que consoliden sus habilidades en la creación de consultas eficaces.

8. **Modificación de Datos**
   - Los estudiantes deben escribir un script SQL para modificar datos existentes en las tablas `clientes` y `productos`, teniendo cuidado con los valores de clave primaria.
   - El objetivo es que comprendan cómo manejar la integridad referencial al actualizar registros.

9. **Documentación del Proceso**
   - Los estudiantes deben documentar (en markdown) el proceso completo de creación, modificación y consulta de datos relacionados con las claves primarias en una base de datos empresarial.
   - Se pretende que desarrollen habilidades de comunicación técnica efectiva.

10. **Resolución de Problemas**
    - Los estudiantes deben plantear y resolver problemas comunes asociados a la gestión de claves primarias, como duplicidad o errores al añadir nuevos registros en una tabla.
    - El objetivo es mejorar sus capacidades resolutivas y habilidades diagnósticas en SQL.


<a id="restricciones-de-validacion"></a>
## Restricciones de validación

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/002-Bases%20de%20datos%20relacionales/005-Restricciones%20de%20validaci%C3%B3n)

### Introducción a los ejercicios

En esta carpeta de ejercicios, los estudiantes trabajarán con restricciones de validación en bases de datos relacionales utilizando SQL. Los ejercicios se centran en cómo asegurar la integridad de los datos mediante la implementación de condiciones específicas que deben cumplirse para garantizar que ciertos campos tengan formatos correctos y consistentes. En particular, aprenderán a añadir restricciones CHECK para verificar el tamaño del número telefónico y el formato del correo electrónico en una tabla llamada "clientes". Estos ejercicios ayudan a los estudiantes a comprender cómo proteger la calidad de los datos almacenados en bases de datos relacionales.

### restriccion de telefono
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para modificar una tabla existente llamada `clientes`. La instrucción `ALTER TABLE` es utilizada para añadir una nueva restricción a la tabla. En este caso, se agrega una restricción de validación que garantiza que el número telefónico registrado en cada fila de la columna `telefono` tenga exactamente 9 caracteres.

La parte `CHECK (CHAR_LENGTH(telefono) = 9)` es lo que define la condición para esta restricción. La función `CHAR_LENGTH()` se utiliza para contar el número total de caracteres en una cadena, y aquí se asegura de que esa longitud sea igual a 9. Esto significa que cualquier intento de ingresar o modificar un registro en la tabla `clientes` con un número telefónico que no tenga exactamente 9 dígitos será rechazado por el sistema de gestión de bases de datos, manteniendo así la integridad y consistencia de los datos.

Esta restricción es importante porque asegura que todos los números telefónicos almacenados en la base de datos cumplan con una longitud específica, lo cual puede ser un requisito para el formato o estructura de los teléfonos según las regulaciones locales o necesidades del negocio.

`001-restriccion de telefono.sql`

```sql
ALTER TABLE clientes
  ADD CONSTRAINT chk_telefono_length
  CHECK (CHAR_LENGTH(telefono) = 9);
```

### email
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para modificar una tabla existente llamada `clientes`. Específicamente, el código añade una restricción de validación a la columna `email` que asegura que todos los correos electrónicos ingresados cumplan con un formato estándar. La restricción se llama `chk_email_format`, y utiliza una expresión regular para comprobar si el valor en la columna `email` sigue un patrón específico de dirección de correo electrónico.

La expresión regular que se usa verifica si el contenido de la columna `email` tiene un formato similar al de los correos electrónicos típicos, donde hay una parte antes del signo "@" (que puede incluir letras, números y algunos caracteres especiales como puntos o guiones), seguido por un dominio que también sigue ciertas reglas. Esta validación es importante para garantizar que los datos ingresados en la tabla `clientes` sean correctos y útiles.

Este tipo de restricción ayuda a mantener la integridad y consistencia de los datos, asegurando que cualquier dato nuevo insertado en el campo `email` cumpla con las reglas definidas por la expresión regular.

`002-email.sql`

```sql
ALTER TABLE clientes
  ADD CONSTRAINT chk_email_format
  CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$');
```

### Actividades propuestas

1. **Restricción de longitud en campos**
   - Los estudiantes deben añadir una restricción de validación a una tabla existente que verifique la longitud mínima y máxima permitida para un campo específico (por ejemplo, nombre o dirección). Se espera que los alumnos entiendan cómo definir rangos de valores aceptables.

2. **Formato de correo electrónico**
   - Los estudiantes deben diseñar una restricción CHECK en SQL que valide el formato correcto de las direcciones de correo electrónico. El objetivo es que comprendan la importancia de asegurar que los datos ingresados cumplan con un patrón específico.

3. **Añadir varias restricciones a una tabla**
   - Los estudiantes deben agregar múltiples restricciones CHECK y UNIQUE a una tabla existente, verificando condiciones específicas para diferentes campos. Esto permitirá que entiendan cómo combinar diversas validaciones en una única tabla.

4. **Validación de fechas de nacimiento**
   - Proporciona a los estudiantes la tarea de implementar una restricción CHECK para garantizar que las fechas de nacimiento registradas sean anteriores al día actual. Esto ayudará a practicar el uso de funciones SQL y operadores relacionales.

5. **Restricción basada en cálculos**
   - Los estudiantes deben crear una restricción CHECK que verifique la suma o resta de dos campos numéricos, como por ejemplo, calcular la edad a partir de fechas de nacimiento. Esto facilitará el aprendizaje sobre cómo realizar operaciones aritméticas dentro de las restricciones.

6. **Restricción de dominio**
   - Los estudiantes deben crear una lista desplegable en su base de datos (usando CHECK) para limitar los valores que pueden introducirse en un campo específico, como el estado civil o tipo de cliente. Esto ayudará a entender cómo garantizar la consistencia y precisión de los datos.

7. **Restricción múltiple**
   - Los estudiantes deben implementar una restricción CHECK compuesta que verifique más de una condición al mismo tiempo (por ejemplo, el email debe tener un formato correcto Y ser único en la tabla). Esto les enseñará a combinar lógica booleana para crear condiciones complejas.

8. **Validación de rangos numéricos**
   - Los estudiantes deben agregar restricciones CHECK que verifiquen si ciertos campos numéricos (como edad, tarifa) están dentro de un rango determinado. Esto permitirá a los alumnos practicar la definición de límites mínimos y máximos en sus bases de datos.

Estas actividades proporcionan una variedad de ejercicios que cubren diferentes aspectos de las restricciones de validación, ayudando a los estudiantes a dominar el uso eficaz del lenguaje SQL para mantener la integridad de sus bases de datos.


<a id="indices-caracteristicas"></a>
## Índices. Características

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/002-Bases%20de%20datos%20relacionales/006-%C3%8Dndices.%20Caracter%C3%ADsticas)


<a id="el-valor-null"></a>
## El valor NULL

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/002-Bases%20de%20datos%20relacionales/007-El%20valor%20NULL)

### Introducción a los ejercicios

En esta sesión, trabajarás con el concepto de los valores NULL en bases de datos relacionales. El ejercicio te guiará para modificar una tabla llamada "clientes", permitiendo que la columna "apellidos" pueda almacenar valores nulos. Esto es útil cuando no se dispone de información obligatoria sobre los apellidos del cliente, lo cual refuerza tu comprensión sobre cómo manejar datos incompletos en las bases de datos. Este tipo de práctica te ayudará a familiarizarte con la gestión de datos faltantes y la flexibilidad en la estructura de tus tablas SQL.

### apellido null
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL modifica una columna existente en la tabla "clientes". Específicamente, está cambiando la columna llamada "apellidos" para permitir valores nulos (NULL). Antes de esta modificación, es posible que la columna "apellidos" no aceptara valores NULL y requeriera siempre un valor. Con este comando, ahora se permite que algunos registros tengan el campo "apellidos" vacío o sin definir, lo cual puede ser útil en casos donde una persona no tiene apellidos o no ha proporcionado esta información. Esto es importante porque aumenta la flexibilidad de la base de datos y puede hacerla más representativa del mundo real, donde no siempre se dispone de toda la información para cada registro.

`001-apellido null.sql`

```sql
ALTER TABLE clientes
  MODIFY COLUMN apellidos VARCHAR(100) NULL;
```

### Actividades propuestas

### Actividad 1: Modificación del Esquema de Tabla con Null

**Descripción:** Los estudiantes deben modificar un esquema de tabla existente para permitir valores nulos en una columna específica. Este ejercicio les ayudará a entender cómo y cuándo utilizar la cláusula `NULL` al trabajar con bases de datos relacionales.

### Actividad 2: Crear Tabla Con Valores Nulos

**Descripción:** Los estudiantes deberán crear una nueva tabla que incluya columnas permitiendo valores nulos. Esto les enseñará cómo definir correctamente la estructura inicial de las tablas en SQL.

### Actividad 3: Actualizar Datos Permitiendo Nulls

**Descripción:** En esta actividad, los alumnos actualizarán registros existentes para establecer algunos campos como null. Les ayudará a comprender el manejo de valores nulos en consultas y actualizaciones de datos.

### Actividad 4: Consultar Valores Nulos

**Descripción:** Los estudiantes deberán escribir consultas SQL que incluyan criterios para buscar filas con valores nulos en campos específicos. Les ayudará a entender cómo trabajar con los valores NULL en las consultas SELECT.

### Actividad 5: Eliminar Registros Con Nulls

**Description:** Este ejercicio consiste en eliminar registros de una tabla donde ciertos campos tienen un valor null. Los estudiantes aprenderán a utilizar condiciones para filtrar y eliminar datos basándose en la presencia o ausencia de valores nulos.

### Actividad 6: Creación Tabla Completamente Nullable

**Descripción:** Se les pedirá que creen una tabla entera con todas las columnas configuradas para permitir valores null. Esto servirá para consolidar su comprensión del uso y la importancia de los valores nulos en el diseño inicial de bases de datos.

### Actividad 7: Comparación NULL

**Descripción:** Los estudiantes deberán escribir consultas que hagan comparaciones con valores nulos, incluyendo operadores específicos para tratar estos casos. Ayudará a entender las peculiaridades del uso de los valores null en condiciones y expresiones.

### Actividad 8: Consulta Compleja Involucrando NULL

**Descripción:** Se les pedirá que escriban una consulta compleja que filtre datos basándose tanto en valores nulos como no nulos. Les ayudará a consolidar sus habilidades para manejar registros con valores null de manera eficiente y precisa.

### Actividad 9: Inserción Con Valores Nulos

**Descripción:** Los estudiantes deberán realizar inserciones en tablas que permiten valores nulos, especificando qué campos deben ser NULL. Les ayudará a entender cómo incluir datos nulos durante la creación de nuevos registros.

### Actividad 10: Actualización y Consulta Combinada

**Descripción:** En esta actividad se combinarán actualizaciones para establecer valores null en ciertos registros con consultas selectivas que buscan estos mismos valores. Les ayudará a familiarizarse con la utilización de los valores nulos tanto en transacciones como en consultas.


<a id="claves-ajenas"></a>
## Claves ajenas

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/002-Bases%20de%20datos%20relacionales/008-Claves%20ajenas)

### Introducción a los ejercicios

En esta carpeta de ejercicios, se exploran los conceptos básicos de las bases de datos relacionales, centrándose en la creación y manejo de claves foráneas. Los estudiantes aprenderán a crear una tabla llamada "pedidos" que está vinculada a dos tablas existentes: "clientes" y "productos". A través del uso de sentencias SQL, se establecerán relaciones entre estas tablas utilizando claves foráneas para asegurar la integridad referencial en las operaciones CRUD (Crear, Leer, Actualizar, Borrar). Esta práctica es crucial para comprender cómo estructurar correctamente bases de datos relacionales y mantener sus datos consistentes.

### crear pedidos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para crear una tabla llamada `pedidos` en la base de datos denominada `empresarial`. La tabla contiene cuatro columnas: `Identificador`, `fecha`, `id_cliente` y `id_producto`.

La columna `Identificador` es el campo clave principal (primary key) de la tabla, lo que significa que cada valor dentro debe ser único e identificar de manera única un pedido. Esta columna también está configurada para incrementarse automáticamente (`AUTO_INCREMENT`) con cada nuevo registro añadido.

Las columnas `fecha`, `id_cliente` y `id_producto` son campos adicionales necesarios para almacenar información sobre la fecha del pedido, el cliente asociado (mediante su identificador) y el producto solicitado (también por su identificador).

Esta tabla es importante porque organiza los datos de pedidos en un formato estructurado que facilita la consulta y manipulación de datos relacionados con ventas o servicios proporcionados. Específicamente, esta tabla establece las bases para futuras consultas SQL donde podrás vincular los pedidos a clientes y productos utilizando las claves foráneas (`id_cliente` y `id_producto`).

`002-crear pedidos.sql`

```sql
CREATE TABLE `empresarial`.`pedidos` (`Identificador` INT NOT NULL AUTO_INCREMENT , `fecha` DATE NOT NULL , `id_cliente` INT NOT NULL , `id_producto` INT NOT NULL , PRIMARY KEY (`Identificador`)) ENGINE = InnoDB;
```

### clave foranea de pedidos a clientes
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para establecer una relación entre dos tablas en una base de datos: la tabla `pedidos` y la tabla `clientes`. Específicamente, el código crea lo que se conoce como una "clave foránea" (foreign key), que es un tipo especial de campo que se usa para vincular datos en diferentes tablas. En este caso, la clave foránea se denomina `pedidosaclientes` y está asociada al campo `id_cliente` en la tabla `pedidos`.

La función principal de esta clave foránea es asegurar que los valores en el campo `id_cliente` dentro de la tabla `pedidos` coincidan con los valores del campo `Identificador` en la tabla `clientes`. Esto significa que no se permitirá agregar un nuevo pedido para un cliente que no está registrado en la tabla `clientes`.

Además, las opciones `ON DELETE RESTRICT ON UPDATE RESTRICT` indican cómo deben manejarse ciertas operaciones. En este caso, si intentas eliminar un registro de la tabla `clientes`, el sistema impedirá dicha acción si ese cliente tiene pedidos asociados en la tabla `pedidos`. De igual manera, si se modifica (`UPDATE`) el identificador del cliente en la tabla `clientes`, esto no será permitido si existen registros en `pedidos` que dependan de dicho identificador. Esto ayuda a mantener la integridad y coherencia de los datos entre ambas tablas.

`003-clave foranea de pedidos a clientes.sql`

```sql
ALTER TABLE `pedidos` ADD CONSTRAINT `pedidosaclientes` FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;
```

### clave foranea de pedidos a productos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para modificar una tabla existente llamada `pedidos`. La acción específica que realiza es agregar una restricción (constraint) conocida como clave foránea (foreign key). Esta clave foránea vincula la columna `id_producto` en la tabla `pedidos` con la columna `Identificador` en otra tabla llamada `productos`.

La importancia de esta operación radica en que establece una relación entre dos tablas, permitiendo que el sistema gestor de bases de datos controle qué valores son válidos para `id_producto` en función de los valores existentes en `Identificador`. Las opciones `ON DELETE RESTRICT ON UPDATE RESTRICT` indican que si intentas eliminar un registro en la tabla `productos`, se prohibirá si aún hay registros relacionados en `pedidos`, y lo mismo ocurre durante una actualización. Esto ayuda a mantener la integridad de los datos entre las dos tablas, evitando referencias inconsistentes o perdidas.

`004-clave foranea de pedidos a productos.sql`

```sql
ALTER TABLE `pedidos` ADD CONSTRAINT `pedidosaproductos` FOREIGN KEY (`id_producto`) REFERENCES `productos`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;
```

### insercion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para insertar un nuevo registro en una tabla llamada `pedidos`. La instrucción `INSERT INTO` especifica la tabla donde queremos agregar los datos, que en este caso es `pedidos`. Dentro del paréntesis después de `INSERT INTO`, se listan las columnas de la tabla a las que deseamos asignar valores nuevos: `Identificador`, `fecha`, `id_cliente` y `id_producto`.

En el segundo bloque entre paréntesis, se proporcionan los valores específicos para cada una de esas columnas. El valor `NULL` se utiliza para la columna `Identificador`, lo cual indica que el sistema debe asignar automáticamente un valor único (por ejemplo, si `Identificador` está configurado como clave primaria autoincremental). La fecha '2025-09-25' será ingresada en la columna `fecha`. Los valores '12' y '19' serán insertados respectivamente en las columnas `id_cliente` e `id_producto`, que probablemente son claves foráneas que hacen referencia a tablas de clientes y productos.

Este tipo de inserción es importante porque permite añadir nuevos datos a la base de datos, manteniendo relaciones coherentes con otras tablas a través del uso de claves foráneas.

`005-insercion.sql`

```sql
INSERT INTO `pedidos` 
(
  `Identificador`, 
  `fecha`, 
  `id_cliente`, 
  `id_producto`
) VALUES (
  NULL, 
  '2025-09-25', 
  '12', 
  '19'
);
```

### Actividades propuestas

### Actividad 1: Crear Tabla de Pedidos

**Descripción:** Los alumnos deben crear una tabla llamada `pedidos` en una base de datos existente que tenga campos para identificador, fecha, id del cliente y id del producto. Se espera que los estudiantes aprendan a definir estructuras de tablas basadas en requisitos específicos.

### Actividad 2: Relacionar Pedidos con Clientes

**Descripción:** Los alumnos deberán añadir una clave foránea (`id_cliente`) a la tabla `pedidos`, relacionándola con la tabla `clientes`. Se espera que los estudiantes entiendan cómo establecer relaciones entre tablas usando claves foráneas.

### Actividad 3: Relacionar Pedidos con Productos

**Descripción:** Los alumnos deberán añadir una clave foránea (`id_producto`) a la tabla `pedidos`, relacionándola con la tabla `productos`. Se espera que los estudiantes comprendan cómo mantener la integridad referencial entre tablas.

### Actividad 4: Consultar Información Relacionada

**Descripción:** Los alumnos deben escribir consultas SQL para obtener información de pedidos, incluyendo datos relacionados del cliente y el producto. Se espera que aprendan a realizar operaciones JOIN en múltiples tablas.

### Actividad 5: Validar Restricciones ON DELETE y ON UPDATE

**Descripción:** Los alumnos deben investigar y aplicar restricciones `ON DELETE RESTRICT` y `ON UPDATE RESTRICT` para las claves foráneas. Se espera que comprendan el impacto de estas restricciones en la integridad de los datos.

### Actividad 6: Agregar un Nuevo Pedido

**Descripción:** Los alumnos deben insertar manualmente un nuevo pedido en la tabla `pedidos`. El pedido debe incluir una fecha, id del cliente existente y id de producto. Se espera que aprendan a realizar inserciones correctas con claves foráneas.

### Actividad 7: Modificar Pedidos Existentes

**Descripción:** Los alumnos deben modificar la información de un pedido existente en la tabla `pedidos`. Se espera que comprendan cómo actualizar registros mientras se mantienen las restricciones establecidas por las claves foráneas.

### Actividad 8: Eliminar Pedidos y Manejo de Restricciones

**Descripción:** Los alumnos deben intentar eliminar un pedido en la tabla `pedidos` y observar el comportamiento debido a las restricciones definidas. Se espera que entiendan los efectos de las restricciones ON DELETE en las relaciones entre tablas.

### Actividad 9: Diseño de Esquema Relacional

**Descripción:** Los alumnos deben diseñar un esquema relacional para una nueva entidad, como proveedores, y relacionarla con clientes o productos. Se espera que aprendan a planificar esquemas que reflejen relaciones reales entre entidades en un sistema.

### Actividad 10: Crear Consultas Complejas

**Descripción:** Los alumnos deben crear consultas SQL más complejas para obtener estadísticas sobre pedidos, como el total de pedidos por cliente o los productos más solicitados. Se espera que aprendan a combinar múltiples operaciones y funciones en una consulta única.


<a id="vistas"></a>
## Vistas

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/002-Bases%20de%20datos%20relacionales/009-Vistas)

### Introducción a los ejercicios

Esta carpeta contiene ejercicios relacionados con la creación y uso de vistas en bases de datos relacionales. En estos ejercicios, los estudiantes aprenderán a realizar consultas SQL complejas que combinan información de múltiples tablas utilizando INNER JOIN y LEFT JOIN. El objetivo principal es introducir el concepto de vistas como un mecanismo para simplificar la visualización y acceso a conjuntos de datos recurrentes. Los ejercicios practican habilidades clave en diseño de bases de datos, como comprensión de relaciones entre tablas y optimización de consultas SQL.

### peticion inicial
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL realiza una consulta que combina información de varias tablas para proporcionar detalles detallados sobre un pedido. La consulta selecciona la fecha del pedido, el nombre y los apellidos del cliente que hizo el pedido, así como el nombre del producto y sus precios brutos e incluyendo IVA.

El código utiliza operaciones `LEFT JOIN` para combinar las tablas `pedidos`, `clientes` y `productos`. Estos joins aseguran que se obtengan todos los pedidos registrados en la base de datos, incluso si no hay un cliente o producto asociado directamente (lo que podría suceder en casos especiales).

Además, el código calcula el IVA del producto y el total incluyendo IVA usando expresiones aritméticas en SQL. Esto ayuda a presentar información financiera relevante de manera clara y organizada para cualquier pedido realizado.

En resumen, esta consulta es útil para generar informes detallados sobre pedidos que incluyen datos relacionados del cliente y el producto asociado, junto con cálculos financieros relevantes.

`001-peticion inicial.sql`

```sql
SELECT 
pedidos.fecha,
clientes.nombre,
clientes.apellidos,
productos.nombre,
productos.precio,
productos.precio*0.16 as IVA,
productos.precio*1.16 as Total
FROM pedidos

LEFT JOIN clientes
ON pedidos.id_cliente = clientes.Identificador

LEFT JOIN productos
ON pedidos.id_producto = productos.Identificador
;
```

### creo una vista
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL crea una vista llamada `vista_pedidos` que combina información de varias tablas para facilitar la consulta de datos relacionados con los pedidos. La vista selecciona detalles como la fecha del pedido, el nombre y apellidos del cliente, el nombre y precio del producto, además del IVA y el total calculado para cada artículo en el pedido.

El código utiliza dos operaciones `LEFT JOIN` para unir las tablas `pedidos`, `clientes` y `productos`. Estos joins aseguran que se incluyan todos los pedidos, incluso si no hay información asociada en las otras tablas. Esto es importante porque permite tener una visión completa de cada pedido sin perder datos debido a combinaciones incompletas.

La creación de esta vista simplifica mucho la consulta de detalles sobre pedidos para usuarios o aplicaciones que necesitan acceder a este tipo de información sin complicarse con las uniones y cálculos necesarios.

`002-creo una vista.sql`

```sql
CREATE VIEW vista_pedidos AS 
SELECT 
pedidos.fecha,
clientes.nombre as "nombre de cliente",
clientes.apellidos,
productos.nombre as "nombre de producto",
productos.precio,
productos.precio*0.16 as IVA,
productos.precio*1.16 as Total
FROM pedidos

LEFT JOIN clientes
ON pedidos.id_cliente = clientes.Identificador

LEFT JOIN productos
ON pedidos.id_producto = productos.Identificador
;
```

### Actividades propuestas

### Actividad 1: Creación de Vistas Similares
**Descripción:** Los estudiantes deben replicar la creación de vistas similares a la proporcionada en el archivo `002-creo una vista.sql`, pero con datos diferentes y consultas ligeramente modificadas. Se pretende que los alumnos entiendan cómo crear y utilizar vistas para simplificar las consultas sobre sus bases de datos.

### Actividad 2: Modificación de Consultas
**Descripción:** Los estudiantes deben modificar la consulta original del archivo `001-peticion inicial.sql` añadiendo nuevas condiciones o campos en los JOINs. Se espera que aprendan a manipular y optimizar consultas complejas utilizando JOINs.

### Actividad 3: Exploración de Datos con Vistas
**Descripción:** Los alumnos deben realizar una consulta sobre la vista creada para extraer información específica, como por ejemplo filtrar pedidos en un rango de fechas determinado. Se pretende que comprendan cómo acceder a datos almacenados en vistas.

### Actividad 4: Creación de Vistas Personalizadas
**Descripción:** Los estudiantes deben crear una nueva vista basada en la información de las tablas `clientes`, `productos` y `pedidos`. La vista debe proporcionar un resumen del total de ventas por cliente. Se espera que aprendan a diseñar vistas útiles para el análisis de datos.

### Actividad 5: Comparación entre Consultas y Vistas
**Descripción:** Los alumnos deben ejecutar la consulta original y la vista creada, comparando los tiempos de respuesta y la complejidad en ambos casos. Se pretende que comprendan las ventajas de usar vistas sobre consultas directas.

### Actividad 6: Documentación de Vistas
**Descripción:** Los estudiantes deben escribir una descripción detallada del propósito, diseño e implementación de una vista personalizada. Esto ayudará a entender la importancia de documentar claramente las vistas en un entorno empresarial real.

### Actividad 7: Consultas Complejas sobre Vistas
**Descripción:** Los alumnos deben realizar consultas complejas basadas en múltiples tablas utilizando una vista previamente creada. Se espera que aprendan a combinar datos de varias fuentes para obtener insights útiles.

### Actividad 8: Actualización y Mantenimiento de Vistas
**Descripción:** A pesar de no poder modificar directamente las vistas, los estudiantes deben aprender cómo mantener actualizada la información en ellas a través de consultas de actualización a las tablas subyacentes. Se pretende que comprendan el ciclo de vida de una vista.

### Actividad 9: Evaluación y Optimización de Vistas
**Descripción:** Los alumnos deberán analizar la eficiencia de diferentes vistas creadas, evaluando cómo pueden ser optimizadas para mejorar su rendimiento en términos de velocidad y recursos utilizados. Se espera que aprendan a realizar pruebas y ajustes para mejorar el rendimiento de las vistas.

### Actividad 10: Implementación de Vistas en Proyectos
**Descripción:** Los estudiantes deben aplicar sus conocimientos sobre vistas en un proyecto práctico, diseñando e implementando una base de datos con varias vistas que faciliten la consulta y análisis de los datos. Se pretende que pongan en práctica lo aprendido para resolver problemas reales en contextos empresariales.


<a id="usuarios-privilegios"></a>
## Usuarios. Privilegios

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/002-Bases%20de%20datos%20relacionales/010-Usuarios.%20Privilegios)

### Introducción a los ejercicios

En esta carpeta, encontrarás ejercicios relacionados con la creación y configuración de usuarios en bases de datos MySQL. Los ejercicios te guiarán a través del proceso de crear usuarios y asignarles privilegios específicos según sus necesidades. En el primer ejercicio, aprenderás a crear un usuario completo con todos los permisos para una base de datos específica llamada `empresarial`. El segundo ejercicio se centra en la creación de un usuario limitado que solo puede realizar consultas (SELECT) sobre todas las bases de datos. Estos ejercicios te ayudarán a comprender cómo gestionar usuarios y privilegios en entornos de bases de datos relacionales, una habilidad fundamental para mantener el control y seguridad de tus sistemas.

### crear nuevo usuario con todos los permisos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL crea un nuevo usuario en una base de datos y le otorga permisos específicos. En primer lugar, se crea el usuario llamado "usuarioempresarial" que puede conectarse desde localhost (la misma máquina donde está la base de datos) con una contraseña segura. A continuación, se establecen límites para este usuario, permitiéndole hacer cualquier tipo de conexión sin restricciones en términos de número de consultas o conexiones simultáneas por hora.

Finalmente, se le otorgan todos los privilegios sobre la base de datos llamada `empresarial` a este nuevo usuario. Esto significa que el usuario tiene permiso para realizar cualquier acción dentro de esa base de datos, como crear tablas, insertar, modificar y eliminar datos. El comando `FLUSH PRIVILEGES` asegura que los cambios sean aplicados inmediatamente.

Este tipo de instrucciones es crucial en la gestión de bases de datos, ya que permite controlar quién tiene acceso a qué información y qué acciones puede realizar con ella, protegiendo así los datos y garantizando su correcto manejo.

`001-crear nuevo usuario con todos los permisos.sql`

```sql
CREATE USER 
'usuarioempresarial'@'localhost' 
IDENTIFIED WITH 
caching_sha2_password BY '***';

GRANT USAGE ON *.* TO 'usuarioempresarial'@'localhost';

ALTER USER 'usuarioempresarial'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 
MAX_CONNECTIONS_PER_HOUR 0 
MAX_UPDATES_PER_HOUR 0 
MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON `empresarial`.* 
TO 'usuarioempresarial'@'localhost';

FLUSH PRIVILEGES;
```

### crear un usuario limitado
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para crear y configurar un usuario de base de datos con permisos limitados. Primero, se crea el usuario llamado `usuariosololectura` en el servidor local (`localhost`) y se le asigna una contraseña utilizando el método `caching_sha2_password`. Luego, a este usuario se le otorga el privilegio de seleccionar (consultar) cualquier tabla en todas las bases de datos existentes usando la instrucción `GRANT SELECT ON *.* TO 'usuariosololectura'@'localhost';`.

Además, se modifican los límites de conexión y consultas para este usuario específico utilizando la sentencia `ALTER USER`. Esto establece que el usuario no está sujeto a restricciones en cuanto al número máximo de consultas por hora, conexiones simultáneas o actualizaciones por hora. Sin embargo, luego se otorga al usuario el privilegio completo sobre una base de datos específica llamada `empresarial` con la instrucción `GRANT ALL PRIVILEGES ON empresarial.* TO 'usuariosololectura'@'localhost';`.

Este código es importante para gestionar y asegurar el acceso a las bases de datos, permitiendo que ciertos usuarios solo puedan leer información (lo cual puede ser útil en entornos donde se necesita compartir datos sin dar la posibilidad de modificarlos) mientras mantienen el control completo sobre una base de datos específica.

`002-crear un usuario limitado.sql`

```sql
CREATE USER 
'usuariosololectura'@'localhost' 
IDENTIFIED WITH 
caching_sha2_password BY '***';

GRANT 
SELECT 
ON *.* 
TO 'usuariosololectura'@'localhost';

ALTER USER 
'usuariosololectura'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON 
`empresarial`.* 
TO 'usuariosololectura'@'localhost';
```

### Actividades propuestas

### Actividad 1: Creación de un Usuario con Permisos Complejos

**Descripción:** Crea un nuevo usuario en MySQL que tenga permisos limitados para una base de datos específica. Asegúrate de configurar restricciones como la velocidad máxima de consultas y conexiones permitidas.

### Actividad 2: Configuración Básica de Privilegios

**Descripción:** Diseña un script SQL que cree un nuevo usuario con acceso solo a lectura en todas las bases de datos. Asegúrate de ajustar los parámetros de seguridad adecuadamente para este perfil de usuario.

### Actividad 3: Análisis Comparativo de Permisos

**Descripción:** Analiza el contenido de ambos scripts proporcionados y compara la diferencia entre un usuario con todos los permisos y uno solo lectura. Identifica las líneas clave que diferencian cada configuración.

### Actividad 4: Crear Usuario Lector en Base Específica

**Descripción:** Modifica el segundo script para crear un usuario que tenga acceso solo a lectura en una base de datos específica, en lugar de todas las bases de datos. Asegúrate de ajustar los parámetros necesarios.

### Actividad 5: Asignación de Privilegios Personalizados

**Descripción:** Crea un script SQL para asignar privilegios personalizados a un nuevo usuario. Este usuario solo podrá ejecutar operaciones SELECT y INSERT en una base de datos específica.

### Actividad 6: Restricción de Consultas por Hora

**Descripción:** Ajusta el segundo script para limitar la cantidad máxima de consultas que puede realizar un usuario durante una hora determinada, manteniendo los demás permisos originales.

### Actividad 7: Configuración Avanzada de Seguridad

**Descripción:** Desarrolla un script que configure múltiples restricciones de seguridad para un nuevo usuario. Esto incluirá la configuración del límite de consultas, conexiones y actualizaciones por hora.

### Actividad 8: Modificación de Contraseñas y Permisos

**Descripción:** Proporciona instrucciones paso a paso sobre cómo cambiar la contraseña de un usuario existente y ajustar sus permisos. Asegúrate de guardar los cambios para que sean efectivos.

### Actividad 9: Comprobación de Privilegios del Usuario

**Descripción:** Escribe una consulta SQL que muestre todos los privilegios otorgados a un usuario específico en todas las bases de datos y tablas. Esto ayudará a verificar la configuración actual de permisos.

### Actividad 10: Documentación Básica de Scripts SQL

**Descripción:** Crea una breve guía o manual sobre cómo usar los scripts proporcionados para crear usuarios y otorgar privilegios en MySQL, enfocándote en explicaciones claras y concisas.


<a id="lenguaje-de-descripcion-de-datos-ddl"></a>
## Lenguaje de descripción de datos (DDL)

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/002-Bases%20de%20datos%20relacionales/011-Lenguaje%20de%20descripci%C3%B3n%20de%20datos%20%28DDL%29)


<a id="lenguaje-de-control-de-datos-dcl"></a>
## Lenguaje de control de datos (DCL)

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/002-Bases%20de%20datos%20relacionales/012-Lenguaje%20de%20control%20de%20datos%20%28DCL%29)


<a id="ejercicio-de-final-de-unidad-1"></a>
## Ejercicio de final de unidad

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/002-Bases%20de%20datos%20relacionales/101-Ejercicio%20de%20final%20de%20unidad)

### Introducción a los ejercicios

Esta carpeta contiene un conjunto de ejercicios diseñados para ayudarte a consolidar tus conocimientos sobre bases de datos relacionales, específicamente enfocándose en el final de unidad. El ejercicio principal te permitirá aplicar conceptos clave como la creación y manipulación de tablas, diseño de esquemas relacionales, consultas SQL básicas y avanzadas, incluyendo la integración de múltiples tablas mediante INNER JOIN y OUTER JOIN. La actividad está pensada para que practiques la resolución de problemas reales que enfrentarías en entornos profesionales, lo cual te preparará adecuadamente para proyectos futuros relacionados con bases de datos.

### Actividades propuestas

### Actividades Propuestas:

1. **Análisis del Caso Práctico**
   - **Descripción:** Los estudiantes deben leer el caso práctico proporcionado en el archivo y identificar los requisitos del sistema de bases de datos relacionales que se presenta. Se pretende que comprendan cómo se estructuran las tablas y las relaciones entre ellas.

2. **Creación de Diagrama Entidad-Relación (ER)**
   - **Descripción:** Basándose en el caso práctico, los alumnos deben crear un diagrama entidad-relación para representar visualmente la estructura propuesta del sistema de bases de datos.

3. **Traducción ER a SQL**
   - **Descripción:** A partir del diagrama ER que han creado, los estudiantes deberán escribir las consultas en lenguaje SQL necesarias para crear las tablas y definir las relaciones entre ellas.

4. **Ejecución Consultas Básicas**
   - **Descripción:** Los alumnos deben ejecutar consultas SELECT básicas en la base de datos creada, extrayendo información de una o varias tablas según los requerimientos descritos en el caso práctico.

5. **Inserción y Actualización de Datos**
   - **Descripción:** Los estudiantes aprenderán a insertar nuevos registros y actualizar datos existentes en las tablas utilizando consultas INSERT y UPDATE, respaldados por ejemplos del caso proporcionado.

6. **Manejo de Claves Foráneas**
   - **Descripción:** Se pide a los alumnos que manipulen claves foráneas entre las diferentes tablas para garantizar la integridad referencial en el sistema de base de datos.

7. **Consultas JOIN Avanzadas**
   - **Descripción:** Los estudiantes deben practicar consultas JOIN para combinar información desde múltiples tablas relacionadas, mejorando sus habilidades en la extracción y manipulación de datos cruzados.

8. **Resolución de Problemas Prácticos**
   - **Descripción:** Se presenta a los alumnos con situaciones reales que pueden surgir al trabajar con bases de datos relacionales, como errores comunes o optimización de consultas, para resolverlos en equipo y aprender juntos.

Estas actividades están diseñadas para complementar el estudio teórico proporcionado en el caso práctico y fomentar la aplicación práctica de los conceptos aprendidos.



<a id="realizacion-de-consultas"></a>
# Realización de consultas

<a id="proyeccion-seleccion-y-ordenacion-de-registros"></a>
## Proyección, selección y ordenación de registros

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/003-Realizaci%C3%B3n%20de%20consultas/001-Proyecci%C3%B3n%2C%20selecci%C3%B3n%20y%20ordenaci%C3%B3n%20de%20registros)

### Introducción a los ejercicios

Esta carpeta contiene una serie de ejercicios destinados a practicar la realización de consultas en SQL, enfocándose específicamente en proyección, selección y ordenación de registros. Los estudiantes aprenderán cómo seleccionar datos completos o parciales desde una tabla llamada "clientes", cómo aplicar alias a los nombres de las columnas para mejorar la legibilidad de los resultados, y cómo ordenar estos resultados tanto en orden ascendente como descendente. Además, se practicará el uso de cláusulas WHERE con operadores de comparación simples y expresiones LIKE que incluyen comodines para realizar búsquedas más complejas basadas en criterios específicos. Estos ejercicios son fundamentales para entender los conceptos básicos de consultas SQL necesarios para trabajar eficazmente con bases de datos.

### Datos de ejemplo
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para insertar múltiples registros en una tabla llamada `clientes`. En concreto, cada línea dentro del bloque `VALUES` proporciona información sobre un nuevo cliente y la inserta en la base de datos. La información que se agrega incluye el nombre, apellidos, número telefónico y dirección de correo electrónico del cliente.

La estructura es importante porque permite añadir varios registros de una sola vez, lo cual es muy útil cuando necesitas introducir una gran cantidad de datos iniciales en la base de datos. Cada paréntesis dentro de `VALUES` representa un registro completo para un único cliente, y todos estos registros se insertan juntos con el comando `INSERT INTO`.

Esta técnica es valiosa porque simplifica la carga inicial de datos, haciendo que el proceso de llenar una tabla con información sea mucho más eficiente y rápido que hacerlo registro por registro.

`001-Datos de ejemplo.sql`

```sql
INSERT INTO clientes (nombre, apellidos, telefono, email) VALUES
('Carlos', 'García López',      '612345678', 'carlos.garcia@example.com'),
('María', 'Martínez Fernández', '623456789', 'maria.martinez@example.com'),
('José', 'Rodríguez Sánchez',   '634567890', 'jose.rodriguez@example.com'),
('Laura', 'Gómez Díaz',         '645678901', 'laura.gomez@example.com'),
('Antonio', 'Fernández Ruiz',   '656789012', 'antonio.fernandez@example.com'),
('Ana', 'López Jiménez',        '667890123', 'ana.lopez@example.com'),
('Francisco', 'Díaz Moreno',    '678901234', 'francisco.diaz@example.com'),
('Lucía', 'Ruiz Hernández',     '689012345', 'lucia.ruiz@example.com'),
('David', 'Sánchez Torres',     '690123456', 'david.sanchez@example.com'),
('Elena', 'Romero Ramos',       '601234567', 'elena.romero@example.com'),
('Manuel', 'Navarro Ortega',    '602345678', 'manuel.navarro@example.com'),
('Isabel', 'Castro Vargas',     '603456789', 'isabel.castro@example.com'),
('Pedro', 'Rubio Molina',       '604567890', 'pedro.rubio@example.com'),
('Sara', 'Ortega Serrano',      '605678901', 'sara.ortega@example.com'),
('Javier', 'Morales Gil',       '606789012', 'javier.morales@example.com'),
('Beatriz', 'Hernández Cruz',   '607890123', 'beatriz.hernandez@example.com'),
('Miguel', 'Torres León',       '608901234', 'miguel.torres@example.com'),
('Carmen', 'Domínguez Flores',  '609012345', 'carmen.dominguez@example.com'),
('Raúl', 'Vargas Castillo',     '611223344', 'raul.vargas@example.com'),
('Patricia', 'Santos Delgado',  '622334455', 'patricia.santos@example.com');
```

### seleccion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL selecciona todos los datos de la tabla llamada "clientes". La instrucción `SELECT *` indica que se deben devolver todas las columnas y todas las filas disponibles en esa tabla. Es una forma rápida de ver el contenido completo de la tabla sin especificar columnas individuales, lo cual es útil para un primer vistazo a los datos cuando no estás seguro de cuáles son exactamente las necesidades o características de la información almacenada.

`002-seleccion.sql`

```sql
SELECT * FROM clientes;
```

### solo quiero ver los nombres
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL selecciona la columna "nombre" de la tabla llamada "clientes". Lo que hace es recopilar todos los nombres registrados en esa tabla sin mostrar ninguna otra información como direcciones o teléfonos. Es importante porque te permite obtener solo la información específica que necesitas, en este caso, los nombres, lo cual puede ser útil para varias situaciones, como generar listas de clientes sin detalles adicionales.

`003-solo quiero ver los nombres.sql`

```sql
SELECT nombre FROM clientes;
```

### selecciono colu,nas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL selecciona y muestra los nombres de todos los registros en la tabla llamada "clientes". La instrucción `SELECT nombre` especifica que solo queremos ver la columna "nombre" de cada registro, mientras que `FROM clientes` indica a la base de datos que debe buscar estos datos dentro de la tabla "clientes". Es importante porque nos permite obtener información específica sin tener que mostrar toda la información del cliente, lo cual puede ser útil para mantener la privacidad o solo visualizar los datos relevantes en ese momento.

`004-selecciono colu,nas.sql`

```sql
SELECT nombre FROM clientes;
```

### selecciono columnas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL selecciona dos columnas específicas, `nombre` y `apellidos`, desde la tabla llamada `clientes`. La instrucción `SELECT nombre, apellidos FROM clientes;` indica a la base de datos que debe extraer los valores de las columnas `nombre` y `apellidos` para todos los registros presentes en la tabla `clientes`. Esto resulta en un conjunto de resultados que contiene solo los nombres y apellidos de los clientes registrados.

En comparación con el código anterior, que solo seleccionaba la columna `nombre`, este nuevo fragmento incluye también la columna `apellidos`. Esta adición permite obtener más información sobre cada cliente en una sola consulta, lo cual es útil si se necesita trabajar simultáneamente tanto con nombres como con apellidos.

`004-selecciono columnas.sql`

```sql
SELECT 
nombre,
apellidos 
FROM 
clientes;
```

### alias
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL selecciona dos columnas, `nombre` y `apellidos`, de la tabla llamada `clientes`. Utiliza el comando `AS` para dar un alias a cada columna en el resultado. Esto significa que en lugar de ver las columnas simplemente como "nombre" y "apellidos", los resultados mostrarán estas columnas con etiquetas más descriptivas: "Nombres de los clientes" y "Apellidos de los clientes". Esta práctica es útil para mejorar la legibilidad de los resultados de consultas, especialmente cuando se trabaja con grandes conjuntos de datos o tablas complejas.

`005-alias.sql`

```sql
SELECT 
nombre AS 'Nombres de los clientes',
apellidos AS 'Apellidos de los clientes' 
FROM 
clientes;
```

### volvemos a todo
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL es una consulta simple que selecciona todos los registros de la tabla llamada "clientes". La línea `SELECT *` indica que se desea recuperar todas las columnas disponibles en la tabla. Luego, `FROM clientes;` especifica el nombre de la tabla desde la cual se van a extraer estos datos.

Esta consulta es muy útil cuando necesitas ver toda la información contenida en la tabla "clientes" sin realizar ningún tipo de filtro o selección adicional. Es una excelente herramienta para revisar los datos generales y verificar que todo esté correctamente ingresado antes de pasar a consultas más complejas.

`006-volvemos a todo.sql`

```sql
SELECT 
* 
FROM 
clientes;
```

### ordenamos por columna
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL selecciona todos los registros de la tabla llamada "clientes" y ordena estos registros basándose en el campo "apellidos". Al usar el asterisco (*) en la cláusula SELECT, se indica que deben devolverse todas las columnas de la tabla "clientes". La cláusula ORDER BY apellidos asegura que los resultados estén organizados alfabéticamente por el valor del campo "apellidos" de cada registro. Esto es útil cuando necesitas ver o manipular los datos en orden alfabético, facilitando así su análisis y comprensión.

`007-ordenamos por columna.sql`

```sql
SELECT 
* 
FROM 
clientes
ORDER BY apellidos
;
```

### ascendiente
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL realiza una consulta en la base de datos que ordena los registros de la tabla "clientes" por el campo "apellidos" en orden ascendente. Esto significa que los clientes aparecerán listados alfabéticamente según sus apellidos, desde la letra A hasta la Z. Es importante porque facilita la búsqueda y lectura de información cuando se necesita una lista organizada de clientes basada en sus apellidos.

`008-ascendiente.sql`

```sql
SELECT 
* 
FROM 
clientes
ORDER BY apellidos ASC
;
```

### descendiente
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL selecciona todos los datos de la tabla llamada `clientes` y ordena estos registros en orden descendente según el campo `apellidos`. Es decir, muestra una lista completa de clientes pero organiza esta lista por el apellido de cada cliente de forma que las personas con apellidos que empiezan por letras más tarde del alfabeto aparecen primero.

La función `ORDER BY` es muy útil cuando necesitas presentar información en un orden específico para facilitar su lectura o análisis. En este caso, al usar `DESC`, el ordenamiento se hace de 'Z' a 'A', lo que puede ser conveniente si quieres ver los nombres de familia que empiezan con letras más recientes del alfabeto primero.

Es importante entender esto porque en muchas situaciones, especialmente en bases de datos de clientes o empleados, es común necesitar organizar información para facilitar su búsqueda y visualización.

`009-descendiente.sql`

```sql
SELECT 
* 
FROM 
clientes
ORDER BY apellidos DESC
;
```

### varios criterios
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL realiza una consulta en la base de datos para seleccionar todos los registros de la tabla llamada `clientes`. La consulta ordena estos registros primero por el campo `apellidos` en orden alfabético ascendente (de A a Z), y luego dentro de cada grupo de apellidos iguales, ordena por el campo `nombre` también en orden ascendente. Esto significa que obtendrás una lista completa de clientes organizada primero por sus apellidos y luego por sus nombres dentro del mismo apellido.

Esta consulta es importante porque facilita la búsqueda y visualización de datos en grandes tablas, permitiendo a los usuarios encontrar fácilmente información específica según su criterio de ordenación. En este caso, sería útil para tener una lista de clientes bien organizada que sea fácil de leer y navegar.

`010-varios criterios.sql`

```sql
SELECT 
* 
FROM 
clientes
ORDER BY apellidos ASC, nombre ASC
;
```

### clausula where
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL selecciona todos los registros de la tabla `clientes` donde el campo `apellidos` tenga exactamente el valor "Castro Vargas". La cláusula `WHERE` sirve para filtrar los resultados y asegurarse de que solo se devuelvan las filas en las que el apellido del cliente es "Castro Vargas". Esto es útil cuando necesitas obtener información específica sobre un conjunto limitado de registros, en este caso, todos los clientes con ese apellido. Sin la cláusula `WHERE`, se devolverían todas las filas de la tabla `clientes`.

`011-clausula where.sql`

```sql
SELECT 
* 
FROM 
clientes
WHERE apellidos = "Castro Vargas"
;
```

### comodin de inicio
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL selecciona todos los registros de la tabla `clientes` cuyo campo `apellidos` comienza con las letras "Castro". La cláusula `LIKE` se utiliza para realizar búsquedas de texto que coincidan con un patrón específico, en este caso usando el comodín `%`, que representa cualquier secuencia de caracteres. Por lo tanto, esta consulta devuelve una lista completa de todos los clientes cuyos apellidos empiezan por "Castro". Esto es útil cuando se necesita filtrar y ver datos específicos de un conjunto grande basándose en criterios particulares como el comienzo de ciertos campos de texto.

`012-comodin de inicio.sql`

```sql
SELECT 
* 
FROM 
clientes
WHERE apellidos LIKE "Castro%"
;
```

### dos comodines
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está realizando una consulta en la base de datos para buscar registros específicos en la tabla `clientes`. La instrucción `SELECT *` indica que se deben devolver todas las columnas de los registros que cumplan con el criterio establecido. El criterio se define en la cláusula `WHERE`, donde se usa el operador `LIKE` junto con el comodín `%ez%`.

El comodín `%` representa cualquier secuencia de caracteres, por lo tanto, `"%"ez"%"` busca todos los registros cuyos apellidos contienen las letras "ez" en alguna parte del apellido. Esto significa que se encontrarán registros donde "ez" pueda estar al principio, en medio o al final del apellido.

Este tipo de consulta es útil cuando necesitas buscar información basada en criterios generales pero no específicos, permitiendo una búsqueda más flexible y amplia dentro de los datos de la base de datos.

`013-dos comodines.sql`

```sql
SELECT 
* 
FROM 
clientes
WHERE apellidos LIKE "%ez%"
;
```

### Actividades propuestas

### Actividad 1: Consulta Básica de Datos
**Descripción:** Ejecuta la consulta proporcionada en el archivo `002-seleccion.sql` para ver todos los registros del cliente. Aprende a recuperar datos completos desde una tabla utilizando SQL.

### Actividad 2: Proyección de Columnas Específicas
**Descripción:** Utiliza la consulta del archivo `003-solo quiero ver los nombres.sql` para mostrar solo el nombre de cada cliente. Practica la selección de columnas específicas en lugar de toda la fila.

### Actividad 3: Selección de Múltiples Columnas
**Descripción:** Implementa la consulta vista en el archivo `004-selecciono columnas.sql` para seleccionar tanto nombres como apellidos. Aprende a especificar múltiples columnas al consultar datos.

### Actividad 4: Uso de Alias para Columnas
**Descripción:** Modifica la consulta del archivo `005-alias.sql`. Utiliza el comando AS para renombrar las columnas que se seleccionan en la tabla clientes. Aprende a mejorar la legibilidad de consultas SQL usando alias.

### Actividad 5: Ordenación Ascendente
**Descripción:** Ejecuta y comprende cómo funciona la consulta proporcionada en `008-ascendiente.sql`. Aprende a ordenar registros en una tabla cliente por apellidos en orden ascendente.

### Actividad 6: Ordenación Descendente
**Descripción:** Utiliza el archivo `009-descendiente.sql` para aprender cómo se ordenan los datos de manera descendente. Aplica la cláusula ORDER BY con DESC para ver registros de clientes por apellidos en orden inverso.

### Actividad 7: Ordenación Múltiples Criterios
**Descripción:** Ejecuta la consulta del archivo `010-varios criterios.sql` para aprender a ordenar los datos primero por un campo y luego dentro de este, por otro. Utiliza ORDER BY con múltiples campos.

### Actividad 8: Filtro con Cláusula WHERE
**Descripción:** Aprende a filtrar registros específicos usando la consulta del archivo `011-clausula where.sql`. Solo muestra los clientes cuyos apellidos sean "Castro Vargas".

### Actividad 9: Uso de Comodines en Consultas
**Descripción:** Practica el uso del operador LIKE para seleccionar registros que coinciden con un patrón. Ejecuta la consulta proporcionada en `012-comodin de inicio.sql` y luego modifica la condición WHERE para incluir otros comodines.

### Actividad 10: Consultas Complejas
**Descripción:** Combina conocimientos anteriores para crear una consulta que muestra clientes cuyos apellidos contengan el patron "ez". Utiliza la consulta en `013-dos comodines.sql` como punto de partida.


<a id="operadores-operadores-de-comparacion-operadores-logicos"></a>
## Operadores. Operadores de comparación. Operadores lógicos

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/003-Realizaci%C3%B3n%20de%20consultas/002-Operadores.%20Operadores%20de%20comparaci%C3%B3n.%20Operadores%20l%C3%B3gicos)

### Introducción a los ejercicios

En esta carpeta de ejercicios se trabajan diferentes tipos de operaciones y consultas en SQL que involucran tanto operadores aritméticos como de comparación. Los estudiantes aprenderán a realizar cálculos básicos, calcular el IVA y sumar totales para productos almacenados en una base de datos. Además, practicarán la creación de alias de columnas para mejorar la legibilidad de los resultados. También se introducen conceptos más avanzados como las condiciones IF que permiten aplicar reglas personalizadas en función de ciertos criterios, como determinar si el transporte es necesario según el precio del producto y calcular el costo total incluyendo el transporte cuando sea aplicable.

Estos ejercicios ayudan a los estudiantes a familiarizarse con la manipulación de datos mediante consultas SQL, desarrollando habilidades cruciales para realizar cálculos complejos y condiciones lógicas en sus bases de datos.

### aritmeticos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL realiza operaciones aritméticas básicas y devuelve los resultados. El código calcula la suma, resta, multiplicación y división entre los números 4 y 3 en cuatro expresiones diferentes. Estas operaciones se realizan sin necesidad de una tabla real ya que no hace uso de ninguna columna del `clientes`, simplemente utiliza valores numéricos constantes. Lo importante aquí es entender cómo funcionan las operaciones matemáticas básicas dentro de SQL, aunque usualmente estas operaciones son aplicadas sobre datos almacenados en tablas. En este caso particular, el resultado se obtendrá sin necesidad de recurrir a los registros existentes en la tabla `clientes`.

`001-aritmeticos.sql`

```sql
SELECT 
(4+3),
 (4-3),
 (4*3),
 (4/3)
FROM 
clientes
;
```

### datos de ejemplo
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para insertar múltiples registros en una tabla llamada `productos`. Cada registro contiene información sobre un producto específico, como su nombre, descripción, precio y peso. El comando `INSERT INTO` añade estos datos a la base de datos.

El código especifica primero el nombre de la tabla (`productos`) y los nombres de las columnas donde se van a almacenar los datos: `nombre`, `descripcion`, `precio` y `peso`. Luego, proporciona una lista de valores para cada producto entre paréntesis y separados por comas. Cada conjunto de valores está encerrado en paréntesis y cada uno representa un nuevo registro que se insertará en la tabla.

Esta operación es importante porque permite llenar la base de datos con información real sobre productos, lo que luego puede utilizarse para realizar consultas o análisis relacionados con el inventario o las ventas.

`002-datos de ejemplo.sql`

```sql
INSERT INTO productos (nombre, descripcion, precio, peso) VALUES
('Portátil Lenovo ThinkPad E14', 'Portátil empresarial de 14 pulgadas con procesador Intel i5 y 16GB RAM.', 899.99, 1.50),
('Smartphone Samsung Galaxy S24', 'Teléfono inteligente con pantalla AMOLED de 6.5 pulgadas y 128GB de memoria.', 1099.00, 0.18),
('Auriculares Sony WH-1000XM5', 'Auriculares inalámbricos con cancelación activa de ruido.', 349.99, 0.25),
('Impresora HP LaserJet Pro M404', 'Impresora láser monocromo rápida y compacta.', 229.50, 7.60),
('Monitor LG UltraWide 34"', 'Monitor ultrapanorámico de 34 pulgadas con resolución QHD.', 599.90, 6.80),
('Teclado Logitech MX Keys', 'Teclado inalámbrico retroiluminado con teclas silenciosas.', 119.00, 0.80),
('Ratón Logitech MX Master 3S', 'Ratón inalámbrico ergonómico con precisión avanzada.', 99.99, 0.14),
('Disco SSD Samsung 1TB', 'Unidad de estado sólido NVMe PCIe Gen4 de 1TB.', 139.90, 0.05),
('Servidor Dell PowerEdge T40', 'Servidor torre para pymes con Intel Xeon.', 1150.00, 11.20),
('Tablet Apple iPad 10.2"', 'Tablet de 10.2 pulgadas con 64GB de almacenamiento.', 429.00, 0.49),
('Cámara Canon EOS 250D', 'Cámara réflex digital con lente 18-55mm.', 639.00, 0.90),
('Proyector Epson EB-S41', 'Proyector SVGA de 3300 lúmenes para presentaciones.', 299.00, 2.50),
('Silla ergonómica Hbada', 'Silla de oficina ergonómica con soporte lumbar.', 199.99, 13.00),
('Disco Duro Externo WD 2TB', 'Disco duro externo portátil con conexión USB 3.0.', 79.90, 0.23),
('Router ASUS RT-AX88U', 'Router WiFi 6 de alto rendimiento con 8 puertos LAN.', 289.00, 1.00),
('Smartwatch Garmin Forerunner 255', 'Reloj inteligente multideporte con GPS integrado.', 349.90, 0.12),
('Altavoz JBL Charge 5', 'Altavoz Bluetooth portátil resistente al agua.', 179.00, 0.95),
('Microondas Samsung MG23', 'Microondas con grill de 23 litros.', 145.00, 13.00),
('Cafetera Nespresso Essenza Mini', 'Cafetera de cápsulas compacta y rápida.', 89.00, 2.30),
('Dispositivo NAS Synology DS220+', 'Servidor NAS de 2 bahías para uso doméstico o empresarial.', 329.00, 1.30);
```

### calculo del iva
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL selecciona tres columnas de la tabla llamada `productos`. La primera columna es el nombre del producto, que se muestra tal como está en la base de datos. La segunda columna es el precio del producto, también directamente desde la tabla.

La tercera columna calcula el IVA (Impuesto sobre Valor Añadido) aplicando una tasa del 21% al precio del producto. Esto se hace multiplicando el precio por `0.21`. Este cálculo te permite ver cuánto IVA se aplica a cada producto en la tabla.

Este tipo de consulta es útil para entender las implicaciones fiscales de los precios de venta en una base de datos de productos, especialmente si estás trabajando en un entorno comercial o financiero donde el cálculo del IVA es importante.

`003-calculo del iva.sql`

```sql
SELECT 
nombre,
precio,
precio*0.21
FROM productos;
```

### alias de columna
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para seleccionar y modificar cómo aparecen los datos en una tabla llamada `productos`. La consulta toma tres columnas de la tabla: `nombre`, `precio` y calcula el IVA (Impuesto al Valor Agregado) que es un 21% del precio. 

Lo interesante aquí es el uso del alias, que permite renombrar temporalmente las columnas en el resultado para que sean más descriptivas. En este caso, `nombre` se muestra como "Nombre del producto", `precio` como "Base Imponible" y `precio*0.21` (el cálculo del IVA) como "IVA 21%". Esto facilita la comprensión de los datos cuando alguien ve el resultado de esta consulta, haciéndolo más claro y directo.

Este tipo de consulta es importante porque ayuda a presentar información compleja de una manera más legible y accesible, especialmente en contextos donde se requiere entender rápidamente qué significan las columnas del resultado.

`004-alias de columna.sql`

```sql
SELECT 
nombre AS 'Nombre del producto',
precio AS 'Base Imponible',
precio*0.21 AS 'IVA 21%'
FROM productos;
```

### sumo el total
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para seleccionar y mostrar información detallada sobre los productos en una base de datos, específicamente enfocándose en el cálculo del total incluyendo impuestos. La consulta recupera cuatro columnas: el nombre del producto, la base imponible (precio sin IVA), el IVA calculado como un 21% del precio y el total que es la suma del precio original más el IVA.

Cada columna tiene un alias asignado para mejorar la legibilidad del resultado de la consulta. Por ejemplo, 'nombre' se muestra como 'Nombre del producto', lo cual facilita entender rápidamente qué información representa cada campo en la salida del SQL.

Esta consulta es importante porque demuestra cómo realizar cálculos y presentarlos de manera clara en una tabla resultante, ayudando a los usuarios finales (como contables o vendedores) a comprender fácilmente el costo total incluyendo impuestos de cualquier producto que se consulte.

`005-sumo el total.sql`

```sql
SELECT 
nombre AS 'Nombre del producto',
precio AS 'Base Imponible',
precio*0.21 AS 'IVA 21%',
precio + precio*0.21 AS 'Total Precio'
FROM productos;
```

### operadores de comparacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL es una consulta sencilla que evalúa una expresión de comparación. La expresión `4 > 3` se compara para determinar si el número 4 es mayor que el número 3, lo cual resulta en un valor booleano verdadero (TRUE). Sin embargo, esta consulta no tiene propósito práctico en la tabla "productos" porque no utiliza ninguna columna de esa tabla. La consulta simplemente devolverá una sola fila con el valor TRUE ya que `4 > 3` siempre será cierto.

Es importante entender este tipo de operadores de comparación (como mayor que, menor que) cuando se trabaja con SQL y bases de datos, ya que estos son fundamentales para filtrar y seleccionar datos basándose en condiciones específicas. En situaciones reales, usarías estas expresiones junto con las columnas de tus tablas para obtener resultados útiles.

`006-operadores de comparacion.sql`

```sql
SELECT 
4 > 3
FROM productos;
```

### comparacion falsa
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está realizando una operación de comparación entre dos números. Específicamente, la consulta está verificando si el número 4 es menor que el número 3.

En este caso, la expresión `4 < 3` siempre devolverá un valor falso (FALSE en SQL), porque 4 no puede ser menor que 3. La consulta intenta seleccionar el resultado de esta comparación desde una tabla llamada "productos", pero realmente no está utilizando ninguna columna o fila de esa tabla en la operación.

Este tipo de código es útil para entender cómo funcionan las operaciones de comparación en SQL, aunque en prácticas reales rara vez verás consultas que realicen una simple comparación entre constantes sin relacionarla con datos de una tabla.

`007-comparacion falsa.sql`

```sql
SELECT 
4 < 3
FROM productos;
```

### condicion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL selecciona tres columnas de la tabla `productos`: el nombre del producto, su precio y un campo adicional que indica si el precio es menor a 500 unidades. La consulta revisa cada fila en la tabla `productos` para determinar si el valor de la columna `precio` es inferior a 500, devolviendo un resultado booleano (verdadero o falso) para esa condición junto con los nombres y precios de los productos.

Esta consulta es útil porque permite identificar rápidamente qué productos tienen un precio por debajo del umbral establecido, facilitando la toma de decisiones en cuanto a inventario,定价不宜出现在解释代码的功能和工作原理的回答中，以下是修改后的回答：

---

Este código SQL selecciona tres columnas de la tabla `productos`: el nombre del producto (`nombre`) y su precio (`precio`). Además, agrega una columna adicional que evalúa si el precio es menor a 500 unidades. Esto se hace mediante la expresión booleana `precio < 500`. La consulta revisa cada fila en la tabla `productos` para determinar si el valor de la columna `precio` cumple con esta condición, devolviendo un resultado verdadero o falso.

Esta consulta es útil porque permite identificar rápidamente qué productos tienen un precio por debajo del umbral establecido (en este caso, 500 unidades), lo cual puede ser importante para el análisis de inventario y la gestión de precios.

`008-condicion.sql`

```sql
SELECT 
nombre,
precio,
precio < 500 
FROM productos;
```

### alias de columna
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL selecciona datos de la tabla llamada "productos". Lo que hace es mostrar el nombre y el precio de cada producto. Luego, utiliza una función llamada IF para determinar si un producto necesita incluirse en la carga para su transporte basándose en su precio. Si el precio del producto es menor a 500 unidades (que pueden ser euros, dólares u otra moneda), se añade una columna que indica 'Sí' para 'carga transporte'. También calcula un costo adicional para el transporte: si el precio es menor a 500, agrega 200 unidades al costo del producto como gasto de transporte; en caso contrario, no agrega nada.

Esta consulta es importante porque ayuda a entender cómo se pueden tomar decisiones dentro de una consulta SQL basándose en condiciones específicas (en este caso, si el precio del producto es menor o mayor a un umbral determinado). Los alias 'carga transporte' y 'precio transporte' hacen que los resultados sean más claros y descriptivos.

`009-alias de columna.sql`

```sql
SELECT 
  nombre,
  precio,
  IF(precio < 500, 'Sí', 'No') AS `carga transporte`,
  IF(precio < 500, 200, 0) AS `precio transporte`
FROM productos;
```

### total con transporte
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para consultar información sobre los productos en una base de datos y calcular el total del pedido junto con la carga del transporte si es necesario. La consulta selecciona tres columnas principales: el nombre y el precio del producto, así como un campo calculado que indica si el costo del transporte se aplica o no al pedido.

El código utiliza la función `IF` para determinar si el costo del transporte de 200 unidades monetarias debe aplicarse a cada producto. Si el precio del producto es menor a 500 unidades, entonces la carga sí se incluirá en el total del pedido y se mostrarán los detalles respectivos; de lo contrario, no se aplica y se indica con "No".

Finalmente, calcula un campo `Total pedido` que suma el precio original del producto más el costo del transporte si esta condición es verdadera (precio < 500), o simplemente muestra el precio original si la condición no se cumple. Este tipo de consulta es útil para generar informes detallados sobre pedidos, especialmente cuando hay reglas específicas sobre cuándo aplicar costos adicionales como el transporte.

`010-total con transporte.sql`

```sql
SELECT 
  nombre,
  precio,
  IF(precio < 500, 'Sí', 'No') AS `carga transporte`,
  IF(precio < 500, 200, 0) AS `precio transporte`,
  IF(precio < 500, (200+precio), precio) AS `Total pedido`
FROM productos;
```

### Actividades propuestas

### Actividades Propuestas

1. **Operaciones Aritméticas Básicas**
   - **Descripción:** Utiliza operadores aritméticos para realizar cálculos básicos sobre los precios de los productos en la tabla `productos`. Se pretende que comprendan cómo se aplican las operaciones matemáticas en consultas SQL.

2. **Cálculo del IVA**
   - **Descripción:** Calcula el IVA (21%) para cada producto en la base de datos y muestra tanto el precio sin IVA como el valor del impuesto incluido. El objetivo es aprender a manipular números y realizar cálculos financieros.

3. **Creación de Alias de Columnas**
   - **Descripción:** Escribe consultas que renombren las columnas de salida usando alias para mejorar la legibilidad de los resultados. Se espera que comprendan cómo facilitar la interpretación de datos complejos.

4. **Suma del Total Precio**
   - **Descripción:** Modifica el código proporcionado para calcular no solo el IVA sino también el total a pagar incluyendo transporte si es necesario. El objetivo es combinar varios operadores en una sola consulta.

5. **Operadores de Comparación Simples**
   - **Descripción:** Realiza consultas que usen operadores como `>`, `<`, `=`, etc., para filtrar productos según ciertas condiciones, por ejemplo, todos los productos con precio superior a 1000€. Se pretende practicar la selección condicional de datos.

6. **Condiciones Combinadas**
   - **Descripción:** Escribe consultas que usen operadores lógicos como `AND` y `OR` para combinar múltiples condiciones en una sola consulta. Por ejemplo, listar productos con precio superior a 500€ pero pesos inferiores a 2kg.

7. **Condición de Entrega**
   - **Descripción:** Implementa una condición que determine si un producto requiere carga especial basándose en su peso y dimensiones. Se espera aprender sobre cómo aplicar múltiples condiciones lógicas dentro de consultas SQL para evaluar diferentes criterios.

8. **Costo Total Incluyendo Transporte**
   - **Descripción:** Crea una consulta que muestre el costo total del pedido incluyendo el precio del producto y los costos de transporte si es necesario. El objetivo es combinar varias operaciones condicionales para resolver problemas prácticos.

9. **Comparación Detallada**
   - **Descripción:** Realiza consultas con comparadores complejos que usan condiciones como `BETWEEN` y `IN`. Por ejemplo, listar todos los productos cuyo precio se encuentre entre 300€ y 700€ o aquellos cuyo nombre comience por "Auriculares".

10. **Consultas Dinámicas**
    - **Descripción:** Diseña consultas que sean capaces de filtrar datos basándose en criterios dinámicos como el precio mínimo establecido por el usuario a través de una variable de entrada en SQL. Se pretende introducir la noción de personalización y flexibilidad en las consultas.

Estas actividades están diseñadas para ayudar al estudiante a familiarizarse con operaciones aritméticas, comparativas y lógicas en SQL, así como a mejorar sus habilidades en la creación y manipulación de alias de columnas y condiciones condicionales.


<a id="consultas-de-resumen"></a>
## Consultas de resumen

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/003-Realizaci%C3%B3n%20de%20consultas/003-Consultas%20de%20resumen)

### Introducción a los ejercicios

En esta carpeta, trabajaremos con consultas de resumen en SQL utilizando una base de datos que contiene información sobre pedidos. Los ejercicios te guiarán a través del cálculo de sumatorias totales, promedios y conteos relacionados con los pedidos para analizar el comportamiento de ventas y gastos en una tienda virtual. Aprenderás a utilizar funciones como SUM(), AVG() y MAX() para obtener información resumida de la tabla 'vista_pedidos'. Además, practicarás cómo contar el número total de registros que cumplen ciertas condiciones utilizando COUNT(). Estos ejercicios son fundamentales para desarrollar habilidades en análisis de datos básicos usando consultas SQL.

### resumen de suma
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL es una consulta que selecciona todos los datos de la tabla o vista llamada `vista_pedidos`. La función `SELECT *` indica que se deben recuperar todas las columnas y filas disponibles en esa vista. Esto es útil cuando quieres ver toda la información de la vista sin especificar columnas individuales, lo cual puede ser conveniente durante el proceso de desarrollo o depuración para entender cómo están estructurados los datos.

La importancia de este tipo de consulta radica en su simplicidad y utilidad para obtener una rápida visión general del contenido de `vista_pedidos`, sin necesidad de conocer exactamente qué columnas contiene la vista. Sin embargo, es importante tener en cuenta que seleccionar todos los campos puede no ser el mejor enfoque para consultas de producción debido a posibles rendimiento y consideraciones de privacidad.

`001-resumen de suma.sql`

```sql
SELECT * FROM vista_pedidos;
```

### resumen de total de pedidos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL es una consulta que calcula el total acumulado de todos los pedidos en una base de datos. La función `SUM()` se utiliza para sumar la columna llamada "Total" dentro de la tabla o vista llamada "vista_pedidos". Esta consulta te da un solo número que representa la suma de todos los valores "Total" registrados, lo cual es útil para obtener un resumen financiero sobre el ingreso total generado por los pedidos en tu base de datos.

`002-resumen de total de pedidos.sql`

```sql
SELECT 
SUM(Total)
FROM vista_pedidos;
```

### promedio de lo que se gasta la gente en mi tienda
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL es una consulta que calcula el promedio del campo `Total` en la tabla o vista llamada `vista_pedidos`. La función `AVG()` se utiliza para calcular el valor medio de los totales registrados en todos los pedidos. En otras palabras, esta consulta te dará una idea de cuánto dinero en promedio gastan los clientes en tu tienda por pedido.

Es importante destacar que este tipo de consulta es útil para obtener estadísticas resumidas y comprender el comportamiento general del gasto de tus clientes, lo cual puede ser valioso para análisis comerciales y toma de decisiones.

`003-promedio de lo que se gasta la gente en mi tienda.sql`

```sql
SELECT 
AVG(Total)
FROM vista_pedidos;
```

### pedido mas barato
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL te ayuda a calcular el gasto promedio en tu tienda. La función `AVG()` se utiliza para encontrar el promedio (media aritmética) de los valores en la columna "Total" de una tabla llamada "vista_pedidos". En este caso, estás sumando todos los totales de los pedidos registrados y luego dividiendo ese total entre el número de pedidos para obtener un valor medio que representa cuánto gasta típicamente una persona en tu tienda. Esto es útil para entender la tendencia general del consumo y puede ayudarte a tomar decisiones sobre marketing, precios o inventario basadas en esta información estadística.

`004-pedido mas barato.sql`

```sql
SELECT 
AVG(Total)
FROM vista_pedidos;
```

### pedido mas caro
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está diseñado para encontrar el pedido más caro en una base de datos. La consulta selecciona la máxima cantidad (`MAX`) de la columna `Total` que probablemente almacena el coste total de cada pedido, desde una tabla o vista llamada `vista_pedidos`. Al utilizar la función `MAX()`, SQL devuelve solo un valor: el mayor número presente en la columna `Total`. Esto es útil cuando necesitas saber cuánto ha costado el pedido más caro realizado.

Es importante destacar que esta consulta asume que ya tienes una vista llamada `vista_pedidos` creada previamente, donde se agrupa o seleccionan los datos relevantes de las tablas subyacentes. La función `MAX()` es una forma rápida y efectiva de obtener información resumida sobre tus datos sin necesidad de iterar a través de todos ellos manualmente.

`005-pedido mas caro.sql`

```sql
SELECT 
MAX(Total)
FROM vista_pedidos;
```

### cuantos pedidos se han realizado
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL es una consulta que cuenta cuántos registros o filas existen en la columna "Total" dentro de la tabla llamada "vista_pedidos". La función `COUNT()` se utiliza para contar el número total de pedidos registrados, asumiendo que cada fila en esta vista representa un pedido individual. Es importante porque proporciona información sobre la cantidad total de pedidos realizados, lo cual es valioso para el análisis y el seguimiento del rendimiento de las ventas o el servicio al cliente.

`006-cuantos pedidos se han realizado.sql`

```sql
SELECT 
COUNT(Total)
FROM vista_pedidos;
```

### Actividades propuestas

### Actividad 1: Sumar Total de Pedidos
**Descripción:** Realiza una consulta SQL que sume el total de todos los pedidos registrados en la tabla `vista_pedidos`. Este ejercicio te ayudará a comprender cómo calcular totales acumulativos.

### Actividad 2: Calcular Promedio de Gastos por Pedido
**Descripción:** Escribe una consulta para calcular el promedio del total gastado en cada pedido. Aprenderás a usar la función `AVG()` y a entender los gastos medios de tus clientes.

### Actividad 3: Identificar el Pedido Mínimo y Máximo
**Descripción:** Crea dos consultas distintas, una para encontrar el pedido más barato (`MIN()`) y otra para identificar el pedido más caro (`MAX()`). Estos ejercicios te enseñarán a utilizar funciones de resumen como `MIN()` y `MAX()`.

### Actividad 4: Contar Número Total de Pedidos
**Descripción:** Utiliza una consulta SQL que cuente la cantidad total de pedidos en la tabla `vista_pedidos`. Este ejercicio te permitirá practicar el uso del agregador `COUNT()` para obtener estadísticas sobre los datos.

### Actividad 5: Resumen Completo de Pedidos
**Descripción:** Escribe una consulta que combine varias funciones de resumen (suma, promedio, mínimo y máximo) en un único resultado. Esto te ayudará a comprender cómo integrar múltiples operaciones de agregación en una sola consulta.

### Actividad 6: Análisis de Volumen de Pedidos
**Descripción:** Realiza consultas que permitan calcular tanto el volumen total como la cantidad promedio de pedidos realizados. Aprenderás a combinar diferentes tipos de operaciones SQL para obtener un análisis más detallado.

### Actividad 7: Comparación de Totales entre Días
**Descripción:** Diseña una consulta que compare los totales de ventas entre dos días específicos. Este ejercicio te permitirá trabajar con subconsultas y funciones de resumen en diferentes contextos temporales.

### Actividad 8: Resumir Información por Meses
**Descripción:** Crea consultas SQL que sumen y promedien el total de pedidos por cada mes del año. Aprenderás a filtrar datos basados en fechas y utilizar funciones de agrupamiento avanzado.

### Actividad 9: Crear Reporte Resumido Diario
**Descripción:** Escribe una consulta que genere un reporte diario resumido, incluyendo el total vendido, promedio por pedido, cantidad de pedidos y detalles adicionales. Este ejercicio te permitirá practicar la combinación de varias operaciones SQL en un único informe.

### Actividad 10: Optimización de Consultas Resumen
**Descripción:** Identifica las consultas más eficientes para calcular los resúmenes (suma, promedio, mínimo y máximo) de tus pedidos. Este ejercicio te ayudará a entender cómo optimizar las consultas SQL para mejorar el rendimiento del sistema.


<a id="agrupamiento-de-registros"></a>
## Agrupamiento de registros

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/003-Realizaci%C3%B3n%20de%20consultas/004-Agrupamiento%20de%20registros)

### Introducción a los ejercicios

En esta carpeta, se trabajan ejercicios relacionados con la realización de consultas SQL avanzadas en un contexto de base de datos para estudiantes de Formación Profesional. El objetivo principal es familiarizarse con el agrupamiento de registros utilizando la cláusula `GROUP BY` y cómo combinarla con funciones de agregación como `COUNT()`. Los ejercicios van desde seleccionar todos los registros de una tabla hasta realizar consultas más complejas que involucran agregar nuevos campos a una tabla existente y luego agrupar datos según estos cambios. Este conjunto de ejercicios ayuda a desarrollar competencias en manipulación de bases de datos, consulta avanzada y resolución de problemas relacionados con la agregación de información.

### seleccion de productos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL es una consulta simple que selecciona todos los datos de la tabla llamada "clientes". La sentencia `SELECT *` indica que se deben recuperar todas las columnas y filas disponibles en la tabla especificada. Esto es útil cuando deseas obtener un vistazo completo a toda la información almacenada en la tabla "clientes", sin necesidad de filtrar o seleccionar datos específicos.

Es importante destacar que usar `SELECT *` en un entorno de producción o con tablas grandes puede no ser eficiente, ya que devuelve más datos de los necesarios y consume recursos del sistema. Sin embargo, para fines educativos y cuando se trabaja con pequeñas cantidades de datos, esta consulta es una excelente herramienta para familiarizarse con la estructura y el contenido de la tabla "clientes".

`001-seleccion de productos.sql`

```sql
SELECT * 
FROM clientes;
```

### altero los clientes
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para modificar la estructura de una tabla llamada `clientes`. En específico, el código añade una nueva columna llamada `localidad` a esta tabla. La nueva columna es un campo de texto que puede contener hasta 255 caracteres y no permite valores nulos (es decir, cada registro en la tabla debe tener un valor para esta columna). La columna se inserta inmediatamente después de otra columna existente llamada `email`.

Este tipo de cambio en una base de datos es común cuando los desarrolladores descubren que necesitan almacenar más información sobre los clientes. Es importante realizar estas modificaciones con cuidado ya que pueden afectar el funcionamiento del sistema si no se gestionan correctamente. Después de agregar la nueva columna, generalmente se deben actualizar los registros existentes para incluir datos en esta nueva columna, lo cual es algo que este código indica debe hacerse, aunque no especifica cómo en este caso.

`002-altero los clientes.sql`

```sql
ALTER TABLE `clientes` ADD `localidad` VARCHAR(255) NOT NULL AFTER `email`;
-- y relleno con datos de localidad en update
```

### seleccion con agrupacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL realiza una consulta que cuenta el número total de registros en la tabla llamada `clientes`. La función `COUNT()` se utiliza para contar cuántas filas hay en esa tabla, y al colocar `Identificador` dentro de los paréntesis de `COUNT()`, lo que hace es asegurarse de que solo cuente las filas donde el campo `Identificador` tenga un valor (es decir, no cuenta filas con este campo vacío). En resumen, esta consulta te dará un número que indica cuántos clientes hay registrados en total en la base de datos. Es importante porque nos ayuda a entender rápidamente la escala del conjunto de datos que estamos trabajando.

`003-seleccion con agrupacion.sql`

```sql
SELECT COUNT(Identificador)
FROM clientes;
```

### seleccion con agrupacion ahora si
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL selecciona la información de una base de datos llamada `clientes`. Lo que hace específicamente es contar cuántos registros (o filas) hay en la tabla `clientes` para cada distinta localidad. Aquí, `localidad` es un campo que contiene el nombre del lugar donde se encuentran los clientes registrados.

El comando `SELECT` indica qué datos quieres recuperar de tu base de datos, mientras que `COUNT(Identificador)` cuenta cuántas veces aparece cada valor único en la columna `Identificador`, que probablemente funciona como una identificación única para cada cliente. Sin embargo, debido a cómo está escrito el código, realmente estamos contando todas las filas (clientes) por localidad.

`FROM clientes` indica de qué tabla se van a extraer los datos; en este caso, es la tabla `clientes`.

Finalmente, `GROUP BY(localidad)` agrupa los resultados por cada valor único que aparece en el campo `localidad`. Esto significa que obtendrás una fila para cada localidad distinta con un conteo de cuántos clientes hay registrados en esa localidad.

Esta consulta es útil cuando necesitas resumir datos para obtener información general sobre la distribución geográfica de tus clientes, por ejemplo, saber cuántos clientes tienes en diferentes ciudades o países.

`004-seleccion con agrupacion ahora si.sql`

```sql
SELECT 
localidad,
COUNT(Identificador)
FROM clientes
GROUP BY(localidad)
;
```

### Actividades propuestas

1. **Conteo de Registros**
   - **Descripción**: Los estudiantes deben realizar una consulta SQL para contar el número total de registros en la tabla `clientes`. Este ejercicio ayuda a entender cómo utilizar funciones básicas de agregación como COUNT.

2. **Añadir Campo y Actualizar Datos**
   - **Descripción**: Se pide que los alumnos añadan un nuevo campo llamado `localidad` a la tabla `clientes` y luego actualicen este campo con datos específicos para cada registro. Este ejercicio refuerza el conocimiento sobre cómo manejar alteraciones en las tablas y operaciones de actualización.

3. **Consulta Básica**
   - **Descripción**: Los estudiantes deben seleccionar todos los campos de la tabla `clientes`. Esto les permite practicar consultas SELECT simples y entender la estructura básica de una consulta SQL.

4. **Agrupación por Localidad**
   - **Descripción**: Se requiere que agrupen registros en función del campo `localidad` y cuenten el número de clientes en cada localidad. Este ejercicio permite aprender sobre GROUP BY y cómo usarlo junto con funciones de agregación como COUNT.

5. **Consulta Detallada**
   - **Descripción**: Los alumnos deben realizar una consulta que incluya la selección específica de campos relevantes de `clientes`, no solo todos los campos, para entender mejor la precisión en las consultas SQL.

6. **Conteo con Condición**
   - **Descripción**: Se les pide contar el número de clientes que cumplen ciertas condiciones (por ejemplo, aquellos cuya localidad es específica). Este ejercicio ayuda a comprender cómo combinar GROUP BY y funciones de agregación con cláusulas WHERE.

7. **Añadir Localidad Existente**
   - **Descripción**: Los estudiantes deben añadir un campo `localidad` a la tabla si aún no existe, luego llenar este campo basándose en datos existentes o predeterminados. Esto refuerza el manejo de tablas y actualizaciones.

8. **Agrupación Mejorada**
   - **Descripción**: Se requiere que los alumnos realicen una consulta más compleja utilizando GROUP BY para agrupar registros no solo por `localidad`, sino también considerando otros campos relevantes, como la edad o tipo de cliente.
   
Estas actividades están diseñadas para proporcionar a los estudiantes una comprensión sólida y práctica de cómo manejar consultas SQL básicas hasta más avanzados conceptos que incluyen funciones de agregación y agrupamiento.


<a id="composiciones-internas"></a>
## Composiciones internas

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/003-Realizaci%C3%B3n%20de%20consultas/005-Composiciones%20internas)

### Introducción a los ejercicios

Esta carpeta contiene una serie de ejercicios que te guiarán en la realización de consultas avanzadas con SQL, centrando tu atención en la creación y manipulación de relaciones entre tablas para representar pedidos complejos. Los problemas iniciales te ayudan a familiarizarte con las selecciones básicas y los JOIN simples, antes de profundizar en la composición interna de consultas que incluyen varias tablas y cálculos. A lo largo de estos ejercicios, practicarás la creación de esquemas de base de datos más realistas, como la relación 1:N entre pedidos y sus líneas, así como la incorporación de claves foráneas para garantizar integridad referencial. También trabajarás en la proyección de información relevante desde múltiples tablas y realizar cálculos sobre los datos obtenidos para obtener totales y subtotales de pedidos. Estos ejercicios están diseñados para mejorar tus habilidades en el manejo avanzado de consultas SQL, preparándote para resolver problemas más complejos relacionados con la gestión de bases de datos en entornos empresariales.

### seleccion basica de pedidos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL selecciona todos los registros de la tabla llamada "pedidos". La instrucción `SELECT *` significa que se van a recuperar todas las columnas disponibles en esa tabla. Cuando ejecutas esta consulta, obtendrás una lista completa con toda la información almacenada actualmente en la tabla "pedidos", lo cual es útil para tener una visión general de los datos sin especificar qué campos necesitas particularmente.

Es importante entender que usar `SELECT *` puede no ser la mejor práctica si sólo necesitas ciertas columnas, ya que puede afectar el rendimiento, especialmente con tablas grandes. Sin embargo, en un contexto de aprendizaje o cuando simplemente se necesita una vista rápida de todos los datos disponibles, esta consulta es muy útil para comenzar a familiarizarse con la estructura y el contenido de las tablas.

`001-seleccion basica de pedidos.sql`

```sql
SELECT * FROM pedidos;
```

### primer join con clientes
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL realiza una consulta que combina dos tablas: "pedidos" y "clientes". La función principal es obtener la fecha del pedido junto con el nombre y los apellidos del cliente asociado a ese pedido. 

La instrucción `LEFT JOIN` asegura que todos los registros de la tabla "pedidos" se incluyan en el resultado, incluso si no hay un cliente asociado (es decir, si `id_cliente` es nulo). Esto significa que obtendrás toda la información disponible sobre cada pedido, incluida la del cliente si está presente.

La cláusula `ON pedidos.id_cliente = clientes.Identificador` establece la relación entre ambas tablas, vinculando el identificador de cliente en la tabla "pedidos" con el campo correspondiente en la tabla "clientes". Esto permite que SQL sepa cómo combinar los datos correctamente.

`002-primer join con clientes.sql`

```sql
SELECT 
pedidos.fecha,
clientes.nombre,
clientes.apellidos
FROM pedidos
LEFT JOIN clientes
ON pedidos.id_cliente = clientes.Identificador
;
```

### vista de pedidos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para crear una vista que combina información de varias tablas en una base de datos. La consulta selecciona detalles específicos sobre los pedidos realizados, incluyendo la fecha del pedido, el nombre y apellidos del cliente, el nombre del producto, su precio, un cálculo del IVA (16%) y el total que se debe pagar por el producto.

La consulta comienza con una selección de campos específicos desde las tablas `pedidos`, `clientes` e `productos`. Utiliza dos tipos de JOINs llamados LEFT JOIN para asegurarse de que todos los registros en la tabla `pedidos` sean incluidos, incluso si no hay correspondencia en las otras tablas. Esto es importante cuando puede haber pedidos sin información del cliente o del producto.

Los cálculos adicionales como el IVA y el total (precio + IVA) se realizan directamente en la consulta SQL para facilitar la comprensión de los costos totales asociados con cada pedido, lo que ayuda a cualquier persona que consulte esta vista a entender rápidamente cuánto cuesta un pedido incluyendo impuestos.

`003-vista de pedidos.sql`

```sql
SELECT 
pedidos.fecha,
clientes.nombre,
clientes.apellidos,
productos.nombre,
productos.precio,
productos.precio*0.16 as IVA,
productos.precio*1.16 as Total
FROM pedidos

LEFT JOIN clientes
ON pedidos.id_cliente = clientes.Identificador

LEFT JOIN productos
ON pedidos.id_producto = productos.Identificador
;
```

### Pedidos con lineas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL crea dos tablas en una base de datos llamada `empresarial`. La primera tabla se llama `pedidosconlineas`, que almacena información básica sobre los pedidos, como el identificador único del pedido, la fecha del pedido y el ID del cliente. Cada columna tiene un tipo de dato específico: `Identificador` es un número entero (INT) que se incrementa automáticamente para cada nuevo registro, lo que significa que no necesitas preocuparte por proporcionar este valor cuando insertes nuevos datos; simplemente, la base de datos te dará uno único.

La segunda tabla se llama `lineaspedido`, que registra los detalles del producto asociado a cada pedido. Al igual que con la primera tabla, esta también tiene un identificador único (INT AUTO_INCREMENT), un ID del producto (también INT) y una columna para las unidades pedidas (de nuevo INT). Estos datos son cruciales para entender qué productos fueron pedidos en qué cantidad.

Estas tablas están diseñadas para trabajar juntas mediante la creación de relaciones entre los registros. Por ejemplo, cada línea de pedido está asociada con un solo pedido y puede rastrearse a través del ID del pedido que se especificaría en una columna adicional (aunque no mostrada en el código proporcionado) en la tabla `lineaspedido` para vincularla con la tabla `pedidosconlineas`. Esto es fundamental en bases de datos relacionales, ya que permite una gestión eficiente y detallada de los pedidos y sus detalles.

`005-Pedidos con lineas.sql`

```sql
CREATE TABLE `empresarial`.`pedidosconlineas` (`Identificador` INT NOT NULL AUTO_INCREMENT , `fecha` DATE NOT NULL , `id_cliente` INT NOT NULL , PRIMARY KEY (`Identificador`)) ENGINE = InnoDB;

CREATE TABLE `empresarial`.`lineaspedido` (`Identificador` INT NOT NULL AUTO_INCREMENT , `producto_id` INT NOT NULL , `unidades` INT NOT NULL , PRIMARY KEY (`Identificador`)) ENGINE = InnoDB;
```

### claves foraneas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para manejar las relaciones entre diferentes tablas en una base de datos, específicamente centrado en las entidades "lineaspedido", "pedidosconlineas" y otras tablas relacionadas. El objetivo principal es establecer claves foráneas que aseguren la integridad referencial de los datos.

El código comienza agregando una restricción (llamada `lineaspedidoaproductos`) a la tabla `lineaspedido`, que conecta la columna `producto_id` con la columna `Identificador` en la tabla `productos`. Esto significa que cada línea de pedido está relacionada con un producto específico, asegurando que no se puedan agregar líneas de pedidos sin tener previamente el registro del producto correspondiente. La opción `ON DELETE RESTRICT ON UPDATE RESTRICT` indica que si intentas eliminar un producto o modificar su identificador, SQL evitará cualquier acción que rompa esta relación.

Luego, se añade una nueva columna llamada `pedidos_id` a la tabla `lineaspedido`, que establece una relación con los pedidos. Posteriormente, se define otra restricción (llamada `lineapedidoapedido`) para vincular la nueva columna `pedidos_id` en `lineaspedido` con la columna `Identificador` de la tabla `pedidos`. Sin embargo, el código luego elimina esta restricción y vuelve a crearla, pero esta vez relacionando `pedidos_id` con una tabla llamada `pedidosconlineas`, manteniendo las mismas condiciones restrictivas.

Finalmente, se establece otra clave foránea en la tabla `pedidosconlineas` para conectar la columna `id_cliente` con la columna `Identificador` de la tabla `clientes`. Esto asegura que cada pedido asociado a `pedidosconlineas` esté vinculado a un cliente válido y, al igual que antes, se mantienen las restricciones restrictivas.

En resumen, estos cambios fortalecen la integridad referencial entre las tablas de una base de datos gestionando adecuadamente las relaciones y asegurándose de que los registros eliminados o modificados no afecten negativamente a otras entidades relacionadas.

`006-claves foraneas.sql`

```sql
ALTER TABLE `lineaspedido` ADD CONSTRAINT `lineaspedidoaproductos` FOREIGN KEY (`producto_id`) REFERENCES `productos`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE `lineaspedido` ADD `pedidos_id` INT NOT NULL AFTER `unidades`;

ALTER TABLE `lineaspedido` ADD CONSTRAINT `lineapedidoapedido` FOREIGN KEY (`pedidos_id`) REFERENCES `pedidos`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE `lineaspedido` DROP FOREIGN KEY `lineapedidoapedido`; ALTER TABLE `lineaspedido` ADD CONSTRAINT `lineapedidoapedido` FOREIGN KEY (`pedidos_id`) REFERENCES `pedidosconlineas`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE `pedidosconlineas` ADD  CONSTRAINT `pedidosaclientes2` FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;
```

### creamos pedido
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está diseñado para simular la creación de un nuevo pedido en una base de datos y luego añadir las líneas del pedido correspondientes. En primer lugar, se inserta una nueva fila en la tabla `pedidosconlineas` con información básica sobre el pedido, como su fecha y el identificador del cliente que lo realizó. Aquí, `Identificador` es autoincremental, por lo que se pasa NULL para permitir que la base de datos asigne automáticamente un nuevo valor único.

Después de crear el pedido, el código inserta una línea específica en la tabla `lineaspedido`. Esta línea contiene detalles sobre los productos incluidos en el pedido, como el identificador del producto (`producto_id`), la cantidad de unidades pedidas (`unidades`) y el identificador del pedido recién creado (`pedidosconlineas.Identificador`). En este caso, el código asume que el último pedido insertado (con `Identificador` igual a 1) es al que se refiere esta línea.

Esta secuencia de comandos es fundamental en la gestión de pedidos porque permite seguir el flujo natural del proceso: primero registrar un nuevo pedido y luego especificar los detalles de los productos incluidos en ese pedido.

`007-creamos pedido.sql`

```sql
-- el cliente hace un pedido
INSERT INTO `pedidosconlineas` (`Identificador`, `fecha`, `id_cliente`) VALUES (NULL, '2025-09-25', '12');

-- insertamos lineas de pedido

INSERT INTO `lineaspedido` (`Identificador`, `producto_id`, `unidades`, `pedidos_id`) VALUES (NULL, '17', '2', '1');
```

### cruzamos tablas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL es una consulta que selecciona todos los registros de la tabla llamada `pedidosconlineas`. La palabra clave `SELECT` indica que estamos solicitando datos, y el asterisco (`*`) después de ella significa "todos los campos" o "todas las columnas". Esto quiere decir que se devolverán todas las filas y todas las columnas disponibles en la tabla especificada.

La estructura simple de esta consulta hace que sea útil para entender rápidamente cómo están organizados los datos en una tabla determinada. Sin embargo, es importante tener cuidado con el uso del asterisco en entornos de producción o donde se manejan grandes volúmenes de datos, ya que puede llevar a un rendimiento lento si la tabla tiene muchos registros.

En contexto educativo y para fines de aprendizaje, este tipo de consulta ayuda a familiarizar al estudiante con los datos disponibles antes de pasar a construir consultas más complejas que filtran o combinan información específica.

`008-cruzamos tablas.sql`

```sql
SELECT * FROM `pedidosconlineas`;
```

### cruzamos con tabla clientes
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está realizando una consulta que combina dos tablas: `pedidosconlineas` y `clientes`. La función principal es obtener la fecha del pedido, el nombre y los apellidos del cliente asociado a cada pedido. Utiliza un tipo especial de combinación llamada `LEFT JOIN`, lo cual asegura que todos los pedidos en la tabla `pedidosconlineas` se incluyen en el resultado, incluso si no existe una correspondencia en la tabla `clientes`. Esto es especialmente útil cuando algunos pedidos pueden haber sido realizados por clientes cuyos datos no están completamente registrados o que no tienen un registro de cliente asociado.

La línea `ON pedidosconlineas.id_cliente = clientes.Identificador` especifica cómo las dos tablas se relacionan entre sí, en este caso a través del campo `id_cliente` de la tabla `pedidosconlineas`, que debe coincidir con el campo `Identificador` de la tabla `clientes`. Esto permite al sistema cruzar los datos y mostrar información completa sobre cada pedido en relación con su cliente.

`009-cruzamos con tabla clientes.sql`

```sql
SELECT 
pedidosconlineas.fecha,
clientes.nombre,
clientes.apellidos
FROM `pedidosconlineas`
LEFT JOIN clientes 
ON pedidosconlineas.id_cliente = clientes.Identificador
;
```

### cruzamos con la tabla de lineas de pedido
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL realiza una consulta que combina información de varias tablas relacionadas con pedidos, clientes y líneas de pedido. La consulta selecciona tres columnas: la fecha del pedido, el nombre y los apellidos del cliente asociado al pedido.

La tabla principal en esta consulta es `pedidosconlineas`, que probablemente contiene información básica sobre cada pedido junto con una referencia a las líneas de ese pedido. Luego, utiliza un JOIN izquierdo (LEFT JOIN) para combinar la tabla `clientes` con `pedidosconlineas` usando el identificador único del cliente (`id_cliente`) en ambas tablas. Esto permite obtener los nombres y apellidos de los clientes que han realizado los pedidos.

Además, se realiza otro LEFT JOIN para unir la tabla `lineaspedido`, que probablemente contiene detalles sobre cada línea individual dentro de un pedido (como el producto específico y su cantidad). Este segundo JOIN utiliza la columna `pedidos_id` en `lineaspedido` y la columna `Identificador` en `pedidosconlineas`.

En resumen, esta consulta es importante porque integra datos de diferentes tablas para proporcionar una vista más completa de los pedidos, incluyendo información sobre el cliente que hizo el pedido y detalles adicionales sobre las líneas del pedido. Esto ayuda a tener una visión integral del proceso de compra en la base de datos.

`010-cruzamos con la tabla de lineas de pedido.sql`

```sql
SELECT 
pedidosconlineas.fecha,
clientes.nombre,
clientes.apellidos
FROM `pedidosconlineas`

LEFT JOIN clientes 
ON pedidosconlineas.id_cliente = clientes.Identificador

LEFT JOIN lineaspedido
ON lineaspedido.pedidos_id = pedidosconlineas.Identificador
;
```

### ajustamos la proyeccion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL realiza una consulta que combina información de varias tablas para obtener detalles específicos sobre los pedidos, incluyendo la fecha del pedido, el nombre y apellidos del cliente, así como las unidades y el ID del producto en cada línea del pedido. 

La consulta utiliza dos operaciones `LEFT JOIN` para unir las tablas `pedidosconlineas`, `clientes`, y `lineaspedido`. El primer `LEFT JOIN` une la tabla `pedidosconlineas` con la tabla `clientes` basándose en el ID del cliente, mientras que el segundo `LEFT JOIN` une nuevamente `pedidosconlineas` con la tabla `lineaspedido` utilizando el ID del pedido. 

Esta consulta es importante porque permite visualizar toda la información relacionada con un pedido de una sola vez, facilitando así el análisis y el manejo de datos en contextos empresariales o comerciales donde se requiere entender completamente cada transacción, desde quién hizo el pedido hasta qué productos incluye y cuántas unidades de cada uno fueron pedidas.

`011-ajustamos la proyeccion.sql`

```sql
SELECT 
pedidosconlineas.fecha,
clientes.nombre,
clientes.apellidos,
lineaspedido.unidades,
lineaspedido.producto_id

FROM `pedidosconlineas`

LEFT JOIN clientes 
ON pedidosconlineas.id_cliente = clientes.Identificador

LEFT JOIN lineaspedido
ON lineaspedido.pedidos_id = pedidosconlineas.Identificador
;
```

### cruzamos con productos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL realiza una consulta compleja que combina información de varias tablas para proporcionar detalles sobre los pedidos, incluyendo datos del cliente y el producto asociado. La consulta selecciona específicamente la fecha del pedido, el nombre y apellidos del cliente, las unidades compradas en cada línea del pedido y el nombre junto con el precio del producto.

El código utiliza varias operaciones `LEFT JOIN` para unir estas tablas basándose en los identificadores únicos que relacionan una tabla con otra. Por ejemplo, la primera operación `LEFT JOIN` une la tabla `pedidosconlineas` con la tabla `clientes` utilizando el campo `id_cliente` de `pedidosconlineas` y el campo `Identificador` de `clientes`. Esto permite obtener toda la información relacionada con el cliente para cada pedido. Luego, se realiza un segundo `LEFT JOIN` para conectar las líneas del pedido a los pedidos mediante sus identificadores únicos. Finalmente, se une la tabla `productos` a través de su ID en la tabla `lineaspedido`.

Esta consulta es importante porque permite obtener una visión completa y detallada de cada pedido, incluyendo información sobre el cliente que realizó el pedido, las líneas del pedido con sus unidades y los productos específicos comprados junto con su precio.

`012-cruzamos con productos.sql`

```sql
SELECT 
pedidosconlineas.fecha,
clientes.nombre,
clientes.apellidos,
lineaspedido.unidades,
productos.nombre,
productos.precio

FROM `pedidosconlineas`

LEFT JOIN clientes 
ON pedidosconlineas.id_cliente = clientes.Identificador

LEFT JOIN lineaspedido
ON lineaspedido.pedidos_id = pedidosconlineas.Identificador

LEFT JOIN productos
ON lineaspedido.producto_id = productos.Identificador
;
```

### calculos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL realiza una consulta que combina información de varias tablas para generar un resumen detallado de los pedidos. La consulta selecciona la fecha del pedido, el nombre y apellidos del cliente, las unidades compradas en cada línea del pedido, el nombre del producto, su precio unitario, así como cálculos adicionales que incluyen el subtotal (precio por unidad multiplicado por la cantidad), el IVA (subtotal multiplicado por 16%), y el total (subtotal más el IVA).

Para obtener estos datos, se utilizan tres operaciones de JOIN:
- Se une primero la tabla `pedidosconlineas` con la tabla `clientes` usando el identificador del cliente.
- Luego, esta combinación se une con la tabla `lineaspedido`, que contiene información sobre las líneas individuales de cada pedido, a través del identificador del pedido.
- Finalmente, se añade otra unión con la tabla `productos`, vinculando los productos de las líneas del pedido a sus respectivos registros en la tabla de productos.

Esta consulta es importante porque proporciona una visión completa y detallada del contenido de cada pedido, incluyendo detalles económicos como el subtotal, IVA y total para cada artículo, lo cual es útil tanto para reportes internos como para facturación.

`013-calculos.sql`

```sql
SELECT 
pedidosconlineas.fecha,
clientes.nombre,
clientes.apellidos,
lineaspedido.unidades,
productos.nombre,
productos.precio,
productos.precio*lineaspedido.unidades AS Subtotal,
productos.precio*lineaspedido.unidades * 0.16 AS IVA,
productos.precio*lineaspedido.unidades * 1.16 AS Total

FROM `pedidosconlineas`

LEFT JOIN clientes 
ON pedidosconlineas.id_cliente = clientes.Identificador

LEFT JOIN lineaspedido
ON lineaspedido.pedidos_id = pedidosconlineas.Identificador

LEFT JOIN productos
ON lineaspedido.producto_id = productos.Identificador
;
```

### sumatorio
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL es una consulta que realiza cálculos sobre datos relacionados en varias tablas. La consulta selecciona la fecha del pedido, el nombre y los apellidos del cliente, y calcula el total de cada pedido incluyendo el IVA (16%). 

La consulta comienza uniendo las tablas `pedidosconlineas`, `clientes`, `lineaspedido` y `productos` usando cláusulas LEFT JOIN para garantizar que se incluyen todos los pedidos, incluso si no tienen asociados clientes o productos específicos en otras tablas. Luego, suma el producto del precio de cada artículo multiplicado por la cantidad comprada (y añade un 16% de IVA) para obtener el total del pedido.

Finalmente, agrupa los resultados por el identificador único de cada pedido (`pedidosconlineas.Identificador`) y muestra la fecha del pedido, el nombre completo del cliente y el total calculado. Esto es útil para tener una visión general de todos los pedidos realizados, incluyendo información sobre quién hizo cada pedido y cuánto costó en total.

Esta consulta es importante porque proporciona un resumen detallado de la actividad comercial basado en datos almacenados en diferentes tablas relacionadas.

`014-sumatorio.sql`

```sql
SELECT 
pedidosconlineas.fecha,
clientes.nombre,
clientes.apellidos,
SUM(productos.precio*lineaspedido.unidades * 1.16) AS Total

FROM `pedidosconlineas`

LEFT JOIN clientes 
ON pedidosconlineas.id_cliente = clientes.Identificador

LEFT JOIN lineaspedido
ON lineaspedido.pedidos_id = pedidosconlineas.Identificador

LEFT JOIN productos
ON lineaspedido.producto_id = productos.Identificador

GROUP BY pedidosconlineas.Identificador
;
```

### Actividades propuestas

### Actividad 1: Consulta Básica de Pedidos
**Descripción:** El alumno debe crear una consulta SQL que seleccione todos los registros de la tabla `pedidos`. Este ejercicio permitirá a los estudiantes familiarizarse con las consultas básicas en SQL.

### Actividad 2: JOIN Simple entre Tablas
**Descripción:** Los alumnos deben escribir una consulta que realice un LEFT JOIN entre las tablas `pedidos` y `clientes`, seleccionando la fecha del pedido, el nombre y los apellidos del cliente. Este ejercicio ayudará a entender cómo combinar datos de múltiples tablas.

### Actividad 3: Consulta Compleja con JOIN
**Descripción:** Los estudiantes deben crear una consulta que realice varios LEFT JOIN entre `pedidos`, `clientes`, `productos` e incluya información como el nombre del producto, su precio, IVA y total por línea de pedido. Este ejercicio permitirá a los alumnos practicar la creación de consultas más complejas.

### Actividad 4: Creación de una Tabla con Líneas de Pedido
**Descripción:** Se pide a los estudiantes que creen dos tablas nuevas, `pedidosconlineas` y `lineaspedido`, para representar un pedido con múltiples líneas. Este ejercicio ayudará a comprender la necesidad y diseño de relaciones 1:N en una base de datos.

### Actividad 5: Definición de Claves Foráneas
**Descripción:** Los alumnos deben definir las claves foráneas para establecer las relaciones entre `pedidosconlineas`, `clientes` y `productos`. Este ejercicio permitirá a los estudiantes entender la importancia de mantener la integridad referencial en una base de datos.

### Actividad 6: Inserción de Datos
**Descripción:** Los alumnos deben insertar un nuevo pedido con varias líneas de pedido en las tablas `pedidosconlineas` y `lineaspedido`. Este ejercicio ayudará a los estudiantes a practicar la inserción de datos relacionados en múltiples tablas.

### Actividad 7: Consulta Cruzada Simples
**Descripción:** Los alumnos deben escribir una consulta que seleccione todos los registros de `pedidosconlineas` y se unan con la tabla `clientes`. Este ejercicio permitirá a los estudiantes practicar consultas de join básico pero en contexto.

### Actividad 8: Consulta Cruzada Compleja
**Descripción:** Los alumnos deben crear una consulta que realice un LEFT JOIN entre `pedidosconlineas`, `clientes` y `lineaspedido`. Este ejercicio permitirá a los estudiantes practicar consultas más avanzadas con múltiples tablas.

### Actividad 9: Consulta Cruzada Ajustada
**Descripción:** Los alumnos deben ajustar una consulta existente para proyectar información relevante como unidades, producto_id y otros campos relevantes. Este ejercicio permitirá a los estudiantes aprender cómo filtrar y seleccionar datos específicos en sus consultas.

### Actividad 10: Consulta con Cálculos Financieros
**Descripción:** Los alumnos deben crear una consulta que calcule el subtotal, IVA y total para cada línea de pedido. Este ejercicio permitirá a los estudiantes practicar cálculos en SQL junto con la selección de datos.

### Actividad 11: Resumen de Total por Pedido
**Descripción:** Los alumnos deben escribir una consulta que muestre el total del pedido agrupado por cada identificador de pedido. Este ejercicio permitirá a los estudiantes aprender cómo utilizar funciones de agregación en SQL, como SUM y GROUP BY.

Estas actividades están diseñadas para cubrir diferentes aspectos del manejo de bases de datos relacionales y consultas SQL, adaptadas al nivel y conocimientos de los estudiantes de Formación Profesional.


<a id="composiciones-externas"></a>
## Composiciones externas

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/003-Realizaci%C3%B3n%20de%20consultas/006-Composiciones%20externas)


<a id="subconsultas"></a>
## Subconsultas

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/003-Realizaci%C3%B3n%20de%20consultas/007-Subconsultas)


<a id="combinacion-de-multiples-selecciones"></a>
## Combinación de múltiples selecciones

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/003-Realizaci%C3%B3n%20de%20consultas/008-Combinaci%C3%B3n%20de%20m%C3%BAltiples%20selecciones)


<a id="optimizacion-de-consultas"></a>
## Optimización de consultas

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/003-Realizaci%C3%B3n%20de%20consultas/009-Optimizaci%C3%B3n%20de%20consultas)


<a id="ejercicio-de-final-de-unidad-2"></a>
## Ejercicio de final de unidad

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/003-Realizaci%C3%B3n%20de%20consultas/101-Ejercicio%20de%20final%20de%20unidad)

### Introducción a los ejercicios

En esta sección de ejercicios, centraremos nuestra atención en la realización de consultas en bases de datos, un tema crucial para cualquier profesional que desee dominar el manejo de información. El único archivo proporcionado, "001-actividad.md", incluye una serie de problemas diseñados para reforzar tu comprensión sobre cómo formular y ejecutar consultas SQL efectivas en distintos contextos. A través de esta actividad, practicarás la creación de consultas complejas que involucran operaciones como JOIN, WHERE y GROUP BY, entre otros conceptos importantes. Además, trabajarás en el análisis de datos para extraer información relevante y útil para toma de decisiones empresariales.

### Actividades propuestas

### Actividad 1: Consultas SQL Básicas

**Descripción:** Los estudiantes deberán realizar varias consultas SQL sobre una base de datos proporcionada. Se espera que practiquen la selección, proyección y combinación de tablas para entender los conceptos fundamentales de las consultas en SQL.

### Actividad 2: Operadores Lógicos y Comparativos

**Descripción:** En esta actividad, los estudiantes deben utilizar operadores lógicos (AND, OR) y comparativos (>, <, =) en sus consultas SQL para filtrar datos según ciertos criterios y aprender a manejar condiciones más complejas.

### Actividad 3: Funciones Agregadas

**Descripción:** Los alumnos trabajarán con funciones agregadas como COUNT, SUM, AVG, MAX y MIN para obtener información resumida de los datos en la base de datos. Se espera que comprendan cómo extraer estadísticas útiles a partir de grandes conjuntos de datos.

### Actividad 4: Consultas JOIN

**Descripción:** Los estudiantes deberán unir varias tablas utilizando INNER JOIN, LEFT JOIN y RIGHT JOIN para obtener información completa desde múltiples fuentes dentro de la base de datos. Se busca mejorar sus habilidades en la combinación efectiva de datos dispersos.

### Actividad 5: Consultas con SUBQUERIES

**Descripción:** Los alumnos aprenderán a crear consultas que incluyen subconsultas para obtener resultados más precisos y complejos. Esto implica entender cómo las subconsultas pueden ser utilizadas en la cláusula WHERE o como parte de una función agregada.

### Actividad 6: Consultas con GROUP BY

**Descripción:** Los estudiantes practicarán el uso del comando GROUP BY junto con funciones agregadas para clasificar datos y obtener resúmenes estadísticos por categorías. Se espera que comprendan cómo organizar resultados de manera coherente.

### Actividad 7: Consultas con ORDENACIÓN

**Descripción:** Los alumnos deben ordenar los resultados de sus consultas utilizando ORDER BY, tanto para columnas numéricas como alfanuméricas, aprendiendo a manipular la presentación de datos de acuerdo a criterios específicos.

### Actividad 8: Creación de Consultas Completas

**Descripción:** En esta actividad final, los estudiantes deberán combinar todos los conceptos aprendidos para diseñar consultas complejas que incluyan JOINs, subconsultas y funciones agregadas. Se busca que puedan abordar problemas prácticos utilizando una variedad de técnicas SQL.

Cada una de estas actividades está diseñada para ayudar a los estudiantes a profundizar en el manejo de bases de datos mediante consultas SQL, adaptando gradualmente la dificultad y el nivel de complejidad.



<a id="tratamiento-de-datos"></a>
# Tratamiento de datos

<a id="insercion-borrado-y-modificacion-de-registros"></a>
## Inserción, borrado y modificación de registros

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/004-Tratamiento%20de%20datos/001-Inserci%C3%B3n%2C%20borrado%20y%20modificaci%C3%B3n%20de%20registros)

### Introducción a los ejercicios

Esta carpeta contiene una serie de ejercicios prácticos que te ayudarán a entender y aplicar las operaciones básicas de manejo de datos en bases de datos, conocidas como CRUD (Crear, Leer, Actualizar, Borrar). Los ejercicios se centran principalmente en la inserción, borrado y modificación de registros en una tabla llamada `clientes`. A través de estos ejercicios, aprenderás a utilizar comandos SQL como `INSERT`, `UPDATE` y `DELETE` correctamente para gestionar los datos de tu base de datos. También explorarás situaciones que pueden ocurrir cuando se producen errores, como añadir un campo adicional no previsto en la tabla o omitir uno necesario.

Estos ejercicios son fundamentales para cualquier estudiante de Formación Profesional interesado en el desarrollo web y bases de datos, ya que te capacitarán para realizar operaciones diarias con seguridad y eficacia.

### insercion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para insertar un nuevo registro en la tabla `clientes`. La instrucción `INSERT INTO` indica que vamos a añadir información a esta tabla. El valor `NULL` en la primera posición es importante porque generalmente las tablas tienen una columna identificadora (como un ID) que actúa como clave primaria y es automática, es decir, el sistema base de datos genera este número automáticamente si se deja en blanco con `NULL`. Los valores restantes ('Nombre del nuevo cliente', 'Apellidos del nuevo cliente', etc.) son los datos específicos del nuevo cliente que deseamos almacenar en la tabla. Al no especificar las columnas por nombre antes de los valores, SQL asume que estás proporcionando valores en el orden exacto en que las columnas están definidas en la estructura de la tabla.

Esta operación es crucial para mantener y actualizar una base de datos con información nueva o actualizada sobre clientes.

`002-insercion.sql`

```sql
INSERT INTO 
clientes 
VALUES
  ( 
    NULL,
    'Nombre del nuevo cliente',
    'Apellidos del nuevo cliente',
    '620891718',
    'info@jocarsa.com',
    'localidad del nuevo cliente'
   );
```

### que pasa si ponemos un campo de menos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para insertar un nuevo registro en la tabla `clientes`. La instrucción `INSERT INTO clientes VALUES` añade una fila con datos específicos a la tabla. En este caso, el primer valor es `NULL`, lo que indica que el campo correspondiente (probablemente la columna ID o alguna otra clave primaria autoincremental) será llenada automáticamente por el sistema de gestión de bases de datos.

Los valores 'Nombre del nuevo cliente', 'Apellidos del nuevo cliente', '620891718' y 'info@jocarsa.com' corresponden a los campos restantes en orden: nombre, apellidos, número telefónico y dirección de correo electrónico del cliente respectivamente. Es importante asegurarse de que el número de valores proporcionados coincida exactamente con el número de columnas en la tabla `clientes`, para evitar errores durante la ejecución del código.

Este tipo de instrucción es crucial cuando se necesita añadir nuevos registros a una base de datos, ya sea para gestionar información sobre clientes, pedidos o cualquier otro tipo de entidad que forme parte de un sistema administrativo.

`003-que pasa si ponemos un campo de menos.sql`

```sql
INSERT INTO 
clientes 
VALUES
  ( 
    NULL,
    'Nombre del nuevo cliente',
    'Apellidos del nuevo cliente',
    '620891718',
    'info@jocarsa.com'
   );
```

### que pasa si pongo un campo de mas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL intenta insertar un nuevo registro en la tabla `clientes`. La instrucción `INSERT INTO clientes VALUES` indica que se añadirá una fila nueva a esta tabla con los valores especificados. Sin embargo, hay un problema importante: el último campo `'campo que me invento'` no tiene ninguna columna correspondiente en la estructura de la tabla `clientes`.

La importancia de este código radica en enseñar qué sucede cuando se intenta insertar datos adicionales que no están previstos en la definición de la tabla. En la mayoría de los casos, el sistema devolverá un error indicando que esa columna extra no existe y la inserción no será exitosa.

Es crucial entender cómo deben ser precisas las instrucciones SQL para corresponder exactamente con la estructura del esquema de base de datos (schema) utilizado. Esto ayuda a prevenir errores y mantener la integridad de los datos en la base de datos.

`004-que pasa si pongo un campo de mas.sql`

```sql
INSERT INTO 
clientes 
VALUES
  ( 
    NULL,
    'Nombre del nuevo cliente',
    'Apellidos del nuevo cliente',
    '620891718',
    'info@jocarsa.com',
    'localidad del nuevo cliente',
    'campo que me invento'
   );
```

### columnas nombradas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está compuesto por dos partes principales: primero, se realiza la modificación de algunas columnas en una tabla llamada `clientes`, y luego se inserta un nuevo registro en esa misma tabla.

En la primera parte, el código utiliza sentencias `ALTER TABLE` para cambiar las características de tres columnas específicas (`telefono`, `email`, y `localidad`) dentro de la tabla `clientes`. Cada una de estas modificaciones cambia el tipo de datos a VARCHAR con un tamaño diferente (50 caracteres para teléfono, 100 para email y 255 para localidad) y especifica que se utilice el conjunto de caracteres UTF8MB4. Además, establece que estos campos pueden aceptar valores nulos (`NULL`).

La segunda parte del código es una sentencia `INSERT INTO`, que añade un nuevo registro a la tabla `clientes`. En este caso, solo se están proporcionando dos columnas para insertar datos: `nombre` y `apellidos`. Se está introduciendo un cliente con el nombre 'Nombre del nuevo cliente' y los apellidos 'Apellidos del nuevo cliente'.

Este código es importante porque muestra cómo puedes modificar las estructuras de tus tablas para adaptarse a nuevas necesidades y cómo añadir nuevos registros basados en esas modificaciones.

`005-columnas nombradas.sql`

```sql
ALTER TABLE `clientes` CHANGE `telefono` `telefono` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE `clientes` CHANGE `email` `email` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE `clientes` CHANGE `localidad` `localidad` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;


INSERT INTO 
clientes (nombre,apellidos)
VALUES
  ( 
    'Nombre del nuevo cliente',
    'Apellidos del nuevo cliente'
   );
```

### modificacion de registros
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para actualizar datos en una base de datos. Específicamente, está cambiando el nombre del campo `nombre` a `"Jose Vicente"` para todos los registros que existen en la tabla llamada `clientes`. La instrucción `UPDATE clientes` indica que estamos modificando la tabla `clientes`, y `SET nombre = "Jose Vicente"` especifica qué campo se actualiza con qué valor nuevo. Es importante tener cuidado al ejecutar este código porque afectará a todos los registros de la tabla, lo que podría no ser el resultado deseado si solo querías actualizar un registro específico.

`006-modificacion de registros.sql`

```sql
UPDATE
clientes
SET 
nombre = "Jose Vicente";
-- Cuidado porque esto actualiza TODA la tabla de clientes
```

### modificacion con un where
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL es una consulta `UPDATE` que se utiliza para modificar datos existentes en una base de datos. En este caso, el objetivo es cambiar el nombre del cliente con un número de teléfono específico. La consulta establece que el campo `nombre` de la tabla `clientes` debe ser actualizado a "Jose Vicente" solo para aquellos registros donde el campo `telefono` sea igual a 620891718.

La cláusula `WHERE` es crucial porque limita los cambios solo a los registros que cumplen con la condición especificada. Sin ella, todos los nombres en la tabla `clientes` se modificarían a "Jose Vicente", lo cual probablemente no sería el resultado deseado. Este tipo de consulta es importante cuando necesitas realizar modificaciones precisas y controladas en tu base de datos para mantener la integridad de tus registros.

`007-modificacion con un where.sql`

```sql
UPDATE
clientes
SET 
nombre = "Jose Vicente"
WHERE
telefono = 620891718;
```

### eliminar registros
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL es una instrucción para eliminar todos los registros de la tabla llamada `clientes`. La línea `DELETE FROM clientes;` indica que se van a borrar todas las filas existentes en esta tabla. Es importante entender que este comando no tiene ninguna condición (`WHERE`) y por lo tanto, afectará a todos los registros sin excepciones.

La segunda línea del código, `-- Nunca ejecutéis esto`, es un comentario que actúa como una advertencia para el usuario. Este mensaje subraya la importancia de tener cuidado al usar este tipo de comandos porque eliminar todos los datos de una tabla puede resultar en la pérdida irreparable de información crítica.

Es crucial ser extremadamente cauteloso con esta instrucción ya que no hay retroceso posible después de ejecutarla; por eso, siempre es recomendable hacer copias de seguridad antes de realizar operaciones de borrado masivo.

`008-eliminar registros.sql`

```sql
DELETE FROM
clientes;
-- Nunca ejecutéis esto
```

### eliminacion con condiciones
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para eliminar un registro específico de la tabla `clientes` en una base de datos. La instrucción `DELETE FROM clientes WHERE telefono = '620891718';` busca el cliente cuyo número telefónico es '620891718' y lo elimina de la tabla.

La cláusula `WHERE` es crucial porque limita la eliminación a un solo registro que cumple con la condición especificada, en este caso, tener el teléfono específico. Sin esta condición, se eliminarían todos los registros de la tabla `clientes`, lo cual probablemente no es el resultado deseado.

Es importante ser cuidadoso al usar instrucciones `DELETE` para asegurar que solo se eliminan los datos que realmente quieren deshacerse y tener precaución para evitar la pérdida accidental de información valiosa.

`009-eliminacion con condiciones.sql`

```sql
DELETE FROM
clientes
WHERE telefono = '620891718';
```

### copia de seguridad de base de datos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es una secuencia de comandos utilizados para crear una copia de seguridad (backup) de una base de datos MySQL. Primero, se crean las carpetas necesarias y luego se intenta realizar el backup usando `mysqldump`, un comando que permite hacer respaldo de bases de datos completas o parciales.

En primer lugar, se observa cómo el usuario cambia a la carpeta del escritorio (`cd Escritorio/`) y crea una nueva carpeta llamada `micopiadeseguridad` donde almacenará los archivos de copias de seguridad. Luego, intenta hacer un backup de la base de datos llamada "empresarial" usando el usuario "usuarioempresarial". Sin embargo, se produce un error debido a que el usuario no tiene suficientes privilegios para realizar esta operación.

Para resolver este problema, se otorga al usuario "usuarioempresarial" los privilegios necesarios ejecutando `GRANT PROCESS ON *.* TO 'usuarioempresarial'@'localhost';`. Esto permite que el usuario pueda acceder a la información de proceso en todas las bases de datos del servidor. El comando `FLUSH PRIVILEGES` actualiza la lista de usuarios y privilegios para asegurar que los cambios se aplican inmediatamente.

Finalmente, después de otorgar los privilegios necesarios, el usuario vuelve a intentar hacer el backup con éxito usando nuevamente `mysqldump`. El resultado es un archivo llamado `copia_de_seguridad_empresarial.sql` que contiene una copia completa de la base de datos "empresarial". Este procedimiento es crucial para asegurar que se pueda recuperar la información en caso de pérdida o daño a la base de datos original.

`010-copia de seguridad de base de datos.sql`

```sql
josevicente@josevicenteportatil:~$ cd Escritorio/
josevicente@josevicenteportatil:~/Escritorio$ mkdir micopiadeseguridad
josevicente@josevicenteportatil:~/Escritorio$ cd copiadeseguridad

josevicente@josevicenteportatil:~/Escritorio/micopiadeseguridad$ mysqldump -u   usuarioempresarial -p empresarial > copia_de_seguridad_empresarial.sql
Enter password: 
mysqldump: Error: 'Access denied; you need (at least one of) the PROCESS privilege(s) for this operation' when trying to dump tablespaces


GRANT PROCESS ON *.* TO 'usuarioempresarial'@'localhost';
FLUSH PRIVILEGES

mysqldump -u 	usuarioempresarial -p empresarial > copia_de_seguridad_empresarial.sql

mysqldump = comando 
-u = te voy a pasar un usuario
usuarioempresarial = el usuario que se va a utilizar 
-p = te voy a pedir la contraseña 
empresarial = nombre de la base de datos 
> = lo va a volcar en un archivo externo 
copia_de_seguridad_empresarial.sql = nombre del archivo de copia de seguridad
```

### Actividades propuestas

### Actividades Propuestas

1. **Creación de Registros**
   - **Descripción:** Los estudiantes deben insertar varios registros nuevos en la tabla `clientes`. Se espera que aprendan a manejar correctamente los valores NULL y entender el impacto de omitir o añadir campos inesperados.

2. **Manejo de Campos Omitidos e Incluidos**
   - **Descripción:** Los estudiantes deben probar qué ocurre cuando se omite un campo necesario durante la inserción (como en `003-que pasa si ponemos un campo de menos.sql`) y también cuando añaden campos adicionales no definidos (como en `004-que pasa si pongo un campo de mas.sql`). Se busca mejorar su comprensión sobre las reglas de esquema.

3. **Modificar Registros: Sin Condiciones**
   - **Descripción:** Los estudiantes deberán escribir y ejecutar comandos SQL para modificar registros en la tabla `clientes` sin usar condiciones específicas (como en `006-modificacion de registros.sql`). Se pretende que entiendan los riesgos involucrados.

4. **Modificar Registros: Con Condición**
   - **Descripción:** Los estudiantes deben escribir y ejecutar un comando SQL para actualizar registros en la tabla `clientes` con una condición específica (como en `007-modificacion con un where.sql`). Se espera que aprendan a seleccionar registros específicos para actualización.

5. **Eliminación de Registros: Sin Condiciones**
   - **Descripción:** Los estudiantes deben escribir y ejecutar comandos SQL para eliminar todos los registros de la tabla `clientes` sin condiciones (como en `008-eliminar registros.sql`). Se pretende que aprendan a evitar la eliminación masiva de datos críticos.

6. **Eliminación de Registros: Con Condición**
   - **Descripción:** Los estudiantes deben escribir y ejecutar comandos SQL para eliminar registros específicos en la tabla `clientes` usando una condición (como en `009-eliminacion con condiciones.sql`). Se espera que aprendan a seleccionar registros específicos para eliminación.

7. **Uso de Campos Nombrados**
   - **Descripción:** Los estudiantes deben escribir un comando SQL para insertar datos en la tabla `clientes` especificando los campos por nombre (como en `005-columnas nombradas.sql`). Se pretende que aprendan a manejar las columnas específicas al momento de inserción.

8. **Creación y Ejecución de Copias de Seguridad**
   - **Descripción:** Los estudiantes deben crear un script para generar una copia de seguridad de la base de datos `empresarial` utilizando el comando mysqldump (como en `010-copia de seguridad de base de datos.sql`). Se espera que aprendan a proteger y respaldar sus bases de datos.

Estas actividades están diseñadas para ayudar a los estudiantes a dominar las operaciones CRUD básicas y avanzadas en SQL, así como entender el impacto de diferentes comandos sobre la integridad de los datos.


<a id="integridad-referencial"></a>
## Integridad referencial

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/004-Tratamiento%20de%20datos/002-Integridad%20referencial)

### Introducción a los ejercicios

El script que proporcionaste realiza varias acciones para respaldar una base de datos MySQL con un enfoque en las tablas y vistas importantes. Aquí está el desglose de lo que hace:

### Paso 1: Creación del Script Shell Python
Se utiliza la biblioteca `sh` para ejecutar comandos shell desde Python.

```python
import sh

# Cambiar a la carpeta actual
sh.cd('.')
```

Este comando cambia a la carpeta actual en la que se está ejecutando el script. Esto es útil si necesitas ejecutar otros comandos relativos a esta ubicación específica.

### Paso 2: Crear Directorio de Respaldos (si no existe)
```python
# Verifica y crea el directorio de respaldo si no existe
sh.mkdir('-p', 'database_backups')
```

Este comando asegura que haya un directorio llamado `database_backups` donde se guardarán los respaldos.

### Paso 3: Crear la Base de Datos en MySQL (si no existe)
```python
# Verificar y crear la base de datos si no existe
sh.mysqldump('--no-data', '--add-drop-database', 'sistemadb').pipe(sh.mysql('-u root'))
```

Este comando verifica si la base de datos `sistemadb` ya existe. Si no, se crea usando los esquemas existentes (las definiciones de las tablas) que `mysqldump --no-data --add-drop-database` proporciona.

### Paso 4: Realizar un DUMP Completo de la Base de Datos
```python
# Crear el respaldo completo del esquema y los datos de la base de datos
sh.mysqldump('-u root', 'sistemadb').to_file('database_backups/sistemadb_backup.sql')
```

Este comando crea un archivo SQL que contiene tanto el esquema (DDL) como los datos (DML) para la base de datos `sistemadb`. El respaldo se guarda en el directorio `database_backups` con el nombre `sistemadb_backup.sql`.

### Paso 5: Crear Tablas y Datos Específicos
Se utilizan comandos `mysqldump` adicionales para respaldar solo ciertas tablas o vistas específicas. Esto es útil si deseas realizar un backup incremental o foco en ciertas partes de la base de datos.

#### Ejemplo:
```python
# Respaldar una tabla específica
sh.mysqldump('-u root', 'sistemadb', 'tabla_especifica').to_file('database_backups/tabla_especifica_backup.sql')

# Respaldar una vista
sh.mysqldump('-u root', 'sistemadb', '--no-create-info', '--skip-triggers', 'vista_especifica').to_file('database_backups/vista_especifica_backup.sql')
```

### Resumen
- **Directorio de respaldo**: `database_backups`
- **Respaldos completos**: `mysqldump` para la base de datos completa y se guarda en un archivo `.sql`.
- **Respaldos parciales**: Se pueden crear respaldos específicos para tablas o vistas individuales.

### Consideraciones Adicionales
1. **Credenciales**: El script asume que el usuario `root` tiene acceso sin contraseña, lo cual no es recomendable en entornos de producción.
2. **Seguridad**: Asegúrate de cifrar los respaldos y limitar el acceso al directorio de respaldo para evitar la exposición de datos sensibles.
3. **Rotación de respaldos**: Considera implementar una rotación automática de respaldos para no llenar el disco con múltiples copias.

Este script es útil para automatizar tareas de respaldo y puede ser adaptado según las necesidades específicas del entorno en que se utilice.

### copia de seguridad con python
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código está diseñado para crear una copia de seguridad de una base de datos MySQL utilizando Python. Lo que hace es ejecutar el comando `mysqldump`, que es una herramienta que viene con MySQL y se usa para hacer respaldos completos o parciales de bases de datos.

El código primero define algunas variables importantes: el nombre del usuario, la contraseña y el nombre de la base de datos a respaldar. También especifica un archivo donde almacenará el respaldo generado por `mysqldump`.

Luego, se crea una lista llamada `comando` que contiene los parámetros necesarios para ejecutar `mysqldump`. La lista incluye las opciones `-u` y `-p`, seguidas del usuario y la contraseña definidos anteriormente, y el nombre de la base de datos.

El código utiliza la función `subprocess.run()` para ejecutar el comando `mysqldump`. El parámetro `stdout=salida` indica que la salida generada por `mysqldump` se escribirá en el archivo especificado. La opción `check=True` asegura que si el comando falla, el programa lanzará una excepción.

Finalmente, imprime un mensaje indicando que la copia de seguridad ha sido creada y muestra el nombre del archivo donde se guardó el respaldo.

Esta técnica es muy útil para mantener copias de seguridad regulares de tus bases de datos, lo cual es crucial en entornos empresariales para evitar perder información importante.

`005-copia de seguridad con python.py`

```python
import subprocess

usuario = "usuarioempresarial"
password = "usuarioempresarial"
base_datos = "empresarial"
archivo_salida = "copia_de_seguridad.sql"

comando = [
    "mysqldump",
    f"-u{usuario}",
    f"-p{password}",
    base_datos
]

with open(archivo_salida, "w") as salida:
    subprocess.run(comando, stdout=salida, check=True)

print(f"Copia de seguridad creada en {archivo_salida}")
```

### copia con fecha
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es una pequeña herramienta escrita en Python que realiza una copia de seguridad de una base de datos MySQL utilizando el comando `mysqldump`. La función principal del código es crear un respaldo de la base de datos "empresarial" y guardar este respaldo con un nombre que incluye la fecha y hora exactos en que se realizó.

El código comienza importando dos módulos: `subprocess`, que permite ejecutar comandos del sistema desde Python, y `datetime`, para trabajar con fechas y horas. Luego obtiene la fecha y hora actuales y las formatea para incluirlas en el nombre del archivo de copia de seguridad.

A continuación, se definen variables como el usuario y contraseña necesarios para conectarse a la base de datos, así como el nombre de la base de datos que será respaldada. El nombre del archivo donde se guardará la copia de seguridad incluye un timestamp (marca temporal) generado usando los valores de fecha y hora.

El código luego crea una lista llamada `comando` que contiene todos los argumentos necesarios para ejecutar el comando `mysqldump`, incluyendo las credenciales del usuario. Se abre un archivo con el nombre generado previamente en modo escritura, y se utiliza `subprocess.run()` para ejecutar el comando `mysqldump`. La salida de este comando es redirigida directamente al archivo que acabamos de abrir.

Finalmente, si la operación se realiza correctamente, el programa imprime un mensaje indicando dónde se ha guardado la copia de seguridad. Este tipo de script es muy útil para automatizar las tareas de respaldo y asegurar que los datos importantes estén siempre protegidos contra posibles fallos o pérdidas.

`006-copia con fecha.py`

```python
import subprocess
from datetime import datetime

ahora = datetime.now()

anio = ahora.year.zfill(2)
mes = ahora.month.zfill(2)
dia = ahora.day.zfill(2)
hora = ahora.hour.zfill(2)
minuto = ahora.minute.zfill(2)
segundo = ahora.second.zfill(2)

usuario = "usuarioempresarial"
password = "usuarioempresarial"
base_datos = "empresarial"
archivo_salida = str(anio)+str(mes)+str(dia)+str(hora)+str(minuto)+str(segundo)+"_copia_de_seguridad.sql"

comando = [
    "mysqldump",
    f"-u{usuario}",
    f"-p{password}",
    base_datos
]

with open(archivo_salida, "w") as salida:
    subprocess.run(comando, stdout=salida, check=True)

print(f"Copia de seguridad creada en {archivo_salida}")
```

### zerofill
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código Python realiza una copia de seguridad de una base de datos MySQL y la guarda en un archivo con nombre específico que incluye la fecha y hora exactos del momento de creación. Primero, el programa importa dos bibliotecas: `subprocess`, para ejecutar comandos externos, y `datetime`, para obtener información sobre la fecha y hora actuales.

Luego, se extraen los componentes de la fecha y hora (año, mes, día, hora, minuto y segundo) y se convierten en cadenas. Es importante notar el uso del método `.zfill(2)` o `.zfill(4)`, que asegura que cada parte tenga un formato de dos dígitos para los meses, días, horas, minutos y segundos, y cuatro dígitos para el año, añadiendo ceros a la izquierda si es necesario. Esto garantiza una consistencia en la nomenclatura del archivo.

Finalmente, se define el nombre del usuario, la contraseña y el nombre de la base de datos que queremos respaldar. Se construye un comando `mysqldump` (un utilitario de MySQL) con estos detalles para generar la copia de seguridad. El programa ejecuta este comando usando `subprocess.run`, redirigiendo la salida del comando a un archivo cuyo nombre es una concatenación de todos los componentes de fecha y hora generados anteriormente, seguido de "_copia_de_seguridad.sql". Al finalizar, se imprime en pantalla el mensaje indicando dónde se ha guardado la copia de seguridad.

Este tipo de script es muy útil para asegurar que no se pierdan datos importantes almacenados en bases de datos MySQL, permitiendo restaurar la base de datos a un estado previo si ocurre algún error o problema.

`007-zerofill.py`

```python
import subprocess
from datetime import datetime

ahora = datetime.now()

anio = str(ahora.year).zfill(4)
mes = str(ahora.month).zfill(2)
dia = str(ahora.day).zfill(2)
hora = str(ahora.hour).zfill(2)
minuto = str(ahora.minute).zfill(2)
segundo = str(ahora.second).zfill(2)

usuario = "usuarioempresarial"
password = "usuarioempresarial"
base_datos = "empresarial"
archivo_salida = str(anio)+str(mes)+str(dia)+str(hora)+str(minuto)+str(segundo)+"_copia_de_seguridad.sql"

comando = [
    "mysqldump",
    f"-u{usuario}",
    f"-p{password}",
    base_datos
]

with open(archivo_salida, "w") as salida:
    subprocess.run(comando, stdout=salida, check=True)

print(f"Copia de seguridad creada en {archivo_salida}")
```

### ahora comprimir
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es una herramienta en Python diseñada para crear copias de seguridad de bases de datos MySQL. El programa empieza por importar las bibliotecas necesarias: `subprocess` para ejecutar comandos del sistema, `datetime` para obtener la fecha y hora actuales, y `zipfile` para comprimir archivos.

Primero, el código obtiene los valores actuales de la fecha y hora y los formatea para crear un nombre único para el archivo de copia de seguridad. Luego, especifica las credenciales del usuario y la base de datos que se va a respaldar, junto con una serie de variables que definen cómo se llamará el archivo SQL.

El script ejecuta el comando `mysqldump`, que es un utilitario MySQL usado para crear copias de seguridad en formato SQL. Este comando toma los datos de la base de datos especificada y los guarda en un archivo con el nombre generado anteriormente.

Después, el código crea un archivo ZIP comprimido a partir del archivo SQL recién creado usando la biblioteca `zipfile`. Finalmente, imprime mensajes que indican dónde se han guardado tanto el archivo SQL como el archivo ZIP.

Este tipo de script es importante en entornos empresariales donde es crucial mantener copias de seguridad seguras y accesibles. La compresión del archivo hace que sea más fácil almacenar y transmitir las copias de seguridad, además de proteger la información contra posibles cambios no autorizados o daños.

`010-ahora comprimir.py`

```python
import subprocess
from datetime import datetime
import zipfile
import os

ahora = datetime.now()

anio = str(ahora.year).zfill(4)
mes = str(ahora.month).zfill(2)
dia = str(ahora.day).zfill(2)
hora = str(ahora.hour).zfill(2)
minuto = str(ahora.minute).zfill(2)
segundo = str(ahora.second).zfill(2)

usuario = "usuarioempresarial"
password = "usuarioempresarial"
base_datos = "empresarial"
archivo_salida = f"{anio}{mes}{dia}{hora}{minuto}{segundo}_copia_de_seguridad.sql"
archivo_zip = archivo_salida.replace(".sql", ".zip")

comando = [
    "mysqldump",
    f"-u{usuario}",
    f"-p{password}",
    base_datos
]

# Crear la copia SQL
with open(archivo_salida, "w") as salida:
    subprocess.run(comando, stdout=salida, check=True)

print(f"Copia de seguridad creada en {archivo_salida}")

# Comprimir a ZIP
with zipfile.ZipFile(archivo_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(archivo_salida)

print(f"Copia comprimida en {archivo_zip}")

# (Opcional) eliminar el SQL y dejar solo el ZIP
# os.remove(archivo_salida)
```

### y borrar el sql
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código Python crea una copia de seguridad de una base de datos MySQL en formato SQL, luego la comprime en un archivo ZIP y finalmente elimina el archivo SQL original para dejar solo el archivo ZIP. 

El código comienza por obtener la fecha y hora actuales y las formatea con ceros a la izquierda para los meses, días, horas, minutos y segundos (por ejemplo, '01' en lugar de '1'). Luego establece variables para el usuario, contraseña y nombre de la base de datos que se va a respaldar. Crea un nombre de archivo para la copia de seguridad SQL utilizando la fecha y hora actuales.

A continuación, usa el comando `mysqldump` (un utilitario externo) para crear una copia de la base de datos especificada en un archivo `.sql`. Este comando se ejecuta usando la función `subprocess.run`, que permite invocar comandos desde Python y redirige su salida estándar al archivo SQL.

Después, el código crea un archivo ZIP con el contenido del archivo SQL recién creado utilizando la biblioteca de compresión interna de Python. Finalmente, elimina el archivo `.sql` para mantener solo la versión comprimida en formato ZIP.

Este tipo de script es útil para automatizar tareas de copias de seguridad y asegurar que tus datos importantes estén protegidos contra pérdida o corrupción, manteniendo una versión archivada del estado actual de tu base de datos.

`011-y borrar el sql.py`

```python
import subprocess
from datetime import datetime
import zipfile
import os

ahora = datetime.now()

anio = str(ahora.year).zfill(4)
mes = str(ahora.month).zfill(2)
dia = str(ahora.day).zfill(2)
hora = str(ahora.hour).zfill(2)
minuto = str(ahora.minute).zfill(2)
segundo = str(ahora.second).zfill(2)

usuario = "usuarioempresarial"
password = "usuarioempresarial"
base_datos = "empresarial"
archivo_salida = f"{anio}{mes}{dia}{hora}{minuto}{segundo}_copia_de_seguridad.sql"
archivo_zip = archivo_salida.replace(".sql", ".zip")

comando = [
    "mysqldump",
    f"-u{usuario}",
    f"-p{password}",
    base_datos
]

# Crear la copia SQL
with open(archivo_salida, "w") as salida:
    subprocess.run(comando, stdout=salida, check=True)

print(f"Copia de seguridad creada en {archivo_salida}")

# Comprimir a ZIP
with zipfile.ZipFile(archivo_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(archivo_salida)

# Eliminar el SQL y dejar solo el ZIP
os.remove(archivo_salida)

print(f"Copia comprimida en {archivo_zip} (se eliminó el SQL)")
```

### aplicacion mysql
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código es parte de un programa en Python que presenta al usuario un menú con diferentes opciones para interactuar con una base de datos de clientes. El programa muestra cuatro posibles acciones: insertar un nuevo cliente, listar todos los clientes existentes, actualizar información de un cliente y borrar un cliente. 

El código imprime estas opciones en la consola y luego espera que el usuario ingrese su elección a través del teclado. La entrada proporcionada por el usuario se convierte en un número entero gracias a `int(input("Escoge tu opción"))` y se almacena en la variable `opcion`. Esta selección permitirá al programa continuar con las acciones específicas correspondientes a cada opción elegida por el usuario.

Esta estructura es común en aplicaciones interactivas que requieren input del usuario para determinar qué acción realizar.

`015-aplicacion mysql.py`

```python
print("Escoge una opcion:")
print("1.-Insertar un cliente")
print("2.-Listar los clientes")
print("3.-Actualizar un cliente")
print("4.-Borrar un cliente")
opcion = int(input("Escoge tu opción"))
```

### tratamos las opciones
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es una parte del menú principal de una aplicación en Python que permite gestionar datos de clientes. El programa muestra al usuario cuatro opciones: insertar un nuevo cliente, listar todos los clientes existentes, actualizar la información de un cliente y eliminar a un cliente. 

El programa imprime estas opciones y luego espera que el usuario ingrese un número correspondiente a la acción que desea realizar. Dependiendo del número ingresado por el usuario (convertido a tipo `int`), se ejecuta una parte específica del código que muestra un mensaje indicando qué operación va a ser realizada.

Esta estructura es común en aplicaciones interactivas donde los usuarios pueden elegir entre varias acciones disponibles. Es importante porque proporciona una interfaz clara y controlada, permitiendo al usuario manejar datos de manera segura y organizada según sus necesidades específicas.

`016-tratamos las opciones.py`

```python
print("Escoge una opcion:")
print("1.-Insertar un cliente")
print("2.-Listar los clientes")
print("3.-Actualizar un cliente")
print("4.-Borrar un cliente")
opcion = int(input("Escoge tu opción"))

if opcion == 1:
  print("Insertamos un cliente")
elif opcion == 2:
  print("Listamos los clientes")
elif opcion == 3:
  print("Actualizamos un cliente")
elif opcion == 4:
  print("Eliminamos un cliente")
```

### nos conectamos a MySQL
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es una parte del programa que te permite interactuar con una base de datos MySQL. En primer lugar, el código solicita al usuario que introduzca información sobre un nuevo cliente: nombre, apellidos, teléfono, email y localidad. Luego, se establece una conexión a la base de datos utilizando la librería `mysql.connector`. El programa utiliza las credenciales de acceso (host, usuario, contraseña y nombre de la base de datos) para conectarse al servidor MySQL que está corriendo en el localhost.

Después de conectarse a la base de datos, se presenta un menú interactivo donde el usuario puede elegir entre cuatro opciones: insertar un nuevo cliente, listar todos los clientes existentes, actualizar información sobre un cliente o eliminar un cliente. Aunque las instrucciones específicas para realizar estas acciones no están completadas en este fragmento (por ejemplo, cómo ejecutar realmente las operaciones CRUD), el código muestra cómo estructurar y navegar por opciones simples dentro de una aplicación de base de datos.

Este tipo de interacción es importante porque permite al usuario administrar fácilmente los registros en la base de datos sin tener que escribir directamente consultas SQL.

`017-nos conectamos a MySQL.py`

```python
import mysql.connector

nombre = input("Introduce el nombre del cliente")
apellidos = input("Introduce los apellidos del cliente")
telefono = input("Introduce el telefono del cliente")
email = input("Introduce el email del cliente")
localidad = input("Introduce la localidad del cliente")

conexion = mysql.connector.connect(
    host="localhost",      
    user="usuarioempresarial",    
    password="usuarioempresarial",  
    database="empresarial"      
)

cursor = conexion.cursor()

print("Escoge una opcion:")
print("1.-Insertar un cliente")
print("2.-Listar los clientes")
print("3.-Actualizar un cliente")
print("4.-Borrar un cliente")
opcion = int(input("Escoge tu opción"))

if opcion == 1:
  print("Insertamos un cliente")
elif opcion == 2:
  print("Listamos los clientes")
elif opcion == 3:
  print("Actualizamos un cliente")
elif opcion == 4:
  print("Eliminamos un cliente")
```

### Desarrollo la parte de insercion de cliente
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código es una pequeña aplicación en Python que conecta a una base de datos MySQL y permite al usuario realizar operaciones básicas como insertar, listar, actualizar o borrar clientes. Primero, el programa solicita los detalles del cliente (nombre, apellidos, teléfono, email y localidad) usando la función `input()`. Luego, establece una conexión a la base de datos MySQL con las credenciales proporcionadas.

El usuario es preguntado para seleccionar una opción entre insertar un nuevo cliente, listar todos los clientes, actualizar un cliente existente o borrar un cliente. Si el usuario selecciona "Insertar un cliente", se solicitan nuevamente los detalles del cliente y luego se ejecuta la sentencia SQL `INSERT INTO` para añadir estos datos en una tabla llamada `clientes`. Es importante notar que esta parte del código tiene vulnerabilidades de seguridad ya que construye directamente las consultas SQL con valores ingresados por el usuario, lo cual puede llevar a ataques SQL Injection.

Después de realizar la operación deseada, se cierran tanto el cursor como la conexión a la base de datos para liberar los recursos. Este código es una introducción básica al manejo de bases de datos en Python y ayuda a entender cómo interactuar con MySQL desde un programa. Sin embargo, para aplicaciones reales, sería recomendable utilizar técnicas más seguras para evitar riesgos de seguridad como el SQL Injection.

`018-Desarrollo la parte de insercion de cliente.py`

```python
import mysql.connector

nombre = input("Introduce el nombre del cliente")
apellidos = input("Introduce los apellidos del cliente")
telefono = input("Introduce el telefono del cliente")
email = input("Introduce el email del cliente")
localidad = input("Introduce la localidad del cliente")

conexion = mysql.connector.connect(
    host="localhost",      
    user="usuarioempresarial",    
    password="usuarioempresarial",  
    database="empresarial"      
)

cursor = conexion.cursor()

print("Escoge una opcion:")
print("1.-Insertar un cliente")
print("2.-Listar los clientes")
print("3.-Actualizar un cliente")
print("4.-Borrar un cliente")
opcion = int(input("Escoge tu opción"))

if opcion == 1:
  print("Insertamos un cliente")
  nombre = input("Introduce el nombre del cliente")
  apellidos = input("Introduce los apellidos del cliente")
  telefono = input("Introduce el telefono del cliente")
  email = input("Introduce el email del cliente")
  localidad = input("Introduce la localidad del cliente")
  cursor.execute('''
    INSERT INTO clientes
    VALUES (
      NULL,
      "'''+nombre+'''",
      "'''+apellidos+'''",
      "'''+telefono+'''",
      "'''+email+'''",
      "'''+localidad+'''"
    )
  ''')
  conexion.commit()
elif opcion == 2:
  print("Listamos los clientes")
elif opcion == 3:
  print("Actualizamos un cliente")
elif opcion == 4:
  print("Eliminamos un cliente")
  
  
cursor.close() 

conexion.close()
```

### me aseguro
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código es una pequeña aplicación en Python que permite al usuario interactuar con una base de datos MySQL llamada `empresarial`. La aplicación conecta a la base de datos y ofrece al usuario cuatro opciones: insertar, listar, actualizar o borrar un cliente. 

Cuando el usuario selecciona la opción 1 (insertar un cliente), se le pide que introduzca información sobre el nuevo cliente como nombre, apellidos, teléfono, email y localidad. Luego, esta información es usada para ejecutar una consulta SQL que inserta un nuevo registro en la tabla `clientes` de la base de datos.

Para las otras opciones (2, 3 y 4), solo se imprimen mensajes indicativos sin realizar acciones específicas con la base de datos.

Es importante notar que este código tiene algunos riesgos, como la falta de comprobación de errores o validaciones en los datos introducidos por el usuario. Además, es recomendable evitar construir consultas SQL directamente a partir de strings introducidas por usuarios para prevenir problemas de seguridad y rendimiento.

El objetivo principal del código es proporcionar una interfaz básica para manejar clientes en una base de datos empresarial, permitiendo realizar operaciones CRUD (Crear, Leer, Actualizar, Borrar) con registros.

`019-me aseguro.py`

```python
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",      
    user="usuarioempresarial",    
    password="usuarioempresarial",  
    database="empresarial"      
)

cursor = conexion.cursor()

print("Escoge una opcion:")
print("1.-Insertar un cliente")
print("2.-Listar los clientes")
print("3.-Actualizar un cliente")
print("4.-Borrar un cliente")
opcion = int(input("Escoge tu opción"))

if opcion == 1:
  print("Insertamos un cliente")
  nombre = input("Introduce el nombre del cliente")
  apellidos = input("Introduce los apellidos del cliente")
  telefono = input("Introduce el telefono del cliente")
  email = input("Introduce el email del cliente")
  localidad = input("Introduce la localidad del cliente")
  cursor.execute('''
    INSERT INTO clientes
    VALUES (
      NULL,
      "'''+nombre+'''",
      "'''+apellidos+'''",
      "'''+telefono+'''",
      "'''+email+'''",
      "'''+localidad+'''"
    )
  ''')
  conexion.commit()
elif opcion == 2:
  print("Listamos los clientes")
elif opcion == 3:
  print("Actualizamos un cliente")
elif opcion == 4:
  print("Eliminamos un cliente")
  
  
cursor.close() 

conexion.close()
```

### arranco un bucle infinito
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código es una pequeña aplicación en Python que interactúa con una base de datos MySQL para realizar operaciones CRUD (Crear, Leer, Actualizar y Borrar) sobre la tabla `clientes`. La aplicación se conecta a la base de datos local mediante las credenciales proporcionadas y presenta al usuario un menú interactivo con cuatro opciones. 

El bucle `while True` asegura que el programa continúa ejecutándose hasta que se interrumpe manualmente, permitiendo así al usuario realizar múltiples operaciones sin necesidad de reiniciar la aplicación después de cada acción.

Cuando el usuario selecciona la opción 1, se le solicitan detalles del cliente y luego se insertan estos datos en la tabla `clientes` de la base de datos. Las demás opciones (Listar, Actualizar y Borrar) están listadas pero no implementadas completamente en este fragmento.

Es importante notar que esta forma básica de manejo de bases de datos es susceptible a inyecciones SQL si los datos del usuario no se validan adecuadamente antes de ser insertados. En un entorno real, sería recomendable usar consultas preparadas para prevenir esto y mejorar la seguridad.

`020-arranco un bucle infinito.py`

```python
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",      
    user="usuarioempresarial",    
    password="usuarioempresarial",  
    database="empresarial"      
)

cursor = conexion.cursor()
while True:
  print("Escoge una opcion:")
  print("1.-Insertar un cliente")
  print("2.-Listar los clientes")
  print("3.-Actualizar un cliente")
  print("4.-Borrar un cliente")
  opcion = int(input("Escoge tu opción"))

  if opcion == 1:
    print("Insertamos un cliente")
    nombre = input("Introduce el nombre del cliente: ")
    apellidos = input("Introduce los apellidos del cliente: ")
    telefono = input("Introduce el telefono del cliente: ")
    email = input("Introduce el email del cliente: ")
    localidad = input("Introduce la localidad del cliente: ")
    cursor.execute('''
      INSERT INTO clientes
      VALUES (
        NULL,
        "'''+nombre+'''",
        "'''+apellidos+'''",
        "'''+telefono+'''",
        "'''+email+'''",
        "'''+localidad+'''"
      )
    ''')
    conexion.commit()
  elif opcion == 2:
    print("Listamos los clientes")
    
  elif opcion == 3:
    print("Actualizamos un cliente")
  elif opcion == 4:
    print("Eliminamos un cliente")
  
  
cursor.close() 

conexion.close()
```

### Listado de clientes
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es una pequeña aplicación en Python que interactúa con una base de datos MySQL para gestionar información sobre clientes. La aplicación permite al usuario realizar operaciones básicas como insertar, listar, actualizar y eliminar registros de la tabla `clientes`.

El programa comienza conectándose a la base de datos mediante un objeto `mysql.connector`, especificando el host (localhost), las credenciales del usuario y la base de datos a utilizar. Luego crea un cursor para ejecutar consultas SQL.

A continuación, entra en un bucle infinito que presenta al usuario un menú interactivo con opciones para gestionar los clientes. Dependiendo de lo que elija el usuario:

1. Si se inserta un cliente (opción 1), el programa solicita datos como nombre, apellidos, teléfono, email y localidad del cliente. Luego ejecuta una consulta SQL `INSERT INTO` para agregar estos detalles en la base de datos.

2. Si se listan los clientes (opción 2), el programa ejecuta una consulta SQL `SELECT * FROM clientes` para recuperar todos los registros de la tabla y luego imprime cada fila del resultado en pantalla.

3. Las opciones para actualizar un cliente (opción 3) y eliminar uno (opción 4) no tienen lógica implementada aún, por lo que simplemente imprimen mensajes informativos sin realizar cambios en la base de datos.

Finalmente, el programa cierra el cursor y la conexión a la base de datos antes de terminar. Este tipo de script es útil para probar funciones básicas de gestión de bases de datos y aprender cómo interactuar con ellas usando Python.

`021-Listado de clientes.py`

```python
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",      
    user="usuarioempresarial",    
    password="usuarioempresarial",  
    database="empresarial"      
)

cursor = conexion.cursor()
while True:
  print("Escoge una opcion:")
  print("1.-Insertar un cliente")
  print("2.-Listar los clientes")
  print("3.-Actualizar un cliente")
  print("4.-Borrar un cliente")
  opcion = int(input("Escoge tu opción"))

  if opcion == 1:
    print("Insertamos un cliente")
    nombre = input("Introduce el nombre del cliente: ")
    apellidos = input("Introduce los apellidos del cliente: ")
    telefono = input("Introduce el telefono del cliente: ")
    email = input("Introduce el email del cliente: ")
    localidad = input("Introduce la localidad del cliente: ")
    cursor.execute('''
      INSERT INTO clientes
      VALUES (
        NULL,
        "'''+nombre+'''",
        "'''+apellidos+'''",
        "'''+telefono+'''",
        "'''+email+'''",
        "'''+localidad+'''"
      )
    ''')
    conexion.commit()
  elif opcion == 2:
    print("Listamos los clientes")
    cursor.execute("SELECT * FROM clientes")
    resultados = cursor.fetchall()
    for fila in resultados:
      print(fila)
  elif opcion == 3:
    print("Actualizamos un cliente")
  elif opcion == 4:
    print("Eliminamos un cliente")
  
  
cursor.close() 

conexion.close()
```

### Desarrollamos la parte de la eliminacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código es una parte de un programa en Python que gestiona operaciones básicas con una base de datos MySQL. El programa se conecta a una base de datos llamada "empresarial" y permite al usuario realizar acciones como insertar, listar, actualizar o eliminar clientes.

La conexión a la base de datos se establece usando el módulo `mysql.connector`. Después de conectarse, el código entra en un bucle infinito donde muestra un menú interactivo para que el usuario pueda seleccionar qué operación desea realizar. Dependiendo de la opción elegida por el usuario, el programa ejecuta diferentes acciones:

1. **Insertar un cliente**: Pide al usuario que introduzca los datos del nuevo cliente (nombre, apellidos, teléfono, email y localidad) y luego inserta estos datos en una tabla llamada `clientes` dentro de la base de datos.

2. **Listar clientes**: Ejecuta una consulta SQL para obtener todos los registros de la tabla `clientes` y muestra estos registros por pantalla.

3. **Actualizar un cliente** (esta opción no tiene código implementado en este fragmento).

4. **Eliminar un cliente**: Pide al usuario que introduzca el identificador del cliente que desea eliminar, luego ejecuta una consulta SQL para borrar ese registro de la tabla `clientes`.

Finalmente, después de terminar las operaciones, se cierra tanto el cursor como la conexión a la base de datos.

Este tipo de programa es útil en entornos donde se necesita administrar fácilmente registros de clientes o usuarios desde un sistema basado en una base de datos MySQL.

`022-Desarrollamos la parte de la eliminacion.py`

```python
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",      
    user="usuarioempresarial",    
    password="usuarioempresarial",  
    database="empresarial"      
)

cursor = conexion.cursor()
while True:
  print("Escoge una opcion:")
  print("1.-Insertar un cliente")
  print("2.-Listar los clientes")
  print("3.-Actualizar un cliente")
  print("4.-Borrar un cliente")
  opcion = int(input("Escoge tu opción"))

  if opcion == 1:
    print("Insertamos un cliente")
    nombre = input("Introduce el nombre del cliente: ")
    apellidos = input("Introduce los apellidos del cliente: ")
    telefono = input("Introduce el telefono del cliente: ")
    email = input("Introduce el email del cliente: ")
    localidad = input("Introduce la localidad del cliente: ")
    cursor.execute('''
      INSERT INTO clientes
      VALUES (
        NULL,
        "'''+nombre+'''",
        "'''+apellidos+'''",
        "'''+telefono+'''",
        "'''+email+'''",
        "'''+localidad+'''"
      )
    ''')
    conexion.commit()
  elif opcion == 2:
    print("Listamos los clientes")
    cursor.execute("SELECT * FROM clientes")
    resultados = cursor.fetchall()
    for fila in resultados:
      print(fila)
  elif opcion == 3:
    print("Actualizamos un cliente")
  elif opcion == 4:
    print("Eliminamos un cliente")
    id = input("Introduce el id del cliente que quieres eliminar: ")
    cursor.execute('''
      DELETE FROM clientes
      WHERE Identificador = '''+id+'''
    ''')
    conexion.commit()
  
  
cursor.close() 

conexion.close()
```

### backup
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este archivo contiene los registros del proceso de creación y compresión de copias de seguridad de una base de datos MySQL. Cada entrada indica que se ha creado un archivo `.sql` con la estructura y los datos actuales de la base de datos en el directorio especificado, y posteriormente se ha comprimido este archivo en un archivo `.zip`. El proceso emite advertencias indicando que usar una contraseña en la línea de comandos puede ser inseguro. Los nombres de los archivos generados incluyen la fecha y hora exacta de creación de la copia de seguridad, lo cual es útil para mantener un registro detallado de las operaciones realizadas.

Este procedimiento asegura que existen respaldos regulares de la base de datos, lo que es fundamental en el mantenimiento y la gestión de información crítica. Al comprimir los archivos `.sql` después de su creación se optimiza el uso del espacio en disco. Sin embargo, es importante tener cuidado con las advertencias sobre seguridad relacionadas con el uso de contraseñas en la línea de comandos para evitar posibles riesgos de acceso no autorizado a la base de datos.

`backup.log`

```
mysqldump: [Warning] Using a password on the command line interface can be insecure.
Copia de seguridad creada en /var/www/html/dam2526/Primero/Bases de datos/004-Tratamiento de datos/002-Integridad referencial/101-Ejercicios/20251002174737_copia_de_seguridad.sql
Copia comprimida en /var/www/html/dam2526/Primero/Bases de datos/004-Tratamiento de datos/002-Integridad referencial/101-Ejercicios/20251002174737_copia_de_seguridad.zip (se eliminó el SQL)
mysqldump: [Warning] Using a password on the command line interface can be insecure.
Copia de seguridad creada en /var/www/html/dam2526/Primero/Bases de datos/004-Tratamiento de datos/002-Integridad referencial/101-Ejercicios/20251002174801_copia_de_seguridad.sql
Copia comprimida en /var/www/html/dam2526/Primero/Bases de datos/004-Tratamiento de datos/002-Integridad referencial/101-Ejercicios/20251002174801_copia_de_seguridad.zip (se eliminó el SQL)
mysqldump: [Warning] Using a password on the command line interface can be insecure.
Copia de seguridad creada en /var/www/html/dam2526/Primero/Bases de datos/004-Tratamiento de datos/002-Integridad referencial/101-Ejercicios/20251002174901_copia_de_seguridad.sql
Copia comprimida en /var/www/html/dam2526/Primero/Bases de datos/004-Tratamiento de datos/002-Integridad referencial/101-Ejercicios/20251002174901_copia_de_seguridad.zip (se eliminó el SQL)
mysqldump: [Warning] Using a password on the command line interface can be insecure.
Copia de seguridad creada en /var/www/html/dam2526/Primero/Bases de datos/004-Tratamiento de datos/002-Integridad referencial/101-Ejercicios/20251002175001_copia_de_seguridad.sql
Copia comprimida en /var/www/html/dam2526/Primero/Bases de datos/004-Tratamiento de datos/002-Integridad referencial/101-Ejercicios/20251002175001_copia_de_seguridad.zip (se eliminó el SQL)
```

### backup
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es un script escrito en Python que realiza una copia de seguridad de una base de datos MySQL. Primero, importa las bibliotecas necesarias como `subprocess`, `datetime` y `zipfile`. Define la ruta absoluta donde se guardará la copia de seguridad y obtiene la fecha y hora actuales para nombrar el archivo de manera única.

El script utiliza comandos MySQL (`mysqldump`) para crear una copia de seguridad en formato SQL del esquema de base de datos "empresarial". Este comando se ejecuta mediante `subprocess.run`, redirigiendo la salida al archivo especificado. Luego, el script comprime este archivo SQL utilizando la biblioteca `zipfile` y crea un archivo ZIP.

Finalmente, el script elimina el archivo SQL original después de haberlo comprimido en un archivo ZIP para ahorrar espacio. Este proceso asegura que solo se conserve una copia segura del backup en formato comprimido, facilitando su almacenamiento y transferencia.

`backup.py`

```python
#!/usr/bin/env python3
import subprocess
from datetime import datetime
import zipfile
import os

# Ruta absoluta de la carpeta
BASE_DIR = "/var/www/html/dam2526/Primero/Bases de datos/004-Tratamiento de datos/002-Integridad referencial/101-Ejercicios"

ahora = datetime.now()

anio = str(ahora.year).zfill(4)
mes = str(ahora.month).zfill(2)
dia = str(ahora.day).zfill(2)
hora = str(ahora.hour).zfill(2)
minuto = str(ahora.minute).zfill(2)
segundo = str(ahora.second).zfill(2)

usuario = "usuarioempresarial"
password = "usuarioempresarial"
base_datos = "empresarial"
archivo_salida = os.path.join(BASE_DIR, f"{anio}{mes}{dia}{hora}{minuto}{segundo}_copia_de_seguridad.sql")
archivo_zip = archivo_salida.replace(".sql", ".zip")

comando = [
    "mysqldump",
    f"-u{usuario}",
    f"-p{password}",
    base_datos
]

# Crear la copia SQL
with open(archivo_salida, "w") as salida:
    subprocess.run(comando, stdout=salida, check=True)

print(f"Copia de seguridad creada en {archivo_salida}")

# Comprimir a ZIP
with zipfile.ZipFile(archivo_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(archivo_salida, os.path.basename(archivo_salida))

# Eliminar el SQL y dejar solo el ZIP
os.remove(archivo_salida)

print(f"Copia comprimida en {archivo_zip} (se eliminó el SQL)")
```

### copia_de_seguridad
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

El archivo proporcionado es un script de creación de base de datos MySQL que incluye la definición de varias tablas y una vista. A continuación, se describen los detalles principales del mismo:

### Tablas

1. **clientes**:
   - **Identificador**: Clave primaria autoincremental.
   - **nombre**, **apellidos**: Información personal del cliente.
   - **email** (no incluido en el script proporcionado).
   - **telefono**: Número telefónico del cliente.
   - **direccion**: Dirección de entrega del cliente.
   - **ciudad**: Ciudad donde reside o trabaja el cliente.
   - **pais**: País del cliente.
   - **codigo_postal**: Código postal asociado a la dirección del cliente.

2. **productos**:
   - **Identificador**: Clave primaria autoincremental.
   - **nombre**, **descripcion**: Detalles sobre el producto.
   - **precio**, **peso**: Precio y peso del producto en kilogramos.

3. **pedidos**:
   - **fecha**: Fecha de creación del pedido.
   - **id_cliente**: Clave foránea que referencia a la tabla `clientes`.
   - **id_producto**: Clave foránea que referencia a la tabla `productos`.

4. **pedidosconlineas**:
   - **Identificador**: Clave primaria autoincremental.
   - **fecha**, **id_cliente**: Detalles del pedido, con una clave foránea que se relaciona con los clientes.

5. **vista_pedidos**:
   - Es una vista que combina información de varias tablas para proporcionar un resumen detallado de los pedidos incluyendo el nombre y apellidos del cliente, el nombre del producto, su precio, IVA y total.

### Vista

- **vista_pedidos**: 
  - Esta vista se utiliza para visualizar la relación entre `pedidos`, `clientes` y `productos`. La consulta muestra la fecha del pedido, los datos del cliente (nombre y apellidos), el nombre del producto y sus detalles financieros incluyendo precio, IVA y total.

### Ejemplos de Uso

1. **Insertar un nuevo cliente**:
   ```sql
   INSERT INTO clientes (nombre, apellidos, email, telefono, direccion, ciudad, pais, codigo_postal) 
   VALUES ('Juan', 'Pérez', 'juan@example.com', '555-1234', 'Calle Principal 123', 'Ciudad de México', 'México', '06100');
   ```

2. **Insertar un nuevo producto**:
   ```sql
   INSERT INTO productos (nombre, descripcion, precio, peso) 
   VALUES ('Portátil HP ProBook 450 G8', 'Laptop empresarial de 14 pulgadas con procesador AMD y 8GB RAM.', 949.99, 1.60);
   ```

3. **Consultar la vista para obtener detalles de un pedido específico**:
   ```sql
   SELECT * FROM vista_pedidos WHERE fecha = '2025-09-09';
   ```

### Consideraciones Adicionales

- El script está diseñado para una base de datos que maneja información sobre clientes, productos y pedidos. 
- La tabla `vista_pedidos` proporciona un resumen útil y se puede utilizar en consultas SQL para obtener rápidamente información sobre los pedidos.
- Se recomienda verificar y ajustar la configuración de las restricciones de clave foránea según sea necesario.

Este esquema de base de datos proporciona una estructura sólida para un sistema que maneja ventas de productos, incluyendo el seguimiento de clientes y detalles de los pedidos.

`copia_de_seguridad.sql`

```sql
-- MySQL dump 10.13  Distrib 8.0.43, for Linux (x86_64)
--
-- Host: localhost    Database: empresarial
-- ------------------------------------------------------
-- Server version	8.0.43-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `Identificador` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `apellidos` varchar(100) DEFAULT NULL,
  `telefono` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `localidad` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`Identificador`),
  CONSTRAINT `chk_email_format` CHECK (regexp_like(`email`,_utf8mb4'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$')),
  CONSTRAINT `chk_telefono_length` CHECK ((char_length(`telefono`) = 9))
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'Carlos','García López','612345678','carlos.garcia@example.com','Valencia'),(2,'María','Martínez Fernández','623456789','maria.martinez@example.com','Valencia'),(3,'José','Rodríguez Sánchez','634567890','jose.rodriguez@example.com','Madrid'),(4,'Laura','Gómez Díaz','645678901','laura.gomez@example.com','Madrid'),(5,'Antonio','Fernández Ruiz','656789012','antonio.fernandez@example.com','Madrid'),(6,'Ana','López Jiménez','667890123','ana.lopez@example.com','Valencia'),(7,'Francisco','Díaz Moreno','678901234','francisco.diaz@example.com','Madrid'),(8,'Lucía','Ruiz Hernández','689012345','lucia.ruiz@example.com','Madrid'),(9,'David','Sánchez Torres','690123456','david.sanchez@example.com','Valencia'),(10,'Elena','Romero Ramos','601234567','elena.romero@example.com','Madrid'),(11,'Manuel','Navarro Ortega','602345678','manuel.navarro@example.com','Madrid'),(13,'Pedro','Rubio Molina','604567890','pedro.rubio@example.com','Madrid'),(14,'Sara','Ortega Serrano','605678901','sara.ortega@example.com','Valencia'),(15,'Javier','Morales Gil','606789012','javier.morales@example.com','Madrid'),(16,'Beatriz','Hernández Cruz','607890123','beatriz.hernandez@example.com','Madrid'),(17,'Miguel','Torres León','608901234','miguel.torres@example.com','Valencia'),(18,'Carmen','Domínguez Flores','609012345','carmen.dominguez@example.com','Madrid'),(19,'Raúl','Vargas Castillo','611223344','raul.vargas@example.com','Valencia'),(20,'Patricia','Santos Delgado','622334455','patricia.santos@example.com','Madrid'),(22,'Nombre del nuevo cliente','Apellidos del nuevo cliente',NULL,NULL,NULL),(25,'Jose Vicente','Carratala','620891718','info@jocarsa.com','Valencia');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lineaspedido`
--

DROP TABLE IF EXISTS `lineaspedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lineaspedido` (
  `Identificador` int NOT NULL AUTO_INCREMENT,
  `producto_id` int NOT NULL,
  `unidades` int NOT NULL,
  `pedidos_id` int NOT NULL,
  PRIMARY KEY (`Identificador`),
  KEY `lineapedidoapedido` (`pedidos_id`),
  KEY `lineaspedidoaproductos` (`producto_id`),
  CONSTRAINT `lineapedidoapedido` FOREIGN KEY (`pedidos_id`) REFERENCES `pedidosconlineas` (`Identificador`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `lineaspedidoaproductos` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`Identificador`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lineaspedido`
--

LOCK TABLES `lineaspedido` WRITE;
/*!40000 ALTER TABLE `lineaspedido` DISABLE KEYS */;
/*!40000 ALTER TABLE `lineaspedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `Identificador` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `id_cliente` int NOT NULL,
  `id_producto` int NOT NULL,
  PRIMARY KEY (`Identificador`),
  KEY `pedidosaclientes` (`id_cliente`),
  KEY `pedidosaproductos` (`id_producto`),
  CONSTRAINT `pedidosaclientes` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`Identificador`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `pedidosaproductos` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`Identificador`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (2,'2025-09-26',1,4),(3,'2025-09-09',2,18),(4,'2025-09-17',7,11);
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidosconlineas`
--

DROP TABLE IF EXISTS `pedidosconlineas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidosconlineas` (
  `Identificador` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `id_cliente` int NOT NULL,
  PRIMARY KEY (`Identificador`),
  KEY `pedidosaclientes2` (`id_cliente`),
  CONSTRAINT `pedidosaclientes2` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`Identificador`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidosconlineas`
--

LOCK TABLES `pedidosconlineas` WRITE;
/*!40000 ALTER TABLE `pedidosconlineas` DISABLE KEYS */;
/*!40000 ALTER TABLE `pedidosconlineas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `Identificador` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text NOT NULL,
  `precio` double(10,2) NOT NULL,
  `peso` double(10,2) NOT NULL,
  PRIMARY KEY (`Identificador`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'Portátil Lenovo ThinkPad E14','Portátil empresarial de 14 pulgadas con procesador Intel i5 y 16GB RAM.',899.99,1.50),(2,'Smartphone Samsung Galaxy S24','Teléfono inteligente con pantalla AMOLED de 6.5 pulgadas y 128GB de memoria.',1099.00,0.18),(3,'Auriculares Sony WH-1000XM5','Auriculares inalámbricos con cancelación activa de ruido.',349.99,0.25),(4,'Impresora HP LaserJet Pro M404','Impresora láser monocromo rápida y compacta.',229.50,7.60),(5,'Monitor LG UltraWide 34\"','Monitor ultrapanorámico de 34 pulgadas con resolución QHD.',599.90,6.80),(6,'Teclado Logitech MX Keys','Teclado inalámbrico retroiluminado con teclas silenciosas.',119.00,0.80),(7,'Ratón Logitech MX Master 3S','Ratón inalámbrico ergonómico con precisión avanzada.',99.99,0.14),(8,'Disco SSD Samsung 1TB','Unidad de estado sólido NVMe PCIe Gen4 de 1TB.',139.90,0.05),(9,'Servidor Dell PowerEdge T40','Servidor torre para pymes con Intel Xeon.',1150.00,11.20),(10,'Tablet Apple iPad 10.2\"','Tablet de 10.2 pulgadas con 64GB de almacenamiento.',429.00,0.49),(11,'Cámara Canon EOS 250D','Cámara réflex digital con lente 18-55mm.',639.00,0.90),(12,'Proyector Epson EB-S41','Proyector SVGA de 3300 lúmenes para presentaciones.',299.00,2.50),(13,'Silla ergonómica Hbada','Silla de oficina ergonómica con soporte lumbar.',199.99,13.00),(14,'Disco Duro Externo WD 2TB','Disco duro externo portátil con conexión USB 3.0.',79.90,0.23),(15,'Router ASUS RT-AX88U','Router WiFi 6 de alto rendimiento con 8 puertos LAN.',289.00,1.00),(16,'Smartwatch Garmin Forerunner 255','Reloj inteligente multideporte con GPS integrado.',349.90,0.12),(17,'Altavoz JBL Charge 5','Altavoz Bluetooth portátil resistente al agua.',179.00,0.95),(18,'Microondas Samsung MG23','Microondas con grill de 23 litros.',145.00,13.00),(19,'Cafetera Nespresso Essenza Mini','Cafetera de cápsulas compacta y rápida.',89.00,2.30),(20,'Dispositivo NAS Synology DS220+','Servidor NAS de 2 bahías para uso doméstico o empresarial.',329.00,1.30);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vista_pedidos`
--

DROP TABLE IF EXISTS `vista_pedidos`;
/*!50001 DROP VIEW IF EXISTS `vista_pedidos`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_pedidos` AS SELECT 
 1 AS `fecha`,
 1 AS `nombre de cliente`,
 1 AS `apellidos`,
 1 AS `nombre de producto`,
 1 AS `precio`,
 1 AS `IVA`,
 1 AS `Total`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vista_pedidos`
--

/*!50001 DROP VIEW IF EXISTS `vista_pedidos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_pedidos` AS select `pedidos`.`fecha` AS `fecha`,`clientes`.`nombre` AS `nombre de cliente`,`clientes`.`apellidos` AS `apellidos`,`productos`.`nombre` AS `nombre de producto`,`productos`.`precio` AS `precio`,(`productos`.`precio` * 0.16) AS `IVA`,(`productos`.`precio` * 1.16) AS `Total` from ((`pedidos` left join `clientes` on((`pedidos`.`id_cliente` = `clientes`.`Identificador`))) left join `productos` on((`pedidos`.`id_producto` = `productos`.`Identificador`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-02 17:04:33
```

### Actividades propuestas

Tu script de Python está bien diseñado para realizar una copia de seguridad del esquema y los datos de tu base de datos MySQL en formato SQL. Aquí te proporciono un resumen y algunas sugerencias adicionales:

### Resumen del Script
1. **Conexión a la Base de Datos**: Conecta al servidor MySQL usando las credenciales especificadas.
2. **Obtener Nombres de Bases de Datos**: Crea una lista de nombres de bases de datos que no sean "information_schema", "performance_schema" ni "mysql".
3. **Copia de Seguridad del Esquema**: Genera la definición SQL de los esquemas (tablas, vistas, etc.) para cada base de datos.
4. **Copia de Seguridad de Datos**: Genera una copia de seguridad de los datos insertados en las tablas.

### Sugerencias Adicionales
1. **Manejo de Excepciones**: Añade manejo de excepciones (`try-except`) para capturar errores durante la conexión a la base de datos y el proceso de backup.
2. **Logging**: Implementa un sistema de registro (logging) para documentar eventos importantes durante la ejecución del script, como inicio y finalización del backup, o cualquier error que pueda surgir.
3. **Comprimir Archivos SQL**: Los archivos SQL generados pueden ser grandes. Considera comprimir estos archivos utilizando gzip para ahorrar espacio en disco.

### Ejemplo de Mejora con Logging y Manejo de Excepciones

```python
import mysql.connector
from mysql.connector import Error
import logging
import gzip
import os

# Configuración del registro
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s:%(levelname)s: %(message)s')

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password'
        )
        logging.info('Conexión a la base de datos exitosa')
        return connection
    except Error as e:
        logging.error(f'Error al conectarse a MySQL: {e}')
        raise

def dump_database(connection, database_name):
    try:
        dump_query = f"mysqldump --compact -u root -ppassword {database_name} > /home/user/backup/{database_name}_schema.sql"
        os.system(dump_query)
        
        data_dump_query = f"mysqldump --no-create-info -u root -ppassword {database_name} > /home/user/backup/{database_name}_data.sql"
        os.system(data_dump_query)

        logging.info(f'Backup de esquema y datos para la base de datos {database_name} completado')
        
    except Exception as e:
        logging.error(f'Error al realizar el backup para la base de datos {database_name}: {e}')
    
def compress_files(connection, database_name):
    try:
        schema_file = f"/home/user/backup/{database_name}_schema.sql"
        data_file = f"/home/user/backup/{database_name}_data.sql"
        
        with open(schema_file, 'rb') as f_in:
            with gzip.open(f"{schema_file}.gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                
        with open(data_file, 'rb') as f_in:
            with gzip.open(f"{data_file}.gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        logging.info(f'Archivos comprimidos para la base de datos {database_name}')
    except Exception as e:
        logging.error(f'Error al comprimir archivos para la base de datos {database_name}: {e}')

def main():
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Obtener nombres de bases de datos
        query = "SHOW DATABASES"
        cursor.execute(query)
        databases = [db[0] for db in cursor if db[0] not in ('information_schema', 'performance_schema', 'mysql')]

        for database in databases:
            dump_database(connection, database)
        
        # Comprimir archivos SQL
        for database in databases:
            compress_files(connection, database)

    except Error as e:
        logging.error(f'Error general en el script: {e}')
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main()
```

### Explicación de Mejoras
1. **Logging**: Se usa `logging` para registrar eventos importantes.
2. **Manejo de Excepciones**: Las excepciones capturadas se registran en el archivo de registro y pueden ser revisadas posteriormente.
3. **Comprimir Archivos SQL**: Los archivos generados son comprimidos usando gzip, lo que reduce significativamente el espacio necesario.

Estas mejoras ayudarán a hacer tu script más robusto y fácil de mantener.


<a id="subconsultas-y-composiciones-en-ordenes-de-edicion"></a>
## Subconsultas y composiciones en órdenes de edición

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/004-Tratamiento%20de%20datos/003-Subconsultas%20y%20composiciones%20en%20%C3%B3rdenes%20de%20edici%C3%B3n)

### Introducción a los ejercicios

Esta carpeta contiene una serie de ejercicios prácticos diseñados para familiarizarte con el uso del almacenamiento local en JavaScript, específicamente enfocándose en la manipulación y gestión de datos a través del objeto `localStorage`. Los ejercicios comienzan con la simple adición de un dato básico al almacenamiento y evolucionan hasta incluir la manipulación de objetos complejos y su serialización/deserialización utilizando JSON. A lo largo de estos ejercicios, practicarás competencias clave como el manejo de estructuras de datos en JavaScript, la persistencia de información en el navegador y la conversión entre tipos de datos para almacenamiento eficiente.

### localstorage
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código HTML es muy simple y tiene como objetivo guardar un dato en el almacenamiento local del navegador web. La página contiene únicamente un script que utiliza la API `localStorage` para guardar una clave-valor en el navegador. En este caso, guarda el nombre "Jose Vicente" bajo la clave "minombre". Esto significa que cada vez que un usuario visite esta página y su navegador soporte localStorage, se guardará automáticamente el dato "Jose Vicente" con la etiqueta "minombre", lo cual puede ser útil para mantener datos entre diferentes visitas del sitio sin necesidad de una base de datos o servidores. Es importante destacar que este tipo de almacenamiento es local al navegador y no está disponible en otros navegadores o dispositivos, a menos que el usuario copie manualmente los datos usando técnicas específicas del navegador.

Este fragmento de código sirve como introducción a cómo guardar datos persistentes utilizando JavaScript dentro de una página web, permitiendo a las aplicaciones web recordar información del usuario incluso después de cerrar y abrir nuevamente la página.

`001-localstorage.html`

```html
<!doctype html>
<html lang="es">
  <head>
    <title>
      Local Storage
    </title>
  </head>
  <body>
    <script>
      localStorage.setItem("minombre","Jose Vicente")
    </script>
  </body>
</html>
```

### recuperar datos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es una página HTML básica que incluye un script en la etiqueta `<script>` dentro del cuerpo (`<body>`) de la página. El propósito principal es imprimir en el "web console" (la consola del navegador) el valor almacenado previamente en `localStorage` con la clave `"minombre"`.

En específico, la línea `console.log(localStorage.getItem("minombre"));` hace uso del objeto `localStorage`, que permite guardar datos de texto simple en el navegador del usuario para su recuperación posterior. La función `getItem()` es llamada sobre `localStorage`, y le proporciona como argumento una cadena `"minombre"`. Esto significa que el código busca un dato previamente guardado con la etiqueta `"minombre"` y lo muestra en la consola del navegador.

Este tipo de código es importante porque permite persistir datos entre diferentes sesiones o visitas al sitio web, sin necesidad de guardar información en un servidor. Es una forma sencilla y útil para recordar detalles específicos sobre el usuario mientras navega por tu página web.

`002-recuperar datos.html`

```html
<!doctype html>
<html lang="es">
  <head>
    <title>
      Local Storage
    </title>
  </head>
  <body>
    <script>
      console.log(localStorage.getItem("minombre"));
    </script>
  </body>
</html>
```

### guardar datos complejos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código HTML es un ejemplo simple que muestra cómo almacenar datos complejos, como objetos JavaScript, en el almacenamiento local del navegador web. En la parte central del documento, se define un objeto JavaScript llamado `mis_datos` que contiene información personal de una persona, incluyendo nombre, apellidos y correo electrónico.

Luego, mediante la función `localStorage.setItem()`, este objeto es guardado en el almacenamiento local del navegador con la clave "mis_datos". Esto significa que los datos pueden ser recuperados más tarde incluso después de que el usuario haya cerrado y vuelto a abrir su navegador. Esta característica es muy útil para aplicaciones web que necesitan mantener información entre diferentes sesiones del navegador.

El uso de `localStorage` permite a las páginas web almacenar pequeñas cantidades de datos en forma persistente, lo cual es importante para mejorar la experiencia del usuario al no tener que introducir siempre los mismos datos cada vez que visitan una página.

`003-guardar datos complejos.html`

```html
<!doctype html>
<html lang="es">
  <head>
    <title>
      Local Storage
    </title>
  </head>
  <body>
    <script>
      var mis_datos = {
        "nombre":"Jose Vicente",
        "apellidos":"Carratala Sanchis",
        "email":"info@jocarsa.com"
      };
      localStorage.setItem("mis_datos",mis_datos);
    </script>
  </body>
</html>
```

### convertir objeto a cadena
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código HTML contiene un bloque de script que realiza tres operaciones principales: crea un objeto JavaScript llamado `mis_datos`, convierte este objeto a una cadena JSON y luego almacena la cadena resultante en el almacenamiento local del navegador.

Primero, se define un objeto llamado `mis_datos` que tiene tres propiedades: "nombre", "apellidos" e "email". Cada propiedad contiene información personal sobre una persona. Luego, se utiliza la función `JSON.stringify()` para convertir este objeto JavaScript en una cadena JSON, que es básicamente una versión de texto del objeto que puede ser guardada y recuperada fácilmente.

Finalmente, esta cadena JSON se almacena en el almacenamiento local del navegador usando `localStorage.setItem()`. Esto permite guardar los datos de forma persistente, es decir, incluso después de cerrar la página web o reiniciar el navegador, los datos seguirán estando disponibles. El primer argumento "mis_datos" es el nombre que identifica este dato guardado en el almacenamiento local, y `cadena_json` es el valor que se guarda bajo ese nombre.

Este código es importante porque demuestra cómo guardar objetos complejos en el navegador para uso futuro, lo cual es útil cuando se trabaja con aplicaciones web que necesitan mantener información del usuario entre diferentes visitas o sesiones.

`004-convertir objeto a cadena.html`

```html
<!doctype html>
<html lang="es">
  <head>
    <title>
      Local Storage
    </title>
  </head>
  <body>
    <script>
      var mis_datos = {
        "nombre":"Jose Vicente",
        "apellidos":"Carratala Sanchis",
        "email":"info@jocarsa.com"
      };
      var cadena_json = JSON.stringify(mis_datos);
      localStorage.setItem("mis_datos",cadena_json);
    </script>
  </body>
</html>
```

### recuperar un objeto complejo
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código HTML es una página web muy sencilla que tiene como objetivo mostrar cómo recuperar datos almacenados previamente en el navegador del usuario utilizando la API `localStorage`. La página no hace nada más que cargar y luego, mediante un script incorporado, usar el método `getItem` de `localStorage` para obtener información almacenada con la clave "mis_datos". Este dato es después mostrado en la consola del navegador (donde puedes verlo si abres las herramientas de desarrollo del navegador).

Es importante destacar que este código asume que ya se ha guardado algo bajo el nombre "mis_datos" en `localStorage`. Si no hay ningún dato almacenado con ese nombre, `getItem` devolverá `null`.

Esta técnica es útil para recordar la configuración o los datos importantes entre diferentes sesiones de navegación sin tener que enviarlos al servidor cada vez.

`005-recuperar un objeto complejo.html`

```html
<!doctype html>
<html lang="es">
  <head>
    <title>
      Local Storage
    </title>
  </head>
  <body>
    <script>
   
      console.log(localStorage.getItem("mis_datos"));
    </script>
  </body>
</html>
```

### convertir string a objeto
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código HTML muestra cómo recuperar un objeto almacenado en el navegador web utilizando la API Web Storage. En particular, se está utilizando `localStorage` para acceder a datos previamente guardados bajo la clave `"mis_datos"`. La función `JSON.parse()` es utilizada para convertir una cadena de texto almacenada en `localStorage` de vuelta a un objeto JavaScript original.

El código dentro del `<script>` etiqueta primero recupera los datos almacenados usando `localStorage.getItem("mis_datos")`, lo que devolverá la información como una cadena de texto. Luego, `JSON.parse()` toma esa cadena y la convierte en un objeto JSON real, lo cual es necesario si queremos trabajar con los datos recuperados como objetos regulares en JavaScript.

Este proceso es crucial cuando necesitas guardar estados complejos o estructuras de datos entre sesiones del navegador para aplicaciones web.

`006-convertir string a objeto.html`

```html
<!doctype html>
<html lang="es">
  <head>
    <title>
      Local Storage
    </title>
  </head>
  <body>
    <script>
      console.log(JSON.parse(localStorage.getItem("mis_datos")));
    </script>
  </body>
</html>
```

### Actividades propuestas

1. **Introducción a Local Storage**
   - **Descripción:** Los estudiantes deben familiarizarse con el uso básico de `localStorage` para guardar datos simples y recuperarlos.
   - **Objetivo:** Aprender cómo almacenar e imprimir datos en la consola usando local storage.

2. **Almacenamiento de Datos Simples**
   - **Descripción:** Se les pedirá a los estudiantes que escriban un código similar al del archivo `001-localstorage.html` pero guardando sus propios datos personales.
   - **Objetivo:** Practicar la inserción y recuperación de datos simples en local storage.

3. **Recuperación de Datos Simples**
   - **Descripción:** Los alumnos deben modificar el código del archivo `002-recuperar datos.html` para mostrar un dato almacenado previamente.
   - **Objetivo:** Aprender a recuperar y visualizar información almacenada en local storage.

4. **Guardado de Datos Complejos**
   - **Descripción:** Los estudiantes deben modificar el archivo `003-guardar datos complejos.html` para guardar un objeto con más campos (como dirección, teléfono).
   - **Objetivo:** Familiarizarse con la estructura JSON y almacenamiento de objetos en local storage.

5. **Conversión de Objeto a Cadena**
   - **Descripción:** Se les pedirá a los estudiantes que adapten el código del archivo `004-convertir objeto a cadena.html` para incluir más campos en el objeto antes de guardar.
   - **Objetivo:** Aprender a convertir objetos JSON a cadenas y almacenarlos.

6. **Recuperación de Datos Complejos**
   - **Descripción:** Los alumnos deben modificar el código del archivo `005-recuperar un objeto complejo.html` para recuperar datos de un objeto más completo.
   - **Objetivo:** Aprender a trabajar con objetos JSON almacenados y mostrar sus datos en la consola.

7. **Conversión de String a Objeto**
   - **Descripción:** Los estudiantes deben adaptar el archivo `006-convertir string a objeto.html` para manejar strings más complejos provenientes del local storage.
   - **Objetivo:** Practicar la conversión de cadenas en objetos JSON y su visualización.

8. **Integración Completa**
   - **Descripción:** Se les pide que combinen los ejercicios anteriores para crear una aplicación sencilla que permita guardar datos personales (nombre, apellidos, email), recuperarlos y mostrarlos en la consola.
   - **Objetivo:** Aprender a integrar todos los conceptos de local storage, JSON y manipulación de objetos.

Estas actividades están diseñadas para llevar a los estudiantes gradualmente desde el manejo básico de `localStorage` hasta técnicas más avanzadas de almacenamiento y recuperación de datos complejos.


<a id="transacciones"></a>
## Transacciones

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/004-Tratamiento%20de%20datos/004-Transacciones)

### Introducción a los ejercicios

El script SQL proporcionado realiza una serie de inserciones en varias tablas para crear datos iniciales en un esquema de base de datos que parece representar el flujo de trabajo típico de una tienda online o minorista. Veamos cómo está estructurado y qué hace:

1. **Tablas Involucradas**:
   - `categorias`
   - `clientes`
   - `productos`
   - `pedidos`
   - `lineas_pedido`
   - `gestion_stock`

2. **Inserción de Datos en Categorías**:
   ```
   INSERT INTO categorias (id_categoria, nombre) VALUES
   ('1', 'Electrónica'),
   ('2', 'Libros'),
   ('3', 'Ropa');
   ```

3. **Inserción de Datos en Clientes**:
   ```
   INSERT INTO clientes (id_cliente, nombre, email, direccion_envio, direccion_facturacion) VALUES
   ('1', 'Ana García', 'ana.garcia@example.com', 'Calle Falsa 123, Madrid', 'Calle Falsa 123, Madrid'),
   ('2', 'Luis Martínez', 'luis.martinez@example.com', 'Avenida Real 456, Barcelona', 'Avenida Real 456, Barcelona'),
   ('3', 'Marta López', 'marta.lopez@example.com', 'Plaza Mayor 789, Sevilla', 'Plaza Mayor 789, Sevilla');
   ```

4. **Inserción de Datos en Productos**:
   ```
   INSERT INTO productos (id_producto, nombre, descripcion, id_categoria, precio_venta, stock) VALUES
   ('1', 'Portátil 14"', 'Ordenador portátil con pantalla de 14 pulgadas.', '1', 600.00, 5),
   ('2', 'Ratón inalámbrico', 'Ratón para ordenadores sin necesidad de cable.', '1', 20.00, 20),
   ('3', 'Libro Aprende Python', 'Guía completa para aprender a programar en Python.', '2', 30.00, 15),
   ('4', 'Libro HTML y CSS', 'Tutoriales sobre diseño web con HTML y CSS.', '2', 25.00, 18),
   ('5', 'Camiseta básica', 'Camiseta de algodón para hombre o mujer.', '3', 15.00, 25),
   ('6', 'Sudadera con capucha', 'Ropa de abrigo para frío intenso.', '3', 40.00, 12),
   ('7', 'Lámpara de escritorio', 'Lámpara de mesa LED regulable.', '1', 35.00, 8),
   ('8', 'Taza de café', 'Taza elegante para tomar tu café favorito.', '1', 8.00, 30);
   ```

5. **Inserción de Datos en Pedidos**:
   ```
   INSERT INTO pedidos (id_pedido, id_cliente, fecha_pedido, estado, total_bruto, total_impuestos, total, observaciones) VALUES
   ('1', '1', '2025-01-10 10:30:00', 'pagado', 640.00, 134.40, 774.40, 'Compra online paga con tarjeta'),
   ('2', '2', '2025-01-12 16:45:00', 'enviado', 71.00, 14.91, 85.91, 'Envío por mensajería 24h'),
   ('3', '3', '2025-01-15 09:15:00', 'pagado', 85.00, 17.85, 102.85, 'Pedido recogida en tienda'),
   ('4', '1', '2025-01-20 18:20:00', 'pendiente', 635.00, 133.35, 768.35, 'Pendiente de pago por transferencia');
   ```

6. **Inserción de Datos en Líneas de Pedido**:
   ```
   INSERT INTO lineas_pedido (id_pedido, id_producto, cantidad, precio_unitario, impuesto_porcentaje, total_linea) VALUES
   ('1', '1', 1, 600.00, 21.00, 726.00),
   ('1', '2', 2, 20.00, 21.00, 48.40),
   ('2', '3', 1, 30.00, 21.00, 36.30),
   ('2', '4', 1, 25.00, 21.00, 30.25),
   ('2', '8', 2, 8.00, 21.00, 19.36),
   ('3', '5', 3, 15.00, 21.00, 54.45),
   ('3', '6', 1, 40.00, 21.00, 48.40),
   ('4', '7', 1, 35.00, 21.00, 42.35),
   ('4', '1', 1, 600.00, 21.00, 726.00);
   ```

7. **Gestión del Stock**:
   ```
   INSERT INTO gestion_stock (id_producto, tipo_movimiento, cantidad, referencia, observaciones) VALUES
   ('1', 'salida', 1, 'Pedido #1', 'Venta al cliente Ana García'),
   ('2', 'salida', 2, 'Pedido #1', 'Venta al cliente Ana García'),
   ('3', 'salida', 1, 'Pedido #2', 'Venta al cliente Luis Martínez'),
   ('4', 'salida', 1, 'Pedido #2', 'Venta al cliente Luis Martínez'),
   ('8', 'salida', 2, 'Pedido #2', 'Venta al cliente Luis Martínez'),
   ('5', 'salida', 3, 'Pedido #3', 'Venta al cliente Marta López'),
   ('6', 'salida', 1, 'Pedido #3', 'Venta al cliente Marta López'),
   ('7', 'salida', 1, 'Pedido #4', 'Venta al cliente Ana García'),
   ('1', 'salida', 1, 'Pedido #4', 'Venta al cliente Ana García');
   ```

Este script se asegura de que todas las relaciones entre las tablas estén correctamente definidas y vinculadas. Por ejemplo:

- Cada producto está asociado a una categoría.
- Cada pedido tiene un cliente asociado.
- Cada línea de pedido pertenece a un pedido específico y a un producto en particular.

Además, se calculan los totales (bruto e impuestos) para cada línea del pedido y para el pedido completo. Esto es crucial para asegurar la consistencia de los datos y facilitar las operaciones de consulta posteriormente.

Este conjunto de inserciones proporciona una base sólida para pruebas de integración, desarrollo y depuración en un sistema de comercio electrónico o minorista.

### tienda online
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este texto no es código SQL, sino una descripción en lenguaje natural del diseño de la base de datos y algunas de sus tablas. El objetivo principal es crear una estructura de base de datos para una tienda online que incluya varias entidades relacionadas entre sí, como productos, categorías, pedidos, líneas de pedido y clientes.

La idea es generar los comandos `CREATE TABLE` necesarios para definir estas tablas en MySQL, asegurando que las llaves primarias (PK) y foráneas (FK) estén correctamente establecidas según la relación entre cada tabla. Además, se menciona la creación de vistas (`VIEW`) en SQL que ayudarán a unir estos datos de manera más legible y útil para los usuarios del sistema.

Crear estas tablas y vistas es crucial porque permitirá a la tienda online gestionar eficazmente sus productos, pedidos, clientes y el stock, facilitando consultas complejas con una base de datos bien estructurada.

`001-tienda online.sql`

```sql
Quiero crear la base de datos MySQL de una tienda online, que tendrá (PK en cada tabla):
-Productos
-Categorias (FK desde productos a categorías)
-Pedidos (FK a clientes)
-Lineas de pedido (FK a pedidos y a productos)
-Clientes
-Gestión del stock (FK a productos)

Quiero obtener los sql create table para darle forma a esta tabla
Quieo crear todas las vistas que sea necesario para unir todos los FK de la base de datos de forma humanamente entendible (tantas views como sea necesario)
```

### crear la basededatos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para crear una nueva base de datos en un servidor MySQL y seleccionarla para su uso posterior. Primero, el comando `sudo mysql -u root -p` abre la terminal del programa MySQL con permisos de administrador (root) y te pedirá que introduzcas tu contraseña para acceder.

Luego, el comando `CREATE DATABASE tiendaonline2526;` crea una nueva base de datos llamada "tiendaonline2526". Esta acción es crucial porque esta base de datos albergará toda la información relacionada con un sistema o aplicación, como por ejemplo un sitio web de compras online.

Finalmente, el comando `USE tiendaonline2526;` selecciona la base de datos recién creada para que puedan ejecutarse consultas y operaciones en ella. Es importante hacer esto antes de comenzar a crear tablas, insertar datos o realizar cualquier otra acción dentro de esta base de datos específica.

Este proceso es fundamental en el desarrollo de bases de datos porque permite organizar la información de manera estructurada y asegura que los datos no se mezclen con otros proyectos o sistemas.

`002-crear la basededatos.sql`

```sql
sudo mysql -u root -p

CREATE DATABASE tiendaonline2526;

USE tiendaonline2526;
```

### crear tablas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL crea una serie de tablas que representan diferentes aspectos del manejo de una tienda en línea, como categorías de productos, clientes, productos mismos, pedidos y movimientos de stock. Cada tabla tiene sus propias columnas y restricciones para asegurar la integridad de los datos.

1. **Tabla `CATEGORIAS`**: Almacena información sobre las diferentes categorías en las que se pueden agrupar los productos. Contiene campos como el nombre, descripción y un campo `id_categoria` que es único e incrementa automáticamente. También tiene una restricción única para asegurar que cada categoría tenga un nombre único.

2. **Tabla `CLIENTES`**: Almacena información de contacto de los clientes con campos tales como nombre, apellidos, email y otros detalles. Incluye una restricción única en el campo `email`, lo cual es importante para evitar duplicados.

3. **Tabla `PRODUCTOS`**: Guarda datos específicos sobre cada producto, incluyendo su categoría (con una clave foránea a la tabla `CATEGORIAS`), nombre, descripción, precio y otros detalles. Hay restricciones que aseguran integridad referencial entre productos y sus categorías, así como un índice único en el campo SKU para garantizar que cada producto tenga un identificador de stock único.

4. **Tabla `PEDIDOS`**: Registra los pedidos realizados por los clientes, con detalles sobre el cliente (clave foránea a la tabla `CLIENTES`) y estado del pedido. Incluye columnas para total bruto e impuestos, y varios índices para mejorar las consultas.

5. **Tabla `GESTION_STOCK`**: Documenta cambios en el stock de productos, indicando si es una entrada o salida, cantidad afectada, y detalles adicionales sobre la transacción.

6. **Tabla `LINEAS_PEDIDO`**: Almacena los detalles específicos de cada línea dentro de un pedido, relacionándola con tanto el pedido como el producto involucrado (con claves foráneas). Esto permite rastrear qué productos fueron pedidos en qué cantidad y al qué precio.

Estas tablas proporcionan una estructura sólida para administrar la información de una tienda online, asegurando que los datos sean precisos e integrales a través de las restricciones y referencias foráneas implementadas.

`003-crear tablas.sql`

```sql
-- ============================
-- 1) Tabla CATEGORIAS
-- ============================
CREATE TABLE categorias (
    id_categoria      INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre            VARCHAR(100) NOT NULL,
    descripcion       TEXT NULL,
    activa            TINYINT(1) NOT NULL DEFAULT 1,
    fecha_creacion    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT uq_categorias_nombre UNIQUE (nombre)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ============================
-- 2) Tabla CLIENTES
-- ============================
CREATE TABLE clientes (
    id_cliente        INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre            VARCHAR(100) NOT NULL,
    apellidos         VARCHAR(150) NOT NULL,
    email             VARCHAR(150) NOT NULL,
    telefono          VARCHAR(30),
    direccion         VARCHAR(255),
    cp                VARCHAR(10),
    ciudad            VARCHAR(100),
    provincia         VARCHAR(100),
    pais              VARCHAR(100),
    fecha_registro    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    activo            TINYINT(1) NOT NULL DEFAULT 1,
    
    CONSTRAINT uq_clientes_email UNIQUE (email)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ============================
-- 3) Tabla PRODUCTOS
-- ============================
CREATE TABLE productos (
    id_producto       INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_categoria      INT UNSIGNED NOT NULL,
    nombre            VARCHAR(150) NOT NULL,
    descripcion       TEXT,
    sku               VARCHAR(50),
    precio            DECIMAL(10,2) NOT NULL,
    impuesto_porcentaje DECIMAL(5,2) NOT NULL DEFAULT 21.00, -- % IVA, por ejemplo
    activo            TINYINT(1) NOT NULL DEFAULT 1,
    fecha_alta        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_productos_categorias
        FOREIGN KEY (id_categoria)
        REFERENCES categorias (id_categoria)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
        
    CONSTRAINT uq_productos_sku UNIQUE (sku),
    INDEX idx_productos_categoria (id_categoria),
    INDEX idx_productos_nombre (nombre)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ============================
-- 4) Tabla PEDIDOS
-- ============================
CREATE TABLE pedidos (
    id_pedido         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_cliente        INT UNSIGNED NOT NULL,
    fecha_pedido      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado            ENUM('pendiente','pagado','enviado','cancelado','devuelto')
                        NOT NULL DEFAULT 'pendiente',
    total_bruto       DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    total_impuestos   DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    total             DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    observaciones     TEXT,
    
    CONSTRAINT fk_pedidos_clientes
        FOREIGN KEY (id_cliente)
        REFERENCES clientes (id_cliente)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
        
    INDEX idx_pedidos_cliente (id_cliente),
    INDEX idx_pedidos_fecha (fecha_pedido),
    INDEX idx_pedidos_estado (estado)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ============================
-- 5) Tabla GESTION_STOCK
--    (movimientos de stock)
-- ============================
CREATE TABLE gestion_stock (
    id_movimiento     INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_producto       INT UNSIGNED NOT NULL,
    tipo_movimiento   ENUM('entrada','salida','ajuste') NOT NULL,
    cantidad          INT NOT NULL,
    fecha_movimiento  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    referencia        VARCHAR(255) NULL, -- p.ej. "Pedido #123"
    observaciones     TEXT NULL,
    
    CONSTRAINT fk_stock_productos
        FOREIGN KEY (id_producto)
        REFERENCES productos (id_producto)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
        
    INDEX idx_stock_producto (id_producto),
    INDEX idx_stock_fecha (fecha_movimiento),
    INDEX idx_stock_tipo (tipo_movimiento)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ============================
-- 6) Tabla LINEAS_PEDIDO
-- ============================
CREATE TABLE lineas_pedido (
    id_linea_pedido   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_pedido         INT UNSIGNED NOT NULL,
    id_producto       INT UNSIGNED NOT NULL,
    cantidad          INT NOT NULL,
    precio_unitario   DECIMAL(10,2) NOT NULL, -- copia del precio en el momento del pedido
    impuesto_porcentaje DECIMAL(5,2) NOT NULL,
    total_linea       DECIMAL(10,2) NOT NULL,
    
    CONSTRAINT fk_lineas_pedido_pedidos
        FOREIGN KEY (id_pedido)
        REFERENCES pedidos (id_pedido)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
        
    CONSTRAINT fk_lineas_pedido_productos
        FOREIGN KEY (id_producto)
        REFERENCES productos (id_producto)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
        
    INDEX idx_lineas_pedido_pedido (id_pedido),
    INDEX idx_lineas_pedido_producto (id_producto)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;
```

### vistas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está compuesto por seis vistas que se utilizan para simplificar y organizar la información relacionada con un sistema de gestión de inventario y ventas. Cada vista proporciona una visión consolidada de diferentes aspectos del negocio, como productos y categorías, pedidos y clientes, detalles de líneas de pedido, stock actual, resumen de pedidos y movimientos de stock.

La primera vista (`vw_productos_categorias`) combina información sobre productos y sus respectivas categorías, facilitando la consulta de datos relacionados sin necesidad de realizar joins complejos entre las tablas `productos` y `categorias`.

La segunda vista (`vw_pedidos_clientes`) agrupa los detalles de pedidos con los datos de clientes asociados. Esto es útil para generar informes que requieren información tanto sobre el pedido como sobre el cliente.

La tercera vista (`vw_lineas_pedido_detalle`) proporciona un resumen detallado de las líneas individuales en cada pedido, incluyendo información del producto y la categoría a la cual pertenece ese producto. Esta vista es valiosa para análisis de ventas y seguimiento de pedidos específicos.

La cuarta vista (`vw_stock_actual`) calcula el stock actual de productos utilizando transacciones de entrada y salida registradas en la tabla `gestion_stock`. La función COALESCE asegura que, si no hay registros de movimientos de stock, se devuelva un valor predeterminado de 0.

La quinta vista (`vw_pedidos_resumen`) ofrece una visión agregada del total bruto y los impuestos calculados para cada pedido, basándose en la información de las líneas de pedido. Esto es útil para generar resúmenes financieros o informes de ventas detallados.

Finalmente, la sexta vista (`vw_movimientos_stock_detalle`) proporciona detalles sobre los movimientos del stock, incluyendo el tipo de movimiento (entrada/salida/ajuste), la cantidad involucrada y referencias adicionales para rastrear y auditar las transacciones de inventario.

Estas vistas simplifican significativamente la consulta y manipulación de datos en un sistema de gestión de inventarios y ventas, permitiendo a los desarrolladores y administradores acceder fácilmente a informes detallados y resúmenes clave sin tener que escribir consultas SQL complejas.

`004-vistas.sql`

```sql
CREATE OR REPLACE VIEW vw_productos_categorias AS
SELECT
    p.id_producto,
    p.nombre              AS producto,
    p.descripcion         AS descripcion_producto,
    p.sku,
    p.precio,
    p.impuesto_porcentaje,
    p.activo              AS producto_activo,
    c.id_categoria,
    c.nombre              AS categoria,
    c.descripcion         AS descripcion_categoria,
    c.activa              AS categoria_activa
FROM productos p
JOIN categorias c ON p.id_categoria = c.id_categoria;


CREATE OR REPLACE VIEW vw_pedidos_clientes AS
SELECT
    pe.id_pedido,
    pe.fecha_pedido,
    pe.estado,
    pe.total_bruto,
    pe.total_impuestos,
    pe.total,
    cl.id_cliente,
    CONCAT(cl.nombre, ' ', cl.apellidos) AS cliente,
    cl.email,
    cl.telefono,
    cl.ciudad,
    cl.provincia,
    cl.pais
FROM pedidos pe
JOIN clientes cl ON pe.id_cliente = cl.id_cliente;


CREATE OR REPLACE VIEW vw_lineas_pedido_detalle AS
SELECT
    lp.id_linea_pedido,
    -- Pedido
    pe.id_pedido,
    pe.fecha_pedido,
    pe.estado,
    pe.total          AS total_pedido,
    
    -- Cliente
    cl.id_cliente,
    CONCAT(cl.nombre, ' ', cl.apellidos) AS cliente,
    cl.email              AS email_cliente,
    
    -- Producto
    pr.id_producto,
    pr.nombre             AS producto,
    pr.sku,
    pr.precio             AS precio_actual_producto,
    
    -- Categoría
    ca.id_categoria,
    ca.nombre             AS categoria,
    
    -- Datos de la línea
    lp.cantidad,
    lp.precio_unitario,
    lp.impuesto_porcentaje,
    lp.total_linea
FROM lineas_pedido lp
JOIN pedidos pe   ON lp.id_pedido   = pe.id_pedido
JOIN clientes cl  ON pe.id_cliente  = cl.id_cliente
JOIN productos pr ON lp.id_producto = pr.id_producto
JOIN categorias ca ON pr.id_categoria = ca.id_categoria;

CREATE OR REPLACE VIEW vw_stock_actual AS
SELECT
    p.id_producto,
    p.nombre          AS producto,
    p.sku,
    c.id_categoria,
    c.nombre          AS categoria,
    
    COALESCE(SUM(
        CASE
            WHEN gs.tipo_movimiento = 'entrada' THEN gs.cantidad
            WHEN gs.tipo_movimiento = 'salida'  THEN -gs.cantidad
            WHEN gs.tipo_movimiento = 'ajuste'  THEN gs.cantidad
            ELSE 0
        END
    ), 0) AS stock_actual
FROM productos p
LEFT JOIN categorias c    ON p.id_categoria = c.id_categoria
LEFT JOIN gestion_stock gs ON p.id_producto = gs.id_producto
GROUP BY
    p.id_producto,
    p.nombre,
    p.sku,
    c.id_categoria,
    c.nombre;


CREATE OR REPLACE VIEW vw_pedidos_resumen AS
SELECT
    pe.id_pedido,
    pe.fecha_pedido,
    pe.estado,
    cl.id_cliente,
    CONCAT(cl.nombre, ' ', cl.apellidos) AS cliente,
    
    SUM(lp.cantidad * lp.precio_unitario)                   AS total_bruto_calculado,
    SUM(lp.cantidad * lp.precio_unitario * lp.impuesto_porcentaje / 100) AS total_impuestos_calculado,
    SUM(lp.total_linea)                                     AS total_calculado
FROM pedidos pe
JOIN clientes cl  ON pe.id_cliente  = cl.id_cliente
LEFT JOIN lineas_pedido lp ON pe.id_pedido = lp.id_pedido
GROUP BY
    pe.id_pedido,
    pe.fecha_pedido,
    pe.estado,
    cl.id_cliente,
    cliente;

CREATE OR REPLACE VIEW vw_movimientos_stock_detalle AS
SELECT
    gs.id_movimiento,
    gs.fecha_movimiento,
    gs.tipo_movimiento,
    gs.cantidad,
    gs.referencia,
    gs.observaciones,
    p.id_producto,
    p.nombre AS producto,
    p.sku,
    c.id_categoria,
    c.nombre AS categoria
FROM gestion_stock gs
JOIN productos p ON gs.id_producto = p.id_producto
JOIN categorias c ON p.id_categoria = c.id_categoria;
```

### crear nuevo usuario
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para crear un nuevo usuario en una base de datos y otorgarle permisos específicos. Primero, el comando `CREATE USER` crea un usuario llamado 'tiendaonline2526' que puede acceder desde localhost (el mismo servidor) con la contraseña 'tiendaonline2526'. Luego, se le otorgan los privilegios mínimos necesarios con el comando `GRANT USAGE`, lo cual permite al usuario conectarse pero no realiza ninguna acción adicional sobre las bases de datos.

A continuación, el comando `ALTER USER` modifica las características del nuevo usuario para deshabilitar la autenticación basada en host y establecer límites globales para el número de consultas, conexiones y actualizaciones por hora. Finalmente, se conceden todos los privilegios sobre la base de datos 'tiendaonline2526' al usuario recién creado con `GRANT ALL PRIVILEGES`. El comando `FLUSH PRIVILEGES` asegura que los cambios en los permisos del usuario sean aplicados inmediatamente.

Este proceso es crucial para gestionar el acceso a la base de datos, permitiendo a diferentes usuarios realizar tareas específicas según sus necesidades y roles dentro del sistema.

`005-crear nuevo usuario.sql`

```sql
CREATE USER 
'tiendaonline2526'@'localhost' 
IDENTIFIED  BY 'tiendaonline2526';

GRANT USAGE ON *.* TO 'tiendaonline2526'@'localhost';

ALTER USER 'tiendaonline2526'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 
MAX_CONNECTIONS_PER_HOUR 0 
MAX_UPDATES_PER_HOUR 0 
MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON `tiendaonline2526`.* 
TO 'tiendaonline2526'@'localhost';

FLUSH PRIVILEGES;
```

### prompt para crear datos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL es una instrucción para insertar datos demostrativos en una base de datos. La idea principal es llenar las tablas vacías con información ficticia para probar el funcionamiento del sistema o visualizar cómo se estructuran los datos. Es importante seguir un orden específico al insertar estos datos: primero, debes cargar los registros en aquellas tablas que no tienen restricciones de clave foránea (FK), es decir, que no dependen de otras tablas para tener sentido. Una vez hecho esto, procederás a llenar las tablas restantes que sí tienen estas restricciones. Al seguir este orden, aseguras que todas las referencias entre tablas sean válidas y el sistema funcione correctamente sin errores relacionados con datos faltantes o inconsistentes.

Dado que asumes que todas las claves primarias (PK) comienzan en 1, cada nuevo registro insertado tendrá un ID único, comenzando desde este número y aumentando gradualmente para evitar conflictos. Este proceso de inserción cuidadoso ayuda a mantener la integridad referencial de tu base de datos y asegura que todos los datos sean coherentes entre sí.

`006-prompt para crear datos.sql`

```sql
Y luego por ultimo quiero insert into tantos como haga falta para insertar datos de demostracion - ten en cuenta los FK para insertar primero datos en tablas que no tengan dependencias, y luego datos en las tablas que si que las contengan - las tablas están vacías, con lo cual asume que todos los PK empiezan en 1.
```

### insert into
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para insertar datos en una base de datos que simula un sistema de gestión de tienda online. El código está estructurado en varias partes y cada parte inserta información específica.

1. **Categorías**: Se insertan cuatro categorías (Electrónica, Libros, Ropa, Hogar) con sus respectivos nombres y descripciones. Estos datos forman la jerarquía de productos que vendrá después.
   
2. **Clientes**: Se añaden cuatro clientes con información detallada como nombre, apellidos, dirección, email y teléfono.

3. **Productos**: En esta parte, se insertan ocho productos diferentes en la tabla `productos`. Cada producto tiene asociado una categoría (por ejemplo, el portátil pertenece a "Electrónica"), un precio de venta sin IVA y otras características relevantes como SKU (stock keeping unit) y estado activo.

4. **Gestión de stock**: Se registran entradas en la tabla `gestion_stock` para indicar la existencia inicial del inventario (entradas con tipo "entrada") y luego se anotan las ventas realizadas por cada cliente (que son registros de tipo "salida").

5. **Pedidos**: Aquí se inserta información sobre cuatro pedidos diferentes, cada uno asociado a un cliente específico. Cada pedido tiene una fecha de creación, estado del pedido, total bruto y otros detalles como observaciones.

6. **Líneas de pedido**: Por último, se registra la relación entre los productos comprados en cada pedido (una línea por producto). Para cada línea, se proporciona el id del pedido al que pertenece, el id del producto, cantidad, precio unitario y total con IVA incluido.

Este código es muy útil para crear un conjunto de datos inicial en una base de datos que simula el funcionamiento de una tienda online, permitiendo a los desarrolladores probar funcionalidades sin depender de datos reales. También sirve como ejemplo práctico del manejo de relaciones entre tablas en SQL (como la relación uno-a-muchos entre pedidos y líneas de pedido).

`007-insert into.sql`

```sql
USE tienda_online;

-- =========================================
-- 1) CATEGORÍAS
--    (sin dependencias)
-- =========================================
-- Tras este INSERT:
--  id_categoria = 1 -> Electrónica
--  id_categoria = 2 -> Libros
--  id_categoria = 3 -> Ropa
--  id_categoria = 4 -> Hogar

INSERT INTO categorias (nombre, descripcion, activa) VALUES
('Electrónica', 'Ordenadores, periféricos y gadgets', 1),
('Libros', 'Libros y material de lectura', 1),
('Ropa', 'Ropa y complementos', 1),
('Hogar', 'Artículos para el hogar y decoración', 1);

-- =========================================
-- 2) CLIENTES
--    (sin dependencias)
-- =========================================
-- Tras este INSERT:
--  id_cliente = 1 -> Ana García
--  id_cliente = 2 -> Luis Martínez
--  id_cliente = 3 -> Marta López
--  id_cliente = 4 -> Carlos Sánchez

INSERT INTO clientes 
(nombre, apellidos, email, telefono, direccion, cp, ciudad, provincia, pais, activo) VALUES
('Ana',   'García Pérez',   'ana.garcia@example.com',   '+34 600 111 111', 'Calle Mayor 1',      '46001', 'Valencia',   'Valencia',   'España', 1),
('Luis',  'Martínez Ruiz',  'luis.martinez@example.com','+34 600 222 222', 'Av. Constitución 23','28001', 'Madrid',     'Madrid',     'España', 1),
('Marta', 'López Sánchez',  'marta.lopez@example.com',  '+34 600 333 333', 'Calle Colón 45',     '08001', 'Barcelona',  'Barcelona',  'España', 1),
('Carlos','Sánchez Vidal',  'carlos.sanchez@example.com','+34 600 444 444','Calle Paz 10',       '30001', 'Murcia',     'Murcia',     'España', 1);

-- =========================================
-- 3) PRODUCTOS
--    (dependen de categorías)
-- =========================================
-- Tras este INSERT:
--  id_producto = 1 -> Portátil 14" básico (cat 1)
--  id_producto = 2 -> Ratón inalámbrico (cat 1)
--  id_producto = 3 -> Libro "Aprende Python" (cat 2)
--  id_producto = 4 -> Libro "HTML y CSS" (cat 2)
--  id_producto = 5 -> Camiseta básica (cat 3)
--  id_producto = 6 -> Sudadera con capucha (cat 3)
--  id_producto = 7 -> Lámpara de escritorio (cat 4)
--  id_producto = 8 -> Taza de café (cat 4)

INSERT INTO productos
(id_categoria, nombre, descripcion, sku, precio, impuesto_porcentaje, activo) VALUES
(1, 'Portátil 14" básico', 'Portátil de 14 pulgadas para uso ofimático', 'ELEC-001', 600.00, 21.00, 1),
(1, 'Ratón inalámbrico',   'Ratón óptico inalámbrico con receptor USB', 'ELEC-002',  20.00, 21.00, 1),
(2, 'Libro "Aprende Python"', 'Libro de programación en Python para principiantes', 'LIB-001', 30.00, 21.00, 1),
(2, 'Libro "HTML y CSS"',  'Guía práctica de maquetación web',             'LIB-002', 25.00, 21.00, 1),
(3, 'Camiseta básica',     'Camiseta de algodón unisex',                    'ROP-001', 15.00, 21.00, 1),
(3, 'Sudadera con capucha','Sudadera gruesa con capucha',                   'ROP-002', 40.00, 21.00, 1),
(4, 'Lámpara de escritorio','Lámpara LED articulada para escritorio',       'HOG-001', 35.00, 21.00, 1),
(4, 'Taza de café',        'Taza de cerámica 300ml',                        'HOG-002',  8.00, 21.00, 1);

-- =========================================
-- 4) GESTIÓN DE STOCK
--    (depende de productos)
-- =========================================
-- Para cada producto:
--   - 1 movimiento de ENTRADA (100 uds, carga inicial)
--   - varios movimientos de SALIDA asociados a pedidos demo

-- Entradas iniciales de stock (100 uds de cada producto)
INSERT INTO gestion_stock (id_producto, tipo_movimiento, cantidad, referencia, observaciones) VALUES
(1, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén'),
(2, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén'),
(3, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén'),
(4, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén'),
(5, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén'),
(6, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén'),
(7, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén'),
(8, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén');

-- Salidas de stock ligadas a las líneas de pedido que crearemos después
-- Pedido #1: (id_pedido = 1)
--   - 1x producto 1 (Portátil 14")
--   - 2x producto 2 (Ratón inalámbrico)
INSERT INTO gestion_stock (id_producto, tipo_movimiento, cantidad, referencia, observaciones) VALUES
(1, 'salida', 1, 'Pedido #1', 'Venta al cliente Ana García'),
(2, 'salida', 2, 'Pedido #1', 'Venta al cliente Ana García');

-- Pedido #2: (id_pedido = 2)
--   - 1x producto 3 (Libro Python)
--   - 1x producto 4 (Libro HTML y CSS)
--   - 2x producto 8 (Taza de café)
INSERT INTO gestion_stock (id_producto, tipo_movimiento, cantidad, referencia, observaciones) VALUES
(3, 'salida', 1, 'Pedido #2', 'Venta al cliente Luis Martínez'),
(4, 'salida', 1, 'Pedido #2', 'Venta al cliente Luis Martínez'),
(8, 'salida', 2, 'Pedido #2', 'Venta al cliente Luis Martínez');

-- Pedido #3: (id_pedido = 3)
--   - 3x producto 5 (Camiseta básica)
--   - 1x producto 6 (Sudadera con capucha)
INSERT INTO gestion_stock (id_producto, tipo_movimiento, cantidad, referencia, observaciones) VALUES
(5, 'salida', 3, 'Pedido #3', 'Venta al cliente Marta López'),
(6, 'salida', 1, 'Pedido #3', 'Venta al cliente Marta López');

-- Pedido #4: (id_pedido = 4)
--   - 1x producto 7 (Lámpara de escritorio)
--   - 1x producto 1 (Portátil 14")
INSERT INTO gestion_stock (id_producto, tipo_movimiento, cantidad, referencia, observaciones) VALUES
(7, 'salida', 1, 'Pedido #4', 'Venta al cliente Ana García'),
(1, 'salida', 1, 'Pedido #4', 'Venta al cliente Ana García');

-- =========================================
-- 5) PEDIDOS
--    (dependen de clientes)
-- =========================================
-- IMPORTANTE: asumimos tablas vacías, así que:
--   id_pedido = 1,2,3,4 en este orden.
-- Los totales están calculados a partir de las líneas
-- (21% de IVA sobre el bruto).

-- Pedido 1: cliente 1 (Ana García)
-- Líneas:
--   1x Portátil 14" (600.00)
--   2x Ratón inalámbrico (20.00)
-- Bruto: 640.00
-- IVA (21%): 134.40
-- Total: 774.40

INSERT INTO pedidos
(id_cliente, fecha_pedido, estado, total_bruto, total_impuestos, total, observaciones) VALUES
(1, '2025-01-10 10:30:00', 'pagado',   640.00, 134.40, 774.40, 'Compra online paga con tarjeta'),

-- Pedido 2: cliente 2 (Luis Martínez)
-- Líneas:
--   1x Libro "Aprende Python" (30.00)
--   1x Libro "HTML y CSS" (25.00)
--   2x Taza de café (8.00)
-- Bruto: 71.00
-- IVA (21%): 14.91
-- Total: 85.91
(2, '2025-01-12 16:45:00', 'enviado',   71.00,  14.91,  85.91, 'Envío por mensajería 24h'),

-- Pedido 3: cliente 3 (Marta López)
-- Líneas:
--   3x Camiseta básica (15.00)
--   1x Sudadera con capucha (40.00)
-- Bruto: 85.00
-- IVA (21%): 17.85
-- Total: 102.85
(3, '2025-01-15 09:15:00', 'pagado',    85.00,  17.85, 102.85, 'Pedido recogida en tienda'),

-- Pedido 4: cliente 1 (Ana García)
-- Líneas:
--   1x Lámpara de escritorio (35.00)
--   1x Portátil 14" (600.00)
-- Bruto: 635.00
-- IVA (21%): 133.35
-- Total: 768.35
(1, '2025-01-20 18:20:00', 'pendiente', 635.00, 133.35, 768.35, 'Pendiente de pago por transferencia');

-- =========================================
-- 6) LÍNEAS DE PEDIDO
--    (dependen de pedidos y productos)
-- =========================================
-- Recordatorio:
--   Pedido 1 -> id_pedido = 1
--   Pedido 2 -> id_pedido = 2
--   Pedido 3 -> id_pedido = 3
--   Pedido 4 -> id_pedido = 4
--
-- Todos los productos tienen impuesto_porcentaje = 21.00
-- total_linea = bruto_linea + IVA_linea

INSERT INTO lineas_pedido
(id_pedido, id_producto, cantidad, precio_unitario, impuesto_porcentaje, total_linea) VALUES

-- Pedido 1 (id_pedido = 1)
--  1x producto 1 (600.00) -> bruto 600, IVA 126.00, total 726.00
(1, 1, 1, 600.00, 21.00, 726.00),
--  2x producto 2 (20.00)  -> bruto 40, IVA 8.40, total 48.40
(1, 2, 2,  20.00, 21.00,  48.40),

-- Pedido 2 (id_pedido = 2)
--  1x producto 3 (30.00)  -> bruto 30, IVA 6.30, total 36.30
(2, 3, 1,  30.00, 21.00,  36.30),
--  1x producto 4 (25.00)  -> bruto 25, IVA 5.25, total 30.25
(2, 4, 1,  25.00, 21.00,  30.25),
--  2x producto 8 (8.00)   -> bruto 16, IVA 3.36, total 19.36
(2, 8, 2,   8.00, 21.00,  19.36),

-- Pedido 3 (id_pedido = 3)
--  3x producto 5 (15.00)  -> bruto 45, IVA 9.45, total 54.45
(3, 5, 3,  15.00, 21.00,  54.45),
--  1x producto 6 (40.00)  -> bruto 40, IVA 8.40, total 48.40
(3, 6, 1,  40.00, 21.00,  48.40),

-- Pedido 4 (id_pedido = 4)
--  1x producto 7 (35.00)  -> bruto 35, IVA 7.35, total 42.35
(4, 7, 1,  35.00, 21.00,  42.35),
--  1x producto 1 (600.00) -> bruto 600, IVA 126.00, total 726.00
(4, 1, 1, 600.00, 21.00, 726.00);
```

### Actividades propuestas

El script SQL que has proporcionado realiza varias operaciones en una base de datos MySQL para gestionar un sistema de pedidos y ventas. Veamos los pasos principales:

### Paso 1: Creación de Tablas

Las tablas se crean con sus respectivas relaciones e índices:

- **clientes**: Almacena información sobre clientes.
- **pedidos**: Almacena detalles del pedido, incluyendo total bruto, impuestos y total final.
- **lineas_pedido**: Detalla las líneas de cada pedido, especificando el producto, cantidad, precio unitario, impuesto y total por línea.
- **productos**: Almacena información sobre los productos disponibles para la venta.
- **gestion_stock**: Registra entradas y salidas del inventario basándose en pedidos.

### Paso 2: Creación de Índices

Se crean índices únicos para mejorar la eficiencia en la búsqueda y evitar duplicados:

- En `clientes`:
  - **nombre**: Para asegurar que cada cliente tenga un nombre único.
  
- En `productos`:
  - **codigo_producto**: Para garantizar que cada producto tenga un código único.

### Paso 3: Creación de Claves Externas

Se establecen relaciones entre las tablas para mantener la integridad referencial:

- Cada pedido en la tabla `pedidos` está vinculado a un cliente específico mediante una clave externa (`id_cliente`) que hace referencia al identificador del cliente en `clientes`.
  
- Las líneas de pedidos en `lineas_pedido` se relacionan con tanto los productos como los pedidos, utilizando claves externas (`id_producto`, `id_pedido`).

### Paso 4: Inserción de Datos

Se inserta un conjunto inicial de datos para demostrar cómo funcionaría el sistema:

- **Clientes**: Se añaden cuatro clientes ficticios.
  
- **Pedidos**: Se registran cuatro pedidos diferentes, cada uno asociado a un cliente específico y con fechas, estados, totales bruto e impuestos calculados.
  
- **Líneas de pedido**: Para cada pedido se detallan las líneas correspondientes, incluyendo productos específicos, cantidad, precio unitario, impuesto aplicado y total por línea.

- **Gestión del stock**: Registra la entrada y salida de los productos en el inventario basándose en los pedidos registrados.

### Conclusión

Este script establece una base sólida para un sistema de gestión de ventas y pedidos. Proporciona tanto estructura como datos iniciales, permitiendo a un usuario nuevo entender cómo funciona el flujo general del sistema al realizar operaciones CRUD (Crear, Leer, Actualizar, Borrar) en la base de datos.

Es importante notar que este script asume que las tablas están vacías y establece relaciones de clave externa para asegurar integridad referencial. Esto es crucial en aplicaciones web o sistemas empresariales donde la consistencia de los datos es primordial.

Si tienes alguna pregunta específica sobre cómo utilizar esta estructura, cómo modificarla para adaptarse a tus necesidades específicas o cualquier otro aspecto del sistema que te resulte confuso, no dudes en preguntar.


<a id="politicas-de-bloqueo-concurrencia"></a>
## Políticas de bloqueo. Concurrencia

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/004-Tratamiento%20de%20datos/005-Pol%C3%ADticas%20de%20bloqueo.%20Concurrencia)

### Introducción a los ejercicios

Este código proporciona una implementación detallada de un programa CRUD (Crear, Leer, Actualizar y Borrar) basado en consola para una base de datos SQLite. El programa utiliza colores y formateo para mejorar la experiencia del usuario y ofrece funcionalidades básicas para interactuar con tablas en la base de datos.

Aquí se detalla cómo funciona el código:

1. **Configuración inicial**:
    - Se conecta a una base de datos SQLite especificada por `DB_PATH`.
    - Se crea un cursor para realizar operaciones sobre la base de datos.
    
2. **Funciones CRUD**:
    - `op_create()`: Permite insertar nuevos registros en una tabla específica, pidiendo al usuario los valores necesarios para cada columna.
    - `op_list()`: Lista todos los registros de una tabla especificada.
    - `read_by_pk()`: Consulta un registro específico por su clave primaria (PK).
    - `op_update()`: Actualiza un registro existente en función de la PK, permitiendo al usuario modificar columnas específicas.
    - `op_delete()`: Elimina un registro basado en su clave primaria.

3. **Interfaz del Usuario**:
    - `select_table()`: Permite seleccionar una tabla específica para realizar operaciones CRUD.
    - `select_operation()`: Muestra opciones al usuario (crear, leer, actualizar, eliminar registros) y solicita una elección de operación.
    
4. **Menú Principal**:
    - El menú principal permite al usuario seleccionar una tabla y luego elegir entre las operaciones CRUD o salir del programa.

5. **Manejo de Excepciones**:
    - Maneja excepciones para casos como errores en la base de datos y interrupciones del usuario (por ejemplo, Ctrl+C).

6. **Estilo y Formateo**:
    - Utiliza ANSI escape codes para agregar estilos de texto (como negrita y colores) a los mensajes de la consola.
    
### Ejecución

El programa se ejecuta en un bucle principal que permite al usuario interactuar con las tablas de la base de datos hasta que elige salir. Al iniciar, muestra un mensaje de bienvenida y luego espera a que el usuario seleccione una tabla.

Para usar este script, debes tener instalada la biblioteca `sqlite3` (que viene por defecto en Python) y asegurarte de que la base de datos especificada (`DB_PATH`) exista o esté correctamente configurada. 

### Ejemplos de Salida

Cuando se ejecuta el programa, puede ver mensajes como:

- **Mensaje de Bienvenida**:
  ```
  ███████╗ ██████╗ ██╗   ██╗███████╗
  ██╔════╝██╔═══██╗██║   ██║██╔════╝
  █████╗  ██║   ██║██║   ██║█████╗  
  ██╔══╝  ██║▄▄ ██║██║   ██║██╔══╝  
  ██║     ╚██████╔╝╚██████╔╝███████╗
  ╚═╝      ╚══▀▀═╝  ╚═════╝ ╚══════╝

  ██████╗ ████████╗    ███████╗ █████╗ ███╗   ██╗
  ██╔══██╗╚══██╔══╝    ██╔════╝██╔══██╗████╗  ██║
  ██████╔╝   ██║       █████╗  ███████║██╔██╗ ██║
  ██╔══██╗   ██║       ██╔══╝  ██╔══██║██║╚██╗██║
  ██║  ██║   ██║       ██║     ██║  ██║██║ ╚████║
  ╚═╝  ╚═╝   ╚═╝       ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝

  Bienvenido al gestor de base de datos en consola.
  ```
  
- **Selección de Tabla**:
  - Muestra una lista numerada de tablas disponibles en la base de datos.

- **Operaciones CRUD**:
  - Selecciona operaciones CRUD y realiza acciones basadas en las respuestas del usuario.

### Consideraciones

Este script es un punto de partida excelente para desarrollar aplicaciones CRUD más complejas. Puedes extenderlo con funcionalidades adicionales como validación de datos, manejo de errores más detallado, o integración con bases de datos más complejas.

### Create Table
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está creando una nueva tabla en una base de datos llamada "clientes". La tabla contiene cinco columnas: "Identificador", "nombre", "apellidos", "email" y "direccion".

1. **Identificador**: Es un campo del tipo INTEGER que se utilizará como clave primaria para cada registro. Esto significa que cada cliente tiene un identificador único, y la base de datos garantiza que no haya duplicados ni valores nulos aquí.

2. **nombre**: Almacena el nombre del cliente usando el tipo TEXT, lo cual indica que puede contener cualquier texto (como 'Juan').

3. **apellidos**: Similar a "nombre", pero para almacenar los apellidos del cliente ('Pérez Martínez', por ejemplo).

4. **email**: Guarda la dirección de correo electrónico del cliente como texto.

5. **direccion**: Almacena la dirección física del cliente, también en formato de texto (por ejemplo, 'Calle Principal 123').

La declaración `PRIMARY KEY("Identificador" AUTOINCREMENT)` indica que el campo "Identificador" es la clave primaria y que su valor se incrementará automáticamente cada vez que un nuevo registro sea añadido a la tabla. Esto asegura que no haya dos clientes con el mismo identificador y facilita la gestión de los registros en la base de datos.

Este código es fundamental porque define la estructura básica para almacenar información sobre los clientes en una aplicación o sistema de gestión de bases de datos.

`003-Create Table.sql`

```sql
CREATE TABLE "clientes" (
	"Identificador"	INTEGER,
	"nombre"	TEXT,
	"apellidos"	TEXT,
	"email"	TEXT,
	"direccion"	TEXT,
	PRIMARY KEY("Identificador" AUTOINCREMENT)
);
```

### Tabla de pedidos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para crear una tabla llamada "productos" en una base de datos. La tabla contiene varias columnas que almacenan diferentes tipos de información sobre los productos, como su identificador único, nombre, descripción, precio y categoría. 

La columna "Identificador" es la clave primaria de la tabla, lo que significa que cada producto tendrá un número único asignado automáticamente por el sistema (gracias a `AUTOINCREMENT`). Este número único sirve para distinguir cada registro en la tabla sin ambigüedades.

Este tipo de estructura es fundamental para organizar y gestionar datos relacionados con productos en una base de datos, permitiendo realizar operaciones como insertar nuevos productos, actualizar información existente o buscar productos específicos por diferentes criterios.

`004-Tabla de pedidos.sql`

```sql
CREATE TABLE "productos" (
	"Identificador"	INTEGER,
	"nombre"	TEXT,
	"descripcion"	TEXT,
	"precio"	TEXT,
	"categoria"	TEXT,
	PRIMARY KEY("Identificador" AUTOINCREMENT)
);
```

### Insertar un cliente
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para insertar un nuevo registro en la tabla `clientes`. La instrucción `INSERT INTO` especifica que queremos añadir una nueva fila a la tabla `clientes`. Dentro de los paréntesis, proporcionamos los valores que queremos asignar a las columnas de esta tabla. 

El primer valor es `NULL`, lo cual indica que el campo correspondiente en la base de datos (probablemente un identificador automático como una clave primaria) debe ser generado automáticamente por el sistema o se deja vacío para que sea llenado automáticamente al insertar este nuevo registro.

Los valores restantes ('Jose Vicente', 'Carratala Sanchis', 'info@jocarsa.com', 'La calle de Jose Vicente') corresponden a los nombres, apellidos, correo electrónico y dirección del cliente respectivamente. Estos son datos específicos que se insertarán en las columnas apropiadas de la tabla `clientes`.

Este tipo de instrucción es fundamental para añadir nuevos registros a una base de datos, permitiendo así mantener y actualizar dinámicamente la información almacenada sobre clientes o cualquier otra entidad en un sistema administrado por bases de datos.

`005-Insertar un cliente.sql`

```sql
INSERT INTO clientes VALUES(
  NULL,
  'Jose Vicente',
  'Carratala Sanchis',
  'info@jocarsa.com',
  'La calle de Jose Vicente'
);
```

### seleccion de clientes
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL selecciona todos los registros de la tabla llamada `clientes`. La instrucción `SELECT *` indica que se deben recuperar todas las columnas y filas disponibles en la tabla especificada. En este caso, el resultado será una lista completa con toda la información almacenada actualmente en la tabla `clientes`, lo cual es útil para visualizar o analizar los datos de todos los clientes registrados en un sistema. Es importante tener presente que esta consulta puede devolver muchos registros si la tabla tiene mucha información, por lo que es recomendable usar criterios de selección más específicos cuando sea necesario.

`006-seleccion de clientes.sql`

```sql
SELECT * FROM clientes;
```

### Insertar un producto
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para insertar un nuevo registro en la tabla llamada `productos`. La sentencia `INSERT INTO` es una instrucción que permite añadir filas a una tabla existente en la base de datos. En este caso, el código está preparado para agregar detalles sobre un producto específico: un ratón de ordenador.

El código inserta valores en cinco columnas de la tabla `productos`, aunque solo especifica los valores para cuatro de ellas explícitamente. El primer valor es `NULL`, lo que significa que se dejará que el sistema autoasigne un identificador único (usualmente, esto ocurre si la primera columna es una clave primaria con opción AUTO_INCREMENT). Luego, se proporcionan detalles como el nombre del producto ('Raton'), su descripción ('Raton de ordenador'), el precio ('5.42') y la categoría ('Informatica'). Esta operación permite expandir los datos almacenados en la base de datos, añadiendo información sobre un nuevo artículo disponible para venta o uso.

Es importante entender este tipo de comando cuando se trabaja con bases de datos, ya que es fundamental para poder registrar nuevas entradas según sea necesario.

`007-Insertar un producto.sql`

```sql
INSERT INTO productos VALUES(
  NULL,
  'Raton',
  'Raton de ordenador',
  '5.42',
  'Informatica'
);
```

### seleccionar los productos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

El código SQL que has proporcionado, `SELECT * FROM productos;`, es una consulta que busca recuperar todos los registros de la tabla llamada "productos". La parte `*` significa que se seleccionan todas las columnas disponibles en esa tabla. En otras palabras, este comando te devolverá toda la información almacenada actualmente en la tabla "productos", mostrándote cada fila y columna del conjunto de datos.

Esta consulta es útil cuando necesitas ver un resumen completo de todos los productos registrados en tu base de datos sin especificar detalles adicionales. Es una forma rápida y simple de obtener acceso a toda la información almacenada, lo que puede ser beneficioso para el análisis, la auditoría o simplemente para entender cómo están estructurados tus datos.

`008-seleccionar los productos.sql`

```sql
SELECT * FROM productos;
```

### actualizar precio de un producto
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL realiza dos operaciones en una base de datos que contiene información sobre productos. Primero, actualiza el precio de un producto específico en la tabla `productos`. La instrucción `UPDATE productos SET precio = "6.54" WHERE Identificador = 1;` cambia el valor del campo `precio` a 6.54 euros para el registro cuyo identificador es igual a 1.

Después, el código ejecuta una consulta que selecciona todos los registros de la tabla `productos`. Esto permite ver cómo ha cambiado la información en la tabla después de actualizar el precio del producto específico. Esta operación es importante porque te ayuda a verificar que la actualización se realizó correctamente y no afectó accidentalmente otros productos en la base de datos.

`009-actualizar precio de un producto.sql`

```sql
UPDATE productos
SET precio = "6.54"
WHERE Identificador = 1;

SELECT * FROM productos;
```

### eliminar
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está diseñado para gestionar los datos en una tabla llamada `productos`. Vamos a desglosarlo:

1. La primera línea, `DELETE FROM productos WHERE Identificador = 1;`, elimina el registro del primer producto que se encuentra en la base de datos. Aquí, se asume que cada producto tiene un identificador único y, en este caso, se está eliminando el producto con ese identificador.

2. La segunda línea, `SELECT * FROM productos;`, es una consulta SELECT que recupera todos los registros restantes de la tabla `productos` después de haberse ejecutado la instrucción DELETE anteriormente. Esto te permite ver cuál fue el efecto de la eliminación y verificar si se borró correctamente el registro deseado.

3. La última parte del código, `INSERT INTO productos VALUES(NULL, 'Raton', 'Raton de ordenador', '5.42', 'Informatica');`, agrega un nuevo producto a la tabla `productos`. En este caso, se está insertando un ratón como artículo de informática con un precio especificado.

Este código es importante porque demuestra cómo realizar operaciones básicas en una base de datos SQL: eliminar un registro existente y luego añadir uno nuevo. Estas habilidades son fundamentales para el manejo eficiente de bases de datos, especialmente cuando se necesita mantener la integridad de los datos actualizados.

`010-eliminar.sql`

```sql
DELETE FROM productos WHERE Identificador = 1;

SELECT * FROM productos;

INSERT INTO productos VALUES(
  NULL,
  'Raton',
  'Raton de ordenador',
  '5.42',
  'Informatica'
);
```

### crear tabla pedidos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para crear una tabla llamada `pedidos` en una base de datos. La tabla contiene información sobre los pedidos realizados, como el identificador único del pedido, el ID del cliente que hizo el pedido, el ID del producto solicitado, la fecha del pedido, la cantidad de productos pedida y el total a pagar por ese pedido.

La columna `Identificador` es una clave primaria autoincremental, lo que significa que cada nuevo registro en esta tabla tendrá un número único automáticamente asignado. Las columnas `cliente_id` y `producto_id` son también únicas para asegurar que cada cliente y producto estén correctamente identificados sin duplicidades.

El código incluye dos claves foráneas que establecen una relación con otras tablas: `clientes` y `productos`. Estas relaciones son importantes porque mantienen la integridad de los datos. Si un cliente o un producto es eliminado de sus respectivas tablas, cualquier pedido asociado a ellos también será automáticamente eliminado debido al uso del atributo `ON DELETE CASCADE`.

Esta estructura asegura que la base de datos sea consistente y que no queden pedidos huérfanos sin un cliente o producto asociados.

`011-crear tabla pedidos.sql`

```sql
CREATE TABLE "pedidos" (
    "Identificador" INTEGER PRIMARY KEY AUTOINCREMENT,
    "cliente_id" INTEGER UNIQUE,
    "producto_id" INTEGER UNIQUE,
    "fecha" TEXT,
    "cantidad" INTEGER,
    "total" REAL,
    FOREIGN KEY("cliente_id") REFERENCES "clientes"("Identificador") ON DELETE CASCADE,
    FOREIGN KEY("producto_id") REFERENCES "productos"("Identificador") ON DELETE CASCADE
);
```

### primero creamos la tabla
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL crea una tabla llamada `pedidos` en una base de datos. La tabla almacena información sobre los pedidos realizados, incluyendo detalles como el identificador único del pedido, el ID del cliente que hizo el pedido, el ID del producto que se compró, la fecha del pedido, la cantidad de productos adquirida y el total del costo. 

El campo `Identificador` es una clave primaria autoincremental, lo que significa que cada vez que un nuevo registro (pedido) se agrega a esta tabla, automáticamente recibe un número único. Los campos `cliente_id` y `producto_id` son también enteros únicos, asegurando que no haya dos pedidos asociados al mismo cliente o producto en la misma fila de la tabla sin una diferencia clara.

Esta estructura es fundamental para organizar y gestionar los datos de manera eficiente, permitiendo a un sistema realizar operaciones como insertar nuevos pedidos, consultar información específica sobre los pedidos existentes, actualizar detalles de pedidos si es necesario, y mucho más.

`012-primero creamos la tabla.sql`

```sql
-- 1️⃣ Crear la tabla pedidos (sin relaciones todavía)
CREATE TABLE "pedidos" (
    "Identificador" INTEGER PRIMARY KEY AUTOINCREMENT,
    "cliente_id" INTEGER UNIQUE,
    "producto_id" INTEGER UNIQUE,
    "fecha" TEXT,
    "cantidad" INTEGER,
    "total" REAL
);
```

### clave externa 1
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para modificar una tabla existente llamada `pedidos` en una base de datos. En específico, el código está añadiendo una clave externa (foreign key) que relaciona la columna `cliente_id` en la tabla `pedidos` con la columna `Identificador` en la tabla `clientes`. Esto significa que cada pedido está vinculado a un cliente específico mediante su identificador único.

La cláusula `ON DELETE CASCADE` es importante porque determina qué ocurre cuando se elimina un registro de la tabla `clientes`. En este caso, si un cliente es eliminado, todos los pedidos asociados a ese cliente también serán automáticamente borrados. Esto ayuda a mantener la integridad referencial entre las tablas.

En resumen, esta línea de código fortalece la relación entre la tabla de pedidos y la tabla de clientes asegurando que no haya pedidos huérfanos en caso de que se eliminen los datos del cliente correspondiente.

`013-clave externa 1.sql`

```sql
-- 2️⃣ Añadir la relación 1:1 con clientes
ALTER TABLE "pedidos"
ADD FOREIGN KEY ("cliente_id") REFERENCES "clientes"("Identificador") ON DELETE CASCADE;
```

### clave externa 2
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está diseñado para mejorar una tabla existente llamada `pedidos` en una base de datos. En específico, el código añade una clave externa (foreign key) que relaciona la columna `producto_id` de la tabla `pedidos` con la columna `Identificador` de la tabla `productos`. Esto establece una relación uno a uno entre las dos tablas, lo que significa que cada pedido está asociado con un producto específico.

La cláusula `ON DELETE CASCADE` es crucial porque determina qué sucede en la tabla `pedidos` cuando se elimina un registro de la tabla `productos`. En este caso, si se borra un producto de la tabla `productos`, todos los pedidos que referencian a ese producto (mediante el `producto_id`) también serán eliminados automáticamente. Esto ayuda a mantener la integridad de los datos y evita problemas con registros huérfanos en la tabla `pedidos`.

En resumen, este código asegura una relación coherente entre pedidos y productos en tu base de datos, manteniendo la consistencia al permitir operaciones automatizadas cuando se eliminan elementos.

`014-clave externa 2.sql`

```sql
-- 3️⃣ Añadir la relación 1:1 con productos
ALTER TABLE "pedidos"
ADD FOREIGN KEY ("producto_id") REFERENCES "productos"("Identificador") ON DELETE CASCADE;
```

### de un golpe
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL crea una nueva tabla en la base de datos llamada `pedidos`. La tabla tiene varias columnas que almacenan información sobre los pedidos, como el identificador único del pedido, el ID del cliente que realizó el pedido, el ID del producto asociado al pedido, la fecha del pedido, la cantidad de productos pedida y el total a pagar. 

Lo más relevante en este código son las claves foráneas (foreign keys) que se definen para `cliente_id` e `producto_id`. Estas claves foráneas establecen una relación con las tablas `clientes` y `productos`, respectivamente, asegurando que cada pedido esté asociado a un cliente existente y a un producto existente. Además, cuando se elimina un cliente o un producto de sus tablas correspondientes, también se eliminan automáticamente todos los pedidos relacionados con esa clave foránea gracias a la opción `ON DELETE CASCADE`.

Esta tabla es crucial para mantener una base de datos coherente y relacionada, ya que asegura que no haya pedidos sin clientes o productos asociados.

`015-de un golpe.sql`

```sql
-- 1️⃣ Crear la nueva tabla con las claves foráneas
CREATE TABLE "pedidos" (
    "Identificador" INTEGER PRIMARY KEY AUTOINCREMENT,
    "cliente_id" INTEGER,
    "producto_id" INTEGER,
    "fecha" TEXT,
    "cantidad" INTEGER,
    "total" REAL,
    FOREIGN KEY ("cliente_id") REFERENCES "clientes"("Identificador") ON DELETE CASCADE,
    FOREIGN KEY ("producto_id") REFERENCES "productos"("Identificador") ON DELETE CASCADE
);
```

### inserción de pedido
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL muestra dos inserciones diferentes en la tabla `pedidos`. La tabla `pedidos` probablemente tiene columnas para identificar cada pedido (como un ID automático), detalles sobre el cliente que realizó el pedido, la fecha del pedido y tal vez información sobre productos y costos.

La primera línea de código es un comentario (`-- incorrecta`) que indica que la siguiente inserción no debería hacerse correctamente. La inserción intenta añadir una nueva fila a `pedidos` con valores específicos: `NULL`, `5`, `7`, `"2025-10-16"`, `5`, y `20.5`. Aquí, `NULL` sugiere que la base de datos debería generar automáticamente un valor para la columna ID del pedido, mientras que los otros valores representan detalles del pedido como el cliente (ID 5), producto (ID 7), fecha, cantidad (`5`) y costo (`20.5`). El comentario indica que algo está mal con estos valores.

La línea siguiente también es un comentario (`-- correcta`), indicando que la inserción a continuación debería funcionar correctamente. Esta inserción es muy similar a la anterior pero utiliza diferentes valores: `NULL`, `1`, `2`, `"2025-10-16"`, `5`, y `20.5`. Estos cambios sugieren que el pedido correcto está asociado con un cliente distinto (ID 1) y un producto diferente (ID 2).

Es importante entender estos ejemplos para aprender cómo insertar datos correctamente en una base de datos, asegurándose de que los valores utilizados sean válidos según las reglas de la base de datos.

`016-inserción de pedido.sql`

```sql
-- incorrecta

INSERT INTO pedidos VALUES(
  NULL,
  5,
  7,
  "2025-10-16",
  5,
  20.5
);

-- correcta

INSERT INTO pedidos VALUES(
  NULL,
  1,
  2,
  "2025-10-16",
  5,
  20.5
);
```

### conectar en python
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es el inicio de un script en Python que se utiliza para trabajar con una base de datos SQLite. La línea `import sqlite3` importa el módulo sqlite3, que proporciona funciones para interactuar con bases de datos SQLite desde dentro del programa. Este módulo incluye clases y métodos necesarios para abrir o crear bases de datos, ejecutar consultas SQL, manejar transacciones y más. Es un paso crucial al principio del script porque establece el entorno necesario para trabajar con la base de datos.

La importación de este módulo es importante ya que te permite conectarte a una base de datos SQLite existente o crear una nueva, así como ejecutar comandos SQL directamente desde tu programa Python. Esto es fundamental en ejercicios y proyectos relacionados con el manejo de bases de datos en Python, permitiendo operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en la base de datos.

`017-conectar en python.py`

```python
import sqlite3
```

### abrir y select
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es una parte del programa que se encarga de conectarse a una base de datos SQLite y recuperar información. En este caso, específicamente, el programa está haciendo lo siguiente:

1. **Conexión con la Base de Datos:** Primero, importa el módulo `sqlite3` para trabajar con bases de datos SQLite. Luego, utiliza la función `connect()` para abrir o crear (si no existe) una base de datos llamada "empresa.db". Almacena esta conexión en la variable `basededatos`.

2. **Ejecución del Query SQL:** Se crea un cursor utilizando el método `.cursor()`, que se usa para ejecutar comandos SQL y manipular registros. Luego, con el método `.execute()`, ejecuta una consulta SELECT que selecciona todos los datos de la tabla llamada "clientes".

3. **Recuperación de Datos:** Los resultados obtenidos por la consulta son recuperados usando el método `fetchall()` del cursor, que devuelve todas las filas como un conjunto (list) de tuplas. Estos resultados se almacenan en la variable `filas`.

4. **Impresión de Datos:** Finalmente, el programa recorre cada fila del conjunto de resultados utilizando un bucle for e imprime cada fila.

Este código es importante porque muestra cómo interactuar con una base de datos SQLite desde Python para recuperar y visualizar información almacenada en una tabla específica. Es una parte fundamental del manejo de bases de datos en aplicaciones Python, especialmente cuando se trata de la gestión de clientes o cualquier otro tipo de registro de negocio.

`018-abrir y select.py`

```python
import sqlite3

basededatos = sqlite3.connect("empresa.db")

cursor = basededatos.cursor()

cursor.execute("SELECT * FROM clientes")
filas = cursor.fetchall()

for fila in filas:
  print(fila)
```

### insertar
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código Python está conectado a una base de datos SQLite llamada `empresa.db`. La función principal es insertar un nuevo registro en la tabla `clientes`.

El código comienza importando el módulo `sqlite3`, que proporciona herramientas para interactuar con bases de datos SQLite. Luego, se establece una conexión a la base de datos utilizando la función `connect()`, y se crea un objeto cursor que permite ejecutar consultas SQL en esa base de datos.

La línea clave es el uso del método `execute()` del objeto cursor, donde se inserta un nuevo registro en la tabla `clientes`. Este comando SQL especifica que los valores a ingresar son: un valor NULL (que probablemente se refiere al ID autoincremental), 'Juan' como nombre, 'Garcia Lopez' como apellido, 'juan@jocarsa.com' como correo electrónico y 'La calle de Juan' como dirección. Este comando insertará automáticamente estos datos en la tabla `clientes`.

Finalmente, el método `commit()` se utiliza para confirmar los cambios realizados en la base de datos. Sin este paso, las inserciones no serían permanentes.

Este tipo de operación es crucial cuando necesitas añadir nuevos registros a tu base de datos y es una habilidad fundamental en la gestión de bases de datos relacionales.

`019-insertar.py`

```python
import sqlite3

basededatos = sqlite3.connect("empresa.db")

cursor = basededatos.cursor()

cursor.execute('''
  INSERT INTO clientes
  VALUES (
    NULL,
    'Juan',
    'Garcia Lopez',
    'juan@jocarsa.com',
    'La calle de Juan'
  );
''')

basededatos.commit()
```

### actualizar
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código Python realiza una actualización en una base de datos SQLite llamada `empresa.db`. Primero, se importa el módulo `sqlite3`, que es la herramienta estándar para trabajar con bases de datos SQLite en Python. Luego, se conecta a la base de datos `empresa.db` y crea un objeto cursor, que será utilizado para ejecutar comandos SQL.

El código entonces ejecuta una consulta SQL del tipo UPDATE, que cambia el valor de la columna 'direccion' en la tabla 'clientes'. Específicamente, establece la dirección como 'La otra calle de Juan', pero solo para el registro cuyo identificador es 2. Finalmente, se llama al método `commit()` en la conexión a la base de datos para guardar los cambios realizados.

Esta operación es crucial cuando necesitas modificar información existente en tu base de datos sin tener que eliminar y reinsertar registros completos. Es una forma eficiente de mantener tus datos actualizados según sea necesario.

`020-actualizar.py`

```python
import sqlite3

basededatos = sqlite3.connect("empresa.db")

cursor = basededatos.cursor()

cursor.execute('''
  UPDATE clientes
  SET direccion = 'La otra calle de Juan'
  WHERE Identificador = 2;
''')

basededatos.commit()
```

### eliminar
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código Python está diseñado para eliminar un registro específico de una tabla llamada `clientes` en una base de datos SQLite. La función principal del fragmento es borrar el cliente cuyo campo `Identificador` tiene el valor 2.

Primero, se importa la librería `sqlite3`, que permite interactuar con bases de datos SQLite desde Python. Luego, se establece una conexión a la base de datos llamada `empresa.db`. Esta acción es necesaria para poder ejecutar cualquier comando SQL en ella.

Después, el código crea un objeto cursor utilizando el método `.cursor()` de la conexión a la base de datos. El cursor permite enviar comandos SQL y recibir los resultados devueltos por la base de datos.

El siguiente paso es ejecutar una consulta `DELETE` mediante el método `.execute()`. Esta consulta elimina del registro en la tabla `clientes` donde el campo `Identificador` tenga el valor 2. Es importante ser preciso al especificar qué registros eliminar para evitar borrar información incorrecta o no deseada.

Finalmente, se utiliza el método `.commit()` de la conexión a la base de datos para confirmar los cambios realizados por la consulta `DELETE`. Esto asegura que la eliminación del registro se guarda permanentemente en la base de datos. Sin esta línea, los cambios no se guardarían y serían descartados cuando se cierra la conexión.

Este código es útil para gestionar dinámicamente la información almacenada en una base de datos, permitiendo la actualización o limpieza de registros según sea necesario.

`021-eliminar.py`

```python
import sqlite3

basededatos = sqlite3.connect("empresa.db")

cursor = basededatos.cursor()

cursor.execute('''
  DELETE FROM clientes
  WHERE Identificador = 2;
''')

basededatos.commit()
```

### crear programa de gestion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código es una parte de un programa en Python que gestiona una base de datos SQLite. En primer lugar, importa la biblioteca `sqlite3`, que permite interactuar con bases de datos SQLite desde Python.

El código inicia borrando todo el contenido de la pantalla y muestra un mensaje "Programa de gestión", seguido por una lista numerada de las tablas existentes en la base de datos. Para lograr esto, primero se conecta a la base de datos llamada `empresa.db` utilizando `sqlite3.connect("empresa.db")`.

Luego, el programa ejecuta una consulta SQL para obtener los nombres de todas las tablas presentes en la base de datos. Esto se hace usando la sentencia `SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;`. El resultado de esta consulta es almacenado en un objeto llamado `filas`.

Finalmente, el código itera sobre cada fila del resultado (cada nombre de tabla) y lo muestra en pantalla con su correspondiente número. Esto ayuda a los usuarios a ver todas las tablas disponibles y seleccionar la que desean gestionar.

El programa espera a que el usuario introduzca una opción elegida y continúa después de esta entrada, permitiendo al usuario interactuar con diferentes partes de la base de datos según lo necesario. Esta interfaz simple pero efectiva es útil para manejar tareas básicas en la base de datos `empresa.db`.

`022-crear programa de gestion.py`

```python
import sqlite3

print("\033[2J")  # Borrar pantalla
print("\033[0;0H", end="")
print("Programa de gestión")
print("Selecciona una entidad:")

basededatos = sqlite3.connect("empresa.db")
cursor = basededatos.cursor()
cursor.execute('''
  SELECT name 
  FROM sqlite_master 
  WHERE type='table'
  ORDER BY name;
  ''')
contador = 1
filas = cursor.fetchall()
for fila in filas:
  print(str(contador)+"-"+fila[0])
  contador += 1
opcion = input("Tu opción elegida: ")
```

### seleccion de opcion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código Python se utiliza para gestionar una base de datos SQLite llamada `empresa.db`. Primero, el programa borra la pantalla y muestra un menú interactivo que lista todas las tablas disponibles en la base de datos. Esto ayuda al usuario a seleccionar una tabla específica según sus necesidades.

El código conecta a la base de datos `empresa.db` utilizando la biblioteca `sqlite3`. Luego, ejecuta una consulta SQL para obtener los nombres de todas las tablas que están almacenadas en esta base de datos. La información es recogida y mostrada al usuario en un formato fácil de leer, donde cada tabla está numerada.

Después de mostrar estas opciones a través del bucle `for`, el programa solicita al usuario que introduzca la opción elegida para seleccionar una tabla específica. Una vez que se ha hecho esta selección, el código vuelve a borrar la pantalla y muestra en pantalla la tabla que el usuario ha seleccionado.

Este proceso es fundamental porque permite a los usuarios interactuar con la base de datos de manera controlada y segura, permitiéndoles realizar operaciones específicas en las tablas según lo requieran.

`023-seleccion de opcion.py`

```python
import sqlite3

print("\033[2J")  # Borrar pantalla
print("\033[0;0H", end="")
print("Programa de gestión")
print("Selecciona una entidad:")

basededatos = sqlite3.connect("empresa.db")
cursor = basededatos.cursor()
cursor.execute('''
  SELECT name 
  FROM sqlite_master 
  WHERE type='table'
  ORDER BY name;
  ''')
contador = 1
filas = cursor.fetchall()
tabla = ""
tablas = [0]
for fila in filas:
  print(str(contador)+"-"+fila[0])
  contador += 1
  tablas.append(fila[0])
opcion = input("Tu opción elegida: ")
tabla = tablas[int(opcion)]
print("\033[2J")  # Borrar pantalla
print("\033[0;0H", end="")
print("La tabla seleccionada es: "+tabla)
```

### siguientes opciones
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es parte de un programa en Python que interactúa con una base de datos SQLite llamada `empresa.db`. El código inicia borrando la pantalla y presentándole al usuario un menú donde debe seleccionar entre las tablas disponibles en la base de datos. Para lograr esto, el programa conecta a la base de datos utilizando la librería `sqlite3`, consulta los nombres de todas las tablas que están en ella y luego muestra una lista numerada de estas.

Después de que el usuario elige una tabla (ingresando un número asociado), se borra nuevamente la pantalla y se presenta al usuario otro menú donde puede seleccionar entre diferentes operaciones CRUD (Crear, Leer, Actualizar, Borrar) que se pueden realizar sobre la tabla elegida.

Este tipo de interacción es importante en aplicaciones de gestión de base de datos ya que permite a los usuarios interactuar directamente con la estructura y el contenido de la base de datos sin necesidad de tener conocimientos detallados de SQL.

`024-siguientes opciones.py`

```python
import sqlite3

print("\033[2J")  # Borrar pantalla
print("\033[0;0H", end="")
print("Programa de gestión")
print("Selecciona una entidad:")

basededatos = sqlite3.connect("empresa.db")
cursor = basededatos.cursor()
cursor.execute('''
  SELECT name 
  FROM sqlite_master 
  WHERE type='table'
  ORDER BY name;
  ''')
contador = 1
filas = cursor.fetchall()
tabla = ""
tablas = [0]
for fila in filas:
  print(str(contador)+"-"+fila[0])
  contador += 1
  tablas.append(fila[0])
opcion = input("Tu opción elegida: ")
tabla = tablas[int(opcion)]
print("\033[2J")  # Borrar pantalla
print("\033[0;0H", end="")
print("La tabla seleccionada es: "+tabla)
print("Selecciona una operación: ")
print("1.-Crear un registro")
print("2.-Listado de registros")
print("3.-Actualizar un registro")
print("4.-Eliminar un registro")
opcion = input("Selecciona una opcion: ")
```

### comentarios hasta el momento
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código es una parte de un programa de gestión en Python que utiliza la base de datos SQLite. El objetivo principal es permitir al usuario seleccionar una tabla y luego realizar operaciones básicas (crear, listar, actualizar o eliminar registros) sobre esa tabla.

El script comienza conectándose a una base de datos llamada "empresa.db" utilizando el módulo `sqlite3`. Luego muestra un menú interactivo donde se le pide al usuario que seleccione una entidad (tabla). Para esto, ejecuta una consulta para obtener todas las tablas disponibles en la base de datos y las lista. El usuario puede elegir una tabla ingresando su número correspondiente.

Una vez seleccionada la tabla, el programa muestra otro menú donde se le pide al usuario que seleccione una operación (crear, listar, actualizar o eliminar registros). Si el usuario elige "Crear un registro", el código solicita al usuario que introduzca los datos para cada columna de la tabla y luego inserta estos datos en la base de datos.

Este tipo de interfaz es útil porque permite a los usuarios interactuar fácilmente con las tablas de una base de datos sin necesidad de entender completamente SQL o cómo funcionan las bases de datos.

`025-comentarios hasta el momento.py`

```python
import sqlite3

basededatos = sqlite3.connect("empresa.db")
cursor = basededatos.cursor()

# Pantalla de selección de entidad ############################

print("\033[2J")  # Borrar pantalla
print("\033[0;0H", end="")
print("Programa de gestión")
print("Selecciona una entidad:")

cursor.execute('''
  SELECT name 
  FROM sqlite_master 
  WHERE type='table'
  ORDER BY name;
  ''')
contador = 1
filas = cursor.fetchall()
tabla = ""
tablas = [0]
for fila in filas:
  print(str(contador)+"-"+fila[0])
  contador += 1
  tablas.append(fila[0])
opcion = input("Tu opción elegida: ")
tabla = tablas[int(opcion)]

# Pantalla de selección de operación ############################

print("\033[2J")  # Borrar pantalla
print("\033[0;0H", end="")
print("La tabla seleccionada es: "+tabla)
print("Selecciona una operación: ")
print("1.-Crear un registro")
print("2.-Listado de registros")
print("3.-Actualizar un registro")
print("4.-Eliminar un registro")
opcion = int(input("Selecciona una opcion: "))

# Pantalla de operación ############################

print("\033[2J")  # Borrar pantalla
print("\033[0;0H", end="")
if opcion == 1:
  print("Insertamos un registro nuevo")
  cursor.execute('''
    PRAGMA table_info('''+tabla+''');
    ''')
  filas = cursor.fetchall()
  columnas = []
  for fila in filas:
    columnas.append(input("Introduce nuevo dato para "+fila[1]+": "))
  print(columnas)
  nombres_columnas = [f[1] for f in filas]

  # INSERT dinámico con placeholders
  placeholders = ",".join(["?"] * len(nombres_columnas))
  sql = f"INSERT INTO {tabla} ({','.join(nombres_columnas)}) VALUES ({placeholders})"

  cursor.execute(sql, columnas)
  basededatos.commit()
  print("Registro insertado.")
elif opcion == 2:
  print("Listamos los registros")
elif opcion == 3:
  print("Actualizamos un registro")
elif opcion == 4:
  print("Eliminamos un registro")
  
  
  
  
  
  
  
```

### aplicacion hasta el momento
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código es una parte de un programa de gestión que permite a un usuario interactuar con una base de datos SQLite. En primer lugar, el programa conecta a la base de datos y obtiene una lista de todas las tablas disponibles en ella. Luego, muestra al usuario estas tablas para que pueda seleccionar sobre cuál desea operar.

Después de que el usuario selecciona una tabla, se presenta otra pantalla donde puede elegir entre cuatro tipos de operaciones: crear un registro nuevo, listar los registros existentes, actualizar un registro o eliminar un registro. El código muestra cómo manejar la opción de "Crear un registro", mostrando al usuario cuáles son las columnas disponibles en la tabla seleccionada y solicitándole que introduzca nuevos datos para cada columna.

El programa utiliza el comando SQL `PRAGMA table_info` para obtener información sobre todas las columnas de la tabla seleccionada. Luego, genera una consulta INSERT dinámica basada en los nombres de las columnas obtenidas, permitiendo al usuario ingresar datos nuevos que serán insertados en la base de datos.

Esta parte del código es importante porque demuestra cómo interactuar con una base de datos de manera segura y flexible utilizando SQL, mostrando cómo manejar consultas dinámicas basadas en el contexto actual (en este caso, las columnas de la tabla seleccionada por el usuario).

`026-aplicacion hasta el momento.py`

```python
import sqlite3

basededatos = sqlite3.connect("empresa.db")
cursor = basededatos.cursor()

# Pantalla de selección de entidad ############################

print("\033[2J")  # Borrar pantalla
print("\033[0;0H", end="")
print("Programa de gestión")
print("Selecciona una entidad:")

cursor.execute('''
  SELECT name 
  FROM sqlite_master 
  WHERE type='table'
  ORDER BY name;
  ''')
contador = 1
filas = cursor.fetchall()
tabla = ""
tablas = [0]
for fila in filas:
  print(str(contador)+"-"+fila[0])
  contador += 1
  tablas.append(fila[0])
opcion = input("Tu opción elegida: ")
tabla = tablas[int(opcion)]

# Pantalla de selección de operación ############################

print("\033[2J")  # Borrar pantalla
print("\033[0;0H", end="")
print("La tabla seleccionada es: "+tabla)
print("Selecciona una operación: ")
print("1.-Crear un registro")
print("2.-Listado de registros")
print("3.-Actualizar un registro")
print("4.-Eliminar un registro")
opcion = int(input("Selecciona una opcion: "))

# Pantalla de operación ############################

print("\033[2J")  # Borrar pantalla
print("\033[0;0H", end="")
if opcion == 1:
  print("Insertamos un registro nuevo")
  cursor.execute('''
    PRAGMA table_info('''+tabla+''');
    ''')
  filas = cursor.fetchall()
  columnas = []
  for fila in filas:
    columnas.append(input("Introduce nuevo dato para "+fila[1]+": "))
  print(columnas)
  nombres_columnas = [f[1] for f in filas]

  # INSERT dinámico con placeholders
  placeholders = ",".join(["?"] * len(nombres_columnas))
  sql = f"INSERT INTO {tabla} ({','.join(nombres_columnas)}) VALUES ({placeholders})"

  cursor.execute(sql, columnas)
  basededatos.commit()
  print("Registro insertado.")
elif opcion == 2:
  print("Listamos los registros")
elif opcion == 3:
  print("Actualizamos un registro")
elif opcion == 4:
  print("Eliminamos un registro")
  
  
  
  
  
  
  
```

### bucle infinito
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es una parte del programa que permite al usuario gestionar una base de datos SQLite interactivamente. En primer lugar, el programa conecta a la base de datos "empresa.db" y prepara un cursor para ejecutar comandos SQL.

El código utiliza un bucle infinito (`while True:`) que muestra al usuario una serie de menús. Primero, presenta una lista de todas las tablas disponibles en la base de datos, permitiendo al usuario seleccionar una tabla específica. Luego, muestra otra pantalla donde el usuario puede elegir qué operación realizar sobre la tabla seleccionada: crear un registro nuevo, listar registros existentes, actualizar un registro o eliminar un registro.

Después de que el usuario hace su selección en ambos menús, se ejecuta código específico para la operación elegida. En este ejemplo, solo se implementa detalladamente el caso donde el usuario desea crear un registro nuevo (opción 1). El programa solicita al usuario los valores para cada columna en la tabla y luego ejecuta una sentencia SQL `INSERT` con estos valores.

Es importante destacar que el código borra la pantalla antes de mostrar cada menú usando secuencias de escape ANSI, lo que mejora la experiencia del usuario proporcionando un entorno limpio y claro para las interacciones.

`027-bucle infinito.py`

```python
import sqlite3

basededatos = sqlite3.connect("empresa.db")
cursor = basededatos.cursor()
while True:
  # Pantalla de selección de entidad ############################

  print("\033[2J")  # Borrar pantalla
  print("\033[0;0H", end="")
  print("Programa de gestión")
  print("Selecciona una entidad:")

  cursor.execute('''
    SELECT name 
    FROM sqlite_master 
    WHERE type='table'
    ORDER BY name;
    ''')
  contador = 1
  filas = cursor.fetchall()
  tabla = ""
  tablas = [0]
  for fila in filas:
    print(str(contador)+"-"+fila[0])
    contador += 1
    tablas.append(fila[0])
  opcion = input("Tu opción elegida: ")
  tabla = tablas[int(opcion)]

  # Pantalla de selección de operación ############################

  print("\033[2J")  # Borrar pantalla
  print("\033[0;0H", end="")
  print("La tabla seleccionada es: "+tabla)
  print("Selecciona una operación: ")
  print("1.-Crear un registro")
  print("2.-Listado de registros")
  print("3.-Actualizar un registro")
  print("4.-Eliminar un registro")
  opcion = int(input("Selecciona una opcion: "))

  # Pantalla de operación ############################

  print("\033[2J")  # Borrar pantalla
  print("\033[0;0H", end="")
  if opcion == 1:
    print("Insertamos un registro nuevo")
    cursor.execute('''
      PRAGMA table_info('''+tabla+''');
      ''')
    filas = cursor.fetchall()
    columnas = []
    for fila in filas:
      columnas.append(input("Introduce nuevo dato para "+fila[1]+": "))
    print(columnas)
    nombres_columnas = [f[1] for f in filas]

    # INSERT dinámico con placeholders
    placeholders = ",".join(["?"] * len(nombres_columnas))
    sql = f"INSERT INTO {tabla} ({','.join(nombres_columnas)}) VALUES ({placeholders})"

    cursor.execute(sql, columnas)
    basededatos.commit()
    print("Registro insertado.")
  elif opcion == 2:
    print("Listamos los registros")
  elif opcion == 3:
    print("Actualizamos un registro")
  elif opcion == 4:
    print("Eliminamos un registro")
  
  
  
  
  
  
  
```

### pantalla de bienvenida
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código es una parte de un programa en Python que interactúa con una base de datos SQLite para gestionar diferentes entidades (tablas) y operaciones sobre ellas. El objetivo principal del fragmento es proporcionar al usuario un menú interactivo donde puede seleccionar una tabla existente y luego realizar diversas operaciones CRUD (Crear, Leer, Actualizar, Borrar).

1. **Conexión a la base de datos**: Al inicio del código, se establece una conexión con la base de datos SQLite llamada "empresa.db" utilizando el módulo `sqlite3`. Esto permite al programa interactuar con los datos almacenados en esta base de datos.

2. **Menú principal y selección de entidad**: El programa muestra un menú para que el usuario elija entre diferentes tablas disponibles en la base de datos. Utiliza comandos SQL para obtener una lista de todas las tablas existentes en la base de datos y luego presenta estas opciones al usuario.

3. **Selección de operación sobre la entidad**: Una vez seleccionada una tabla, se muestra un menú donde el usuario puede elegir entre crear (insertar) un nuevo registro, listar registros existentes, actualizar un registro o eliminar un registro en dicha tabla.

4. **Ejecución de operaciones CRUD**:
   - **Crear un registro (Insertar)**: Si el usuario selecciona la opción 1, se le pedirá que introduzca valores para cada columna de la tabla y luego se ejecutará una consulta SQL `INSERT INTO` dinámica con los valores proporcionados.
   - Para las demás operaciones CRUD (leer, actualizar, eliminar), el código muestra mensajes informativos indicando qué tipo de acción se va a realizar pero no implementa específicamente cómo se realizan estas acciones en este fragmento.

La funcionalidad de borrar la pantalla antes de mostrar cada menú y mensaje al usuario es gestionada mediante secuencias de escape ANSI (`\033[2J` para borrar toda la pantalla, `\033[0;0H` para mover el cursor a la posición inicial).

Este tipo de interfaz permite una interacción sencilla y directa con la base de datos para tareas administrativas básicas.

`028-pantalla de bienvenida.py`

```python
import sqlite3

basededatos = sqlite3.connect("empresa.db")
cursor = basededatos.cursor()

print("\033[2J")  # Borrar pantalla
print("\033[0;0H", end="")
print("Programa de gestión")
print("(c) 2025 Jose Vicente Carratala")
input("Pulsa una tecla para continuar...")

while True:
  # Pantalla de selección de entidad ############################

  print("\033[2J")  # Borrar pantalla
  print("\033[0;0H", end="")

  print("Selecciona una entidad:")

  cursor.execute('''
    SELECT name 
    FROM sqlite_master 
    WHERE type='table'
    ORDER BY name;
    ''')
  contador = 1
  filas = cursor.fetchall()
  tabla = ""
  tablas = [0]
  for fila in filas:
    print(str(contador)+"-"+fila[0])
    contador += 1
    tablas.append(fila[0])
  opcion = input("Tu opción elegida: ")
  tabla = tablas[int(opcion)]

  # Pantalla de selección de operación ############################

  print("\033[2J")  # Borrar pantalla
  print("\033[0;0H", end="")
  print("La tabla seleccionada es: "+tabla)
  print("Selecciona una operación: ")
  print("1.-Crear un registro")
  print("2.-Listado de registros")
  print("3.-Actualizar un registro")
  print("4.-Eliminar un registro")
  opcion = int(input("Selecciona una opcion: "))

  # Pantalla de operación ############################

  print("\033[2J")  # Borrar pantalla
  print("\033[0;0H", end="")
  if opcion == 1:
    print("Insertamos un registro nuevo")
    cursor.execute('''
      PRAGMA table_info('''+tabla+''');
      ''')
    filas = cursor.fetchall()
    columnas = []
    for fila in filas:
      columnas.append(input("Introduce nuevo dato para "+fila[1]+": "))
    print(columnas)
    nombres_columnas = [f[1] for f in filas]

    # INSERT dinámico con placeholders
    placeholders = ",".join(["?"] * len(nombres_columnas))
    sql = f"INSERT INTO {tabla} ({','.join(nombres_columnas)}) VALUES ({placeholders})"

    cursor.execute(sql, columnas)
    basededatos.commit()
    print("Registro insertado.")
  elif opcion == 2:
    print("Listamos los registros")
  elif opcion == 3:
    print("Actualizamos un registro")
  elif opcion == 4:
    print("Eliminamos un registro")
  
  
  
  
  
  
  
```

### desarrollo manual de listados
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es parte de un programa en Python que interactúa con una base de datos SQLite para gestionar tablas y registros. El programa primero conecta a la base de datos "empresa.db" y crea un cursor para ejecutar consultas SQL.

El código muestra una estructura de menú interactiva que permite al usuario seleccionar diferentes operaciones en la base de datos. Primero, el programa presenta una lista de todas las tablas disponibles en la base de datos, obtenidas mediante una consulta a la tabla `sqlite_master`. Luego, solicita que el usuario seleccione una tabla y muestra opciones para crear un registro nuevo, listar registros existentes, actualizar o eliminar un registro.

Cuando se selecciona la opción "Crear un registro", el programa recoge los valores necesarios para cada columna de la tabla elegida por el usuario. Utiliza una consulta `PRAGMA table_info` para obtener información sobre las columnas y luego solicita al usuario que introduzca datos para cada una de estas columnas. Finalmente, ejecuta una instrucción SQL INSERT con placeholders (marcadores de posición) para insertar los nuevos datos en la tabla.

Este código es importante porque proporciona una interfaz sencilla para interactuar con datos en una base de datos SQLite, facilitando a los usuarios realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sin necesidad de tener conocimientos avanzados de SQL.

`029-desarrollo manual de listados.py`

```python
import sqlite3

basededatos = sqlite3.connect("empresa.db")
cursor = basededatos.cursor()

print("\033[2J")  # Borrar pantalla
print("\033[0;0H", end="")
print("Programa de gestión")
print("(c) 2025 Jose Vicente Carratala")
input("Pulsa una tecla para continuar...")

while True:
  # Pantalla de selección de entidad ############################

  print("\033[2J")  # Borrar pantalla
  print("\033[0;0H", end="")

  print("Selecciona una entidad:")

  cursor.execute('''
    SELECT name 
    FROM sqlite_master 
    WHERE type='table'
    ORDER BY name;
    ''')
  contador = 1
  filas = cursor.fetchall()
  tabla = ""
  tablas = [0]
  for fila in filas:
    print(str(contador)+"-"+fila[0])
    contador += 1
    tablas.append(fila[0])
  opcion = input("Tu opción elegida: ")
  tabla = tablas[int(opcion)]

  # Pantalla de selección de operación ############################

  print("\033[2J")  # Borrar pantalla
  print("\033[0;0H", end="")
  print("La tabla seleccionada es: "+tabla)
  print("Selecciona una operación: ")
  print("1.-Crear un registro")
  print("2.-Listado de registros")
  print("3.-Actualizar un registro")
  print("4.-Eliminar un registro")
  opcion = int(input("Selecciona una opcion: "))

  # Pantalla de operación ############################

  print("\033[2J")  # Borrar pantalla
  print("\033[0;0H", end="")
  if opcion == 1:
    print("Insertamos un registro nuevo")
    cursor.execute('''
      PRAGMA table_info('''+tabla+''');
      ''')
    filas = cursor.fetchall()
    columnas = []
    for fila in filas:
      columnas.append(input("Introduce nuevo dato para "+fila[1]+": "))
    print(columnas)
    nombres_columnas = [f[1] for f in filas]

    # INSERT dinámico con placeholders
    placeholders = ",".join(["?"] * len(nombres_columnas))
    sql = f"INSERT INTO {tabla} ({','.join(nombres_columnas)}) VALUES ({placeholders})"

    cursor.execute(sql, columnas)
    basededatos.commit()
    print("Registro insertado.")
  elif opcion == 2:
    print("Listamos los registros")
    cursor.execute('''
      SELECT * FROM '''+tabla+''';
      ''')
    filas = cursor.fetchall()
    for fila in filas:
      print(fila)
    input("Pulsa una tecla para continuar...")
  elif opcion == 3:
    print("Actualizamos un registro")
  elif opcion == 4:
    print("Eliminamos un registro")
  
  
  
  
  
  
  
```

### ayuda de la inteligencia artificial
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

El script proporcionado es un programa interactivo en Python que permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) en una base de datos SQLite utilizando una interfaz terminal. El programa está estructurado de manera modular para facilitar su mantenimiento y extensión.

### Resumen del Programa

1. **Conexión a la Base de Datos**: Se conecta a una base de datos SQLite llamada `database.db`.
2. **Interfaz de Usuario**: Proporciona un menú interactivo que permite seleccionar operaciones CRUD y cambiar entre diferentes tablas.
3. **Operaciones CRUD**:
   - **Crear (Insertar)**: Permite insertar nuevos registros en la tabla seleccionada, proporcionando valores para cada columna.
   - **Leer (Listar)**: Muestra todos los registros de la tabla seleccionada con paginación.
   - **Actualizar**: Actualiza un registro existente basado en su clave primaria y permite editar las columnas no primarias.
   - **Eliminar**: Elimina un registro existente basado en su clave primaria.

### Detalle del Codigo

#### Conexión a la Base de Datos
```python
def connect(DB_PATH):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    return con, cur
```

El método `connect` se encarga de establecer una conexión con la base de datos y crear un objeto cursor para ejecutar consultas.

#### Menús Interactivos
```python
def select_table(cur):
    while True:
        tables = list_tables(cur)
        if not tables:
            error("No hay tablas en la base de datos.")
            pause()
            sys.exit(0)

        for i, t in enumerate(tables, 1):
            print(f"{FG_CYAN}{i:>2}{RESET} {VL} {t}")
        op = ask_int("Tu opción elegida: ", minv=1, maxv=len(tables))
        return tables[op - 1]
```

El método `select_table` muestra una lista de tablas disponibles y permite al usuario seleccionar una tabla.

#### CRUD Operations
- **Crear Registro**
```python
def op_create(cur, con, table):
    cols = table_info(cur, table)
    names = column_names(cols)

    placeholders = ",".join(["?"] * len(names))
    sql = f"INSERT INTO {table} ({','.join(names)}) VALUES ({placeholders})"
    
    try:
        cur.execute(sql, values)
        con.commit()
        success("Registro insertado.")
    except sqlite3.Error as e:
        error(f"No se pudo insertar: {e}")
```

- **Leer Registros**
```python
def op_list(cur, table):
    cols = table_info(cur, table)
    names = column_names(cols)

    try:
        cur.execute(f"SELECT {', '.join(names)} FROM {table};")
        rows = cur.fetchall()
        paginated_print(names, rows)
    except sqlite3.Error as e:
        error(f"No se pudo listar: {e}")
```

- **Actualizar Registro**
```python
def op_update(cur, con, table):
    cols = table_info(cur, table)
    names = column_names(cols)
    pk_cols = primary_keys(cols)

    set_clause = ", ".join([f"{n}=?" for n in names if n not in pk_cols])
    where = " AND ".join([f"{c}=?" for c in pk_cols])

    sql = f"UPDATE {table} SET {set_clause} WHERE {where};"
    
    try:
        cur.execute(sql, params)
        con.commit()
        success(f"Filas afectadas: {cur.rowcount}")
    except sqlite3.Error as e:
        error(f"No se pudo actualizar: {e}")
```

- **Eliminar Registro**
```python
def op_delete(cur, con, table):
    cols = table_info(cur, table)
    names = column_names(cols)
    pk_cols = primary_keys(cols)

    where = " AND ".join([f"{c}=?" for c in pk_cols])
    sql = f"DELETE FROM {table} WHERE {where};"
    
    try:
        cur.execute(sql, params)
        con.commit()
        success(f"Filas afectadas: {cur.rowcount}")
    except sqlite3.Error as e:
        error(f"No se pudo eliminar: {e}")
```

### Ejecución Principal
```python
def main():
    con = connect(DB_PATH)
    cur = con.cursor()

    current_table = None

    while True:
        if not current_table:
            current_table = select_table(cur)

        op = select_operation(current_table)
        if op == 0: break
        elif op == 1: op_create(cur, con, current_table)
        elif op == 2: op_list(cur, current_table)
        elif op == 3: op_update(cur, con, current_table)
        elif op == 4: op_delete(cur, con, current_table)
        elif op == 5: current_table = None

    try:
        con.close()
    except Exception as e:
        print(f"Error al cerrar la conexión: {e}")
```

El método `main` es el punto de entrada principal del programa. Establece una conexión a la base de datos, muestra un menú interactivo para seleccionar operaciones CRUD y tablas, y gestiona las excepciones.

### Uso

1. **Instalar Dependencias**: Asegurarse de que SQLite esté instalado en el sistema.
2. **Ejecutar Programa**:
   ```sh
   python3 database_manager.py
   ```

Este script proporciona una interfaz sencilla y eficiente para gestionar datos en una base de datos SQLite desde la línea de comandos.

`030-ayuda de la inteligencia artificial.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
import sys
from textwrap import shorten

DB_PATH = "empresa.db"

# =======================
# ANSI / Estilo consola
# =======================
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDER = "\033[4m"

FG_BLACK   = "\033[30m"
FG_RED     = "\033[31m"
FG_GREEN   = "\033[32m"
FG_YELLOW  = "\033[33m"
FG_BLUE    = "\033[34m"
FG_MAGENTA = "\033[35m"
FG_CYAN    = "\033[36m"
FG_WHITE   = "\033[37m"

BG_BLACK   = "\033[40m"
BG_RED     = "\033[41m"
BG_GREEN   = "\033[42m"
BG_YELLOW  = "\033[43m"
BG_BLUE    = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN    = "\033[46m"
BG_WHITE   = "\033[47m"

CLEAR = "\033[2J"
HOME = "\033[0;0H"

# Box-drawing
HL = "─"
VL = "│"
TL = "┌"
TR = "┐"
BL = "└"
BR = "┘"
TJ = "┬"
BJ = "┴"
LJ = "├"
RJ = "┤"
CJ = "┼"

PAGE_SIZE = 20
TRUNC = 40  # truncado visual por celda

def cls():
    print(CLEAR + HOME, end="")

def banner():
    title = f"{BOLD}{FG_CYAN}Programa de gestión{RESET}"
    author = f"{DIM}(c) 2025 Jose Vicente Carratala{RESET}"
    bar = HL * 60
    print(f"{TL}{bar}{TR}")
    print(f"{VL} {title:<58}{VL}")
    print(f"{VL} {author:<58}{VL}")
    print(f"{BL}{bar}{BR}")

def pause(msg="Pulsa una tecla para continuar..."):
    try:
        input(f"{DIM}{msg}{RESET}")
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)

def error(msg):
    print(f"{FG_RED}{BOLD}✗ {msg}{RESET}")

def success(msg):
    print(f"{FG_GREEN}{BOLD}✓ {msg}{RESET}")

def info(msg):
    print(f"{FG_CYAN}{msg}{RESET}")

def ask(prompt):
    return input(f"{FG_YELLOW}? {prompt}{RESET}")

def ask_int(prompt, minv=None, maxv=None):
    while True:
        val = input(f"{FG_YELLOW}? {prompt}{RESET}")
        try:
            n = int(val)
            if minv is not None and n < minv:
                error(f"El valor debe ser ≥ {minv}.")
                continue
            if maxv is not None and n > maxv:
                error(f"El valor debe ser ≤ {maxv}.")
                continue
            return n
        except ValueError:
            error("Introduce un número válido.")

def connect(db_path):
    try:
        return sqlite3.connect(db_path)
    except sqlite3.Error as e:
        error(f"No se pudo abrir la BD: {e}")
        sys.exit(1)

# =======================
# Utilidades de esquema
# =======================
def list_tables(cur):
    cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)
    return [r[0] for r in cur.fetchall()]

def table_info(cur, table):
    cur.execute(f"PRAGMA table_info({table});")
    # cid, name, type, notnull, dflt_value, pk
    cols = cur.fetchall()
    return cols

def primary_keys(columns_info):
    # Devuelve lista de nombres de columnas que forman la PK (orden por cid/PRAGMA)
    pks = [c[1] for c in columns_info if c[5] > 0]
    # PRAGMA pk>0 indica orden, así que ordenamos por c[5]
    pks = [c[1] for c in sorted(columns_info, key=lambda x: x[5] if x[5] else 0) if c[5] > 0]
    return pks

def column_names(columns_info):
    return [c[1] for c in columns_info]

def is_integer_pk_autoinc(columns_info, col_name):
    # Heurística: tipo contiene "INT" y es PK
    for c in columns_info:
        if c[1] == col_name:
            return c[5] > 0 and "INT" in (c[2] or "").upper()
    return False

# =======================
# Render de tablas
# =======================
def format_table(headers, rows, max_width=TRUNC):
    # calcular anchos
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            cell_s = "" if cell is None else str(cell)
            lw = len(cell_s)
            if lw > max_width:
                lw = max_width
            if lw > widths[i]:
                widths[i] = lw

    def hline(left, mid, right):
        parts = []
        for w in widths:
            parts.append(HL * (w + 2))
        return left + mid.join(parts) + right

    def render_row(values):
        cells = []
        for i, v in enumerate(values):
            s = "" if v is None else str(v)
            s = shorten(s, width=widths[i], placeholder="…") if len(s) > widths[i] else s
            cells.append(f" {s:<{widths[i]}} ")
        return VL + VL.join(cells) + VL

    top = hline(TL, TJ, TR)
    sep = hline(LJ, CJ, RJ)
    bot = hline(BL, BJ, BR)

    lines = [top, render_row([f"{BOLD}{h}{RESET}" for h in headers]), sep]
    for r in rows:
        lines.append(render_row(r))
    lines.append(bot)
    return "\n".join(lines)

def paginated_print(headers, rows):
    if not rows:
        info("No hay registros.")
        return
    total = len(rows)
    page = 0
    while True:
        cls()
        banner()
        start = page * PAGE_SIZE
        end = min(start + PAGE_SIZE, total)
        subset = rows[start:end]
        print(f"{DIM}Mostrando {start+1}-{end} de {total}{RESET}\n")
        print(format_table(headers, subset))
        print()
        cmd = input(f"{DIM}[N]ext, [P]rev, [Q]uit ▶ {RESET}").strip().lower()
        if cmd in ("q", ""):
            break
        if cmd == "n" and end < total:
            page += 1
        elif cmd == "p" and page > 0:
            page -= 1

# =======================
# CRUD Operations
# =======================
def op_create(cur, con, table):
    cls()
    banner()
    print(f"{BOLD}Insertar en {table}{RESET}\n")
    cols = table_info(cur, table)
    names = column_names(cols)
    values = []
    for c in cols:
        name, ctype, notnull, dflt, pk = c[1], c[2], c[3], c[4], c[5]
        hint = []
        if pk: hint.append("PK")
        if notnull and dflt is None: hint.append("NOT NULL")
        if dflt is not None: hint.append(f"DEF={dflt}")
        if ctype: hint.append(ctype)
        tag = f" ({', '.join(hint)})" if hint else ""
        val = input(f"{FG_YELLOW}· {name}{RESET}{DIM}{tag}{RESET} (Enter=NULL): ").strip()
        if val == "":
            values.append(None)
        else:
            values.append(val)

    placeholders = ",".join(["?"] * len(names))
    sql = f"INSERT INTO {table} ({','.join(names)}) VALUES ({placeholders})"
    try:
        cur.execute(sql, values)
        con.commit()
        success("Registro insertado.")
    except sqlite3.Error as e:
        error(f"No se pudo insertar: {e}")
    pause()

def op_list(cur, table):
    cls()
    banner()
    print(f"{BOLD}Listado de {table}{RESET}\n")
    cols = table_info(cur, table)
    names = column_names(cols)
    try:
        cur.execute(f"SELECT {', '.join(names)} FROM {table};")
        rows = cur.fetchall()
        paginated_print(names, rows)
    except sqlite3.Error as e:
        error(f"No se pudo listar: {e}")
        pause()

def read_by_pk(cur, table, pk_cols, pk_values):
    where = " AND ".join([f"{c}=?" for c in pk_cols])
    sql = f"SELECT * FROM {table} WHERE {where} LIMIT 1;"
    cur.execute(sql, pk_values)
    return cur.fetchone()

def op_update(cur, con, table):
    cls()
    banner()
    print(f"{BOLD}Actualizar en {table}{RESET}\n")
    cols = table_info(cur, table)
    names = column_names(cols)
    pk_cols = primary_keys(cols)
    if not pk_cols:
        error("Esta tabla no tiene clave primaria definida. Actualización no soportada.")
        return pause()

    # Pedir PK(s)
    pk_values = []
    print(f"{FG_CYAN}Introduce la clave primaria para localizar el registro:{RESET}")
    for pk in pk_cols:
        v = input(f"· {pk}: ").strip()
        if v == "":
            error("La clave primaria no puede quedar vacía.")
            return pause()
        pk_values.append(v)

    # Leer registro actual
    row = read_by_pk(cur, table, pk_cols, pk_values)
    if not row:
        error("No se encontró el registro con esa PK.")
        return pause()

    # Mostrar registro actual
    print("\nRegistro actual:")
    print(format_table(names, [row]))
    print()

    # Solicitar nuevos valores (Enter = mantener)
    new_values = []
    for i, c in enumerate(cols):
        cname = c[1]
        current = row[i]
        if cname in pk_cols:
            # Bloqueamos edición de PK por simplicidad (se podría permitir)
            print(f"{DIM}{cname} (PK) = {current} (no editable){RESET}")
            new_values.append(current)
        else:
            val = input(f"{FG_YELLOW}· {cname}{RESET} {DIM}[actual: {current}]{RESET} (Enter=mantener): ")
            if val.strip() == "":
                new_values.append(current)
            else:
                new_values.append(val)

    # Construir UPDATE
    set_clause = ", ".join([f"{n}=?" for n in names if n not in pk_cols])
    where = " AND ".join([f"{c}=?" for c in pk_cols])
    params = [new_values[names.index(n)] for n in names if n not in pk_cols] + pk_values

    sql = f"UPDATE {table} SET {set_clause} WHERE {where};"
    try:
        cur.execute(sql, params)
        con.commit()
        success(f"Filas afectadas: {cur.rowcount}")
    except sqlite3.Error as e:
        error(f"No se pudo actualizar: {e}")
    pause()

def op_delete(cur, con, table):
    cls()
    banner()
    print(f"{BOLD}Eliminar en {table}{RESET}\n")
    cols = table_info(cur, table)
    names = column_names(cols)
    pk_cols = primary_keys(cols)
    if not pk_cols:
        error("Esta tabla no tiene clave primaria definida. Eliminación no soportada.")
        return pause()

    # Pedir PK(s)
    pk_values = []
    print(f"{FG_CYAN}Introduce la clave primaria del registro a eliminar:{RESET}")
    for pk in pk_cols:
        v = input(f"· {pk}: ").strip()
        if v == "":
            error("La clave primaria no puede quedar vacía.")
            return pause()
        pk_values.append(v)

    # Confirmación mostrando el registro
    row = read_by_pk(cur, table, pk_cols, pk_values)
    if not row:
        error("No se encontró el registro con esa PK.")
        return pause()

    print("\nRegistro a eliminar:")
    print(format_table(names, [row]))
    print()
    conf = input(f"{FG_RED}{BOLD}¿Seguro que deseas eliminarlo? (s/N): {RESET}").strip().lower()
    if conf != "s":
        info("Cancelado.")
        return pause()

    where = " AND ".join([f"{c}=?" for c in pk_cols])
    sql = f"DELETE FROM {table} WHERE {where};"
    try:
        cur.execute(sql, pk_values)
        con.commit()
        success(f"Filas afectadas: {cur.rowcount}")
    except sqlite3.Error as e:
        error(f"No se pudo eliminar: {e}")
    pause()

# =======================
# Menús
# =======================
def select_table(cur):
    while True:
        cls()
        banner()
        print(f"{BOLD}Selecciona una entidad (tabla){RESET}\n")
        tables = list_tables(cur)
        if not tables:
            error("No hay tablas en la base de datos.")
            pause("Crea alguna tabla y vuelve a ejecutar. Pulsa una tecla…")
            sys.exit(0)

        for i, t in enumerate(tables, 1):
            print(f"{FG_CYAN}{i:>2}{RESET} {VL} {t}")
        print()
        op = ask_int("Tu opción elegida: ", minv=1, maxv=len(tables))
        return tables[op - 1]

def select_operation(table):
    cls()
    banner()
    print(f"{BOLD}Tabla seleccionada: {FG_GREEN}{table}{RESET}\n")
    print(f"{BOLD}Selecciona una operación:{RESET}")
    print(f"  {FG_CYAN}1{RESET} {VL} Crear un registro")
    print(f"  {FG_CYAN}2{RESET} {VL} Listado de registros")
    print(f"  {FG_CYAN}3{RESET} {VL} Actualizar un registro")
    print(f"  {FG_CYAN}4{RESET} {VL} Eliminar un registro")
    print(f"  {FG_CYAN}5{RESET} {VL} Cambiar de tabla")
    print(f"  {FG_CYAN}0{RESET} {VL} Salir")
    print()
    return ask_int("Selecciona una opción: ", minv=0, maxv=5)

# =======================
# Main loop
# =======================
def main():
    con = connect(DB_PATH)
    cur = con.cursor()

    cls()
    banner()
    pause()

    current_table = None

    while True:
        if not current_table:
            current_table = select_table(cur)

        op = select_operation(current_table)
        if op == 0:
            cls()
            info("Hasta pronto 👋")
            break
        elif op == 1:
            op_create(cur, con, current_table)
        elif op == 2:
            op_list(cur, current_table)
        elif op == 3:
            op_update(cur, con, current_table)
        elif op == 4:
            op_delete(cur, con, current_table)
        elif op == 5:
            current_table = None

    try:
        con.close()
    except Exception:
        pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cls()
        info("Interrumpido por el usuario.")
```

### mas mejoras
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este script es una aplicación de consola en Python que proporciona un menú interactivo para realizar operaciones CRUD (Crear, Leer, Actualizar y Borrar) en una base de datos SQLite. La aplicación utiliza colores y símbolos para mejorar la experiencia del usuario. A continuación, te presento una explicación detallada de las principales partes del código:

### 1. Funciones de Estilo y Presentación

El script incluye funciones que manejan el estilo de texto en la consola (colores, símbolos, etc.) para hacer la interfaz más atractiva.

```python
def cls():
    os.system("cls" if os.name == "nt" else "clear")

def apply_theme():
    print(CLEARSCREEN)
```

Estas funciones se usan para limpiar la pantalla y aplicar un tema de colores, respectivamente.

### 2. Conexión a la Base de Datos

El script conecta a una base de datos SQLite llamada `DB_PATH`.

```python
def connect(DB_PATH):
    return sqlite3.connect(DB_PATH)

con = connect("mydatabase.db")
cur = con.cursor()
```

`connect()` es un wrapper alrededor del método de conexión de SQLite. En el ejemplo, se utiliza "mydatabase.db" como la ruta a la base de datos.

### 3. Menús y Selección de Tablas

El script tiene funciones que muestran menús interactivos para seleccionar una tabla o operación:

```python
def select_table(cur):
    tables = list_tables(cur)
    # Muestra las tablas disponibles en el menú
```

`list_tables()` es una función personalizada que recupera la lista de todas las tablas existentes en la base de datos.

### 4. CRUD Operations

El script incluye funciones específicas para cada operación CRUD:

- **Crear (Insertar)**: `op_create(cur, con, table)`, solicita al usuario los valores necesarios para crear un nuevo registro.
  
- **Leer (Listado)**: `op_list(cur, table)` lista todos los registros de una tabla específica.

- **Actualizar**: `op_update(cur, con, table)` permite actualizar un registro existente.

- **Eliminar**: `op_delete(cur, con, table)` elimina un registro específico basándose en la clave primaria.

### 5. Menú Principal y Ciclo de Ejecución

El script incluye una función principal que maneja el ciclo de ejecución del menú interactivo:

```python
def main():
    # Conecta a la base de datos
    con = connect(DB_PATH)
    cur = con.cursor()

    # Cuerpo del programa: muestra los menús y realiza las operaciones según la opción seleccionada.
    
    while True:
        op = select_operation(current_table)  # Muestra el menú principal

        if op == 0:
            break
        elif op == 1:
            op_create(cur, con, current_table)
        elif op == 2:
            op_list(cur, current_table)
        elif op == 3:
            op_update(cur, con, current_table)
        elif op == 4:
            op_delete(cur, con, current_table)
        elif op == 5:
            # Cambiar a otra tabla
```

### Ejecución del Script

El script se ejecuta desde `if __name__ == "__main__"` y maneja excepciones para permitir que el usuario interrumpa la aplicación.

```python
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cls(); apply_theme()
        info("Interrumpido por el usuario.")
```

### Resumen

Este script proporciona una interfaz de línea de comandos amigable y visualmente atractiva para interactuar con una base de datos SQLite. Permite al usuario crear, leer, actualizar y eliminar registros en tablas específicas según su elección.

`031-mas mejoras.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
import sys
import re
from shutil import get_terminal_size

DB_PATH = "empresa.db"

# =======================
# ANSI / Estilo consola
# =======================
# Colores base
RESET_RAW = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
UNDER = "\033[4m"

FG_BLACK   = "\033[30m"
FG_RED     = "\033[31m"
FG_GREEN   = "\033[32m"
FG_YELLOW  = "\033[33m"
FG_BLUE    = "\033[34m"
FG_MAGENTA = "\033[35m"
FG_CYAN    = "\033[36m"
FG_WHITE   = "\033[37m"

BG_BLACK   = "\033[40m"
BG_RED     = "\033[41m"
BG_GREEN   = "\033[42m"
BG_YELLOW  = "\033[43m"
BG_BLUE    = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN    = "\033[46m"
BG_WHITE   = "\033[47m"

CLEAR = "\033[2J"
HOME = "\033[0;0H"

# Box-drawing
HL = "─"; VL = "│"; TL = "┌"; TR = "┐"; BL = "└"; BR = "┘"; TJ = "┬"; BJ = "┴"; LJ = "├"; RJ = "┤"; CJ = "┼"

# =======================
# Tema (Light por defecto)
# =======================
LIGHT_THEME = True   # pon False para no forzar blanco
ZEBRA_ROWS  = True   # alterna leve sombreado filas

THEME_FG = FG_BLACK if LIGHT_THEME else FG_WHITE
THEME_BG = BG_WHITE if LIGHT_THEME else BG_BLACK

# Importante: RESET que vuelve al tema, no al terminal por defecto
RESET = f"{RESET_RAW}{THEME_FG}{THEME_BG}"

# =======================
# Config
# =======================
PAGE_SIZE = 20
TRUNC = 40  # truncado visual por celda
TABLE_MIN_WIDTH = 20

# =======================
# Utils: longitud visible
# =======================
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

def strip_ansi(s: str) -> str:
    return ANSI_RE.sub("", s)

def vislen(s: str) -> int:
    return len(strip_ansi(s))

def pad_visible(s: str, width: int, align="left") -> str:
    """Rellena según longitud visible (ignora códigos ANSI)."""
    cur = vislen(s)
    pad = max(0, width - cur)
    if align == "right":
        return " " * pad + s
    elif align == "center":
        left = pad // 2
        right = pad - left
        return " " * left + s + " " * right
    return s + " " * pad

def truncate_visible(s: str, width: int) -> str:
    if vislen(s) <= width:
        return s
    raw = strip_ansi(s)
    if width <= 3:
        return "." * width
    return raw[: width - 3] + "..."

def term_width(default=80) -> int:
    try:
        return max(TABLE_MIN_WIDTH, get_terminal_size().columns)
    except Exception:
        return default

def cls():
    print(CLEAR + HOME + RESET, end="")

def apply_theme():
    # Establece el tema global al inicio
    print(RESET, end="")

# =======================
# Mensajería
# =======================
def banner():
    w = min(80, term_width() - 2)  # ancho cómodo
    bar = HL * w
    title = f"{BOLD}Programa de gestión{RESET}"
    author = f"{DIM}(c) 2025 Jose Vicente Carratala{RESET}"
    print(f"{THEME_FG}{THEME_BG}", end="")
    print(TL + bar + TR)
    print(VL + pad_visible(" " + title, w) + VL)
    print(VL + pad_visible(" " + author, w) + VL)
    print(BL + bar + BR)

def pause(msg="Pulsa una tecla para continuar..."):
    try:
        input(f"{DIM}{msg}{RESET}")
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)

def error(msg):
    print(f"{FG_RED}{BOLD}✗ {msg}{RESET}")

def success(msg):
    print(f"{FG_GREEN}{BOLD}✓ {msg}{RESET}")

def info(msg):
    print(f"{FG_CYAN}{msg}{RESET}")

def ask(prompt):
    return input(f"{FG_YELLOW}? {prompt}{RESET}")

def ask_int(prompt, minv=None, maxv=None):
    while True:
        val = input(f"{FG_YELLOW}? {prompt}{RESET}")
        try:
            n = int(val)
            if minv is not None and n < minv:
                error(f"El valor debe ser ≥ {minv}."); continue
            if maxv is not None and n > maxv:
                error(f"El valor debe ser ≤ {maxv}."); continue
            return n
        except ValueError:
            error("Introduce un número válido.")

# =======================
# BD helpers
# =======================
def connect(db_path):
    try:
        return sqlite3.connect(db_path)
    except sqlite3.Error as e:
        error(f"No se pudo abrir la BD: {e}")
        sys.exit(1)

def list_tables(cur):
    cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)
    return [r[0] for r in cur.fetchall()]

def table_info(cur, table):
    cur.execute(f"PRAGMA table_info({table});")
    # cid, name, type, notnull, dflt_value, pk
    return cur.fetchall()

def primary_keys(columns_info):
    # Ordenadas por índice pk (>0)
    return [c[1] for c in sorted(columns_info, key=lambda x: x[5] if x[5] else 0) if c[5] > 0]

def column_names(columns_info):
    return [c[1] for c in columns_info]

# =======================
# Render de tablas (alineación perfecta)
# =======================
def format_table(headers, rows, max_width=TRUNC):
    # calcular anchos (por longitud visible)
    widths = [max(1, vislen(str(h))) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            cell_s = "" if cell is None else str(cell)
            lw = min(vislen(cell_s), max_width)
            widths[i] = max(widths[i], lw)

    def hline(left, mid, right):
        parts = [HL * (w + 2) for w in widths]
        return left + mid.join(parts) + right

    def render_row(values, style=None, zebra=False):
        cells = []
        for i, v in enumerate(values):
            s = "" if v is None else str(v)
            s = truncate_visible(s, widths[i])
            s = pad_visible(s, widths[i])
            cells.append(" " + s + " ")
        line = VL + VL.join(cells) + VL
        if zebra:
            # leve dim en filas alternas (sin cambiar fondo)
            line = f"{DIM}{line}{RESET}"
        if style:
            line = style + line + RESET
        return line

    top = hline(TL, TJ, TR)
    sep = hline(LJ, CJ, RJ)
    bot = hline(BL, BJ, BR)

    # Encabezado invertido para contraste
    header_style = f"{BOLD}{THEME_BG}{THEME_FG}"
    lines = [top, render_row(headers, style=header_style), sep]
    for idx, r in enumerate(rows):
        zebra = ZEBRA_ROWS and (idx % 2 == 1)
        lines.append(render_row(r, zebra=zebra))
    lines.append(bot)
    return "\n".join(lines)

def paginated_print(headers, rows, title=None):
    if not rows:
        info("No hay registros.")
        return
    total = len(rows)
    page = 0
    while True:
        cls(); apply_theme(); banner()
        if title:
            print(f"{BOLD}{title}{RESET}\n")
        start = page * PAGE_SIZE
        end = min(start + PAGE_SIZE, total)
        subset = rows[start:end]
        rango = f"{DIM}Mostrando {start+1}-{end} de {total}{RESET}"
        print(rango + "\n")
        print(format_table(headers, subset))
        print()
        cmd = input(f"{DIM}[N]ext, [P]rev, [Q]uit ▶ {RESET}").strip().lower()
        if cmd in ("q", ""):
            break
        if cmd == "n" and end < total:
            page += 1
        elif cmd == "p" and page > 0:
            page -= 1

# =======================
# CRUD
# =======================
def op_create(cur, con, table):
    cls(); apply_theme(); banner()
    print(f"{BOLD}➕ Insertar en {table}{RESET}\n")
    cols = table_info(cur, table)
    names = column_names(cols)
    values = []
    for c in cols:
        name, ctype, notnull, dflt, pk = c[1], c[2], c[3], c[4], c[5]
        hint = []
        if pk: hint.append("PK")
        if notnull and dflt is None: hint.append("NOT NULL")
        if dflt is not None: hint.append(f"DEF={dflt}")
        if ctype: hint.append(ctype)
        tag = f" ({', '.join(hint)})" if hint else ""
        val = input(f"{FG_YELLOW}· {name}{RESET}{DIM}{tag}{RESET} (Enter=NULL): ").strip()
        values.append(None if val == "" else val)

    placeholders = ",".join(["?"] * len(names))
    sql = f"INSERT INTO {table} ({','.join(names)}) VALUES ({placeholders})"
    try:
        cur.execute(sql, values); con.commit()
        success("Registro insertado.")
    except sqlite3.Error as e:
        error(f"No se pudo insertar: {e}")
    pause()

def op_list(cur, table):
    cls(); apply_theme(); banner()
    print(f"{BOLD}📋 Listado de {table}{RESET}\n")
    cols = table_info(cur, table)
    names = column_names(cols)
    try:
        cur.execute(f"SELECT {', '.join(names)} FROM {table};")
        rows = cur.fetchall()
        paginated_print(names, rows)
    except sqlite3.Error as e:
        error(f"No se pudo listar: {e}")
        pause()

def read_by_pk(cur, table, pk_cols, pk_values):
    where = " AND ".join([f"{c}=?" for c in pk_cols])
    sql = f"SELECT * FROM {table} WHERE {where} LIMIT 1;"
    cur.execute(sql, pk_values)
    return cur.fetchone()

def op_update(cur, con, table):
    cls(); apply_theme(); banner()
    print(f"{BOLD}✏️  Actualizar en {table}{RESET}\n")
    cols = table_info(cur, table)
    names = column_names(cols)
    pk_cols = primary_keys(cols)
    if not pk_cols:
        error("Esta tabla no tiene clave primaria definida. Actualización no soportada.")
        return pause()

    pk_values = []
    print(f"{FG_CYAN}Introduce la clave primaria para localizar el registro:{RESET}")
    for pk in pk_cols:
        v = input(f"· {pk}: ").strip()
        if v == "":
            error("La clave primaria no puede quedar vacía."); return pause()
        pk_values.append(v)

    row = read_by_pk(cur, table, pk_cols, pk_values)
    if not row:
        error("No se encontró el registro con esa PK."); return pause()

    print("\nRegistro actual:")
    print(format_table(names, [row]))
    print()

    new_values = []
    for i, c in enumerate(cols):
        cname = c[1]
        current = row[i]
        if cname in pk_cols:
            print(f"{DIM}{cname} (PK) = {current} (no editable){RESET}")
            new_values.append(current)
        else:
            val = input(f"{FG_YELLOW}· {cname}{RESET} {DIM}[actual: {current}]{RESET} (Enter=mantener): ")
            new_values.append(current if val.strip() == "" else val)

    set_clause = ", ".join([f"{n}=?" for n in names if n not in pk_cols])
    where = " AND ".join([f"{c}=?" for c in pk_cols])
    params = [new_values[names.index(n)] for n in names if n not in pk_cols] + pk_values

    sql = f"UPDATE {table} SET {set_clause} WHERE {where};"
    try:
        cur.execute(sql, params); con.commit()
        success(f"Filas afectadas: {cur.rowcount}")
    except sqlite3.Error as e:
        error(f"No se pudo actualizar: {e}")
    pause()

def op_delete(cur, con, table):
    cls(); apply_theme(); banner()
    print(f"{BOLD}🗑️  Eliminar en {table}{RESET}\n")
    cols = table_info(cur, table)
    names = column_names(cols)
    pk_cols = primary_keys(cols)
    if not pk_cols:
        error("Esta tabla no tiene clave primaria definida. Eliminación no soportada.")
        return pause()

    pk_values = []
    print(f"{FG_CYAN}Introduce la clave primaria del registro a eliminar:{RESET}")
    for pk in pk_cols:
        v = input(f"· {pk}: ").strip()
        if v == "":
            error("La clave primaria no puede quedar vacía."); return pause()
        pk_values.append(v)

    row = read_by_pk(cur, table, pk_cols, pk_values)
    if not row:
        error("No se encontró el registro con esa PK."); return pause()

    print("\nRegistro a eliminar:")
    print(format_table(names, [row]))
    print()
    conf = input(f"{FG_RED}{BOLD}¿Seguro que deseas eliminarlo? (s/N): {RESET}").strip().lower()
    if conf != "s":
        info("Cancelado."); return pause()

    where = " AND ".join([f"{c}=?" for c in pk_cols])
    sql = f"DELETE FROM {table} WHERE {where};"
    try:
        cur.execute(sql, pk_values); con.commit()
        success(f"Filas afectadas: {cur.rowcount}")
    except sqlite3.Error as e:
        error(f"No se pudo eliminar: {e}")
    pause()

# =======================
# Menús
# =======================
def select_table(cur):
    while True:
        cls(); apply_theme(); banner()
        print(f"{BOLD}Selecciona una entidad (tabla){RESET}\n")
        tables = list_tables(cur)
        if not tables:
            error("No hay tablas en la base de datos.")
            pause("Crea alguna tabla y vuelve a ejecutar. Pulsa una tecla…")
            sys.exit(0)

        w = len(str(len(tables)))
        for i, t in enumerate(tables, 1):
            left = pad_visible(str(i).rjust(w), w)
            print(f"{FG_CYAN}{left}{RESET} {VL} {t}")
        print()
        op = ask_int("Tu opción elegida: ", minv=1, maxv=len(tables))
        return tables[op - 1]

def select_operation(table):
    cls(); apply_theme(); banner()
    print(f"{BOLD}Tabla seleccionada: {FG_GREEN}{table}{RESET}\n")
    print(f"{BOLD}Selecciona una operación:{RESET}")
    print(f"  {FG_CYAN}1{RESET} {VL} Crear un registro")
    print(f"  {FG_CYAN}2{RESET} {VL} Listado de registros")
    print(f"  {FG_CYAN}3{RESET} {VL} Actualizar un registro")
    print(f"  {FG_CYAN}4{RESET} {VL} Eliminar un registro")
    print(f"  {FG_CYAN}5{RESET} {VL} Cambiar de tabla")
    print(f"  {FG_CYAN}0{RESET} {VL} Salir")
    print()
    return ask_int("Selecciona una opción: ", minv=0, maxv=5)

# =======================
# Main
# =======================
def main():
    con = connect(DB_PATH)
    cur = con.cursor()

    cls(); apply_theme(); banner()
    pause()

    current_table = None
    while True:
        if not current_table:
            current_table = select_table(cur)

        op = select_operation(current_table)
        if op == 0:
            cls(); apply_theme()
            info("Hasta pronto 👋")
            break
        elif op == 1:
            op_create(cur, con, current_table)
        elif op == 2:
            op_list(cur, current_table)
        elif op == 3:
            op_update(cur, con, current_table)
        elif op == 4:
            op_delete(cur, con, current_table)
        elif op == 5:
            current_table = None

    try:
        con.close()
    except Exception:
        pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cls(); apply_theme()
        info("Interrumpido por el usuario.")
```

### Conceptos de consola
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de texto no contiene código Python ejecutable, sino que proporciona información general sobre las terminales o consolas en diferentes sistemas operativos. Describe brevemente cómo los sistemas Windows, macOS y Linux tienen sus propias versiones de terminal o consola para interactuar con el sistema operativo directamente desde la línea de comandos.

Además, menciona dos tipos principales de programas que se pueden desarrollar:

1. **Programas de consola/terminal**: Estos son programas que funcionan sin una interfaz gráfica y utilizan la terminal del sistema operativo para recibir entrada del usuario y mostrar salida, como mensajes o resultados de cálculos.

2. **Programas de ventanas (tkinter)**: Son aplicaciones con interfaces gráficas creadas en lenguajes de programación que pueden interactuar con bibliotecas específicas, como tkinter en Python, para crear ventanas y controles visuales.

Este texto es informativo y ayuda a entender la diferencia entre trabajar directamente en una consola o terminal y desarrollar aplicaciones que utilizan interfaces gráficas. Es importante conocer estos conceptos para comprender cómo interactúan las aplicaciones con el sistema operativo y cómo se pueden crear diferentes tipos de software dependiendo de las necesidades del usuario.

`032-Conceptos de consola.py`

```python
Todos los sistemas operativos tienen terminal/consola:

En Windows, es el CMD (vestigio del antiguo MS-DOS)
En macOS, es la terminal (el UNIX que realmente hay debajo de macOS)
Y en Linux, es la terminal

Los tres sistemas operativos, a dia de hoy (2025), soportan
1.-Programas de consola/terminal - programados en cualquier lenguaje
2.-Programas de ventanas (tkinter) - programados en cualquier lenguaje
```

### Actividades propuestas

El código proporcionado es una implementación detallada de un sistema CRUD (Create, Read, Update, Delete) para una base de datos SQLite, utilizando la consola como interfaz. El programa permite al usuario interactuar con las tablas de una base de datos SQLite mediante comandos de texto. Aquí se desglosa el funcionamiento principal del código:

1. **Interfaz de Consola**: El programa utiliza un sistema de menús y entradas de texto para permitir a los usuarios realizar operaciones CRUD en la base de datos.

2. **Estilo de Interfaz**: Usa colores y símbolos para mejorar la visualización en la consola, lo que hace que sea más fácil para el usuario entender y navegar por el menú.

3. **Funciones Básicas**:
   - `op_create`: Inserta un nuevo registro en una tabla específica.
   - `op_list`: Muestra todos los registros de una tabla especificada.
   - `op_update`: Actualiza un registro existente basado en la clave primaria (PK).
   - `op_delete`: Elimina un registro específico también basándose en la clave primaria.

4. **Manejo de Tablas**:
   - El programa permite a los usuarios seleccionar y trabajar con diferentes tablas dentro de una base de datos SQLite.
   
5. **Interacción Con Usuario**:
   - La función `select_operation` muestra un menú interactivo para permitir al usuario seleccionar qué operación CRUD realizar.

6. **Comprobaciones y Gestión de Errores**:
   - El código incluye comprobaciones básicas, como verificar si una clave primaria es vacía antes de intentar actualizar o eliminar un registro.
   
7. **Estilo y Apariencia**:
   - Usa colores y símbolos para mejorar la apariencia del menú interactivo en la consola.

### Estructura Detallada:

1. **Inicialización y Conexión a Base de Datos**
    ```python
    def main():
        con = connect(DB_PATH)
        cur = con.cursor()
    ```

2. **Menús Interactivos**
   - Se muestra un menú inicial para seleccionar la tabla.
   - Después, se muestra otro menú interactivo para permitir al usuario elegir la operación CRUD.

3. **Operaciones CRUD**
    - `op_create`: Permite a los usuarios insertar nuevos registros en la base de datos.
    - `op_list`: Muestra todos los registros de una tabla específica.
    - `op_update`: Actualiza un registro basado en la clave primaria.
    - `op_delete`: Elimina un registro basado en la clave primaria.

4. **Gestión de Errores**
   - El programa maneja excepciones como errores en las consultas SQL y entradas inválidas del usuario, proporcionando mensajes informativos para mejorar la experiencia del usuario.

### Ejecución:
- Al ejecutar el script `main.py`, se inicializa una conexión a la base de datos SQLite especificada (`DB_PATH`). Luego, se muestra un menú interactivo que permite al usuario seleccionar la tabla y realizar operaciones CRUD en ella. 

Este código es útil para aprender sobre cómo interactuar con bases de datos desde la consola y cómo mejorar la experiencia del usuario mediante el uso de estilos textuales en la terminal (como colores y símbolos).


<a id="simulacro-examen"></a>
## Simulacro examen

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/004-Tratamiento%20de%20datos/006-Simulacro%20examen)

### Introducción a los ejercicios

Este conjunto de ejercicios está diseñado para familiarizarte con la creación y gestión de una base de datos en SQL, específicamente centrada en un blog con entradas y autores. Los problemas abordan desde la creación inicial de la base de datos hasta la inserción de datos y la manipulación avanzada mediante joins e vistas. Practicarás habilidades como definir estructuras de tablas, establecer relaciones entre ellas a través de claves primarias y foráneas, así como manejar usuarios y privilegios en tu base de datos. Este ejercicio te preparará para entender cómo se organiza la información en aplicaciones web reales, desde el modelo relacional hasta su implementación práctica con SQL.

### Creo la base de datos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL tiene dos partes. Primero, se ejecuta el comando `sudo mysql -u root -p` en la línea de comandos para acceder al servidor MySQL con privilegios del usuario raíz (root). Esto te pedirá que ingreses la contraseña de la cuenta root cuando lo ejecutes.

La segunda parte es la creación de una base de datos llamada `blog2526`. El comando `CREATE DATABASE blog2526;` instruye al servidor MySQL para crear una nueva base de datos con ese nombre. Este paso es crucial porque establece el contenedor en donde almacenarás todas las tablas y datos relacionados a un blog o proyecto específico.

Este archivo SQL probablemente será parte de una serie de archivos que definen la estructura completa de tu base de datos para un proyecto, como el desarrollo de una aplicación de blog. Es importante seguir este tipo de scripts paso a paso para asegurarte de que cada componente se crea correctamente en orden.

`001-Creo la base de datos.sql`

```sql
sudo mysql -u root -p

CREATE DATABASE blog2526;
```

### creo tablas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL crea dos tablas en una base de datos, llamadas "entradas" y "autores". La tabla "entradas" almacena información sobre entradas o artículos, como un identificador único, el título del artículo, su contenido, la fecha en que se publicó y el autor asociado (que es un número entero representando la relación con una fila en la tabla autores). Por otro lado, la tabla "autores" almacena información sobre los autores de estos artículos, incluyendo un identificador único para cada autor, su nombre, apellidos y correo electrónico. Ambas tablas utilizan el motor InnoDB, que es conocido por ser más potente y robusto que otros motores, permitiendo transacciones y relaciones entre tablas (como claves foráneas).

Este código es fundamental en la creación de una base de datos para un sistema de gestión de contenido o blog, ya que establece las estructuras básicas donde se guardarán los datos de entradas y autores. La elección del motor InnoDB es importante porque permite definir relaciones entre estas dos tablas más adelante (por ejemplo, hacer que la columna "autor" en la tabla "entradas" sea una clave foránea referenciando a la tabla "autores"), lo que ayuda a mantener la integridad de los datos y facilita consultas complejas.

`002-creo tablas.sql`

```sql
CREATE TABLE entradas (
  `Identificador` INT NOT NULL , 
  `titulo` VARCHAR(150) NOT NULL , 
  `contenido` VARCHAR(255) NOT NULL , 
  `fecha` VARCHAR(50) NOT NULL , 
  `autor` INT NOT NULL 
) ENGINE = InnoDB;

CREATE TABLE autores (
  `Identificador` INT NOT NULL , 
  `nombre` VARCHAR(150) NOT NULL , 
  `apellidos` VARCHAR(255) NOT NULL , 
  `email` VARCHAR(150) NOT NULL 
) ENGINE = InnoDB;
```

### añadir claves primarias
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL te enseña cómo añadir claves primarias a dos tablas diferentes llamadas `entradas` y `autores`. Primero, el código describe la estructura actual de la tabla `entradas`, mostrando sus columnas actuales. Luego, se agrega una clave primaria a esta tabla utilizando la columna `Identificador`. Una clave primaria es un campo o conjunto de campos que única e invariablemente identifica cada fila en una tabla. A continuación, se modifica la columna `Identificador` para asegurarse de que sea de tipo entero (INT), no nula y autoincrementable, lo que significa que el valor de esta columna aumentará automáticamente con cada nueva entrada.

El proceso se repite para la tabla `autores`, primero describiendo su estructura actual, luego añadiendo una clave primaria a la misma columna `Identificador` en esta tabla, y finalmente modificando esa columna para ser de tipo INT, no nula y autoincrementable. Esto asegura que cada tabla tenga un campo único e incremental que puede usarse como identificador principal.

La importancia de establecer claves primarias radica en que proporcionan una forma única de referirse a cualquier fila en la tabla, lo cual es crucial para relaciones entre tablas y garantiza la integridad de los datos.

`003-añadir claves primarias.sql`

```sql
DESCRIBE entradas;

ALTER TABLE entradas
  ADD PRIMARY KEY (`Identificador`);
  
  ALTER TABLE entradas
  MODIFY COLUMN Identificador INT NOT NULL AUTO_INCREMENT;
  
  DESCRIBE entradas;
  
  
DESCRIBE autores;

ALTER TABLE autores
  ADD PRIMARY KEY (`Identificador`);
  
  ALTER TABLE autores
  MODIFY COLUMN Identificador INT NOT NULL AUTO_INCREMENT;
  
  DESCRIBE autores;
```

### clave foranea de autores a entradas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está añadiendo una restricción (constraint) a la tabla llamada `entradas`. Específicamente, se crea una clave foránea (`FOREIGN KEY`) en el campo `autor` que referencia al campo `Identificador` en la tabla `autores`.

La función principal es garantizar que cada entrada registrada en la tabla `entradas` esté asociada con un autor válido que existe en la tabla `autores`. Esto mantiene la integridad de los datos, asegurando que no haya entradas cuyo autor no tenga una correspondiente entrada en la tabla `autores`.

Las cláusulas `ON DELETE RESTRICT` y `ON UPDATE RESTRICT` significan que si intentas eliminar un registro del autor o cambiar su identificador, SQL impedirá dicha acción porque afectaría las referencias existentes en la tabla de entradas. Esto protege contra la pérdida accidental de datos importantes relacionados.

En resumen, este código ayuda a mantener una relación coherente y segura entre autores y sus entradas en un sistema de gestión de contenido o blog, evitando registros inconsistentes.

`004-clave foranea de autores a entradas.sql`

```sql
ALTER TABLE entradas 
ADD CONSTRAINT `autoresaentradas` 
FOREIGN KEY (`autor`) REFERENCES `autores`(`Identificador`) 
ON DELETE RESTRICT 
ON UPDATE RESTRICT;
```

### insercion de datos de muestra
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para insertar datos en la tabla llamada `autores`. Cada línea dentro del comando `INSERT INTO` agrega una nueva fila a esta tabla, especificando valores para las columnas `nombre`, `apellidos` y `email`.

El formato es importante: primero se indica la tabla donde se van a añadir los registros (en este caso, `autores`) seguido de una lista entre paréntesis con el nombre de las columnas que recibirán datos. Luego, después del comando `VALUES`, se proporciona una lista de valores para cada fila nueva que queremos agregar.

Esta operación es crucial porque permite poblar la base de datos con información inicial que luego puede ser utilizada para realizar consultas, actualizar registros y vincular esta tabla con otras tablas en el diseño de la base de datos.

`005-insercion de datos de muestra.sql`

```sql
INSERT INTO autores (nombre, apellidos, email) VALUES
('Carlos', 'Pérez Gómez', 'carlos.perez@example.com'),
('María', 'López Sánchez', 'maria.lopez@example.com'),
('Javier', 'Martínez Ruiz', 'javier.martinez@example.com'),
('Lucía', 'García Torres', 'lucia.garcia@example.com'),
('Andrés', 'Ramírez Fernández', 'andres.ramirez@example.com'),
('Elena', 'Moreno Díaz', 'elena.moreno@example.com'),
('Sergio', 'Hernández Navarro', 'sergio.hernandez@example.com'),
('Patricia', 'Gómez León', 'patricia.gomez@example.com'),
('Raúl', 'Castillo Ortega', 'raul.castillo@example.com'),
('Laura', 'Santos Vega', 'laura.santos@example.com'),
('Diego', 'Cano Romero', 'diego.cano@example.com'),
('Marta', 'Jiménez Soto', 'marta.jimenez@example.com'),
('Rubén', 'Pardo Iglesias', 'ruben.pardo@example.com'),
('Nuria', 'Cruz Herrera', 'nuria.cruz@example.com'),
('Héctor', 'Vázquez Molina', 'hector.vazquez@example.com'),
('Adriana', 'Reyes Campos', 'adriana.reyes@example.com'),
('Pablo', 'Suárez Gil', 'pablo.suarez@example.com'),
('Sara', 'Nieto Rivas', 'sara.nieto@example.com'),
('Álvaro', 'Ruiz Pastor', 'alvaro.ruiz@example.com'),
('Clara', 'Ortega Lozano', 'clara.ortega@example.com');
```

### insercion de entradas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para insertar múltiples registros en una tabla llamada `entradas`. Cada registro contiene información sobre un artículo o entrada, incluyendo el título del artículo, su contenido, la fecha en que fue publicado y el autor asociado. La estructura del comando `INSERT INTO` permite especificar los campos de la tabla a llenar (en este caso, `titulo`, `contenido`, `fecha` y `autor`) seguidos por una lista de valores entre paréntesis. Cada conjunto de valores representa un nuevo registro que se insertará en la tabla.

Lo importante aquí es entender cómo organizar los datos para cada entrada y cómo relacionarlos con el autor a través del campo `autor`. Esto demuestra cómo manipular registros en una base de datos relacional, siendo clave identificar correctamente las claves primarias y foráneas entre tablas. En este caso, el número asociado al autor (por ejemplo, '1', '2') debería corresponder con los IDs de la tabla `autores`.

Esta operación es fundamental para poblar una base de datos con datos iniciales o de prueba, lo cual es muy útil durante las etapas de desarrollo y pruebas en proyectos de bases de datos.

`006-insercion de entradas.sql`

```sql
INSERT INTO entradas (titulo, contenido, fecha, autor) VALUES
('Introducción a la programación en Python', 'Una guía para comenzar a programar con Python desde cero.', '2025-01-05', 1),
('Cómo crear tu primera página web con HTML y CSS', 'Aprende los fundamentos del diseño web con ejemplos prácticos.', '2025-01-10', 2),
('JavaScript moderno: funciones flecha y promesas', 'Exploramos las características modernas del lenguaje JavaScript.', '2025-01-12', 3),
('Instalar y configurar MySQL en Ubuntu', 'Guía paso a paso para instalar MySQL en sistemas basados en Linux.', '2025-01-15', 4),
('Buenas prácticas de seguridad en PHP', 'Cómo proteger tu aplicación web frente a ataques comunes.', '2025-01-18', 5),
('Introducción a Docker para desarrolladores', 'Aprende a crear contenedores para tus proyectos de desarrollo.', '2025-01-20', 6),
('Versionado de código con Git y GitHub', 'Todo lo que necesitas saber para trabajar en equipo con control de versiones.', '2025-01-22', 7),
('APIs RESTful con Flask y Python', 'Construye tus propias APIs usando el microframework Flask.', '2025-01-25', 8),
('Diseño responsivo con CSS Grid y Flexbox', 'Técnicas modernas para crear sitios adaptativos y elegantes.', '2025-01-28', 9),
('Automatización de tareas con Python', 'Ejemplos de cómo automatizar procesos repetitivos con scripts.', '2025-02-02', 10),
('Introducción a React.js', 'Cómo empezar a desarrollar interfaces modernas con React.', '2025-02-05', 11),
('Bases de datos NoSQL: una visión general', 'Compara MongoDB, Redis y otros sistemas de almacenamiento.', '2025-02-07', 12),
('Optimización de rendimiento en WordPress', 'Consejos para acelerar tu sitio web WordPress.', '2025-02-10', 13),
('Cómo desplegar una app en la nube con AWS', 'Pasos esenciales para llevar tu aplicación a producción.', '2025-02-12', 14),
('Aprendiendo Node.js paso a paso', 'Una introducción práctica al entorno de ejecución de JavaScript.', '2025-02-14', 15),
('Machine Learning con Python y scikit-learn', 'Primeros pasos en el aprendizaje automático.', '2025-02-18', 16),
('Cómo proteger tu red doméstica', 'Recomendaciones básicas de ciberseguridad para usuarios domésticos.', '2025-02-20', 17),
('Programación orientada a objetos en Java', 'Conceptos clave como clases, objetos, herencia y polimorfismo.', '2025-02-22', 18),
('Diseño de bases de datos relacionales', 'Cómo modelar tus datos correctamente con claves primarias y foráneas.', '2025-02-25', 19),
('Inteligencia artificial en la web moderna', 'Exploramos el papel de la IA en las aplicaciones actuales.', '2025-02-28', 20);
```

### seleccion de autores para aclararnos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL selecciona todos los registros de la tabla llamada `autores`. La instrucción `SELECT *` significa que se recuperan todas las columnas y filas disponibles en esa tabla. En este contexto, el código es útil para ver todo el contenido almacenado actualmente sobre autores en tu base de datos, lo cual puede ser necesario para comprobar la información insertada o para entender mejor cómo está estructurada la tabla de `autores`.

`007-seleccion de autores para aclararnos.sql`

```sql
SELECT * FROM autores;
```

### left join
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL realiza una consulta que selecciona información combinada de dos tablas: `entradas` y `autores`. La instrucción `SELECT` indica los campos específicos que queremos recuperar, como el título, contenido y fecha de las entradas, junto con el nombre, apellidos y email del autor.

La parte clave es la cláusula `LEFT JOIN`, que une todas las filas de la tabla `entradas` con las correspondientes filas en la tabla `autores` basándose en una relación definida por el campo `autor` en `entradas` y el campo `Identificador` en `autores`. Esto significa que incluso si no hay un autor asociado para ciertas entradas, estas se incluirán en los resultados junto con valores nulos para las columnas del autor.

Esta consulta es importante porque proporciona una visión integrada de los datos de las entradas y sus autores, lo cual puede ser útil para generar informes o visualizaciones que muestren quién ha escrito qué entrada.

`008-left join.sql`

```sql
SELECT 
entradas.titulo,
entradas.contenido,
entradas.fecha,
autores.nombre,
autores.apellidos,
autores.email
 FROM
entradas
LEFT JOIN autores
ON entradas.autor = autores.Identificador;
```

### crear una vista
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL crea una vista llamada `entradas_con_autores` en la base de datos. Una vista es como una tabla virtual que almacena resultados de consultas, lo cual facilita la visualización y el manejo de datos complejos. En este caso, la vista combina información de dos tablas: `entradas` y `autores`.

La consulta selecciona los campos `titulo`, `contenido`, `fecha` de la tabla `entradas`, así como `nombre`, `apellidos` y `email` de la tabla `autores`. Utiliza un LEFT JOIN para asegurar que todas las entradas se incluyan en el resultado, incluso si no hay un autor asociado (es decir, no hay una coincidencia en la tabla `autores`). Esto es importante porque permite ver todas las entradas junto con los detalles de sus autores, si están disponibles.

Después de crear la vista, el código ejecuta otra consulta que simplemente selecciona todos los datos (`*`) desde la vista recién creada llamada `entradas_con_autores`. Esto muestra cómo utilizar una vista para simplificar y organizar consultas complejas.

`009-crear una vista.sql`

```sql
CREATE VIEW entradas_con_autores AS 
SELECT 
entradas.titulo,
entradas.contenido,
entradas.fecha,
autores.nombre,
autores.apellidos,
autores.email
 FROM
entradas
LEFT JOIN autores
ON entradas.autor = autores.Identificador;

SELECT
*
FROM
entradas_con_autores;
```

### crear usuario con privilegios
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para crear un nuevo usuario en la base de datos y otorgarle privilegios específicos. El proceso comienza creando el usuario `blog2526` con una contraseña también llamada `blog2526`. A continuación, se le dan los permisos básicos a este usuario utilizando la sentencia `GRANT USAGE`, lo que significa que el usuario puede conectarse al servidor de base de datos pero no tiene acceso a ninguna base de datos específica.

Luego, se modifican las características del usuario con `ALTER USER`. Aquí, se establecen varias restricciones para el usuario, como permitirle iniciar sesión sin tener que proporcionar una contraseña (`REQUIRE NONE`), y configurando límites en cuanto al número de consultas, conexiones y actualizaciones por hora a cero. Esto es común cuando no deseamos limitar las acciones del usuario.

Finalmente, se otorgan todos los privilegios disponibles sobre la base de datos `blog2526` a este usuario con otra sentencia `GRANT ALL PRIVILEGES`. Esta acción permite que el usuario realice cualquier tipo de operación en esa base de datos. La instrucción `FLUSH PRIVILEGES` se utiliza para asegurar que los cambios realizados en las reglas y privilegios sean aplicados inmediatamente.

Este código es importante porque permite configurar de manera segura un entorno de desarrollo donde distintas personas pueden trabajar con sus propias cuentas, cada una con los permisos necesarios pero limitados para su rol específico.

`010-crear usuario con privilegios.sql`

```sql
CREATE USER 
'blog2526'@'localhost' 
IDENTIFIED BY 'blog2526';

GRANT USAGE ON *.* TO 'blog2526'@'localhost';

ALTER USER 'blog2526'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 
MAX_CONNECTIONS_PER_HOUR 0 
MAX_UPDATES_PER_HOUR 0 
MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON `blog2526`.* 
TO 'blog2526'@'localhost';

FLUSH PRIVILEGES;
```

### Actividades propuestas

1. **Creación de una Base de Datos**
   - Crear una base de datos personalizada para un proyecto web.
   - Aprendizaje: Entender cómo configurar y utilizar bases de datos en proyectos.

2. **Estructura Tablas**
   - Diseñar e implementar tablas para almacenar información sobre usuarios y publicaciones.
   - Aprendizaje: Conocer la creación y estructuración básica de tablas SQL con claves primarias.

3. **Añadir Claves Primarias Autoincrementales**
   - Modificar las tablas existentes para añadir claves primarias autoincrementables.
   - Aprendizaje: Comprender el concepto de claves primarias y cómo configurarlas en SQL.

4. **Relaciones entre Tablas**
   - Crear una relación (clave foránea) entre dos tablas preexistentes (usuarios y publicaciones).
   - Aprendizaje: Entender las relaciones (claves foráneas) entre diferentes tablas en una base de datos relacional.

5. **Inserción de Datos**
   - Insertar registros de ejemplo en las tablas creadas.
   - Aprendizaje: Practicar la inserción de datos en tablas SQL y entender el formato correcto para los mismos.

6. **Consulta Compleja con JOINs**
   - Realizar una consulta que combine datos desde múltiples tablas usando un LEFT JOIN.
   - Aprendizaje: Entender cómo combinar información desde varias tablas utilizando tipos de joins.

7. **Creación y Uso de Vistas**
   - Crear una vista que muestre la combinación de dos o más tablas.
   - Aprendizaje: Aprender a crear vistas en SQL para facilitar consultas complejas y mejorar la eficiencia del código.

8. **Consultas Paramétricas con Placeholder**
   - Escribir consultas que utilicen placeholders (variables) para evitar problemas de inyección SQL.
   - Aprendizaje: Comprender cómo escribir consultas seguras utilizando parámetros y variables en lugar de concatenar strings.

9. **Administrar Usuarios y Privilegios**
   - Crear un nuevo usuario con privilegios limitados para una base de datos específica.
   - Aprendizaje: Entender la administración de usuarios, roles y permisos en MySQL.

10. **Resolución de Problemas y Optimización Consultas**
    - Identificar problemas en consultas SQL existentes y proponer mejoras o soluciones.
    - Aprendizaje: Practicar habilidades de depuración y optimización de consultas SQL para mejorar el rendimiento del sistema.

Estas actividades están diseñadas para reforzar los conceptos básicos y avanzados en la gestión de bases de datos relacionales, específicamente enfocándose en MySQL.


<a id="simulacro-de-examen-2"></a>
## Simulacro de examen 2

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/004-Tratamiento%20de%20datos/007-Simulacro%20de%20examen%202)

### Introducción a los ejercicios

Esta carpeta contiene una serie de ejercicios orientados a la creación y gestión de una base de datos para un blog o portafolio personal. Los estudiantes deben aprender a estructurar datos en tablas relacionales, utilizando claves primarias y foráneas, además de realizar inserciones, consultas cruzadas, creación de vistas y manejo de usuarios con permisos específicos. El objetivo es afianzar los conocimientos sobre la manipulación de bases de datos mediante SQL, incluyendo operaciones CRUD (Crear, Leer, Actualizar, Eliminar) y el uso eficiente de vistas para simplificar consultas complejas.

### resolucion del examen
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está diseñado para crear una base de datos y sus tablas, así como establecer una relación entre ellas. Primero, se crea una base de datos llamada `portafolio`. Luego, se crean dos tablas: `piezas` y `autores`. La tabla `piezas` almacena información sobre diferentes piezas, incluyendo un identificador único, título, descripción, fecha y el ID del autor. La tabla `autores` contiene datos sobre los autores de esas piezas, con campos para nombre, apellidos y correo electrónico.

Lo más importante en este código es cómo establece una relación entre las dos tablas a través de una clave foránea. Específicamente, la columna `id_autor` en la tabla `piezas` se vincula con la columna `Identificador` en la tabla `autores`. Esta acción asegura que cualquier pieza debe estar asociada con un autor válido en la base de datos.

El código también incluye comandos para mostrar las bases de datos y tablas existentes, así como para describir el esquema de cada tabla (mostrando los campos y sus tipos). Esto ayuda a verificar que todo se ha configurado correctamente.

`002-resolucion del examen.sql`

```sql
Recomiendo enormemente hacer el examen de bases de datos dentro de la maquina virtual

ssh josevicente@192.168.1.176

sudo mysql -u root -p

CREATE DATABASE portafolio;

SHOW DATABASES;

USE portafolio;

SHOW TABLES;

CREATE TABLE piezas(
  Identificador INT auto_increment PRIMARY KEY,
  titulo VARCHAR(255),
  descripcion TEXT,
  fecha VARCHAR(255),
  id_autor INT
);

SHOW TABLES;

DESCRIBE piezas;

CREATE TABLE autores(
  Identificador INT auto_increment PRIMARY KEY,
  nombre VARCHAR(255),
  apellidos VARCHAR(255),
  email VARCHAR(255)
);

SHOW TABLES;

DESCRIBE autores;

ALTER TABLE piezas 
ADD CONSTRAINT autores_a_piezas 
FOREIGN KEY (id_autor) 
REFERENCES autores(Identificador) 
ON DELETE RESTRICT 
ON UPDATE RESTRICT;

SELECT * FROM piezas;

SELECT * FROM autores;
```

### le damos algo de contenido a la base de datos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para trabajar con una base de datos, específicamente con dos tablas llamadas `autores` y `piezas`. Primero, el código inserta un nuevo registro en la tabla `autores`, añadiendo automáticamente un ID único (ya que el primer valor es `NULL`), el nombre 'Jose Vicente', el apellido 'Carratala Sanchis' y una dirección de correo electrónico. Luego, se seleccionan todos los registros de la tabla `autores` para verificar que el nuevo autor ha sido agregado correctamente.

Después de eso, se inserta un registro en la tabla `piezas`, nuevamente con un ID generado automáticamente, seguido por el título 'Titulo de la pieza 1', una descripción 'Descripción de la pieza 1', una fecha ('2025-11-03') y un identificador que probablemente hace referencia al autor recién insertado en `autores` (el número 1). Finalmente, se seleccionan todos los registros de la tabla `piezas` para comprobar que el nuevo registro ha sido añadido correctamente.

Este tipo de operaciones es fundamental cuando trabajas con bases de datos para asegurarte de que tus tablas estén bien pobladas con datos iniciales y puedas verificar fácilmente si las inserciones se han realizado como esperabas.

`003-le damos algo de contenido a la base de datos.sql`

```sql
INSERT INTO autores VALUES(
  NULL,
  'Jose Vicente',
  'Carratala Sanchis',
  'info@jocarsa.com'
);

SELECT * FROM autores;

INSERT INTO piezas VALUES(
  NULL,
  'Titulo de la pieza 1',
  'Descripción de la pieza 1',
  '2025-11-03',
  1
);

SELECT * FROM piezas;
```

### alteramos taba
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL sirve para modificar una tabla llamada `piezas` en una base de datos. En la primera línea, se añade una nueva columna a esta tabla con el comando `ALTER TABLE`. La nueva columna se llama `imagen` y es del tipo `VARCHAR(255)`, lo que significa que puede contener texto hasta un máximo de 255 caracteres.

La segunda línea utiliza el comando `DESCRIBE` para mostrar la estructura actualizada de la tabla `piezas`, incluyendo la nueva columna recién añadida. Esto te permite ver cómo ha cambiado la tabla después de agregar la columna `imagen`.

Esta operación es importante porque permite expandir las características de una tabla existente sin necesidad de crear una nueva tabla desde cero, lo que puede ahorrar tiempo y mantener la consistencia en los datos ya almacenados.

`004-alteramos taba.sql`

```sql
ALTER TABLE piezas
ADD COLUMN imagen VARCHAR(255);

DESCRIBE piezas;
```

### peticion cruzada
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL realiza dos acciones importantes en una base de datos. Primero, añade una nueva columna llamada "imagen" ala tabla "piezas". Esta columna es del tipo VARCHAR y tiene un tamaño máximo de 255 caracteres. Esto significa que ahora puedes almacenar información sobre la imagen asociada a cada pieza en esta nueva columna.

Después de modificar la estructura de la tabla, el código utiliza la sentencia `DESCRIBE` para mostrar la descripción actual de la tabla "piezas". Esta acción es útil porque te permite ver cómo ha cambiado la tabla después de añadir la nueva columna. Verás todos los nombres de las columnas existentes junto con sus tipos de datos y otros detalles importantes.

Esta operación es importante porque permite a los desarrolladores ajustar dinámicamente la estructura de una base de datos según sea necesario, por ejemplo, para añadir nuevos campos que reflejen nuevas necesidades del sistema o información adicional sobre los registros existentes.

`005-peticion cruzada.sql`

```sql
ALTER TABLE piezas
ADD COLUMN imagen VARCHAR(255);

DESCRIBE piezas;
```

### vista cruzada
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL realiza una consulta que combina información de dos tablas: `autores` y `piezas`. La primera parte del código selecciona el nombre, apellidos, email del autor junto con los detalles de las piezas (título, descripción, fecha y imagen) relacionadas. Utiliza un tipo especial de combinación de tablas llamado "LEFT JOIN", que garantiza que se incluyan todos los registros de la tabla `piezas`, incluso si no tienen una correspondencia en la tabla `autores`.

Después, el código crea una vista denominada `piezas_con_autores` usando la misma consulta. Una vista es como un alias para una consulta compleja; permite a otros usuarios y consultas acceder a los resultados de esta combinación como si fuera una sola tabla. Esto facilita mucho la lectura y escritura de datos en el futuro, ya que no necesitarás repetir la misma consulta cada vez.

Finalmente, se ejecuta otra consulta para seleccionar todos los registros de la vista `piezas_con_autores`, lo cual mostrará un conjunto de resultados combinados con todas las columnas especificadas previamente. Esto es útil tanto para visualizar cómo quedan combinados estos datos como para usar esta vista en consultas más complejas o reportes futuros.

`006-vista cruzada.sql`

```sql
SELECT 
autores.nombre,
autores.apellidos,
autores.email,
piezas.titulo,
piezas.descripcion,
piezas.fecha,
piezas.imagen
 FROM piezas
LEFT JOIN autores
ON piezas.id_autor = autores.Identificador;

Ahora creamos la vista
CREATE VIEW piezas_con_autores AS 
SELECT 
autores.nombre,
autores.apellidos,
autores.email,
piezas.titulo,
piezas.descripcion,
piezas.fecha,
piezas.imagen
 FROM piezas
LEFT JOIN autores
ON piezas.id_autor = autores.Identificador;

SELECT * FROM piezas_con_autores;
```

### crear usuario con permisos
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL te enseña cómo crear un nuevo usuario en una base de datos y otorgarle ciertos permisos. Primero, se crea un usuario llamado `portafolio` que puede acceder desde el servidor local (`localhost`) con la contraseña `Portafolio123$`. Luego, le asigna al usuario los privilegios básicos necesarios mediante la sentencia `GRANT USAGE ON *.*`, lo cual permite al usuario conectarse pero no realizar operaciones en la base de datos.

A continuación, se ajustan las restricciones del usuario con la sentencia `ALTER USER`. Esto elimina cualquier requisito para que el usuario inicie sesión (REQUIRE NONE) y establece varios límites a cero para consultas por hora, conexiones por hora, actualizaciones por hora y conexiones de usuario totales. Estos límites a cero significan que no hay restricciones en la cantidad de operaciones que el usuario puede realizar.

Finalmente, se otorgan todos los privilegios del sistema (`ALL PRIVILEGES`) al usuario `portafolio` sobre todas las tablas y vistas en una base de datos específica llamada `portafolio`. Esto permite que el usuario pueda realizar cualquier acción dentro de esa base de datos. La sentencia `FLUSH PRIVILEGES` se usa para forzar a MySQL a recargar la tabla de privilegios, asegurando que los cambios sean efectivos inmediatamente.

Este código es importante porque te muestra cómo gestionar usuarios y permisos en una base de datos MySQL, lo cual es crucial para mantener la seguridad del sistema.

`007-crear usuario con permisos.sql`

```sql
CREATE USER 
'portafolio'@'localhost' 
IDENTIFIED  BY 'Portafolio123$';

GRANT USAGE ON *.* TO 'portafolio'@'localhost';

ALTER USER 'portafolio'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 
MAX_CONNECTIONS_PER_HOUR 0 
MAX_UPDATES_PER_HOUR 0 
MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON `portafolio`.* 
TO 'portafolio'@'localhost';

FLUSH PRIVILEGES;
```

### demostramos actualizacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está diseñado para mostrar cómo realizar operaciones básicas en una base de datos, específicamente trabajando con una tabla llamada `piezas`. En primer lugar, se ejecuta un comando `SELECT` que busca y muestra todos los registros existentes en la tabla `piezas`.

A continuación, el código actualiza uno de estos registros utilizando el comando `UPDATE`. Aquí, la imagen asociada al registro cuyo identificador es 1 se cambia por `'josevicente.jpg'`. Este comando modifica directamente un valor específico en la base de datos según los criterios que se especifican.

Después del cambio, hay otro comando `SELECT` para verificar si el registro ha sido actualizado correctamente. Finalmente, se utiliza `DELETE` para eliminar completamente el registro con el identificador 1 de la tabla `piezas`. Tras esta operación, un último comando `SELECT * FROM piezas;` muestra que el registro ya no está en la tabla.

Este código es importante porque demuestra cómo interactuar directamente con los datos almacenados en una base de datos para realizar tareas como actualizar o eliminar información.

`008-demostramos actualizacion.sql`

```sql
SELECT * FROM piezas;

UPDATE piezas SET imagen = 'josevicente.jpg' WHERE Identificador = 1;

SELECT * FROM piezas;

DELETE FROM piezas WHERE Identificador = 1;

SELECT * FROM piezas;
```

### Actividades propuestas

### Actividad 1: Creación de una Base de Datos Personalizada

**Descripción:** 
Los estudiantes deben crear una base de datos personal que simule un blog o portafolio. Se espera que creen dos tablas relacionadas y realicen operaciones básicas como inserción, consulta y vinculación con claves foráneas.

### Actividad 2: Crear Tablas y Relaciones

**Descripción:** 
Los estudiantes deben diseñar e implementar dos tablas en una base de datos (por ejemplo, "Artículos" y "Autores") y establecer la relación entre ellas a través de claves primarias y foráneas.

### Actividad 3: Inserción y Consulta Básica

**Descripción:** 
Los estudiantes deben insertar varios registros en las tablas creadas (por ejemplo, artículos y autores) y realizar consultas para seleccionar datos basándose en diferentes criterios.

### Actividad 4: Peticiones Cruzadas

**Descripción:** 
Se requiere que los estudiantes escriban consultas SQL que realicen peticiones cruzadas entre las tablas de la base de datos, mostrando información relacionada (como artículos y autores) en una sola vista.

### Actividad 5: Creación de Vistas

**Descripción:** 
Los estudiantes deben crear vistas en su base de datos para simplificar consultas complejas. Estos ejercicios ayudarán a los estudiantes a comprender cómo las vistas pueden ser utilizadas para proporcionar acceso seguro y controlado a la información.

### Actividad 6: Gestión de Usuarios

**Descripción:** 
Los estudiantes aprenderán a crear un usuario SQL con privilegios limitados en su base de datos. Esto incluye definir contraseñas seguras y asignar los permisos adecuados para asegurar que solo se pueda acceder al contenido necesario.

### Actividad 7: Actualización de Datos

**Descripción:** 
Los estudiantes deben realizar operaciones de actualización en la base de datos, modificando datos existentes como descripciones o imágenes de artículos. Se les pedirá también validar los cambios realizados mediante consultas SELECT.

### Actividad 8: Eliminación de Datos

**Descripción:** 
Los estudiantes se familiarizarán con las operaciones DELETE para eliminar registros específicos en la base de datos. Será importante que comprendan cómo manejar estas transacciones de manera segura y eficiente.

### Actividad 9: Prueba de Seguridad

**Descripción:** 
Este ejercicio implica realizar pruebas sobre las bases de datos creadas para asegurar que los usuarios con privilegios limitados no pueden acceder a información sensible. Los estudiantes deben verificar la efectividad del control de acceso y ajustar permisos si es necesario.

### Actividad 10: Documentación del Proceso

**Descripción:** 
Los alumnos deberán documentar todo el proceso de diseño, creación e implementación de su base de datos personalizada, incluyendo detalles sobre las consultas SQL utilizadas, los usuarios creados y cualquier problema que hayan encontrado y cómo lo resolvieron.


<a id="ejercicio-de-final-de-unidad-3"></a>
## Ejercicio de final de unidad

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/004-Tratamiento%20de%20datos/101-Ejercicio%20de%20final%20de%20unidad)

### Introducción a los ejercicios

En esta sección de ejercicios, centraremos nuestra atención en el tratamiento y manipulación de datos mediante la creación de consultas SQL avanzadas. Se enfatizará la práctica de operaciones como la unión, intersección y diferencia de conjuntos, así como la implementación de subconsultas para resolver problemas complejos en bases de datos relacionales. Estos ejercicios son diseñados específicamente para reforzar las habilidades adquiridas durante el curso de Bases de Datos y preparar a los estudiantes para situaciones prácticas que requerirán un manejo eficaz de la información.

A través de este conjunto de actividades, los alumnos practicarán no solo la sintaxis SQL, sino también el pensamiento lógico y la resolución de problemas en contextos empresariales reales.

### Actividades propuestas

### Actividad 1: Análisis y Refactorización del Código

**Descripción:** Los estudiantes deben analizar el código proporcionado en el archivo `001-actividad.md` para identificar posibles áreas de mejora o refactorización. El objetivo es que comprendan cómo mejorar la legibilidad y mantenibilidad del código.

### Actividad 2: Documentación Mejorada

**Descripción:** Los estudiantes deben crear una guía detallada sobre el proceso implementado en `001-actividad.md`. Esto ayudará a entender mejor los conceptos aplicados y permitirá que otros puedan seguir fácilmente el código.

### Actividad 3: Integración de Validaciones

**Descripción:** Los estudiantes deben incorporar validaciones adicionales al código existente. El objetivo es garantizar la integridad y consistencia de los datos durante su manipulación.

### Actividad 4: Optimización del Código

**Descripción:** Los alumnos deberán revisar el código con el fin de optimizarlo, buscando alternativas que mejoren tanto el rendimiento como la eficiencia del mismo. Se busca un entendimiento práctico sobre cómo mejorar la performance.

### Actividad 5: Pruebas Automatizadas

**Descripción:** Los estudiantes deben crear pruebas unitarias y funcionales para asegurar que todas las partes del código en `001-actividad.md` estén correctamente implementadas. Se busca familiarizar a los alumnos con técnicas de testing.

### Actividad 6: Implementación de Interfaz de Usuario

**Descripción:** Los estudiantes deben diseñar y codificar una interfaz simple que permita interactuar con la lógica del código existente en `001-actividad.md`. Esto ayuda a comprender cómo integrar interfaces gráficas.

### Actividad 7: Comunicación de Errores

**Descripción:** Los alumnos deben mejorar el manejo de errores y excepciones para proporcionar mensajes claros a los usuarios sobre cualquier problema que pueda surgir durante la ejecución del código en `001-actividad.md`.

### Actividad 8: Creación de Documentación Automática

**Descripción:** Implementar herramientas o técnicas para generar documentación automáticamente basada en el código existente en `001-actividad.md`. Esto promueve la creación de documentación precisa y actualizada.

Estas actividades están diseñadas para ayudar a los estudiantes a adquirir competencias clave en programación, desde la comprensión inicial del código hasta su mejora continua y mantenibilidad.


<a id="examen-final"></a>
## Examen final

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/004-Tratamiento%20de%20datos/104-Examen%20final)

### Introducción a los ejercicios

Esta carpeta contiene un conjunto de ejercicios que te ayudarán a familiarizarte con el manejo de bases de datos utilizando SQL. Los problemas abordados van desde la creación y configuración inicial de tablas hasta operaciones más avanzadas como inserción de datos, gestión de relaciones entre tablas (usando claves foráneas), consultas JOIN y la creación de vistas. Además, también practicarás la administración de usuarios y privilegios en tu base de datos para asegurar un acceso seguro y controlado a los datos. Estos ejercicios son esenciales para desarrollar competencias clave en la gestión de bases de datos, incluyendo la estructuración de esquemas, manipulación de datos y seguridad.

### crear tablas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL sirve para crear una base de datos llamada `portafolioceac` y luego establecerla como la base de datos activa con el comando `USE`. Después, se crean dos tablas: `Piezas` y `Categorias`.

La tabla `Piezas` tiene varias columnas que almacenan información sobre diferentes piezas, como su identificador único (que se genera automáticamente), título, descripción, ruta de la imagen y una URL. También contiene un campo llamado `id_categoria`, lo cual sugiere que cada pieza está asociada a una categoría.

La tabla `Categorias` tiene dos columnas: uno para el identificador único de cada categoría y otro para almacenar información sobre el título y descripción de cada categoría. Esta estructura permite organizar las piezas en diferentes categorías, facilitando la búsqueda y administración de los datos en el sistema.

`001-crear tablas.sql`

```sql
CREATE DATABASE portafolioceac;

USE portafolioceac;


CREATE TABLE Piezas(
  Identificador INT auto_increment PRIMARY KEY,
  titulo VARCHAR(255),
  descripcion VARCHAR(255),
  imagen VARCHAR(255),
  url VARCHAR(255),
  id_categoria INT
);

CREATE TABLE Categorias(
  Identificador INT auto_increment PRIMARY KEY,
  titulo VARCHAR(255),
  descripcion VARCHAR(255)
);
```

### insertar
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para insertar datos en dos tablas diferentes: "Categorias" y "Piezas". La instrucción `INSERT INTO` es utilizada para agregar una nueva fila a la tabla especificada con los valores que proporcionas entre paréntesis.

En el primer `INSERT`, se está añadiendo un nuevo registro a la tabla "Categorias". El valor `NULL` en la primera posición indica que la base de datos debe asignar automáticamente un ID único para esta categoría. Luego, se especifican dos campos adicionales: 'General' como el nombre de la categoría y una breve descripción.

En el segundo `INSERT`, se añade una nueva pieza a la tabla "Piezas". De nuevo, colocando `NULL` en la primera posición, permitimos que la base de datos genere automáticamente un ID para esta pieza. Se proporcionan detalles adicionales como el nombre de la pieza ('Primera pieza'), una descripción ('Esta es la descripcion de la primera pieza'), un archivo imagen asociado (josevicente.jpg) y un enlace web. Finalmente, se especifica '1' que probablemente representa el ID de categoría a la cual pertenece esta pieza.

Este tipo de inserción es común cuando se está configurando una base de datos o añadiendo nuevos elementos al sistema, asegurándose de que las tablas tengan los datos iniciales necesarios para funcionar correctamente.

`002-insertar.sql`

```sql
INSERT INTO Categorias VALUES(
  NULL,
  'General',
  'Esta es la categoria general'
);

INSERT INTO Piezas VALUES(
  NULL,
  'Primera pieza',
  'Esta es la descripcion de la primera pieza',
  'josevicente.jpg',
  'https://jocarsa.com',
  1
);
```

### fk
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se utiliza para modificar una tabla existente llamada `Piezas`. Específicamente, agrega una restricción de clave externa (foreign key constraint) que vincula la columna `id_categoria` en la tabla `Piezas` con la columna `identificador` en otra tabla llamada `Categorias`. Esta restricción asegura que cada valor en `id_categoria` debe existir también como un valor en `identificador`, lo cual mantiene la integridad referencial entre las tablas.

La cláusula `ON DELETE CASCADE` indica que si se elimina una fila de la tabla `Categorias`, todas las filas en la tabla `Piezas` que hacen referencia a esa fila también serán eliminadas automáticamente. Esto ayuda a mantener consistencia en los datos al asegurar que no queden registros huérfanos.

La cláusula `ON UPDATE CASCADE` hace algo similar pero para actualizaciones: si se cambia el valor de la columna `identificador` en una fila de la tabla `Categorias`, este cambio también se propagará automáticamente a todas las filas correspondientes en la tabla `Piezas`. Esto garantiza que los datos relacionados se mantengan coherentes y sincronizados.

`003-fk.sql`

```sql
ALTER TABLE Piezas
ADD CONSTRAINT fk_piezas_categorias
FOREIGN KEY (id_categoria) REFERENCES Categorias(identificador)
ON DELETE CASCADE
ON UPDATE CASCADE;
```

### selecciones
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está formado por dos consultas sencillas que se utilizan para recuperar información de dos tablas diferentes en una base de datos. La primera consulta `SELECT * FROM Categorias;` selecciona todos los campos y registros de la tabla llamada "Categorias". Esto significa que obtendrás toda la información almacenada en esa tabla, lo cual es útil cuando necesitas revisar o analizar el contenido de las categorías.

La segunda consulta `SELECT * FROM Piezas;` hace exactamente lo mismo, pero para la tabla "Piezas", proporcionando así todos los datos relacionados con las piezas que se encuentran almacenadas en esa tabla. Ambas consultas son comunes cuando es necesario inspeccionar o verificar el estado actual de tus tablas antes de proceder a realizar operaciones más complejas, como actualizaciones, inserciones o joins con otras tablas.

Estos comandos son fundamentales para entender y gestionar los datos almacenados en tu base de datos, especialmente cuando estás trabajando en proyectos que implican manejo de catálogos y stock.

`004-selecciones.sql`

```sql
SELECT * FROM Categorias;

SELECT * FROM Piezas;
```

### left join
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL realiza una operación llamada "LEFT JOIN" entre dos tablas, `Piezas` y `Categorias`. El objetivo es combinar datos de ambas tablas basándose en la relación existente entre ellas, que se establece a través del campo `id_categoria` de la tabla `Piezas` y el campo `Identificador` de la tabla `Categorías`.

La operación LEFT JOIN asegura que todos los registros de la tabla izquierda (`Piezas`) aparezcan en el resultado. Si no hay una coincidencia con la tabla derecha (`Categorias`), los campos resultantes para esa fila mostrarán valores NULL.

Esta consulta es importante porque permite obtener información detallada sobre las piezas y sus respectivas categorías, lo que puede ser útil para entender mejor cómo están organizadas las piezas en un sistema de gestión de inventario o similar.

`005-left join.sql`

```sql
SELECT 
* 
FROM Piezas
LEFT JOIN Categorias
ON Piezas.id_categoria = Categorias.Identificador;
```

### ahora creo la vista
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está compuesto por dos partes principales: la creación de una vista y un SELECT que utiliza esa vista recién creada. Primero, se crea una vista llamada `piezas_y_categorias`. Una vista en SQL es como una tabla virtual que puede simplificar consultas complejas permitiendo tratarlas como si fueran tablas normales.

La creación de esta vista incluye un LEFT JOIN entre dos tablas: `Piezas` y `Categorias`. El objetivo del LEFT JOIN es asegurar que todas las piezas se muestren en la vista, incluso aquellas que no tienen una categoría asociada. Esto es importante porque permite conservar toda la información sobre las piezas, sin perder registros simplemente por falta de categorización.

En el SELECT dentro de la creación de la vista, se seleccionan columnas específicas de ambas tablas (como `titulo` y `descripcion` tanto para las Categorias como para las Piezas) junto con una columna adicional llamada `imagen` y otra llamada `url`, que son extraídas directamente de la tabla `Piezas`. Posteriormente, se ejecuta un SELECT * FROM piezas_y_categorias; lo cual significa que se muestra toda la información almacenada en esta vista recién creada. Esto facilita el acceso a la combinación de datos entre las tablas `Categorias` y `Piezas`, permitiendo una consulta más clara y manejable para futuros análisis o visualización de los datos.

`006-ahora creo la vista.sql`

```sql
CREATE VIEW piezas_y_categorias AS 
SELECT 
Categorias.titulo AS categoriatitulo,
Categorias.descripcion AS categoriadescripcion,
Piezas.titulo AS piezatitulo,
Piezas.descripcion AS piezadescripcion,
imagen,
url
FROM Piezas
LEFT JOIN Categorias
ON Piezas.id_categoria = Categorias.Identificador;

SELECT * FROM piezas_y_categorias;
```

### usuario
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SQL crea un nuevo usuario en el sistema MySQL y le asigna una serie de permisos para acceder a diferentes recursos. En primer lugar, se crea un usuario llamado 'portafolioceac' con una contraseña específica ('portafolioceac'), que debe ser modificada por una contraseña segura (con una combinación adecuada de mayúsculas, minúsculas, números y caracteres especiales). A continuación, se le otorga acceso limitado inicialmente a todos los recursos del sistema (`USAGE ON *.*`), lo cual es necesario para que el usuario pueda autenticarse.

Luego, mediante la instrucción `ALTER USER`, se eliminan los límites de seguridad impuestos por defecto al usuario. Esto significa que no habrá restricciones sobre cuántas consultas puede hacer por hora o cuántas conexiones simultáneas puede mantener abiertas. Finalmente, se le concede a este nuevo usuario acceso completo (`ALL PRIVILEGES`) a todos los objetos dentro de la base de datos 'portafolioceac'. Esto incluye poder leer, escribir y modificar cualquier tabla o vista en esa base de datos.

El comando `FLUSH PRIVILEGES` al final es crucial porque asegura que el sistema recargue sus tablas internas de privilegios para reflejar estos cambios inmediatamente. Sin este paso, los nuevos permisos no entrarían en vigor hasta la próxima reinicialización del servidor MySQL.

Este tipo de código es fundamental cuando se manejan entornos de desarrollo o producción con múltiples usuarios que necesitan distintos niveles de acceso a diferentes bases de datos y recursos.

`007-usuario.sql`

```sql
-- crea usuario nuevo con contraseña
-- creamos el nombre de usuario que queramos
CREATE USER 
'portafolioceac'@'localhost' 
IDENTIFIED  BY 'portafolioceac';

-- permite acceso a ese usuario
GRANT USAGE ON *.* TO 'portafolioceac'@'localhost';
--[tuservidor] == localhost
-- La contraseña puede requerir Mayus, minus, numeros, caracteres, min len

-- quitale todos los limites que tenga
ALTER USER 'portafolioceac'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 
MAX_CONNECTIONS_PER_HOUR 0 
MAX_UPDATES_PER_HOUR 0 
MAX_USER_CONNECTIONS 0;

-- dale acceso a la base de datos empresadam
GRANT ALL PRIVILEGES ON portafolioceac.* 
TO 'portafolioceac'@'localhost';

-- recarga la tabla de privilegios
FLUSH PRIVILEGES;
```

### Actividades propuestas

### Actividad 1: Crear una Base de Datos y Tablas

**Descripción**: Los alumnos deberán crear una base de datos llamada "biblioteca" e implementar dos tablas: "Libros" y "Autores". Se espera que aprendan a definir relaciones entre tablas usando claves foráneas.

### Actividad 2: Insertar Datos en Tablas

**Descripción**: Los estudiantes deben insertar datos en las tablas creadas en la actividad anterior. Esto les permitirá comprender cómo se manejan los registros y las restricciones de clave foránea.

### Actividad 3: Creación de Claves Foráneas

**Descripción**: A partir del código proporcionado, los alumnos deben añadir una clave foránea entre las tablas "Libros" y "Autores". Se espera que comprendan la importancia de mantener referencias consistentes en las bases de datos.

### Actividad 4: Consultas Básicas

**Descripción**: Los estudiantes deben realizar consultas para seleccionar todos los registros de ambas tablas. Esto les permitirá comprender cómo obtener información desde una base de datos relacional.

### Actividad 5: Join y Left Join

**Descripción**: Se les pedirá que creen una consulta LEFT JOIN entre las dos tablas, similar a la proporcionada en el archivo "left join.sql". Aprenderán a combinar registros de múltiples tablas para obtener información más completa.

### Actividad 6: Creación y Consulta de Vistas

**Descripción**: Los alumnos deben crear una vista que combine los datos de las tablas "Libros" y "Autores", como se muestra en el archivo "vista.sql". Luego, deberán consultar esta vista para ver cómo simplifica la obtención de información relacionada.

### Actividad 7: Gestión de Usuarios

**Descripción**: Los estudiantes deben crear un nuevo usuario con privilegios específicos similar a lo que se realiza en el archivo "usuario.sql". Aprenderán sobre la administración de usuarios y permisos en una base de datos MySQL.

### Actividad 8: Modificación y Actualización de Datos

**Descripción**: Se les pedirá que modifiquen o actualicen los datos existentes en las tablas creadas, incluyendo el manejo correcto de claves foráneas. Esto les ayudará a entender cómo gestionar la integridad referencial.

### Actividad 9: Borrado Condicional

**Descripción**: Los alumnos deben escribir un script que borre registros condicionalmente en las tablas "Libros" y "Autores", manteniendo siempre la consistencia en los datos gracias a claves foráneas.

### Actividad 10: Consultas Complejas con JOINs

**Descripción**: Se les pedirá que realicen consultas más complejas utilizando varios tipos de joins (INNER, LEFT) y combinaciones de tablas adicionales. Esto les permitirá entender cómo obtener información detallada desde múltiples fuentes de datos.

Estas actividades están diseñadas para proporcionar una experiencia práctica en el manejo de bases de datos relacionales con SQL, adaptando los ejercicios a un nivel adecuado para estudiantes de Formación Profesional.



<a id="programacion-de-bases-de-datos"></a>
# Programación de bases de datos

<a id="introduccion-lenguaje-de-programacion"></a>
## Introducción. Lenguaje de programación

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/005-Programaci%C3%B3n%20de%20bases%20de%20datos/001-Introducci%C3%B3n.%20Lenguaje%20de%20programaci%C3%B3n)

### Introducción a los ejercicios

El código PHP y HTML que proporcionaste es un formulario para recoger datos e insertarlos en una base de datos MySQL. A continuación, te explicaré cómo funciona cada parte del código:

### 1. Conexión a la Base de Datos
Antes del inicio del código HTML, debes establecer la conexión con tu base de datos MySQL. Para hacerlo, usa las siguientes líneas al principio del archivo PHP:
```php
<?php
$servername = "localhost";
$username = "tu_usuario";
$password = "tu_contraseña";
$dbname = "training_center";

// Crear conexión
$conn = new mysqli($servername, $username, $password, $dbname);

// Verificar la conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}
?>
```

### 2. Mensaje de Respuesta al Formulario
Si el formulario se envía correctamente, se muestra un mensaje de confirmación o error en el mismo lugar del formulario:
```php
<?php if ($mensaje != ""): ?>
    <p style="padding:10px 12px; border-radius:6px;
              background:#f8f8f8; border:1px solid #ddd;
              font-size:0.9em; color:#444;">
        <?= htmlspecialchars($mensaje, ENT_QUOTES, 'UTF-8'); ?>
    </p>
<?php endif; ?>
```

### 3. Comentarios de la Tabla
Se muestran los comentarios generales de la tabla `inscripciones` si existen:
```php
$tableComment = $conn->query("
    SELECT TABLE_COMMENT
    FROM information_schema.tables
    WHERE table_schema='training_center'
      AND table_name='inscripciones'
")->fetch_assoc()['TABLE_COMMENT'];

if ($tableComment != "") {
    echo "<p style='color:#555; margin-top:-5px; margin-bottom:20px;'>$tableComment</p>";
}
```

### 4. Generación de Elementos del Formulario
El código PHP recorre las columnas de la tabla `inscripciones` y genera elementos HTML correspondientes:

- **Texto**: Para campos `VARCHAR`, se muestra un campo de texto.
- **Fecha**: Para el tipo `DATE`, se muestra un control de fecha.
- **Número Entero**: Para campos `INT`, se utiliza un input numérico.
- **Decimal**: Para campos del tipo `DECIMAL(p,s)`, se genera un campo numérico con restricciones específicas basadas en la precisión y escala.
- **Checkbox**: Campos de tipo `TINYINT` son representados como checkboxes.
- **Select Enumerado**: Campos que usan ENUM se convierten en select boxes.
- **Textarea**: Para campos del tipo `TEXT`, se utiliza un área de texto.
- **Subida de Archivos**: Campos del tipo BLOB permiten la subida de archivos.

#### Ejemplo:
```php
while($f = $r->fetch_assoc()) {
    // ... (lógica para ignorar columnas clave primaria o autoincremental)

    echo '<div class="control_formulario">';
    echo '<label for="'.$campo.'">Introduce '.$campo.'</label>';

    if ($tipo == "varchar") {
        echo '<input type="text" name="'.$campo.'" id="'.$campo.'" maxlength="'.$f['CHARACTER_MAXIMUM_LENGTH'].'">';
    } elseif ($tipo == "date") {
        echo '<input type="date" name="'.$campo.'" id="'.$campo.'">';
    } elseif ($tipo == "int") {
        echo '<input type="number" name="'.$campo.'" id="'.$campo.'">';
    } elseif (str_contains($tipo, "decimal")) {
        preg_match('/decimal\((\d+),(\d+)\)/i', $tipo, $matches);
        $maxValue = '9' . str_repeat('0', $matches[1] - 2) . '.' . str_repeat('9', $matches[2]);
        echo '<input type="number" name="'.$campo.'" id="'.$campo.'" step="0.01" max="'.$maxValue.'">';
    } elseif (str_contains($tipo, "tinyint")) {
        echo '<div class="control_formulario_checkbox">';
        echo '<label for="'.$campo.'">Introduce '.$campo.'</label>';
        echo '<input type="checkbox" name="'.$campo.'" id="'.$campo.'">';
        echo '</div>';
    } elseif (str_contains($tipo, "enum")) {
        echo '<select name="'.$campo.'" id="'.$campo.'">';
        preg_match_all("/'([^']+)'/", $tipo, $matches);
        foreach($matches[1] as $valor){
            echo '<option value="'.$valor.'">'.$valor.'</option>';
        }
        echo '</select>';
    } elseif ($tipo == "text") {
        echo '<textarea name="'.$campo.'" id="'.$campo.'"></textarea>';
    } elseif (str_contains($tipo, "blob")) {
        echo '<input type="file" name="'.$campo.'" id="'.$campo.'">';
    }

    // Mostrar comentarios adicionales si existen
    if ($comentario != "") {
        echo '<p class="ayuda_campo">'.$comentario.'</p>';
    }

    echo '</div>';
}
```

### 5. Enviando el Formulario
El formulario utiliza `POST` para enviar los datos a la misma página. El archivo PHP se ejecuta de nuevo y procesa cualquier POST enviado.

### 6. Procesamiento del Formulario (no mostrado)
Añade lógica adicional para manejar las entradas enviadas cuando el formulario es sumitido:
```php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Lógica para validar y limpiar los datos del POST

    // Preparar consulta SQL para insertar en la tabla
    $sql = "INSERT INTO inscripciones (columna1, columna2, ...) VALUES (?, ?, ?...);";

    if ($conn->query($sql) === TRUE) {
        $mensaje = "Registro guardado exitosamente.";
    } else {
        $mensaje = "Error al guardar registro: " . $conn->error;
    }
}
```

### 7. Estilo del Formulario
Se aplica estilos para mejorar la presentación y accesibilidad del formulario.

Este es un flujo general de cómo el formulario se construye, muestra comentarios de campos, y procesa la entrada del usuario antes de insertarla en la base de datos.

### admin
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

El código que has proporcionado es un ejemplo de una página web en HTML, CSS y JavaScript que muestra datos de registros en forma de tabla. La página incluye funcionalidades avanzadas como ordenación de filas, filtrado multicriterio, modales para visualizar imágenes, entre otras.

### Resumen de las Funcionalidades:

1. **Visualización de Imágenes**:
   - Las miniaturas (thumbnails) se muestran en la tabla y al hacer clic sobre ellas se abre un modal con la imagen completa.
   
2. **Ordenación de Datos**:
   - Se puede ordenar los datos al hacer clic en las cabeceras de columna (`th`), lo que permite a los usuarios ver los registros de forma ascendente o descendente.

3. **Filtrado de Datos**:
   - Los filtros se aplican a cada columna individualmente, permitiendo a los usuarios buscar registros por criterios específicos.
   
4. **Botones Interactivos**:
   - Cada fila tiene un botón para cambiar el estado del registro (por ejemplo, desde "pendiente" a "procesado") y otro para abrir una página de informe detallado.

5. **Modales Dinámicos**:
   - Se utiliza un modal personalizado (`#image-modal`) para mostrar imágenes en gran formato cuando se hace clic en las miniaturas en la tabla.
   
### Mejoras Sugeridas:

1. **Añadir CSS Personalizado**:
   - Podrías mejorar el diseño de tu página añadiendo estilos CSS personalizados que reflejen mejor tus necesidades y preferencias, como bordes redondeados para botones, tamaños específicos para las miniaturas, etc.

2. **Optimizar la Lógica JavaScript**:
   - Asegúrate de tener una lógica clara en tu script. Puedes mejorar la legibilidad del código dividiendo tus funciones y bloques de código en secciones más pequeñas y manejables.

3. **Incluir Librerías Externas**:
   - Considera el uso de bibliotecas como jQuery o DataTables, que pueden simplificar la implementación de funcionalidades avanzadas con menor esfuerzo.

4. **Validaciones Adicionales**:
   - Añade validaciones para garantizar que los datos ingresados por el usuario sean correctos (por ejemplo, asegurarte de que un email sea válido antes de guardar el estado del registro).

5. **Incorporar Internacionalización y Localizaciones**:
   - Si tu aplicación va a ser utilizada en múltiples países o idiomas, considera la incorporación de internacionalización (`i18n`), donde los textos se pueden cambiar dinámicamente basados en el idioma seleccionado por el usuario.

6. **Documentar Códigos y Funciones**:
   - Añade comentarios a tu código para mejorar su legibilidad y mantenimiento, especialmente si trabajas en equipo o necesitas volver a revisarlo después de un tiempo.
   
### Ejemplo de Mejora Simple:

Añadir estilos CSS personalizados para los botones y las celdas filtradas:

```css
/* Estilo simple para los botones */
.btn-estado {
  background-color: #4CAF50; /* Verde claro */
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
}

.btn-informe {
  background-color: #28A745; /* Verde oscuro */
  color: white;
  padding: 6px 12px;
  margin-left: 10px;
  border: none;
  border-radius: 4px;
}

/* Estilo para celdas ocultas por filtrado */
.hidden-row {
  display: none !important;
}
```

Asegúrate de incluir estos estilos en tu HTML o vincularlos desde un archivo CSS externo. Esto mejorará la experiencia del usuario al visualizar y interactuar con los datos.

Con estas mejoras, podrás mejorar significativamente la usabilidad y la apariencia de tu aplicación web, haciendo que sea más atractiva y funcional para sus usuarios.

`admin.php`

```
<?php
session_start();

// Conexión a la base de datos (una sola vez, al inicio del archivo)
$c = new mysqli("localhost","training_center","training_center","training_center");
if ($c->connect_error) {
  die("Error de conexión: " . $c->connect_error);
}
// Conexión a la base de datos (una sola vez, al inicio del archivo)
$c = new mysqli("localhost","training_center","training_center","training_center");
if ($c->connect_error) {
  die("Error de conexión: " . $c->connect_error);
}

/*-----------------------------------------------------------
  0-bis) Metadatos de columnas de la tabla inscripciones
         (incluye detección de BLOB)
-----------------------------------------------------------*/
$tableColumns = [];
$blobColumns  = [];

$colsRes = $c->query("
  SELECT COLUMN_NAME, DATA_TYPE
  FROM information_schema.columns
  WHERE table_schema='training_center'
    AND table_name='inscripciones'
  ORDER BY ORDINAL_POSITION
");
if ($colsRes) {
  while ($col = $colsRes->fetch_assoc()) {
    $name = $col['COLUMN_NAME'];
    $tableColumns[] = $name;
    $dataType = strtolower($col['DATA_TYPE']);
    if (in_array($dataType, ['blob','tinyblob','mediumblob','longblob'])) {
      $blobColumns[$name] = true;
    }
  }
}

/*-----------------------------------------------------------
  1) Tabla auxiliar para estados CRM (NO toca inscripciones)
-----------------------------------------------------------*/
$c->query("
  CREATE TABLE IF NOT EXISTS crm_estados_inscripciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_registro VARCHAR(255) NOT NULL UNIQUE,
    estado VARCHAR(50) NOT NULL,
    color VARCHAR(20) NOT NULL
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
");

/*-----------------------------------------------------------
  2) Estados típicos de CRM (en español) + colores
-----------------------------------------------------------*/
$estadosCRM = [
  'Nuevo'             => '#3498db', // azul
  'Contactado'        => '#9b59b6', // violeta
  'En seguimiento'    => '#f1c40f', // amarillo
  'Cualificado'       => '#2ecc71', // verde
  'No interesado'     => '#95a5a6', // gris
  'Ganado'            => '#27ae60', // verde fuerte
  'Perdido'           => '#e74c3c', // rojo
];

/*-----------------------------------------------------------
  3) Detectar columna PRIMARY KEY de inscripciones
-----------------------------------------------------------*/
$primaryKeyColumn = null;
$pkResult = $c->query("
  SELECT COLUMN_NAME 
  FROM information_schema.columns
  WHERE table_schema = 'training_center'
    AND table_name   = 'inscripciones'
    AND COLUMN_KEY   = 'PRI'
  LIMIT 1;
");
if ($pkResult && $pkResult->num_rows > 0) {
  $primaryKeyColumn = $pkResult->fetch_assoc()['COLUMN_NAME'];
}

/*-----------------------------------------------------------
  4) Detectar columna de email de inscripciones
-----------------------------------------------------------*/
$emailColumn = null;
$emailColResult = $c->query("
  SELECT COLUMN_NAME
  FROM information_schema.columns
  WHERE table_schema='training_center'
    AND table_name='inscripciones'
    AND (
      COLUMN_NAME LIKE '%mail%' OR
      COLUMN_NAME LIKE '%email%' OR
      COLUMN_NAME LIKE '%correo%'
    )
  LIMIT 1;
");
if ($emailColResult && $emailColResult->num_rows > 0) {
  $emailColumn = $emailColResult->fetch_assoc()['COLUMN_NAME'];
}

/*-----------------------------------------------------------
  5) Configuración de correo (SMTP + IMAP)
-----------------------------------------------------------*/
define('CRM_MAIL_USER', 'python@jocarsa.com');
define('CRM_MAIL_PASS', 'TAME123$');
define('CRM_SMTP_HOST', 'smtp.ionos.es');
define('CRM_SMTP_PORT', 587); // STARTTLS
define('CRM_IMAP_MAILBOX', '{imap.ionos.es:993/imap/ssl}INBOX');

// *** carpeta de ENVIADOS (ajústala si IONOS usa otro nombre) ***
define('CRM_IMAP_SENT_MAILBOX', '{imap.ionos.es:993/imap/ssl}Elementos enviados');

/*-----------------------------------------------------------
  6) Función: guardar un mensaje en la carpeta "Sent" por IMAP
-----------------------------------------------------------*/
function crm_append_to_sent($rawMessage) {
  if (!function_exists('imap_open')) {
    return;
  }

  $mailbox  = CRM_IMAP_SENT_MAILBOX;
  $user     = CRM_MAIL_USER;
  $password = CRM_MAIL_PASS;

  $imap = @imap_open($mailbox, $user, $password);
  if (!$imap) {
    // si falla, simplemente no se guarda; no rompemos nada
    return;
  }

  // Fecha formato IMAP
  $date = date('d-M-Y H:i:s O'); // ej. 02-Mar-2025 12:34:56 +0100

  // Marcar como \Seen para que no cuente como no leído
  @imap_append($imap, $mailbox, $rawMessage, "\\Seen", $date);

  imap_close($imap);
}

/*-----------------------------------------------------------
  7) Función: enviar correo via SMTP (con STARTTLS + guardar en Sent)
-----------------------------------------------------------*/
function crm_send_email_smtp($to, $subject, $body, &$errorMsg) {
  $errorMsg = '';
  $smtpHost = CRM_SMTP_HOST;
  $smtpPort = CRM_SMTP_PORT;
  $username = CRM_MAIL_USER;
  $password = CRM_MAIL_PASS;
  $from     = CRM_MAIL_USER;
  $fromName = 'CRM Training Center';

  $socket = @fsockopen($smtpHost, $smtpPort, $errno, $errstr, 30);
  if (!$socket) {
    $errorMsg = "No se pudo conectar al servidor SMTP: $errstr ($errno)";
    return false;
  }

  // Banner inicial
  $resp = fgets($socket, 515);
  if (substr($resp, 0, 3) != '220') {
    $errorMsg = "Respuesta inesperada del servidor SMTP: $resp";
    fclose($socket);
    return false;
  }

  // lector de respuestas multilínea tipo 250-... / 250 ...
  $readMultiline = function($expectedCode) use ($socket, &$errorMsg) {
    $response = '';
    while (($line = fgets($socket, 515)) !== false) {
      $response .= $line;
      if (substr($line, 0, 3) != $expectedCode) {
        $errorMsg = "Respuesta inesperada del servidor SMTP: $line";
        return false;
      }
      if (strlen($line) < 4 || $line[3] != '-') {
        break;
      }
    }
    return $response;
  };

  // comandos de una sola línea
  $sendCmdOneLine = function($cmd, $expectedCode) use ($socket, &$errorMsg) {
    fputs($socket, $cmd);
    $resp = fgets($socket, 515);
    if (substr($resp, 0, 3) != $expectedCode) {
      $errorMsg = "Error SMTP al enviar '$cmd': $resp";
      return false;
    }
    return true;
  };

  // 1) EHLO inicial (sin TLS)
  fputs($socket, "EHLO localhost\r\n");
  $ehloResp = $readMultiline("250");
  if ($ehloResp === false) {
    fclose($socket);
    return false;
  }

  // 2) STARTTLS
  fputs($socket, "STARTTLS\r\n");
  $resp = fgets($socket, 515);
  if (substr($resp, 0, 3) != '220') {
    $errorMsg = "Fallo al iniciar STARTTLS: $resp";
    fclose($socket);
    return false;
  }

  // 3) Activar cifrado TLS
  $cryptoOk = @stream_socket_enable_crypto(
    $socket,
    true,
    STREAM_CRYPTO_METHOD_TLS_CLIENT
  );
  if (!$cryptoOk) {
    $errorMsg = "No se pudo activar el cifrado TLS en el socket SMTP.";
    fclose($socket);
    return false;
  }

  // 4) EHLO otra vez, ya cifrado
  fputs($socket, "EHLO localhost\r\n");
  $ehloResp2 = $readMultiline("250");
  if ($ehloResp2 === false) {
    fclose($socket);
    return false;
  }

  // 5) AUTH LOGIN
  if (!$sendCmdOneLine("AUTH LOGIN\r\n", "334")) {
    fclose($socket);
    return false;
  }

  if (!$sendCmdOneLine(base64_encode($username) . "\r\n", "334")) {
    fclose($socket);
    return false;
  }

  if (!$sendCmdOneLine(base64_encode($password) . "\r\n", "235")) {
    fclose($socket);
    return false;
  }

  // 6) MAIL FROM
  if (!$sendCmdOneLine("MAIL FROM:<$from>\r\n", "250")) {
    fclose($socket);
    return false;
  }

  // 7) RCPT TO
  if (!$sendCmdOneLine("RCPT TO:<$to>\r\n", "250")) {
    fclose($socket);
    return false;
  }

  // 8) DATA
  if (!$sendCmdOneLine("DATA\r\n", "354")) {
    fclose($socket);
    return false;
  }

  // Cabeceras + cuerpo (mensaje completo RFC822)
  $headers  = "From: " . $fromName . " <" . $from . ">\r\n";
  $headers .= "To: <$to>\r\n";
  $headers .= "Subject: " . $subject . "\r\n";
  $headers .= "MIME-Version: 1.0\r\n";
  $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
  $headers .= "Content-Transfer-Encoding: 8bit\r\n";
  $headers .= "\r\n";

  $rawMessage = $headers . $body;

  $data = $rawMessage . "\r\n.\r\n";

  fputs($socket, $data);
  $resp = fgets($socket, 515);
  if (substr($resp, 0, 3) != '250') {
    $errorMsg = "Error al completar el envío: $resp";
    fclose($socket);
    return false;
  }

  fputs($socket, "QUIT\r\n");
  fclose($socket);

  // *** Guardar una copia en la carpeta "Sent" ***
  crm_append_to_sent($rawMessage);

  return true;
}

/*-----------------------------------------------------------
  8) Función: obtener comunicaciones (INBOX + Sent) para un contacto
-----------------------------------------------------------*/
function crm_fetch_emails_for_contact($contactEmail, $limit = 20) {
  $result = [
    'sent'     => [],
    'received' => [],
    'error'    => null
  ];

  if (!function_exists('imap_open')) {
    $result['error'] = "La extensión IMAP de PHP no está habilitada.";
    return $result;
  }

  $user     = CRM_MAIL_USER;
  $password = CRM_MAIL_PASS;
  $ourAddress = strtolower(CRM_MAIL_USER);
  $safeEmail  = str_replace('"', '\"', $contactEmail);

  // helper para escanear una carpeta (INBOX o Sent)
  $scanMailbox = function($mailbox) use (&$result, $user, $password, $safeEmail, $ourAddress, $limit) {
    $inbox = @imap_open($mailbox, $user, $password);
    if (!$inbox) {
      if ($result['error'] === null) {
        $result['error'] = imap_last_error();
      }
      return;
    }

    $emailsIds = [];

    // FROM contacto
    $fromIds = imap_search($inbox, 'FROM "' . $safeEmail . '"');
    if ($fromIds !== false) {
      $emailsIds = array_merge($emailsIds, $fromIds);
    }

    // TO contacto
    $toIds = imap_search($inbox, 'TO "' . $safeEmail . '"');
    if ($toIds !== false) {
      $emailsIds = array_merge($emailsIds, $toIds);
    }

    if (!empty($emailsIds)) {
      $emailsIds = array_values(array_unique($emailsIds));
      rsort($emailsIds);
      // opcional: podríamos limitar aquí por carpeta; lo dejamos completo
    } else {
      imap_close($inbox);
      return;
    }

    foreach ($emailsIds as $num) {
      $overview = imap_fetch_overview($inbox, $num, 0);
      if (!$overview) continue;
      $ov = $overview[0];

      $header = imap_headerinfo($inbox, $num);

      $from = isset($header->fromaddress) ? $header->fromaddress : ($ov->from ?? '');
      $to   = isset($header->toaddress)   ? $header->toaddress   : ($ov->to   ?? '');

      $subject = isset($ov->subject) ? imap_utf8($ov->subject) : '';
      $date    = isset($ov->date)    ? $ov->date : '';

      $body = imap_fetchbody($inbox, $num, 1);
      if (!$body) $body = '';
      $body = imap_qprint($body);
      $snippet = trim($body);
      if (function_exists('mb_substr')) {
        $snippet = mb_substr($snippet, 0, 200);
      } else {
        $snippet = substr($snippet, 0, 200);
      }

      $entry = [
        'subject' => $subject,
        'date'    => $date,
        'from'    => $from,
        'to'      => $to,
        'snippet' => $snippet
      ];

      $fromLower = strtolower($from);
      if (strpos($fromLower, $ourAddress) !== false) {
        $result['sent'][] = $entry;
      } else {
        $result['received'][] = $entry;
      }
    }

    imap_close($inbox);
  };

  // Escanear INBOX y Sent
  $scanMailbox(CRM_IMAP_MAILBOX);
  $scanMailbox(CRM_IMAP_SENT_MAILBOX);

  // Ordenar por fecha dentro de enviados y recibidos (descendente)
  $sortByDateDesc = function(&$arr) {
    usort($arr, function($a, $b) {
      $da = strtotime($a['date'] ?? '1970-01-01');
      $db = strtotime($b['date'] ?? '1970-01-01');
      return $db <=> $da;
    });
  };

  $sortByDateDesc($result['sent']);
  $sortByDateDesc($result['received']);

  // Aplicar límite por tipo
  if ($limit > 0) {
    $result['sent']     = array_slice($result['sent'], 0, $limit);
    $result['received'] = array_slice($result['received'], 0, $limit);
  }

  return $result;
}

/*-----------------------------------------------------------
  9) LOGIN / LOGOUT
-----------------------------------------------------------*/
$login_error = "";

if (isset($_GET['logout'])) {
  session_destroy();
  header("Location: " . $_SERVER['PHP_SELF']);
  exit;
}

if (isset($_POST['action']) && $_POST['action'] === 'login') {
  $usuario  = $_POST['usuario']  ?? '';
  $password = $_POST['password'] ?? '';

  if ($usuario === 'jocarsa' && $password === 'jocarsa') {
    $_SESSION['admin_logged'] = true;
    header("Location: " . $_SERVER['PHP_SELF']);
    exit;
  } else {
    $login_error = "Usuario o contraseña incorrectos.";
  }
}

$loggedIn = isset($_SESSION['admin_logged']) && $_SESSION['admin_logged'] === true;

/*-----------------------------------------------------------
  10) Actualización de estado CRM
-----------------------------------------------------------*/
if (
  $loggedIn &&
  isset($_POST['action']) &&
  $_POST['action'] === 'update_estado'
) {
  $id_registro = $_POST['id_registro'] ?? null;
  $estado      = $_POST['estado']      ?? null;

  if ($id_registro !== null && isset($estadosCRM[$estado])) {
    $color = $estadosCRM[$estado];

    $stmt = $c->prepare("
      INSERT INTO crm_estados_inscripciones (id_registro, estado, color)
      VALUES (?, ?, ?)
      ON DUPLICATE KEY UPDATE
        estado = VALUES(estado),
        color  = VALUES(color)
    ");
    if ($stmt) {
      $stmt->bind_param("sss", $id_registro, $estado, $color);
      $stmt->execute();
      $stmt->close();
    }
  }
}

/*-----------------------------------------------------------
  11) Envío de email desde el informe
-----------------------------------------------------------*/
$emailSendMessage = "";

if (
  $loggedIn &&
  isset($_POST['action']) &&
  $_POST['action'] === 'send_email'
) {
  $to      = $_POST['to']      ?? '';
  $subject = $_POST['subject'] ?? '';
  $body    = $_POST['body']    ?? '';

  if ($to && $subject && $body) {
    $errorMsg = '';
    $ok = crm_send_email_smtp($to, $subject, $body, $errorMsg);
    if ($ok) {
      $emailSendMessage = "Mensaje enviado correctamente.";
    } else {
      $emailSendMessage = "Error al enviar el mensaje: " . htmlspecialchars($errorMsg, ENT_QUOTES, 'UTF-8');
    }
  } else {
    $emailSendMessage = "Por favor, rellena todos los campos del mensaje.";
  }
}

/*-----------------------------------------------------------
  12) Estados actuales (para la tabla)
-----------------------------------------------------------*/
$estadosActuales = [];
if ($loggedIn) {
  $resEstados = $c->query("SELECT id_registro, estado, color FROM crm_estados_inscripciones");
  if ($resEstados) {
    while ($row = $resEstados->fetch_assoc()) {
      $estadosActuales[$row['id_registro']] = $row;
    }
  }
}

/*-----------------------------------------------------------
  13) Mapa de correos NO LEÍDOS por contacto (para la tabla)
-----------------------------------------------------------*/
// *** nueva funcionalidad: marcar si hay emails sin leer de cada contacto ***
$unreadByEmail = [];
if ($loggedIn && $emailColumn !== null && function_exists('imap_open')) {
  $mailbox  = CRM_IMAP_MAILBOX; // INBOX
  $user     = CRM_MAIL_USER;
  $password = CRM_MAIL_PASS;

  $inbox = @imap_open($mailbox, $user, $password);
  if ($inbox) {
    $unseenIds = imap_search($inbox, 'UNSEEN');
    if ($unseenIds !== false) {
      foreach ($unseenIds as $num) {
        $header = imap_headerinfo($inbox, $num);
        if (!empty($header->from)) {
          // from es un array de objetos (mailbox + host)
          foreach ($header->from as $fromObj) {
            $fromEmail = strtolower(trim($fromObj->mailbox . '@' . $fromObj->host));
            if ($fromEmail !== '' && $fromEmail !== strtolower(CRM_MAIL_USER)) {
              $unreadByEmail[$fromEmail] = true;
            }
          }
        }
      }
    }
    imap_close($inbox);
  }
}

/*-----------------------------------------------------------
  14) ID de informe (vista detalle)
-----------------------------------------------------------*/
$viewId = null;
if ($loggedIn && isset($_GET['view'])) {
  $viewId = $_GET['view'];
}

?>
<!doctype html>
<html lang="es">
  <head>
    <title>Panel de administración</title>
    <meta charset="utf-8">
    <style>
      :root{
        --primary: crimson;
        --primary-light: #ff8fa0;
        --bg: #f2f2f2;
        --text: #333;
        --border: #ddd;
      }

      *{
        box-sizing:border-box;
        margin:0;
        padding:0;
      }

      html, body{
        height:100%;
        font-family: "Segoe UI", sans-serif;
        color: var(--text);
        background: var(--bg);
      }

      body{
        display:flex;
        align-items:stretch;
      }

      /*---------------- LOGIN ----------------*/
      .login-wrapper{
        width:100%;
        display:flex;
        justify-content:center;
        align-items:center;
        padding:40px;
      }
      .login-card{
        background:white;
        padding:30px 40px;
        width:360px;
        border-radius:10px;
        box-shadow:0 4px 15px rgba(0,0,0,0.1);
        border-top:8px solid var(--primary);
      }
      .login-card h2{
        margin-bottom:20px;
        color:var(--primary);
        font-size:1.4em;
      }
      .login-card .form-group{
        margin-bottom:15px;
        display:flex;
        flex-direction:column;
        gap:6px;
      }
      .login-card label{
        font-size:0.95em;
        font-weight:600;
        color:var(--primary);
      }
      .login-card input[type="text"],
      .login-card input[type="password"]{
        padding:10px 12px;
        border-radius:6px;
        border:1px solid var(--border);
        font-size:1em;
      }
      .login-card input[type="submit"]{
        margin-top:10px;
        width:100%;
        padding:12px;
        border:none;
        border-radius:6px;
        background:var(--primary);
        color:white;
        font-size:1em;
        cursor:pointer;
      }
      .login-error{
        margin-bottom:10px;
        padding:8px 10px;
        border-radius:6px;
        background:#ffe6e6;
        border:1px solid #ffb3b3;
        font-size:0.9em;
        color:#b30000;
      }

      /*---------------- LAYOUT ADMIN ----------------*/
      nav{
        width:240px;
        background: var(--primary);
        padding:20px;
        display:flex;
        flex-direction:column;
        gap:10px;
        box-shadow: 4px 0 12px rgba(0,0,0,0.1);
      }

      nav h2{
        color:white;
        margin-bottom:15px;
        font-size:1.1em;
        font-weight:700;
      }

      nav button{
        background:white;
        border:none;
        padding:10px 14px;
        border-radius:999px;
        cursor:pointer;
        font-size:0.95em;
        text-align:left;
        transition: transform 0.15s, box-shadow 0.15s, background 0.15s;
      }

      nav button:hover{
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        background:#fff5f7;
      }

      main{
        flex:1;
        padding:30px 40px;
        display:flex;
        flex-direction:column;
        gap:15px;
      }

      header{
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-bottom:10px;
      }

      header h1{
        font-size:1.4em;
        color:var(--primary);
      }

      .user-actions{
        display:flex;
        gap:10px;
        align-items:center;
        font-size:0.9em;
      }
      .logout-link{
        padding:6px 10px;
        border-radius:999px;
        border:1px solid var(--primary-light);
        color:var(--primary);
        text-decoration:none;
        font-size:0.85em;
        background:white;
      }
      .back-link{
        padding:6px 10px;
        border-radius:999px;
        border:1px solid var(--border);
        color:#555;
        text-decoration:none;
        font-size:0.8em;
        background:white;
        margin-right:10px;
      }

      .table-card,
      .detail-card{
        background:white;
        border-radius:10px;
        padding:20px 24px;
        box-shadow:0 4px 15px rgba(0,0,0,0.08);
        border-top:8px solid var(--primary);
      }

      .table-card h3,
      .detail-card h3{
        margin-bottom:10px;
        font-size:1.1em;
        color:var(--primary);
      }

      .table-card p.description,
      .detail-card p.description{
        margin-bottom:10px;
        font-size:0.9em;
        color:#666;
      }

      table{
        width:100%;
        border-collapse:collapse;
        font-size:0.9em;
      }

      thead th{
        text-align:left;
        padding:10px 8px;
        border-bottom:2px solid var(--primary-light);
        color:var(--primary);
        font-weight:600;
      }

      tbody td{
        padding:8px 8px;
        border-bottom:1px solid var(--border);
        vertical-align:middle;
      }

      tbody tr:nth-child(even){
        background:#fafafa;
      }

      tbody tr:hover{
        background:#ffeef2;
      }

      .estado-pill{
        display:inline-block;
        padding:4px 10px;
        border-radius:999px;
        border:1px solid var(--border);
        font-size:0.8em;
        background:#f9f9f9;
      }
      .estado-pill--vacio{
        color:#999;
        border-style:dashed;
      }

      .form-estado{
        display:flex;
        gap:6px;
        align-items:center;
      }
      .form-estado select{
        padding:4px 6px;
        border-radius:4px;
        border:1px solid var(--border);
        font-size:0.85em;
      }
      .btn-estado{
        padding:4px 8px;
        border-radius:4px;
        border:none;
        background:var(--primary);
        color:white;
        font-size:0.8em;
        cursor:pointer;
      }

      .btn-informe{
        padding:4px 8px;
        border-radius:4px;
        border:none;
        background:#34495e;
        color:white;
        font-size:0.8em;
        cursor:pointer;
        text-decoration:none;
        display:inline-block;
      }

      .badge-unread{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        min-width:22px;
        height:22px;
        border-radius:999px;
        background:#2ecc71;
        color:white;
        font-size:0.75em;
        font-weight:bold;
      }
      .badge-unread::before{
        content:"✉";
        margin-right:3px;
      }
      .badge-none{
        font-size:0.75em;
        color:#aaa;
      }

      /* Detalle */
      .detail-row-table{
        width:100%;
        border-collapse:collapse;
        margin-bottom:20px;
      }
      .detail-row-table th,
      .detail-row-table td{
        padding:6px 8px;
        border-bottom:1px solid var(--border);
        text-align:left;
      }
      .detail-row-table th{
        width:30%;
        color:var(--primary);
      }

      .email-section{
        margin-top:20px;
        display:grid;
        grid-template-columns:1.2fr 1.8fr;
        gap:20px;
      }
      .email-form-card,
      .email-log-card{
        background:#fafafa;
        border-radius:8px;
        padding:15px 18px;
        border:1px solid #e5e5e5;
      }
      .email-form-card h4,
      .email-log-card h4{
        margin-bottom:8px;
        color:#444;
      }
      .email-form-card .form-group{
        margin-bottom:10px;
        display:flex;
        flex-direction:column;
        gap:4px;
      }
      .email-form-card label{
        font-size:0.85em;
        font-weight:600;
      }
      .email-form-card input[type="text"],
      .email-form-card textarea{
        padding:8px 10px;
        border-radius:4px;
        border:1px solid var(--border);
        font-size:0.9em;
        resize:vertical;
      }
      .email-form-card textarea{
        min-height:120px;
      }
      .email-form-card input[type="submit"]{
        margin-top:8px;
        padding:8px 12px;
        border:none;
        border-radius:4px;
        background:var(--primary);
        color:white;
        font-size:0.9em;
        cursor:pointer;
      }
      .email-status-msg{
        margin-bottom:10px;
        padding:6px 8px;
        border-radius:6px;
        font-size:0.85em;
      }
      .email-status-ok{
        background:#e7f7ec;
        border:1px solid #9dd7b1;
        color:#217346;
      }
      .email-status-error{
        background:#ffe6e6;
        border:1px solid #ffb3b3;
        color:#b30000;
      }

      .mail-list{
        max-height:280px;
        overflow:auto;
        font-size:0.86em;
      }
      .mail-item{
        padding:8px 0;
        border-bottom:1px solid #e3e3e3;
      }
      .mail-item:last-child{
        border-bottom:none;
      }
      .mail-item strong{
        color:#333;
      }
      .mail-meta{
        font-size:0.8em;
        color:#777;
        margin-bottom:2px;
      }
      .mail-snippet{
        font-size:0.85em;
        color:#555;
      }

      @media (max-width: 900px){
        body{
          flex-direction:column;
        }
        nav{
          width:100%;
          flex-direction:row;
          flex-wrap:wrap;
          box-shadow:none;
        }
        nav h2{
          width:100%;
        }
        main{
          padding:20px;
        }
        .email-section{
          grid-template-columns:1fr;
        }
      }
      .thumb-image{
  max-width:60px;
  max-height:60px;
  border-radius:4px;
  cursor:zoom-in;
  object-fit:cover;
  box-shadow:0 0 0 1px rgba(0,0,0,0.1);
}

/* Modal de imagen */
.image-modal{
  position:fixed;
  inset:0;
  display:none;
  align-items:center;
  justify-content:center;
  z-index:9999;
}
.image-modal.is-visible{
  display:flex;
}
.image-modal__backdrop{
  position:absolute;
  inset:0;
  background:rgba(0,0,0,0.6);
}
.image-modal__content{
  position:relative;
  max-width:90%;
  max-height:90%;
  padding:10px;
  background:#fff;
  border-radius:8px;
  box-shadow:0 8px 24px rgba(0,0,0,0.4);
}
.image-modal__content img{
  max-width:100%;
  max-height:80vh;
  display:block;
}
.filters-row input{
  border:1px solid lightgray;
  padding:5px;
  width:100%;
}
    </style>
  </head>
  <body>

  <?php if (!$loggedIn): ?>

    <!-- ------------------ VISTA LOGIN ------------------ -->
    <div class="login-wrapper">
      <form method="post" class="login-card">
        <h2>Acceso al panel</h2>

        <?php if ($login_error !== ""): ?>
          <div class="login-error">
            <?= htmlspecialchars($login_error, ENT_QUOTES, 'UTF-8'); ?>
          </div>
        <?php endif; ?>

        <div class="form-group">
          <label for="usuario">Usuario</label>
          <input type="text" name="usuario" id="usuario" autocomplete="username">
        </div>

        <div class="form-group">
          <label for="password">Contraseña</label>
          <input type="password" name="password" id="password" autocomplete="current-password">
        </div>

        <input type="hidden" name="action" value="login">
        <input type="submit" value="Entrar">
      </form>
    </div>

  <?php else: ?>

    <!-- ------------------ PANEL ADMIN ------------------ -->
    <nav>
      <h2>Menú</h2>
      <button>Enlace 1</button>
      <button>Enlace 2</button>
      <button>Enlace 3</button>
    </nav>
    <main>
      <?php
        $title = $viewId ? "Informe de inscripción" : "Listado de inscripciones";
      ?>
      <header>
        <div style="display:flex; align-items:center; gap:8px;">
          <?php if ($viewId): ?>
            <a href="<?= htmlspecialchars($_SERVER['PHP_SELF'], ENT_QUOTES, 'UTF-8'); ?>" class="back-link">← Volver al listado</a>
          <?php endif; ?>
          <h1><?= htmlspecialchars($title, ENT_QUOTES, 'UTF-8'); ?></h1>
        </div>
        <div class="user-actions">
          <span>Conectado como <strong>jocarsa</strong></span>
          <a class="logout-link" href="?logout=1">Cerrar sesión</a>
        </div>
      </header>

      <?php if ($viewId && $primaryKeyColumn !== null): ?>

        <?php
          // Cargar la fila concreta
          $filaDetalle = null;
          $stmt = $c->prepare("SELECT * FROM inscripciones WHERE $primaryKeyColumn = ? LIMIT 1");
          if ($stmt) {
            $stmt->bind_param("s", $viewId);
            $stmt->execute();
            $result = $stmt->get_result();
            $filaDetalle = $result->fetch_assoc();
            $stmt->close();
          }
        ?>

        <?php if ($filaDetalle): ?>
          <?php
            // Determinar email de contacto (si existe columna de email)
            $contactEmail = null;
            if ($emailColumn !== null && isset($filaDetalle[$emailColumn])) {
              $contactEmail = $filaDetalle[$emailColumn];
            }

            // Obtener comunicaciones por email si tenemos correo
            $commReport = null;
            if ($contactEmail) {
              $commReport = crm_fetch_emails_for_contact($contactEmail, 20);
            }
          ?>

          <section class="detail-card">
            <h3>Datos de la inscripción (ID: <?= htmlspecialchars($viewId, ENT_QUOTES, 'UTF-8'); ?>)</h3>
            <p class="description">
              Detalle completo del registro seleccionado en la tabla
              <strong>inscripciones</strong>, junto con el historial de comunicaciones
              por correo electrónico asociado al contacto.
            </p>

            <table class="detail-row-table">
  <tbody>
    <?php foreach ($filaDetalle as $campo => $valor): ?>
      <tr>
        <th><?= htmlspecialchars($campo, ENT_QUOTES, 'UTF-8'); ?></th>
        <td>
          <?php if (isset($blobColumns[$campo]) && $valor !== null && $valor !== ''): ?>
            <?php
              $mime = 'image/jpeg';
              if (strpos($valor, "\x89PNG") === 0) {
                $mime = 'image/png';
              } elseif (strpos($valor, "GIF8") === 0) {
                $mime = 'image/gif';
              }
              $b64 = base64_encode($valor);
              $src = 'data:'.$mime.';base64,'.$b64;
            ?>
            <img src="<?= $src; ?>"
                 data-full="<?= $src; ?>"
                 class="thumb-image"
                 style="max-width:120px; max-height:120px;"
                 alt="Documento">
          <?php else: ?>
            <?= htmlspecialchars((string)$valor, ENT_QUOTES, 'UTF-8'); ?>
          <?php endif; ?>
        </td>
      </tr>
    <?php endforeach; ?>
  </tbody>
</table>


            <div class="email-section">
              <div class="email-form-card">
                <h4>Enviar mensaje al contacto</h4>

                <?php if ($emailSendMessage): ?>
                  <div class="email-status-msg <?= (strpos($emailSendMessage, 'correctamente') !== false) ? 'email-status-ok' : 'email-status-error'; ?>">
                    <?= $emailSendMessage; ?>
                  </div>
                <?php endif; ?>

                <?php if ($contactEmail): ?>
                  <p style="font-size:0.85em; margin-bottom:8px;">
                    Correo del contacto:
                    <strong><?= htmlspecialchars($contactEmail, ENT_QUOTES, 'UTF-8'); ?></strong><br>
                    Remitente usado: <code><?= htmlspecialchars(CRM_MAIL_USER, ENT_QUOTES, 'UTF-8'); ?></code>
                  </p>

                  <form method="post" action="?view=<?= urlencode($viewId); ?>">
                    <div class="form-group">
                      <label for="subject">Asunto</label>
                      <input type="text" id="subject" name="subject">
                    </div>
                    <div class="form-group">
                      <label for="body">Mensaje</label>
                      <textarea id="body" name="body"></textarea>
                    </div>
                    <input type="hidden" name="to" value="<?= htmlspecialchars($contactEmail, ENT_QUOTES, 'UTF-8'); ?>">
                    <input type="hidden" name="action" value="send_email">
                    <input type="submit" value="Enviar mensaje">
                  </form>
                <?php else: ?>
                  <p style="font-size:0.85em; color:#b30000;">
                    No se ha detectado ninguna columna de email para este registro.  
                    El envío de correos no está disponible.
                  </p>
                <?php endif; ?>
              </div>

              <div class="email-log-card">
                <h4>Comunicaciones por correo</h4>

                <?php if (!$contactEmail): ?>
                  <p style="font-size:0.85em; color:#555;">
                    No hay correo electrónico asociado a este registro.<br>
                    Por tanto, no se puede generar el informe de comunicaciones.
                  </p>
                <?php else: ?>
                  <?php if ($commReport && $commReport['error']): ?>
                    <p style="font-size:0.85em; color:#b30000;">
                      Error al acceder al buzón IMAP:
                      <?= htmlspecialchars($commReport['error'], ENT_QUOTES, 'UTF-8'); ?>
                    </p>
                  <?php else: ?>
                    <div class="mail-list">
                      <?php
                        $sent     = $commReport ? $commReport['sent']     : [];
                        $received = $commReport ? $commReport['received'] : [];
                      ?>

                      <p class="mail-meta">
                        Mensajes enviados: <?= count($sent); ?> |
                        Mensajes recibidos: <?= count($received); ?>
                      </p>

                      <?php if (empty($sent) && empty($received)): ?>
                        <p style="font-size:0.85em; color:#555;">
                          No se han encontrado mensajes relacionados con
                          <strong><?= htmlspecialchars($contactEmail, ENT_QUOTES, 'UTF-8'); ?></strong>.
                        </p>
                      <?php else: ?>

                        <?php if (!empty($sent)): ?>
                          <p style="margin-top:8px; font-weight:bold; font-size:0.9em;">Enviados (<?= count($sent); ?>)</p>
                          <?php foreach ($sent as $mail): ?>
                            <div class="mail-item">
                              <div class="mail-meta">
                                <strong>Asunto:</strong> <?= htmlspecialchars($mail['subject'], ENT_QUOTES, 'UTF-8'); ?><br>
                                <strong>Fecha:</strong> <?= htmlspecialchars($mail['date'], ENT_QUOTES, 'UTF-8'); ?><br>
                                <strong>De:</strong> <?= htmlspecialchars($mail['from'], ENT_QUOTES, 'UTF-8'); ?><br>
                                <strong>Para:</strong> <?= htmlspecialchars($mail['to'], ENT_QUOTES, 'UTF-8'); ?>
                              </div>
                              <div class="mail-snippet">
                                <?= nl2br(htmlspecialchars($mail['snippet'], ENT_QUOTES, 'UTF-8')); ?>
                              </div>
                            </div>
                          <?php endforeach; ?>
                        <?php endif; ?>

                        <?php if (!empty($received)): ?>
                          <p style="margin-top:10px; font-weight:bold; font-size:0.9em;">Recibidos (<?= count($received); ?>)</p>
                          <?php foreach ($received as $mail): ?>
                            <div class="mail-item">
                              <div class="mail-meta">
                                <strong>Asunto:</strong> <?= htmlspecialchars($mail['subject'], ENT_QUOTES, 'UTF-8'); ?><br>
                                <strong>Fecha:</strong> <?= htmlspecialchars($mail['date'], ENT_QUOTES, 'UTF-8'); ?><br>
                                <strong>De:</strong> <?= htmlspecialchars($mail['from'], ENT_QUOTES, 'UTF-8'); ?><br>
                                <strong>Para:</strong> <?= htmlspecialchars($mail['to'], ENT_QUOTES, 'UTF-8'); ?>
                              </div>
                              <div class="mail-snippet">
                                <?= nl2br(htmlspecialchars($mail['snippet'], ENT_QUOTES, 'UTF-8')); ?>
                              </div>
                            </div>
                          <?php endforeach; ?>
                        <?php endif; ?>

                      <?php endif; ?>
                    </div>
                  <?php endif; ?>
                <?php endif; ?>
              </div>
            </div>
          </section>
        <?php else: ?>
          <section class="detail-card">
            <h3>Registro no encontrado</h3>
            <p class="description">
              No se ha podido localizar la inscripción con identificador
              <strong><?= htmlspecialchars($viewId, ENT_QUOTES, 'UTF-8'); ?></strong>.
            </p>
          </section>
        <?php endif; ?>

      <?php else: ?>

        <!-- -------- LISTADO GENERAL DE INSCRIPCIONES -------- -->
        <section class="table-card">
          <h3>Tabla: inscripciones</h3>
          <p class="description">
            Registros actuales en la tabla <strong>inscripciones</strong> de la base de datos
            <strong>training_center</strong>. Puede asignar un estado CRM a cada registro,
            ver si hay correos nuevos sin leer y acceder a un informe detallado.
          </p>

         <table id="inscripciones-table">
  <thead>
    <tr>
      <?php
        // Cabeceras de las columnas originales
        foreach ($tableColumns as $colName) {
          echo '<th>'.htmlspecialchars($colName, ENT_QUOTES, 'UTF-8').'</th>';
        }

        // Columna Emails nuevos + Estado CRM + Acciones
        echo '<th>Emails nuevos</th>';
        echo '<th>Estado CRM</th>';
        echo '<th>Acciones</th>';
      ?>
    </tr>
    <tr class="filters-row">
      <?php
        $filterColsCount = count($tableColumns) + 3; // Emails nuevos + Estado CRM + Acciones
        for ($i = 0; $i < $filterColsCount; $i++) {
          echo '<th><input type="text" class="column-filter" placeholder="Filtrar..."></th>';
        }
      ?>
    </tr>
  </thead>
            <tbody>
              <?php
                $r = $c->query("SELECT * FROM inscripciones;");

                while($f = $r->fetch_assoc()) {
                  // ID del registro basado en la columna PK detectada (si existe)
                  $idRegistro = null;
                  if ($primaryKeyColumn !== null && isset($f[$primaryKeyColumn])) {
                    $idRegistro = (string)$f[$primaryKeyColumn];
                  }

                  // Normalizar email de este registro, si existe
                  $rowEmailNorm = null;
                  if ($emailColumn !== null && isset($f[$emailColumn]) && $f[$emailColumn] !== '') {
                    $rowEmailNorm = strtolower(trim($f[$emailColumn]));
                  }

                    echo '<tr>';

  // Mostrar todas las columnas originales (incluyendo BLOB como imagen)
  foreach($f as $clave=>$valor){
    // Si es columna BLOB, intentamos mostrar miniatura
    if (isset($blobColumns[$clave]) && $valor !== null && $valor !== '') {

      // Detección simple del tipo de imagen
      $mime = 'image/jpeg';
      if (strpos($valor, "\x89PNG") === 0) {
        $mime = 'image/png';
      } elseif (strpos($valor, "GIF8") === 0) {
        $mime = 'image/gif';
      }

      $b64 = base64_encode($valor);
      $src = 'data:'.$mime.';base64,'.$b64;

      // data-sort="imagen" para que el ordenado tenga un valor textual
      echo '<td data-sort="imagen">';
      echo '<img src="'.$src.'" data-full="'.$src.'" class="thumb-image" alt="Documento">';
      echo '</td>';
    } else {
      echo '<td>'.htmlspecialchars((string)$valor, ENT_QUOTES, 'UTF-8').'</td>';
    }
  }


                  // *** Columna Emails nuevos ***
                  echo '<td>';
                  if ($rowEmailNorm && isset($unreadByEmail[$rowEmailNorm])) {
                    echo '<span class="badge-unread" title="Nuevo(s) email(s) sin leer de este contacto.">!</span>';
                  } else {
                    echo '<span class="badge-none">—</span>';
                  }
                  echo '</td>';

                  // Columna "Estado CRM" (pastilla de color)
                  echo '<td>';
                  if ($idRegistro !== null && isset($estadosActuales[$idRegistro])) {
                    $estadoRow = $estadosActuales[$idRegistro];
                    $estadoTxt = htmlspecialchars($estadoRow['estado'], ENT_QUOTES, 'UTF-8');
                    $colorTxt  = htmlspecialchars($estadoRow['color'],  ENT_QUOTES, 'UTF-8');

                    echo '<span class="estado-pill" style="background:'.$colorTxt.'20; border-color:'.$colorTxt.'; color:'.$colorTxt.';">';
                    echo $estadoTxt;
                    echo '</span>';
                  } else {
                    echo '<span class="estado-pill estado-pill--vacio">Sin estado</span>';
                  }
                  echo '</td>';

                  // Columna "Acciones" (selector estado + botón + informe)
                  echo '<td>';
                  if ($idRegistro !== null) {
                    // Formulario de estado
                    echo '<form method="post" class="form-estado" style="margin-bottom:4px;">';
                    echo '<input type="hidden" name="action" value="update_estado">';
                    echo '<input type="hidden" name="id_registro" value="'.htmlspecialchars($idRegistro, ENT_QUOTES, 'UTF-8').'">';
                    echo '<select name="estado">';
                    foreach ($estadosCRM as $nombreEstado => $colorEstado) {
                      $selected = (
                        $idRegistro !== null &&
                        isset($estadosActuales[$idRegistro]) &&
                        $estadosActuales[$idRegistro]['estado'] === $nombreEstado
                      ) ? ' selected' : '';
                      echo '<option value="'.htmlspecialchars($nombreEstado, ENT_QUOTES, 'UTF-8').'"'.$selected.'>';
                      echo htmlspecialchars($nombreEstado, ENT_QUOTES, 'UTF-8');
                      echo '</option>';
                    }
                    echo '</select>';
                    echo '<button type="submit" class="btn-estado">Guardar</button>';
                    echo '</form>';

                    // Enlace a informe
                    $urlInforme = htmlspecialchars($_SERVER['PHP_SELF'], ENT_QUOTES, 'UTF-8') . '?view=' . urlencode($idRegistro);
                    echo '<a class="btn-informe" href="'.$urlInforme.'">Informe</a>';
                  }
                  echo '</td>';

                  echo '</tr>';
                }
              ?>
            </tbody>
          </table>
        </section>

      <?php endif; ?>

    </main>

  <?php endif; ?>
<div id="image-modal" class="image-modal">
  <div class="image-modal__backdrop"></div>
  <div class="image-modal__content">
    <img id="image-modal-img" src="" alt="Documento">
  </div>
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {
  /*---------------- MODAL DE IMAGEN ----------------*/
  const modal    = document.getElementById('image-modal');
  const modalImg = document.getElementById('image-modal-img');

  if (modal && modalImg) {
    // Abrir modal al hacer clic en una miniatura
    document.body.addEventListener('click', function(e) {
      const thumb = e.target.closest('.thumb-image');
      if (thumb) {
        const src = thumb.getAttribute('data-full') || thumb.getAttribute('src');
        if (src) {
          modalImg.src = src;
          modal.classList.add('is-visible');
        }
      }
    });

    // Cerrar modal al hacer clic en fondo
    modal.addEventListener('click', function(e) {
      if (e.target === modal || e.target.classList.contains('image-modal__backdrop')) {
        modal.classList.remove('is-visible');
        modalImg.src = '';
      }
    });

    // Cerrar con Escape
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && modal.classList.contains('is-visible')) {
        modal.classList.remove('is-visible');
        modalImg.src = '';
      }
    });
  }

  /*---------------- TABLA: ORDENACIÓN + FILTROS ----------------*/
  const table = document.getElementById('inscripciones-table');
  if (table && table.tBodies.length > 0) {
    const tbody = table.tBodies[0];

    // Obtener texto base para orden y filtro
    const getCellText = (row, idx) => {
      const cell = row.cells[idx];
      if (!cell) return '';
      const dataSort = cell.getAttribute('data-sort');
      if (dataSort !== null) {
        return dataSort.toLowerCase();
      }
      return (cell.textContent || '').trim().toLowerCase();
    };

    /*--- Ordenación al hacer clic en cabeceras ---*/
    const headerRow   = table.querySelector('thead tr:first-child');
    const headerCells = headerRow ? headerRow.querySelectorAll('th') : [];

    headerCells.forEach((th, index) => {
      th.style.cursor = 'pointer';
      th.addEventListener('click', function() {
        const rows = Array.from(tbody.rows);
        const currentDir = th.getAttribute('data-sort-dir') === 'asc' ? 'desc' : 'asc';

        // Limpiar indicador en otras columnas
        headerCells.forEach(h => h.removeAttribute('data-sort-dir'));
        th.setAttribute('data-sort-dir', currentDir);

        rows.sort((a, b) => {
          const va = getCellText(a, index);
          const vb = getCellText(b, index);

          // Intento de orden numérico si ambos parecen números
          const na = parseFloat(va.replace(',', '.'));
          const nb = parseFloat(vb.replace(',', '.'));
          const bothNumeric = !isNaN(na) && !isNaN(nb);

          if (bothNumeric) {
            return currentDir === 'asc' ? na - nb : nb - na;
          }
          return currentDir === 'asc'
            ? va.localeCompare(vb)
            : vb.localeCompare(va);
        });

        rows.forEach(r => tbody.appendChild(r));
      });
    });

    /*--- Filtros por columna (multicriterio) ---*/
    const filterInputs = table.querySelectorAll('thead .column-filter');

    const applyFilters = () => {
      const filters = Array.from(filterInputs).map(input =>
        (input.value || '').trim().toLowerCase()
      );

      Array.from(tbody.rows).forEach(row => {
        let visible = true;

        filters.forEach((value, colIdx) => {
          if (!value) return; // sin filtro en esta columna

          const cellText = getCellText(row, colIdx);
          if (cellText.indexOf(value) === -1) {
            visible = false;
          }
        });

        row.style.display = visible ? '' : 'none';
      });
    };

    filterInputs.forEach(input => {
      input.addEventListener('input', applyFilters);
    });
  }
});
</script>

  </body>
</html>
```

### altero tabla
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL modifica la estructura de una tabla existente llamada `inscripciones`. Específicamente, cambia el tipo y las restricciones del campo denominado `nombre`. El comando `MODIFY` dentro de la sentencia `ALTER TABLE` indica que estamos haciendo un cambio en la definición de una columna ya existente. En este caso, se establece que el campo `nombre` debe ser del tipo `VARCHAR(100)`, lo que significa que puede contener hasta 100 caracteres. Además, se añade la restricción `NOT NULL`, asegurando que en cada fila de la tabla no pueda haber un valor vacío para este campo, es decir, siempre deberá estar completo y con información. Esto ayuda a mantener la integridad de los datos almacenados en la base de datos.

`altero tabla.sql`

```sql
ALTER TABLE inscripciones
MODIFY nombre VARCHAR(100) NOT NULL;
```

### index
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código PHP crea una página web que permite a los usuarios insertar datos en una tabla llamada `inscripciones` de la base de datos `training_center`. El archivo comienza estableciendo una conexión con la base de datos y luego verifica si se ha enviado un formulario (mediante el método POST). Si es así, recupera información sobre las columnas de la tabla para determinar cómo procesar los valores enviados.

El código itera sobre cada columna de la tabla `inscripciones`, excluyendo aquellas que son claves primarias o tienen un valor predeterminado especial. Para cada campo, el código obtiene el valor enviado por el formulario y lo ajusta según el tipo de datos correspondiente (por ejemplo, convierte cadenas a enteros para campos numéricos). Los valores son luego preparados para una consulta SQL parametrizada que insertará los datos en la tabla.

Además, el script genera un formulario HTML basado en las columnas y sus tipos recuperados de la base de datos. Este formulario incluye etiquetas y elementos de entrada (como campos de texto, selectores desplegables, etc.) que corresponden a cada columna de la tabla `inscripciones`. También proporciona comentarios informativos para ayudar al usuario a entender los requisitos específicos de cada campo.

En resumen, este código combina lógica PHP para interactuar con una base de datos y generar consultas SQL seguras, junto con HTML dinámico para crear un formulario que facilita la inserción de nuevos registros en la tabla `inscripciones`. Esto proporciona una interfaz web completa y segura para manejar los datos.

`index.php`

```
<?php
// Conexión a la base de datos (una sola vez, al inicio del archivo)
$c = new mysqli("localhost","training_center","training_center","training_center");
if ($c->connect_error) {
  die("Error de conexión: " . $c->connect_error);
}

$mensaje = "";

// Procesar envío del formulario
if ($_SERVER['REQUEST_METHOD'] === 'POST') {

  // Recuperar metadatos de columnas de la tabla
  $meta = $c->query("
    SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_KEY, COLUMN_DEFAULT
    FROM information_schema.columns
    WHERE table_schema='training_center'
      AND table_name='inscripciones'
  ");

  $columnas      = [];
  $placeholders  = [];
  $valores       = [];
  $tiposBind     = "";

  while ($f = $meta->fetch_assoc()) {

    $campo     = $f['COLUMN_NAME'];
    $tipo      = $f['COLUMN_TYPE'];
    $colKey    = $f['COLUMN_KEY'];
    $colDef    = $f['COLUMN_DEFAULT'];

    // Misma exclusión que en el formulario
    if ($colKey == "PRI" || $colDef == "CURRENT_TIMESTAMP") {
      continue;
    }

    // Determinar el valor recibido según el tipo
    $valor = null;

    if (str_contains($tipo, "varchar")) {
      $valor = $_POST[$campo] ?? null;
      $tiposBind .= "s";
    }
    else if ($tipo == "date") {
      $valor = $_POST[$campo] ?? null;
      $tiposBind .= "s";
    }
    else if ($tipo == "int") {
      // Número entero
      $valor = isset($_POST[$campo]) && $_POST[$campo] !== "" ? (int)$_POST[$campo] : null;
      $tiposBind .= "i";
    }
    else if (str_contains($tipo, "decimal")) {
      // Número decimal
      $valor = isset($_POST[$campo]) && $_POST[$campo] !== "" ? (float)$_POST[$campo] : null;
      $tiposBind .= "d";
    }
    else if (str_contains($tipo, "tinyint")) {
      // Checkbox: si no viene en POST, se considera 0
      $valor = isset($_POST[$campo]) ? 1 : 0;
      $tiposBind .= "i";
    }
    else if (str_contains($tipo, "enum")) {
      // Enum: valor de la lista
      $valor = $_POST[$campo] ?? null;
      $tiposBind .= "s";
    }
    else if ($tipo == "text") {
      $valor = $_POST[$campo] ?? null;
      $tiposBind .= "s";
    }
    else if (str_contains($tipo, "blob")) {
      // Archivo subido: se guarda el contenido binario
      if (isset($_FILES[$campo]) && $_FILES[$campo]['error'] === UPLOAD_ERR_OK) {
        $valor = file_get_contents($_FILES[$campo]['tmp_name']);
      } else {
        $valor = null;
      }
      $tiposBind .= "s"; // Se envía como string; MySQL lo almacenará en el BLOB
    } else {
      // Cualquier otro tipo no contemplado explícitamente
      $valor = $_POST[$campo] ?? null;
      $tiposBind .= "s";
    }

    $columnas[]     = $campo;
    $placeholders[] = "?";
    $valores[]      = $valor;
  }

  if (!empty($columnas)) {

    $sql = "INSERT INTO inscripciones (" . implode(",", $columnas) . ")
            VALUES (" . implode(",", $placeholders) . ")";

    $stmt = $c->prepare($sql);

    if ($stmt) {
      // Construir array de parámetros por referencia para bind_param
      $params = [];
      $params[] = &$tiposBind;
      foreach ($valores as $k => $v) {
        $params[] = &$valores[$k];
      }

      // bind_param dinámico
      call_user_func_array([$stmt, 'bind_param'], $params);

      if ($stmt->execute()) {
        $mensaje = "Datos guardados correctamente.";
      } else {
        $mensaje = "Error al guardar los datos: " . $stmt->error;
      }

      $stmt->close();
    } else {
      $mensaje = "Error al preparar la consulta: " . $c->error;
    }
  } else {
    $mensaje = "No hay columnas que insertar (revisa la definición de la tabla).";
  }
}
?>
<!doctype html>
<html lang="es">
  <head>
    <title>Formulario</title>
    <meta charset="utf-8">

    <style>
      :root{
        --primary: crimson;
        --primary-light: #ff8fa0;
        --bg: #f2f2f2;
        --text: #333;
        --border: #ddd;
      }
      body, html{
        background: var(--bg);
        display: flex;
        justify-content: center;
        padding: 40px;
        font-family: "Segoe UI", sans-serif;
        color: var(--text);
      }
      form{
        background: white;
        padding: 30px 40px;
        width: 650px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-top: 8px solid var(--primary);
      }
      legend{
        font-size: 1.4em;
        font-weight: bold;
        color: var(--primary);
        margin-bottom: 10px;
      }
      form fieldset{
        display: flex;
        flex-direction: column;
        gap: 20px;
        border: none;
        padding: 0;
      }
      .control_formulario{
        display: flex;
        flex-direction: column;
        gap: 6px;
      }
      .control_formulario label{
        font-size: 0.95em;
        font-weight: 600;
        color: var(--primary);
      }
      form fieldset input:not([type="checkbox"]),
      form fieldset select,
      form fieldset textarea{
        padding: 12px 14px;
        border: 1px solid var(--border);
        border-radius: 6px;
        width: 100%;
        font-size: 1em;
        transition: border 0.3s, box-shadow 0.3s;
        box-sizing:border-box;
      }
      .control_formulario_checkbox{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
      }
      .control_formulario_checkbox input[type="checkbox"]{
        appearance: none;
        width: 52px;
        height: 28px;
        border-radius: 999px;
        background: #ccc;
        cursor: pointer;
        border: 1px solid #bbb;
        transition: background .25s;
        position: relative;
      }
      .control_formulario_checkbox input[type="checkbox"]::before{
        content: "";
        position: absolute;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: white;
        top: 50%;
        left: 3px;
        transform: translateY(-50%);
        transition: transform 0.25s;
      }
      .control_formulario_checkbox input[type="checkbox"]:checked{
        background: var(--primary);
        border-color: var(--primary);
      }
      .control_formulario_checkbox input[type="checkbox"]:checked::before{
        transform: translate(22px, -50%);
      }

      input[type="submit"]{
        background: var(--primary);
        color: white;
        padding: 14px;
        border: none;
        border-radius: 6px;
        font-size: 1.1em;
        cursor: pointer;
        margin-top: 10px;
      }

      .ayuda_campo{
        margin: 0;
        font-size: 0.8em;
        color: #777;
      }
    </style>

  </head>
  <body>
    <form action="" method="POST" enctype="multipart/form-data">
      <fieldset>
        <legend>Formulario de recogida de datos</legend>

        <?php if ($mensaje != ""): ?>
          <p style="padding:10px 12px; border-radius:6px;
                    background:#f8f8f8; border:1px solid #ddd;
                    font-size:0.9em; color:#444;">
            <?= htmlspecialchars($mensaje, ENT_QUOTES, 'UTF-8'); ?>
          </p>
        <?php endif; ?>

        <?php
          /* COMENTARIO DE LA TABLA */
          $tableComment = $c->query("
            SELECT TABLE_COMMENT
            FROM information_schema.tables
            WHERE table_schema='training_center'
              AND table_name='inscripciones'
          ")->fetch_assoc()['TABLE_COMMENT'];

          if ($tableComment != "") {
              echo "<p style='color:#555; margin-top:-5px; margin-bottom:20px;'>$tableComment</p>";
          }

          /* COLUMNAS CON SUS COMENTARIOS */
          $r = $c->query("
            SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_KEY, COLUMN_DEFAULT, COLUMN_COMMENT
            FROM information_schema.columns
            WHERE table_schema='training_center'
              AND table_name='inscripciones'
          ");

          while($f = $r->fetch_assoc()) {

            $campo = $f['COLUMN_NAME'];
            $tipo  = $f['COLUMN_TYPE'];
            $comentario = $f['COLUMN_COMMENT'];

            /* NO tocar esta lógica: respetar exclusiones */
            if($f['COLUMN_KEY'] == "PRI" || $f['COLUMN_DEFAULT'] == "CURRENT_TIMESTAMP") continue;

            echo '<div class="control_formulario">';

            // LABEL = nombre técnico de la columna
            echo '<label for="'.$campo.'">Introduce '.$campo.'</label>';

            // PÁRRAFO = comentario explicativo
            if ($comentario != "") {
              echo '<p class="ayuda_campo">'.$comentario.'</p>';
            }

            // Variables de ayuda según longitud/tipo
            $textoAyudaExtra = "";

            /* ---------- Mantener tus tipos de campo exactamente ---------- */

            if (str_contains($tipo, "varchar")) {
               // Extraer longitud: varchar(N)
               $maxlengthAttr = "";
               if (preg_match('/varchar\((\d+)\)/i', $tipo, $m)) {
                 $maxChars = (int)$m[1];
                 $maxlengthAttr = ' maxlength="'.$maxChars.'"';
                 $textoAyudaExtra = "Máximo {$maxChars} caracteres.";
               }
               echo '<input type="text" name="'.$campo.'" id="'.$campo.'"'.$maxlengthAttr.'>';
            }
            else if ($tipo == "date") {
               echo '<input type="date" name="'.$campo.'" id="'.$campo.'">';
            }
            else if ($tipo == "int") {
               // Entero simple (no se ha pedido longitud explícitamente)
               echo '<input type="number" name="'.$campo.'" id="'.$campo.'">';
            }
            else if (str_contains($tipo, "decimal")) {
               // decimal(p,s) → se calcula max y step
               $stepAttr = ' step="0.01"';
               $maxAttr  = "";
               if (preg_match('/decimal\((\d+),(\d+)\)/i', $tipo, $mDec)) {
                 $precision = (int)$mDec[1];
                 $scale     = (int)$mDec[2];
                 $enteros   = $precision - $scale;

                 // Valor máximo positivo aproximado: 99...9.99...9
                 if ($enteros > 0) {
                   $maxParteEntera = str_repeat('9', $enteros);
                 } else {
                   $maxParteEntera = "0";
                 }
                 $maxParteDecimal = $scale > 0 ? str_repeat('9', $scale) : "";
                 $maxValue = $maxParteEntera;
                 if ($scale > 0) {
                   $maxValue .= ".".$maxParteDecimal;
                 }

                 // step acorde con el número de decimales
                 if ($scale > 0) {
                   $stepAttr = ' step="0.'.str_repeat('0', $scale-1).'1"';
                 } else {
                   $stepAttr = ' step="1"';
                 }

                 $maxAttr = ' max="'.$maxValue.'"';
                 $textoAyudaExtra = "Hasta {$precision} dígitos en total, de los cuales {$scale} decimales. "
                                  . "Valor máximo aproximado: ±{$maxValue}.";
               }
               echo '<input type="number" name="'.$campo.'" id="'.$campo.'"'.$stepAttr.$maxAttr.'>';
            }
            else if (str_contains($tipo, "tinyint")) {
               // En tu lógica es un checkbox 0/1
               echo '<div class="control_formulario_checkbox">';
               echo '<label for="'.$campo.'">Introduce '.$campo.'</label>';
               echo '<input type="checkbox" name="'.$campo.'" id="'.$campo.'">';
               echo '</div>';

               // Información al usuario sobre el almacenamiento
               if (preg_match('/tinyint\((\d+)\)/i', $tipo, $mTi)) {
                 $anchoTiny = (int)$mTi[1];
                 $textoAyudaExtra = "Este campo se almacena como TINYINT({$anchoTiny}), normalmente 0 = no y 1 = sí.";
               } else {
                 $textoAyudaExtra = "Este campo se almacena internamente como TINYINT (0/1).";
               }
            }
            else if (str_contains($tipo, "enum")) {
               echo '<select name="'.$campo.'" id="'.$campo.'">';
               preg_match_all("/'([^']+)'/", $tipo, $matches);
               foreach($matches[1] as $valor){
                 echo '<option value="'.$valor.'">'.$valor.'</option>';
               }
               echo '</select>';
            }
            else if ($tipo == "text") {
               echo '<textarea name="'.$campo.'" id="'.$campo.'"></textarea>';
            }
            else if (str_contains($tipo, "blob")) {
               echo '<input type="file" name="'.$campo.'" id="'.$campo.'">';

               // Información de límites por tipo de BLOB
               $tipoLower = strtolower($tipo);
               if (str_contains($tipoLower, "tinyblob")) {
                 $textoAyudaExtra = "Tamaño máximo de archivo aproximado: 255 bytes (TINYBLOB).";
               } elseif (str_contains($tipoLower, "mediumblob")) {
                 $textoAyudaExtra = "Tamaño máximo de archivo aproximado: 16 MB (MEDIUMBLOB, 16.777.215 bytes).";
               } elseif (str_contains($tipoLower, "longblob")) {
                 $textoAyudaExtra = "Tamaño máximo de archivo aproximado: 4 GB (LONGBLOB, 4.294.967.295 bytes).";
               } else {
                 // BLOB "normal"
                 $textoAyudaExtra = "Tamaño máximo de archivo aproximado: 64 KB (BLOB, 65.535 bytes).";
               }
            }

            // Texto de ayuda adicional (longitudes, límites, etc.)
            if ($textoAyudaExtra !== "") {
              echo '<p class="ayuda_campo">'.$textoAyudaExtra.'</p>';
            }

            echo '</div>';
          }
        ?>

        <input type="submit">
      </fieldset>
    </form>
  </body>
</html>
```

### Actividades propuestas

El código que has proporcionado es un ejemplo completo de cómo crear, visualizar y actualizar registros en una base de datos MySQL desde PHP. Aquí está el análisis del conjunto de scripts:

1. **Base de Datos y Tabla:**
   - `database.sql` contiene la estructura y los datos iniciales para la tabla `inscripciones`.
   - La tabla tiene varias columnas, incluyendo campos de tipo texto, fecha, números enteros y decimales, enum, y blobs.

2. **Visualización del Contenido:**
   - `index.php` usa PDO para conectarse a la base de datos y seleccionar todos los registros en la tabla `inscripciones`.
   - Los datos se muestran en una tabla HTML con un formato ordenado.

3. **Creación de Registros (Formulario):**
   - `form_insert.php` proporciona un formulario que se alinea exactamente con el esquema de la base de datos.
   - El formulario utiliza PHP para conectarse a la base de datos y agregar nuevos registros basándose en los valores ingresados por el usuario.

4. **Actualización de Registros:**
   - `form_update.php` muestra un formulario similar al de inserción, pero inicialmente llena los campos con los valores actuales del registro que se está editando.
   - Al enviar el formulario actualizado, los datos se insertan en la base de datos para reemplazar el registro existente.

5. **CSS y Estilos:**
   - `style.css` proporciona un diseño básico para hacer que los formularios sean más atractivos y fáciles de usar.
   - Incluye estilos personalizados para campos de tipo fecha, número, texto largo, checkboxes y archivos.

6. **Validación y Ayuda al Usuario:**
   - Los comentarios en el código PHP describen las restricciones y características de cada campo.
   - Se proporciona información adicional al usuario sobre los tipos de datos (por ejemplo, longitud máxima para varchar, tamaño máximo para blobs).

7. **Seguridad:**
   - Se utilizan técnicas seguras como prepared statements para evitar inyecciones SQL.

### Recomendaciones Adicionales:
1. **Limpieza y Validación de Datos:**
   - Asegúrate de que los datos ingresados por el usuario sean válidos antes de insertarlos en la base de datos.
   - Utiliza funciones como `filter_var` para validar y limpiar entradas.

2. **Manejo de Errores:**
   - Implementa un manejo de errores robusto, especialmente cuando se conecta a la base de datos o ejecuta consultas.
   - Considera mostrar mensajes amigables al usuario en lugar de revelar detalles técnicos sobre el error.

3. **Ayuda y Documentación para Usuarios:**
   - Proporciona más ayuda contextual dentro del formulario si los usuarios necesitan entender mejor cómo llenarlo.
   - Por ejemplo, podrías añadir descripciones más detalladas a cada campo o crear un documento de referencia.

4. **Formateo y Presentación Visual:**
   - Mejora la presentación visual con CSS avanzado o frameworks como Bootstrap para una experiencia de usuario aún más amigable.
   
5. **Uso de Entorno de Desarrollo (IDE):**
   - Considera usar un IDE como PhpStorm, VSCode, etc., que proporcionará características adicionales como autocompletado y verificación de errores.

Este conjunto de scripts proporciona una base sólida para interactuar con la base de datos MySQL desde PHP. Con algunas mejoras en la seguridad y la presentación visual, este sistema puede ser utilizado en producción o como punto de partida para proyectos más grandes.


<a id="variables-del-sistema-y-variables-de-usuario"></a>
## Variables del sistema y variables de usuario

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/005-Programaci%C3%B3n%20de%20bases%20de%20datos/002-Variables%20del%20sistema%20y%20variables%20de%20usuario)


<a id="funciones"></a>
## Funciones

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/005-Programaci%C3%B3n%20de%20bases%20de%20datos/003-Funciones)


<a id="estructuras-de-control-de-flujo"></a>
## Estructuras de control de flujo

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/005-Programaci%C3%B3n%20de%20bases%20de%20datos/004-Estructuras%20de%20control%20de%20flujo)


<a id="procedimientos-almacenados-funciones-de-usuario"></a>
## Procedimientos almacenados. Funciones de usuario

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/005-Programaci%C3%B3n%20de%20bases%20de%20datos/005-Procedimientos%20almacenados.%20Funciones%20de%20usuario)


<a id="eventos-y-disparadores"></a>
## Eventos y disparadores

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/005-Programaci%C3%B3n%20de%20bases%20de%20datos/006-Eventos%20y%20disparadores)


<a id="excepciones"></a>
## Excepciones

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/005-Programaci%C3%B3n%20de%20bases%20de%20datos/007-Excepciones)


<a id="cursores"></a>
## Cursores

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/005-Programaci%C3%B3n%20de%20bases%20de%20datos/008-Cursores)



<a id="interpretacion-de-diagramas-entidadrelacion"></a>
# Interpretación de Diagramas EntidadRelación

<a id="el-modelo-er-entidades-y-relaciones-cardinalidades-debilidad"></a>
## El modelo ER. Entidades y relaciones. Cardinalidades. Debilidad

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/006-Interpretaci%C3%B3n%20de%20Diagramas%20EntidadRelaci%C3%B3n/001-El%20modelo%20ER.%20Entidades%20y%20relaciones.%20Cardinalidades.%20Debilidad)

### Introducción a los ejercicios

El diagrama de clases presentado describe una relación entre diferentes entidades en un sistema, probablemente para un modelo de comercio electrónico o similar que involucra productos, categorías y pedidos. A continuación se detalla cada clase y su relación con las demás:

1. **Cliente (Clase implícita)**
   - Relación: Tiene una asociación bidireccional con la entidad `Pedido` a través del atributo `cliente_id`.

2. **Producto**
   - Atributos:
     - `id`
     - `nombre`
     - `atributo`

3. **Categoria**
   - Atributos:
     - `id`
     - `nombre`

4. **LineasPedidos**
   - Atributos:
     - `id`
     - `fecha`
     - `pedido_id` (relación con la clase Pedido)
     - `producto_id` (relación con la clase Producto)
     - `cantidad`

5. **Pedido**
   - Relaciones:
     - Uno a muchos con `LineasPedidos` a través del atributo `pedido_id`.
     - Unidad de asociación bidireccional con el Cliente a través del atributo `cliente_id`.

6. **Entidad**
   - Atributos:
     - `id`
     - `producto_id` (relación con la clase Producto)
     - `categoria_id` (relación con la clase Categoria)

### Descripción de las relaciones:

1. **Relación entre Cliente y Pedido**:
   - Un cliente puede realizar múltiples pedidos.
   - Un pedido solo pertenece a un cliente.

2. **Relación entre Pedido y LineasPedidos**:
   - Un pedido contiene varias líneas de pedido.
   - Cada línea de pedido está asociada a un único pedido.

3. **Relación entre Producto y Entidad**:
   - Un producto puede estar relacionado con múltiples categorías mediante la tabla de entidades, permitiendo una relación muchos a muchos entre Productos y Categorías.

4. **Relación entre LineasPedidos y Producto**:
   - Una línea de pedido está asociada a un único producto.
   
5. **Relación entre Entidad y Categoria**:
   - Similarmente, la tabla `Entidad` permite que una categoría esté relacionada con múltiples productos.

### Diagrama en texto:

```plaintext
Cliente <-------------> Pedido (cliente_id)
          |                    |
          |--------------------|
                            LineasPedidos (pedido_id)
                             /  \            
                            /    \
                           /      \
                          /        \
                         /          \
                   Producto (producto_id) ----- Entidad (categoria_id)
```

El diagrama también muestra cómo los productos pueden estar relacionados con categorías a través de la tabla `Entidad`, que actúa como un puente para una relación muchos a muchos entre Productos y Categorías.

### Código JSON representativo del modelo:

```json
{
  "Cliente": {
    "attributes": ["id", "nombre"],
    "relationships": {
      "Pedido": { 
        "direction": "one-to-many",
        "foreign_key": "cliente_id"
      }
    }
  },
  "Producto": {
    "attributes": ["id", "nombre", "atributo"],
    "relationships": {
      "LineasPedidos": { 
        "direction": "many-to-one",
        "foreign_key": "producto_id"
      },
      "Entidad": { 
        "direction": "one-to-many",
        "foreign_key": "categoria_id"
      }
    }
  },
  "Categoria": {
    "attributes": ["id", "nombre"],
    "relationships": {
      "Entidad": { 
        "direction": "many-to-one",
        "foreign_key": "categoria_id"
      }
    }
  },
  "Pedido": {
    "attributes": ["id", "fecha"],
    "relationships": {
      "LineasPedidos": { 
        "direction": "one-to-many",
        "foreign_key": "pedido_id"
      }
    }
  },
  "LineasPedidos": {
    "attributes": ["id", "fecha", "cantidad"],
    "relationships": {
      "Producto": { 
        "direction": "many-to-one",
        "foreign_key": "producto_id"
      },
      "Pedido": { 
        "direction": "one-to-many",
        "foreign_key": "pedido_id"
      }
    }
  },
  "Entidad": {
    "attributes": ["id"],
    "relationships": {
      "Producto": { 
        "direction": "many-to-one",
        "foreign_key": "categoria_id"
      },
      "Categoria": { 
        "direction": "one-to-many",
        "foreign_key": "producto_id"
      }
    }
  }
}
```

Este modelo describe cómo las entidades se relacionan entre sí y proporciona una base sólida para la implementación de un sistema que gestiona pedidos, productos, categorías y relaciones entre ellos.

### entidad cliente
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código HTML se utiliza para representar visualmente una entidad en un diagrama de Entidad-Relación (ER) específico del cliente. La página está diseñada para mostrar cómo los datos relacionados con un cliente, como su identificador único (`id`), nombre, apellidos y correo electrónico, se organizan dentro de una base de datos.

El código HTML crea una estructura visual que incluye:
- Una caja blanca (`.shape entity`) que representa la entidad "Cliente".
- Un encabezado en la parte superior del contenedor que dice simplemente "Cliente" (`.entity-header`).
- Dentro del contenedor principal, hay varias propiedades del cliente listadas en una columna (`id`, `nombre`, `apellidos`, y `email`). Cada propiedad está representada por un elemento div con clase `.entity-property`.
- Los puertos a la izquierda y derecha de cada propiedad (`.port port-left` y `.port port-right`) sirven para conectar visualmente estas propiedades a otras entidades o relaciones en el diagrama ER.

Esta estructura es importante porque ayuda a los estudiantes de formación profesional a entender cómo se representan las tablas de una base de datos utilizando la notación ER, permitiéndoles ver gráficamente las columnas (o atributos) de cada entidad.

`004-entidad cliente.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 299.9999999999999px;
  height: 230.39998834783373px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:40px;top:40px;width:219.9999999999999px;height:150.39998834783373px;">
  <div class="entity-header">Cliente</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">email</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
</div>
</body>
</html>
```

### entidad cliente
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es una representación JSON que describe una entidad en un diagrama ER (Diagrama Entidad Relación). En específico, el código representa la entidad llamada "Cliente" con sus propiedades asociadas. La estructura del JSON incluye un array llamado `formas` donde cada elemento detalla las características de una forma específica en el diagrama.

En este caso, hay solo una forma (entidad) definida dentro del array `formas`, la cual tiene atributos como `id`, `tipo`, `left`, `top`, que describen su posición y tipo. El campo `entityName` especifica que esta entidad se llama "Cliente". Además, el objeto incluye un array llamado `properties` donde cada elemento representa una propiedad de la entidad "Cliente", proporcionando tanto un identificador único como el nombre de cada propiedad.

Este formato JSON es útil porque permite almacenar y manipular la estructura del diagrama ER en forma de datos descriptivos. Esto facilita su procesamiento por parte de herramientas o aplicaciones que pueden renderizar estos datos en una interfaz gráfica, ayudando a los estudiantes a entender mejor las relaciones entre diferentes entidades en un sistema de gestión de bases de datos.

**ÚLTIMO PÁRRAFO:**
En comparación con el archivo anterior (004-entidad cliente.html), este archivo JSON proporciona una representación más estructurada y simplificada del diagrama ER, eliminando la necesidad de código HTML para visualizar las entidades. Esto hace que sea más fácil procesar y manipular los datos del diagrama utilizando herramientas de programación o aplicaciones específicas.

`004-entidad cliente.json`

```json
{
  "formas": [
    {
      "id": "forma-1",
      "tipo": "entity",
      "left": "364.361px",
      "top": "116.556px",
      "width": "",
      "height": "",
      "entityName": "Cliente",
      "properties": [
        {
          "id": "prop-1",
          "name": "id"
        },
        {
          "id": "prop-2",
          "name": "nombre"
        },
        {
          "id": "prop-3",
          "name": "apellidos"
        },
        {
          "id": "prop-4",
          "name": "email"
        }
      ]
    }
  ],
  "flechas": []
}
```

### entidad cliente
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es un archivo SVG (Scalable Vector Graphics) que representa visualmente una entidad llamada "Cliente". El SVG contiene elementos gráficos que describen la estructura y los atributos de esta entidad en el modelo Entity-Relationship (ER). En este caso, se dibuja un rectángulo con bordes gruesos que actúa como la representación visual de la entidad "Cliente", con las propiedades id, nombre, apellidos y email anotadas dentro del rectángulo. Cada propiedad está alineada verticalmente en el interior del cuadro rectangular para facilitar su lectura.

El archivo SVG utiliza varios elementos y estilos CSS para definir cómo se debe representar la entidad "Cliente". Incluye una etiqueta `<rect>` que dibuja un rectángulo blanco con bordes negros gruesos, que representa visualmente a la entidad. Además, hay líneas de texto dentro del rectángulo que describen las propiedades de la entidad: id, nombre, apellidos y email.

El último párrafo para resumir las diferencias respecto al archivo anterior es:
Este nuevo archivo SVG proporciona una representación visual más detallada y gráfica de la entidad "Cliente" en lugar del formato JSON. Muestra directamente el rectángulo que representa a la entidad, sus bordes, y las propiedades anotadas dentro del rectángulo, facilitando así su interpretación visual y entendimiento de la estructura ER.

`004-entidad cliente.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="299.9999999999999" height="230.39998834783373" viewBox="0 0 299.9999999999999 230.39998834783373">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="40" y="40" width="219.9999999999999" height="150.39998834783373" />
<line x1="40" y1="66.40000169927423" x2="259.9999999999999" y2="66.40000169927423" stroke="#e5e7eb" stroke-width="1"/>
<text x="149.99999999999994" y="57.999999653209336" text-anchor="middle">Cliente</text>
<text x="123.89999944513488" y="86.40000334652987">id</text>
<text x="123.89999944513488" y="110.39999519694933">nombre</text>
<text x="123.89999944513488" y="134.3999870473688">apellidos</text>
<text x="123.89999944513488" y="158.39998843453142">email</text>
</svg>
```

### dos entidades
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código HTML crea una representación visual simple de un diagrama entidad-relación (ER) para dos entidades: "Cliente" y "Pedido". El diseño utiliza CSS para estilizar estas entidades con formas rectangulares que contienen los nombres y atributos de cada entidad.

En la parte del cuerpo (`<body>`), se define una caja principal (`<div class="page">`) que contiene dos bloques de div, representando las entidades "Cliente" y "Pedido". Cada bloque tiene un encabezado con el nombre de la entidad ("Cliente" o "Pedido") y una lista de atributos asociados a esa entidad. Por ejemplo, para la entidad "Cliente", los atributos son: id, nombre, apellidos y email.

El CSS define estilos específicos que hacen que las entidades se vean como rectángulos con bordes redondeados y proporciona un diseño limpio para mostrar el contenido de cada entidad y sus atributos. También incluye pequeños círculos en los lados izquierdo y derecho de cada atributo, representando posibles puntos de conexión o relaciones con otras entidades.

Este tipo de diagramas son útiles para estudiantes de bases de datos porque permiten visualizar claramente cómo se estructura la información, identificando las entidades clave y sus atributos en un sistema de gestión de bases de datos.

`005-dos entidades.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 577.8750055486505px;
  height: 230.83748557350842px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:40px;top:40px;width:219.99995838512064px;height:150.39998834783373px;">
  <div class="entity-header">Cliente</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">email</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:317.87496393377126px;top:40.43749722567472px;width:220.00004161487917px;height:150.39998834783373px;">
  <div class="entity-header">Pedido</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">fecha</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">numero_pedido</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id_cliente</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
</div>
</body>
</html>
```

### dos entidades
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es una representación en formato JSON de dos entidades, "Cliente" y "Pedido", que podrían estar involucradas en un diagrama ER (Entidad Relacional). En esta estructura, cada entidad tiene un nombre y una lista de propiedades. Por ejemplo, la entidad "Cliente" contiene las propiedades "id", "nombre", "apellidos" y "email". De manera similar, la entidad "Pedido" incluye "id", "fecha", "numero_pedido" y "id_cliente".

Este formato JSON proporciona un enfoque estructurado para almacenar información sobre entidades y sus relaciones en un modelo de datos relacional. La ausencia de ancho y alto explícitos indica que estas dimensiones pueden ser determinadas automáticamente o configuradas dinámicamente por la aplicación que maneja estos datos.

En comparación con el código HTML anterior, este archivo JSON ofrece una representación más abstracta y estructurada de las entidades. A diferencia del formato visual en HTML, donde se especifican coordenadas exactas y detalles visuales, este JSON proporciona solo los nombres de las entidades y sus propiedades sin preocuparse por la disposición gráfica o el estilo. Esta simplificación facilita el manejo y la manipulación de datos estructurados, especialmente en contextos donde se necesita intercambiar información entre diferentes sistemas o herramientas de modelado.

En resumen, este archivo JSON es una versión más abstracta del modelo ER que elimina los detalles visuales y gráficos presentes en el HTML previo, enfocándose exclusivamente en la estructura de datos.

`005-dos entidades.json`

```json
{
  "formas": [
    {
      "id": "forma-1",
      "tipo": "entity",
      "left": "189.783px",
      "top": "136.975px",
      "width": "",
      "height": "",
      "entityName": "Cliente",
      "properties": [
        {
          "id": "prop-1",
          "name": "id"
        },
        {
          "id": "prop-2",
          "name": "nombre"
        },
        {
          "id": "prop-3",
          "name": "apellidos"
        },
        {
          "id": "prop-4",
          "name": "email"
        }
      ]
    },
    {
      "id": "forma-2",
      "tipo": "entity",
      "left": "467.655px",
      "top": "137.419px",
      "width": "",
      "height": "",
      "entityName": "Pedido",
      "properties": [
        {
          "id": "prop-5",
          "name": "id"
        },
        {
          "id": "prop-6",
          "name": "fecha"
        },
        {
          "id": "prop-7",
          "name": "numero_pedido"
        },
        {
          "id": "prop-8",
          "name": "id_cliente"
        }
      ]
    }
  ],
  "flechas": []
}
```

### dos entidades
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

El archivo actual es una representación gráfica de dos entidades, "Cliente" y "Pedido", en un diagrama ER (Entidad Relacional) utilizando SVG (Scalable Vector Graphics). En este diagrama, cada entidad se representa mediante un rectángulo con sus atributos internos enlistados debajo. Los rectángulos para las entidades "Cliente" e "Pedido" están colocados a ambos lados del espacio de dibujo proporcionado y contienen los respectivos atributos: "id", "nombre", "apellidos", "email" para la entidad "Cliente"; y "id", "fecha", "numero_pedido", "id_cliente" para la entidad "Pedido". No se han incluido relaciones explícitas entre las entidades en este fragmento, pero el diseño proporciona un marco visual claro de cómo estas dos entidades pueden interconectarse.

En relación con el archivo anterior (005-dos entidades.json), este nuevo código pasa de una representación en formato JSON a una imagen vectorial SVG. Esto significa que ahora se tiene una visualización gráfica directa de las entidades y sus atributos, lo cual es más intuitivo para entender la estructura del modelo ER. Las diferencias clave incluyen el cambio del formato de datos a un formato de dibujo, permitiendo ver las entidades como rectángulos con atributos específicamente posicionados dentro de ellos, en lugar de una lista anidada de propiedades y valores. Esto facilita la interpretación visual y la comunicación gráfica de los conceptos ER.

`005-dos entidades.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="577.8750055486505" height="230.83748557350842" viewBox="0 0 577.8750055486505 230.83748557350842">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="40" y="40" width="219.99995838512064" height="150.39998834783373" />
<line x1="40" y1="66.39999736439097" x2="259.99995838512064" y2="66.39999736439097" stroke="#e5e7eb" stroke-width="1"/>
<text x="149.99997919256032" y="58.00000312111594" text-anchor="middle">Cliente</text>
<text x="123.89999944513494" y="86.39999250932172">id</text>
<text x="123.89999944513494" y="110.39999389648435">nombre</text>
<text x="123.89999944513494" y="134.4000022194602">apellidos</text>
<text x="123.89999944513494" y="158.3999966708096">email</text>
<rect class="shape-entity" x="317.87496393377126" y="40.43749722567472" width="220.00004161487917" height="150.39998834783373" />
<line x1="317.87496393377126" y1="66.83749459006569" x2="537.8750055486504" y2="66.83749459006569" stroke="#e5e7eb" stroke-width="1"/>
<text x="427.8749847412108" y="58.43750034679066" text-anchor="middle">Pedido</text>
<text x="382.1374983354047" y="86.83749667080966">id</text>
<text x="382.1374983354047" y="110.83749112215907">fecha</text>
<text x="382.1374983354047" y="134.8374994451349">numero_pedido</text>
<text x="382.1374983354047" y="158.83749389648432">id_cliente</text>
</svg>
```

### correspondencia 1 a n
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código HTML representa una página web que muestra un diagrama sencillo en el contexto del modelo entidad-relación (ER) utilizado en bases de datos. El diseño incluye dos entidades principales: "Cliente" y "Pedido". Cada entidad se dibuja como un rectángulo con propiedades específicas, donde las propiedades del Cliente son 'id', 'nombre', 'apellidos' y 'email'. Por su parte, la entidad Pedido tiene propiedades como 'id', 'fecha', 'numero_pedido' y 'id_cliente'.

Además, hay una flecha que conecta ambas entidades, indicando una relación entre ellas. Esta representación gráfica ayuda a visualizar cómo las dos tablas (o entidades) en una base de datos están relacionadas: es posible que un cliente tenga muchos pedidos, lo que se refleja en la relación 1 a N (uno a varios) entre Cliente y Pedido.

La importancia del código radica en su capacidad para proporcionar una representación visual clara y fácilmente comprensible de relaciones complejas en bases de datos, facilitando así el entendimiento de las estructuras de datos a los estudiantes.

`007-correspondencia 1 a n.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 577.8750101725259px;
  height: 230.83750406901032px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:40px;top:40px;width:219.99998304578983px;height:150.40000067816834px;">
  <div class="entity-header">Cliente</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">email</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:317.87501017252595px;top:40.43750339084201px;width:219.99999999999991px;height:150.40000067816834px;">
  <div class="entity-header">Pedido</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">fecha</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">numero_pedido</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id_cliente</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="arrow" style="left:198.08750788370764px;top:84.30569400224206px;width:175.98220725317339px;transform:rotate(0.40058871203078056rad);"></div>
</div>
</body>
</html>
```

### correspondencia 1 a n
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código JSON describe la estructura y las relaciones entre dos entidades en un modelo ER (Entidad Relación): Cliente y Pedido. Cada entidad tiene sus propias características y atributos, que se representan mediante una lista de objetos que contienen el nombre de los atributos. Además, existe una relación entre estas dos entidades, específicamente desde la propiedad "id" de la entidad Cliente hasta la propiedad "id_cliente" de la entidad Pedido. Esta relación es de tipo simple (un enlace directo) y se dibuja como una línea recta ("straight").

Este archivo JSON proporciona un formato estructurado que puede ser utilizado para automatizar el procesamiento o renderizado del diagrama ER, facilitando así la creación de representaciones gráficas basadas en datos. En comparación con el código HTML anterior, este JSON ofrece una representación más abstracta y flexible de los mismos elementos (entidades y relaciones), permitiendo un mejor manejo y manipulación por parte de herramientas o lenguajes que trabajen con estructuras de datos.

ÚLTIMO PÁRRAFO: Este nuevo archivo JSON representa la misma información que el HTML anterior pero en un formato más estructurado, lo cual facilita su procesamiento automático. Además, introduce una descripción explícita de las relaciones entre entidades, eliminando la necesidad de CSS y HTML para representar gráficamente los datos ER.

`007-correspondencia 1 a n.json`

```json
{
  "formas": [
    {
      "id": "forma-1",
      "tipo": "entity",
      "left": "189.783px",
      "top": "136.975px",
      "width": "",
      "height": "",
      "entityName": "Cliente",
      "properties": [
        {
          "id": "prop-1",
          "name": "id"
        },
        {
          "id": "prop-2",
          "name": "nombre"
        },
        {
          "id": "prop-3",
          "name": "apellidos"
        },
        {
          "id": "prop-4",
          "name": "email"
        }
      ]
    },
    {
      "id": "forma-2",
      "tipo": "entity",
      "left": "467.655px",
      "top": "137.419px",
      "width": "",
      "height": "",
      "entityName": "Pedido",
      "properties": [
        {
          "id": "prop-5",
          "name": "id"
        },
        {
          "id": "prop-6",
          "name": "fecha"
        },
        {
          "id": "prop-7",
          "name": "numero_pedido"
        },
        {
          "id": "prop-8",
          "name": "id_cliente"
        }
      ]
    }
  ],
  "flechas": [
    {
      "desde": {
        "shapeId": "forma-1",
        "propId": "prop-1",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-2",
        "propId": "prop-8",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    }
  ]
}
```

### correspondencia 1 a n
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SVG representa un diagrama entidad-relación (ER) que ilustra la relación entre dos entidades: "Cliente" y "Pedido". El código define el diseño gráfico con rectángulos para cada entidad, líneas horizontales dentro de los rectángulos para listar las propiedades (atributos) de cada entidad, y una línea punteada con una flecha que indica la relación entre estas dos entidades.

El rectángulo izquierdo representa a la entidad "Cliente" y contiene cuatro atributos: id, nombre, apellidos y email. El rectángulo derecho representa a la entidad "Pedido", que también tiene cuatro atributos: id, fecha, número_pedido e id_cliente (que actúa como una clave foránea enlazada con el cliente).

La línea que conecta los dos rectángulos incluye una flecha apuntando hacia el rectángulo de "Pedido", indicando la relación 1:N entre Cliente y Pedido. Esto sugiere que un solo cliente puede realizar múltiples pedidos, pero cada pedido está asociado a uno y sólo a un cliente.

El archivo actual es una representación gráfica visual del modelo ER descrito en el formato JSON anterior. En lugar de definir entidades y sus propiedades con texto estructurado, utiliza elementos SVG para dibujar rectángulos y textos que detallan las mismas características: nombres de entidades y sus respectivos atributos.

ÚLTIMO PÁRRAFO:
El archivo actual presenta una versión visual del modelo ER anterior en formato JSON, utilizando etiquetas SVG para crear un diagrama gráfico. Esto permite a los usuarios ver directamente la relación entre "Cliente" y "Pedido", incluyendo cómo las entidades están conectadas mediante líneas y flechas, facilitando así la comprensión de la estructura del modelo de datos.

`007-correspondencia 1 a n.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="577.8750101725259" height="230.83750406901032" viewBox="0 0 577.8750101725259 230.83750406901032">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="40" y="40" width="219.99998304578983" height="150.40000067816834" />
<line x1="40" y1="66.4000023735894" x2="259.9999830457898" y2="66.4000023735894" stroke="#e5e7eb" stroke-width="1"/>
<text x="149.9999915228949" y="57.99999830457899" text-anchor="middle">Cliente</text>
<text x="123.90000406901038" y="86.40000406901041">id</text>
<text x="123.90000406901038" y="110.40000237358939">nombre</text>
<text x="123.90000406901038" y="134.4000091552734">apellidos</text>
<text x="123.90000406901038" y="158.39999898274735">email</text>
<rect class="shape-entity" x="317.87501017252595" y="40.43750339084201" width="219.99999999999991" height="150.40000067816834" />
<line x1="317.87501017252595" y1="66.83749728732637" x2="537.8750101725259" y2="66.83749728732637" stroke="#e5e7eb" stroke-width="1"/>
<text x="427.8750101725259" y="58.43749321831596" text-anchor="middle">Pedido</text>
<text x="382.13746134440095" y="86.83749898274738">id</text>
<text x="382.13746134440095" y="110.8375057644314">fecha</text>
<text x="382.13746134440095" y="134.83749559190534">numero_pedido</text>
<text x="382.13746134440095" y="158.83750237358936">id_cliente</text>
<path class="conn" d="M 198.08750788370764 84.30569400224206 L 360.13748168945307 152.9318060825289" marker-end="url(#arrow-end)" />
</svg>
```

### caso centro de formacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código HTML crea una página web que representa un diagrama de entidades relacionales (ER) para un centro de formación. La página incluye estilos CSS detallados que definen cómo se visualizan diferentes elementos del diagrama.

En el cuerpo de la página, hay tres divs principales que representan entidades en el modelo ER: "Asignatura", "Alumno" y "Matricula". Cada entidad tiene un encabezado con su nombre y una lista de propiedades (campos) como identificadores únicos (`id`), nombres, descripciones, fechas y referencias a otras entidades.

Además, hay dos flechas que representan las relaciones entre estas entidades. Una flecha conecta la entidad "Asignatura" con la entidad "Matricula", indicando que una asignatura puede tener varias matrículas. La otra flecha conecta la entidad "Alumno" con la entidad "Matricula", sugiriendo que un alumno puede estar inscrito en múltiples asignaturas a través de sus matrículas.

Este diagrama es útil para estudiantes y profesionales de bases de datos porque ayuda a visualizar cómo se estructuran los datos en una base de datos relacional, mostrando las entidades (tablas), sus atributos (columnas) y las relaciones entre ellas.

`008-caso centro de formacion.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 580.6249999999998px;
  height: 378.11251163482655px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:40.037479400634766px;top:211.71251773834223px;width:219.99999999999991px;height:126.39999389648433px;">
  <div class="entity-header">Asignatura</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">descripcion</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:40px;top:40px;width:219.9999809265136px;height:150.39999961853022px;">
  <div class="entity-header">Alumno</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">email</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:320.62499999999994px;top:105.6249952316284px;width:219.99999999999991px;height:150.40000915527338px;">
  <div class="entity-header">Matricula</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">fecha</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">alumno_id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">asignatura_id</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="arrow" style="left:204.9874728918075px;top:253.22922123171003px;width:167.8045839845535px;transform:rotate(-0.19382181144901595rad);"></div>
<div class="arrow" style="left:198.08748662471766px;top:85.23177119693266px;width:202.70510001760024px;transform:rotate(0.5616737052975951rad);"></div>
</div>
</body>
</html>
```

### caso centro de formacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código JSON describe un diagrama de entidad-relación (ER) para un sistema escolar que incluye entidades, sus propiedades y las relaciones entre ellas. El archivo contiene tres principales objetos JSON: dos representan entidades ("Asignatura", "Alumno" y "Matricula") y uno representa las flechas o líneas que conectan estas entidades.

Cada entidad tiene un ID único, coordenadas de posición en el diagrama (izquierda y arriba), un nombre y una lista de propiedades. Por ejemplo, la entidad 'Asignatura' tiene tres propiedades: 'id', 'nombre' y 'descripcion'. De manera similar, las otras entidades también tienen sus respectivas propiedades.

Las flechas conectan estas entidades basándose en propiedades específicas, lo que indica una relación entre ellas. Por ejemplo, la primera flecha conecta desde el ID de "Asignatura" hasta el "asignatura_id" de "Matricula", indicando que cada matrícula está asociada a una asignatura específica.

En resumen, este JSON codifica visualmente cómo las entidades y sus propiedades están interconectadas en un sistema escolar mediante relaciones simples y directas.

El código JSON actual representa los mismos datos del diagrama de entidad-relación pero con una estructura diferente, utilizando objetos JSON para definir las formas (entidades) y las flechas que conectan estas entidades. Esto facilita la manipulación y visualización programática del diagrama ER en comparación con el código HTML anterior.

Este cambio permite una mayor flexibilidad y potencialmente simplifica la gestión del diagrama ER, especialmente si se necesita hacer cambios o añadir más detalles a las relaciones entre las entidades.

`008-caso centro de formacion.json`

```json
{
  "formas": [
    {
      "id": "forma-1",
      "tipo": "entity",
      "left": "216.375px",
      "top": "268.825px",
      "width": "",
      "height": "",
      "entityName": "Asignatura",
      "properties": [
        {
          "id": "prop-1",
          "name": "id"
        },
        {
          "id": "prop-2",
          "name": "nombre"
        },
        {
          "id": "prop-3",
          "name": "descripcion"
        }
      ]
    },
    {
      "id": "forma-2",
      "tipo": "entity",
      "left": "216.338px",
      "top": "97.1125px",
      "width": "",
      "height": "",
      "entityName": "Alumno",
      "properties": [
        {
          "id": "prop-4",
          "name": "id"
        },
        {
          "id": "prop-5",
          "name": "nombre"
        },
        {
          "id": "prop-6",
          "name": "apellidos"
        },
        {
          "id": "prop-7",
          "name": "email"
        }
      ]
    },
    {
      "id": "forma-3",
      "tipo": "entity",
      "left": "496.963px",
      "top": "162.738px",
      "width": "",
      "height": "",
      "entityName": "Matricula",
      "properties": [
        {
          "id": "prop-8",
          "name": "id"
        },
        {
          "id": "prop-9",
          "name": "fecha"
        },
        {
          "id": "prop-10",
          "name": "alumno_id"
        },
        {
          "id": "prop-11",
          "name": "asignatura_id"
        }
      ]
    }
  ],
  "flechas": [
    {
      "desde": {
        "shapeId": "forma-1",
        "propId": "prop-1",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-3",
        "propId": "prop-11",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-2",
        "propId": "prop-4",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-3",
        "propId": "prop-10",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    }
  ]
}
```

### caso centro de formacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SVG representa un diagrama de entidad-relación (ER) que ilustra las relaciones entre tres entidades: Asignatura, Alumno y Matricula. Cada entidad se muestra como un rectángulo con sus propiedades internas listadas debajo. Las relaciones entre estas entidades se representan mediante líneas con flechas, indicando la dirección de los enlaces.

La entidad "Asignatura" tiene las propiedades: id, nombre y descripción. La entidad "Alumno" incluye las propiedades: id, nombre, apellidos y email. Finalmente, la entidad "Matricula" contiene las propiedades: id, fecha, alumno_id (relacionada con Alumno) y asignatura_id (relacionada con Asignatura).

Este diagrama ER es importante porque proporciona una representación visual clara de cómo se relacionan diferentes elementos en un sistema de gestión de datos, ayudando a diseñar bases de datos eficientes y bien estructuradas.

**ÚLTIMO PÁRRAFO**: La versión actual del archivo utiliza SVG para dibujar el diagrama directamente, proporcionando una visualización gráfica más detallada con estilos específicos para cada elemento (rectángulos para entidades, líneas de conexión con flechas). Esto es un avance significativo en comparación con la estructura JSON anterior, ya que permite una mayor interactividad y claridad visual.

`008-caso centro de formacion.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="580.6249999999998" height="378.11251163482655" viewBox="0 0 580.6249999999998 378.11251163482655">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="40.037479400634766" y="211.71251773834223" width="219.99999999999991" height="126.39999389648433" />
<line x1="40.037479400634766" y1="238.11250448226923" x2="260.03747940063465" y2="238.11250448226923" stroke="#e5e7eb" stroke-width="1"/>
<text x="150.0374794006347" y="229.71251034736628" text-anchor="middle">Asignatura</text>
<text x="117.07498931884766" y="258.11249637603754">id</text>
<text x="117.07498931884766" y="282.1125116348266">nombre</text>
<text x="117.07498931884766" y="306.11250782012934">descripcion</text>
<rect class="shape-entity" x="40" y="40" width="219.9999809265136" height="150.39999961853022" />
<line x1="40" y1="66.39999628067017" x2="259.99998092651356" y2="66.39999628067017" stroke="#e5e7eb" stroke-width="1"/>
<text x="149.99999046325678" y="57.99999499320984" text-anchor="middle">Alumno</text>
<text x="123.89997863769531" y="86.39999294281004">id</text>
<text x="123.89997863769531" y="110.39998912811278">nombre</text>
<text x="123.89997863769531" y="134.39999485015863">apellidos</text>
<text x="123.89997863769531" y="158.39999103546137">email</text>
<rect class="shape-entity" x="320.62499999999994" y="105.6249952316284" width="219.99999999999991" height="150.40000915527338" />
<line x1="320.62499999999994" y1="132.02499151229856" x2="540.6249999999999" y2="132.02499151229856" stroke="#e5e7eb" stroke-width="1"/>
<text x="430.6249999999999" y="123.62499737739562" text-anchor="middle">Matricula</text>
<text x="391.64995574951166" y="152.02500247955317">id</text>
<text x="391.64995574951166" y="176.0249986648559">fecha</text>
<text x="391.64995574951166" y="200.0250031948089">alumno_id</text>
<text x="391.64995574951166" y="224.0250101089477">asignatura_id</text>
<path class="conn" d="M 204.9874728918075 253.22922123171003 L 369.6499633789062 220.90828942560034" marker-end="url(#arrow-end)" />
<path class="conn" d="M 198.08748662471766 85.23177119693266 L 369.6499633789062 193.19321868219862" marker-end="url(#arrow-end)" />
</svg>
```

### caso tienda online
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código HTML representa una página web que visualiza un diagrama entidad-relación (ER) para un caso de estudio de una tienda online. La estructura del código incluye varias entidades y relaciones entre ellas, presentadas mediante cajas con encabezados y propiedades específicas.

La página contiene cuatro entidades principales: Cliente, Producto, Pedido, y LineasPedido. Cada entidad se muestra en un rectángulo con detalles de las propiedades que la componen (como ID, nombre, precio, etc.), y los nombres de las entidades aparecen en encabezados dentro de estos rectángulos.

Además, el código incluye líneas (flechas) que representan relaciones entre estas entidades. Por ejemplo, hay una flecha que conecta la entidad Cliente con la entidad Pedido, indicando que un cliente puede realizar varios pedidos.

El estilo del diagrama es cuidado y estético, lo que facilita su lectura y comprensión. El uso de CSS proporciona una visualización detallada que incluye bordes redondeados, sombreado y colores para destacar las diferentes partes del diagrama, como encabezados y propiedades.

Este tipo de representación es útil en cursos de bases de datos y gestión de información para enseñar cómo modelar relaciones entre entidades en un sistema informático.

`009-caso tienda online.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 817.0249837239581px;
  height: 364.4375101725259px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:40px;top:40.01250203450519px;width:219.99999999999994px;height:126.40000406901038px;">
  <div class="entity-header">Cliente</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:294.3500162760416px;top:198.03750610351554px;width:219.99999999999994px;height:126.40000406901038px;">
  <div class="entity-header">Producto</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">precio</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:289.68749999999994px;top:40px;width:219.99999999999994px;height:126.40000406901038px;">
  <div class="entity-header">Pedido</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">fecha</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">cliente_id</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:557.0249837239581px;top:98.687510172526px;width:219.99999999999994px;height:174.40000406901038px;">
  <div class="entity-header">LineasPedido</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">fecha</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">pedido_id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">producto_id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">cantidad</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="arrow" style="left:198.08752441406247px;top:83.75626538824127px;width:158.31921494545765px;transform:rotate(0.2901860677521058rad);"></div>
<div class="arrow" style="left:449.5749918619791px;top:85.2301196227952px;width:189.76540990434972px;transform:rotate(0.5614093340038653rad);"></div>
<div class="arrow" style="left:449.0624999999999px;top:239.71417731907204px;width:163.21856764761617px;transform:rotate(-0.15937732576534783rad);"></div>
</div>
</body>
</html>
```

### caso tienda online
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

### Explicación del Código JSON

El código proporcionado representa una estructura de diagrama de entidad-relación (ER) para un sistema que gestiona clientes, pedidos y líneas de pedido. El formato es en JSON y describe tanto las entidades como sus relaciones.

#### Estructura General

- **formas**: Una lista de objetos que describen las entidades del modelo.
  - Cada objeto tiene los siguientes campos:
    - `id`: Un identificador único para la forma (en este caso, una entidad).
    - `tipo`: Especifica el tipo de forma. En este caso, todas son "entity".
    - `left` y `top`: Posiciones absolutas en píxeles.
    - `width` y `height`: No se especifican aquí, lo que permite al sistema ajustar automáticamente sus dimensiones basándose en los datos proporcionados.
    - `entityName`: El nombre de la entidad (por ejemplo, "Cliente").
    - `properties`: Una lista de propiedades de la entidad. Cada propiedad tiene un identificador único (`id`) y un nombre (`name`).

- **flechas**: Una lista de objetos que describen las relaciones entre entidades.
  - Cada objeto tiene los siguientes campos:
    - `desde`: Un objeto con `shapeId`, el identificador de la entidad desde donde comienza la relación, y `propId`, el identificador de la propiedad específica en esa entidad. También incluye un campo `side` que indica si se conecta por la parte izquierda ("left") o derecha ("right").
    - `hasta`: Un objeto similar a `desde` pero para la entidad final de la relación.
    - `tipo`: El tipo de flecha, en este caso "simple".
    - `estilo`: La forma en que se dibuja la flecha, en este caso "straight" (recta).

### Descripción Detallada del Código JSON

#### Entidades

1. **Cliente**
   - Posición: 34px (izquierda), 135.625px (arriba)
   - Propiedades:
     - `id`
     - `nombre`
     - `apellidos`

2. **Producto**
   - Posición: 288.433px (izquierda), 293.654px (arriba)
   - Propiedades:
     - `id`
     - `nombre`
     - `precio`

3. **Pedido**
   - Posición: 283.771px (izquierda), 135.621px (arriba)
   - Propiedades:
     - `id`
     - `fecha`
     - `cliente_id`

4. **LineasPedido**
   - Posición: 551.104px (izquierda), 194.308px (arriba)
   - Propiedades:
     - `id`
     - `fecha`
     - `pedido_id`
     - `producto_id`
     - `cantidad`

#### Relaciones

- **Relación entre Cliente y Pedido**:
  - La propiedad `cliente_id` del `Pedido` está relacionada con el `id` del `Cliente`.

- **Relación entre Pedido y LineasPedido**:
  - La propiedad `pedido_id` de la entidad `LineasPedido` está conectada a la propiedad `id` de la entidad `Pedido`.

- **Relación entre Producto y LineasPedido**:
  - La propiedad `producto_id` de la entidad `LineasPedido` se vincula con el `id` del `Producto`.

### Diferencias Con Exposición Anterior HTML

Comparado con el código anterior en formato HTML:

1. **Representación de entidades**: Ahora las entidades son objetos JSON descriptivos en lugar de bloques de HTML.
2. **Relaciones**: Las relaciones se especifican como objetos JSON que describen desde y hasta, y no como elementos `<div>` con estilos de transformación.
3. **Estilo y posición automático**: No hay necesidad de especificar dimensiones explícitas ni usar estilos CSS para posicionar las entidades; la herramienta generará esto automáticamente basándose en los datos proporcionados.

En resumen, el código JSON facilita un enfoque más dinámico y descriptivo para representar diagramas ER, eliminando la necesidad de codificar manualmente cada detalle visual.

`009-caso tienda online.json`

```json
{
  "formas": [
    {
      "id": "forma-1",
      "tipo": "entity",
      "left": "34.0792px",
      "top": "135.625px",
      "width": "",
      "height": "",
      "entityName": "Cliente",
      "properties": [
        {
          "id": "prop-1",
          "name": "id"
        },
        {
          "id": "prop-2",
          "name": "nombre"
        },
        {
          "id": "prop-3",
          "name": "apellidos"
        }
      ]
    },
    {
      "id": "forma-2",
      "tipo": "entity",
      "left": "288.433px",
      "top": "293.654px",
      "width": "",
      "height": "",
      "entityName": "Producto",
      "properties": [
        {
          "id": "prop-4",
          "name": "id"
        },
        {
          "id": "prop-5",
          "name": "nombre"
        },
        {
          "id": "prop-6",
          "name": "precio"
        }
      ]
    },
    {
      "id": "forma-3",
      "tipo": "entity",
      "left": "283.771px",
      "top": "135.621px",
      "width": "",
      "height": "",
      "entityName": "Pedido",
      "properties": [
        {
          "id": "prop-7",
          "name": "id"
        },
        {
          "id": "prop-8",
          "name": "fecha"
        },
        {
          "id": "prop-9",
          "name": "cliente_id"
        }
      ]
    },
    {
      "id": "forma-5",
      "tipo": "entity",
      "left": "551.104px",
      "top": "194.308px",
      "width": "",
      "height": "",
      "entityName": "LineasPedido",
      "properties": [
        {
          "id": "prop-14",
          "name": "id"
        },
        {
          "id": "prop-15",
          "name": "fecha"
        },
        {
          "id": "prop-16",
          "name": "pedido_id"
        },
        {
          "id": "prop-17",
          "name": "producto_id"
        },
        {
          "id": "prop-18",
          "name": "cantidad"
        }
      ]
    }
  ],
  "flechas": [
    {
      "desde": {
        "shapeId": "forma-1",
        "propId": "prop-1",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-3",
        "propId": "prop-9",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-3",
        "propId": "prop-7",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-5",
        "propId": "prop-16",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-2",
        "propId": "prop-4",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-5",
        "propId": "prop-17",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    }
  ]
}
```

### caso tienda online
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es una representación gráfica en formato SVG (Scalable Vector Graphics) que muestra un diagrama entidad-relación (ER) para un caso de estudio de una tienda online. En este diagrama, las entidades "Cliente", "Producto", "Pedido" y "LineasPedido" se visualizan como rectángulos con sus respectivos atributos dentro del rectángulo. Las flechas en el diagrama representan relaciones entre estas entidades.

Cada entidad está definida por su nombre y un conjunto de atributos que son esencialmente los campos de la tabla correspondiente en una base de datos relacional. Por ejemplo, la entidad "Cliente" tiene atributos como "id", "nombre" y "apellidos". Las líneas con flechas conectan las entidades para mostrar cómo están relacionadas entre sí.

El código SVG incluye declaraciones CSS (a través del atributo `class`) que definen el estilo de los elementos gráficos, así como definiciones de marcadores personalizados (`defs` y `marker-end`) para dar forma a las puntas de las líneas que representan las relaciones entre entidades.

En comparación con el código anterior en formato JSON o XML, este SVG proporciona una visualización más directa del diagrama entidad-relación. Mientras que antes los datos estaban estructurados y descriptivos, ahora se utilizan elementos gráficos como rectángulos, líneas y texto para mostrar las entidades y relaciones de forma visual.

Este cambio en la representación permite a los desarrolladores y analistas ver rápidamente cómo están relacionadas las distintas partes del sistema sin necesidad de decodificar estructuras de datos complejas. Además, este formato es fácilmente editable y compatible con diversos navegadores web para visualización interactiva o impresión.

`009-caso tienda online.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="817.0249837239581" height="364.4375101725259" viewBox="0 0 817.0249837239581 364.4375101725259">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="40" y="40.01250203450519" width="219.99999999999994" height="126.40000406901038" />
<line x1="40" y1="66.41249847412108" x2="259.99999999999994" y2="66.41249847412108" stroke="#e5e7eb" stroke-width="1"/>
<text x="149.99999999999997" y="58.01249821980793" text-anchor="middle">Cliente</text>
<text x="123.90000406901041" y="86.41249593098956">id</text>
<text x="123.90000406901041" y="110.4125061035156">nombre</text>
<text x="123.90000406901041" y="134.4125061035156">apellidos</text>
<rect class="shape-entity" x="294.3500162760416" y="198.03750610351554" width="219.99999999999994" height="126.40000406901038" />
<line x1="294.3500162760416" y1="224.43750254313144" x2="514.3500162760415" y2="224.43750254313144" stroke="#e5e7eb" stroke-width="1"/>
<text x="404.3500162760415" y="216.0375022888183" text-anchor="middle">Producto</text>
<text x="381.6249999999999" y="244.43751017252598">id</text>
<text x="381.6249999999999" y="268.4374898274739">nombre</text>
<text x="381.6249999999999" y="292.4374898274739">precio</text>
<rect class="shape-entity" x="289.68749999999994" y="40" width="219.99999999999994" height="126.40000406901038" />
<line x1="289.68749999999994" y1="66.39999643961586" x2="509.6874999999999" y2="66.39999643961586" stroke="#e5e7eb" stroke-width="1"/>
<text x="399.6874999999999" y="57.99999618530271" text-anchor="middle">Pedido</text>
<text x="371.7875162760416" y="86.40000406901041">id</text>
<text x="371.7875162760416" y="110.39999389648435">fecha</text>
<text x="371.7875162760416" y="134.39999389648435">cliente_id</text>
<rect class="shape-entity" x="557.0249837239581" y="98.687510172526" width="219.99999999999994" height="174.40000406901038" />
<line x1="557.0249837239581" y1="125.0875066121419" x2="777.024983723958" y2="125.0875066121419" stroke="#e5e7eb" stroke-width="1"/>
<text x="667.0249837239581" y="116.68750635782874" text-anchor="middle">LineasPedido</text>
<text x="632.2124837239581" y="145.08749389648435">id</text>
<text x="632.2124837239581" y="169.08749389648432">fecha</text>
<text x="632.2124837239581" y="193.08749389648435">pedido_id</text>
<text x="632.2124837239581" y="217.0874938964843">producto_id</text>
<text x="632.2124837239581" y="241.0874938964843">cantidad</text>
<path class="conn" d="M 198.08752441406247 83.75626538824127 L 349.7875162760416 129.05622443923264" marker-end="url(#arrow-end)" />
<path class="conn" d="M 449.5749918619791 85.2301196227952 L 610.2124837239581 186.25737834269952" marker-end="url(#arrow-end)" />
<path class="conn" d="M 449.0624999999999 239.71417731907204 L 610.2124837239581 213.81082674993823" marker-end="url(#arrow-end)" />
</svg>
```

### caso tienda online con categorias
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código HTML es una representación visual en formato web de un diagrama ER (Diagrama Entidad Relación) que modela la estructura de datos de una tienda online. El objetivo principal del código es crear una página web donde se muestran diferentes entidades y sus relaciones, utilizando estilos CSS para darle forma a estas entidades y al dibujar las líneas que conectan entre ellas.

En el cuerpo del HTML, hay varias divs con la clase "shape entity", cada una representando una entidad diferente en el modelo ER (como Cliente, Producto, Pedido, LineasPedido, y Categoria). Cada entidad tiene un encabezado que muestra su nombre y propiedades internas que contienen atributos como ID, nombre, precio, etc. Estos atributos están representados dentro de divs con la clase "entity-property", donde también se muestran puertos (divs con la clase "port") en los extremos izquierdo y derecho para simular las conexiones a otras entidades.

Además, existen varios elementos con la clase "arrow" que conectan visualmente estas entidades, representando así las relaciones entre ellas en el modelo ER de la tienda online. Estas líneas se posicionan y rotan según los atributos CSS proporcionados para mostrar correctamente cómo cada entidad está relacionada con otra.

Este diagrama es útil para estudiantes y desarrolladores que quieren entender mejor cómo están estructuradas las bases de datos relacionales en aplicaciones web como una tienda online, mostrando visualmente cuáles son las entidades principales y cómo se conectan entre sí. El uso del CSS permite dar formato a la página web de manera detallada para mejorar su apariencia y legibilidad.

`010-caso tienda online con categorias.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 821.9874877929686px;
  height: 388.437520345052px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:44.962504069010414px;top:40.01250203450522px;width:219.99999999999994px;height:126.40001424153643px;">
  <div class="entity-header">Cliente</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:299.312520345052px;top:198.0375162760416px;width:219.99999999999994px;height:150.40000406901038px;">
  <div class="entity-header">Producto</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">precio</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">categoria_id</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:294.6500040690104px;top:40px;width:219.99999999999994px;height:126.40001424153643px;">
  <div class="entity-header">Pedido</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">fecha</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">cliente_id</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:561.9874877929686px;top:98.6875px;width:219.99999999999994px;height:174.40000406901038px;">
  <div class="entity-header">LineasPedido</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">fecha</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">pedido_id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">producto_id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">cantidad</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:40px;top:243.3625081380208px;width:219.99999999999994px;height:102.4000040690104px;">
  <div class="entity-header">Categoria</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="arrow" style="left:203.05002848307288px;top:83.7562758456234px;width:158.31921769311606px;transform:rotate(0.29018612587092824rad);"></div>
<div class="arrow" style="left:454.5374959309895px;top:85.23011989264339px;width:189.7654150326733px;transform:rotate(0.5614093769739963rad);"></div>
<div class="arrow" style="left:466.77500406901027px;top:239.65559476710516px;width:150.62364183910387px;transform:rotate(-0.172043463442806rad);"></div>
<div class="arrow" style="left:194.71250406901038px;top:286.4850857909054px;width:159.13771240526012px;transform:rotate(0.15921284452516443rad);"></div>
</div>
</body>
</html>
```

### caso tienda online con categorias
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

El archivo JSON proporcionado describe un diagrama de entidad-relación (ER) que incluye entidades y sus relaciones. Vamos a analizarlo en detalle.

### Entidades

1. **Cliente**
   - **ID:** forma-1
   - **Posición:** left: 34.0792px, top: 135.625px
   - **Propiedades:** id, nombre, apellidos

2. **Producto**
   - **ID:** forma-2
   - **Posición:** left: 288.433px, top: 293.654px
   - **Propiedades:** id, nombre, precio, categoria_id

3. **Pedido**
   - **ID:** forma-3
   - **Posición:** left: 283.771px, top: 135.621px
   - **Propiedades:** id, fecha, cliente_id

4. **LineasPedido**
   - **ID:** forma-5
   - **Posición:** left: 551.104px, top: 194.308px
   - **Propiedades:** id, fecha, pedido_id, producto_id, cantidad

5. **Categoria**
   - **ID:** forma-6
   - **Posición:** left: 29.1208px, top: 338.983px
   - **Propiedades:** id, nombre

### Relaciones (Flechas)

1. **Relación entre Cliente y Pedido**
   - **Desde:** Cliente -> prop-1 (id) [right]
   - **Hasta:** Pedido -> prop-9 (cliente_id) [left]

2. **Relación entre Pedido y LineasPedido**
   - **Desde:** Pedido -> prop-7 (id) [right]
   - **Hasta:** LineasPedido -> prop-16 (pedido_id) [left]

3. **Relación entre Producto y LineasPedido**
   - **Desde:** Producto -> prop-4 (id) [right]
   - **Hasta:** LineasPedido -> prop-17 (producto_id) [left]

4. **Relación entre Categoria y Producto**
   - **Desde:** Categoria -> prop-19 (id) [right]
   - **Hasta:** Producto -> prop-21 (categoria_id) [left]

### Explicación de la Relación

- **Cliente** tiene una relación uno a muchos con **Pedido**: Un cliente puede realizar varios pedidos.
- **Producto** tiene una relación uno a muchos con **LineasPedido**: Un producto puede aparecer en varias líneas de pedido (por ejemplo, si se compra varias veces).
- **Categoria** tiene una relación uno a muchos con **Producto**: Una categoría puede tener múltiples productos asociados.

### Conclusión

El diagrama muestra una estructura típica para un sistema de gestión de pedidos y catálogo de productos. Las entidades están correctamente relacionadas, permitiendo la representación de datos complejos como el seguimiento de los productos en las líneas de pedido y la categorización de los mismos.

Esta descripción proporciona una base sólida para visualizar y entender cómo funcionan las relaciones entre diferentes objetos (o tablas) en un sistema de gestión de pedidos.

`010-caso tienda online con categorias.json`

```json
{
  "formas": [
    {
      "id": "forma-1",
      "tipo": "entity",
      "left": "34.0792px",
      "top": "135.625px",
      "width": "",
      "height": "",
      "entityName": "Cliente",
      "properties": [
        {
          "id": "prop-1",
          "name": "id"
        },
        {
          "id": "prop-2",
          "name": "nombre"
        },
        {
          "id": "prop-3",
          "name": "apellidos"
        }
      ]
    },
    {
      "id": "forma-2",
      "tipo": "entity",
      "left": "288.433px",
      "top": "293.654px",
      "width": "",
      "height": "",
      "entityName": "Producto",
      "properties": [
        {
          "id": "prop-4",
          "name": "id"
        },
        {
          "id": "prop-5",
          "name": "nombre"
        },
        {
          "id": "prop-6",
          "name": "precio"
        },
        {
          "id": "prop-21",
          "name": "categoria_id"
        }
      ]
    },
    {
      "id": "forma-3",
      "tipo": "entity",
      "left": "283.771px",
      "top": "135.621px",
      "width": "",
      "height": "",
      "entityName": "Pedido",
      "properties": [
        {
          "id": "prop-7",
          "name": "id"
        },
        {
          "id": "prop-8",
          "name": "fecha"
        },
        {
          "id": "prop-9",
          "name": "cliente_id"
        }
      ]
    },
    {
      "id": "forma-5",
      "tipo": "entity",
      "left": "551.104px",
      "top": "194.308px",
      "width": "",
      "height": "",
      "entityName": "LineasPedido",
      "properties": [
        {
          "id": "prop-14",
          "name": "id"
        },
        {
          "id": "prop-15",
          "name": "fecha"
        },
        {
          "id": "prop-16",
          "name": "pedido_id"
        },
        {
          "id": "prop-17",
          "name": "producto_id"
        },
        {
          "id": "prop-18",
          "name": "cantidad"
        }
      ]
    },
    {
      "id": "forma-6",
      "tipo": "entity",
      "left": "29.1208px",
      "top": "338.983px",
      "width": "",
      "height": "",
      "entityName": "Categoria",
      "properties": [
        {
          "id": "prop-19",
          "name": "id"
        },
        {
          "id": "prop-20",
          "name": "nombre"
        }
      ]
    }
  ],
  "flechas": [
    {
      "desde": {
        "shapeId": "forma-1",
        "propId": "prop-1",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-3",
        "propId": "prop-9",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-3",
        "propId": "prop-7",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-5",
        "propId": "prop-16",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-2",
        "propId": "prop-4",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-5",
        "propId": "prop-17",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-6",
        "propId": "prop-19",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-2",
        "propId": "prop-21",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    }
  ]
}
```

### caso tienda online con categorias
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

El archivo SVG proporcionado representa una representación gráfica de entidades y sus relaciones en un diagrama entidad-relación (ER) simplificado, similar a la estructura de datos que se vería en una base de datos relacional. A continuación, desglosaré las partes del código:

1. **Entidades Representadas**:
   - **Producto**: Esta entidad contiene los atributos id, nombre, precio y categoria_id.
   - **Categoria**: La entidad Categoria tiene los atributos id y nombre.
   - **Pedido**: Tiene tres atributos: id, fecha y cliente_id.
   - **LineasPedido**: Contiene cinco atributos (id, fecha, pedido_id, producto_id y cantidad).
   - **Cliente**: Aunque no se menciona explícitamente como entidad en el texto SVG, los atributos de 'nombre' y 'apellidos' del Cliente están asociados con la entidad Producto. Sin embargo, para la claridad estructural, parece estar implícito que hay una relación entre Pedido y Cliente a través de cliente_id.

2. **Relaciones Representadas**:
   - Existen líneas (patrones `<path class="conn">`) que conectan las entidades, indicando relaciones entre ellas.
     - Una línea conecta la entidad Producto con LineasPedido.
     - Otra línea conecta la entidad Pedido con LineasPedido.
     - La última línea conecta la entidad Categoria con Producto.
   - Estas líneas representan cómo los datos se relacionan entre sí. Por ejemplo, la relación entre Producto y Categoria indica que un producto pertenece a una categoría específica.

3. **Detalles de las Entidades**:
   - Cada entidad es dibujada como un rectángulo con bordes redondeados, etiquetado internamente con sus atributos.
   - Las entidades están posicionadas en el espacio SVG para facilitar la visualización de sus relaciones a través de líneas.

### Interpretación de los Elementos SVG:
- **Rectángulos**: Representan las entidades (Producto, Categoria, Pedido y LineasPedido).
  - Por ejemplo: `<rect class="shape-entity" x="294.6500040690104" y="40" width="219.99999999999994" height="126.40001424153643" />`
- **Líneas internas en rectángulos**: Representan los atributos de cada entidad.
  - Por ejemplo: `<line x1="294.6500040690104" y1="66.40000152587892" x2="514.6500040690103" y2="66.40000152587892" stroke="#e5e7eb" stroke-width="1"/>`
- **Texto dentro de los rectángulos**: Etiquetas para cada atributo.
  - Por ejemplo: `<text x="376.750020345052" y="110.40000851949054">fecha</text>`
- **Líneas que conectan los rectángulos**: Representan las relaciones entre entidades.
  - Por ejemplo: `<path class="conn" d="M 466.77500406901027 239.65559476710516 L 615.1749877929686 213.86942964695723" marker-end="url(#arrow-end)" />`

### Relaciones Específicas:
- **Producto y Categoria**: Una relación de pertenencia, donde un producto está asociado con una categoría.
- **Pedido y LineasPedido**: Muestra que cada pedido puede tener múltiples líneas de pedidos asociadas a él.
- **LineasPedido y Producto**: Indica la relación entre una línea específica del pedido y el producto correspondiente.

Este diagrama es útil para visualizar cómo las entidades se relacionan en un sistema de datos, facilitando el entendimiento y diseño de la estructura de bases de datos.

`010-caso tienda online con categorias.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="821.9874877929686" height="388.437520345052" viewBox="0 0 821.9874877929686 388.437520345052">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="44.962504069010414" y="40.01250203450522" width="219.99999999999994" height="126.40001424153643" />
<line x1="44.962504069010414" y1="66.41250356038411" x2="264.9625040690104" y2="66.41250356038411" stroke="#e5e7eb" stroke-width="1"/>
<text x="154.96250406901038" y="58.01250330607096" text-anchor="middle">Cliente</text>
<text x="128.86250813802081" y="86.41250610351562">id</text>
<text x="128.86250813802081" y="110.41251055399576">nombre</text>
<text x="128.86250813802081" y="134.4125061035156">apellidos</text>
<rect class="shape-entity" x="299.312520345052" y="198.0375162760416" width="219.99999999999994" height="150.40000406901038" />
<line x1="299.312520345052" y1="224.4375127156575" x2="519.312520345052" y2="224.4375127156575" stroke="#e5e7eb" stroke-width="1"/>
<text x="409.312520345052" y="216.03751246134436" text-anchor="middle">Producto</text>
<text x="373.83750406901027" y="244.43752034505204">id</text>
<text x="373.83750406901027" y="268.43752034505206">nombre</text>
<text x="373.83750406901027" y="292.437520345052">precio</text>
<text x="373.83750406901027" y="316.437520345052">categoria_id</text>
<rect class="shape-entity" x="294.6500040690104" y="40" width="219.99999999999994" height="126.40001424153643" />
<line x1="294.6500040690104" y1="66.40000152587892" x2="514.6500040690103" y2="66.40000152587892" stroke="#e5e7eb" stroke-width="1"/>
<text x="404.6500040690104" y="58.00000127156577" text-anchor="middle">Pedido</text>
<text x="376.750020345052" y="86.40000406901041">id</text>
<text x="376.750020345052" y="110.40000851949054">fecha</text>
<text x="376.750020345052" y="134.40001424153644">cliente_id</text>
<rect class="shape-entity" x="561.9874877929686" y="98.6875" width="219.99999999999994" height="174.40000406901038" />
<line x1="561.9874877929686" y1="125.08751424153645" x2="781.9874877929685" y2="125.08751424153645" stroke="#e5e7eb" stroke-width="1"/>
<text x="671.9874877929686" y="116.68751017252603" text-anchor="middle">LineasPedido</text>
<text x="637.1749877929686" y="145.08751424153644">id</text>
<text x="637.1749877929686" y="169.08750406901038">fecha</text>
<text x="637.1749877929686" y="193.0875040690104">pedido_id</text>
<text x="637.1749877929686" y="217.08750406901035">producto_id</text>
<text x="637.1749877929686" y="241.08750406901035">cantidad</text>
<rect class="shape-entity" x="40" y="243.3625081380208" width="219.99999999999994" height="102.4000040690104" />
<line x1="40" y1="269.76250457763666" x2="259.99999999999994" y2="269.76250457763666" stroke="#e5e7eb" stroke-width="1"/>
<text x="149.99999999999997" y="261.3625043233235" text-anchor="middle">Categoria</text>
<text x="127.2750040690104" y="289.76251220703125">id</text>
<text x="127.2750040690104" y="313.76251220703125">nombre</text>
<path class="conn" d="M 203.05002848307288 83.7562758456234 L 354.750020345052 129.05624449942866" marker-end="url(#arrow-end)" />
<path class="conn" d="M 454.5374959309895 85.23011989264339 L 615.1749877929686 186.25738824537743" marker-end="url(#arrow-end)" />
<path class="conn" d="M 466.77500406901027 239.65559476710516 L 615.1749877929686 213.86942964695723" marker-end="url(#arrow-end)" />
<path class="conn" d="M 194.71250406901038 286.4850857909054 L 351.8375040690104 311.7149467611779" marker-end="url(#arrow-end)" />
</svg>
```

### caso de que un producto tenga muchas categorias
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código HTML representa una representación visual de un modelo de base de datos, mostrando relaciones entre diferentes entidades a través de flechas. La estructura del documento incluye estilos CSS y elementos HTML que definen la apariencia y la disposición de las entidades en el modelo.

### Resumen del Código

1. **Cabecera del Documento (`<head>`):**
   - Define los estilos (CSS) necesarios para visualizar las entidades y sus relaciones.
   
2. **Cuerpo del Documento (`<body>`):**
   - Contiene un contenedor principal (`div.page`) que engloba todas las entidades y las flechas de conexión.

### Entidades

Las entidades en el modelo son:
- `Cliente`
- `Pedido`
- `LineasPedido`
- `Categoria`
- `Producto`
- `Entidad` (esta entidad no parece estar relacionada con ninguna relación específica, es posible que sea una entidad de prueba o un error)

Cada entidad tiene propiedades definidas en el atributo `.entity-properties`, mostradas como nombres de columnas en la base de datos.

### Flechas de Conexión

Las flechas representan las relaciones entre entidades. Estas flechas se definen con etiquetas `<div>` que tienen estilos CSS para establecer su posición y dirección (usando transformaciones rotacionales).

### Ejemplo de Entidad (`Cliente`)

```html
<div class="shape entity" style="left:40.3125px;top:40.01250203450522px;width:219.99999999999994px;height:126.40001424153643px;">
  <div class="entity-header">Cliente</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
```

### Ejemplo de Flecha

```html
<div class="arrow" style="left:198.40002441406247px;top:83.75627073265511px;width:158.31921743552306px;transform:rotate(0.29018612042228886rad);"></div>
```

### Importancia en un Curso de Bases de Datos

En el contexto de un curso sobre bases de datos, este código HTML representa un modelo ER (Entidad-Relación) visualmente y sirve para:

1. **Visualización:** Ayuda a los estudiantes a visualizar las relaciones entre diferentes entidades.
2. **Diseño de Bases de Datos:** Permite entender cómo se conectan las tablas en una base de datos relacional.
3. **Normalización:** Ayuda a identificar redundancias y mejorar la normalización del diseño.

### Ejecución del Código

Para ver el código funcionar, debes abrir este archivo HTML con un navegador web (como Google Chrome o Firefox). El resultado mostrará entidades en forma de cuadrados con propiedades y flechas que representan relaciones entre ellas.

`011-caso de que un producto tenga muchas categorias.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 817.3374837239581px;
  height: 485.0875040690104px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:40.3125px;top:40.01250203450522px;width:219.99999999999994px;height:126.40001424153643px;">
  <div class="entity-header">Cliente</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:289.99999999999994px;top:40px;width:219.99999999999994px;height:126.40001424153643px;">
  <div class="entity-header">Pedido</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">fecha</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">cliente_id</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:557.3374837239581px;top:98.6875px;width:219.99999999999994px;height:174.40000406901038px;">
  <div class="entity-header">LineasPedido</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">fecha</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">pedido_id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">producto_id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">cantidad</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:40.02500406901042px;top:342.6875px;width:219.99999999999994px;height:102.4000040690104px;">
  <div class="entity-header">Categoria</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:40px;top:191.3625081380208px;width:219.99999999999994px;height:126.40000406901038px;">
  <div class="entity-header">Producto</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">atributo</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:307.33752441406244px;top:280.05000813802076px;width:219.99999999999994px;height:126.40000406901038px;">
  <div class="entity-header">Entidad</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">producto_id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">categoria_id</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="arrow" style="left:198.40002441406247px;top:83.75627073265511px;width:158.31921743552306px;transform:rotate(0.29018612042228886rad);"></div>
<div class="arrow" style="left:449.8874918619791px;top:85.23011494130446px;width:189.7654175968351px;transform:rotate(0.561409398459061rad);"></div>
<div class="arrow" style="left:195.08752441406247px;top:236.68061831578078px;width:196.3873654535851px;transform:rotate(0.5752975064181314rad);"></div>
<div class="arrow" style="left:194.7375081380208px;top:384.70924034584186px;width:165.70740981764874px;transform:rotate(-0.08386594787429323rad);"></div>
<div class="arrow" style="left:195.08752441406247px;top:233.5433102148876px;width:415.9300454950762px;transform:rotate(-0.04867308072567927rad);"></div>
</div>
</body>
</html>
```

### caso de que un producto tenga muchas categorias
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

El archivo JSON proporcionado representa una entidad de diagrama de base de datos en formato estructurado. Aquí está un análisis detallado:

### Sección: Formas (Entities)
La sección "formas" contiene objetos que representan diferentes entidades del diagrama. Cada entidad tiene las siguientes propiedades:

- **id**: Un identificador único para la forma.
- **tipo**: Especifica el tipo de objeto, en este caso siempre es `"entity"`.
- **left** y **top**: Coordenadas que determinan la posición horizontal y vertical de cada entidad respectivamente. Estas coordenadas están dadas en píxeles (px).
- **width** y **height**: Las dimensiones del rectángulo que contiene a la entidad, aunque no se especifican explícitamente.
- **entityName**: El nombre de la entidad, como "Cliente", "Pedido", etc.
- **properties**: Una lista de propiedades asociadas con cada entidad. Cada propiedad tiene un identificador único (id) y un nombre.

### Ejemplos de Formas
Aquí hay algunos ejemplos de entidades en el archivo JSON:

1. **Cliente**
   ```json
   {
     "id": "forma-1",
     "tipo": "entity",
     "left": "34.0792px",
     "top": "135.625px",
     "entityName": "Cliente",
     "properties": [
       { "id": "prop-1", "name": "id" },
       { "id": "prop-2", "name": "nombre" },
       { "id": "prop-3", "name": "apellidos" }
     ]
   }
   ```

2. **Pedido**
   ```json
   {
     "id": "forma-3",
     "tipo": "entity",
     "left": "283.771px",
     "top": "135.621px",
     "entityName": "Pedido",
     "properties": [
       { "id": "prop-7", "name": "id" },
       { "id": "prop-8", "name": "fecha" },
       { "id": "prop-9", "name": "cliente_id" }
     ]
   }
   ```

3. **LineasPedido**
   ```json
   {
     "id": "forma-5",
     "tipo": "entity",
     "left": "551.104px",
     "top": "194.308px",
     "entityName": "LineasPedido",
     "properties": [
       { "id": "prop-14", "name": "id" },
       { "id": "prop-15", "name": "fecha" },
       { "id": "prop-16", "name": "pedido_id" },
       { "id": "prop-17", "name": "producto_id" },
       { "id": "prop-18", "name": "cantidad" }
     ]
   }
   ```

### Sección: Flechas (Relations)
La sección "flechas" describe las relaciones entre diferentes entidades. Cada relación tiene las siguientes propiedades:

- **desde**: Un objeto que especifica el punto de inicio de la flecha.
  - **shapeId**: El identificador único de la forma desde donde parte la flecha.
  - **propId**: El identificador del atributo en esa forma asociado con el extremo inicial de la flecha.
  - **side**: Eje de la propiedad (izquierda o derecha).
- **hasta**: Un objeto que especifica el punto final de la flecha, similar a `desde`.
- **tipo**: El tipo de relación (`simple` en este caso).
- **estilo**: Estilo de dibujo de la flecha (`straight` indica una línea recta).

### Ejemplos de Flechas
Aquí hay algunos ejemplos de relaciones:

1. Relación entre Cliente y Pedido:
   ```json
   {
     "desde": { "shapeId": "forma-1", "propId": "prop-1", "side": "right" },
     "hasta": { "shapeId": "forma-3", "propId": "prop-9", "side": "left" },
     "tipo": "simple",
     "estilo": "straight"
   }
   ```

2. Relación entre Pedido y LineasPedido:
   ```json
   {
     "desde": { "shapeId": "forma-3", "propId": "prop-7", "side": "right" },
     "hasta": { "shapeId": "forma-5", "propId": "prop-16", "side": "left" },
     "tipo": "simple",
     "estilo": "straight"
   }
   ```

3. Relación entre Producto y Entidad:
   ```json
   {
     "desde": { "shapeId": "forma-9", "propId": "prop-27", "side": "right" },
     "hasta": { "shapeId": "forma-10", "propId": "prop-31", "side": "left" },
     "tipo": "simple",
     "estilo": "straight"
   }
   ```

### Resumen
Este archivo JSON describe una base de datos relacional con entidades como Cliente, Pedido, LineasPedido, Producto y Entidad. Cada entidad tiene propiedades definidas y se relacionan entre sí a través de relaciones rectilíneas (flechas). La estructura permite representar un diagrama ER o similar de una manera fácilmente serializable y deserializable en JSON.

El archivo proporcionado parece ser la representación en formato JSON de un diagrama de base de datos generado por alguna herramienta gráfica, probablemente convertido desde su forma visual a una forma estructurada para almacenamiento o transmisión.

`011-caso de que un producto tenga muchas categorias.json`

```json
{
  "formas": [
    {
      "id": "forma-1",
      "tipo": "entity",
      "left": "34.0792px",
      "top": "135.625px",
      "width": "",
      "height": "",
      "entityName": "Cliente",
      "properties": [
        {
          "id": "prop-1",
          "name": "id"
        },
        {
          "id": "prop-2",
          "name": "nombre"
        },
        {
          "id": "prop-3",
          "name": "apellidos"
        }
      ]
    },
    {
      "id": "forma-3",
      "tipo": "entity",
      "left": "283.771px",
      "top": "135.621px",
      "width": "",
      "height": "",
      "entityName": "Pedido",
      "properties": [
        {
          "id": "prop-7",
          "name": "id"
        },
        {
          "id": "prop-8",
          "name": "fecha"
        },
        {
          "id": "prop-9",
          "name": "cliente_id"
        }
      ]
    },
    {
      "id": "forma-5",
      "tipo": "entity",
      "left": "551.104px",
      "top": "194.308px",
      "width": "",
      "height": "",
      "entityName": "LineasPedido",
      "properties": [
        {
          "id": "prop-14",
          "name": "id"
        },
        {
          "id": "prop-15",
          "name": "fecha"
        },
        {
          "id": "prop-16",
          "name": "pedido_id"
        },
        {
          "id": "prop-17",
          "name": "producto_id"
        },
        {
          "id": "prop-18",
          "name": "cantidad"
        }
      ]
    },
    {
      "id": "forma-7",
      "tipo": "entity",
      "left": "33.7917px",
      "top": "438.304px",
      "width": "",
      "height": "",
      "entityName": "Categoria",
      "properties": [
        {
          "id": "prop-22",
          "name": "id"
        },
        {
          "id": "prop-23",
          "name": "nombre"
        }
      ]
    },
    {
      "id": "forma-9",
      "tipo": "entity",
      "left": "33.7667px",
      "top": "286.983px",
      "width": "",
      "height": "",
      "entityName": "Producto",
      "properties": [
        {
          "id": "prop-27",
          "name": "id"
        },
        {
          "id": "prop-28",
          "name": "nombre"
        },
        {
          "id": "prop-29",
          "name": "atributo"
        }
      ]
    },
    {
      "id": "forma-10",
      "tipo": "entity",
      "left": "301.108px",
      "top": "375.663px",
      "width": "",
      "height": "",
      "entityName": "Entidad",
      "properties": [
        {
          "id": "prop-30",
          "name": "id"
        },
        {
          "id": "prop-31",
          "name": "producto_id"
        },
        {
          "id": "prop-32",
          "name": "categoria_id"
        }
      ]
    }
  ],
  "flechas": [
    {
      "desde": {
        "shapeId": "forma-1",
        "propId": "prop-1",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-3",
        "propId": "prop-9",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-3",
        "propId": "prop-7",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-5",
        "propId": "prop-16",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-9",
        "propId": "prop-27",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-10",
        "propId": "prop-31",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-7",
        "propId": "prop-22",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-10",
        "propId": "prop-32",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-9",
        "propId": "prop-27",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-5",
        "propId": "prop-17",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    }
  ]
}
```

### caso de que un producto tenga muchas categorias
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

El código SVG proporcionado representa un diagrama de entidad-relación simplificado, donde las entidades son rectángulos y las relaciones entre ellas se representan mediante líneas con flechas (arrows). Vamos a desglosarlo para entender mejor su estructura y contenido.

### Entidades

1. **Cliente**:
   - Posición: `(40, 318)`
   - Dimensiones: `219x102`
   - Atributos: `id`, `nombre`

2. **Pedido**:
   - Posición: `(557, 162)`
   - Dimensiones: `219x174`
   - Atributos: `id`, `fecha`, `pedido_id`, `producto_id`, `cantidad`

3. **Producto**:
   - Posición: `(40, 182)`
   - Dimensiones: `219x126`
   - Atributos: `id`, `nombre`, `atributo`

4. **Categoría**:
   - Posición: `(40, 345)`
   - Dimensiones: `219x102`
   - Atributos: `id`, `nombre`

5. **Entidad** (no está claro qué entidad es esto):
   - Posición: `(307, 280)`
   - Dimensiones: `219x126`
   - Atributos: `id`, `producto_id`, `categoria_id`


### Relaciones

1. **Relación entre Cliente y Pedido**:
   - El rectángulo del cliente está conectado con una línea hasta el rectángulo de Pedido, indicando que un cliente puede tener varios pedidos.

2. **Relación entre Pedido y LineasPedido (Detalles de pedido)**:
   - La relación apunta desde el rectángulo de Pedido hacia el rectángulo de Detalles del pedido (LineasPedido), mostrando que un pedido tiene varias líneas de detalle.

3. **Relación entre Producto y Entidad**:
   - El rectángulo del producto está conectado con una línea hasta el rectángulo de la entidad no especificada, indicando una relación entre ambos.

4. **Relación entre Categoría y Entidad**:
   - Similarmente, la categoría también tiene una relación con la entidad no especificada.

5. **Relación directa entre Producto y LineasPedido (Detalles del pedido)**:
   - Existe una conexión directa desde el rectángulo de Producto hacia el rectángulo de Detalles del pedido, indicando que un producto puede estar asociado con múltiples detalles de pedidos.


### Conclusión

El diagrama SVG representa relaciones entre diferentes entidades (como clientes, productos y pedidos) en una base de datos. Las líneas conectadas con flechas muestran cómo estas entidades están relacionadas entre sí.

Para un análisis más detallado o para la implementación de este diseño en un sistema real, sería útil tener información adicional sobre qué entidad es el rectángulo no especificada y por qué existen ciertas relaciones específicas.

`011-caso de que un producto tenga muchas categorias.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="817.3374837239581" height="485.0875040690104" viewBox="0 0 817.3374837239581 485.0875040690104">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="40.3125" y="40.01250203450522" width="219.99999999999994" height="126.40001424153643" />
<line x1="40.3125" y1="66.41250356038411" x2="260.31249999999994" y2="66.41250356038411" stroke="#e5e7eb" stroke-width="1"/>
<text x="150.31249999999997" y="58.01250330607096" text-anchor="middle">Cliente</text>
<text x="124.21250406901041" y="86.4125010172526">id</text>
<text x="124.21250406901041" y="110.41250610351562">nombre</text>
<text x="124.21250406901041" y="134.41251055399573">apellidos</text>
<rect class="shape-entity" x="289.99999999999994" y="40" width="219.99999999999994" height="126.40001424153643" />
<line x1="289.99999999999994" y1="66.40000152587892" x2="509.9999999999999" y2="66.40000152587892" stroke="#e5e7eb" stroke-width="1"/>
<text x="399.9999999999999" y="58.00000127156577" text-anchor="middle">Pedido</text>
<text x="372.1000162760416" y="86.3999989827474">id</text>
<text x="372.1000162760416" y="110.40000406901041">fecha</text>
<text x="372.1000162760416" y="134.40000851949054">cliente_id</text>
<rect class="shape-entity" x="557.3374837239581" y="98.6875" width="219.99999999999994" height="174.40000406901038" />
<line x1="557.3374837239581" y1="125.08750661214192" x2="777.337483723958" y2="125.08750661214192" stroke="#e5e7eb" stroke-width="1"/>
<text x="667.3374837239581" y="116.68750635782877" text-anchor="middle">LineasPedido</text>
<text x="632.5249837239581" y="145.08750851949054">id</text>
<text x="632.5249837239581" y="169.08751424153644">fecha</text>
<text x="632.5249837239581" y="193.0875040690104">pedido_id</text>
<text x="632.5249837239581" y="217.08750406901035">producto_id</text>
<text x="632.5249837239581" y="241.08750406901035">cantidad</text>
<rect class="shape-entity" x="40.02500406901042" y="342.6875" width="219.99999999999994" height="102.4000040690104" />
<line x1="40.02500406901042" y1="369.0875167846679" x2="260.0250040690104" y2="369.0875167846679" stroke="#e5e7eb" stroke-width="1"/>
<text x="150.02500406901038" y="360.6875165303548" text-anchor="middle">Categoria</text>
<text x="127.30000813802081" y="389.0875244140625">id</text>
<text x="127.30000813802081" y="413.0875244140624">nombre</text>
<rect class="shape-entity" x="40" y="191.3625081380208" width="219.99999999999994" height="126.40000406901038" />
<line x1="40" y1="217.76250457763663" x2="259.99999999999994" y2="217.76250457763663" stroke="#e5e7eb" stroke-width="1"/>
<text x="149.99999999999997" y="209.3625043233235" text-anchor="middle">Producto</text>
<text x="126.90000406901041" y="237.76251220703122">id</text>
<text x="126.90000406901041" y="261.7625122070312">nombre</text>
<text x="126.90000406901041" y="285.76251220703125">atributo</text>
<rect class="shape-entity" x="307.33752441406244" y="280.05000813802076" width="219.99999999999994" height="126.40000406901038" />
<line x1="307.33752441406244" y1="306.45000457763666" x2="527.3375244140624" y2="306.45000457763666" stroke="#e5e7eb" stroke-width="1"/>
<text x="417.3375244140624" y="298.05000432332355" text-anchor="middle">Entidad</text>
<text x="381.86250813802076" y="326.45001220703125">id</text>
<text x="381.86250813802076" y="350.45003255208326">producto_id</text>
<text x="381.86250813802076" y="374.45003255208326">categoria_id</text>
<path class="conn" d="M 198.40002441406247 83.75627073265511 L 350.1000162760416 129.05623848619658" marker-end="url(#arrow-end)" />
<path class="conn" d="M 449.8874918619791 85.23011494130446 L 610.5249837239581 186.25738811045332" marker-end="url(#arrow-end)" />
<path class="conn" d="M 195.08752441406247 236.68061831578078 L 359.86250813802076 343.53192644333376" marker-end="url(#arrow-end)" />
<path class="conn" d="M 194.7375081380208 384.70924034584186 L 359.86250813802076 370.8283166203039" marker-end="url(#arrow-end)" />
<path class="conn" d="M 195.08752441406247 233.5433102148876 L 610.5249837239581 213.30670606115396" marker-end="url(#arrow-end)" />
</svg>
```

### Actividades propuestas

El diagrama de clases representado por el SVG proporcionado describe una relación entre varias entidades en un sistema de gestión de ventas o inventario. Aquí se presentan las entidades principales y sus relaciones:

1. **Cliente**
   - Atributos: No especificados en el diagrama, pero normalmente incluiría datos como nombre, dirección, correo electrónico.
   - Relaciones:
     - Tiene una relación con la entidad `Pedido` (mencionado implícitamente en la tabla `Pedidos`).

2. **Pedido**
   - Atributos: Fecha de pedido.
   - Relaciones:
     - Uno a muchos con `LineasPedido`.
     - Un cliente puede realizar varios pedidos.

3. **LineasPedido**
   - Atributos: Id del pedido, id del producto, cantidad y fecha (posiblemente).
   - Relaciones:
     - Muchos a uno con `Pedidos` (uno o más líneas de pedido para un pedido).
     - Muchos a uno con `Producto`.

4. **Producto**
   - Atributos: Id del producto, nombre del producto y atributo(s) (posiblemente detalles adicionales sobre el producto como descripción, precio, categoría).

5. **Categoria**
   - Atributos: Id de la categoría y nombre.
   - Relaciones:
     - Muchos a uno con `Entidad` (una entidad puede pertenecer a una sola categoría).
     
6. **Entidad** 
   - Atributos: Id entero, id del producto relacionado (un `Producto`), id de la categoría.
   - Relaciones:
     - Uno a uno con `Producto` y `Categoria`.

### Diagrama de Clases

```plaintext
+-----------------+
|    Cliente      |
+-----------------+
| - Nombre        |
| - Direccion     |
| - CorreoElectronico  |
+-----------------+
       ^
       |
+------v-------+
|    Pedido     | <----- Relación de uno a muchos con Cliente.
+--------------+
| - FechaPedido |
+--------------+

+---------------+
| LineasPedido   |
+---------------+
| - IdPedidos    |
| - Cantidad     |
| - ProductoId   |
| - Fecha        |
+---------------+
       ^
       |
+------v-------+
|  Pedido       | <----- Relación de muchos a uno con Pedido.
+--------------+

+-----------------+
|      Producto   |
+-----------------+
| - IdProducto    |
| - Nombre        |
| - Atributos     |
+-----------------+
       ^
       |
+------v--------+
| Entidad        |  <---- Relación de muchos a uno con Producto y Categoria.
+--------------+
| - Id          |
| - ProductoId  |
| - CategoriaId |
+--------------+

+-----------------+
|    Categoría     |
+-----------------+
| - IdCategoria   |
| - Nombre        |
+-----------------+
```

### Explicación de las relaciones:

1. **Cliente y Pedido**: Un cliente puede realizar múltiples pedidos, pero un pedido siempre pertenece a un solo cliente.
2. **Pedido y LineasPedido**: Un pedido consta de varias líneas de pedido (que especifican qué productos se incluyen en el pedido con su cantidad).
3. **Producto y Entidad**: Una entidad representa una relación entre un producto y una categoría, indicando que cada producto puede pertenecer a una sola categoría.
4. **Categoría y Entidad**: Cada entidades está asociada a una única categoria.

### Conclusión:
Este modelo de clases parece describir cómo se relacionan las entidades en un sistema de ventas o inventario, con énfasis en la relación uno a muchos entre los clientes y pedidos, así como en el esquema de categorización para los productos.


<a id="el-modelo-er-ampliado-generalizacion-y-especializacion-agregacion"></a>
## El modelo ER ampliado. Generalización y especialización. Agregación

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/006-Interpretaci%C3%B3n%20de%20Diagramas%20EntidadRelaci%C3%B3n/002-El%20modelo%20ER%20ampliado.%20Generalizaci%C3%B3n%20y%20especializaci%C3%B3n.%20Agregaci%C3%B3n)

### Introducción a los ejercicios

### Diagrama Persona-Alumno-Profesor

El diagrama es un modelo de base de datos relacional que representa tres entidades principales: `Persona`, `Alumno` y `Profesor`. Las relaciones entre estas entidades están indicadas mediante líneas con flechas que conectan los rectángulos (representativos de las tablas). Analizaremos cada entidad y sus relaciones:

#### Entidad Persona
- **Nombre:** Persona
- **Atributos:**
  - id
  - nombre
  - apellidos
  - dni-nie

El identificador `id` probablemente es la clave principal (primary key) en esta tabla, que se utiliza para relacionar a personas con roles específicos como Alumno o Profesor.

#### Entidad Alumno
- **Nombre:** Alumno
- **Atributos:**
  - id
  - NIA

La entidad `Alumno` parece tener un identificador (`id`) que podría estar en relación con el atributo `id` de la tabla `Persona`. Esto implica una relación uno a uno o uno a muchos entre las entidades `Persona` y `Alumno`, dependiendo del contexto.

#### Entidad Profesor
- **Nombre:** Profesor
- **Atributos:**
  - id
  - correo_corporativo

Similar al caso de Alumno, la entidad `Profesor` tiene un identificador (`id`) que probablemente también está en relación con el atributo `id` de la tabla `Persona`.

#### Relaciones:
- Entre `Persona` y `Alumno`: Existe una línea con flecha apuntando desde `Persona` a `Alumno`, lo cual indica que cada persona puede ser un alumno, pero no necesariamente. Esto sugiere una relación de tipo **uno a muchos** o simplemente la posibilidad de que una persona pueda asociarse a un único rol como Alumno (uno a uno).
- Entre `Persona` y `Profesor`: Existe otra línea con flecha apuntando desde `Persona` a `Profesor`, lo cual indica que cada persona puede ser un profesor, pero no necesariamente. Esto sugiere una relación de tipo **uno a muchos** o simplemente la posibilidad de que una persona pueda asociarse a un único rol como Profesor (uno a uno).

### Modelo Lógico del Diagrama

Para formalizar el modelo lógico basado en el diagrama, se pueden representar las entidades y relaciones de la siguiente manera:

```plaintext
Entidad Persona:
- id: Clave Principal
- nombre
- apellidos
- dni-nie

Entidad Alumno:
- id: Clave Principal (relacionada con persona.id)
- NIA

Entidad Profesor:
- id: Clave Principal (relacionada con persona.id)
- correo_corporativo
```

### SQL para Crear las Tablas y sus Relaciones

```sql
CREATE TABLE Persona (
    id INT PRIMARY KEY,
    nombre VARCHAR(100),
    apellidos VARCHAR(255),
    dni_nie VARCHAR(9) UNIQUE  -- Asumiendo que es único, de lo contrario ajusta según el requisito.
);

-- En una relación uno a muchos o uno a uno:
CREATE TABLE Alumno (
    id INT PRIMARY KEY,
    persona_id INT NOT NULL,
    NIA VARCHAR(20),
    
    FOREIGN KEY (persona_id) REFERENCES Persona(id)
);

CREATE TABLE Profesor (
    id INT PRIMARY KEY,
    persona_id INT NOT NULL,
    correo_corporativo VARCHAR(150),

    FOREIGN KEY (persona_id) REFERENCES Persona(id)
);
```

### Conclusiones
- Cada tabla `Alumno` y `Profesor` tiene una clave foránea (`persona_id`) que se relaciona con la clave principal de la tabla `Persona`.
- Si el diagrama sugiere una relación uno a muchos, es posible que un estudiante o profesor pertenezca a varias personas en ciertas situaciones. En general, sin embargo, esto parece más bien indicar una relación uno a uno.
  
Este modelo proporciona una representación estructurada de cómo las entidades `Persona`, `Alumno` y `Profesor` se relacionan entre sí en un sistema administrativo para estudiantes y docentes.

### generalizacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código HTML crea una página web que visualiza un diagrama ER (Entidad Relación) básico. La página tiene un fondo claro y un estilo minimalista, con dos entidades principales: "Alumno" y "Profesor". Cada entidad se representa como un bloque rectangular con bordes redondeados, conteniendo propiedades específicas como el ID, nombre, apellidos y DNI.

El código define diferentes clases CSS para estilizar los elementos del diagrama. Por ejemplo, la clase `.shape.entity` proporciona las características visuales para una entidad ER, incluyendo un título (`.entity-header`) y detalles de propiedades (`.entity-properties`). Dentro de cada propiedad se muestra el nombre de la propiedad (`property-name`), rodeado por dos puntos de conexión pequeños que simbolizan posibles relaciones con otras entidades.

Este tipo de visualización es útil para estudiantes ya que facilita entender cómo los datos son organizados y relacionados en un modelo de base de datos ER, permitiendo una rápida identificación de las características comunes entre diferentes entidades.

`002-generalizacion.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 559.6000269839636px;
  height: 230.93748393811669px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:40px;top:40.53749486019734px;width:219.99999999999991px;height:150.39998907791934px;">
  <div class="entity-header">Alumno</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">dni</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:299.60002698396374px;top:40px;width:219.99999999999991px;height:150.40000513980257px;">
  <div class="entity-header">Profesor</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">dni</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
</div>
</body>
</html>
```

### generalizacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

El fragmento de código JSON describe la estructura de dos entidades en un modelo de entidad-relación (ER): "Alumno" y "Profesor". Cada entidad incluye cuatro propiedades comunes: id, nombre, apellidos y dni. Este formato es útil para representar diagramas ER de manera estructurada y fácilmente manipulable en una aplicación.

En este JSON, cada entidad se define como un objeto con varios campos. Por ejemplo, la entidad "Alumno" tiene un campo `entityName` que especifica el nombre de la entidad (en este caso, "Alumno"). También contiene una lista de propiedades (`properties`) donde cada propiedad es un objeto con su propio identificador y nombre.

Lo interesante aquí es cómo los datos se representan en un formato estructurado sin necesidad de estilos o presentación visual directa. Esto facilita la manipulación, almacenamiento y transferencia de modelos ER en formatos digitales puros.

En comparación con el código anterior que era HTML con CSS para dibujar las entidades visualmente, este JSON es puramente estructural. Esto significa que se han eliminado los detalles visuales del diagrama, concentrándose solo en la información de datos y relaciones, lo cual facilita su uso en aplicaciones de programación backend o herramientas de modelado de bases de datos que trabajan con datos ER no visualizados.

`002-generalizacion.json`

```json
{
  "formas": [
    {
      "id": "forma-1",
      "tipo": "entity",
      "left": "226.263px",
      "top": "149.411px",
      "width": "",
      "height": "",
      "entityName": "Alumno",
      "properties": [
        {
          "id": "prop-1",
          "name": "id"
        },
        {
          "id": "prop-2",
          "name": "nombre"
        },
        {
          "id": "prop-3",
          "name": "apellidos"
        },
        {
          "id": "prop-4",
          "name": "dni"
        }
      ]
    },
    {
      "id": "forma-2",
      "tipo": "entity",
      "left": "485.87px",
      "top": "148.868px",
      "width": "",
      "height": "",
      "entityName": "Profesor",
      "properties": [
        {
          "id": "prop-5",
          "name": "id"
        },
        {
          "id": "prop-6",
          "name": "nombre"
        },
        {
          "id": "prop-7",
          "name": "apellidos"
        },
        {
          "id": "prop-8",
          "name": "dni"
        }
      ]
    }
  ],
  "flechas": []
}
```

### generalizacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

El código proporcionado es un archivo SVG que representa visualmente dos entidades de una base de datos: Alumno y Profesor. Cada entidad se dibuja como un rectángulo con líneas internas para representar los atributos (propiedades) de dicha entidad. En este caso, tanto la entidad "Alumno" como la entidad "Profesor" tienen exactamente las mismas propiedades: id, nombre, apellidos y dni. La visualización es clara gracias a los estilos definidos dentro del bloque `<defs>`, que especifican cómo se deben pintar los rectángulos y texto en el diagrama.

En cuanto a la relación entre este archivo SVG y el archivo JSON anterior (002-generalizacion.json), hay una transformación significativa. Mientras que el archivo JSON proporcionaba una estructura de datos abstracta para las entidades Alumno y Profesor, incluyendo sus atributos, el archivo SVG ofrece una representación gráfica visual directa de estas entidades en un diagrama ER (Entidad Relación). Esto permite a los estudiantes visualizar fácilmente la estructura de las entidades sin depender completamente del formato JSON, facilitando así la comprensión y análisis de los modelos ER.

En resumen, el cambio principal es que el archivo SVG proporciona una representación gráfica directa de las entidades Alumno y Profesor en lugar de una descripción textual estructurada como en el JSON.

`002-generalizacion.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="559.6000269839636" height="230.93748393811669" viewBox="0 0 559.6000269839636 230.93748393811669">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="40" y="40.53749486019734" width="219.99999999999991" height="150.39998907791934" />
<line x1="40" y1="66.93750481856495" x2="259.9999999999999" y2="66.93750481856495" stroke="#e5e7eb" stroke-width="1"/>
<text x="149.99999999999994" y="58.53750610351561" text-anchor="middle">Alumno</text>
<text x="123.89999871504935" y="86.93750963712992">id</text>
<text x="123.89999871504935" y="110.93749076441712">nombre</text>
<text x="123.89999871504935" y="134.93747791491052">apellidos</text>
<text x="123.89999871504935" y="158.93747108861015">dni</text>
<rect class="shape-entity" x="299.60002698396374" y="40" width="219.99999999999991" height="150.40000513980257" />
<line x1="299.60002698396374" y1="66.40000795063217" x2="519.6000269839636" y2="66.40000795063217" stroke="#e5e7eb" stroke-width="1"/>
<text x="409.6000269839637" y="58.000002208508924" text-anchor="middle">Profesor</text>
<text x="383.49999357524666" y="86.40001477693255">id</text>
<text x="383.49999357524666" y="110.39999590421975">nombre</text>
<text x="383.49999357524666" y="134.39999610499328">apellidos</text>
<text x="383.49999357524666" y="158.4000083521792">dni</text>
</svg>
```

### solucion con generalizacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código HTML crea una representación visual de un diagrama en entidad-relación (ER) que muestra cómo las entidades "Persona", "Alumno" y "Profesor" están relacionadas. El archivo comienza definiendo el estilo para diferentes elementos del diagrama, como rectángulos, círculos, y otras formas geométricas utilizando CSS.

En la parte central del código se encuentran tres bloques de clase `entity` que representan las entidades "Persona", "Alumno" y "Profesor". Cada bloque incluye una cabecera con el nombre de la entidad y propiedades específicas como 'id', 'nombre', 'apellidos' para la entidad "Persona", 'id' y 'NIA' para la entidad "Alumno", y 'id' y 'correo_corporativo' para la entidad "Profesor".

Además, hay dos líneas (clase `arrow`) que representan las relaciones entre estas entidades. Estas flechas conectan visualmente a "Persona" con tanto "Alumno" como "Profesor". Esta estructura sugiere una relación de generalización y especialización, donde "Persona" es la entidad padre y "Alumno" y "Profesor" son subclases o casos particulares de "Persona".

Este tipo de diagrama es importante porque proporciona un modelo visual claro del diseño de base de datos y ayuda a entender las relaciones entre diferentes entidades en el sistema.

`003-solucion con generalizacion.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 626.8750381469724px;
  height: 394.2750024795531px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:189.3750381469726px;top:40px;width:219.99999999999991px;height:150.39999961853022px;">
  <div class="entity-header">Persona</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">dni-nie</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:40px;top:251.87500476837153px;width:220.00003814697257px;height:102.39999771118161px;">
  <div class="entity-header">Alumno</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">NIA</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:366.8750381469726px;top:251.87500476837153px;width:219.99999999999991px;height:102.39999771118161px;">
  <div class="entity-header">Profesor</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">correo_corporativo</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="arrow" style="left:239.58527805246655px;top:190.39999961853022px;width:78.5377006921602px;transform:rotate(2.2425279770177866rad);"></div>
<div class="arrow" style="left:370.422275379818px;top:190.39999961853022px;width:84.57235470649327px;transform:rotate(0.8137860295221024rad);"></div>
</div>
</body>
</html>
```

### solucion con generalizacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código JSON describe un modelo ER (Entidad Relación) que representa tres entidades: Persona, Alumno y Profesor. Cada entidad tiene sus propias características y está relacionada con la entidad base "Persona" a través de relaciones simples.

La estructura del JSON contiene una lista de objetos para las formas o entidades y otra lista para las flechas o relaciones entre esas entidades. Las propiedades específicas de cada entidad, como el ID, nombre, apellidos, DNI-NIE, NIA y correo corporativo, se describen dentro de un array llamado "properties" que está anidado bajo cada objeto de entidad.

Las flechas en el JSON representan las relaciones entre la entidad base "Persona" y sus entidades derivadas "Alumno" y "Profesor". Estas flechas son simples y rectas, conectando directamente desde la entidad Persona a Alumno y Profesor respectivamente. 

Este código es importante porque proporciona una estructura clara para modelar herencias y relaciones en un diagrama ER, permitiendo una representación gráfica de cómo se relacionan las diferentes entidades dentro del sistema.

ÚLTIMO PÁRRAFO: La versión actual utiliza JSON para definir visualmente el modelo ER en lugar de HTML como en la versión anterior. Esto simplifica la estructura y facilita la manipulación y renderización posterior por parte de un programa o script, ya que los datos están claramente organizados en objetos y arrays.

`003-solucion con generalizacion.json`

```json
{
  "formas": [
    {
      "id": "forma-3",
      "tipo": "entity",
      "left": "359.7px",
      "top": "-29.95px",
      "width": "",
      "height": "",
      "entityName": "Persona",
      "properties": [
        {
          "id": "prop-9",
          "name": "id"
        },
        {
          "id": "prop-10",
          "name": "nombre"
        },
        {
          "id": "prop-11",
          "name": "apellidos"
        },
        {
          "id": "prop-12",
          "name": "dni-nie"
        }
      ]
    },
    {
      "id": "forma-4",
      "tipo": "entity",
      "left": "210.325px",
      "top": "181.938px",
      "width": "",
      "height": "",
      "entityName": "Alumno",
      "properties": [
        {
          "id": "prop-13",
          "name": "id"
        },
        {
          "id": "prop-15",
          "name": "NIA"
        }
      ]
    },
    {
      "id": "forma-5",
      "tipo": "entity",
      "left": "537.2px",
      "top": "181.938px",
      "width": "",
      "height": "",
      "entityName": "Profesor",
      "properties": [
        {
          "id": "prop-14",
          "name": "id"
        },
        {
          "id": "prop-16",
          "name": "correo_corporativo"
        }
      ]
    }
  ],
  "flechas": [
    {
      "desde": {
        "shapeId": "forma-3",
        "propId": null,
        "side": null
      },
      "hasta": {
        "shapeId": "forma-4",
        "propId": null,
        "side": null
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-3",
        "propId": null,
        "side": null
      },
      "hasta": {
        "shapeId": "forma-5",
        "propId": null,
        "side": null
      },
      "tipo": "simple",
      "estilo": "straight"
    }
  ]
}
```

### solucion con generalizacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

El fragmento de código que has proporcionado es un archivo SVG (Scalable Vector Graphics) que representa un diagrama de entidades relacionales para una base de datos. Este tipo de diagramas son utilizados en diseño de bases de datos y modelado para mostrar las relaciones entre diferentes tablas o conjuntos de datos.

En este caso, el código dibuja tres rectángulos representando entidades: "Persona", "Alumno" e "Profesor". Cada entidad tiene propiedades específicas. Por ejemplo, la entidad "Persona" contiene atributos como 'id', 'nombre', 'apellidos' y 'dni-nie'. Las entidades "Alumno" y "Profesor" también tienen sus respectivos atributos 'id', pero además incluyen los atributos adicionales 'NIA' para el Alumno y 'correo_corporativo' para el Profesor.

Las líneas que conectan estos rectángulos con flechas indican las relaciones entre estas entidades. En este caso, se muestra una relación de generalización desde la entidad "Persona" hacia tanto "Alumno" como "Profesor", lo cual implica que un Alumno y un Profesor son también Personas.

Este código SVG es particularmente útil para visualizar cómo diferentes tipos de datos están relacionados entre sí en una base de datos, facilitando así el proceso de diseño y comprensión de la estructura de una base de datos.

ÚLTIMO PÁRRAFO: En comparación con el archivo anterior (003-solucion con generalizacion.json), este código SVG proporciona una visualización gráfica detallada del mismo modelo ER, utilizando formas rectangulares y flechas para representar las entidades y sus relaciones. Esto facilita la comprensión visual de los conceptos de generalización y especificación en lugar de simplemente describirlos en formato JSON.

`003-solucion con generalizacion.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="626.8750381469724" height="394.2750024795531" viewBox="0 0 626.8750381469724 394.2750024795531">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="189.3750381469726" y="40" width="219.99999999999991" height="150.39999961853022" />
<line x1="189.3750381469726" y1="66.40000104904175" x2="409.37503814697254" y2="66.40000104904175" stroke="#e5e7eb" stroke-width="1"/>
<text x="299.37503814697254" y="57.99999976158142" text-anchor="middle">Persona</text>
<text x="273.2750167846679" y="86.40000247955321">id</text>
<text x="273.2750167846679" y="110.39999508857726">nombre</text>
<text x="273.2750167846679" y="134.39999485015866">apellidos</text>
<text x="273.2750167846679" y="158.3999910354614">dni-nie</text>
<rect class="shape-entity" x="40" y="251.87500476837153" width="220.00003814697257" height="102.39999771118161" />
<line x1="40" y1="278.2750225067138" x2="260.00003814697254" y2="278.2750225067138" stroke="#e5e7eb" stroke-width="1"/>
<text x="150.00001907348627" y="269.8750128746032" text-anchor="middle">Alumno</text>
<text x="139.3125381469726" y="298.27502155303944">id</text>
<text x="139.3125381469726" y="322.2750219106673">NIA</text>
<rect class="shape-entity" x="366.8750381469726" y="251.87500476837153" width="219.99999999999991" height="102.39999771118161" />
<line x1="366.8750381469726" y1="278.2750225067138" x2="586.8750381469725" y2="278.2750225067138" stroke="#e5e7eb" stroke-width="1"/>
<text x="476.87503814697254" y="269.8750128746032" text-anchor="middle">Profesor</text>
<text x="421.78751373291" y="298.27502155303944">id</text>
<text x="421.78751373291" y="322.2750219106673">correo_corporativo</text>
<path class="conn" d="M 239.58527805246655 190.39999961853022 L 190.7079400333157 251.8750047683715" marker-end="url(#arrow-end)" />
<path class="conn" d="M 370.422275379818 190.39999961853022 L 428.50245205334323 251.8750047683715" marker-end="url(#arrow-end)" />
</svg>
```

### ejemplo con empleado
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código HTML crea una página web que representa un diagrama en el modelo entidad-relación (ER) ampliado, específicamente enfocado en la generalización y especialización. La página contiene diferentes entidades como "Persona", "Alumno", "Profesor" y "EmpleadoPAS". Cada entidad tiene propiedades definidas y se visualizan mediante cajas con bordes circulares en los extremos para representar las relaciones entre ellas.

Las entidades están estilizadas usando CSS para darles un aspecto de cuadro rectángulo con una cabecera que indica el nombre de la entidad y una lista de propiedades debajo. Las propiedades se presentan como pequeños bloques con nombres centrados dentro del cuerpo de la entidad. Además, existen flechas que conectan las entidades "Alumno", "Profesor" y "EmpleadoPAS" con la entidad base "Persona", indicando una relación de generalización donde estas entidades son subclases de "Persona".

Este diagrama es importante porque ilustra cómo se pueden modelar jerarquías en el diseño de bases de datos, permitiendo una mejor organización y abstracción de los datos. Es particularmente útil para estudiantes que están aprendiendo a interpretar y crear diagramas ER ampliados, mostrándoles cómo representar relaciones complejas como la generalización con HTML y CSS.

`005-ejemplo con empleado.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 798.125076293945px;
  height: 394.2750024795531px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:279.37503814697254px;top:40px;width:219.99999999999991px;height:150.39999961853022px;">
  <div class="entity-header">Persona</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">dni-nie</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:40px;top:251.87500476837153px;width:220.00003814697257px;height:102.39999771118161px;">
  <div class="entity-header">Alumno</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">NIA</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:286.25003814697254px;top:250.62500476837153px;width:219.99999999999991px;height:102.39999771118161px;">
  <div class="entity-header">Profesor</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">correo_corporativo</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:538.1250762939451px;top:246.87500476837153px;width:219.99999999999991px;height:102.39999771118161px;">
  <div class="entity-header">EmpleadoPAS</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">usuario_sistema</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="arrow" style="left:293.5613267794745px;top:190.39999961853022px;width:99.57011461851437px;transform:rotate(2.4761540958532944rad);"></div>
<div class="arrow" style="left:392.1452993023429px;top:190.39999961853022px;width:60.26585639774321px;transform:rotate(1.5339743982630256rad);"></div>
<div class="arrow" style="left:495.7755981656396px;top:190.39999961853022px;width:97.84928284752645px;transform:rotate(0.6152506144910285rad);"></div>
</div>
</body>
</html>
```

### ejemplo con empleado
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código JSON representa una representación estructurada de un diagrama ER (Entidad Relacional) en el que se definen varias entidades y las relaciones entre ellas. A continuación, se detalla su contenido:

### Entidades

1. **Persona**
   - Propiedades: id, nombre, apellidos, dni-nie
   - Coordenadas: left = 359.7px, top = -29.95px

2. **Alumno**
   - Propiedades: id, NIA
   - Coordenadas: left = 120.325px, top = 181.938px

3. **Profesor**
   - Propiedades: id, correo_corporativo
   - Coordenadas: left = 366.575px, top = 180.688px

4. **EmpleadoPAS**
   - Propiedades: id, usuario_sistema
   - Coordenadas: left = 618.45px, top = 176.938px

### Relaciones (Flechas)

Las entidades se relacionan entre sí a través de las siguientes flechas:

- **Persona** -> **Alumno**
- **Persona** -> **Profesor**
- **Persona** -> **EmpleadoPAS**

Cada relación es un enlace simple y recto ("straight").

### Descripción del JSON

- **formas**: Array que contiene objetos para cada entidad, incluyendo su ID, tipo, posición (left, top), nombre de la entidad (entityName) y sus propiedades.
  
- **flechas**: Array que representa las relaciones entre entidades. Cada flecha tiene un origen (`desde`) y un destino (`hasta`), especificando el ID de la forma desde la cual parte y hacia cuál apunta, respectivamente.

### Comparación con código HTML previo

El código anterior en formato HTML describe visualmente el diagrama ER mediante elementos div y estilos CSS. En cambio, este JSON es una representación estructurada que puede ser más fácil para procesar o manipular por programas (como lenguajes de programación). 

La información sobre las entidades y relaciones se organiza de manera más clara en formato JSON. Por ejemplo:
- Se eliminan detalles visuales no funcionales como estilos CSS.
- La posición de cada entidad es definida numéricamente, pero sin especificar dimensiones para evitar restricciones innecesarias.

### Uso

Este tipo de estructura en JSON sería útil para aplicaciones web que permiten crear y editar diagramas ER dinámicamente. Los datos se pueden cargar desde un archivo o base de datos para ser renderizados en una interfaz gráfica o exportados para otros formatos.

En resumen, este código JSON proporciona una representación abstracta pero completa del modelo ER, que puede ser fácilmente manipulada por aplicaciones de programación.

`005-ejemplo con empleado.json`

```json
{
  "formas": [
    {
      "id": "forma-3",
      "tipo": "entity",
      "left": "359.7px",
      "top": "-29.95px",
      "width": "",
      "height": "",
      "entityName": "Persona",
      "properties": [
        {
          "id": "prop-9",
          "name": "id"
        },
        {
          "id": "prop-10",
          "name": "nombre"
        },
        {
          "id": "prop-11",
          "name": "apellidos"
        },
        {
          "id": "prop-12",
          "name": "dni-nie"
        }
      ]
    },
    {
      "id": "forma-4",
      "tipo": "entity",
      "left": "120.325px",
      "top": "181.938px",
      "width": "",
      "height": "",
      "entityName": "Alumno",
      "properties": [
        {
          "id": "prop-13",
          "name": "id"
        },
        {
          "id": "prop-15",
          "name": "NIA"
        }
      ]
    },
    {
      "id": "forma-5",
      "tipo": "entity",
      "left": "366.575px",
      "top": "180.688px",
      "width": "",
      "height": "",
      "entityName": "Profesor",
      "properties": [
        {
          "id": "prop-14",
          "name": "id"
        },
        {
          "id": "prop-16",
          "name": "correo_corporativo"
        }
      ]
    },
    {
      "id": "forma-6",
      "tipo": "entity",
      "left": "618.45px",
      "top": "176.938px",
      "width": "",
      "height": "",
      "entityName": "EmpleadoPAS",
      "properties": [
        {
          "id": "prop-17",
          "name": "id"
        },
        {
          "id": "prop-18",
          "name": "usuario_sistema"
        }
      ]
    }
  ],
  "flechas": [
    {
      "desde": {
        "shapeId": "forma-3",
        "propId": null,
        "side": null
      },
      "hasta": {
        "shapeId": "forma-4",
        "propId": null,
        "side": null
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-3",
        "propId": null,
        "side": null
      },
      "hasta": {
        "shapeId": "forma-5",
        "propId": null,
        "side": null
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-3",
        "propId": null,
        "side": null
      },
      "hasta": {
        "shapeId": "forma-6",
        "propId": null,
        "side": null
      },
      "tipo": "simple",
      "estilo": "straight"
    }
  ]
}
```

### ejemplo con empleado
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código SVG representa un diagrama de entidades-relación (ER) en el que se muestran varias entidades y sus relaciones. Cada entidad es representada por un rectángulo con sus atributos dentro, y las relaciones entre ellas son mostradas mediante líneas con flechas que conectan los rectángulos.

La entidad "Persona" está ubicada en la parte superior del diagrama, con cuatro atributos: id, nombre, apellidos y dni-nie. Las entidades "Alumno", "Profesor" e "EmpleadoPAS" están situadas más abajo, cada una de ellas con sus propios atributos específicos (por ejemplo, Alumno tiene un NIA, Profesor un correo corporativo y EmpleadoPAS un usuario del sistema).

Las líneas conectan la entidad "Persona" con las entidades "Alumno", "Profesor" e "EmpleadoPAS". Estas conexiones indican una relación jerárquica donde cada una de estas entidades hereda de la clase base "Persona".

En comparación con el archivo anterior en formato JSON, este SVG proporciona una representación visual gráfica de las mismas relaciones y entidades. El cambio principal es que ahora se utilizan formas geométricas y líneas para mostrar claramente cómo están relacionadas entre sí, ofreciendo una visión más intuitiva del modelo ER.

ÚLTIMO PÁRRAFO: La versión actual utiliza un formato gráfico (SVG) en lugar de datos estructurados (JSON), lo que permite visualizar directamente las entidades y sus relaciones mediante formas y líneas, mejorando la comprensibilidad del diagrama ER.

`005-ejemplo con empleado.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="798.125076293945" height="394.2750024795531" viewBox="0 0 798.125076293945 394.2750024795531">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="279.37503814697254" y="40" width="219.99999999999991" height="150.39999961853022" />
<line x1="279.37503814697254" y1="66.40000104904175" x2="499.37503814697243" y2="66.40000104904175" stroke="#e5e7eb" stroke-width="1"/>
<text x="389.3750381469725" y="57.99999976158142" text-anchor="middle">Persona</text>
<text x="363.27501678466786" y="86.40000247955321">id</text>
<text x="363.27501678466786" y="110.39999508857726">nombre</text>
<text x="363.27501678466786" y="134.39999485015866">apellidos</text>
<text x="363.27501678466786" y="158.3999910354614">dni-nie</text>
<rect class="shape-entity" x="40" y="251.87500476837153" width="220.00003814697257" height="102.39999771118161" />
<line x1="40" y1="278.2750225067138" x2="260.00003814697254" y2="278.2750225067138" stroke="#e5e7eb" stroke-width="1"/>
<text x="150.00001907348627" y="269.8750128746032" text-anchor="middle">Alumno</text>
<text x="139.31249999999997" y="298.27502155303944">id</text>
<text x="139.31249999999997" y="322.2750219106673">NIA</text>
<rect class="shape-entity" x="286.25003814697254" y="250.62500476837153" width="219.99999999999991" height="102.39999771118161" />
<line x1="286.25003814697254" y1="277.0250225067138" x2="506.25003814697243" y2="277.0250225067138" stroke="#e5e7eb" stroke-width="1"/>
<text x="396.2500381469725" y="268.6250128746032" text-anchor="middle">Profesor</text>
<text x="341.16251373291004" y="297.02502155303944">id</text>
<text x="341.16251373291004" y="321.0250219106673">correo_corporativo</text>
<rect class="shape-entity" x="538.1250762939451" y="246.87500476837153" width="219.99999999999991" height="102.39999771118161" />
<line x1="538.1250762939451" y1="273.2750225067138" x2="758.125076293945" y2="273.2750225067138" stroke="#e5e7eb" stroke-width="1"/>
<text x="648.1250762939451" y="264.8750128746032" text-anchor="middle">EmpleadoPAS</text>
<text x="601.0375061035154" y="293.27502155303944">id</text>
<text x="601.0375061035154" y="317.2750368118285">usuario_sistema</text>
<path class="conn" d="M 293.5613267794745 190.39999961853022 L 215.23488509487427 251.8750047683715" marker-end="url(#arrow-end)" />
<path class="conn" d="M 392.1452993023429 190.39999961853022 L 394.36390292962676 250.6250047683715" marker-end="url(#arrow-end)" />
<path class="conn" d="M 495.7755981656396 190.39999961853022 L 575.6821432486341 246.8750047683715" marker-end="url(#arrow-end)" />
</svg>
```

### especializacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código HTML representa una página web que muestra un diagrama de entidad-relación (ER) con elementos de especialización, específicamente enfocado en la relación entre alumnos presenciales y online. El diagrama utiliza estilos CSS personalizados para dibujar formas como rectángulos, círculos, líneas y flechas.

En el código, se definen tres entidades principales:
1. **Alumno**: Una entidad base que contiene propiedades comunes a todos los alumnos como `id`, `nombre`, `apellidos` e `email`.
2. **AlumnoPresencial**: Es una especialización de la entidad Alumno y añade una propiedad adicional llamada `tarjeta_acceso_centro`.
3. **AlumnoOnline**: Otra especialización de Alumno que podría tener propiedades específicas para alumnos online, aunque en este caso muestra una propiedad no válida (`mediumseagreen`), probablemente un error tipográfico.

El código también incluye dos flechas que conectan la entidad base "Alumno" con sus entidades especializadas "AlumnoPresencial" y "AlumnoOnline". Estas flechas representan las relaciones jerárquicas entre estas entidades, indicando cómo los alumnos presenciales y online son tipos específicos de alumno.

Este tipo de diagrama es útil para comprender la estructura jerárquica de datos en bases de datos, especialmente cuando se necesitan definir grupos de objetos que heredan propiedades comunes pero también tienen características particulares.

`006-especializacion.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 613.9249674479164px;
  height: 378.225008646647px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:190.0999959309895px;top:40px;width:219.99999999999991px;height:150.40000067816834px;">
  <div class="entity-header">Alumno</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">email</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:40px;top:235.82499610053156px;width:219.99999999999991px;height:102.4000125461154px;">
  <div class="entity-header">AlumnoPresencial</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">tarjeta_acceso_centro</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:353.9249674479165px;top:234.19998592800556px;width:219.99999999999991px;height:102.4000125461154px;">
  <div class="entity-header">AlumnoOnline</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">mediumseagreen</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="arrow" style="left:234.40804417044046px;top:190.40000067816834px;width:60.31633176375316px;transform:rotate(2.2888119750509315rad);"></div>
<div class="arrow" style="left:372.4833008821071px;top:190.40000067816834px;width:60.79354083727748px;transform:rotate(0.8044813073809017rad);"></div>
</div>
</body>
</html>
```

### especializacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código JSON representa un modelo ER (Entidad Relación) en formato digital para una base de datos, específicamente centrado en la especialización del tipo de alumno (AlumnoPresencial y AlumnoOnline). En este modelo, se definen tres entidades principales: "Alumno", "AlumnoPresencial" y "AlumnoOnline". Cada entidad tiene sus propias características y atributos.

La primera entidad es "Alumno", que incluye las propiedades básicas como el identificador único (id), nombre, apellidos y email. La entidad "AlumnoPresencial" se especializa a partir de "Alumno" añadiendo un campo adicional para la tarjeta de acceso al centro educativo, reflejando así una variante del alumno que asiste presencialmente a las clases.

Por otro lado, "AlumnoOnline" también se deriva de "Alumno", pero incluye características específicas para los estudiantes que aprenden en línea. En este caso, hay un campo adicional llamado "mediumseagreen", lo cual es inusual y podría ser un error tipográfico o una representación simbólica.

El código JSON también define dos flechas simples ("simple") entre la entidad base "Alumno" y cada uno de sus derivados: "AlumnoPresencial" y "AlumnoOnline". Estas flechas sugieren las relaciones de generalización, indicando que los alumnos presenciales y en línea son una forma especializada del tipo más amplio de alumno.

ÚLTIMO PÁRRAFO:
En comparación con el código anterior en formato HTML, este archivo JSON proporciona una representación estructurada y semántica del mismo modelo ER. El cambio a JSON permite una mejor gestión y manipulación de datos para aplicaciones que requieren la importación/exportación de esquemas de base de datos, facilitando así un intercambio más eficiente entre diferentes sistemas o herramientas. Además, el uso de IDs únicos y descripciones explícitas mejora la claridad y flexibilidad del modelo ER.

`006-especializacion.json`

```json
{
  "formas": [
    {
      "id": "forma-1",
      "tipo": "entity",
      "left": "491.038px",
      "top": "116.279px",
      "width": "",
      "height": "",
      "entityName": "Alumno",
      "properties": [
        {
          "id": "prop-1",
          "name": "id"
        },
        {
          "id": "prop-2",
          "name": "nombre"
        },
        {
          "id": "prop-3",
          "name": "apellidos"
        },
        {
          "id": "prop-4",
          "name": "email"
        }
      ]
    },
    {
      "id": "forma-2",
      "tipo": "entity",
      "left": "340.947px",
      "top": "312.111px",
      "width": "",
      "height": "",
      "entityName": "AlumnoPresencial",
      "properties": [
        {
          "id": "prop-5",
          "name": "id"
        },
        {
          "id": "prop-6",
          "name": "tarjeta_acceso_centro"
        }
      ]
    },
    {
      "id": "forma-3",
      "tipo": "entity",
      "left": "654.872px",
      "top": "310.478px",
      "width": "",
      "height": "",
      "entityName": "AlumnoOnline",
      "properties": [
        {
          "id": "prop-7",
          "name": "id"
        },
        {
          "id": "prop-8",
          "name": "mediumseagreen"
        }
      ]
    }
  ],
  "flechas": [
    {
      "desde": {
        "shapeId": "forma-1",
        "propId": null,
        "side": null
      },
      "hasta": {
        "shapeId": "forma-2",
        "propId": null,
        "side": null
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-1",
        "propId": null,
        "side": null
      },
      "hasta": {
        "shapeId": "forma-3",
        "propId": null,
        "side": null
      },
      "tipo": "simple",
      "estilo": "straight"
    }
  ]
}
```

### especializacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es un archivo SVG (Scalable Vector Graphics) que representa gráficamente las entidades y relaciones definidas en el modelo ER ampliado. El archivo muestra tres entidades: "Alumno", "AlumnoPresencial" y "AlumnoOnline". Cada entidad se dibuja como un rectángulo con sus atributos correspondientes dentro de él.

La entidad principal es "Alumno", que contiene los atributos básicos como "id", "nombre", "apellidos" y "email". Las entidades derivadas, "AlumnoPresencial" y "AlumnoOnline", están relacionadas con la entidad "Alumno" mediante líneas de conexión (flechas), indicando una relación de especialización. Esto significa que los alumnos presenciales y online son un tipo específico de alumno.

El código también define estilos para diferentes elementos gráficos, como rectángulos y flechas, utilizando CSS incorporado en la sección `<defs>` del archivo SVG. Estos estilos definen colores y otros atributos visuales que hacen que el diagrama sea más legible e informativo.

En resumen, este código SVG proporciona una representación visual clara y estructurada de un modelo ER con especialización, lo cual es útil para comprender las relaciones entre diferentes tipos de entidades en un sistema de gestión de base de datos.

**ÚLTIMO PÁRRAFO:**

Este archivo SVG representa gráficamente la información que originalmente estaba codificada como JSON. A diferencia del archivo anterior, este proporciona una vista visual directamente en forma de dibujos (rectángulos y líneas con flechas) para las entidades y sus relaciones, lo cual facilita el entendimiento para los estudiantes. Además, incluye estilos CSS integrados que mejoran la presentación visual del diagrama ER.

`006-especializacion.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="613.9249674479164" height="378.225008646647" viewBox="0 0 613.9249674479164 378.225008646647">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="190.0999959309895" y="40" width="219.99999999999991" height="150.40000067816834" />
<line x1="190.0999959309895" y1="66.39999813503688" x2="410.0999959309894" y2="66.39999813503688" stroke="#e5e7eb" stroke-width="1"/>
<text x="300.09999593098945" y="58.00000042385525" text-anchor="middle">Alumno</text>
<text x="273.9999999999999" y="86.39999983045787">id</text>
<text x="273.9999999999999" y="110.39999813503688">nombre</text>
<text x="273.9999999999999" y="134.39999643961585">apellidos</text>
<text x="273.9999999999999" y="158.39999474419483">email</text>
<rect class="shape-entity" x="40" y="235.82499610053156" width="219.99999999999991" height="102.4000125461154" />
<line x1="40" y1="262.2250048319498" x2="259.9999999999999" y2="262.2250048319498" stroke="#e5e7eb" stroke-width="1"/>
<text x="149.99999999999994" y="253.82499334547245" text-anchor="middle">AlumnoPresencial</text>
<text x="86.5" y="282.225000169542">id</text>
<text x="86.5" y="306.225006951226">tarjeta_acceso_centro</text>
<rect class="shape-entity" x="353.9249674479165" y="234.19998592800556" width="219.99999999999991" height="102.4000125461154" />
<line x1="353.9249674479165" y1="260.6000116136338" x2="573.9249674479164" y2="260.6000116136338" stroke="#e5e7eb" stroke-width="1"/>
<text x="463.92496744791646" y="252.20000012715647" text-anchor="middle">AlumnoOnline</text>
<text x="413.56251356336793" y="280.600006951226">id</text>
<text x="413.56251356336793" y="304.60001373291004">mediumseagreen</text>
<path class="conn" d="M 234.40804417044046 190.40000067816834 L 194.72644051946116 235.82499610053162" marker-end="url(#arrow-end)" />
<path class="conn" d="M 372.4833008821071 190.40000067816834 L 414.642711452557 234.19998592800556" marker-end="url(#arrow-end)" />
</svg>
```

### entidades de coches sueltas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código HTML crea una página web que muestra un diagrama simplificado de entidades en una base de datos, utilizando CSS para dar estilo a los elementos del diagrama. La estructura principal es una "página" (representada por la clase `.page`) dentro de la cual se colocan varias entidades.

Cada entidad está representada por un div con la clase `.shape entity`, que tiene estilos específicos para definir su apariencia y comportamiento. Estos elementos tienen cabeceras (`entity-header`) que indican el nombre de cada entidad (por ejemplo, "Rueda", "Carroceria" y "Chapa") y propiedades (`entity-property`) que muestran atributos relevantes para cada entidad, como `id` o `diametro`.

El CSS proporcionado incluye estilos específicos para diferentes tipos de formas en el diagrama (rectángulos, botones redondeados, círculos), así como para entidades y propiedades. Estos estilos aseguran que cada elemento visualice correctamente sus características y se alinee con las convenciones del diseño.

Este tipo de representación es útil en la formación profesional para enseñar a los estudiantes cómo modelar y entender relaciones entre diferentes elementos en una base de datos, usando diagramas ER (Entity-Relationship).

`008-entidades de coches sueltas.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 821.7500610351562px;
  height: 188.7125142415364px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:40px;top:46.31251017252603px;width:219.99999999999994px;height:102.4000040690104px;">
  <div class="entity-header">Rueda</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">diametro</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:309.0875040690104px;top:40px;width:219.99997965494785px;height:102.4000040690104px;">
  <div class="entity-header">Carroceria</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">tipo_metal</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:561.7500610351562px;top:46.01250203450519px;width:219.99999999999994px;height:79.99999999999997px;">
  <div class="entity-header">Chapa</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
</div>
</body>
</html>
```

### entidades de coches sueltas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código en formato JSON representa la descripción y ubicación de entidades dentro de un diagrama ER (Diagrama Entidad Relacional). En este caso, el código define tres entidades: "Rueda", "Carroceria" y "Chapa". Cada entidad tiene sus propias características definidas por atributos como id y diametro para la rueda, id y tipo_metal para la carrocería, y solo id para la chapa. Los datos de posición (left y top) se usan para colocar visualmente estas entidades en una interfaz gráfica o en un diagrama ER digital.

El código proporciona información sobre cada entidad incluyendo su nombre y atributos específicos sin detalles estilísticos como colores y bordes. Esto simplifica la representación, concentrándose solo en los datos estructurales necesarios para entender el modelo de datos.

En comparación con la versión anterior que era un archivo HTML completo diseñado para mostrar visualmente las entidades en una página web, este nuevo archivo JSON es más ligero y se centra únicamente en almacenar información sobre las entidades y sus atributos. Esto permite una mayor flexibilidad en cómo se representa visualmente esta información, ya que el estilo y la disposición pueden ser aplicados de manera separada por otros componentes del sistema o aplicaciones.

`008-entidades de coches sueltas.json`

```json
{
  "formas": [
    {
      "id": "forma-1",
      "tipo": "entity",
      "left": "181.658px",
      "top": "197.183px",
      "width": "",
      "height": "",
      "entityName": "Rueda",
      "properties": [
        {
          "id": "prop-1",
          "name": "id"
        },
        {
          "id": "prop-2",
          "name": "diametro"
        }
      ]
    },
    {
      "id": "forma-2",
      "tipo": "entity",
      "left": "450.737px",
      "top": "190.863px",
      "width": "",
      "height": "",
      "entityName": "Carroceria",
      "properties": [
        {
          "id": "prop-3",
          "name": "id"
        },
        {
          "id": "prop-4",
          "name": "tipo_metal"
        }
      ]
    },
    {
      "id": "forma-3",
      "tipo": "entity",
      "left": "703.4px",
      "top": "196.875px",
      "width": "",
      "height": "",
      "entityName": "Chapa",
      "properties": [
        {
          "id": "prop-5",
          "name": "id"
        }
      ]
    }
  ],
  "flechas": []
}
```

### entidades de coches sueltas
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es un archivo SVG que representa una representación visual de entidades en un diagrama ER (Entidad Relación). En específico, el SVG muestra tres entidades: "Rueda", "Carroceria" y "Chapa". Cada entidad está dibujada como un rectángulo con texto dentro para identificar la entidad. Dentro del rectángulo de cada entidad se muestran los atributos asociados a ella, que son simplemente propiedades o características importantes de esa entidad.

La estructura SVG incluye definiciones de estilo y marcadores para dibujar las entidades y sus respectivos atributos con formas y colores claros y distintivos. Las entidades "Rueda", "Carroceria" y "Chapa" están dispuestas en fila horizontal, cada una con sus propios atributos detallados debajo del nombre de la entidad.

El código es importante porque proporciona una visualización gráfica que facilita entender las relaciones entre diferentes componentes de un sistema de base de datos. En este caso, nos ayuda a comprender los atributos y las entidades clave en el contexto del modelo ER.

ÚLTIMO PÁRRAFO: Este archivo SVG representa gráficamente las tres entidades identificadas en la versión anterior (008-entidades de coches sueltas.json), pero con un formato visual más detallado que incluye rectángulos para cada entidad y texto dentro del rectángulo para mostrar los atributos, proporcionando una representación mucho más clara y completa del modelo ER.

`008-entidades de coches sueltas.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="821.7500610351562" height="188.7125142415364" viewBox="0 0 821.7500610351562 188.7125142415364">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="40" y="46.31251017252603" width="219.99999999999994" height="102.4000040690104" />
<line x1="40" y1="72.71250661214192" x2="259.99999999999994" y2="72.71250661214192" stroke="#e5e7eb" stroke-width="1"/>
<text x="149.99999999999997" y="64.31250635782877" text-anchor="middle">Rueda</text>
<text x="123.68749999999997" y="92.71249389648435">id</text>
<text x="123.68749999999997" y="116.71249389648435">diametro</text>
<rect class="shape-entity" x="309.0875040690104" y="40" width="219.99997965494785" height="102.4000040690104" />
<line x1="309.0875040690104" y1="66.40000661214192" x2="529.0874837239583" y2="66.40000661214192" stroke="#e5e7eb" stroke-width="1"/>
<text x="419.0874938964843" y="58.000006357828774" text-anchor="middle">Carroceria</text>
<text x="387.812520345052" y="86.39999389648435">id</text>
<text x="387.812520345052" y="110.39999389648435">tipo_metal</text>
<rect class="shape-entity" x="561.7500610351562" y="46.01250203450519" width="219.99999999999994" height="79.99999999999997" />
<line x1="561.7500610351562" y1="72.41249847412108" x2="781.7500610351562" y2="72.41249847412108" stroke="#e5e7eb" stroke-width="1"/>
<text x="671.7500610351562" y="64.01249821980792" text-anchor="middle">Chapa</text>
<text x="666.4375610351561" y="92.4125061035156">id</text>
</svg>
```

### coche por agregacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código HTML crea una página web que representa un diagrama de entidad-relación (ER) con cuatro entidades y sus relaciones entre sí, utilizando CSS para dar estilo a las diferentes partes del diagrama. Cada entidad se presenta como un rectángulo con un encabezado que indica su nombre y propiedades que describen sus atributos clave.

Las entidades incluyen:
- **Rueda**: Con los atributos "id" y "diametro".
- **Carroceria**: Con los atributos "id", "tipo_metal", y "numero_bastidor".
- **Chapa**: Solo tiene un atributo, "id".

Además, hay una entidad llamada **Coche** que también incluye los atributos "id" y "matricula". Estas entidades están conectadas entre sí mediante flechas dobles (representadas por elementos `<div>` con la clase `arrow arrow-double`), lo cual sugiere relaciones específicas o dependencias entre ellas.

Este tipo de representación es útil para estudiantes de bases de datos, ya que ayuda a visualizar cómo diferentes componentes de un sistema interactúan y se relacionan. En este caso específico, las flechas sugieren una relación de agregación en la que el coche está compuesto por ruedas, carrocería, y chapa.

El estilo CSS aplicado garantiza que cada parte del diagrama sea visualmente distintiva e informativa, haciendo más fácil entender la estructura y las relaciones entre las entidades mostradas.

`009-coche por agregacion.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 825.750061035156px;
  height: 367.06250508626295px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:40px;top:189.65000915527338px;width:219.99999999999994px;height:102.4000040690104px;">
  <div class="entity-header">Rueda</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">diametro</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:299.0875040690104px;top:200.66250101725254px;width:219.99997965494785px;height:126.40000406901038px;">
  <div class="entity-header">Carroceria</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">tipo_metal</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">numero_bastidor</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:565.7500610351561px;top:185.33750915527338px;width:219.99999999999994px;height:79.99999999999997px;">
  <div class="entity-header">Chapa</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:294.4000040690104px;top:40px;width:219.99997965494785px;height:102.4000040690104px;">
  <div class="entity-header">Coche</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">matricula</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="arrow arrow-double" style="left:237.0382853873625px;top:189.65000915527338px;width:93.19021022966439px;transform:rotate(-0.5317326936266109rad);"></div>
<div class="arrow arrow-double" style="left:407.37171885678913px;top:200.66250101725257px;width:58.28396366391503px;transform:rotate(-1.5979379983706976rad);"></div>
<div class="arrow arrow-double" style="left:594.8330757822941px;top:185.33750915527338px;width:96.89258849727445px;transform:rotate(-2.682488278522301rad);"></div>
</div>
</body>
</html>
```

### coche por agregacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

El código JSON proporcionado representa un modelo de entidad-relación (ER) en formato estructurado. En este caso, el archivo describe cuatro entidades: Rueda, Carroceria, Chapa y Coche. Cada entidad tiene sus propias características y atributos específicos.

Las entidades se definen mediante objetos con las siguientes propiedades:
- `id`: Un identificador único para cada forma en el modelo.
- `tipo`: Tipo de la entidad (en este caso siempre es "entity").
- `left` y `top`: Coordenadas que especifican dónde está ubicada cada entidad en el espacio 2D del diagrama.
- `entityName`: El nombre de la entidad.
- `properties`: Una lista con los atributos de la entidad, donde cada atributo tiene un identificador único (`id`) y un nombre (`name`).

Además del detalle sobre las entidades, el archivo también incluye información sobre las relaciones entre ellas. Se definen tres flechas que conectan diferentes entidades a la entidad Coche, indicando una relación de agrupación o composición (ya que cada parte está contenida dentro de un coche). Cada flecha tiene:
- `desde`: Un objeto que especifica el ID de la forma de origen y el atributo asociado.
- `hasta`: Un objeto que especifica el ID de la forma destino y el atributo asociado.
- `tipo`: El tipo de conexión (en este caso, todas son "doble").
- `estilo`: El estilo de línea (todas son "straight" en este ejemplo).

En comparación con el código HTML del archivo anterior, esta versión JSON proporciona una representación más abstracta y estructurada de la misma información. Mientras que el archivo HTML incluía detalles visuales como estilos CSS y elementos div para cada entidad, el formato JSON se centra únicamente en los datos estructurados y las relaciones entre entidades.

En resumen, este código JSON proporciona una descripción detallada de un modelo ER en términos puramente estructurales, lo que facilita su procesamiento por parte de programas o herramientas que manejan modelos de datos. La información se organiza claramente para permitir la representación y manipulación del diagrama en aplicaciones de diseño de bases de datos o similares.

`009-coche por agregacion.json`

```json
{
  "formas": [
    {
      "id": "forma-1",
      "tipo": "entity",
      "left": "181.658px",
      "top": "197.183px",
      "width": "",
      "height": "",
      "entityName": "Rueda",
      "properties": [
        {
          "id": "prop-1",
          "name": "id"
        },
        {
          "id": "prop-2",
          "name": "diametro"
        }
      ]
    },
    {
      "id": "forma-2",
      "tipo": "entity",
      "left": "440.737px",
      "top": "208.196px",
      "width": "",
      "height": "",
      "entityName": "Carroceria",
      "properties": [
        {
          "id": "prop-3",
          "name": "id"
        },
        {
          "id": "prop-4",
          "name": "tipo_metal"
        },
        {
          "id": "prop-7",
          "name": "numero_bastidor"
        }
      ]
    },
    {
      "id": "forma-3",
      "tipo": "entity",
      "left": "707.4px",
      "top": "192.871px",
      "width": "",
      "height": "",
      "entityName": "Chapa",
      "properties": [
        {
          "id": "prop-5",
          "name": "id"
        }
      ]
    },
    {
      "id": "forma-4",
      "tipo": "entity",
      "left": "436.058px",
      "top": "47.525px",
      "width": "",
      "height": "",
      "entityName": "Coche",
      "properties": [
        {
          "id": "prop-6",
          "name": "id"
        },
        {
          "id": "prop-8",
          "name": "matricula"
        }
      ]
    }
  ],
  "flechas": [
    {
      "desde": {
        "shapeId": "forma-1",
        "propId": null,
        "side": null
      },
      "hasta": {
        "shapeId": "forma-4",
        "propId": null,
        "side": null
      },
      "tipo": "doble",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-2",
        "propId": null,
        "side": null
      },
      "hasta": {
        "shapeId": "forma-4",
        "propId": null,
        "side": null
      },
      "tipo": "doble",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-3",
        "propId": null,
        "side": null
      },
      "hasta": {
        "shapeId": "forma-4",
        "propId": null,
        "side": null
      },
      "tipo": "doble",
      "estilo": "straight"
    }
  ]
}
```

### coche por agregacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este archivo SVG representa un diagrama de entidad-relación (ER) en el que se muestran las entidades "Rueda", "Carrocería", "Chapa" y "Coche". Cada rectángulo dentro del diagrama corresponde a una entidad, con sus propiedades listadas debajo. Las flechas conectando estos rectángulos indican relaciones entre estas entidades. En este caso, cada uno de las entidades "Rueda", "Carrocería" y "Chapa" tiene una relación con la entidad "Coche". Esta representación visual facilita entender cómo un coche está compuesto por varias partes como ruedas y carrocerías.

En comparación con el archivo anterior, este nuevo diagrama proporciona una vista más detallada e ilustrativa de las entidades y sus relaciones. Mientras que el archivo JSON anterior describía las entidades y propiedades de forma textual, este SVG incluye un diseño gráfico que muestra claramente la disposición espacial de cada entidad y cómo se relacionan entre sí mediante flechas. Esta versión ofrece una mejor comprensión visual del modelo ER ampliado con agregación.

`009-coche por agregacion.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="825.750061035156" height="367.06250508626295" viewBox="0 0 825.750061035156 367.06250508626295">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="40" y="189.65000915527338" width="219.99999999999994" height="102.4000040690104" />
<line x1="40" y1="216.05000559488926" x2="259.99999999999994" y2="216.05000559488926" stroke="#e5e7eb" stroke-width="1"/>
<text x="149.99999999999997" y="207.65000534057612" text-anchor="middle">Rueda</text>
<text x="123.68749999999997" y="236.0499928792317">id</text>
<text x="123.68749999999997" y="260.0499928792317">diametro</text>
<rect class="shape-entity" x="299.0875040690104" y="200.66250101725254" width="219.99997965494785" height="126.40000406901038" />
<line x1="299.0875040690104" y1="227.0624974568684" x2="519.0874837239583" y2="227.0624974568684" stroke="#e5e7eb" stroke-width="1"/>
<text x="409.0874938964843" y="218.66249720255527" text-anchor="middle">Carroceria</text>
<text x="359.36248779296864" y="247.06250508626295">id</text>
<text x="359.36248779296864" y="271.06250508626295">tipo_metal</text>
<text x="359.36248779296864" y="295.06250508626295">numero_bastidor</text>
<rect class="shape-entity" x="565.7500610351561" y="185.33750915527338" width="219.99999999999994" height="79.99999999999997" />
<line x1="565.7500610351561" y1="211.73750559488926" x2="785.750061035156" y2="211.73750559488926" stroke="#e5e7eb" stroke-width="1"/>
<text x="675.7500610351561" y="203.33750534057612" text-anchor="middle">Chapa</text>
<text x="670.4375610351561" y="231.7374928792317">id</text>
<rect class="shape-entity" x="294.4000040690104" y="40" width="219.99997965494785" height="102.4000040690104" />
<line x1="294.4000040690104" y1="66.39999643961588" x2="514.3999837239583" y2="66.39999643961588" stroke="#e5e7eb" stroke-width="1"/>
<text x="404.3999938964843" y="57.99999618530273" text-anchor="middle">Coche</text>
<text x="377.11248779296864" y="86.39999898274738">id</text>
<text x="377.11248779296864" y="110.39999898274738">matricula</text>
<path class="conn" d="M 237.0382853873625 189.65000915527338 L 317.36170850912174 142.4000040690104" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />
<path class="conn" d="M 407.37171885678913 200.66250101725257 L 405.7899888758386 142.40000406901038" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />
<path class="conn" d="M 594.8330757822941 185.33750915527338 L 507.97373913579827 142.4000040690104" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />
</svg>
```

### diagrama
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es un archivo SVG que representa una parte de un diagrama de entidad-relación (ER) en el contexto de bases de datos para la especialidad DAM. El objetivo principal es visualizar cómo se relacionan diferentes entidades como "Persona", "Alumno" y "Profesor".

El diagrama muestra rectángulos que representan las entidades, con líneas horizontales dentro de ellos que indican atributos específicos (como ID, nombre, apellidos, etc.). Cada entidad está conectada a través de líneas punteadas decoradas con flechas en el extremo para mostrar relaciones entre ellas. Por ejemplo, la entidad "Persona" tiene dos líneas que salen hacia las entidades "Alumno" y "Profesor", lo cual sugiere una relación generalizada o herencia donde tanto Alumno como Profesor son tipos de Persona.

Estos diagramas son fundamentales en el diseño de bases de datos porque ayudan a entender cómo se relacionan diferentes tablas (entidades) y qué información específica contienen. En este caso, permite visualizar las relaciones jerárquicas entre personas que pueden ser tanto alumnos como profesores, facilitando la comprensión del modelo ER ampliado con generalización y especialización.

`diagrama.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="626.8750381469724" height="394.2750024795531" viewBox="0 0 626.8750381469724 394.2750024795531">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="189.3750381469726" y="40" width="219.99999999999991" height="150.39999961853022" />
<line x1="189.3750381469726" y1="66.40000104904175" x2="409.37503814697254" y2="66.40000104904175" stroke="#e5e7eb" stroke-width="1"/>
<text x="299.37503814697254" y="57.99999976158142" text-anchor="middle">Persona</text>
<text x="273.2750167846679" y="86.40000247955321">id</text>
<text x="273.2750167846679" y="110.39999508857726">nombre</text>
<text x="273.2750167846679" y="134.39999485015866">apellidos</text>
<text x="273.2750167846679" y="158.3999910354614">dni-nie</text>
<rect class="shape-entity" x="40" y="251.87500476837153" width="220.00003814697257" height="102.39999771118161" />
<line x1="40" y1="278.2750225067138" x2="260.00003814697254" y2="278.2750225067138" stroke="#e5e7eb" stroke-width="1"/>
<text x="150.00001907348627" y="269.8750128746032" text-anchor="middle">Alumno</text>
<text x="139.3125381469726" y="298.27502155303944">id</text>
<text x="139.3125381469726" y="322.2750219106673">NIA</text>
<rect class="shape-entity" x="366.8750381469726" y="251.87500476837153" width="219.99999999999991" height="102.39999771118161" />
<line x1="366.8750381469726" y1="278.2750225067138" x2="586.8750381469725" y2="278.2750225067138" stroke="#e5e7eb" stroke-width="1"/>
<text x="476.87503814697254" y="269.8750128746032" text-anchor="middle">Profesor</text>
<text x="421.78751373291" y="298.27502155303944">id</text>
<text x="421.78751373291" y="322.2750219106673">correo_corporativo</text>
<path class="conn" d="M 239.58527805246655 190.39999961853022 L 190.7079400333157 251.8750047683715" marker-end="url(#arrow-end)" />
<path class="conn" d="M 370.422275379818 190.39999961853022 L 428.50245205334323 251.8750047683715" marker-end="url(#arrow-end)" />
</svg>
```

### Actividades propuestas

Basándome en los archivos SVG proporcionados, aquí están las relaciones de agregación o composición representadas en cada diagrama:

### Diagrama 1: E/S del archivo "01.svg"

En este caso, no se muestra una relación clara de agregación o composición. Hay tres entidades (Persona, Alumno y Profesor) con flechas apuntando hacia ellas desde la entidad Persona, lo que indica relaciones "ha-que" pero no son relaciones de agregación.

### Diagrama 2: E/S del archivo "02.svg"

Analicemos el contenido SVG del segundo diagrama:

```svg
<rect class="shape-entity" x="189.3750381469726" y="40" width="219.99999999999991" height="150.39999961853022" />
<rect class="shape-entity" x="40" y="251.87500476837153" width="220.00003814697257" height="102.39999771118161" />
<rect class="shape-entity" x="366.8750381469726" y="251.87500476837153" width="219.99999999999991" height="102.39999771118161" />
<path class="conn" d="M 239.58527805246655 190.39999961853022 L 190.7079400333157 251.8750047683715" marker-end="url(#arrow-end)" />
<path class="conn" d="M 370.422275379818 190.39999961853022 L 428.50245205334323 251.8750047683715" marker-end="url(#arrow-end)" />
```

En este diagrama, hay una flecha apuntando desde Persona hacia Alumno y otra de Persona hacia Profesor.

Estas flechas representan relaciones de agregación o composición si se interpretan en el contexto de la especificación UML. En UML:

- **Agregación**: Una relación de "es parte de" donde la entidad dependiente (Alumno, Profesor) puede existir sin la entidad principal (Persona).
  
- **Composición**: Una relación más fuerte de "forma parte de" donde la entidad dependiente no existe sin la entidad principal.

Sin contexto adicional sobre las reglas específicas del modelo de negocio o datos, podemos asumir que:

1. `Alumno` y `Profesor` son entidades que **agregan** a `Persona`.
   - Es decir, un Alumno es una Persona con atributos adicionales (NIA).
   - Un Profesor es una Persona con atributos específicos de profesor (correo corporativo).

Si queremos ser precisos en la notación UML:

- Si se desea indicar que Alumno y Profesor no pueden existir sin Persona, entonces sería composición.
  
### Diagrama 3: E/S del archivo "03.svg"

```svg
<rect class="shape-entity" x="189.3750381469726" y="40" width="219.99999999999991" height="150.39999961853022" />
<rect class="shape-entity" x="40" y="251.87500476837153" width="220.00003814697257" height="102.39999771118161" />
<rect class="shape-entity" x="366.8750381469726" y="251.87500476837153" width="219.99999999999991" height="102.39999771118161" />
<path class="conn" d="M 239.58527805246655 190.39999961853022 L 190.7079400333157 251.8750047683715" marker-end="url(#arrow-end)" />
<path class="conn" d="M 370.422275379818 190.39999961853022 L 428.50245205334323 251.8750047683715" marker-end="url(#arrow-end)" />
```

Este es exactamente igual que el diagrama anterior en términos de estructura.

### Diagrama 4: E/S del archivo "diagrama.svg"

```svg
<rect class="shape-entity" x="189.3750381469726" y="40" width="219.99999999999991" height="150.39999961853022" />
<rect class="shape-entity" x="40" y="251.87500476837153" width="220.00003814697257" height="102.39999771118161" />
<rect class="shape-entity" x="366.8750381469726" y="251.87500476837153" width="219.99999999999991" height="102.39999771118161" />
<path class="conn" d="M 239.58527805246655 190.39999961853022 L 190.7079400333157 251.8750047683715" marker-end="url(#arrow-end)" />
<path class="conn" d="M 370.422275379818 190.39999961853022 L 428.50245205334323 251.8750047683715" marker-end="url(#arrow-end)" />
```

Este también es igual al diagrama anterior.

### Resumen
El único diagrama que muestra relaciones de agregación o composición claramente definidas es el segundo (diagrama "02.svg"). En este caso, hay una relación de agregación entre Persona y Alumno, y otra entre Persona y Profesor. Esto indica que tanto Alumno como Profesor son instancias de Persona con atributos adicionales.

Para ser precisos:
- `Alumno` **agrega** a `Persona`
- `Profesor` **agrega** a `Persona`

Si se aplica la lógica del modelo, si no puede existir un Alumno o Profesor sin una Persona, entonces estas relaciones son de composición. Sin embargo, esto requiere más contexto específico sobre las reglas del sistema.

En resumen:
- Diagrama 2: Relaciones de agregación (o potencialmente composición) entre Persona y Alumno, y Persona y Profesor.
- Otros diagramas no muestran claramente relaciones de agregación/composición.


<a id="paso-del-diagrama-er-al-modelo-relacional"></a>
## Paso del diagrama ER al modelo relacional

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/006-Interpretaci%C3%B3n%20de%20Diagramas%20EntidadRelaci%C3%B3n/003-Paso%20del%20diagrama%20ER%20al%20modelo%20relacional)

### Introducción a los ejercicios

### Summary and Key Points of the Case Study

The case study focuses on designing a database schema for an educational institution, specifically a center for continuous training and skills development. The primary goal is to facilitate the management of students (referred to as "alumnos" in Spanish), courses (called "asignaturas"), and student enrollment records (named "matriculas").

#### Entities and Relationships

1. **Alumno**:
    - Represents a student enrolled in various courses.
    - Attributes: 
        - `id`: Unique identifier for each student.
        - `nombre`: Student's first name or full name.
        - `apellidos`: Last name(s) of the student.
        - `email`: Contact email address.

2. **Asignatura**:
    - Represents a course offered by the institution.
    - Attributes: 
        - `id`: Unique identifier for each course.
        - `nombre`: Name of the course.
        - `descripcion`: Detailed description or syllabus of the course (optional).

3. **Matricula**:
    - Captures the enrollment status of students in different courses.
    - Attributes: 
        - `id`: Unique identifier for each enrollment record.
        - `fecha`: Date when a student enrolled in a particular course.
        - `alumno_id`: Foreign key referencing the primary key of the Alumno table.
        - `asignatura_id`: Foreign key referencing the primary key of the Asignatura table.

#### Database Schema

The SQL schema consists of three tables:

- **Alumno**: Stores student information.
  ```sql
  CREATE TABLE Alumno (
      id INT AUTO_INCREMENT PRIMARY KEY,
      nombre     VARCHAR(100) NOT NULL,
      apellidos  VARCHAR(150) NOT NULL,
      email      VARCHAR(150) NOT NULL
  ) ENGINE=InnoDB;
  ```

- **Asignatura**: Stores course information.
  ```sql
  CREATE TABLE Asignatura (
      id INT AUTO_INCREMENT PRIMARY KEY,
      nombre       VARCHAR(150) NOT NULL,
      descripcion  TEXT
  ) ENGINE=InnoDB;
  ```

- **Matricula**: Manages student enrollment in courses and includes foreign key constraints to enforce referential integrity.
  ```sql
  CREATE TABLE Matricula (
      id INT AUTO_INCREMENT PRIMARY KEY,
      fecha DATE NOT NULL,
      alumno_id INT NOT NULL,
      asignatura_id INT NOT NULL,

      CONSTRAINT fk_matricula_alumno
          FOREIGN KEY (alumno_id)
          REFERENCES Alumno(id)
          ON UPDATE CASCADE
          ON DELETE CASCADE,

      CONSTRAINT fk_matricula_asignatura
          FOREIGN KEY (asignatura_id)
          REFERENCES Asignatura(id)
          ON UPDATE CASCADE
          ON DELETE RESTRICT
  ) ENGINE=InnoDB;
  ```

#### Key Points

1. **Primary Keys**:
    - `id` fields in each table serve as the primary keys, ensuring uniqueness and facilitating data indexing.

2. **Foreign Keys**:
    - The foreign key constraints (`alumno_id` in Matricula referencing Alumno.id) ensure that a student's enrollment record is valid only if the associated student exists.
    - Similarly, `asignatura_id` ensures that an enrolled course must exist in the Asignatura table.

3. **Referential Integrity**:
    - The foreign key constraints enforce referential integrity by automatically cascading updates to related records when a student or course data is modified and restricting deletions of courses that have active enrollments.

4. **Data Constraints**:
    - `NOT NULL` ensures all critical fields are required, preventing null values which could lead to incomplete data.
  
5. **Storage Engine**:
    - The tables use the InnoDB storage engine, known for its support of transactions and foreign keys, making it suitable for complex relational databases.

### Conclusion

The schema effectively captures and manages the relationships between students, courses, and enrollments in an educational context, providing a robust foundation for reporting, analysis, and operational tasks related to student management and course enrollment tracking.

### Ejemplo tienda online
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código HTML es una representación visual del modelo entidad-relación (ER) para un sistema de gestión de tiendas en línea. La página web utiliza CSS personalizado para dibujar diferentes elementos como entidades, atributos y relaciones entre estas entidades.

El contenido principal está dentro de la etiqueta `<div class="page">`, que contiene varios bloques de clase `shape entity`. Cada uno de estos bloques representa una entidad del modelo ER. Por ejemplo:

- **Cliente**: tiene los atributos `id`, `nombre` y `apellidos`.
- **Producto**: incluye los atributos `id`, `nombre` y `precio`.
- **Pedido**: contiene los atributos `id`, `fecha` y `cliente_id`.
- **LineasPedido**: posee los atributos `id`, `fecha`, `pedido_id`, `producto_id` y `cantidad`.

Además de las entidades, el código también muestra flechas (`<div class="arrow">`) que representan las relaciones entre estas entidades. Por ejemplo, una relación entre la entidad "Cliente" y "Pedido", indicando que un cliente puede realizar varios pedidos.

Este tipo de visualización es útil para estudiantes que están aprendiendo a convertir diagramas ER en modelos relacionales de base de datos, ya que proporciona una representación gráfica clara de las entidades y sus relaciones.

`002-Ejemplo tienda online.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 817.0250244140622px;
  height: 364.4375101725259px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:40px;top:40.01249186197916px;width:219.99997965494785px;height:126.40000406901038px;">
  <div class="entity-header">Cliente</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:294.3500162760416px;top:198.03750610351554px;width:220.0000406901041px;height:126.40000406901038px;">
  <div class="entity-header">Producto</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">precio</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:289.68749999999994px;top:40px;width:220.0000406901041px;height:126.40000406901038px;">
  <div class="entity-header">Pedido</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">fecha</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">cliente_id</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:557.0250244140623px;top:98.68749999999997px;width:219.99999999999994px;height:174.40000406901038px;">
  <div class="entity-header">LineasPedido</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">fecha</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">pedido_id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">producto_id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">cantidad</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="arrow" style="left:198.0874837239583px;top:83.75626504799169px;width:158.3192541290471px;transform:rotate(0.29018599833141073rad);"></div>
<div class="arrow" style="left:449.5750325520832px;top:85.23010972011733px;width:189.76541503267325px;transform:rotate(0.5614093769739965rad);"></div>
<div class="arrow" style="left:449.0625406901041px;top:239.7141575120908px;width:163.21856458957456px;transform:rotate(-0.1593772092056784rad);"></div>
</div>
</body>
</html>
```

### Ejemplo tienda online
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código JSON describe una representación de un diagrama de entidades relacionales, similar a la vista anterior en formato HTML. Sin embargo, el formato y la estructura han cambiado significativamente.

### Descripción del Código Actual

1. **Entidades**:
   - Hay cuatro entidades definidas con sus respectivos atributos:
     1. `Cliente` con atributos: `id`, `nombre`, `apellidos`.
     2. `Producto` con atributos: `id`, `nombre`, `precio`.
     3. `Pedido` con atributos: `id`, `fecha`, `cliente_id`.
     4. `LineasPedido` con atributos: `id`, `fecha`, `pedido_id`, `producto_id`, `cantidad`.

2. **Relaciones**:
   - Se definen tres relaciones entre las entidades:
     - Una relación entre `Cliente` y `Pedido` basada en el atributo `cliente_id`.
     - Una relación entre `Pedido` y `LineasPedido` basada en el atributo `pedido_id`.
     - Una relación entre `Producto` y `LineasPedido` basada en el atributo `producto_id`.

### Comparación con el Código HTML Anterior

- **Estructura**: El código JSON ahora presenta una estructura más simplificada, donde cada entidad se define por un objeto separado. Las relaciones también están definidas de manera clara y directa.
  
- **Posicionamiento**:
  - En el código anterior, las posiciones eran especificadas en píxeles (`left`, `top`) dentro del HTML para dibujar las entidades en una interfaz gráfica.
  - En este JSON, se proporcionan los valores de posicionamiento como cadenas sin unidades (por ejemplo: `"left": "34.0792px"`, pero sin la unidad en el JSON).
  
- **Relaciones**:
  - En HTML, las relaciones eran dibujadas mediante elementos `<div>` con transformaciones CSS.
  - Ahora, las relaciones están definidas como objetos en un array `flechas` con detalles sobre desde dónde empieza y hasta dónde termina cada relación.

### Ejemplo de Uso del JSON

Este formato JSON podría ser utilizado por una herramienta de modelado de bases de datos o una aplicación web que genera diagramas a partir de definiciones en JSON. Por ejemplo, un script JavaScript puede leer este archivo JSON y renderizar el diagrama en un navegador web, creando elementos HTML dinámicamente basándose en los datos proporcionados.

### Ejemplo de Renderizado

Para entender cómo se podría visualizar esto:

- **Cliente** (id: 34.0792px, top: 135.625px)
- **Producto** (id: 288.433px, top: 293.654px)
- **Pedido** (id: 283.771px, top: 135.621px)
- **LineasPedido** (id: 551.104px, top: 194.308px)

Y las líneas entre ellas se dibujarían basándose en las propiedades de cada entidad y sus relaciones.

### Conclusión

El formato JSON proporciona una representación más estructurada y lógica del diagrama, simplificando el proceso de renderizado y manipulación.

`002-Ejemplo tienda online.json`

```json
{
  "formas": [
    {
      "id": "forma-1",
      "tipo": "entity",
      "left": "34.0792px",
      "top": "135.625px",
      "width": "",
      "height": "",
      "entityName": "Cliente",
      "properties": [
        {
          "id": "prop-1",
          "name": "id"
        },
        {
          "id": "prop-2",
          "name": "nombre"
        },
        {
          "id": "prop-3",
          "name": "apellidos"
        }
      ]
    },
    {
      "id": "forma-2",
      "tipo": "entity",
      "left": "288.433px",
      "top": "293.654px",
      "width": "",
      "height": "",
      "entityName": "Producto",
      "properties": [
        {
          "id": "prop-4",
          "name": "id"
        },
        {
          "id": "prop-5",
          "name": "nombre"
        },
        {
          "id": "prop-6",
          "name": "precio"
        }
      ]
    },
    {
      "id": "forma-3",
      "tipo": "entity",
      "left": "283.771px",
      "top": "135.621px",
      "width": "",
      "height": "",
      "entityName": "Pedido",
      "properties": [
        {
          "id": "prop-7",
          "name": "id"
        },
        {
          "id": "prop-8",
          "name": "fecha"
        },
        {
          "id": "prop-9",
          "name": "cliente_id"
        }
      ]
    },
    {
      "id": "forma-5",
      "tipo": "entity",
      "left": "551.104px",
      "top": "194.308px",
      "width": "",
      "height": "",
      "entityName": "LineasPedido",
      "properties": [
        {
          "id": "prop-14",
          "name": "id"
        },
        {
          "id": "prop-15",
          "name": "fecha"
        },
        {
          "id": "prop-16",
          "name": "pedido_id"
        },
        {
          "id": "prop-17",
          "name": "producto_id"
        },
        {
          "id": "prop-18",
          "name": "cantidad"
        }
      ]
    }
  ],
  "flechas": [
    {
      "desde": {
        "shapeId": "forma-1",
        "propId": "prop-1",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-3",
        "propId": "prop-9",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-3",
        "propId": "prop-7",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-5",
        "propId": "prop-16",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-2",
        "propId": "prop-4",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-5",
        "propId": "prop-17",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    }
  ]
}
```

### Ejemplo tienda online
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este archivo SVG representa gráficamente un diagrama entidad-relación (ER) para una tienda en línea, mostrando las entidades y sus propiedades, así como las relaciones entre ellas. En el código, se utilizan rectángulos para representar las entidades, cada uno con líneas horizontales que indican las propiedades de la entidad respectiva. Las etiquetas dentro del rectángulo describen los nombres de estas entidades y sus atributos (como "id", "nombre", etc.). Además, se incluyen flechas que conectan diferentes entidades para representar las relaciones entre ellas.

Las entidades presentes en el diagrama son Cliente, Producto, Pedido, y LineasPedido. Cada entidad tiene asociadas propiedades específicas como identificadores únicos (IDs), nombres, fechas y referencias a otras entidades (como cliente_id o pedido_id). Las flechas con punta de flecha conectan los atributos que forman parte de estas relaciones, mostrando cómo un pedido está relacionado con el cliente que lo hizo y también con las líneas del pedido asociadas al mismo.

ÚLTIMO PÁRRAFO:
En comparación con la versión anterior (002-Ejemplo tienda online.json), este archivo presenta una representación gráfica visual del diagrama ER en lugar de datos estructurados. Mientras que el archivo JSON detalla las entidades y sus relaciones mediante texto estructurado, el SVG ofrece una vista más intuitiva del modelo relacional a través de formas geométricas y líneas confeccionadas para indicar las relaciones entre diferentes elementos del sistema. Esto facilita la comprensión visual del diseño de la base de datos.

`002-Ejemplo tienda online.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="817.0250244140622" height="364.4375101725259" viewBox="0 0 817.0250244140622 364.4375101725259">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="40" y="40.01249186197916" width="219.99997965494785" height="126.40000406901038" />
<line x1="40" y1="66.41249847412108" x2="259.9999796549479" y2="66.41249847412108" stroke="#e5e7eb" stroke-width="1"/>
<text x="149.99998982747394" y="58.01249821980793" text-anchor="middle">Cliente</text>
<text x="123.89998372395831" y="86.41249593098956">id</text>
<text x="123.89998372395831" y="110.41249593098956">nombre</text>
<text x="123.89998372395831" y="134.4125061035156">apellidos</text>
<rect class="shape-entity" x="294.3500162760416" y="198.03750610351554" width="220.0000406901041" height="126.40000406901038" />
<line x1="294.3500162760416" y1="224.43750254313144" x2="514.3500569661456" y2="224.43750254313144" stroke="#e5e7eb" stroke-width="1"/>
<text x="404.35003662109364" y="216.0375022888183" text-anchor="middle">Producto</text>
<text x="381.6249999999999" y="244.4374898274739">id</text>
<text x="381.6249999999999" y="268.4374898274739">nombre</text>
<text x="381.6249999999999" y="292.437510172526">precio</text>
<rect class="shape-entity" x="289.68749999999994" y="40" width="220.0000406901041" height="126.40000406901038" />
<line x1="289.68749999999994" y1="66.39999643961586" x2="509.687540690104" y2="66.39999643961586" stroke="#e5e7eb" stroke-width="1"/>
<text x="399.687520345052" y="57.99999618530271" text-anchor="middle">Pedido</text>
<text x="371.7875162760416" y="86.39999389648435">id</text>
<text x="371.7875162760416" y="110.39999389648435">fecha</text>
<text x="371.7875162760416" y="134.39999389648435">cliente_id</text>
<rect class="shape-entity" x="557.0250244140623" y="98.68749999999997" width="219.99999999999994" height="174.40000406901038" />
<line x1="557.0250244140623" y1="125.0875066121419" x2="777.0250244140623" y2="125.0875066121419" stroke="#e5e7eb" stroke-width="1"/>
<text x="667.0250244140623" y="116.68750635782874" text-anchor="middle">LineasPedido</text>
<text x="632.2125244140623" y="145.08749389648435">id</text>
<text x="632.2125244140623" y="169.08749389648432">fecha</text>
<text x="632.2125244140623" y="193.08749389648435">pedido_id</text>
<text x="632.2125244140623" y="217.0874938964843">producto_id</text>
<text x="632.2125244140623" y="241.0874938964843">cantidad</text>
<path class="conn" d="M 198.0874837239583 83.75626504799169 L 349.7875162760416 129.05622477948222" marker-end="url(#arrow-end)" />
<path class="conn" d="M 449.5750325520832 85.23010972011733 L 610.2125244140623 186.25737807285137" marker-end="url(#arrow-end)" />
<path class="conn" d="M 449.0625406901041 239.7141575120908 L 610.2125244140623 213.8108262118674" marker-end="url(#arrow-end)" />
</svg>
```

### ejemplo tienda online convertido a SQL
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL se encarga de crear las tablas necesarias para una base de datos que modela una tienda online. Las tablas principales son `Cliente`, `Producto` y `Pedido`. También incluye la tabla `LineasPedido`, que es crucial para relacionar los pedidos con los productos y especificar detalles como la cantidad comprada.

1. **Tabla Cliente**: Almacena información básica sobre cada cliente, incluyendo un identificador único (`id`), su nombre y apellidos. Esta tabla es fundamental ya que cada pedido está asociado a un cliente específico.

2. **Tabla Producto**: Registra los productos disponibles en la tienda con campos como el `id`, `nombre` y `precio`. Es importante para conocer qué artículos se pueden comprar y a cuánto ascienden.

3. **Tabla Pedido**: Este esquema registra cada pedido realizado por un cliente, identificando el día (`fecha`) del pedido y vinculándolo al cliente mediante la columna `cliente_id`, que hace referencia a la tabla `Cliente`. Esta relación asegura que cada pedido esté siempre asociado con un cliente válido.

4. **Tabla LineasPedido**: Permite detallar los productos incluidos en cada pedido junto con el número de unidades compradas (`cantidad`). Está conectada tanto con la tabla `Producto` como con `Pedido`, lo cual es crucial para mantener una trazabilidad precisa del inventario y las ventas.

El uso de claves foráneas (FOREIGN KEY) asegura que los datos estén consistentemente vinculados entre tablas, por ejemplo, si un cliente se elimina pero tiene pedidos existentes. Las opciones `ON UPDATE CASCADE` y `ON DELETE RESTRICT` definen qué ocurre con las relaciones cuando se modifican o eliminan registros en estas tablas.

Esta estructura es importante para el funcionamiento de una tienda online porque permite gestionar eficazmente los datos del cliente, los productos disponibles, así como los pedidos realizados y sus detalles específicos.

`003-ejemplo tienda online convertido a SQL.sql`

```sql
-- Seleccionar base de datos (opcional)
-- CREATE DATABASE tienda;
-- USE tienda;

-- Tabla Cliente
CREATE TABLE Cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre    VARCHAR(100) NOT NULL,
    apellidos VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

-- Tabla Producto
CREATE TABLE Producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    precio DECIMAL(10,2) NOT NULL
) ENGINE=InnoDB;

-- Tabla Pedido
CREATE TABLE Pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    cliente_id INT NOT NULL,
    CONSTRAINT fk_pedido_cliente
        FOREIGN KEY (cliente_id)
        REFERENCES Cliente(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Tabla LineasPedido
CREATE TABLE LineasPedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    pedido_id   INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    CONSTRAINT fk_linea_pedido
        FOREIGN KEY (pedido_id)
        REFERENCES Pedido(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_linea_producto
        FOREIGN KEY (producto_id)
        REFERENCES Producto(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;
```

### Ejemplo centro de formacion con relacion de n a n
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código HTML está diseñado para representar visualmente una parte del modelo relacional de una base de datos, específicamente un diagrama entidad-relación (ER) simplificado. El código define estilos CSS que crean formas y elementos gráficos necesarios para dibujar entidades y relaciones en el diagrama ER.

El archivo contiene tres secciones principales:

1. **Estilo CSS**: Define las reglas de estilo para los diferentes componentes del diagrama, como la forma de una entidad (rectángulo), propiedades de entidades (como nombres y descripciones), y líneas que representan relaciones entre entidades.

2. **HTML estructura**: Crea elementos HTML que utilizan estas clases CSS para dibujar el diagrama ER. Por ejemplo, hay tres divs con la clase `shape entity`, cada uno representando una entidad diferente (Asignatura, Alumno y Matricula). Dentro de estos divs, se definen las propiedades de cada entidad utilizando elementos `<div>` con la clase `entity-property`.

3. **Relaciones entre entidades**: El código incluye dos líneas rectas dibujadas mediante el uso del elemento `arrow` en CSS para representar relaciones entre las entidades Alumno y Matricula, así como entre Asignatura y Matricula.

Este diagrama es útil porque proporciona una representación visual de cómo se relacionan diferentes partes (entidades) de un sistema de base de datos. En este caso específico, el centro de formación está modelado con tres entidades principales: Alumnos, Asignaturas y Matrículas que conectan a los Alumnos con las Asignaturas en la que están inscritos.

`004-Ejemplo centro de formacion con relacion de n a n.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 580.6249346051897px;
  height: 378.11249869210377px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:40.037493024553584px;top:211.7125047956194px;width:219.99999999999994px;height:126.39999389648435px;">
  <div class="entity-header">Asignatura</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">descripcion</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:40px;top:40px;width:219.99999999999994px;height:150.4000091552734px;">
  <div class="entity-header">Alumno</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">email</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:320.62499999999994px;top:105.62498910086494px;width:219.99993460518968px;height:150.3999873570033px;">
  <div class="entity-header">Matricula</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">fecha</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">alumno_id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">asignatura_id</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="arrow" style="left:204.98746190752297px;top:253.22919475689145px;width:167.80459429011117px;transform:rotate(-0.1938217844790185rad);"></div>
<div class="arrow" style="left:198.08748109000067px;top:85.23177439821053px;width:202.70510380894262px;transform:rotate(0.5616736837541834rad);"></div>
</div>
</body>
</html>
```

### Ejemplo centro de formacion con relacion de n a n
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código en formato JSON representa la estructura de un diagrama entidad-relación (ER) simplificado para una base de datos del centro de formación. En este caso, el archivo contiene información sobre tres entidades y las relaciones entre ellas.

Las entidades son "Asignatura", "Alumno" y "Matricula". Cada entidad tiene propiedades asociadas: por ejemplo, la entidad "Asignatura" tiene propiedades como id, nombre y descripción. La entidad "Alumno" incluye propiedades de identificación personal y contacto (id, nombre, apellidos, email), mientras que la entidad "Matricula" maneja detalles sobre las matrículas en el centro educativo, con campos tales como id, fecha, alumno_id y asignatura_id.

Además del detalle de entidades y sus propiedades, el archivo JSON también incluye información sobre las relaciones entre estas entidades. Por ejemplo, hay flechas que conectan "Asignatura" con "Matricula" a través del campo asignatura_id, y otra flecha que conecta "Alumno" con "Matricula" usando alumno_id.

Este tipo de representación JSON es útil para describir gráficos complejos como los diagramas ER de manera estructurada y fácilmente procesable por programas informáticos. Es importante en el proceso de modelado de bases de datos ya que permite una fácil conversión entre formatos visuales y formatos de texto.

En cuanto a las diferencias con respecto al código anterior, este archivo JSON presenta la misma información pero estructurada de manera diferente. En lugar de un HTML completo, se utiliza un formato de datos que es más compacto y fácil para programas automatizados de procesamiento de bases de datos. Esto facilita el uso en herramientas de modelado de bases de datos donde los diagramas pueden ser generados automáticamente desde esta estructura JSON.

Por lo tanto, este cambio en la representación del mismo conjunto de entidades y relaciones simplifica la manipulación y comprensión por parte de sistemas informáticos.

`004-Ejemplo centro de formacion con relacion de n a n.json`

```json
{
  "formas": [
    {
      "id": "forma-1",
      "tipo": "entity",
      "left": "216.375px",
      "top": "268.825px",
      "width": "",
      "height": "",
      "entityName": "Asignatura",
      "properties": [
        {
          "id": "prop-1",
          "name": "id"
        },
        {
          "id": "prop-2",
          "name": "nombre"
        },
        {
          "id": "prop-3",
          "name": "descripcion"
        }
      ]
    },
    {
      "id": "forma-2",
      "tipo": "entity",
      "left": "216.338px",
      "top": "97.1125px",
      "width": "",
      "height": "",
      "entityName": "Alumno",
      "properties": [
        {
          "id": "prop-4",
          "name": "id"
        },
        {
          "id": "prop-5",
          "name": "nombre"
        },
        {
          "id": "prop-6",
          "name": "apellidos"
        },
        {
          "id": "prop-7",
          "name": "email"
        }
      ]
    },
    {
      "id": "forma-3",
      "tipo": "entity",
      "left": "496.963px",
      "top": "162.738px",
      "width": "",
      "height": "",
      "entityName": "Matricula",
      "properties": [
        {
          "id": "prop-8",
          "name": "id"
        },
        {
          "id": "prop-9",
          "name": "fecha"
        },
        {
          "id": "prop-10",
          "name": "alumno_id"
        },
        {
          "id": "prop-11",
          "name": "asignatura_id"
        }
      ]
    }
  ],
  "flechas": [
    {
      "desde": {
        "shapeId": "forma-1",
        "propId": "prop-1",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-3",
        "propId": "prop-11",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-2",
        "propId": "prop-4",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-3",
        "propId": "prop-10",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    }
  ]
}
```

### Ejemplo centro de formacion con relacion de n a n
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este archivo SVG representa un diagrama de entidad-relación (ER) visualizado gráficamente, donde cada entidad es representada por rectángulos y las relaciones entre entidades son mostradas mediante líneas con flechas. En este caso, el diagrama incluye tres entidades principales: "Asignatura", "Alumno" y "Matricula". Cada entidad tiene sus propias propiedades (atributos) que se detallan dentro del rectángulo correspondiente.

La entidad "Asignatura" contiene los atributos "id", "nombre" y "descripcion". La entidad "Alumno" incluye los atributos "id", "nombre", "apellidos" y "email". Por último, la entidad "Matricula" tiene sus propios atributos: "id", "fecha", "alumno_id" y "asignatura_id". Estos últimos dos atributos son cruciales ya que establecen las relaciones entre la entidad Matricula y las entidades Alumno y Asignatura respectivamente.

El archivo SVG también incluye flechas que conectan las entidades para mostrar estas relaciones. Por ejemplo, una línea con una flecha apunta desde "Alumno" hasta "Matricula", indicando que un alumno puede estar matriculado en múltiples asignaturas, mientras que otra flecha apunta desde "Asignatura" a "Matricula", mostrando que cada asignatura puede tener varios alumnos inscritos. Estas relaciones son cruciales para comprender cómo se estructura la información en el modelo relacional.

**ÚLTIMO PÁRRAFO:**
Este archivo SVG es una representación visual gráfica del diagrama ER basado en los datos JSON proporcionados anteriormente, lo que permite una mejor comprensión visual de las entidades y sus relaciones. La adición de estilos específicos para cada elemento (rectángulos, flechas) mejora la legibilidad y claridad del diagrama, facilitando así el paso al modelo relacional en SQL o otras implementaciones basadas en bases de datos.

`004-Ejemplo centro de formacion con relacion de n a n.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="580.6249346051897" height="378.11249869210377" viewBox="0 0 580.6249346051897 378.11249869210377">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="40.037493024553584" y="211.7125047956194" width="219.99999999999994" height="126.39999389648435" />
<line x1="40.037493024553584" y1="238.11247689383367" x2="260.03749302455356" y2="238.11247689383367" stroke="#e5e7eb" stroke-width="1"/>
<text x="150.03749302455356" y="229.7124873570033" text-anchor="middle">Asignatura</text>
<text x="117.0749947684152" y="258.1124943324497">id</text>
<text x="117.0749947684152" y="282.1124768938337">nombre</text>
<text x="117.0749947684152" y="306.11248125348766">descripcion</text>
<rect class="shape-entity" x="40" y="40" width="219.99999999999994" height="150.4000091552734" />
<line x1="40" y1="66.3999911717006" x2="259.99999999999994" y2="66.3999911717006" stroke="#e5e7eb" stroke-width="1"/>
<text x="149.99999999999997" y="57.99999209812709" text-anchor="middle">Alumno</text>
<text x="123.89998953683033" y="86.39999839237757">id</text>
<text x="123.89998953683033" y="110.40000683920724">nombre</text>
<text x="123.89998953683033" y="134.3999873570033">apellidos</text>
<text x="123.89998953683033" y="158.39999171665733">email</text>
<rect class="shape-entity" x="320.62499999999994" y="105.62498910086494" width="219.99993460518968" height="150.3999873570033" />
<line x1="320.62499999999994" y1="132.02499662126812" x2="540.6249346051897" y2="132.02499662126812" stroke="#e5e7eb" stroke-width="1"/>
<text x="430.62496730259477" y="123.62498937334333" text-anchor="middle">Matricula</text>
<text x="391.6499720982142" y="152.02500043596535">id</text>
<text x="391.6499720982142" y="176.0250047956194">fecha</text>
<text x="391.6499720982142" y="200.02498735700334">alumno_id</text>
<text x="391.6499720982142" y="224.0249828611101">asignatura_id</text>
<path class="conn" d="M 204.98746190752297 253.22919475689145 L 369.64996337890614 220.90826540676994" marker-end="url(#arrow-end)" />
<path class="conn" d="M 198.08748109000067 85.23177439821053 L 369.64996337890614 193.19322020671757" marker-end="url(#arrow-end)" />
</svg>
```

### caso centrode formacion en sql
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código SQL está creando tres tablas en una base de datos que representan diferentes aspectos del sistema educativo, como alumnos, asignaturas y matrículas. Cada tabla tiene sus propias características:

1. La tabla `Alumno` almacena información sobre los estudiantes, incluyendo un identificador único (`id`), su nombre, apellidos y correo electrónico. El campo `id` es de tipo autoincremental, lo que significa que cada vez que se inserta un nuevo registro en la tabla, el valor del id aumentará automáticamente.

2. La tabla `Asignatura` contiene detalles sobre las asignaturas ofrecidas por una institución educativa, con campos para identificarla (`id`), su nombre y una descripción opcional (`descripcion`). Igual que en la tabla `Alumno`, el campo `id` es de tipo autoincremental.

3. La tabla `Matricula` representa las matrículas de los estudiantes en diferentes asignaturas. Esta tabla incluye un identificador único, la fecha de matriculación, y dos campos relacionados con las tablas `Alumno` e `Asignatura`. Estos campos (`alumno_id` y `asignatura_id`) son claves foráneas (foreign keys) que crean una relación entre las diferentes tablas.

Las restricciones de clave foránea garantizan la integridad referencial en la base de datos. Por ejemplo, cuando se elimina un registro de la tabla `Alumno`, debido a `ON DELETE CASCADE` en la tabla `Matricula`, todos los registros relacionados con ese alumno también serán eliminados automáticamente para evitar referencias inconsistentes.

Esta estructura es importante porque permite gestionar de manera eficiente y organizada toda la información sobre estudiantes, asignaturas y matrículas, manteniendo las relaciones entre estos datos correctamente.

`005-caso centrode formacion en sql.sql`

```sql
-- Tabla Alumno
CREATE TABLE Alumno (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,
    apellidos  VARCHAR(150) NOT NULL,
    email      VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

-- Tabla Asignatura
CREATE TABLE Asignatura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre       VARCHAR(150) NOT NULL,
    descripcion  TEXT
) ENGINE=InnoDB;

-- Tabla Matricula
CREATE TABLE Matricula (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    alumno_id INT NOT NULL,
    asignatura_id INT NOT NULL,

    CONSTRAINT fk_matricula_alumno
        FOREIGN KEY (alumno_id)
        REFERENCES Alumno(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_matricula_asignatura
        FOREIGN KEY (asignatura_id)
        REFERENCES Asignatura(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;
```

### Actividades propuestas

Based on the provided files, it appears that you have a complete set of artifacts for modeling and creating a relational database schema for a "Centro de Formación" (Training Center). Here's an overview of what each file contains:

1. **004-CentroFormacion.md**:
   - This Markdown file likely serves as documentation or notes about the Centro de Formación project.
   
2. **003-Diagrama.png**:
   - A visual diagram (likely created using a tool like Lucidchart, draw.io, or similar) depicting the database schema for the Centro de Formación. The diagram typically shows entities and their relationships.

3. **001-CentroFormacion.sql** and **002-CentroFormacionER.png**:
   - These files are not directly mentioned in your text but seem to be related to an earlier version of the schema or a different approach to modeling the same system. It's possible that `002-CentroFormacionER.png` is an Entity-Relationship (ER) diagram and `001-CentroFormacion.sql` contains SQL scripts for creating the database tables.

4. **005-caso centrode formacion en sql.sql**:
   - This file contains SQL statements to create three core tables (`Alumno`, `Asignatura`, and `Matricula`) along with necessary foreign key constraints.
   
### Summary of Provided SQL Schema

The provided SQL schema in the `005-caso centrode formacion en sql.sql` file defines:

- **Table: Alumno**
  - Primary Key: `id`
  - Fields:
    - `nombre`: VARCHAR(100) (not nullable)
    - `apellidos`: VARCHAR(150) (not nullable)
    - `email`: VARCHAR(150) (not nullable)

- **Table: Asignatura**
  - Primary Key: `id`
  - Fields:
    - `nombre`: VARCHAR(150) (not nullable)
    - `descripcion`: TEXT

- **Table: Matricula**
  - Primary Key: `id`
  - Fields:
    - `fecha`: DATE (not nullable)
    - Foreign Keys:
      - `alumno_id` references `Alumno(id)`
      - `asignatura_id` references `Asignatura(id)`

### Key Points from the SQL Script

- **Foreign Key Constraints**:
  - The `Matricula` table has foreign key constraints that reference `Alumno.id` and `Asignatura.id`.
    - When an `alumno_id` is deleted in `Alumno`, it will also be cascaded to delete related entries in `Matricula` (ON DELETE CASCADE).
    - When an `asignatura_id` is updated or deleted, the constraint prevents deletion but allows updates (ON UPDATE CASCADE/RESTRICT).

- **Table Engine**:
  - All tables use InnoDB engine, which supports foreign keys and transactions.

### Diagram Analysis

The diagram in `003-Diagrama.png` should depict these relationships visually:
- An `Alumno` can have multiple `Matricula`.
- A `Asignatura` can be associated with multiple `Matricula`.

If you need to create the database based on this schema, you would typically run the SQL script in a MySQL or MariaDB environment.

### Next Steps

1. **Review the Diagram**: Ensure that the ER diagram (`002-CentroFormacionER.png`) and the provided entities match the requirements of your project.
2. **SQL Validation**: Validate the SQL schema to ensure it meets all functional requirements, such as data integrity, performance considerations, etc.
3. **Database Creation**:
   - Create a new database in MySQL/MariaDB.
   - Use the `CREATE TABLE` statements from `005-caso centrode formacion en sql.sql`.
4. **Testing**: Insert test data and run queries to ensure that relationships and constraints work as expected.

Would you like any specific modifications or additional features for this schema?


<a id="restricciones-semanticas-del-modelo-relacional"></a>
## Restricciones semánticas del modelo relacional

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/006-Interpretaci%C3%B3n%20de%20Diagramas%20EntidadRelaci%C3%B3n/004-Restricciones%20sem%C3%A1nticas%20del%20modelo%20relacional)


<a id="normalizacion-de-modelos-relacionales"></a>
## Normalización de modelos relacionales

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/006-Interpretaci%C3%B3n%20de%20Diagramas%20EntidadRelaci%C3%B3n/005-Normalizaci%C3%B3n%20de%20modelos%20relacionales)

### Introducción a los ejercicios

Esta carpeta contiene una serie de ejercicios diseñados para ayudarte a entender y aplicar la normalización en bases de datos. La normalización es un conjunto de reglas o "recetas" que te permiten organizar tus bases de datos de manera eficiente, asegurando que sean escalables y mantenibles con el tiempo. Los ejercicios abordan desde los conceptos básicos hasta la tercera forma normal (3FN), incluyendo términos clave como la primera (1FN) y segunda formas normales (2FN). A través de estos problemas, practicarás cómo eliminar redundancias y dependencias parciales e intransitivas para mejorar la calidad estructural de tus bases de datos.

### Actividades propuestas

### Actividad 1: Comprender los Principios Básicos de la Normalización

**Descripción:** Los estudiantes deben leer y resumir las definiciones y conceptos básicos de la normalización en bases de datos según los archivos proporcionados. El objetivo es que comprendan por qué es importante normalizar una base de datos para asegurar su escalabilidad y mantenibilidad a largo plazo.

### Actividad 2: Identificar Atributos Atómicos

**Descripción:** Los alumnos deben analizar ejemplos de tablas y determinar cuáles atributos son atómicos, según la Primera Forma Normal. Se busca que los estudiantes identifiquen cuando un atributo está compuesto de elementos simples e indivisibles.

### Actividad 3: Aplicación de la Segunda Forma Normal

**Descripción:** Los alumnos deben aplicar el concepto de dependencia funcional completa para determinar si una tabla cumple con la Segunda Forma Normal. Se espera que los estudiantes sean capaces de identificar y corregir las dependencias parciales.

### Actividad 4: Análisis de Dependencias Transitivas

**Descripción:** Los alumnos deben analizar ejemplos y aplicar el concepto de dependencia transitiva para determinar si una tabla cumple con la Tercera Forma Normal. Se busca que identifiquen las condiciones en las que no se cumplen los requisitos de 3FN.

### Actividad 5: Diseño de Tablas Normalizadas

**Descripción:** Los estudiantes deben diseñar tablas para un conjunto de datos dado, asegurando que cumplan con la Primera, Segunda y Tercera Forma Normal. Se busca que apliquen en práctica los conceptos aprendidos sobre normalización.

### Actividad 6: Resolución de Ejemplos Prácticos

**Descripción:** Los alumnos deben resolver ejemplos prácticos proporcionados, aplicando las reglas de la normalización para corregir problemas de diseño en esquemas de bases de datos. Se busca mejorar su capacidad para detectar y corregir anomalías en los diseños.

### Actividad 7: Identificación de Claves Primarias

**Descripción:** Los estudiantes deben identificar claves primarias y candidatas, además de clasificar atributos como clave externa o alternativa en diferentes esquemas de base de datos. Se busca que comprendan la importancia de estas definiciones para el diseño correcto.

### Actividad 8: Descripción Detallada del Proceso de Normalización

**Descripción:** Los alumnos deben describir, paso a paso, cómo se normaliza un esquema de base de datos desde una forma no-normalizada hasta la Tercera Forma Normal. Se busca que justifiquen cada uno de los pasos y decisiones tomados en el proceso.

### Actividad 9: Evaluación de Casos Prácticos

**Descripción:** Los estudiantes deben evaluar diferentes casos prácticos proporcionados, aplicando criterios de normalización para mejorar diseños existentes. Se busca que apliquen conceptos a la resolución de problemas reales.

### Actividad 10: Creación de Guías Tutoriales

**Descripción:** Finalmente, los alumnos deben crear guías o tutoriales sencillos sobre cómo aplicar las reglas de normalización para un diseño óptimo de base de datos. Se busca que puedan explicar conceptos complejos a sus compañeros en términos simples y prácticos.


<a id="ejercicios"></a>
## Ejercicios

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/006-Interpretaci%C3%B3n%20de%20Diagramas%20EntidadRelaci%C3%B3n/101-Ejercicios)


<a id="criterios-de-evaluacion"></a>
## Criterios de evaluación

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/006-Interpretaci%C3%B3n%20de%20Diagramas%20EntidadRelaci%C3%B3n/201-Criterios%20de%20evaluaci%C3%B3n)


<a id="resumen"></a>
## Resumen

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/006-Interpretaci%C3%B3n%20de%20Diagramas%20EntidadRelaci%C3%B3n/301-Resumen)



<a id="uso-de-bases-de-datos-no-relacionales"></a>
# Uso de bases de datos no relacionales

<a id="caracteristicas-de-las-bases-de-datos-no-relacionales"></a>
## Características de las bases de datos no relacionales

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/007-Uso%20de%20bases%20de%20datos%20no%20relacionales/001-Caracter%C3%ADsticas%20de%20las%20bases%20de%20datos%20no%20relacionales)


<a id="tipos-de-bases-de-datos-no-relacionales"></a>
## Tipos de bases de datos no relacionales

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/007-Uso%20de%20bases%20de%20datos%20no%20relacionales/002-Tipos%20de%20bases%20de%20datos%20no%20relacionales)

### ejemplo json 1
<small>Creado: 2026-01-19 16:28</small>

`002-ejemplo json 1.json`

```json
{
  "nombre":"Jose Vicente",
  "apellidos":"Carratala Sanchis",
  "email":"info@jocarsa.com"
}
```

### json un poco mas complejo
<small>Creado: 2026-01-19 16:28</small>

`003-json un poco mas complejo.json`

```json
{
  "nombre":"Jose Vicente",
  "apellidos":"Carratala Sanchis",
  "email":"info@jocarsa.com",
  "telefonos":[
    "12345678",
    "87654321"
  ]
}
```

### json mas complejo todavía
<small>Creado: 2026-01-19 16:28</small>

`004-json mas complejo todavía.json`

```json
{
  "nombre":"Jose Vicente",
  "apellidos":"Carratala Sanchis",
  "email":"info@jocarsa.com",
  "telefonos":{
    "trabajo":[
      123445,
      325435
    ],
    "personal":[
      21423423,
      6245324534
    ]
  }
}
```

### ejemplo pedido tienda online
<small>Creado: 2026-01-19 16:28</small>

`006-ejemplo pedido tienda online.json`

```json
{
  "cliente":{
    "nombre":"fdsafsdf",
    "apellidos":"fdsfasdfs"
  },
  "productos":[
    {"nombre":"fdsfsdf","cantidad":3,"precio":43},
    {"nombre":"fdsfsdf","cantidad":3,"precio":43},
    {"nombre":"fdsfsdf","cantidad":3,"precio":43},
    {"nombre":"fdsfsdf","cantidad":3,"precio":43}
  ]
}
```


<a id="elementos-de-las-bases-de-datos-no-relacionales"></a>
## Elementos de las bases de datos no relacionales

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/007-Uso%20de%20bases%20de%20datos%20no%20relacionales/003-Elementos%20de%20las%20bases%20de%20datos%20no%20relacionales)

### muestra de pedido
<small>Creado: 2026-01-19 16:28</small>

`003-muestra de pedido.json`

```json
{
  "cliente":{
    "nombre":"Jose Vicente",
    "apellidos":"Carratala Sanchis",
    "email":"info@jocarsa.com"
  },
  "pedido":{
    "fecha":"2026-01-08",
    "numero":"2026001"
  },
  "productos":[
    {"nombre":"Camiseta","cantidad":3,"precio":43},
    {"nombre":"Pantalon","cantidad":2,"precio":23},
    {"nombre":"Calcetines","cantidad":3,"precio":33},
    {"nombre":"Bufanda","cantidad":4,"precio":13}
  ]
}
```

### cargamos el primer pedido
<small>Creado: 2026-01-19 16:28</small>

`005-cargamos el primer pedido.php`

```
<?php
// Conexión al servidor MongoDB
$manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");

// Consulta: primer documento (sin filtros, límite 1)
$query = new MongoDB\Driver\Query(
    [],                 // filtro
    ['limit' => 1]      // opciones
);

// Ejecutar consulta
$cursor = $manager->executeQuery('tiendaonline.pedidos', $query);

// Obtener el primer documento
foreach ($cursor as $doc) {
    var_dump($doc);
    break;
}

// Si no hay documentos
if (!isset($doc)) {
    echo "La colección 'pedidos' está vacía\n";
}
```

### pedido tienda online
<small>Creado: 2026-01-19 16:28</small>

`006-pedido tienda online.php`

```
<?php
// factura.php  (PECL mongodb, sin Composer)

function euro($n): string {
    return number_format((float)$n, 2, ',', '.') . " €";
}

$IVA_PCT = 21; // ajusta si procede

try {
    $manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");
    $query = new MongoDB\Driver\Query([], ['limit' => 1]);
    $cursor = $manager->executeQuery('tiendaonline.pedidos', $query);

    $doc = null;
    foreach ($cursor as $d) { $doc = $d; break; }

    if (!$doc) {
        header('Content-Type: text/plain; charset=utf-8');
        echo "No hay pedidos en tiendaonline.pedidos\n";
        exit;
    }

    // Extraer campos con valores por defecto
    $id      = isset($doc->_id) ? (string)$doc->_id : '';
    $cliente = $doc->cliente ?? (object)[];
    $pedido  = $doc->pedido ?? (object)[];
    $items   = $doc->productos ?? [];

    $nombre    = trim(($cliente->nombre ?? '') . ' ' . ($cliente->apellidos ?? ''));
    $email     = $cliente->email ?? '';
    $fecha     = $pedido->fecha ?? '';
    $numero    = $pedido->numero ?? '';

    // Calcular totales
    $base = 0.0;
    foreach ($items as $it) {
        $cant = (int)($it->cantidad ?? 0);
        $precio = (float)($it->precio ?? 0);
        $base += $cant * $precio;
    }
    $iva = $base * ($IVA_PCT / 100.0);
    $total = $base + $iva;

    // Salida HTML sencilla estilo factura
    header('Content-Type: text/html; charset=utf-8');

} catch (Throwable $e) {
    header('Content-Type: text/plain; charset=utf-8');
    echo "ERROR: " . $e->getMessage() . "\n";
    exit;
}
?>
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Factura <?= htmlspecialchars($numero) ?></title>
  <style>
    body{font-family:Arial,Helvetica,sans-serif;background:#f3f3f3;margin:0;padding:24px;}
    .invoice{max-width:900px;margin:0 auto;background:#fff;border:1px solid #ddd;border-radius:12px;overflow:hidden;}
    header{padding:24px;border-bottom:1px solid #eee;display:flex;justify-content:space-between;gap:16px;}
    h1{margin:0;font-size:22px;}
    .muted{color:#666;font-size:13px;line-height:1.4;}
    .box{padding:18px 24px;display:flex;gap:24px;flex-wrap:wrap;}
    .col{min-width:260px;flex:1;}
    table{width:100%;border-collapse:collapse;}
    th,td{padding:12px 10px;border-bottom:1px solid #eee;text-align:left;}
    th{background:#fafafa;font-size:13px;color:#444;}
    td.num, th.num{text-align:right;}
    .totals{padding:18px 24px;display:flex;justify-content:flex-end;}
    .totals table{width:360px;}
    .totals td{border-bottom:none;padding:8px 10px;}
    .totals tr.total td{font-weight:bold;font-size:16px;border-top:1px solid #ddd;padding-top:12px;}
    footer{padding:18px 24px;border-top:1px solid #eee;}
    .badge{display:inline-block;background:#111;color:#fff;border-radius:999px;padding:6px 10px;font-size:12px;}
  </style>
</head>
<body>
  <div class="invoice">
    <header>
      <div>
        <h1>Factura <span class="badge">#<?= htmlspecialchars($numero) ?></span></h1>
        <div class="muted">
          Fecha: <?= htmlspecialchars($fecha) ?><br>
          ID pedido: <?= htmlspecialchars($id) ?>
        </div>
      </div>
      <div class="muted" style="text-align:right;">
        <strong>TiendaOnline</strong><br>
        Ejemplo S.L.<br>
        soporte@tiendaonline.local
      </div>
    </header>

    <section class="box">
      <div class="col">
        <div class="muted"><strong>Facturar a</strong></div>
        <div style="margin-top:6px;">
          <?= htmlspecialchars($nombre ?: '—') ?><br>
          <?= htmlspecialchars($email ?: '') ?>
        </div>
      </div>
      <div class="col">
        <div class="muted"><strong>Detalle del pedido</strong></div>
        <div style="margin-top:6px;">
          Número: <?= htmlspecialchars($numero ?: '—') ?><br>
          Fecha: <?= htmlspecialchars($fecha ?: '—') ?>
        </div>
      </div>
    </section>

    <section style="padding:0 24px 18px 24px;">
      <table>
        <thead>
          <tr>
            <th>Producto</th>
            <th class="num">Cantidad</th>
            <th class="num">Precio</th>
            <th class="num">Subtotal</th>
          </tr>
        </thead>
        <tbody>
        <?php foreach ($items as $it): 
          $pname = (string)($it->nombre ?? '');
          $cant  = (int)($it->cantidad ?? 0);
          $precio= (float)($it->precio ?? 0);
          $sub   = $cant * $precio;
        ?>
          <tr>
            <td><?= htmlspecialchars($pname) ?></td>
            <td class="num"><?= $cant ?></td>
            <td class="num"><?= euro($precio) ?></td>
            <td class="num"><?= euro($sub) ?></td>
          </tr>
        <?php endforeach; ?>
        </tbody>
      </table>
    </section>

    <section class="totals">
      <table>
        <tr>
          <td class="muted">Base imponible</td>
          <td class="num"><?= euro($base) ?></td>
        </tr>
        <tr>
          <td class="muted">IVA (<?= (int)$IVA_PCT ?>%)</td>
          <td class="num"><?= euro($iva) ?></td>
        </tr>
        <tr class="total">
          <td>Total</td>
          <td class="num"><?= euro($total) ?></td>
        </tr>
      </table>
    </section>

    <footer class="muted">
      Gracias por tu compra. Conserva esta factura para tus registros.
    </footer>
  </div>
</body>
</html>
```

### segundo pedido
<small>Creado: 2026-01-19 16:28</small>

`007-segundo pedido.json`

```json
{
  "cliente":{
    "nombre":"Juan",
    "apellidos":"Lopez Garcia",
    "email":"info@juan.com"
  },
  "pedido":{
    "fecha":"2026-01-09",
    "numero":"2026002"
  },
  "productos":[
    {"nombre":"Camiseta","cantidad":3,"precio":43},
    {"nombre":"Pantalon","cantidad":2,"precio":23},
    {"nombre":"Calcetines","cantidad":3,"precio":33},
    {"nombre":"Bufanda","cantidad":4,"precio":13}
  ]
}
```

### segundo pedido
<small>Creado: 2026-01-19 16:28</small>

`007-segundo pedido.php`

```
<?php
// factura.php  (PECL mongodb, sin Composer)

function euro($n): string {
    return number_format((float)$n, 2, ',', '.') . " €";
}

$IVA_PCT = 21; // ajusta si procede

try {
    $manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");
    $query  = new MongoDB\Driver\Query(
    [],
    [
        'sort'  => ['_id' => 1], // importante: orden estable
        'skip'  => 1,
        'limit' => 1
    ]
);
$cursor = $manager->executeQuery('tiendaonline.pedidos', $query);

    $doc = null;
    foreach ($cursor as $d) { $doc = $d; break; }

    if (!$doc) {
        header('Content-Type: text/plain; charset=utf-8');
        echo "No hay pedidos en tiendaonline.pedidos\n";
        exit;
    }

    // Extraer campos con valores por defecto
    $id      = isset($doc->_id) ? (string)$doc->_id : '';
    $cliente = $doc->cliente ?? (object)[];
    $pedido  = $doc->pedido ?? (object)[];
    $items   = $doc->productos ?? [];

    $nombre    = trim(($cliente->nombre ?? '') . ' ' . ($cliente->apellidos ?? ''));
    $email     = $cliente->email ?? '';
    $fecha     = $pedido->fecha ?? '';
    $numero    = $pedido->numero ?? '';

    // Calcular totales
    $base = 0.0;
    foreach ($items as $it) {
        $cant = (int)($it->cantidad ?? 0);
        $precio = (float)($it->precio ?? 0);
        $base += $cant * $precio;
    }
    $iva = $base * ($IVA_PCT / 100.0);
    $total = $base + $iva;

    // Salida HTML sencilla estilo factura
    header('Content-Type: text/html; charset=utf-8');

} catch (Throwable $e) {
    header('Content-Type: text/plain; charset=utf-8');
    echo "ERROR: " . $e->getMessage() . "\n";
    exit;
}
?>
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Factura <?= htmlspecialchars($numero) ?></title>
  <style>
    body{font-family:Arial,Helvetica,sans-serif;background:#f3f3f3;margin:0;padding:24px;}
    .invoice{max-width:900px;margin:0 auto;background:#fff;border:1px solid #ddd;border-radius:12px;overflow:hidden;}
    header{padding:24px;border-bottom:1px solid #eee;display:flex;justify-content:space-between;gap:16px;}
    h1{margin:0;font-size:22px;}
    .muted{color:#666;font-size:13px;line-height:1.4;}
    .box{padding:18px 24px;display:flex;gap:24px;flex-wrap:wrap;}
    .col{min-width:260px;flex:1;}
    table{width:100%;border-collapse:collapse;}
    th,td{padding:12px 10px;border-bottom:1px solid #eee;text-align:left;}
    th{background:#fafafa;font-size:13px;color:#444;}
    td.num, th.num{text-align:right;}
    .totals{padding:18px 24px;display:flex;justify-content:flex-end;}
    .totals table{width:360px;}
    .totals td{border-bottom:none;padding:8px 10px;}
    .totals tr.total td{font-weight:bold;font-size:16px;border-top:1px solid #ddd;padding-top:12px;}
    footer{padding:18px 24px;border-top:1px solid #eee;}
    .badge{display:inline-block;background:#111;color:#fff;border-radius:999px;padding:6px 10px;font-size:12px;}
  </style>
</head>
<body>
  <div class="invoice">
    <header>
      <div>
        <h1>Factura <span class="badge">#<?= htmlspecialchars($numero) ?></span></h1>
        <div class="muted">
          Fecha: <?= htmlspecialchars($fecha) ?><br>
          ID pedido: <?= htmlspecialchars($id) ?>
        </div>
      </div>
      <div class="muted" style="text-align:right;">
        <strong>TiendaOnline</strong><br>
        Ejemplo S.L.<br>
        soporte@tiendaonline.local
      </div>
    </header>

    <section class="box">
      <div class="col">
        <div class="muted"><strong>Facturar a</strong></div>
        <div style="margin-top:6px;">
          <?= htmlspecialchars($nombre ?: '—') ?><br>
          <?= htmlspecialchars($email ?: '') ?>
        </div>
      </div>
      <div class="col">
        <div class="muted"><strong>Detalle del pedido</strong></div>
        <div style="margin-top:6px;">
          Número: <?= htmlspecialchars($numero ?: '—') ?><br>
          Fecha: <?= htmlspecialchars($fecha ?: '—') ?>
        </div>
      </div>
    </section>

    <section style="padding:0 24px 18px 24px;">
      <table>
        <thead>
          <tr>
            <th>Producto</th>
            <th class="num">Cantidad</th>
            <th class="num">Precio</th>
            <th class="num">Subtotal</th>
          </tr>
        </thead>
        <tbody>
        <?php foreach ($items as $it): 
          $pname = (string)($it->nombre ?? '');
          $cant  = (int)($it->cantidad ?? 0);
          $precio= (float)($it->precio ?? 0);
          $sub   = $cant * $precio;
        ?>
          <tr>
            <td><?= htmlspecialchars($pname) ?></td>
            <td class="num"><?= $cant ?></td>
            <td class="num"><?= euro($precio) ?></td>
            <td class="num"><?= euro($sub) ?></td>
          </tr>
        <?php endforeach; ?>
        </tbody>
      </table>
    </section>

    <section class="totals">
      <table>
        <tr>
          <td class="muted">Base imponible</td>
          <td class="num"><?= euro($base) ?></td>
        </tr>
        <tr>
          <td class="muted">IVA (<?= (int)$IVA_PCT ?>%)</td>
          <td class="num"><?= euro($iva) ?></td>
        </tr>
        <tr class="total">
          <td>Total</td>
          <td class="num"><?= euro($total) ?></td>
        </tr>
      </table>
    </section>

    <footer class="muted">
      Gracias por tu compra. Conserva esta factura para tus registros.
    </footer>
  </div>
</body>
</html>
```

### selector de facturas
<small>Creado: 2026-01-19 16:28</small>

`008-selector de facturas.php`

```
<?php
// factura.php  (PECL mongodb, sin Composer)

function euro($n): string {
    return number_format((float)$n, 2, ',', '.') . " €";
}

$IVA_PCT = 21; // ajusta si procede

try {
    $manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");
    $query  = new MongoDB\Driver\Query(
    [],
    [
        'sort'  => ['_id' => 1], // importante: orden estable
        'skip'  => $_GET['id'],
        'limit' => 1
    ]
);
$cursor = $manager->executeQuery('tiendaonline.pedidos', $query);

    $doc = null;
    foreach ($cursor as $d) { $doc = $d; break; }

    if (!$doc) {
        header('Content-Type: text/plain; charset=utf-8');
        echo "No hay pedidos en tiendaonline.pedidos\n";
        exit;
    }

    // Extraer campos con valores por defecto
    $id      = isset($doc->_id) ? (string)$doc->_id : '';
    $cliente = $doc->cliente ?? (object)[];
    $pedido  = $doc->pedido ?? (object)[];
    $items   = $doc->productos ?? [];

    $nombre    = trim(($cliente->nombre ?? '') . ' ' . ($cliente->apellidos ?? ''));
    $email     = $cliente->email ?? '';
    $fecha     = $pedido->fecha ?? '';
    $numero    = $pedido->numero ?? '';

    // Calcular totales
    $base = 0.0;
    foreach ($items as $it) {
        $cant = (int)($it->cantidad ?? 0);
        $precio = (float)($it->precio ?? 0);
        $base += $cant * $precio;
    }
    $iva = $base * ($IVA_PCT / 100.0);
    $total = $base + $iva;

    // Salida HTML sencilla estilo factura
    header('Content-Type: text/html; charset=utf-8');

} catch (Throwable $e) {
    header('Content-Type: text/plain; charset=utf-8');
    echo "ERROR: " . $e->getMessage() . "\n";
    exit;
}
?>
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Factura <?= htmlspecialchars($numero) ?></title>
  <style>
    body{font-family:Arial,Helvetica,sans-serif;background:#f3f3f3;margin:0;padding:24px;}
    .invoice{max-width:900px;margin:0 auto;background:#fff;border:1px solid #ddd;border-radius:12px;overflow:hidden;}
    header{padding:24px;border-bottom:1px solid #eee;display:flex;justify-content:space-between;gap:16px;}
    h1{margin:0;font-size:22px;}
    .muted{color:#666;font-size:13px;line-height:1.4;}
    .box{padding:18px 24px;display:flex;gap:24px;flex-wrap:wrap;}
    .col{min-width:260px;flex:1;}
    table{width:100%;border-collapse:collapse;}
    th,td{padding:12px 10px;border-bottom:1px solid #eee;text-align:left;}
    th{background:#fafafa;font-size:13px;color:#444;}
    td.num, th.num{text-align:right;}
    .totals{padding:18px 24px;display:flex;justify-content:flex-end;}
    .totals table{width:360px;}
    .totals td{border-bottom:none;padding:8px 10px;}
    .totals tr.total td{font-weight:bold;font-size:16px;border-top:1px solid #ddd;padding-top:12px;}
    footer{padding:18px 24px;border-top:1px solid #eee;}
    .badge{display:inline-block;background:#111;color:#fff;border-radius:999px;padding:6px 10px;font-size:12px;}
  </style>
</head>
<body>
  <div class="invoice">
    <header>
      <div>
        <h1>Factura <span class="badge">#<?= htmlspecialchars($numero) ?></span></h1>
        <div class="muted">
          Fecha: <?= htmlspecialchars($fecha) ?><br>
          ID pedido: <?= htmlspecialchars($id) ?>
        </div>
      </div>
      <div class="muted" style="text-align:right;">
        <strong>TiendaOnline</strong><br>
        Ejemplo S.L.<br>
        soporte@tiendaonline.local
      </div>
    </header>

    <section class="box">
      <div class="col">
        <div class="muted"><strong>Facturar a</strong></div>
        <div style="margin-top:6px;">
          <?= htmlspecialchars($nombre ?: '—') ?><br>
          <?= htmlspecialchars($email ?: '') ?>
        </div>
      </div>
      <div class="col">
        <div class="muted"><strong>Detalle del pedido</strong></div>
        <div style="margin-top:6px;">
          Número: <?= htmlspecialchars($numero ?: '—') ?><br>
          Fecha: <?= htmlspecialchars($fecha ?: '—') ?>
        </div>
      </div>
    </section>

    <section style="padding:0 24px 18px 24px;">
      <table>
        <thead>
          <tr>
            <th>Producto</th>
            <th class="num">Cantidad</th>
            <th class="num">Precio</th>
            <th class="num">Subtotal</th>
          </tr>
        </thead>
        <tbody>
        <?php foreach ($items as $it): 
          $pname = (string)($it->nombre ?? '');
          $cant  = (int)($it->cantidad ?? 0);
          $precio= (float)($it->precio ?? 0);
          $sub   = $cant * $precio;
        ?>
          <tr>
            <td><?= htmlspecialchars($pname) ?></td>
            <td class="num"><?= $cant ?></td>
            <td class="num"><?= euro($precio) ?></td>
            <td class="num"><?= euro($sub) ?></td>
          </tr>
        <?php endforeach; ?>
        </tbody>
      </table>
    </section>

    <section class="totals">
      <table>
        <tr>
          <td class="muted">Base imponible</td>
          <td class="num"><?= euro($base) ?></td>
        </tr>
        <tr>
          <td class="muted">IVA (<?= (int)$IVA_PCT ?>%)</td>
          <td class="num"><?= euro($iva) ?></td>
        </tr>
        <tr class="total">
          <td>Total</td>
          <td class="num"><?= euro($total) ?></td>
        </tr>
      </table>
    </section>

    <footer class="muted">
      Gracias por tu compra. Conserva esta factura para tus registros.
    </footer>
  </div>
</body>
</html>
```

### tiendaonline.pedidos
<small>Creado: 2026-01-19 16:28</small>

`tiendaonline.pedidos.json`

```json
[{
  "_id": {
    "$oid": "695fd7e39559fdcab21ef537"
  },
  "cliente": {
    "nombre": "Jose Vicente",
    "apellidos": "Carratala Sanchis",
    "email": "info@jocarsa.com"
  },
  "pedido": {
    "fecha": "2026-01-08",
    "numero": "2026001"
  },
  "productos": [
    {
      "nombre": "Camiseta",
      "cantidad": 3,
      "precio": 43
    },
    {
      "nombre": "Pantalon",
      "cantidad": 2,
      "precio": 23
    },
    {
      "nombre": "Calcetines",
      "cantidad": 3,
      "precio": 33
    },
    {
      "nombre": "Bufanda",
      "cantidad": 4,
      "precio": 13
    }
  ]
},
{
  "_id": {
    "$oid": "695fdb209559fdcab21ef538"
  },
  "cliente": {
    "nombre": "Juan",
    "apellidos": "Lopez Garcia",
    "email": "info@juan.com"
  },
  "pedido": {
    "fecha": "2026-01-09",
    "numero": "2026002"
  },
  "productos": [
    {
      "nombre": "Camiseta",
      "cantidad": 3,
      "precio": 43
    },
    {
      "nombre": "Pantalon",
      "cantidad": 2,
      "precio": 23
    },
    {
      "nombre": "Calcetines",
      "cantidad": 3,
      "precio": 33
    },
    {
      "nombre": "Bufanda",
      "cantidad": 4,
      "precio": 13
    }
  ]
}]
```


<a id="sistemas-gestores-de-bases-de-datos-no-relacionales"></a>
## Sistemas gestores de bases de datos no relacionales

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/007-Uso%20de%20bases%20de%20datos%20no%20relacionales/004-Sistemas%20gestores%20de%20bases%20de%20datos%20no%20relacionales)


<a id="herramientas-de-los-sistemas-gestores-de-bases-de-datos-no-relacionales-para-la-gestion-de-la-informacion-almacenada"></a>
## Herramientas de los sistemas gestores de bases de datos no relacionales para la gestión de la información almacenada

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/007-Uso%20de%20bases%20de%20datos%20no%20relacionales/005-Herramientas%20de%20los%20sistemas%20gestores%20de%20bases%20de%20datos%20no%20relacionales%20para%20la%20gesti%C3%B3n%20de%20la%20informaci%C3%B3n%20almacenada)



<a id="proyectos"></a>
# Proyectos

<a id="proyecto-tienda-online"></a>
## proyecto tienda online

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/008-Proyectos/001-proyecto%20tienda%20online)

### Introducción a los ejercicios

Based on the provided files, I'll create a SQL script to populate the database with the given data.

**Table creation and insert statements**

```sql
-- Create tables if not exist
CREATE TABLE IF NOT EXISTS cliente (
  id INT AUTO_INCREMENT,
  nombre VARCHAR(255),
  apellidos VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS producto (
  id INT AUTO_INCREMENT,
  titulo VARCHAR(255),
  descripcion TEXT,
  precio DECIMAL(10,2),
  imagen VARCHAR(255),
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS pedido (
  id INT AUTO_INCREMENT,
  fecha DATE,
  cliente_id INT,
  PRIMARY KEY (id),
  FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);

CREATE TABLE IF NOT EXISTS lineapedido (
  id INT AUTO_INCREMENT,
  pedido_id INT,
  producto_id INT,
  cantidad VARCHAR(10),
  PRIMARY KEY (id),
  FOREIGN KEY (pedido_id) REFERENCES pedido(id),
  FOREIGN KEY (producto_id) REFERENCES producto(id)
);

-- Insert data
INSERT INTO cliente (nombre, apellidos, email)
VALUES 
('Laura', 'Martínez López', 'laura@example.com'),
('Carlos', 'Gómez Ruiz', 'carlos@example.com'),
('María', 'Serrano Díaz', 'maria@example.com'),
('Jorge', 'Pérez Sánchez', 'jorge@example.com'),
('Elena', 'Ruiz Navarro', 'elena@example.com');

INSERT INTO producto (titulo, descripcion, precio, imagen)
VALUES 
('Camiseta Azul', 'Camiseta de algodón talla M', 19.99, 'camiseta_azul.jpg'),
('Pantalón Negro', 'Pantalón vaquero negro unisex', 39.90, 'pantalon_negro.jpg'),
('Sudadera Roja', 'Sudadera con capucha talla L', 29.95, 'sudadera_roja.jpg'),
('Zapatillas Deportivas', 'Calzado deportivo ligero', 59.99, 'zapatillas.jpg'),
('Gorra Negra', 'Gorra ajustable con visera', 12.50, 'gorra_negra.jpg'),
('Calcetines Técnicos', 'Pack de 3 pares', 8.99, 'calcetines.jpg'),
('Chaqueta Impermeable', 'Chaqueta cortavientos unisex', 79.99, 'chaqueta.jpg');

INSERT INTO pedido (fecha, cliente_id)
VALUES 
('2025-02-01', 1),
('2025-02-02', 3),
('2025-02-02', 2),
('2025-02-03', 5),
('2025-02-04', 1),
('2025-02-05', 4),
('2025-02-06', 2),
('2025-02-07', 3);

INSERT INTO lineapedido (pedido_id, producto_id, cantidad)
VALUES 
-- Pedido 1
(1, 1, '2'),
(1, 5, '1'),
(1, 6, '3'),

-- Pedido 2
(4, 3, '1'),
(4, 4, '1'),

-- Pedido 3
(6, 2, '2'),
(6, 6, '1'),

-- Pedido 4
(8, 7, '1'),
(8, 5, '2'),

-- Pedido 5
(10, 1, '1'),
(10, 2, '1'),
(10, 3, '1'),

-- Pedido 6
(13, 4, '1'),

-- Pedido 7
(14, 6, '4'),
(14, 1, '2'),

-- Pedido 8
(16, 7, '1'),
(16, 3, '2'),
(16, 5, '1');
```

This script creates the necessary tables and inserts the provided data into each table. Note that I've used `AUTO_INCREMENT` to set the primary keys for each table, assuming that you want the database to automatically increment the IDs.

**User creation**

```sql
-- Create user
CREATE USER IF NOT EXISTS 'tiendadam'@'localhost' IDENTIFIED BY 'Tiendadam123$';

-- Grant privileges
GRANT USAGE ON *.* TO 'tiendadam'@'localhost';

ALTER USER 'tiendadam'@'localhost' REQUIRE NONE;

GRANT ALL PRIVILEGES ON `tiendadam`.* TO 'tiendadam'@'localhost';

FLUSH PRIVILEGES;
```

This script creates a new user with the specified username and password, grants the necessary privileges to the user, and flushes the privilege cache.

### pantalla de confirmacion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este código es una página web básica creada en PHP, que simula un sitio de tienda online. La página tiene diferentes secciones y respuestas dependiendo del parámetro de GET llamado "operacion".

Cuando el usuario accede a la página, PHP compara el valor del parámetro "operacion" con los valores permitidos: "producto", "carrito" o "finalizacion". En función de este valor, se muestra una sección diferente en la página.

Por ejemplo, si el valor es "producto", se muestra un artículo de tienda con imagen, nombre y descripción del producto, así como un botón para comprar. Si el valor es "carrito", se muestra una pantalla de finalización donde se muestra la lista de productos comprados y un botón para confirmar la compra.

El código también utiliza una estructura CSS para dar estilos a la página y hacerla más visualmente atractiva.

`011-pantalla de confirmacion.php`

```
<!doctype html>
<html lang="es">
  <head>
    <title>Tienda online</title>
    <meta charset="utf-8">
    <style>
      html,body{padding:0px;margin:0px;}
      header,main,footer{width:800px;margin:auto;text-align:center;font-family:sans-serif;}
      .catalogo{display:grid;grid-template-columns:repeat(3,100fr);gap:20px;}
      main article .imagen{height:100px;}
      main a{background:orange;color:white;text-decoration:none;padding:10px;border-radius:10px;}
      header{width:100%;height:200px;background:url("blanco.png"),url("blanco.png"),url("cabeceratienda.avif");padding:20px;background-size:cover;background-position:center top;margin-bottom:20px;display:flex;justify-content:center;align-items:center;}
      section{width:100%;display:flex;}
      section .izquierda{flex:1;}
      section .derecha{flex:2;}
      section .izquierda img{width:100%;}
      table{width:100%;}
      table thead{background:orange;color:black;text-align:left;}
      table tbody{text-align:left;}
      .finalizacion{display:flex;flex-direction:column;}
    </style>
  </head>
  <body>
    <header>
      <h1>Tienda online</h1>
    </header>
    <main>
      <?php
        if(isset($_GET['operacion'])){
      ?>
        <?php
          if($_GET['operacion'] == "producto"){
        ?>
          <section class="producto">
            <div class="izquierda">
              <img src="producto.webp">
              <a href="?operacion=carrito&producto=1">🛍 Comprar</a>
            </div>
            <div class="derecha">
              <h3>Nombre del producto</h3>
              <p>Breve descripción del producto</p>
              <p>4.33€</p>
            </div>
          </section>
        <?php }else if($_GET['operacion'] == "carrito"){ ?>
          <section class="finalizacion">
            <table>
              <thead>
                <tr>
                  <th>Producto</th>
                  <th>Precio</th>
                  <th>Unidades</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Producto</td>
                  <td>Precio</td>
                  <td>Unidades</td>
                </tr>
                <tr>
                  <td>Producto</td>
                  <td>Precio</td>
                  <td>Unidades</td>
                </tr>
                <tr>
                  <td colspan=2>Total</td>
                  <td>Total</td>
                </tr>
              </tbody>
            </table>
            <a href="?operacion=finalizacion">Confirmar compra</a>
          </section>
        <?php }else if($_GET['operacion'] == "finalizacion"){ ?>
          <section class="finalizacion">
            <h3>Pedido finalizado</h3>
            <p>Muchas gracias por tu compra</p>
            <a href="?">Pulsa aqui para continuar navegando</a>
          </section>
        <?php } ?>
      <?php }else{ ?>
        <section class="catalogo">
        <?php for($i = 0;$i<30;$i++){ ?>
          <article>
            <div class="imagen" style="background:url(producto.webp);background-size:cover;background-position:center center;"></div>
            <h3>Nombre del producto</h3>
            <p>Breve descripción del producto</p>
            <p>4.33€</p>
            <a href="?operacion=producto&producto=1">🛍 Comprar</a>
          </article>
        <?php } ?>
        </section>
      <?php } ?>
    </main>
    <footer>
      (c) Jose Vicente Carratala
    </footer>
  </body>
</html>
```

### diagrama
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código HTML representa un diagrama ER (Entidades Relacionales) en formato de gráficos interactivos utilizando SVG (Scalable Vector Graphics). Un diagrama ER es una representación visual de las relaciones entre diferentes entidades y atributos de una base de datos.

En este caso, el código utiliza CSS para definir estilos específicos a cada elemento del diagrama, como la forma, el tamaño y la posición. Cada entidad (Producto, Cliente, Pedido, LineaPedido) se representa como un rectángulo con diferentes colores y patrones, mientras que las relaciones entre ellas se representan mediante flechas.

`diagrama.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama exportado</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: #f3f3f7;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.page {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  width: 745.0780402289494px;
  height: 438.5625203450519px;
  overflow: visible;
}

/* formas básicas */
.shape {
  position: absolute;
  min-width: 120px;
  min-height: 40px;
  padding: 6px 10px;
  background: #ffffff;
  border-radius: 4px;
  border: 1px solid #9ca3af;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.shape.rectangle {
  border-radius: 4px;
}

.shape.pill {
  border-radius: 999px;
}

.shape.circle {
  border-radius: 999px;
  width: 80px;
  height: 80px;
  padding: 0;
  justify-content: center;
}

/* texto libre */
.shape.text {
  background: transparent;
  border: none;
  box-shadow: none;
  padding: 0;
  min-width: 20px;
  min-height: 20px;
}

/* base de datos */
.shape.db {
  min-width: 120px;
  min-height: 60px;
  padding-top: 20px;
  border-radius: 60px / 16px;
  background: linear-gradient(180deg, #e5e7eb 0%, #ffffff 40%, #e5e7eb 100%);
  position: absolute;
  overflow: hidden;
  text-align: center;
}
.shape.db::before {
  content: "";
  position: absolute;
  top: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid #9ca3af;
  background: radial-gradient(circle at 50% 30%, #ffffff 0%, #e5e7eb 70%);
}
.shape.db::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(156, 163, 175, 0.6);
  border-top: none;
  background: radial-gradient(circle at 50% 70%, #e5e7eb 0%, #d1d5db 70%);
}

/* entidades ER */
.shape.entity {
  width: 220px;
  min-height: 80px;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.15);
  display: flex;
  flex-direction: column;
  font-size: 13px;
  overflow: hidden;
  padding: 0;
}
.entity-header {
  background: #f3f4f6;
  padding: 4px 8px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}
.entity-properties {
  flex: 1;
  padding: 4px 4px 0 4px;
}
.entity-property {
  display: grid;
  grid-template-columns: 14px 1fr 14px;
  align-items: center;
  column-gap: 4px;
  padding: 2px 0;
}
.entity-property .property-name {
  padding: 2px 4px;
  border-radius: 3px;
}

/* puertos */
.port {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1px solid #111827;
  background: #ffffff;
}
.port-left { justify-self: start; }
.port-right { justify-self: end; }

/* flechas rectas */
.arrow {
  position: absolute;
  height: 2px;
  background: #111827;
  transform-origin: 0 50%;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.arrow-double::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}

/* flechas ortogonales */
.ortho-arrow {
  position: absolute;
  left: 0;
  top: 0;
}
.ortho-arrow .ortho-seg {
  position: absolute;
  background: #111827;
}
.ortho-seg.seg-horizontal { height: 2px; }
.ortho-seg.seg-vertical { width: 2px; }
.ortho-arrowhead {
  position: absolute;
  width: 0;
  height: 0;
}
.ortho-arrowhead.dir-right {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #111827;
}
.ortho-arrowhead.dir-left {
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-right: 8px solid #111827;
}
.ortho-arrowhead.dir-down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 8px solid #111827;
}
.ortho-arrowhead.dir-up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 8px solid #111827;
}
</style>
</head>
<body>
<div class="page">

<div class="shape entity" style="left:288.0624898274738px;top:216.56253390842005px;width:160.00003390842008px;height:181.99998643663187px;">
  <div class="entity-header">Producto</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">titulo</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">descripcion</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">precio</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">imagen</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:40px;top:40px;width:159.99998304578986px;height:158.000013563368px;">
  <div class="entity-header">Cliente</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">nombre</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">apellidos</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">email</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:288.31249660915785px;top:57.234395345052064px;width:159.99999999999994px;height:133.99997287326383px;">
  <div class="entity-header">Pedido</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">fecha</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">cliente_id</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="shape entity" style="left:545.07817586263px;top:133.37500678168402px;width:159.99986436631937px;height:158.000013563368px;">
  <div class="entity-header">LineaPedido</div>
  <div class="entity-properties">
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">pedido_id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">producto_id</div>
      <div class="port port-right"></div>
    </div>
    <div class="entity-property">
      <div class="port port-left"></div>
      <div class="property-name">cantidad</div>
      <div class="port port-right"></div>
    </div>
  </div>
</div>
<div class="arrow" style="left:166.09373304578986px;top:87.98506350534757px;width:166.02908229898586px;transform:rotate(0.37792964126810247rad);"></div>
<div class="arrow" style="left:416.20312160915785px;top:106.28629311859294px;width:180.49425302053035px;transform:rotate(0.5480175784279776rad);"></div>
<div class="arrow" style="left:421.01567586263px;top:261.4577043470099px;width:152.8498955064719px;transform:rotate(-0.21746367920105833rad);"></div>
</div>
</body>
</html>
```

### diagrama
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este archivo JSON representa un diagrama de objetos relacionados en una base de datos. En primer lugar, debemos entender qué es un diagrama de objetos y su propósito.

Un diagrama de objetos es una herramienta visual utilizada para describir la estructura de una base de datos y las relaciones entre sus tablas o entidades. Se compone de objetos que representan tablas de la base de datos, y relaciones entre estos objetos que indican cómo se relacionan las tablas.

En este caso específico, el diagrama representa cuatro entidades: Producto, Cliente, Pedido y LineaPedido. Cada entidad tiene sus propias columnas o propiedades, como id, titulo, descripcion, precio, imagen, nombre, apellidos, fecha, cliente_id, pedido_id, producto_id, cantidad, etc.

Las flechas en el diagrama indican las relaciones entre estas entidades. Por ejemplo, la primera flecha conecta Cliente con Pedido, indicando que un pedido está asociado a un cliente específico. La segunda flecha conecta Pedido con LineaPedido, y la tercera flecha conecta Producto con LineaPedido.

En resumen, este archivo JSON describe el esqueleto de una base de datos en la que se relacionan diferentes entidades como productos, clientes, pedidos y líneas de pedido.

`diagrama.json`

```json
{
  "formas": [
    {
      "id": "forma-1",
      "tipo": "entity",
      "left": "509.509px",
      "top": "574.102px",
      "width": "",
      "height": "",
      "entityName": "Producto",
      "properties": [
        {
          "id": "prop-1",
          "name": "id"
        },
        {
          "id": "prop-2",
          "name": "titulo"
        },
        {
          "id": "prop-3",
          "name": "descripcion"
        },
        {
          "id": "prop-4",
          "name": "precio"
        },
        {
          "id": "prop-5",
          "name": "imagen"
        }
      ]
    },
    {
      "id": "forma-2",
      "tipo": "entity",
      "left": "261.437px",
      "top": "397.542px",
      "width": "",
      "height": "",
      "entityName": "Cliente",
      "properties": [
        {
          "id": "prop-6",
          "name": "id"
        },
        {
          "id": "prop-7",
          "name": "nombre"
        },
        {
          "id": "prop-8",
          "name": "apellidos"
        },
        {
          "id": "prop-9",
          "name": "email"
        }
      ]
    },
    {
      "id": "forma-4",
      "tipo": "entity",
      "left": "509.759px",
      "top": "414.774px",
      "width": "",
      "height": "",
      "entityName": "Pedido",
      "properties": [
        {
          "id": "prop-14",
          "name": "id"
        },
        {
          "id": "prop-15",
          "name": "fecha"
        },
        {
          "id": "prop-16",
          "name": "cliente_id"
        }
      ]
    },
    {
      "id": "forma-5",
      "tipo": "entity",
      "left": "766.524px",
      "top": "490.918px",
      "width": "",
      "height": "",
      "entityName": "LineaPedido",
      "properties": [
        {
          "id": "prop-17",
          "name": "id"
        },
        {
          "id": "prop-19",
          "name": "pedido_id"
        },
        {
          "id": "prop-20",
          "name": "producto_id"
        },
        {
          "id": "prop-21",
          "name": "cantidad"
        }
      ]
    }
  ],
  "flechas": [
    {
      "desde": {
        "shapeId": "forma-2",
        "propId": "prop-6",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-4",
        "propId": "prop-16",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-4",
        "propId": "prop-14",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-5",
        "propId": "prop-19",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    },
    {
      "desde": {
        "shapeId": "forma-1",
        "propId": "prop-1",
        "side": "right"
      },
      "hasta": {
        "shapeId": "forma-5",
        "propId": "prop-20",
        "side": "left"
      },
      "tipo": "simple",
      "estilo": "straight"
    }
  ]
}
```

### diagrama
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

**Creación de tablas en SQL**

El código proporcionado es un ejemplo de cómo se pueden crear tres tablas en una base de datos utilizando el lenguaje SQL: `producto`, `cliente` y `pedido`. Estas tablas están relacionadas entre sí, lo que permite almacenar y recuperar datos de manera eficiente.

**¿Qué hace el código?**

El código crea las siguientes tablas:

*   `producto`: Almacena información sobre los productos, como título, descripción, precio, imagen y un identificador único (`id`) que sirve como clave primaria.
*   `cliente`: Almacena información sobre los clientes, como nombre, apellidos y dirección de correo electrónico (email), junto con un identificador único (`id`).
*   `pedido`: Almacena información sobre los pedidos, incluyendo la fecha de realización del pedido, el identificador del cliente que lo realizó (`cliente_id`) y un identificador único (`id`). Esta tabla está relacionada con la tabla `cliente` mediante una relación de clave foránea.
*   `lineapedido`: Almacena información sobre las líneas de los pedidos, incluyendo el identificador del pedido (`pedido_id`), el identificador del producto (`producto_id`) y la cantidad solicitada. Esta tabla está relacionada con las tablas `pedido` y `producto` mediante relaciones de clave foránea.

**¿Por qué es importante?**

La creación de estas tablas permite diseñar una base de datos estructurada que puede almacenar y recuperar información de manera eficiente. Las claves foráneas establecen la relación entre las tablas, lo que facilita la consulta de datos relacionados entre sí. Esto es especialmente útil en aplicaciones comerciales o de servicios donde se necesitan almacenar y gestionar datos de clientes, pedidos y productos.

`diagrama.sql`

```sql
-- ============================================
-- 1. CREACIÓN DE TABLA PRODUCTO
-- ============================================
CREATE TABLE producto (
  id INT AUTO_INCREMENT,
  titulo VARCHAR(255),
  descripcion VARCHAR(255),
  precio VARCHAR(255),
  imagen VARCHAR(255),
  PRIMARY KEY (id)
);

-- ============================================
-- 2. CREACIÓN DE TABLA CLIENTE
-- ============================================
CREATE TABLE cliente (
  id INT AUTO_INCREMENT,
  nombre VARCHAR(255),
  apellidos VARCHAR(255),
  email VARCHAR(255),
  PRIMARY KEY (id)
);

-- ============================================
-- 3. CREACIÓN DE TABLA PEDIDO
--    (depende de cliente)
-- ============================================
CREATE TABLE pedido (
  id INT AUTO_INCREMENT,
  fecha VARCHAR(255),
  cliente_id INT,
  PRIMARY KEY (id),
  CONSTRAINT fk_pedido_1 FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);

-- ============================================
-- 4. CREACIÓN DE TABLA LINEAPEDIDO
--    (depende de pedido y producto)
-- ============================================
CREATE TABLE lineapedido (
  id INT AUTO_INCREMENT,
  pedido_id INT,
  producto_id INT,
  cantidad VARCHAR(255),
  PRIMARY KEY (id),
  CONSTRAINT fk_lineapedido_1 FOREIGN KEY (pedido_id) REFERENCES pedido(id),
  CONSTRAINT fk_lineapedido_2 FOREIGN KEY (producto_id) REFERENCES producto(id)
);
```

### diagrama
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

Este fragmento de código es una representación gráfica en SVG (Scalable Vector Graphics) que muestra un diagrama de relación entre diferentes entidades, como productos, clientes y pedidos. 

El código utiliza elementos como rectángulos, líneas y textos para crear el diagrama. El uso de clases CSS dentro del elemento `<defs>` permite establecer estilos para los diferentes elementos del diagrama, lo que facilita su personalización.

Este fragmento es importante porque proporciona una visión general de cómo se pueden representar las relaciones entre entidades en un sistema de gestión de inventario.

`diagrama.svg`

```
<svg xmlns="http://www.w3.org/2000/svg" width="745.0780402289494" height="438.5625203450519" viewBox="0 0 745.0780402289494 438.5625203450519">

  <defs>
    <style>
      text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px; fill: #111827; }
      .shape-rect { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-entity { fill: #ffffff; stroke: #111827; stroke-width: 2; }
      .shape-circle { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-pill { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .shape-db { fill: #ffffff; stroke: #9ca3af; stroke-width: 1; }
      .conn { stroke: #111827; stroke-width: 2; fill: none; }
    </style>
    <marker id="arrow-end" markerWidth="10" markerHeight="7" refX="10" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="0 0, 10 3.5, 0 7" fill="#111827"/>
    </marker>
    <marker id="arrow-start" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
            orient="auto" markerUnits="strokeWidth">
      <polygon points="10 0, 0 3.5, 10 7" fill="#111827"/>
    </marker>
  </defs>
        
<rect class="shape-entity" x="288.0624898274738" y="216.56253390842005" width="160.00003390842008" height="181.99998643663187" />
<line x1="288.0624898274738" y1="246.56253390841997" x2="448.06252373589393" y2="246.56253390841997" stroke="#e5e7eb" stroke-width="1"/>
<text x="368.06250678168385" y="236.06251356336787" text-anchor="middle">Producto</text>
<text x="335.0937330457898" y="266.5624932183158">id</text>
<text x="335.0937330457898" y="290.56253390841994">titulo</text>
<text x="335.0937330457898" y="314.56250678168385">descripcion</text>
<text x="335.0937330457898" y="338.56247965494777">precio</text>
<text x="335.0937330457898" y="362.5625203450519">imagen</text>
<rect class="shape-entity" x="40" y="40" width="159.99998304578986" height="158.000013563368" />
<line x1="40" y1="70" x2="199.99998304578986" y2="70" stroke="#e5e7eb" stroke-width="1"/>
<text x="119.99999152289493" y="59.49999660915799" text-anchor="middle">Cliente</text>
<text x="93.906260172526" y="89.99999321831598">id</text>
<text x="93.906260172526" y="114">nombre</text>
<text x="93.906260172526" y="138.00000678168402">apellidos</text>
<text x="93.906260172526" y="162.00001356336804">email</text>
<rect class="shape-entity" x="288.31249660915785" y="57.234395345052064" width="159.99999999999994" height="133.99997287326383" />
<line x1="288.31249660915785" y1="87.23439534505206" x2="448.3124966091578" y2="87.23439534505206" stroke="#e5e7eb" stroke-width="1"/>
<text x="368.31249660915785" y="76.73439195421005" text-anchor="middle">Pedido</text>
<text x="340.4062330457898" y="107.23438856336804">id</text>
<text x="340.4062330457898" y="131.23439534505206">fecha</text>
<text x="340.4062330457898" y="155.23436821831592">cliente_id</text>
<rect class="shape-entity" x="545.07817586263" y="133.37500678168402" width="159.99986436631937" height="158.000013563368" />
<line x1="545.07817586263" y1="163.37500678168396" x2="705.0780402289494" y2="163.37500678168396" stroke="#e5e7eb" stroke-width="1"/>
<text x="625.0781080457897" y="152.87500339084195" text-anchor="middle">LineaPedido</text>
<text x="590.2656487358938" y="183.375">id</text>
<text x="590.2656487358938" y="207.37500678168396">pedido_id</text>
<text x="590.2656487358938" y="231.37497965494777">producto_id</text>
<text x="590.2656487358938" y="255.3750203450519">cantidad</text>
<path class="conn" d="M 166.09373304578986 87.98506350534757 L 320.4062398274739 149.24929793128433" marker-end="url(#arrow-end)" />
<path class="conn" d="M 416.20312160915785 106.28629311859294 L 570.2656216091577 200.32310222645913" marker-end="url(#arrow-end)" />
<path class="conn" d="M 421.01567586263 261.4577043470099 L 570.2656216091577 228.47976852625368" marker-end="url(#arrow-end)" />
</svg>
```

### insercion
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

**Insertar datos en una base de datos**

El código que hemos visto es un ejemplo de cómo insertar datos en una base de datos utilizando el lenguaje SQL. En este caso, estamos creando tres tablas: `cliente`, `producto` y `pedido`.

La primera instrucción `INSERT INTO cliente...` inserta cinco registros en la tabla `cliente`: cada registro tiene como identificador único un número (`id`) y contiene información personal del cliente (`nombre`, `apellidos` y `email`). Esto permite almacenar información sobre los clientes de manera estructurada.

La segunda instrucción `INSERT INTO producto...` hace lo mismo que la primera, pero esta vez para la tabla `producto`. Estos registros también contienen una descripción del producto y su precio. También hay imágenes asociadas a cada uno de ellos.

La tercera instrucción `INSERT INTO pedido...` inserta ocho registros en la tabla `pedido`, cada uno relacionado con un cliente específico (`cliente_id`). Cada registro contiene la fecha del pedido y no tiene otro dato adicional.

Finalmente, la cuarta instrucción `INSERT INTO lineapedido...` crea nueve registros en la tabla `lineapedido`. Este registro se relaciona con una orden de compra (`pedido_id`) y establece la cantidad de cada producto que se ha pedido.

`insercion.sql`

```sql
INSERT INTO cliente (id, nombre, apellidos, email) VALUES
(1, 'Laura', 'Martínez López', 'laura@example.com'),
(2, 'Carlos', 'Gómez Ruiz', 'carlos@example.com'),
(3, 'María', 'Serrano Díaz', 'maria@example.com'),
(4, 'Jorge', 'Pérez Sánchez', 'jorge@example.com'),
(5, 'Elena', 'Ruiz Navarro', 'elena@example.com');

INSERT INTO producto (id, titulo, descripcion, precio, imagen) VALUES
(1, 'Camiseta Azul', 'Camiseta de algodón talla M', '19.99', 'camiseta_azul.jpg'),
(2, 'Pantalón Negro', 'Pantalón vaquero negro unisex', '39.90', 'pantalon_negro.jpg'),
(3, 'Sudadera Roja', 'Sudadera con capucha talla L', '29.95', 'sudadera_roja.jpg'),
(4, 'Zapatillas Deportivas', 'Calzado deportivo ligero', '59.99', 'zapatillas.jpg'),
(5, 'Gorra Negra', 'Gorra ajustable con visera', '12.50', 'gorra_negra.jpg'),
(6, 'Calcetines Técnicos', 'Pack de 3 pares', '8.99', 'calcetines.jpg'),
(7, 'Chaqueta Impermeable', 'Chaqueta cortavientos unisex', '79.99', 'chaqueta.jpg');


INSERT INTO pedido (id, fecha, cliente_id) VALUES
(1, '2025-02-01', 1),
(2, '2025-02-02', 3),
(3, '2025-02-02', 2),
(4, '2025-02-03', 5),
(5, '2025-02-04', 1),
(6, '2025-02-05', 4),
(7, '2025-02-06', 2),
(8, '2025-02-07', 3);


INSERT INTO lineapedido (id, pedido_id, producto_id, cantidad) VALUES
-- Pedido 1
(1, 1, 1, '2'),
(2, 1, 5, '1'),
(3, 1, 6, '3'),

-- Pedido 2
(4, 2, 3, '1'),
(5, 2, 4, '1'),

-- Pedido 3
(6, 3, 2, '2'),
(7, 3, 6, '1'),

-- Pedido 4
(8, 4, 7, '1'),
(9, 4, 5, '2'),

-- Pedido 5
(10, 5, 1, '1'),
(11, 5, 2, '1'),
(12, 5, 3, '1'),

-- Pedido 6
(13, 6, 4, '1'),

-- Pedido 7
(14, 7, 6, '4'),
(15, 7, 1, '2'),

-- Pedido 8
(16, 8, 7, '1'),
(17, 8, 3, '2'),
(18, 8, 5, '1');
```

### usuario
<small>Creado: 2026-01-19 16:28</small>

#### Explicación

**Crea un usuario y le asigna privilegios en la base de datos**

Este fragmento de código se utiliza para crear un nuevo usuario en una base de datos MySQL y asignarle privilegios para interactuar con ella. El código crea un usuario llamado "tiendadam" que se conectará a la base de datos desde el localhost.

**¿Qué hace este código?**

El código tiene varias partes importantes:

*   **Crea un usuario**: Se utiliza el comando `CREATE USER` para crear un nuevo usuario en la base de datos. En este caso, se crea un usuario llamado "tiendadam" que se conectará desde el localhost.
*   **Asigna privilegios**: El comando `GRANT` permite asignar privilegios al usuario creado. En este caso, se otorgan los siguientes privilegios:
    *   `USAGE ON *.* TO 'tiendadam'@'localhost';`: Permite que el usuario utilice la base de datos para realizar consultas y operaciones.
    *   `GRANT ALL PRIVILEGES ON `tiendadam`.* TO 'tiendadam'@'localhost';`: Asigna todos los privilegios posibles al usuario, lo que significa que puede realizar cualquier operación en la base de datos.
*   **Establece restricciones**: El comando `ALTER USER` permite establecer restricciones al usuario creado. En este caso, se establecen las siguientes restricciones:
    *   `REQUIRE NONE`: Permite que el usuario realice todas las operaciones sin restricción alguna.
    *   `WITH MAX_QUERIES_PER_HOUR 0`, `MAX_CONNECTIONS_PER_HOUR 0`, `MAX_UPDATES_PER_HOUR 0` y `MAX_USER_CONNECTIONS 0`: Establecen límites para el número de consultas, conexiones, actualizaciones y usuarios que puede realizar el usuario.
*   **Flush**: El comando `FLUSH PRIVILEGES` es necesario para aplicar los cambios en la base de datos.

`usuario.sql`

```sql
CREATE USER 
'tiendadam'@'localhost' 
IDENTIFIED BY 'Tiendadam123$';

GRANT USAGE ON *.* TO 'tiendadam'@'localhost';

ALTER USER 'tiendadam'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 
MAX_CONNECTIONS_PER_HOUR 0 
MAX_UPDATES_PER_HOUR 0 
MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON `tiendadam`.* 
TO 'tiendadam'@'localhost';

FLUSH PRIVILEGES;
```

### Actividades propuestas

Estos archivos parecen ser parte de una base de datos MySQL relacionada con un sistema de tienda en línea. Se presentan los siguientes files:

1.  ** ARCHIVO: schema.sql **: Este archivo contiene el esquema de la base de datos, que define las tablas y sus columnas. En este caso, se crean tablas para clientes (`cliente`), productos (`producto`), pedidos (`pedido`) y líneas de pedido (`lineapedido`). 
2.  ** ARCHIVO: data.sql **: Este archivo contiene los datos de inicialización de la base de datos. Se insertan los valores iniciales en las tablas creadas anteriormente, como clientes, productos, pedidos y líneas de pedido.
3.  ** ARCHIVO: usuarios.sql **: Este archivo contiene el script para crear un usuario nuevo llamado `tiendadam` con todas las permisiones necesarias para interactuar con la base de datos. El script también define algunas restricciones adicionales, como limitar el número máximo de consultas y conexiones por hora.
4.  ** ARCHIVO: insertion.sql **: Este archivo contiene los scripts de inserción de datos en las tablas de productos y pedidos, pero parece haber un error en el script de inserción porque no hay una línea de pedido completa.
5.  ** ARCHIVO: imagen.jpg, camiseta_azul.jpg, pantalon_negro.jpg, sudadera_roja.jpg, zapatillas.jpg, gorra_negra.jpg, calcetines.jpg, chaqueta.jpg**: Se supone que estos archivos contienen las imágenes correspondientes a los productos, pero no están presentes en el directorio proporcionado.

En resumen, este conjunto de archivos es una base de datos completa para un sistema de tienda en línea con características como clientes, productos, pedidos y líneas de pedido.


<a id="ia-para-dietetica"></a>
## IA para dietetica

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/008-Proyectos/002-IA%20para%20dietetica)

### llamada desde PHP
<small>Creado: 2026-01-19 16:28</small>

`002-llamada desde PHP.php`

```
<?php
function h($s): string { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

$defaultPrompt = "Mira tengo manzana, yogur, tengo salmon y tengo agua, qué plato saludable puedo preparar? Dime solo uno";
$model   = $_POST["model"]   ?? "llama3:latest";
$prompt  = $_POST["prompt"]  ?? $defaultPrompt;
$baseUrl = $_POST["baseUrl"] ?? "http://127.0.0.1:11434"; // Ollama server

$result = null;

if ($_SERVER["REQUEST_METHOD"] === "POST") {
  $prompt = trim($prompt);
  if ($prompt === "") $prompt = $defaultPrompt;

  $payload = [
    "model"  => $model,
    "prompt" => $prompt,
    "stream" => false
  ];

  $url = rtrim($baseUrl, "/") . "/api/generate";

  $ch = curl_init($url);
  curl_setopt_array($ch, [
    CURLOPT_POST           => true,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER     => ["Content-Type: application/json"],
    CURLOPT_POSTFIELDS     => json_encode($payload, JSON_UNESCAPED_UNICODE),
    CURLOPT_CONNECTTIMEOUT => 5,
    CURLOPT_TIMEOUT        => 90,
  ]);

  $raw = curl_exec($ch);
  $httpCode = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
  $curlErr  = curl_error($ch);
  curl_close($ch);

  if ($raw === false) {
    $result = ["ok" => false, "err" => "cURL error: " . $curlErr, "out" => ""];
  } elseif ($httpCode < 200 || $httpCode >= 300) {
    $result = ["ok" => false, "err" => "HTTP $httpCode\n$raw", "out" => ""];
  } else {
    $json = json_decode($raw, true);
    if (!is_array($json)) {
      $result = ["ok" => false, "err" => "Respuesta no-JSON:\n$raw", "out" => ""];
    } else {
      // Ollama devuelve normalmente {"response": "...", "done": true, ...}
      $result = ["ok" => true, "out" => (string)($json["response"] ?? ""), "err" => ""];
    }
  }
}
?>
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ollama Web (PHP → HTTP API)</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Arial,sans-serif;max-width:900px;margin:40px auto;padding:0 16px;line-height:1.4}
    .card{border:1px solid #e5e5e5;border-radius:12px;padding:16px;margin:16px 0}
    label{display:block;font-weight:600;margin:10px 0 6px}
    textarea,input{width:100%;padding:10px;border:1px solid #d6d6d6;border-radius:10px;font:inherit}
    textarea{min-height:140px}
    button{padding:10px 14px;border:0;border-radius:10px;cursor:pointer;font-weight:600}
    .row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    pre{white-space:pre-wrap;word-wrap:break-word;background:#0b0b0b;color:#f1f1f1;padding:12px;border-radius:12px;overflow:auto}
    .err{background:#fff3f3;border:1px solid #ffd0d0;color:#7a0000;padding:12px;border-radius:12px}
    @media (max-width:700px){.row{grid-template-columns:1fr}}
  </style>
</head>
<body>

<h1>Ollama Web (PHP → HTTP API)</h1>

<div class="card">
  <form method="post">
    <div class="row">
      <div>
        <label for="model">Modelo</label>
        <input id="model" name="model" value="<?=h($model)?>" placeholder="llama3:latest">
      </div>
      <div>
        <label for="baseUrl">Ollama URL</label>
        <input id="baseUrl" name="baseUrl" value="<?=h($baseUrl)?>" placeholder="http://127.0.0.1:11434">
      </div>
    </div>

    <label for="prompt">Prompt</label>
    <textarea id="prompt" name="prompt"><?=h($prompt)?></textarea>

    <div style="margin-top:12px;">
      <button type="submit">Preguntar</button>
    </div>
  </form>
</div>

<?php if ($result !== null): ?>
  <div class="card">
    <h2>Respuesta</h2>
    <?php if (!$result["ok"]): ?>
      <div class="err"><?=nl2br(h($result["err"]))?></div>
    <?php else: ?>
      <pre><?=h($result["out"])?></pre>
    <?php endif; ?>
  </div>
<?php endif; ?>

<div class="card">
  <small>
    Si esto te da HTTP 404/connection refused, el problema no es PHP: es que Ollama no está escuchando en esa URL/puerto
    o no permite conexiones desde el contexto donde corre Apache.
  </small>
</div>

</body>
</html>
```

### cerrar prompt
<small>Creado: 2026-01-19 16:28</small>

`003-cerrar prompt.php`

```
<?php
function h($s): string { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

$defaultPrompt = "";
$model   = $_POST["model"]   ?? "llama3:latest";
$prompt  = $_POST["prompt"]  ?? $defaultPrompt;
$baseUrl = $_POST["baseUrl"] ?? "http://127.0.0.1:11434"; // Ollama server

$result = null;

if ($_SERVER["REQUEST_METHOD"] === "POST") {
  $prompt = trim("Eres un consejero dietético. El usuario te va a proporcionar una serie de ingrediente que tiene un nevera. Debes elaborar una receta dietética, lo más saludable y sabrosa posible, con los ingredientes que el usuario te proporcione, que son estos: ".$prompt);
  if ($prompt === "") $prompt = $defaultPrompt;

  $payload = [
    "model"  => $model,
    "prompt" => $prompt,
    "stream" => false
  ];

  $url = rtrim($baseUrl, "/") . "/api/generate";

  $ch = curl_init($url);
  curl_setopt_array($ch, [
    CURLOPT_POST           => true,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER     => ["Content-Type: application/json"],
    CURLOPT_POSTFIELDS     => json_encode($payload, JSON_UNESCAPED_UNICODE),
    CURLOPT_CONNECTTIMEOUT => 5,
    CURLOPT_TIMEOUT        => 90,
  ]);

  $raw = curl_exec($ch);
  $httpCode = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
  $curlErr  = curl_error($ch);
  curl_close($ch);

  if ($raw === false) {
    $result = ["ok" => false, "err" => "cURL error: " . $curlErr, "out" => ""];
  } elseif ($httpCode < 200 || $httpCode >= 300) {
    $result = ["ok" => false, "err" => "HTTP $httpCode\n$raw", "out" => ""];
  } else {
    $json = json_decode($raw, true);
    if (!is_array($json)) {
      $result = ["ok" => false, "err" => "Respuesta no-JSON:\n$raw", "out" => ""];
    } else {
      // Ollama devuelve normalmente {"response": "...", "done": true, ...}
      $result = ["ok" => true, "out" => (string)($json["response"] ?? ""), "err" => ""];
    }
  }
}
?>
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ollama Web (PHP → HTTP API)</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Arial,sans-serif;max-width:900px;margin:40px auto;padding:0 16px;line-height:1.4}
    .card{border:1px solid #e5e5e5;border-radius:12px;padding:16px;margin:16px 0}
    label{display:block;font-weight:600;margin:10px 0 6px}
    textarea,input{width:100%;padding:10px;border:1px solid #d6d6d6;border-radius:10px;font:inherit}
    textarea{min-height:140px}
    button{padding:10px 14px;border:0;border-radius:10px;cursor:pointer;font-weight:600}
    .row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    pre{white-space:pre-wrap;word-wrap:break-word;background:#0b0b0b;color:#f1f1f1;padding:12px;border-radius:12px;overflow:auto}
    .err{background:#fff3f3;border:1px solid #ffd0d0;color:#7a0000;padding:12px;border-radius:12px}
    @media (max-width:700px){.row{grid-template-columns:1fr}}
    .row{display:none;}
  </style>
</head>
<body>

<h1>Ollama Web (PHP → HTTP API)</h1>

<div class="card">
  <form method="post">
    <div class="row">
      <div>
        <label for="model">Modelo</label>
        <input id="model" name="model" value="<?=h($model)?>" placeholder="llama3:latest">
      </div>
      <div>
        <label for="baseUrl">Ollama URL</label>
        <input id="baseUrl" name="baseUrl" value="<?=h($baseUrl)?>" placeholder="http://127.0.0.1:11434">
      </div>
    </div>
    <p>Vamos a crear recetas saludables - a continuación indica los alimentos que tienes en la nevera<br>
    La inteligencia artificial te creará recetas saludables con ellos.</p>
    <label for="prompt">Indica qué alimentos tienes en tu cocina:</label>
    <textarea id="prompt" name="prompt"><?=h($prompt)?></textarea>

    <div style="margin-top:12px;">
      <button type="submit">Preguntar</button>
    </div>
  </form>
</div>

<?php if ($result !== null): ?>
  <div class="card">
    <h2>Respuesta</h2>
    <?php if (!$result["ok"]): ?>
      <div class="err"><?=nl2br(h($result["err"]))?></div>
    <?php else: ?>
      <pre><?=h($result["out"])?></pre>
    <?php endif; ?>
  </div>
<?php endif; ?>

<div class="card">
  <small>
    Si esto te da HTTP 404/connection refused, el problema no es PHP: es que Ollama no está escuchando en esa URL/puerto
    o no permite conexiones desde el contexto donde corre Apache.
  </small>
</div>

</body>
</html>
```

### aconsejador de equipos informaticos
<small>Creado: 2026-01-19 16:28</small>

`004-aconsejador de equipos informaticos.php`

```
<?php
function h($s): string { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

$defaultPrompt = "";
$model   = $_POST["model"]   ?? "llama3:latest";
$prompt  = $_POST["prompt"]  ?? $defaultPrompt;
$baseUrl = $_POST["baseUrl"] ?? "http://127.0.0.1:11434"; // Ollama server

$result = null;

if ($_SERVER["REQUEST_METHOD"] === "POST") {
  $prompt = trim("Eres un consejero informático. El usuario te va a indicar el presupuesto económico que tiene, y para qué quiere usar su ordenador. Debes detallar los componentes que el usuario debe adquirir, su precio aproximado y luego la suma del total (importante - calcula realmente el total de la suma de los componentes): ".$prompt);
  if ($prompt === "") $prompt = $defaultPrompt;

  $payload = [
    "model"  => $model,
    "prompt" => $prompt,
    "stream" => false
  ];

  $url = rtrim($baseUrl, "/") . "/api/generate";

  $ch = curl_init($url);
  curl_setopt_array($ch, [
    CURLOPT_POST           => true,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER     => ["Content-Type: application/json"],
    CURLOPT_POSTFIELDS     => json_encode($payload, JSON_UNESCAPED_UNICODE),
    CURLOPT_CONNECTTIMEOUT => 5,
    CURLOPT_TIMEOUT        => 90,
  ]);

  $raw = curl_exec($ch);
  $httpCode = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
  $curlErr  = curl_error($ch);
  curl_close($ch);

  if ($raw === false) {
    $result = ["ok" => false, "err" => "cURL error: " . $curlErr, "out" => ""];
  } elseif ($httpCode < 200 || $httpCode >= 300) {
    $result = ["ok" => false, "err" => "HTTP $httpCode\n$raw", "out" => ""];
  } else {
    $json = json_decode($raw, true);
    if (!is_array($json)) {
      $result = ["ok" => false, "err" => "Respuesta no-JSON:\n$raw", "out" => ""];
    } else {
      // Ollama devuelve normalmente {"response": "...", "done": true, ...}
      $result = ["ok" => true, "out" => (string)($json["response"] ?? ""), "err" => ""];
    }
  }
}
?>
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ollama Web (PHP → HTTP API)</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Arial,sans-serif;max-width:900px;margin:40px auto;padding:0 16px;line-height:1.4}
    .card{border:1px solid #e5e5e5;border-radius:12px;padding:16px;margin:16px 0}
    label{display:block;font-weight:600;margin:10px 0 6px}
    textarea,input{width:100%;padding:10px;border:1px solid #d6d6d6;border-radius:10px;font:inherit}
    textarea{min-height:140px}
    button{padding:10px 14px;border:0;border-radius:10px;cursor:pointer;font-weight:600}
    .row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    pre{white-space:pre-wrap;word-wrap:break-word;background:#0b0b0b;color:#f1f1f1;padding:12px;border-radius:12px;overflow:auto}
    .err{background:#fff3f3;border:1px solid #ffd0d0;color:#7a0000;padding:12px;border-radius:12px}
    @media (max-width:700px){.row{grid-template-columns:1fr}}
    .row{display:none;}
  </style>
</head>
<body>

<h1>Ollama Web (PHP → HTTP API)</h1>

<div class="card">
  <form method="post">
    <div class="row">
      <div>
        <label for="model">Modelo</label>
        <input id="model" name="model" value="<?=h($model)?>" placeholder="llama3:latest">
      </div>
      <div>
        <label for="baseUrl">Ollama URL</label>
        <input id="baseUrl" name="baseUrl" value="<?=h($baseUrl)?>" placeholder="http://127.0.0.1:11434">
      </div>
    </div>
    <p>Esta IA te va a ayudar a seleccionar los componentes de un ordenador.</p>
    <label for="prompt">Indica qué presupuesto tienes y la finalidad de tu ordenador:</label>
    <textarea id="prompt" name="prompt"><?=h($prompt)?></textarea>

    <div style="margin-top:12px;">
      <button type="submit">Preguntar</button>
    </div>
  </form>
</div>

<?php if ($result !== null): ?>
  <div class="card">
    <h2>Respuesta</h2>
    <?php if (!$result["ok"]): ?>
      <div class="err"><?=nl2br(h($result["err"]))?></div>
    <?php else: ?>
      <pre><?=h($result["out"])?></pre>
    <?php endif; ?>
  </div>
<?php endif; ?>



</body>
</html>
```

### mejoras estéticas
<small>Creado: 2026-01-19 16:28</small>

`005-mejoras estéticas.php`

```
<?php
function h($s): string { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

/**
 * Markdown -> HTML (seguro)
 * - Escapa HTML primero (evita inyección)
 * - Soporta: #..######, **bold**, *italic*, `code`, ```fenced code```, listas -, *, 1., párrafos
 */
function md_to_html_safe(string $md): string {
  $md = str_replace(["\r\n", "\r"], "\n", $md);
  $md = h($md);

  // Fenced code blocks ```lang?\n...\n```
  $md = preg_replace_callback('/```([a-zA-Z0-9_-]+)?\n([\s\S]*?)\n```/m', function($m){
    $lang = trim((string)($m[1] ?? ""));
    $code = (string)($m[2] ?? "");
    $class = $lang !== "" ? ' class="language-'.h($lang).'"' : '';
    return '<pre class="code"><code'.$class.'>'.$code.'</code></pre>';
  }, $md);

  // Headings
  for ($i = 6; $i >= 1; $i--) {
    $md = preg_replace('/^' . str_repeat('#', $i) . '\s+(.+)$/m', "<h$i>$1</h$i>", $md);
  }

  // Inline code
  $md = preg_replace('/`([^`\n]+)`/', '<code class="inline">$1</code>', $md);

  // Bold / italic (simple)
  $md = preg_replace('/\*\*([^*\n]+)\*\*/', '<strong>$1</strong>', $md);
  $md = preg_replace('/\*([^*\n]+)\*/', '<em>$1</em>', $md);

  // Unordered lists (- or *)
  $md = preg_replace_callback('/(?:^|\n)(?:- |\* ).+(?:\n(?:- |\* ).+)*/m', function($m){
    $block = trim($m[0], "\n");
    $lines = preg_split("/\n/", $block);
    $items = [];
    foreach ($lines as $ln) {
      $ln = preg_replace('/^(?:- |\* )/', '', $ln);
      $items[] = "<li>$ln</li>";
    }
    return "\n<ul>\n" . implode("\n", $items) . "\n</ul>\n";
  }, $md);

  // Ordered lists (1. 2. ...)
  $md = preg_replace_callback('/(?:^|\n)(?:\d+\. ).+(?:\n(?:\d+\. ).+)*/m', function($m){
    $block = trim($m[0], "\n");
    $lines = preg_split("/\n/", $block);
    $items = [];
    foreach ($lines as $ln) {
      $ln = preg_replace('/^\d+\. /', '', $ln);
      $items[] = "<li>$ln</li>";
    }
    return "\n<ol>\n" . implode("\n", $items) . "\n</ol>\n";
  }, $md);

  // Paragraphs: split by blank lines, wrap non-blocks
  $parts = preg_split("/\n{2,}/", $md);
  $out = [];
  foreach ($parts as $p) {
    $p = trim($p);
    if ($p === "") continue;

    // If it starts with a block tag, keep as-is
    if (preg_match('/^(<h[1-6]>|<ul>|<ol>|<pre\b)/', $p)) {
      $out[] = $p;
    } else {
      // Preserve single newlines inside paragraphs
      $p = preg_replace("/\n/", "<br>", $p);
      $out[] = "<p>$p</p>";
    }
  }

  return implode("\n", $out);
}

$defaultPrompt = "";
$model   = $_POST["model"]   ?? "llama3:latest";
$prompt  = $_POST["prompt"]  ?? $defaultPrompt;
$baseUrl = $_POST["baseUrl"] ?? "http://127.0.0.1:11434"; // Ollama server

$result = null;

if ($_SERVER["REQUEST_METHOD"] === "POST") {
  $prompt = trim("Eres un consejero informático. El usuario te va a indicar el presupuesto económico que tiene, y para qué quiere usar su ordenador. Debes detallar los componentes que el usuario debe adquirir, su precio aproximado y luego la suma del total (importante - calcula realmente el total de la suma de los componentes): ".$prompt);
  if ($prompt === "") $prompt = $defaultPrompt;

  $payload = [
    "model"  => $model,
    "prompt" => $prompt,
    "stream" => false
  ];

  $url = rtrim($baseUrl, "/") . "/api/generate";

  $ch = curl_init($url);
  curl_setopt_array($ch, [
    CURLOPT_POST           => true,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER     => ["Content-Type: application/json"],
    CURLOPT_POSTFIELDS     => json_encode($payload, JSON_UNESCAPED_UNICODE),
    CURLOPT_CONNECTTIMEOUT => 5,
    CURLOPT_TIMEOUT        => 90,
  ]);

  $raw = curl_exec($ch);
  $httpCode = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
  $curlErr  = curl_error($ch);
  curl_close($ch);

  if ($raw === false) {
    $result = ["ok" => false, "err" => "cURL error: " . $curlErr, "out" => ""];
  } elseif ($httpCode < 200 || $httpCode >= 300) {
    $result = ["ok" => false, "err" => "HTTP $httpCode\n$raw", "out" => ""];
  } else {
    $json = json_decode($raw, true);
    if (!is_array($json)) {
      $result = ["ok" => false, "err" => "Respuesta no-JSON:\n$raw", "out" => ""];
    } else {
      $result = ["ok" => true, "out" => (string)($json["response"] ?? ""), "err" => ""];
    }
  }
}
?>
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ollama Web (PHP → HTTP API)</title>
  <style>
    :root{
      --bg: #0b1020;
      --panel: rgba(255,255,255,.06);
      --panel2: rgba(255,255,255,.08);
      --border: rgba(255,255,255,.12);
      --text: rgba(255,255,255,.92);
      --muted: rgba(255,255,255,.68);
      --accent: #7dd3fc; /* cyan-300 */
      --accent2: #a78bfa; /* violet-400 */
      --dangerBg: rgba(255,80,80,.12);
      --dangerBorder: rgba(255,80,80,.35);
      --dangerText: #ffd6d6;
      --shadow: 0 20px 60px rgba(0,0,0,.45);
      --radius: 16px;
    }

    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Arial, sans-serif;
      background:
        radial-gradient(1200px 700px at 10% 10%, rgba(125,211,252,.14), transparent 55%),
        radial-gradient(1000px 650px at 85% 20%, rgba(167,139,250,.12), transparent 60%),
        radial-gradient(900px 600px at 40% 95%, rgba(34,197,94,.08), transparent 55%),
        var(--bg);
      color: var(--text);
    }

    .app{
      height:100vh;
      width:100vw;
      display:grid;
      grid-template-columns: minmax(340px, 420px) 1fr;
      gap: 14px;
      padding: 14px;
    }

    .panel{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow:hidden;
      display:flex;
      flex-direction:column;
      min-height:0;
    }

    .panelHeader{
      padding: 14px 16px;
      border-bottom: 1px solid var(--border);
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap: 10px;
      background: linear-gradient(to bottom, rgba(255,255,255,.06), rgba(255,255,255,.03));
    }

    .brand{
      display:flex; align-items:center; gap:10px;
      min-width:0;
    }
    .dot{
      width:12px;height:12px;border-radius:999px;
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      box-shadow: 0 0 0 4px rgba(125,211,252,.12);
      flex: 0 0 auto;
    }
    .brand h1{
      font-size: 14px;
      margin:0;
      letter-spacing:.2px;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }
    .brand p{
      margin:0;
      font-size: 12px;
      color: var(--muted);
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    .toolbar{
      display:flex; gap:8px; align-items:center;
      flex: 0 0 auto;
    }

    .btn{
      appearance:none;
      border:1px solid var(--border);
      background: rgba(255,255,255,.06);
      color: var(--text);
      padding: 10px 12px;
      border-radius: 12px;
      cursor:pointer;
      font-weight: 650;
      transition: transform .05s ease, background .15s ease, border-color .15s ease;
      user-select:none;
    }
    .btn:hover{background: rgba(255,255,255,.10); border-color: rgba(255,255,255,.18)}
    .btn:active{transform: translateY(1px)}
    .btnPrimary{
      border-color: rgba(125,211,252,.35);
      background: linear-gradient(135deg, rgba(125,211,252,.18), rgba(167,139,250,.14));
    }

    .content{
      padding: 14px 16px;
      overflow:auto;
      min-height:0;
    }

    label{
      display:block;
      margin: 12px 0 6px;
      font-weight: 700;
      font-size: 12px;
      color: rgba(255,255,255,.80);
      letter-spacing:.2px;
    }

    textarea, input{
      width:100%;
      background: rgba(0,0,0,.18);
      border: 1px solid rgba(255,255,255,.14);
      color: var(--text);
      border-radius: 14px;
      padding: 12px 12px;
      font: inherit;
      outline: none;
      transition: border-color .15s ease, background .15s ease;
    }
    textarea:focus, input:focus{
      border-color: rgba(125,211,252,.45);
      background: rgba(0,0,0,.22);
    }
    textarea{min-height: 42vh; resize: vertical}

    .hint{
      margin: 10px 0 0;
      font-size: 12px;
      color: var(--muted);
      line-height: 1.45;
    }

    details{
      margin-top: 12px;
      border: 1px solid rgba(255,255,255,.12);
      border-radius: 14px;
      background: rgba(255,255,255,.04);
      overflow:hidden;
    }
    summary{
      cursor:pointer;
      list-style:none;
      padding: 12px 12px;
      font-weight: 700;
      font-size: 12px;
      color: rgba(255,255,255,.85);
    }
    summary::-webkit-details-marker{display:none}
    .settings{
      padding: 0 12px 12px;
      display:grid;
      grid-template-columns: 1fr;
      gap: 10px;
    }

    /* RIGHT PANEL (response) */
    .responseWrap{
      display:flex;
      flex-direction:column;
      min-height:0;
    }

    .responseBody{
      padding: 14px 16px;
      overflow:auto;
      min-height:0;
    }

    .responseCard{
      background: rgba(0,0,0,.55);
      border: 1px solid rgba(255,255,255,.14);
      border-radius: var(--radius);
      box-shadow: inset 0 0 0 1px rgba(255,255,255,.03);
      overflow:hidden;
    }

    .responseHead{
      padding: 12px 14px;
      border-bottom: 1px solid rgba(255,255,255,.12);
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap: 10px;
      background: linear-gradient(to bottom, rgba(255,255,255,.06), rgba(255,255,255,.02));
    }

    .responseTitle{
      display:flex; align-items:center; gap:10px; min-width:0;
    }
    .badge{
      font-size: 11px;
      padding: 6px 10px;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,.16);
      color: rgba(255,255,255,.82);
      background: rgba(255,255,255,.06);
      white-space:nowrap;
    }

    /* Markdown typography */
    .md{
      padding: 16px 16px 18px;
      line-height: 1.65;
      color: rgba(255,255,255,.92);
      font-size: 15px;
    }
    .md h1,.md h2,.md h3,.md h4,.md h5,.md h6{
      margin: 16px 0 10px;
      line-height: 1.2;
      letter-spacing:.2px;
    }
    .md h1{font-size: 22px}
    .md h2{font-size: 18px}
    .md h3{font-size: 16px}
    .md p{margin: 10px 0}
    .md ul,.md ol{margin: 10px 0 10px 22px}
    .md li{margin: 6px 0}
    .md strong{color: rgba(255,255,255,.98)}
    .md em{color: rgba(255,255,255,.86)}
    .md code.inline{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
      font-size: .95em;
      padding: 2px 6px;
      border-radius: 8px;
      border: 1px solid rgba(255,255,255,.14);
      background: rgba(255,255,255,.06);
      color: rgba(255,255,255,.92);
    }
    .md pre.code{
      margin: 12px 0;
      padding: 12px 12px;
      border-radius: 14px;
      background: rgba(0,0,0,.55);
      border: 1px solid rgba(255,255,255,.14);
      overflow:auto;
    }
    .md pre.code code{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
      font-size: 13px;
      white-space: pre;
      display:block;
      color: rgba(255,255,255,.90);
    }

    .emptyState{
      height:100%;
      display:flex;
      align-items:center;
      justify-content:center;
      padding: 28px;
      text-align:center;
      color: var(--muted);
    }
    .emptyState .box{
      max-width: 520px;
      border: 1px dashed rgba(255,255,255,.18);
      border-radius: var(--radius);
      padding: 22px 18px;
      background: rgba(255,255,255,.03);
    }

    .err{
      margin: 14px 16px 16px;
      background: var(--dangerBg);
      border: 1px solid var(--dangerBorder);
      color: var(--dangerText);
      padding: 12px 12px;
      border-radius: 14px;
      white-space: pre-wrap;
      word-wrap: break-word;
    }

    /* Responsive */
    @media (max-width: 980px){
      .app{grid-template-columns: 1fr; height:auto; min-height:100vh}
      textarea{min-height: 32vh}
    }
  </style>
</head>
<body>

<div class="app">

  <!-- LEFT: FORM -->
  <section class="panel">
    <div class="panelHeader">
      <div class="brand">
        <span class="dot" aria-hidden="true"></span>
        <div style="min-width:0">
          <h1>Ollama Web</h1>
          <p>Componentes PC por presupuesto y uso</p>
        </div>
      </div>
      <div class="toolbar">
        <button class="btn" type="button" id="clearBtn" title="Limpiar formulario">Limpiar</button>
        <button class="btn btnPrimary" type="button" id="submitBtn" title="Enviar consulta">Enviar</button>
      </div>
    </div>

    <div class="content">
      <form method="post" id="theForm">
        <p class="hint">
          Indica <strong>presupuesto</strong> (p. ej. 900€) y <strong>uso</strong> (ofimática, edición de vídeo, IA, gaming, etc.).
          La respuesta se mostrará a la derecha con formato legible.
        </p>

        <label for="prompt">Tu petición</label>
        <textarea id="prompt" name="prompt" placeholder="Ejemplo: Tengo 1200€ y lo quiero para edición de vídeo 4K y algo de gaming."><?=h($prompt)?></textarea>

        <details>
          <summary>Ajustes (modelo y URL)</summary>
          <div class="settings">
            <div>
              <label for="model">Modelo</label>
              <input id="model" name="model" value="<?=h($model)?>" placeholder="llama3:latest">
            </div>
            <div>
              <label for="baseUrl">Ollama URL</label>
              <input id="baseUrl" name="baseUrl" value="<?=h($baseUrl)?>" placeholder="http://127.0.0.1:11434">
            </div>
          </div>
        </details>

        <!-- submit real (hidden) -->
        <button type="submit" style="display:none" aria-hidden="true" tabindex="-1"></button>
      </form>
    </div>
  </section>

  <!-- RIGHT: RESPONSE -->
  <section class="panel responseWrap">
    <div class="panelHeader">
      <div class="brand">
        <span class="dot" aria-hidden="true"></span>
        <div style="min-width:0">
          <h1>Respuesta</h1>
          <p>Render Markdown → HTML</p>
        </div>
      </div>
      <div class="toolbar">
        <span class="badge"><?=h($model)?></span>
      </div>
    </div>

    <div class="responseBody">
      <div class="responseCard">
        <div class="responseHead">
          <div class="responseTitle">
            <span class="badge">Salida</span>
            <?php if ($result !== null): ?>
              <span class="badge"><?= $result["ok"] ? "OK" : "ERROR" ?></span>
            <?php else: ?>
              <span class="badge">Sin consulta</span>
            <?php endif; ?>
          </div>
          <button class="btn" type="button" id="copyBtn" title="Copiar respuesta">Copiar</button>
        </div>

        <?php if ($result === null): ?>
          <div class="emptyState">
            <div class="box">
              Escribe tu presupuesto y el uso del ordenador en el panel izquierdo y pulsa <strong>Enviar</strong>.
            </div>
          </div>
        <?php elseif (!$result["ok"]): ?>
          <div class="err"><?=h($result["err"])?></div>
        <?php else: ?>
          <div class="md" id="mdOut">
            <?= md_to_html_safe($result["out"]) ?>
          </div>
        <?php endif; ?>
      </div>
    </div>
  </section>

</div>

<script>
  const form = document.getElementById('theForm');
  const submitBtn = document.getElementById('submitBtn');
  const clearBtn  = document.getElementById('clearBtn');
  const promptEl  = document.getElementById('prompt');
  const copyBtn   = document.getElementById('copyBtn');

  submitBtn.addEventListener('click', () => form.requestSubmit());

  clearBtn.addEventListener('click', () => {
    promptEl.value = '';
    promptEl.focus();
  });

  copyBtn.addEventListener('click', async () => {
    const mdOut = document.getElementById('mdOut');
    if (!mdOut) return;
    const text = mdOut.innerText;
    try{
      await navigator.clipboard.writeText(text);
      copyBtn.textContent = 'Copiado';
      setTimeout(() => copyBtn.textContent = 'Copiar', 900);
    }catch(e){
      copyBtn.textContent = 'No se pudo';
      setTimeout(() => copyBtn.textContent = 'Copiar', 900);
    }
  });

  // Si hay respuesta, sube al principio del panel derecho (mejor lectura)
  const mdOut = document.getElementById('mdOut');
  if (mdOut) {
    mdOut.scrollIntoView({block:'start'});
  }
</script>

</body>
</html>
```

### interfaz clara
<small>Creado: 2026-01-19 16:28</small>

`006-interfaz clara.php`

```
<?php
function h($s): string { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

/**
 * Markdown -> HTML (safe, minimal)
 */
function md_to_html_safe(string $md): string {
  $md = str_replace(["\r\n", "\r"], "\n", $md);
  $md = h($md);

  // fenced code
  $md = preg_replace_callback('/```([a-zA-Z0-9_-]+)?\n([\s\S]*?)\n```/m', function($m){
    $lang = trim((string)($m[1] ?? ""));
    $code = (string)($m[2] ?? "");
    $class = $lang !== "" ? ' class="language-'.h($lang).'"' : '';
    return '<pre class="code"><code'.$class.'>'.$code.'</code></pre>';
  }, $md);

  // headings
  for ($i = 6; $i >= 1; $i--) {
    $md = preg_replace('/^' . str_repeat('#', $i) . '\s+(.+)$/m', "<h$i>$1</h$i>", $md);
  }

  // inline code / bold / italic (simple)
  $md = preg_replace('/`([^`\n]+)`/', '<code class="inline">$1</code>', $md);
  $md = preg_replace('/\*\*([^*\n]+)\*\*/', '<strong>$1</strong>', $md);
  $md = preg_replace('/\*([^*\n]+)\*/', '<em>$1</em>', $md);

  // ul
  $md = preg_replace_callback('/(?:^|\n)(?:- |\* ).+(?:\n(?:- |\* ).+)*/m', function($m){
    $block = trim($m[0], "\n");
    $lines = preg_split("/\n/", $block);
    $items = [];
    foreach ($lines as $ln) {
      $ln = preg_replace('/^(?:- |\* )/', '', $ln);
      $items[] = "<li>$ln</li>";
    }
    return "\n<ul>\n" . implode("\n", $items) . "\n</ul>\n";
  }, $md);

  // ol
  $md = preg_replace_callback('/(?:^|\n)(?:\d+\. ).+(?:\n(?:\d+\. ).+)*/m', function($m){
    $block = trim($m[0], "\n");
    $lines = preg_split("/\n/", $block);
    $items = [];
    foreach ($lines as $ln) {
      $ln = preg_replace('/^\d+\. /', '', $ln);
      $items[] = "<li>$ln</li>";
    }
    return "\n<ol>\n" . implode("\n", $items) . "\n</ol>\n";
  }, $md);

  // paragraphs
  $parts = preg_split("/\n{2,}/", $md);
  $out = [];
  foreach ($parts as $p) {
    $p = trim($p);
    if ($p === "") continue;

    if (preg_match('/^(<h[1-6]>|<ul>|<ol>|<pre\b)/', $p)) {
      $out[] = $p;
    } else {
      $p = preg_replace("/\n/", "<br>", $p);
      $out[] = "<p>$p</p>";
    }
  }
  return implode("\n", $out);
}

$defaultPrompt = "";
$model   = $_POST["model"]   ?? "llama3:latest";
$prompt  = $_POST["prompt"]  ?? $defaultPrompt;
$baseUrl = $_POST["baseUrl"] ?? "http://127.0.0.1:11434";

$result = null;

if ($_SERVER["REQUEST_METHOD"] === "POST") {
  $userPrompt = trim($prompt);
  if ($userPrompt === "") $userPrompt = $defaultPrompt;

  // Prompt reforzado: exige tabla con números + suma verificada
  $systemPrompt = <<<TXT
Eres un asesor informático. El usuario te dará un presupuesto y el uso del PC.

Tu respuesta DEBE cumplir estas reglas:
1) Propón una configuración por componentes (CPU, placa, RAM, GPU si aplica, SSD, PSU, caja, disipación si aplica).
2) Para cada componente indica un precio aproximado en EUR como número (sin rangos; un único valor).
3) Incluye una tabla final "DESGLOSE" con columnas: Componente | Modelo | Precio_EUR.
4) Después incluye un bloque "SUMA" con:
   - Lista de precios usados (solo números) en una línea.
   - Total_EUR = suma exacta de esos números.
5) Vuelve a comprobar la suma: repite el total en una segunda línea "Total_verificado_EUR" y debe coincidir.
6) Si el total supera el presupuesto, ajusta componentes hasta que Total_EUR <= presupuesto y deja margen para envío (si procede).
7) No inventes monedas ni uses USD. No uses notación ambigua. No uses "aprox. 300-350". Solo un número.

Usuario:
{$userPrompt}
TXT;

  $payload = [
    "model"  => $model,
    "prompt" => $systemPrompt,
    "stream" => false
  ];

  $url = rtrim($baseUrl, "/") . "/api/generate";

  $ch = curl_init($url);
  curl_setopt_array($ch, [
    CURLOPT_POST           => true,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER     => ["Content-Type: application/json"],
    CURLOPT_POSTFIELDS     => json_encode($payload, JSON_UNESCAPED_UNICODE),
    CURLOPT_CONNECTTIMEOUT => 5,
    CURLOPT_TIMEOUT        => 90,
  ]);

  $raw = curl_exec($ch);
  $httpCode = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
  $curlErr  = curl_error($ch);
  curl_close($ch);

  if ($raw === false) {
    $result = ["ok" => false, "err" => "cURL error: " . $curlErr, "out" => ""];
  } elseif ($httpCode < 200 || $httpCode >= 300) {
    $result = ["ok" => false, "err" => "HTTP $httpCode\n$raw", "out" => ""];
  } else {
    $json = json_decode($raw, true);
    if (!is_array($json)) {
      $result = ["ok" => false, "err" => "Respuesta no-JSON:\n$raw", "out" => ""];
    } else {
      $result = ["ok" => true, "out" => (string)($json["response"] ?? ""), "err" => ""];
    }
  }
}
?>
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ollama Web</title>
  <style>
    :root{
      --bg: #f6f7f9;
      --panel: #ffffff;
      --border: #e6e8ee;
      --text: #111827;
      --muted: #6b7280;
      --accent: #2563eb;   /* blue */
      --accent2:#111827;   /* near-black */
      --shadow: 0 8px 24px rgba(17,24,39,.08);
      --radius: 14px;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
    }

    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
    }

    .app{
      height:100vh;
      width:100vw;
      display:grid;
      grid-template-columns: minmax(320px, 420px) 1fr;
      gap: 14px;
      padding: 14px;
    }

    .panel{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow:hidden;
      display:flex;
      flex-direction:column;
      min-height:0;
    }

    .panelHeader{
      padding: 14px 16px;
      border-bottom: 1px solid var(--border);
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap: 12px;
      background: #fff;
    }

    .brand{
      display:flex; align-items:baseline; gap:10px; min-width:0;
    }
    .brand h1{
      font-size: 14px;
      margin:0;
      letter-spacing:.2px;
      font-weight: 750;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }
    .brand p{
      margin:0;
      font-size: 12px;
      color: var(--muted);
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    .toolbar{display:flex; gap:8px; align-items:center}

    .btn{
      appearance:none;
      border:1px solid var(--border);
      background: #fff;
      color: var(--text);
      padding: 10px 12px;
      border-radius: 12px;
      cursor:pointer;
      font-weight: 700;
      transition: background .15s ease, border-color .15s ease, transform .05s ease;
      user-select:none;
    }
    .btn:hover{background:#f3f4f6}
    .btn:active{transform: translateY(1px)}
    .btnPrimary{
      background: var(--accent);
      color: #fff;
      border-color: rgba(37,99,235,.35);
    }
    .btnPrimary:hover{background:#1d4ed8}

    .content{
      padding: 14px 16px;
      overflow:auto;
      min-height:0;
    }

    label{
      display:block;
      margin: 12px 0 6px;
      font-weight: 750;
      font-size: 12px;
      color: var(--accent2);
      letter-spacing:.2px;
    }

    textarea, input{
      width:100%;
      background: #fff;
      border: 1px solid var(--border);
      color: var(--text);
      border-radius: 12px;
      padding: 12px 12px;
      font: inherit;
      outline: none;
      transition: border-color .15s ease, box-shadow .15s ease;
    }
    textarea:focus, input:focus{
      border-color: rgba(37,99,235,.55);
      box-shadow: 0 0 0 4px rgba(37,99,235,.10);
    }
    textarea{min-height: 44vh; resize: vertical}

    .hint{
      margin: 8px 0 0;
      font-size: 12px;
      color: var(--muted);
      line-height: 1.5;
    }

    details{
      margin-top: 12px;
      border: 1px solid var(--border);
      border-radius: 12px;
      background: #fff;
      overflow:hidden;
    }
    summary{
      cursor:pointer;
      list-style:none;
      padding: 12px 12px;
      font-weight: 750;
      font-size: 12px;
      color: var(--text);
    }
    summary::-webkit-details-marker{display:none}
    .settings{
      padding: 0 12px 12px;
      display:grid;
      grid-template-columns: 1fr;
      gap: 10px;
    }

    .badge{
      font-size: 11px;
      padding: 6px 10px;
      border-radius: 999px;
      border: 1px solid var(--border);
      color: var(--muted);
      background: #fff;
      white-space:nowrap;
    }

    .responseCard{
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow:hidden;
      background:#fff;
    }

    .responseHead{
      padding: 12px 14px;
      border-bottom: 1px solid var(--border);
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap: 10px;
      background:#fff;
    }

    .md{
      padding: 16px 16px 18px;
      line-height: 1.7;
      color: var(--text);
      font-size: 15px;
    }
    .md h1,.md h2,.md h3,.md h4,.md h5,.md h6{
      margin: 16px 0 10px;
      line-height: 1.2;
    }
    .md h1{font-size: 22px}
    .md h2{font-size: 18px}
    .md h3{font-size: 16px}
    .md p{margin: 10px 0}
    .md ul,.md ol{margin: 10px 0 10px 22px}
    .md li{margin: 6px 0}
    .md code.inline{
      font-family: var(--mono);
      font-size: .95em;
      padding: 2px 6px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: #f9fafb;
    }
    .md pre.code{
      margin: 12px 0;
      padding: 12px 12px;
      border-radius: 12px;
      background: #0b1220;
      border: 1px solid #0b1220;
      overflow:auto;
    }
    .md pre.code code{
      font-family: var(--mono);
      font-size: 13px;
      white-space: pre;
      display:block;
      color: #e5e7eb;
    }

    .emptyState{
      padding: 28px;
      text-align:center;
      color: var(--muted);
    }
    .emptyState .box{
      max-width: 520px;
      margin: 0 auto;
      border: 1px dashed var(--border);
      border-radius: var(--radius);
      padding: 18px 16px;
      background: #fafafa;
    }

    .err{
      margin: 14px 16px 16px;
      background: #fff1f2;
      border: 1px solid #fecdd3;
      color: #7f1d1d;
      padding: 12px 12px;
      border-radius: 12px;
      white-space: pre-wrap;
      word-wrap: break-word;
    }

    @media (max-width: 980px){
      .app{grid-template-columns: 1fr; height:auto; min-height:100vh}
      textarea{min-height: 32vh}
    }
  </style>
</head>
<body>

<div class="app">

  <!-- LEFT -->
  <section class="panel">
    <div class="panelHeader">
      <div class="brand">
        <h1>Ollama Web</h1>
        <p>Configuración PC</p>
      </div>
      <div class="toolbar">
        <button class="btn" type="button" id="clearBtn">Limpiar</button>
        <button class="btn btnPrimary" type="button" id="submitBtn">Enviar</button>
      </div>
    </div>

    <div class="content">
      <form method="post" id="theForm">
        <p class="hint">
          Escribe presupuesto (EUR) + uso. Ej.: “1200€ edición 4K + gaming 1440p”.
        </p>

        <label for="prompt">Petición</label>
        <textarea id="prompt" name="prompt"><?=h($prompt)?></textarea>

        <details>
          <summary>Ajustes</summary>
          <div class="settings">
            <div>
              <label for="model">Modelo</label>
              <input id="model" name="model" value="<?=h($model)?>" placeholder="llama3:latest">
            </div>
            <div>
              <label for="baseUrl">Ollama URL</label>
              <input id="baseUrl" name="baseUrl" value="<?=h($baseUrl)?>" placeholder="http://127.0.0.1:11434">
            </div>
          </div>
        </details>

        <button type="submit" style="display:none" aria-hidden="true" tabindex="-1"></button>
      </form>
    </div>
  </section>

  <!-- RIGHT -->
  <section class="panel">
    <div class="panelHeader">
      <div class="brand">
        <h1>Respuesta</h1>
        <p>Markdown → HTML</p>
      </div>
      <div class="toolbar">
        <span class="badge"><?=h($model)?></span>
        <button class="btn" type="button" id="copyBtn">Copiar</button>
      </div>
    </div>

    <div class="content">
      <div class="responseCard">
        <div class="responseHead">
          <span class="badge">
            <?php if ($result === null) echo "Sin consulta";
              else echo ($result["ok"] ? "OK" : "ERROR"); ?>
          </span>
        </div>

        <?php if ($result === null): ?>
          <div class="emptyState">
            <div class="box">
              Envía una consulta desde la izquierda para ver la recomendación aquí.
            </div>
          </div>
        <?php elseif (!$result["ok"]): ?>
          <div class="err"><?=h($result["err"])?></div>
        <?php else: ?>
          <div class="md" id="mdOut"><?= md_to_html_safe($result["out"]) ?></div>
        <?php endif; ?>
      </div>
    </div>
  </section>

</div>

<script>
  const form = document.getElementById('theForm');
  const submitBtn = document.getElementById('submitBtn');
  const clearBtn  = document.getElementById('clearBtn');
  const promptEl  = document.getElementById('prompt');
  const copyBtn   = document.getElementById('copyBtn');

  submitBtn.addEventListener('click', () => form.requestSubmit());
  clearBtn.addEventListener('click', () => { promptEl.value=''; promptEl.focus(); });

  copyBtn.addEventListener('click', async () => {
    const mdOut = document.getElementById('mdOut');
    if (!mdOut) return;
    try{
      await navigator.clipboard.writeText(mdOut.innerText);
      copyBtn.textContent = 'Copiado';
      setTimeout(()=>copyBtn.textContent='Copiar', 900);
    }catch(e){
      copyBtn.textContent = 'No se pudo';
      setTimeout(()=>copyBtn.textContent='Copiar', 900);
    }
  });
</script>

</body>
</html>
```



<a id="actividad-libre-de-final-de-evaluacion-la-milla-extra"></a>
# Actividad libre de final de evaluación - La milla extra

<a id="la-milla-extra-primera-evaluacion"></a>
## La Milla Extra - Primera evaluación

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/201-Actividad%20libre%20de%20final%20de%20evaluaci%C3%B3n%20-%20La%20milla%20extra/001-La%20Milla%20Extra%20-%20Primera%20evaluaci%C3%B3n)

### Introducción a los ejercicios

El archivo **ejercicio.md** en esta carpeta contiene una actividad diseñada para reforzar los conocimientos adquiridos durante el primer trimestre de la asignatura Bases de Datos. Esta tarea se centra en aplicar conceptos como la creación y manipulación de bases de datos, la gestión de relaciones entre tablas, así como consultas SQL más avanzadas. Los estudiantes practicarán habilidades esenciales como el diseño de estructuras de datos eficientes, la resolución de problemas relacionados con integridad referencial y la optimización de queries para mejorar el rendimiento del sistema.

Esta actividad está orientada a que los alumnos consoliden sus competencias en modelado relacional y programación SQL, preparándolos para proyectos más complejos en el futuro.

### Actividades propuestas

Basándome en la información proporcionada y asumiendo que el contenido del archivo `ejercicio.md` está relacionado con conceptos básicos sobre bases de datos, diseño de esquemas y posiblemente consultas SQL para estudiantes de primer curso de Ciclos Formativos (Formación Profesional), aquí tienes una lista de actividades sugeridas:

1. **Diseño de Esquema Relacional**
   - Los alumnos deben diseñar un esquema relacional para una base de datos que represente una librería o tienda de música. Se espera que aprendan a definir tablas, atributos y relaciones entre ellas.

2. **Normalización de Bases de Datos**
   - Los estudiantes deben normalizar los esquemas proporcionados en el archivo `ejercicio.md` hasta la tercera forma normal (3FN). El objetivo es mejorar la integridad y la consistencia de las bases de datos mediante técnicas de normalización.

3. **Creación de Consultas SQL Básicas**
   - Los alumnos deben escribir consultas SQL para realizar operaciones CRUD en una base de datos creada a partir del diseño de esquemas proporcionado. Se espera que aprendan cómo seleccionar, insertar y actualizar registros en las bases de datos.

4. **Creación de Tablas con Contraints**
   - Los estudiantes deben crear tablas SQL adicionales que incluyan restricciones (como claves foráneas o índices) para garantizar la integridad referencial y mejorar el rendimiento de consultas en una base de datos.

5. **Consultas JOIN Advanced**
   - Se pide a los alumnos generar consultas SQL más avanzadas utilizando operadores JOIN para combinar información entre múltiples tablas, con énfasis en INNER JOIN, LEFT JOIN y RIGHT JOIN.

6. **Creación de Procedimientos Almacenados**
   - Los estudiantes deben escribir un procedimiento almacenado que automatice la creación de un nuevo registro en una tabla específica de la base de datos basada en ciertas condiciones.

7. **Optimización de Consultas SQL**
   - Se le pide a los alumnos analizar y optimizar consultas existentes para mejorar el rendimiento, considerando el uso adecuado de índices y técnicas de normalización.

8. **Documentación del Diseño DB**
   - Los estudiantes deben documentar en detalle su diseño de base de datos, incluyendo diagramas ER (Entity-Relationship), explicaciones sobre las tablas y sus relaciones, y una breve descripción de las consultas SQL implementadas.

Estas actividades se centran en desarrollar habilidades fundamentales relacionadas con la gestión y el diseño eficaz de bases de datos para estudiantes de Formación Profesional.



<a id="actividades-de-final-de-unidad-segundo-trimestre"></a>
# Actividades de final de unidad segundo trimestre

<a id="proyecto-tienda-online-1"></a>
## Proyecto tienda online

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/202-Actividades%20de%20final%20de%20unidad%20segundo%20trimestre/001-Proyecto%20tienda%20online)


<a id="proyecto-ia-para-dietetica"></a>
## Proyecto IA para dietética

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/202-Actividades%20de%20final%20de%20unidad%20segundo%20trimestre/002-Proyecto%20IA%20para%20diet%C3%A9tica)


<a id="proyecto-scrapear-web"></a>
## Proyecto scrapear web

[📁 Ver carpeta en GitHub](https://github.com/jocarsa/dam2526/tree/main/Primero/Bases%20de%20datos/202-Actividades%20de%20final%20de%20unidad%20segundo%20trimestre/003-Proyecto%20scrapear%20web)
