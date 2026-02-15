Utilizamos IA para crear la documentación de los repostitorios.

Por ejemplo:

# carpetaspython

Programa en **Python** que muestra el **árbol de carpetas y archivos** de un directorio usando `os.walk`, dibujando ramas con ASCII y añadiendo **emojis** para carpetas y archivos.

> 📁 Carpetas → `📁`
>
> 📄 Archivos → `📄`

---

## ✨ Características

* Recorre recursivamente cualquier ruta local.
* Dibuja la jerarquía con indentación ASCII.
* Emojis para distinguir carpetas y archivos.
* Función principal que **devuelve** el árbol como cadena (útil para tests / logging) y script que lo **imprime** en consola.

---

## 🚀 Requisitos

* Python **3.8+**
* No necesita dependencias externas.

---

## 📦 Instalación

Clona el repositorio:

```bash
git clone https://github.com/jocarsa/carpetaspython.git
cd carpetaspython
```

---

## 🧰 Uso rápido

Ejecuta el script y escribe la ruta cuando te la pida:

```bash
python carpetas.py
```

Salida esperada (ejemplo):

```
Introduce la ruta: /home/usuario/proyecto
📁 proyecto/
    📁 datos/
        📄 ventas.csv
    📁 src/
        📄 main.py
        📄 utils.py
    📄 README.md
```

> 💡 En Windows, si no ves emojis, asegúrate de usar una consola que los soporte (Windows Terminal / PowerShell moderno).

---

## 🧩 Código principal

Si quieres usar la función en otro módulo, puedes importarla. La función **devuelve** una cadena con el árbol:

```python
import os

def mostrar_arbol_directorio(ruta_directorio: str) -> str:
    """
    Muestra el árbol de directorios y archivos de la ruta especificada.
    Parámetros:
        ruta_directorio (str): La ruta del directorio a mostrar.
    Retorna:
        str: Cadena de texto con el árbol de directorios y archivos.
    """
    lineas = []
    for raiz, carpetas, archivos in os.walk(ruta_directorio):
        nivel = raiz.replace(ruta_directorio, "").count(os.sep)
        indentacion = " " * 4 * nivel
        lineas.append(f"{indentacion}📁 {os.path.basename(raiz) or os.path.basename(ruta_directorio)}/")
        sub_indentacion = " " * 4 * (nivel + 1)
        for archivo in archivos:
            lineas.append(f"{sub_indentacion}📄 {archivo}")
    return "\n".join(lineas)

if __name__ == "__main__":
    ruta = input("Introduce la ruta: ").strip()
    if not ruta:
        print("⚠️ Debes introducir una ruta.")
    elif not os.path.isdir(ruta):
        print(f"❌ La ruta no existe o no es un directorio: {ruta}")
    else:
        print(mostrar_arbol_directorio(ruta))
```

---

## 🧪 Ejemplo programático

```python
from carpetas import mostrar_arbol_directorio
print(mostrar_arbol_directorio("/ruta/a/inspeccionar"))
```

---

## 🛠️ Detalles de implementación

* `os.walk(ruta)` recorre la estructura de carpetas.
* El **nivel** de profundidad se calcula contando separadores (`os.sep`).
* La **indentación** se hace con 4 espacios por nivel.
* El **nombre base** de la carpeta se obtiene con `os.path.basename`.

---

## 🗺️ Roadmap (ideas)

* Opción CLI con `argparse` (`python carpetas.py --path . --no-emoji`).
* Parámetro para **ordenar** carpetas/archivos alfabéticamente.
* Alternar símbolos ASCII puros (`+--` / `|  `) para compatibilidad 100% sin emojis.
* Exclusiones por patrón (`--ignore ".git,__pycache__"`).
* Test unitarios simples con `pytest`.

---

## 🤝 Contribuir

¡Se aceptan PRs! Abre un *issue* con propuestas o errores detectados.

---

## 📄 Licencia

MIT © Jose Vicente Carratalá

---

## 👤 Autor

**Jose Vicente Carratalá** — [@jocarsa](https://github.com/jocarsa)
