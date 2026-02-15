josevicente@ubuntuserver:~/dam2526$ git pull origin main
remote: Enumerating objects: 44, done.
remote: Counting objects: 100% (44/44), done.
remote: Compressing objects: 100% (31/31), done.
remote: Total 38 (delta 7), reused 38 (delta 7), pack-reused 0 (from 0)
Unpacking objects: 100% (38/38), 11.61 KiB | 125.00 KiB/s, done.
From https://github.com/jocarsa/dam2526
 * branch            main       -> FETCH_HEAD
   b9e511b..cc19c26  main       -> origin/main
Updating b9e511b..cc19c26
Fast-forward
 .../Contenidos b\303\241sicos.md"          |  0
 .../001-inicio sesion en el servidor.md    | 38 +++++++++++++++++
 .../101-Ejercicios/002-tenemos git.md      | 11 +++++
 .../003-averiguar la version.md            |  5 +++
 ...4-me conecto a git desde el servidor.md |  5 +++
 .../101-Ejercicios/005-configuracion.md    |  5 +++
 .../006-clonar repositorio.md              |  3 ++
 .../Criterios de evaluaci\303\263n.md"     |  0
 .../Contenidos b\303\241sicos.md"          |  0
 .../Criterios de evaluaci\303\263n.md"     |  0
 .../Contenidos b\303\241sicos.md"          |  0
 .../Criterios de evaluaci\303\263n.md"     |  0
 .../000-Resumen.md"                        |  0
 .../Contenidos b\303\241sicos.md"          |  0
 .../Criterios de evaluaci\303\263n.md"     |  0
 .../Contenidos b\303\241sicos.md"          | 17 ++++++++
 .../Criterios de evaluaci\303\263n.md"     |  0
 .../Contenidos b\303\241sicos.md"          | 17 ++++++++
 .../Criterios de evaluaci\303\263n.md"     |  0
 .../Contenidos b\303\241sicos.md"          | 17 ++++++++
 .../Criterios de evaluaci\303\263n.md"     |  0
 .../Contenidos b\303\241sicos.md"          | 17 ++++++++
 .../Criterios de evaluaci\303\263n.md"     |  0
 .../Contenidos b\303\241sicos.md"          | 17 ++++++++
 .../Criterios de evaluaci\303\263n.md"     |  0
 .../Criterios de evaluacion.md"            |  0
 .../000-Resumen.md"                        |  0
 .../Contenidos b\303\241sicos.md"          | 17 ++++++++
 .../Criterios de evaluaci\303\263n.md"     |  0
 .../Contenidos b\303\241sicos.md"          |  0
 .../Criterios de evaluaci\303\263n.md"     |  0
 .../Contenidos b\303\241sicos.md"          |  0
 .../Criterios de evaluaci\303\263n.md"     |  0
 .../Contenidos b\303\241sicos.md"          |  0
 .../Criterios de evaluaci\303\263n.md"     |  0
 .../Contenidos b\303\241sicos.md"          |  0
 .../Criterios de evaluaci\303\263n.md"     |  0
 .../Contenidos b\303\241sicos.md"          |  0
 .../Criterios de evaluaci\303\263n.md"     |  0
 .../Criterios de evaluacion.md"            |  0
 .../101-Ejercicios/003-dist upgrade.md"    | 10 +++++
 .../004-instalar paquete.md"               |  9 ++++
 .../005-actualizar apache.md"              |  3 ++
 ...crear carpeta de copia de seguridad.md" |  6 +++
 .../007-creo un archivo sh.md"             | 15 +++++++
 .../008-especificar ejecutable.md"         |  3 ++
 .../009-Introduccion a cron.md"            | 23 ++++++++++
 47 files changed, 238 insertions(+)
 rename "Primero/Entornos de desarrollo/005-Elaboraci\303\263n de diagramas de clases/001-Repositorios remotos/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" => "Primero/Entornos de desarrollo/005-Repositorio. Herramientas de control de versiones. Uso integrado en el entorno de desarrollo/001-Repositorios remotos/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" (100%)
 create mode 100644 Primero/Entornos de desarrollo/005-Repositorio. Herramientas de control de versiones. Uso integrado en el entorno de desarrollo/001-Repositorios remotos/101-Ejercicios/001-inicio sesion en el servidor.md
 create mode 100644 Primero/Entornos de desarrollo/005-Repositorio. Herramientas de control de versiones. Uso integrado en el entorno de desarrollo/001-Repositorios remotos/101-Ejercicios/002-tenemos git.md
 create mode 100644 Primero/Entornos de desarrollo/005-Repositorio. Herramientas de control de versiones. Uso integrado en el entorno de desarrollo/001-Repositorios remotos/101-Ejercicios/003-averiguar la version.md
 create mode 100644 Primero/Entornos de desarrollo/005-Repositorio. Herramientas de control de versiones. Uso integrado en el entorno de desarrollo/001-Repositorios remotos/101-Ejercicios/004-me conecto a git desde el servidor.md
 create mode 100644 Primero/Entornos de desarrollo/005-Repositorio. Herramientas de control de versiones. Uso integrado en el entorno de desarrollo/001-Repositorios remotos/101-Ejercicios/005-configuracion.md
 create mode 100644 Primero/Entornos de desarrollo/005-Repositorio. Herramientas de control de versiones. Uso integrado en el entorno de desarrollo/001-Repositorios remotos/101-Ejercicios/006-clonar repositorio.md
 rename "Primero/Entornos de desarrollo/005-Elaboraci\303\263n de diagramas de clases/001-Repositorios remotos/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" => "Primero/Entornos de desarrollo/005-Repositorio. Herramientas de control de versiones. Uso integrado en el entorno de desarrollo/001-Repositorios remotos/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" (100%)
 rename "Primero/Entornos de desarrollo/005-Elaboraci\303\263n de diagramas de clases/002-Documentaci\303\263n. Uso de comentarios. Alternativas/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" => "Primero/Entornos de desarrollo/005-Repositorio. Herramientas de control de versiones. Uso integrado en el entorno de desarrollo/002-Documentaci\303\263n. Uso de comentarios. Alternativas/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" (100%)
 rename "Primero/Entornos de desarrollo/005-Elaboraci\303\263n de diagramas de clases/002-Documentaci\303\263n. Uso de comentarios. Alternativas/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" => "Primero/Entornos de desarrollo/005-Repositorio. Herramientas de control de versiones. Uso integrado en el entorno de desarrollo/002-Documentaci\303\263n. Uso de comentarios. Alternativas/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" (100%)
 rename "Primero/Entornos de desarrollo/005-Elaboraci\303\263n de diagramas de clases/003-Integraci\303\263n continua. Herramientas/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" => "Primero/Entornos de desarrollo/005-Repositorio. Herramientas de control de versiones. Uso integrado en el entorno de desarrollo/003-Integraci\303\263n continua. Herramientas/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" (100%)
 rename "Primero/Entornos de desarrollo/005-Elaboraci\303\263n de diagramas de clases/003-Integraci\303\263n continua. Herramientas/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" => "Primero/Entornos de desarrollo/005-Repositorio. Herramientas de control de versiones. Uso integrado en el entorno de desarrollo/003-Integraci\303\263n continua. Herramientas/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" (100%)
 rename "Primero/Entornos de desarrollo/005-Elaboraci\303\263n de diagramas de clases/000-Resumen.md" => "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de clases/000-Resumen.md" (100%)
 rename "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de comportamiento/001-Clases. Atributos, m\303\251todos y visibilidad/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" => "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de clases/001-Clases. Atributos, m\303\251todos y visibilidad/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" (100%)
 rename "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de comportamiento/001-Clases. Atributos, m\303\251todos y visibilidad/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" => "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de clases/001-Clases. Atributos, m\303\251todos y visibilidad/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" (100%)
 create mode 100755 "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de clases/002-Objetos. Instanciaci\303\263n/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md"
 rename "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de comportamiento/002-Objetos. Instanciaci\303\263n/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" => "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de clases/002-Objetos. Instanciaci\303\263n/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" (100%)
 create mode 100755 "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de clases/003-Relaciones. Asociaci\303\263n, navegabilidad y multiplicidad. Herencia, composici\303\263n, agregaci\303\263n. Realizaci\303\263n y dependencia/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md"
 rename "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de comportamiento/003-Relaciones. Asociaci\303\263n, navegabilidad y multiplicidad. Herencia, composici\303\263n, agregaci\303\263n. Realizaci\303\263n y dependencia/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" => "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de clases/003-Relaciones. Asociaci\303\263n, navegabilidad y multiplicidad. Herencia, composici\303\263n, agregaci\303\263n. Realizaci\303\263n y dependencia/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" (100%)
 create mode 100755 "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de clases/004-Notaci\303\263n de los diagramas de clases/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md"
 rename "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de comportamiento/004-Notaci\303\263n de los diagramas de clases/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" => "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de clases/004-Notaci\303\263n de los diagramas de clases/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" (100%)
 create mode 100755 "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de clases/005-Herramientas/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md"
 rename "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de comportamiento/005-Herramientas/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" => "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de clases/005-Herramientas/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" (100%)
 create mode 100755 "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de clases/006-Generaci\303\263n autom\303\241tica de c\303\263digo. Ingenier\303\255a inversa/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md"
 rename "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de comportamiento/006-Generaci\303\263n autom\303\241tica de c\303\263digo. Ingenier\303\255a inversa/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" => "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de clases/006-Generaci\303\263n autom\303\241tica de c\303\263digo. Ingenier\303\255a inversa/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md" (100%)
 rename "Primero/Entornos de desarrollo/005-Elaboraci\303\263n de diagramas de clases/Criterios de evaluacion.md" => "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de clases/Criterios de evaluacion.md" (100%)
 rename "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de comportamiento/000-Resumen.md" => "Primero/Entornos de desarrollo/007-Elaboraci\303\263n de diagramas de comportamiento/000-Resumen.md" (100%)
 create mode 100755 "Primero/Entornos de desarrollo/007-Elaboraci\303\263n de diagramas de comportamiento/001-Clases. Atributos, m\303\251todos y visibilidad/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md"
 create mode 100755 "Primero/Entornos de desarrollo/007-Elaboraci\303\263n de diagramas de comportamiento/001-Clases. Atributos, m\303\251todos y visibilidad/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md"
 rename "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de comportamiento/002-Objetos. Instanciaci\303\263n/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" => "Primero/Entornos de desarrollo/007-Elaboraci\303\263n de diagramas de comportamiento/002-Objetos. Instanciaci\303\263n/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" (100%)
 create mode 100755 "Primero/Entornos de desarrollo/007-Elaboraci\303\263n de diagramas de comportamiento/002-Objetos. Instanciaci\303\263n/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md"
 rename "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de comportamiento/003-Relaciones. Asociaci\303\263n, navegabilidad y multiplicidad. Herencia, composici\303\263n, agregaci\303\263n. Realizaci\303\263n y dependencia/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" => "Primero/Entornos de desarrollo/007-Elaboraci\303\263n de diagramas de comportamiento/003-Relaciones. Asociaci\303\263n, navegabilidad y multiplicidad. Herencia, composici\303\263n, agregaci\303\263n. Realizaci\303\263n y dependencia/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" (100%)
 create mode 100755 "Primero/Entornos de desarrollo/007-Elaboraci\303\263n de diagramas de comportamiento/003-Relaciones. Asociaci\303\263n, navegabilidad y multiplicidad. Herencia, composici\303\263n, agregaci\303\263n. Realizaci\303\263n y dependencia/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md"
 rename "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de comportamiento/004-Notaci\303\263n de los diagramas de clases/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" => "Primero/Entornos de desarrollo/007-Elaboraci\303\263n de diagramas de comportamiento/004-Notaci\303\263n de los diagramas de clases/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" (100%)
 create mode 100755 "Primero/Entornos de desarrollo/007-Elaboraci\303\263n de diagramas de comportamiento/004-Notaci\303\263n de los diagramas de clases/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md"
 rename "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de comportamiento/005-Herramientas/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" => "Primero/Entornos de desarrollo/007-Elaboraci\303\263n de diagramas de comportamiento/005-Herramientas/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" (100%)
 create mode 100755 "Primero/Entornos de desarrollo/007-Elaboraci\303\263n de diagramas de comportamiento/005-Herramientas/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md"
 rename "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de comportamiento/006-Generaci\303\263n autom\303\241tica de c\303\263digo. Ingenier\303\255a inversa/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" => "Primero/Entornos de desarrollo/007-Elaboraci\303\263n de diagramas de comportamiento/006-Generaci\303\263n autom\303\241tica de c\303\263digo. Ingenier\303\255a inversa/001-Contenidos b\303\241sicos/Contenidos b\303\241sicos.md" (100%)
 create mode 100755 "Primero/Entornos de desarrollo/007-Elaboraci\303\263n de diagramas de comportamiento/006-Generaci\303\263n autom\303\241tica de c\303\263digo. Ingenier\303\255a inversa/201-Criterios de evaluaci\303\263n/Criterios de evaluaci\303\263n.md"
 rename "Primero/Entornos de desarrollo/006-Elaboraci\303\263n de diagramas de comportamiento/Criterios de evaluacion.md" => "Primero/Entornos de desarrollo/007-Elaboraci\303\263n de diagramas de comportamiento/Criterios de evaluacion.md" (100%)
 create mode 100644 "Primero/Sistemas inform\303\241ticos/002-Instalaci\303\263n de sistemas operativos/012-Actualizaci\303\263n y recuperaci\303\263n de sistemas operativos y aplicaciones/101-Ejercicios/003-dist upgrade.md"
 create mode 100644 "Primero/Sistemas inform\303\241ticos/002-Instalaci\303\263n de sistemas operativos/012-Actualizaci\303\263n y recuperaci\303\263n de sistemas operativos y aplicaciones/101-Ejercicios/004-instalar paquete.md"
 create mode 100644 "Primero/Sistemas inform\303\241ticos/002-Instalaci\303\263n de sistemas operativos/012-Actualizaci\303\263n y recuperaci\303\263n de sistemas operativos y aplicaciones/101-Ejercicios/005-actualizar apache.md"
 create mode 100644 "Primero/Sistemas inform\303\241ticos/002-Instalaci\303\263n de sistemas operativos/012-Actualizaci\303\263n y recuperaci\303\263n de sistemas operativos y aplicaciones/101-Ejercicios/006-crear carpeta de copia de seguridad.md"
 create mode 100644 "Primero/Sistemas inform\303\241ticos/002-Instalaci\303\263n de sistemas operativos/012-Actualizaci\303\263n y recuperaci\303\263n de sistemas operativos y aplicaciones/101-Ejercicios/007-creo un archivo sh.md"
 create mode 100644 "Primero/Sistemas inform\303\241ticos/002-Instalaci\303\263n de sistemas operativos/012-Actualizaci\303\263n y recuperaci\303\263n de sistemas operativos y aplicaciones/101-Ejercicios/008-especificar ejecutable.md"
 create mode 100644 "Primero/Sistemas inform\303\241ticos/002-Instalaci\303\263n de sistemas operativos/012-Actualizaci\303\263n y recuperaci\303\263n de sistemas operativos y aplicaciones/101-Ejercicios/009-Introduccion a cron.md"

