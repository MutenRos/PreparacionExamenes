# Proyecto Ollama Curriculums — Análisis de CVs con IA local

![Proyecto Ollama Curriculums](docs/img/banner.png)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/Proyecto-intermodular-004-Proyecto-ollama-curriculums/](https://mutenros.github.io/Proyecto-intermodular-004-Proyecto-ollama-curriculums/)

## Introducción

Este proyecto demuestra cómo utilizar inteligencia artificial local (Ollama con el modelo qwen2.5) para analizar currículums vitae de forma automática. El flujo comienza extrayendo texto de un PDF, lo convierte a Markdown y luego lo envía a un modelo LLM que genera un resumen profesional y una valoración de idoneidad para un puesto docente. Todo sin depender de APIs externas ni servicios en la nube.

## Desarrollo de las partes

### 1. Extracción de texto desde PDF

El primer script se encarga de transformar un CV en formato PDF a texto Markdown legible, utilizando las librerías `pypdf` para la extracción y `markdownify` para la conversión.

- **Archivo:** `001-Ejercicios/001-procesar curriculum.py`, líneas 8–39
- **Ruta:** `001-Ejercicios/001-procesar curriculum.py`

```python
def pdf_to_md(path_pdf, path_md):
    if not os.path.isfile(path_pdf):
        print(f"Error: no se encontró el archivo '{path_pdf}'")
        sys.exit(1)

    reader = PdfReader(path_pdf)
    full_text = ""

    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        full_text += text + "\n\n"
        print(f"Página {i}/{len(reader.pages)} extraída")

    md_text = md(full_text)

    with open(path_md, "w", encoding="utf-8") as f:
        f.write(md_text)
```

El script recorre cada página del PDF, acumula el texto y lo guarda como `.md`. Se añadió verificación de existencia del archivo y progreso por página.

### 2. Configuración de Ollama y modelo LLM

El segundo script configura la conexión con Ollama, un servidor local que ejecuta modelos de lenguaje. Se definen constantes para el modelo, el host y el archivo de entrada.

- **Archivo:** `001-Ejercicios/002-procesar md.py`, líneas 1–15
- **Ruta:** `001-Ejercicios/002-procesar md.py`

```python
ARCHIVO_MD = "CV José Vicente Carratalá Sánchis.md"
MODELO_DEFECTO = "qwen2.5:3b-instruct"
HOST_DEFECTO = "http://localhost:11434"
```

Se usa el modelo `qwen2.5:3b-instruct`, suficientemente ligero para ejecutar en local pero capaz de generar resúmenes coherentes en español.

### 3. Prompt de análisis profesional

El corazón del proyecto es el prompt que se envía al modelo. Instruye a la IA para actuar como experto en selección de personal y generar un resumen profesional del CV, además de emitir una opinión sobre la idoneidad del candidato.

- **Archivo:** `001-Ejercicios/002-procesar md.py`, líneas 35–58
- **Ruta:** `001-Ejercicios/002-procesar md.py`

```python
prompt = dedent(f"""
    Eres un experto en selección de personal y redacción de perfiles profesionales.
    
    Tu tarea:
    - Leer el CV cuidadosamente.
    - Identificar habilidades clave, tecnologías, experiencia relevante y logros.
    - Escribir un resumen profesional conciso en tercera persona.
    - Extensión orientativa: 7–10 líneas (máximo ~200 palabras).
    
    -Importante: Emite una opinion acerca de si el perfil es valido o no es válido
     para el puesto de trabajo: profesor de ciclos formativos.

    CV (Markdown):
    ---
    {contenido_md}
    ---
""")
```

### 4. Comunicación con la API de Ollama

Se envía el prompt al endpoint `/api/generate` de Ollama mediante una petición POST con `requests`. La respuesta incluye el resumen generado por la IA.

- **Archivo:** `001-Ejercicios/002-procesar md.py`, líneas 60–90
- **Ruta:** `001-Ejercicios/002-procesar md.py`

```python
url = f"{host}/api/generate"
payload = {
    "model": modelo.strip(),
    "prompt": prompt,
    "stream": False,
}

response = requests.post(url, json=payload, timeout=600)
response.raise_for_status()
data = response.json()
return data["response"].strip()
```

Se usa `stream: False` para recibir la respuesta completa de una sola vez. El timeout de 600 segundos permite que modelos más pesados completen su respuesta.

### 5. CV de ejemplo: José Vicente Carratalá

El proyecto incluye un CV real de 902 líneas convertido a Markdown. Incluye experiencia como profesor de ciclos formativos, CEO de JOCARSA, instructor en LinkedIn Learning y una extensa formación en diseño industrial, programación y gráficos 3D.

- **Archivo:** `001-Ejercicios/CV José Vicente Carratalá Sánchis.md`, líneas 1–902
- **Ruta:** `001-Ejercicios/CV José Vicente Carratalá Sánchis.md`

El CV cubre experiencia laboral, formación académica, certificaciones, idiomas y habilidades tecnológicas — todo el material que la IA debe procesar.

### 6. Mejoras aplicadas

Se añadieron mejoras transversales en ambos scripts:

- **Docstrings** con formato Google en la función `pdf_to_md`.
- **Verificación de archivo** con `os.path.isfile()` antes de procesarlo.
- **Progreso por página** al extraer el PDF.
- **`argparse`** para poder pasar el archivo y modelo por línea de comandos.
- **Errores específicos:** `ConnectionError` si Ollama no está corriendo, `Timeout` si tarda demasiado.
- **Timing:** muestra cuántos segundos tardó la IA en responder.
- **Constantes en el encabezado** para modelo y host.

## Presentación del proyecto

El proyecto **Ollama Curriculums** combina dos tecnologías: el procesamiento de documentos PDF y la inteligencia artificial local con modelos LLM. El pipeline funciona en dos fases:

1. **Fase de extracción:** El primer script toma un CV en PDF, extrae el texto de cada página con `pypdf` y lo convierte a Markdown. Esto normaliza el contenido para que la IA pueda leerlo.

2. **Fase de análisis:** El segundo script carga el Markdown, construye un prompt especializado en selección de personal y lo envía a Ollama. El modelo devuelve un resumen profesional y una valoración de idoneidad para el puesto de profesor de ciclos formativos.

Lo más interesante del proyecto es que toda la inteligencia artificial se ejecuta en local — no se envían datos a ningún servidor externo. Esto garantiza la privacidad del CV procesado, algo fundamental cuando se trabaja con datos personales.

El CV de ejemplo es el del propio profesor, José Vicente Carratalá, con más de 20 años de experiencia en docencia, programación y diseño 3D.

## Conclusión

Este proyecto muestra cómo la inteligencia artificial local puede integrarse en flujos de trabajo reales de una forma sencilla y respetuosa con la privacidad. Con apenas dos scripts de Python y un servidor Ollama, se consigue automatizar el análisis de currículums, una tarea que normalmente requiere tiempo y criterio humano. La progresión del proyecto — primero extraer, luego analizar — refleja un enfoque modular y escalable que podría ampliarse con más modelos, más formatos de entrada o una interfaz web.
