"""003-crear imagen.py
Genera una imagen a partir de un prompt de texto usando Stable Diffusion.
Requiere: torch, diffusers, PIL (Pillow).
"""
import os
import sys
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

# --- Configuración ---
MODEL_ID = "runwayml/stable-diffusion-v1-5"  # example (may require HF access depending on model)
PROMPT = "a cozy modern desk setup, cinematic lighting, ultra detailed, 35mm photo"
OUTPUT_FILE = "out.png"
STEPS = 30           # numero de pasos de inferencia (mas pasos = mas calidad)
GUIDANCE = 7.5       # escala de guidance (adherencia al prompt)
IMG_SIZE = 512       # ancho y alto en pixeles

# --- Seleccion de dispositivo (GPU si hay, si no CPU) ---
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32
print(f"Dispositivo seleccionado: {device}")

try:
    # --- Cargar el pipeline de Stable Diffusion ---
    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
        safety_checker=None,  # optional
    )
    pipe = pipe.to(device)

    # --- Generar la imagen ---
    print(f"Generando imagen con prompt: '{PROMPT}'...")
    img = pipe(
        PROMPT,
        num_inference_steps=STEPS,
        guidance_scale=GUIDANCE,
        height=IMG_SIZE,
        width=IMG_SIZE,
    ).images[0]

    # --- Guardar resultado ---
    img.save(OUTPUT_FILE)
    print(f"Imagen guardada en: {os.path.abspath(OUTPUT_FILE)}")

except Exception as e:
    print(f"Error al generar la imagen: {e}", file=sys.stderr)
    sys.exit(1)

