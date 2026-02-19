# Proyecto Piero — Web Scraping e Imágenes con Python

![Proyecto Piero](docs/img/banner.png)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/Proyecto-intermodular-001-Proyecto-Piero/](https://mutenros.github.io/Proyecto-intermodular-001-Proyecto-Piero/)

## Introducción

Este proyecto recorre paso a paso el camino desde una simple petición HTTP hasta un scraper completo de Google Images con sesiones, cabeceras realistas y descarga masiva de ficheros. Cada iteración del código añade una capa nueva de complejidad, lo que permite entender cómo funcionan las peticiones web, el análisis de HTML y la automatización de descargas de recursos multimedia.

## Desarrollo de las partes

### 1. Primeros pasos con `requests`

El punto de partida es importar la librería `requests`, la herramienta estándar de Python para realizar peticiones HTTP. En esta fase se comprueba que el entorno está listo.

```python
import requests
```

Este primer fichero sirve como prueba de concepto mínima: si el import funciona, el entorno tiene las dependencias necesarias.

### 2. Petición GET a una web propia

Se realiza una petición GET a `jocarsa.com` para obtener el código HTML completo de la página. Se imprime el código de estado y el contenido.

```python
url = "https://jocarsa.com"
response = requests.get(url, headers=HEADERS, timeout=10)
response.raise_for_status()
print("Status:", response.status_code)
print("Encoding:", response.encoding)
html = response.text
```

Se añadieron cabeceras User-Agent y manejo de errores con `try/except` para capturar fallos de conexión, timeout y errores HTTP.

### 3. Scraper de imágenes desde una web

Se extrae automáticamente cada imagen de `jocarsa.com` utilizando dos técnicas complementarias:

- **Etiquetas `<img>`:** BeautifulSoup recorre el DOM buscando atributos `src`.
- **CSS `background-image`:** Se aplica una expresión regular sobre los atributos `style` para capturar URLs en `background-image:url(...)`.

```python
for img in soup.find_all("img"):
    src = img.get("src")
    if src:
        full_url = urljoin(URL, src)
        image_urls.add(full_url)

pattern = re.compile(
    r"background-image\s*:\s*url\(['\"]?(.*?)['\"]?\)",
    re.IGNORECASE
)
```

Las imágenes se descargan en la carpeta `imagenes/` con gestión de nombres duplicados y control de errores.

### 4. Scraping de Google Images

Se adapta el scraper anterior para buscar imágenes en Google. La URL de búsqueda se simplificó eliminando parámetros efímeros y dejando solo los esenciales (`q`, `tbm`).

```python
SEARCH_QUERY = "ardilla"
URL = f"https://www.google.com/search?q={SEARCH_QUERY}&tbm=isch&hl=es"
```

Se añadió User-Agent y timeout para evitar bloqueos por parte de Google.

### 5. Scraper avanzado con sesiones y múltiples métodos

Esta iteración supone un salto cualitativo importante:

| Característica | Detalle |
|---|---|
| **Sesiones** | `requests.Session()` mantiene cookies entre peticiones |
| **Cabeceras completas** | User-Agent, Accept, DNT, etc. |
| **Retardos aleatorios** | `time.sleep(random.uniform(2, 5))` para evitar detección |
| **Tres métodos de extracción** | Etiquetas `<img>`, URLs dentro de `<script>` y base64 |
| **Paginación** | Se avanza por páginas de resultados de forma automática |
| **Descarga con streaming** | `iter_content(chunk_size=8192)` para ficheros grandes |

```python
session = requests.Session()
session.headers.update(HEADERS)

# Método 1: img tags
# Método 2: URLs en scripts JSON
# Método 3: base64 en data attributes
```

### 6. Parámetro personalizado por el usuario

La última iteración permite al usuario introducir el término de búsqueda por consola. Se añadió validación de entrada para rechazar cadenas vacías.

```python
SEARCH_QUERY = input("Introduce el termino que quieres buscar: ").strip()
if not SEARCH_QUERY:
    print("Error: debes introducir un término de búsqueda.")
    exit(1)
```

### 7. Mejoras transversales aplicadas

En todas las iteraciones se aplicaron mejoras de calidad:

- **Cabeceras User-Agent** para evitar bloqueos del servidor.
- **Timeout** en todas las peticiones para evitar bloqueos infinitos.
- **Try/except** con tipos de excepción específicos (`ConnectionError`, `Timeout`, `HTTPError`).
- **Validación de input** en la versión interactiva.
- **Limpieza de la URL de Google** eliminando parámetros efímeros y tokens.

## Presentación del proyecto

El proyecto **Piero** demuestra una progresión didáctica completa del web scraping en Python. Se parte de la operación más básica — importar una librería — y se llega hasta un sistema de descarga masiva de imágenes desde Google con técnicas anti-detección.

El pipeline completo funciona de la siguiente manera:

1. El usuario ejecuta el script y opcionalmente introduce un término de búsqueda.
2. El programa construye la URL de Google Images y envía la petición con cabeceras realistas.
3. BeautifulSoup analiza el HTML devuelto y extrae URLs de imágenes por tres vías diferentes.
4. Cada imagen se descarga de forma secuencial con retardos aleatorios, se valida su tipo MIME y se guarda en disco con un nombre limpio.

Las carpetas `imagenes/` y `google_images/` contienen los resultados reales de las ejecuciones: desde los recursos de `jocarsa.com` hasta fotografías de ardillas obtenidas de Google.

## Conclusión

Este proyecto muestra cómo una funcionalidad aparentemente simple — descargar imágenes de internet — requiere en realidad un conocimiento profundo de HTTP, parsing HTML, expresiones regulares y buenas prácticas de programación defensiva. Cada iteración introduce un concepto nuevo (sesiones, headers, base64, streaming, validación) que se acumula sobre lo anterior, formando un aprendizaje incremental y sólido. El resultado final es un scraper funcional, robusto y configurable que puede adaptarse a cualquier término de búsqueda.
