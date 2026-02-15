# Generación de imágenes con IA — Stable Diffusion + Ollama + Python

![Imagen generada con Stable Diffusion](101-Ejercicios/generated_images/hero-gestión-académica-moderna.png)

## Introducción

Este proyecto explora la **generación de imágenes con inteligencia artificial** utilizando el modelo **Stable Diffusion** y scripts en **Python**. El trabajo progresa desde la instalación básica del entorno hasta un pipeline automatizado completo que lee un archivo XML de producto, genera prompts inteligentes con **Ollama (LLaMA 3)** y produce imágenes de marketing SaaS con Stable Diffusion.

El resultado es un sistema capaz de tomar una descripción de producto en formato XML y generar automáticamente todas las imágenes necesarias para una landing page, sin intervención manual en la creación de prompts ni en la generación de las imágenes.

---

## Desarrollo de las partes

### 1. Instalación del entorno — AUTOMATIC1111 y Stable Diffusion WebUI

El primer paso documenta cómo instalar la interfaz web de Stable Diffusion (AUTOMATIC1111) en un sistema Linux. Se utiliza un entorno virtual de Python y se clona el repositorio oficial.

```bash
# 001-Instalar modelo de imagen.md — líneas 1-6
# Ruta: 101-Ejercicios/001-Instalar modelo de imagen.md
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip

git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
cd stable-diffusion-webui
./webui.sh
```

Este archivo es la base de todo el proyecto: sin el modelo instalado, los scripts posteriores no pueden funcionar. AUTOMATIC1111 proporciona una interfaz gráfica web para generar imágenes.

---

### 2. Instalación de dependencias Python — Diffusers y PyTorch

El segundo ejercicio documenta la instalación de las librerías Python necesarias para ejecutar Stable Diffusion desde código (sin interfaz web). Usa `diffusers` de Hugging Face, `torch` con soporte CUDA para GPU, y `Pillow` para el tratamiento de imágenes.

```bash
# 002-stable diffusion.md — líneas 1-8
# Ruta: 101-Ejercicios/002-stable diffusion.md
sudo apt install -y python3-venv git
python3 -m venv venv
source venv/bin/activate

pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install diffusers transformers accelerate safetensors pillow
```

Se instala PyTorch con soporte CUDA 12.1 para aprovechar la GPU en la generación de imágenes, lo que reduce el tiempo de generación drásticamente.

---

### 3. Generación de una imagen simple — Script básico

El script `003-crear imagen.py` es el primer ejercicio práctico: genera una imagen a partir de un prompt de texto usando el pipeline de Stable Diffusion v1.5. Detecta automáticamente si hay GPU disponible y ajusta la precisión (float16 para CUDA, float32 para CPU).

```python
# 003-crear imagen.py — líneas 15-26
# Ruta: 101-Ejercicios/003-crear imagen.py
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32
print(f"Dispositivo seleccionado: {device}")

try:
    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
        safety_checker=None,
    )
    pipe = pipe.to(device)
```

Los parámetros clave son `num_inference_steps=30` (calidad), `guidance_scale=7.5` (adherencia al prompt) y `height/width=512` (resolución). Se añadió manejo de errores con try/except para capturar fallos de modelo o GPU.

---

### 4. Generación por lotes — Lista de prompts

El script `004-lista de peticiones.py` genera múltiples imágenes a partir de una lista de prompts. La mejora principal respecto al código original es que **el pipeline se carga una sola vez** fuera del bucle, en lugar de recargarlo en cada iteración (lo que ahorra minutos de carga).

```python
# 004-lista de peticiones.py — líneas 12-17
# Ruta: 101-Ejercicios/004-lista de peticiones.py
lista = [
  'a green dog over green grass',
  'a pink cat over a sofa',
  'a horse running in the forest'
]
```

```python
# 004-lista de peticiones.py — líneas 20-29
# Ruta: 101-Ejercicios/004-lista de peticiones.py
# --- Cargar el pipeline UNA sola vez (mejora de rendimiento) ---
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=dtype,
    safety_checker=None,
)
pipe = pipe.to(device)
```

Cada imagen se guarda con el nombre del prompt como archivo (ej: `a green dog over green grass.png`). Se añadió progreso visual `[1/3]` y manejo de errores individual por imagen.

---

### 5. Pipeline XML completo — Ollama + Stable Diffusion

El script `005-crear imagenes a partir de xml.py` es el más avanzado (349 líneas). Lee un archivo XML de producto (`producto.xml`), extrae contexto semántico, envía las descripciones de imagen a **Ollama** (modelo LLaMA 3 local) para que genere prompts profesionales de Stable Diffusion, y luego genera todas las imágenes automáticamente.

```python
# 005-crear imagenes a partir de xml.py — líneas 101-133
# Ruta: 101-Ejercicios/005-crear imagenes a partir de xml.py
def build_context_from_xml(root: ET.Element) -> dict:
    """Builds a compact context object from key fields in the XML."""
    title = get_text("./meta/title")
    category = get_text("./meta/category")
    # ... extrae titulo, categoria, propuesta de valor, problemas, beneficios, features
    return {
        "slug": slug,
        "title": title,
        "category": category,
        "valueProposition": value_prop,
        "problems": problems[:8],
        "benefits": benefits[:8],
        "features": features[:10],
        "style": {
            "look": "apple-like, clean, modern SaaS, minimal, premium",
            "avoid": "text, letters, logos, watermarks, UI screenshots with readable text",
        }
    }
```

