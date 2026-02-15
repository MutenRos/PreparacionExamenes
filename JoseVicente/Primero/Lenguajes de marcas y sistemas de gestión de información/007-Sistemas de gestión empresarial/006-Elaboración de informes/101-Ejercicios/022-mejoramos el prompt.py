#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv
import json
import requests
from collections import defaultdict

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
URL = "http://localhost:11434/api/generate"

# Recommended for strict grading:
#   "gemma2:9b-instruct-q4_0"
#   "llama3.1:8b-instruct-q4_0"
MODEL = "gemma2:9b-instruct-q4_0"

CSV_PATH = "respuestas.csv"

OLLAMA_OPTIONS = {
    "temperature": 0.0,
    "top_p": 1.0,
    "num_ctx": 4096,
}

# --------------------------------------------------
# ANSWER KEY (THE ONLY TRUTH)
# Keys must match question text found in the CSV.
# --------------------------------------------------
ANSWER_KEY = {
    "PHP es un lenguaje de:": "Servidor",
    "Javascript es un lenguaje de": "Cliente",
    "CSS es un lenguaje de": "Estilo",
    "HTML es un lenguaje de": "Marcas",
    "IF es:": "Estructura condicional",
    "While es una estructura de:": "Bucle",
}

# --------------------------------------------------
# READ CSV RAW (NO PARSING FOR LLM)
# --------------------------------------------------
try:
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        csv_raw = f.read()
except FileNotFoundError:
    print(f"ERROR: No existe el archivo: {CSV_PATH}", file=sys.stderr)
    sys.exit(1)

# --------------------------------------------------
# LOCAL PARSING (FOR BASE-10 SCORES TABLE)
#   - Ignores rows with empty name
#   - Treats names as distinct (case-sensitive) as requested
#   - Computes score over only questions that exist in ANSWER_KEY
# --------------------------------------------------
def compute_scores_base10(csv_path: str, answer_key: dict) -> dict:
    stats = defaultdict(lambda: {"aciertos": 0, "fallos": 0, "sin_clave": 0})

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue

            # Expect at least: name, question, answer, options_json
            # If malformed, skip safely
            if len(row) < 3:
                continue

            name = (row[0] or "").strip()
            question = (row[1] or "").strip()
            answer = (row[2] or "").strip()

            # Rule: ignore empty-name rows completely
            if name == "":
                continue

            if question not in answer_key:
                stats[name]["sin_clave"] += 1
                continue

            expected = answer_key[question]
            if answer == expected:
                stats[name]["aciertos"] += 1
            else:
                stats[name]["fallos"] += 1

    # Convert to base-10 (0..10) using only questions with key
    results = {}
    for name, s in stats.items():
        total_con_clave = s["aciertos"] + s["fallos"]
        if total_con_clave <= 0:
            nota10 = None
        else:
            nota10 = (s["aciertos"] / total_con_clave) * 10.0
        results[name] = {
            **s,
            "total_con_clave": total_con_clave,
            "nota_sobre_10": nota10,
        }

    return results


def render_console_table(scores: dict) -> str:
    # Sort: highest nota first, then name
    def sort_key(item):
        name, s = item
        nota = s["nota_sobre_10"]
        return (-(nota if nota is not None else -1e9), name)

    rows = []
    for name, s in sorted(scores.items(), key=sort_key):
        nota = s["nota_sobre_10"]
        nota_str = "N/A" if nota is None else f"{nota:.2f}"
        rows.append([
            name,
            str(s["aciertos"]),
            str(s["fallos"]),
            str(s["sin_clave"]),
            str(s["total_con_clave"]),
            nota_str,
        ])

    headers = ["Alumno", "OK", "FAIL", "SIN_CLAVE", "TOTAL_CLAVE", "NOTA/10"]

    # column widths
    cols = list(zip(headers, *rows)) if rows else [headers]
    widths = [max(len(str(cell)) for cell in col) for col in cols]

    def fmt_row(r):
        return " | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(r))

    sep = "-+-".join("-" * w for w in widths)

    out = []
    out.append(fmt_row(headers))
    out.append(sep)
    for r in rows:
        out.append(fmt_row(r))
    return "\n".join(out)


scores = compute_scores_base10(CSV_PATH, ANSWER_KEY)
table_txt = render_console_table(scores)

# --------------------------------------------------
# BUILD PROMPT (HARDENED) FOR THE DETAILED REPORT
# --------------------------------------------------
def format_answer_key(key: dict) -> str:
    return "\n".join([f'- "{q}" -> "{a}"' for q, a in key.items()])

prompt = f"""
Eres un corrector AUTOMÁTICO. Debes seguir reglas estrictas y NO inventar información.

Tienes el contenido bruto de un CSV (respuestas.csv) con filas con este patrón:
NOMBRE, PREGUNTA, RESPUESTA, OPCIONES_JSON

REGLAS ESTRICTAS (OBLIGATORIAS):
1) NO adivines "la respuesta correcta" si no está definida en la CLAVE.
2) Solo puedes marcar Correcto/Incorrecto comparando con la CLAVE DE RESPUESTAS (única verdad).
3) Si una fila no tiene nombre (vacío), IGNÓRALA por completo (no cuenta para nadie).
4) Trata nombres distintos como alumnos distintos: "Javi" != "javier" != "Javier".
5) Si la pregunta no está en la CLAVE, marca esa fila como "SIN CLAVE" (pero igualmente muéstrala en el alumno).
6) Por alumno: lista cada pregunta con:
   - Pregunta
   - Respuesta dada
   - Veredicto: OK / FAIL / SIN_CLAVE
   - Si hay clave: "Esperada: <...>"
7) FORMATO:
   - Informe estilo terminal Linux, monoespaciado, claro y sin relleno.

CLAVE DE RESPUESTAS (única verdad):
{format_answer_key(ANSWER_KEY)}

=== respuestas.csv (BRUTO; NO lo reescribas como código) ===
{csv_raw}
=== fin del archivo ===

Genera el informe.
"""

# --------------------------------------------------
# REQUEST TO OLLAMA (DETAILED REPORT)
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
    print(f"ERROR: No se pudo conectar a Ollama en {URL}: {e}", file=sys.stderr)
    sys.exit(2)

if response.status_code != 200:
    print(f"ERROR: Ollama devolvió HTTP {response.status_code}\n{response.text}", file=sys.stderr)
    sys.exit(3)

data = response.json()
report = data.get("response", "").strip()
if not report:
    print("ERROR: Respuesta vacía del modelo.", file=sys.stderr)
    print(data, file=sys.stderr)
    sys.exit(4)

# --------------------------------------------------
# OUTPUT: TABLE + REPORT
# --------------------------------------------------
print()
print("=== TABLA DE NOTAS (0..10) ===")
print(table_txt)
print()
print("=== INFORME DETALLADO ===")
print(report)

