#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
URL = "http://localhost:11434/api/generate"

# Models recommended for reasoning + grading
# - gemma2:9b-instruct-q4_0
# - llama3.1:8b-instruct-q4_0
MODEL = "gemma2:9b-instruct-q4_0"

CSV_PATH = "respuestas.csv"

OLLAMA_OPTIONS = {
    "temperature": 0.0,
    "top_p": 1.0,
    "num_ctx": 4096,
}

# --------------------------------------------------
# READ CSV RAW (NO PARSING)
# --------------------------------------------------
try:
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        csv_raw = f.read()
except FileNotFoundError:
    print(f"ERROR: No existe el archivo: {CSV_PATH}", file=sys.stderr)
    sys.exit(1)

# --------------------------------------------------
# PROMPT (GENERIC, NO ANSWER KEYS)
# --------------------------------------------------
prompt = f"""
Eres un evaluador AUTOMÁTICO de exámenes de programación e informática.

Dispones del contenido bruto de un archivo CSV llamado respuestas.csv.
Cada fila sigue este patrón lógico:

NOMBRE, PREGUNTA, RESPUESTA, OPCIONES_JSON

REGLAS ESTRICTAS:
1) NO asumas claves externas ni respuestas predefinidas.
2) Evalúa cada respuesta según el conocimiento estándar de programación.
3) Si una fila NO tiene nombre, ignórala completamente.
4) Trata los nombres de forma literal (no normalices):
   "Javi" != "javier" != "Javier".
5) Evalúa si la respuesta es:
   - Correcta
   - Parcialmente correcta
   - Incorrecta
6) Usa solo tu conocimiento general de informática y programación.

SALIDA OBLIGATORIA (EN ESTE ORDEN):

1) TABLA RESUMEN (formato terminal Linux):
   Columnas:
   - Alumno
   - Aciertos
   - Parciales
   - Fallos
   - Nota_sobre_10

   La nota sobre 10 se calcula así:
   - Correcta = 1 punto
   - Parcial = 0.5 puntos
   - Incorrecta = 0 puntos
   - Nota = (puntos_obtenidos / preguntas_totales) * 10

2) INFORME DETALLADO:
   Para cada alumno:
   - Lista de preguntas
   - Respuesta dada
   - Evaluación (OK / PARCIAL / FAIL)
   - Breve justificación técnica
   - Resumen final del alumno

FORMATO:
- Estilo terminal Linux
- Texto monoespaciado
- Sin emojis
- Sin explicaciones meta
- Sin referencias al prompt

=== respuestas.csv (BRUTO) ===
{csv_raw}
=== fin del archivo ===

Genera ahora la salida completa.
"""

# --------------------------------------------------
# REQUEST
# --------------------------------------------------
payload = {
    "model": MODEL,
    "prompt": prompt,
    "stream": False,
    "options": OLLAMA_OPTIONS,
}

try:
    response = requests.post(URL, json=payload, timeout=120)
except requests.RequestException as e:
    print(f"ERROR: No se pudo conectar a Ollama: {e}", file=sys.stderr)
    sys.exit(2)

if response.status_code != 200:
    print(f"ERROR HTTP {response.status_code}\n{response.text}", file=sys.stderr)
    sys.exit(3)

data = response.json()
output = data.get("response", "").strip()

if not output:
    print("ERROR: Respuesta vacía del modelo", file=sys.stderr)
    print(data, file=sys.stderr)
    sys.exit(4)

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------
print(output)