El flujo es: **XML → contexto → Ollama genera prompts → Stable Diffusion genera imágenes → XML actualizado con rutas locales**.

---

### 6. Generación de prompts con Ollama

La función `ollama_generate_json` se comunica con un modelo LLaMA 3 local a través de la API REST de Ollama. Le envía el contexto del producto y la lista de imágenes, y recibe prompts en inglés optimizados para Stable Diffusion, con negative prompts para evitar texto y logos.

```python
# 005-crear imagenes a partir de xml.py — líneas 64-96
# Ruta: 101-Ejercicios/005-crear imagenes a partir de xml.py
def ollama_generate_json(system: str, user: str) -> dict:
    """Asks Ollama to return strict JSON. Retries once if parsing fails."""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": user,
        "system": system,
        "stream": False,
        "options": {"temperature": 0.4}
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=OLLAMA_TIMEOUT)
    r.raise_for_status()
    # Retry con temperatura más baja si el JSON no es válido
```

Si Ollama devuelve JSON mal formado, el sistema reintenta automáticamente con temperatura reducida y una instrucción más estricta (`DEVUELVE SOLO JSON`).

---

### 7. Estructura del XML de producto

El archivo `producto.xml` define la estructura completa de una landing page de producto SaaS educativo ("Gestión Académica Pro"). Tiene secciones para hero, problema, solución, funcionalidades, público objetivo, casos de uso, beneficios, integraciones, confianza, CTA y FAQ, cada una con su propia imagen.

```xml
<!-- producto.xml — líneas 1-16 -->
<!-- Ruta: 101-Ejercicios/producto.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<productPage lang="es" type="softwareEducativo" version="1.1">
  <meta>
    <slug>gestion-academica-pro</slug>
    <title>Gestión Académica Pro</title>
    <category>SaaS educativo</category>
    <audience>
      <segment>Dirección</segment>
      <segment>Secretaría / Administración</segment>
      <segment>Docentes</segment>
      <segment>Coordinación académica</segment>
    </audience>
  </meta>
```

El XML es el input del pipeline automatizado: cada `<image>` se procesa para generar la imagen correspondiente con IA.

---

### 8. Imágenes generadas con IA

El directorio `generated_images/` contiene 5 imágenes generadas automáticamente por el pipeline:

- `hero-gestión-académica-moderna.png` — imagen principal de la landing
- `problem-problemas-de-gestión-educativa.png` — visualización del problema
- `solution-solución-centralizada.png` — representación de la solución
- `features-funcionalidades-clave.png` — ilustración de funcionalidades
- `audience-público-objetivo.png` — imagen del público objetivo

Cada nombre de archivo se genera automáticamente con la función `safe_filename_from_alt()` que combina la sección + alt text del XML en un slug legible.

---

### 9. Mejoras aplicadas

Se aplicaron mejoras de nivel estudiante sobre los scripts originales:

- **Docstrings** en cada script para documentar el propósito y requisitos.
- **Manejo de errores** con `try/except` en los scripts 003 y 004 para capturar fallos de modelo o GPU.
- **Pipeline fuera del bucle** en 004: antes se recargaba el modelo entero (~2GB) en cada iteración del for; ahora se carga una sola vez.
- **Progreso visual** en 004: mensajes `[1/3] Generando: 'prompt'...` para saber en qué imagen va.
- **Constantes configurables** en 003 (`STEPS`, `GUIDANCE`, `IMG_SIZE`, `OUTPUT_FILE`) en lugar de valores hardcoded.
- **Comentarios en español** explicando cada sección del código.
- **Tiempo total** en 005: al final del main se muestra el tiempo transcurrido.

---

## Presentación del proyecto

Este proyecto muestra un recorrido progresivo por la generación de imágenes con inteligencia artificial. Empezamos instalando Stable Diffusion y su interfaz web, para entender el modelo por fuera. Después pasamos a controlarlo desde Python con la librería `diffusers`, generando primero una imagen simple y luego un lote de varias imágenes.

El ejercicio más avanzado combina dos IAs: Ollama (LLaMA 3) genera los prompts de forma inteligente leyendo un XML de producto, y Stable Diffusion genera las imágenes correspondientes. El resultado son imágenes estilo marketing SaaS tipo Apple, creadas automáticamente sin intervención manual.

Las imágenes generadas (en `generated_images/`) demuestran que el pipeline funciona de extremo a extremo: hero, problema, solución, funcionalidades y público objetivo, todo generado a partir de la descripción XML del producto.

---

## Conclusión

Este proyecto demuestra cómo la IA generativa puede automatizar tareas creativas que antes requerían diseñadores gráficos. La progresión desde un script básico de una imagen hasta un pipeline completo XML→Ollama→Stable Diffusion ilustra conceptos fundamentales: entornos virtuales Python, uso de GPU con CUDA, APIs REST (Ollama), procesamiento XML, y generación de imágenes con modelos de difusión.

Las mejoras aplicadas — extracción del pipeline fuera del bucle, manejo de errores, documentación y constantes configurables — dan robustez y claridad al código, y demuestran buenas prácticas de programación aplicadas a un proyecto de IA.
