#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b-instruct-q4_0"
CSV_PATH = "respuestas.csv"

# --------------------------------------------------
# READ CSV RAW (NO PARSING)
# --------------------------------------------------
with open(CSV_PATH, "r", encoding="utf-8") as f:
    csv_raw = f.read()

# --------------------------------------------------
# PROMPT
# --------------------------------------------------
prompt = f"""
A continuación tienes el contenido bruto de un archivo CSV llamado respuestas.csv.

NO lo transformes ni lo reinterpretas como código.
Analízalo conceptualmente.

=== respuestas.csv ===
{csv_raw}
=== fin del archivo ===

Petición:
realiza una evaluación de cada alumno y presenta un informe en formato de terminal de linux
"""

# --------------------------------------------------
# REQUEST
# --------------------------------------------------
payload = {
    "model": MODEL,
    "prompt": prompt,
    "stream": False
}

response = requests.post(URL, json=payload)
data = response.json()

print(data["response"])

