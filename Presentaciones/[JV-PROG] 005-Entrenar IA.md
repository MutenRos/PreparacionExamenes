# Entrenar IA — Fine-tuning de modelo Qwen 2.5 con LoRA

![Fine-tuning LoRA sobre Qwen 2.5 — entrenamiento personalizado de modelo de IA local](https://img.shields.io/badge/Python-LoRA_Fine--tuning-3776AB?style=for-the-badge&logo=python&logoColor=white)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/Programacion-005-Entrenar-IA/](https://mutenros.github.io/Programacion-005-Entrenar-IA/)

## Introducción

Este proyecto es un recorrido completo por el proceso de personalización de un modelo de inteligencia artificial: desde la preparación de los datos de entrenamiento (JSONL), pasando por el fine-tuning con LoRA/QLoRA en Python, la inferencia del modelo resultante, hasta la construcción de una interfaz web tipo chat que consume el modelo. El proyecto cubre 10 ejercicios progresivos más archivos auxiliares (servidor Flask, módulo de inferencia) y un frontend HTML/CSS/JS. Demuestra que es posible entrenar un modelo de IA con datos propios en un equipo local usando técnicas eficientes como LoRA, sin necesidad de GPUs profesionales ni servicios en la nube.

---

## Desarrollo de las partes

### 1. Chat PHP con Ollama — Base del proyecto (001, 002)

Los dos primeros ejercicios son aplicaciones PHP que conectan con Ollama (igual que en el proyecto anterior). La diferencia clave del ejercicio 002 es la instrucción adicional "no infieras": se le dice al modelo que si no conoce la respuesta, lo indique explícitamente.

```php
// Archivo: 101-Ejercicios/002-no inferencia.php, líneas 9-11
$prompt = $userPrompt . "
  - responde en un solo párrafo, sin código, en prosa.
  - respuestas solo en español
  - no infieras, si no conoces la respuesta, indícalo";
```

Esta instrucción es fundamental: demuestra por qué necesitamos entrenar el modelo con datos propios — un modelo genérico no conoce información específica sobre una persona o institución.

---

### 2. Plantilla de entrenamiento JSONL (003)

El formato de datos de entrenamiento es JSONL (JSON Lines): cada línea es un par pregunta-respuesta independiente. La plantilla muestra la estructura mínima que espera el script de entrenamiento.

```jsonl
// Archivo: 101-Ejercicios/003-plantilla de entrenamiento.jsonl
{"question": "X", "answer": "Y"}
```

---

### 3. Dataset personalizado — 20 pares QA (004)

Se rellena la plantilla con 20 pares pregunta-respuesta sobre Jose Vicente Carratalá Sanchis: su profesión, tecnologías, proyectos, estilo pedagógico, etc. Este dataset es lo que el modelo "aprenderá" en el fine-tuning.

```jsonl
// Archivo: 101-Ejercicios/004-plantilla rellenada con mis datos.jsonl, líneas 1-3
{"question":"¿Quién es Jose Vicente Carratalá Sanchis?","answer":"Jose Vicente Carratalá Sanchis es un desarrollador de software, formador y creador de contenidos técnicos especializado en programación, sistemas e inteligencia artificial."}
{"question":"¿A qué se dedica Jose Vicente Carratalá Sanchis profesionalmente?","answer":"Jose Vicente Carratalá Sanchis se dedica al desarrollo de software, a la formación técnica en programación y a la creación de proyectos tecnológicos educativos."}
{"question":"¿Qué tipo de software desarrolla Jose Vicente Carratalá Sanchis?","answer":"Jose Vicente Carratalá Sanchis desarrolla aplicaciones web, plataformas educativas, herramientas de gestión empresarial y sistemas basados en inteligencia artificial."}
```

El dataset completo tiene 20 pares cubriendo: identidad, profesión, lenguajes, experiencia web, libros, Jocarsa, IA, modelos, administración de sistemas, Moodle, gráficos, preferencias de estilo, y el objetivo del entrenamiento.

---

### 4. Preparación del entorno Python (005)

Script shell que documenta los comandos necesarios para crear un entorno virtual Python e instalar las dependencias: `torch`, `datasets`, `peft` y `transformers`.

```bash
# Archivo: 101-Ejercicios/005-preparamos entorno.sh, líneas 3-13
python3 -m venv venv
source venv/bin/activate
pip install torch
pip install datasets
pip install peft
pip install transformers
```

---

### 5. Entrenamiento LoRA — Script principal (006)

El archivo central del proyecto (276 líneas). Carga el dataset JSONL, descarga el modelo base Qwen2.5-0.5B-Instruct, aplica adaptadores LoRA y entrena durante 80 épocas. Incluye la generación automática de un informe Markdown con métricas.

```python
# Archivo: 101-Ejercicios/006-entrenar el modelo - afinar el modelo.py, líneas 18-42
DATA_PATH = "outputs/*.jsonl"
BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
OUTPUT_DIR = "./qwen25-05b-jvc"

MAX_LENGTH = 512
NUM_EPOCHS = 80
LR = 2e-4
BATCH_SIZE = 1
GRAD_ACCUM = 4

LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05
```

La configuración LoRA aplica adaptadores a 7 capas del transformer (`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`) con rango 16 y alpha 32. El entrenamiento usa *answer-only loss*: solo se calcula la pérdida sobre los tokens de la respuesta, no del prompt.

```python
# Archivo: 101-Ejercicios/006-entrenar el modelo - afinar el modelo.py, líneas 143-149
lora = LoraConfig(
    r=LORA_R,
    lora_alpha=LORA_ALPHA,
    lora_dropout=LORA_DROPOUT,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
)
```

La mejora añadida valida que el dataset contenga los campos `question` y `answer` antes de proceder:

```python
# Archivo: 101-Ejercicios/006-entrenar el modelo - afinar el modelo.py, líneas 121-126
required_fields = {"question", "answer"}
missing = required_fields - set(raw.column_names)
if missing:
    print(f"❌ Error: faltan campos en el dataset: {missing}")
    return
```

---

### 6. Exportación del modelo fusionado (007)

Después del entrenamiento, los adaptadores LoRA se fusionan con el modelo base usando `merge_and_unload()`, y se guarda el resultado como modelo completo independiente.

```python
# Archivo: 101-Ejercicios/007-exportar fusionado.py, líneas 37-43
print("Fusionando LoRA en el modelo base (merge_and_unload)...")
merged = model.merge_and_unload()
merged.eval()

print("Guardando modelo fusionado en:", OUT_PATH)
merged.save_pretrained(OUT_PATH, safe_serialization=True)
```

El modelo fusionado (`.safetensors`) se puede usar sin necesidad de cargar el adaptador LoRA por separado, simplificando la inferencia.

---

### 7. Inferencia con el modelo entrenado (008, 009)

El ejercicio 008 es la inferencia básica: carga el modelo fusionado, aplica el chat template de Qwen y genera con `temperature=0.6` y `do_sample=True`.

El ejercicio 009 mejora significativamente la calidad: usa generación determinista (`do_sample=False`), limita a 64 tokens, añade `repetition_penalty=1.05` y aplica post-procesado con `clean_answer()` que recorta respuestas verbosas y detecta el fallback.

```python
# Archivo: 101-Ejercicios/009-inferencia de mas calidad.py, líneas 74-80
def clean_answer(text: str) -> str:
    if not text:
        return FALLBACK_EXACT
    t = text.strip()
    if FALLBACK_EXACT in t:
        return FALLBACK_EXACT
    first_line = t.splitlines()[0].strip()
    return first_line if first_line else FALLBACK_EXACT
```

---

### 8. Diagnóstico del entrenamiento (010)

Script avanzado que evalúa si el fine-tuning ha funcionado. Compara la *negative log-likelihood* de dos continuaciones alternativas: la respuesta correcta del dataset vs. una respuesta inventada.

```python
# Archivo: 101-Ejercicios/010-diagnostico.py, líneas 98-114
nll_ok, len_ok, mean_ok = neg_loglik_of_continuation(model, tokenizer, score_prompt, ANSWER_OK)
nll_bad, len_bad, mean_bad = neg_loglik_of_continuation(model, tokenizer, score_prompt, ANSWER_BAD)

if nll_ok < nll_bad:
    print("RESULT: Model prefers the FINE-TUNED (OK) answer.")
else:
    print("RESULT: Model prefers the WRONG (BAD) answer -> fine-tune not applied.")
```

Si el modelo asigna mayor probabilidad a la respuesta correcta, el entrenamiento ha funcionado.

---

### 9. Servidor Flask — API REST (server.py)

Un servidor Flask minimalista que expone la interfaz web y un endpoint `/api/chat` que recibe mensajes JSON y devuelve la respuesta del modelo.

```python
# Archivo: 101-Ejercicios/server.py, líneas 14-23
@app.post("/api/chat")
def api_chat():
    data = request.get_json(force=True, silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"ok": False, "error": "Empty message"}), 400
    try:
        answer = infer(message)
        return jsonify({"ok": True, "answer": answer})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
```

---

### 10. Frontend web — HTML, CSS y JavaScript

La interfaz web consta de tres archivos: `index.html` (estructura), `style.css` (257 líneas con diseño tipo ChatGPT) y `app.js` (101 líneas con lógica de chat asíncrono).

```javascript
// Archivo: 101-Ejercicios/web/app.js, líneas 52-76
async function send() {
  const msg = (input.value || "").trim();
  if (!msg) return;
  addMessage("user", msg);
  messageCount++;
  setTyping(true);
  sendBtn.disabled = true;
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg })
    });
    const data = await res.json();
    setTyping(false);
    if (!data.ok) { addMessage("assistant", `Error: ${data.error}`); return; }
    addMessage("assistant", data.answer || "");
  } catch (e) {
    setTyping(false);
    addMessage("assistant", `Error: ${String(e)}`);
  } finally { sendBtn.disabled = false; input.focus(); }
}
```

El CSS incluye modo oscuro automático (`prefers-color-scheme: dark`), animación de typing con parpadeo, transiciones en botones y diseño responsive.

---

### 11. Módulo reutilizable de inferencia (infer.py)

Módulo Python que encapsula la lógica de inferencia con lazy-loading del modelo (singleton), prompt engineering estricto y limpieza de respuesta. Es importado tanto por `server.py` como ejecutable por sí mismo.

```python
# Archivo: 101-Ejercicios/infer.py, líneas 60-80
def load_model():
    global _TOKENIZER, _MODEL
    if _TOKENIZER is not None and _MODEL is not None:
        return _TOKENIZER, _MODEL
    _TOKENIZER = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
    _MODEL = AutoModelForCausalLM.from_pretrained(MODEL_PATH, local_files_only=True)
    _MODEL.eval()
    return _TOKENIZER, _MODEL
```

El patrón singleton evita recargar el modelo en cada petición, ahorrando memoria y tiempo.

---

## Presentación del proyecto

Este proyecto demuestra el flujo completo de personalización de un modelo de inteligencia artificial, de principio a fin. Partimos de un problema real: un modelo de IA genérico no conoce información específica sobre una persona o institución. Cuando le preguntas "¿Quién es Jose Vicente Carratalá?", inventa o no sabe.

La solución es entrenar el modelo con datos propios. Primero creamos un dataset JSONL con 20 pares pregunta-respuesta cuidadosamente redactados. Luego usamos LoRA (Low-Rank Adaptation), una técnica de fine-tuning eficiente que solo entrena unos pocos millones de parámetros en lugar de los miles de millones del modelo completo. Esto permite entrenar en un ordenador normal, incluso sin GPU dedicada.

El script de entrenamiento (006) carga el modelo base Qwen 2.5 de 0.5B parámetros, le aplica adaptadores LoRA en 7 capas del transformer, y entrena durante 80 épocas optimizando solo la pérdida sobre los tokens de respuesta. Después, fusionamos los adaptadores con el modelo base (007) para obtener un modelo independiente.

Para verificar que el entrenamiento ha funcionado, el script de diagnóstico (010) compara la probabilidad que el modelo asigna a la respuesta correcta vs. una incorrecta. Si prefiere la correcta, el fine-tuning ha tenido éxito.

Finalmente, exponemos el modelo a través de un servidor Flask con una API REST y una interfaz web tipo chat con diseño profesional, modo oscuro automático y comunicación asíncrona con fetch.

---

## Conclusión

Este proyecto muestra que el entrenamiento personalizado de modelos de IA es accesible para un estudiante de programación. Con herramientas de código abierto (Hugging Face Transformers, PEFT, PyTorch), un dataset modesto de 20 ejemplos y la técnica LoRA, es posible enseñarle a un modelo información nueva que no conocía. La cadena completa — datos JSONL → entrenamiento LoRA → fusión → inferencia → servidor web → interfaz chat — demuestra la integración de múltiples tecnologías (Python, Flask, HTML, CSS, JavaScript) en un proyecto cohesivo. El diagnóstico con negative log-likelihood añade rigor al verificar cuantitativamente que el modelo ha aprendido, y la interfaz web permite cualquier persona interactuar con el resultado final.
