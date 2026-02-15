# Creador masivo de artículos de blog con IA local

![Generador de blog con Ollama](https://img.shields.io/badge/Ollama-qwen2.5:7b-blueviolet)
![Python 3](https://img.shields.io/badge/Python-3.x-blue)
![SQLite](https://img.shields.io/badge/SQLite-3-green)

## Introducción

Este proyecto automatiza la generación de cientos de artículos de blog sobre Inteligencia Artificial a partir de cursos escritos en Markdown. Utiliza un modelo de lenguaje local (Ollama con qwen2.5:7b-instruct) para redactar cada artículo, y almacena los resultados en una base de datos SQLite. El objetivo es poblar un blog técnico con contenido de calidad sin depender de APIs externas de pago, manteniendo todo el procesamiento en local.

## Desarrollo de las partes

### 1. Corpus de documentos Markdown

La carpeta `documentos/` contiene más de 60 archivos Markdown, cada uno correspondiente a un curso completo sobre temas de IA: desde "Introducción a la Inteligencia Artificial" hasta "PyTorch desde cero", pasando por NLP, visión por computador, prompt engineering y deep learning.

Cada documento sigue una estructura jerárquica consistente:

```markdown
---
slug: analisis-de-sentimiento
title: Análisis de sentimiento
level: Intermedio
---

# Unidad 1 — Qué es el análisis de sentimiento
## 1.1 — Definición y alcance
### Lección 1.1.1 — Qué mide realmente el sentimiento
### Lección 1.1.2 — Polaridad vs emoción
```

El front-matter YAML aporta metadatos (slug, nivel, duración estimada, prerrequisitos) y el cuerpo usa headings H1/H2/H3 para organizar unidades, secciones y lecciones.

### 2. Extracción de jerarquía H1 → H2 → H3

El script `generar.py` recorre cada `.md` y extrae los headings de nivel 3; para cada uno, memoriza el H1 y H2 actuales, formando una categoría jerárquica:

```python
def extract_hierarchy_items(md_body: str, file_stem: str) -> List[H3Item]:
    h1_current = ""
    h2_current = ""
    items: List[H3Item] = []

    for line in normalize_newlines(md_body).splitlines():
        m1 = re.match(r"^\s*#\s+(.+?)\s*$", line)
        if m1:
            h1_current = m1.group(1).strip()
            h2_current = ""
            continue
        m2 = re.match(r"^\s*##\s+(.+?)\s*$", line)
        if m2:
            h2_current = m2.group(1).strip()
            continue
        m3 = re.match(r"^\s*###\s+(.+?)\s*$", line)
        if m3:
            raw_h3 = m3.group(1).strip()
            title = strip_numbering_from_h3(raw_h3)
            category = f"{file_stem}, {h1_current}, {h2_current}"
            items.append(H3Item(...))
    return items
```

Para cada H3 como "Lección 1.1.1 — Qué mide realmente el sentimiento", se limpia la numeración (`strip_numbering_from_h3`) dejando solo el título limpio, y se construye una categoría del tipo `"Análisis de sentimiento, Unidad 1, 1.1 — Definición y alcance"`.

### 3. Generación con Ollama (LLM local)

Cada artículo se genera enviando un prompt estructurado a Ollama via su API REST:

```python
def ollama_generate(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "top_p": 0.9, "num_ctx": 8192},
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json()["response"].strip()
```

El prompt incluye el documento completo como contexto, la categoría del artículo y un esqueleto de estructura (introducción, explicación con código, errores típicos, checklist, siguientes pasos) para garantizar artículos completos de 900-1400 palabras.

### 4. Caché JSON en disco

Para no regenerar artículos ya procesados, cada respuesta de Ollama se guarda como JSON en `.cache_articulos/`:

```python
def cache_key(file_path, title, category) -> Path:
    base = f"{file_path.name}__{title}__{category}"
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "_", base)[:180]
    return CACHE_DIR / f"{safe}.json"
```

Si el script se interrumpe, al relanzarlo recupera los artículos de caché sin volver a llamar a Ollama, ahorrando tiempo de GPU.

### 5. Almacenamiento en SQLite

La base de datos `blog.sqlite` contiene una tabla `posts` con columnas `id`, `date`, `title`, `content` (Markdown), `category`. El script usa `INSERT` con deduplicación:

```python
def post_exists(conn, title, category) -> bool:
    cur = conn.execute(
        "SELECT 1 FROM posts WHERE title = ? AND category = ? LIMIT 1",
        (title, category),
    )
    return cur.fetchone() is not None
```

Se crean índices en `date DESC` y `category` para facilitar consultas rápidas del blog.

### 6. Parsing de front-matter YAML

Antes de extraer headings, el script detecta y separa el bloque front-matter delimitado por `---`:

```python
def extract_front_matter(md: str) -> Tuple[Dict[str, str], str]:
    if not md.startswith("---\n"):
        return {}, md
    parts = md.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, md
    # parsea clave: valor línea a línea
    ...
    return fm, body
```

Esto evita que los metadatos YAML se interpreten como headings de contenido.

### 7. Limpieza de numeración en títulos

La función `strip_numbering_from_h3` elimina prefijos como "Lección", "Tema", "Capítulo" y numeración como "1.2.3 —" dejando solo el título descriptivo:

```python
def strip_numbering_from_h3(title: str) -> str:
    t = re.sub(r"^(lecci[oó]n|lesson|tema|...)\s*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"^\s*\d+(?:[\.\-]\d+){0,6}\s*[\)\.\-–—:]*\s*", "", t)
    t = re.sub(r"^\s*[–—-]\s*", "", t)
    return t.strip()
```

### 8. Mejoras aplicadas

Se añadieron las siguientes mejoras al script original:

- **Logging estructurado** con `logging` en lugar de `print()`, con timestamps y niveles
- **Modo `--dry-run`** para previsualizar qué artículos se generarían sin llamar a Ollama
- **Variables de entorno** (`OLLAMA_MODEL`, `OLLAMA_URL`, `OLLAMA_TIMEOUT`) para configurar sin tocar código
- **Excepciones específicas** (`ConnectionError`, `Timeout`) en el retry de Ollama
- **Estadísticas ampliadas**: contador de artículos desde caché, errores, tiempo total de ejecución
- **Resiliencia**: los errores de generación individual no detienen todo el proceso

## Presentación del proyecto

El generador procesa un corpus de más de 60 cursos de IA en Markdown. Por cada heading de nivel 3, construye un prompt contextualizado que incluye todo el documento como referencia, y solicita a Ollama (modelo qwen2.5:7b-instruct) un artículo completo con estructura didáctica.

El resultado es una base de datos SQLite con cientos de posts listos para servir desde un blog PHP. Cada artículo tiene título limpio, categoría jerárquica (archivo → unidad → sección) y contenido en Markdown listo para renderizar.

La caché en JSON permite relanzar el script de forma segura: solo se generan los artículos que faltan. El modo `--dry-run` permite verificar qué se generaría antes de invertir tiempo de GPU.

## Conclusión

Este proyecto demuestra la integración de un LLM local (Ollama) con Python para automatizar la generación de contenido técnico a escala. La combinación de Markdown como formato fuente, SQLite como almacenamiento estructurado y JSON como caché intermedia crea un pipeline robusto y reanudable. Las mejoras de logging, dry-run y variables de entorno lo preparan para uso en producción, y la arquitectura es extensible a otros modelos o dominios temáticos.
