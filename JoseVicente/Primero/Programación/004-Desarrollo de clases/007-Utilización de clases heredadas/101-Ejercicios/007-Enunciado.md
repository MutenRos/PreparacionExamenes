Objetivo

Crear un pequeño programa de consola que gestione dos animales (un Gato y un Perro) heredando de una clase base Animal. El programa pedirá datos al usuario, aplicará validaciones, clasificará a los animales por edad y mostrará una “ficha” de cada uno.

Requisitos funcionales

Clase base Animal

Propiedades públicas: color (cadena), edad (entero, empieza en 0).

Propiedad privada: __raza (cadena).

Constructor sin parámetros que inicialice valores por defecto.

Métodos:

setEdad(nuevaedad): solo permite incrementar la edad exactamente de uno en uno (si self.edad == nuevaedad - 1, entonces asigna; si no, imprime “operación no permitida”).

getEdad(): devuelve la edad.

setRaza(raza) y getRaza().

descripcion(): devuelve (no imprime) una cadena corta con color, edad y raza.

Añade un docstring a la clase o a algún método explicando qué hace.

Clases hijas Gato y Perro

Heredan de Animal.

Sus constructores llaman a super().__init__().

Cada una tiene un método propio:

Gato.maulla() → imprime "miau".

Perro.ladra() → imprime "guau".

Constantes y validaciones

Define constantes en MAYÚSCULAS (por ejemplo EDAD_MAX_GATO = 25, EDAD_MAX_PERRO = 30).

Aserción: al finalizar la entrada de datos, asegura con assert que ninguna edad es negativa.

Excepción: cuando leas la edad desde input(), conviértela a int dentro de un try/except. Si hay error, muestra un mensaje y pon la edad a 0.

Interacción por consola

Muestra un mensaje inicial con tu nombre (print).

Pide al usuario:

Color del gato y del perro.

Raza del gato y del perro.

Edad inicial del gato y del perro (entero).

Clasificación por edad (usar if/elif/else):

< 1 → “cachorro”

>= 1 y < 7 → “adulto joven”

>= 7 → “adulto”

Imprime la categoría para cada animal.

Bucle y operadores abreviados

Simula el paso del tiempo para el gato: usando un while, incrementa su edad con += 1 hasta alcanzar la edad que indique el usuario (p. ej., “¿hasta qué edad quieres simular?”).

Cada intento de cambio de edad debe hacerse únicamente a través de setEdad() para respetar la regla.

Funciones auxiliares

Crea una función libre formatea_ficha(animal, titulo) que devuelva una cadena multilínea con la ficha (usa el descripcion() del animal).

Crea otra función clasifica_edad(edad) que devuelva la categoría (“cachorro”, “adulto joven”, “adulto”) y reutilízala para gato y perro.

Uso básico de booleanos

Imprime si al menos uno de los dos animales es “adulto” (usa or con la clasificación).

Imprime si ambos son “cachorro” (usa and).

Recorrido de propiedades

Muestra por pantalla todas las propiedades públicas del perro recorriendo perro.__dict__ con un for y formatea clave: valor.

Salida final requerida

Fichas de Gato y Perro (devueltas por formatea_ficha(...) y luego impresas).

Categorías por edad.

Mensajes del bucle de simulación (cómo va creciendo el gato).

Resultados de las comprobaciones booleanas.

Nota: no uses listas/arrays ni ficheros.
