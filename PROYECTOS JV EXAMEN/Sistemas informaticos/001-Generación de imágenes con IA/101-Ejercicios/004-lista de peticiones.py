"""004-lista de peticiones.py
Genera multiples imagenes a partir de una lista de prompts.
Mejora: el pipeline se carga UNA sola vez fuera del bucle para mayor eficiencia.
"""
import os
import sys
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

MODEL_ID = "runwayml/stable-diffusion-v1-5"  # example (may require HF access depending on model)

# Lista de prompts a generar
lista = [
  'a green dog over green grass',
  'a pink cat over a sofa',
  'a horse running in the forest'
]

# --- Cargar el pipeline UNA sola vez (mejora de rendimiento) ---
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32
print(f"Dispositivo: {device} | Generando {len(lista)} imagenes...")

try:
    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
        safety_checker=None,  # optional
    )
    pipe = pipe.to(device)
except Exception as e:
    print(f"Error al cargar el modelo: {e}", file=sys.stderr)
    sys.exit(1)

# --- Generar cada imagen de la lista ---
for i, peticion in enumerate(lista, start=1):
    try:
        print(f"[{i}/{len(lista)}] Generando: '{peticion}'...")
        img = pipe(
            peticion,
            num_inference_steps=30,
            guidance_scale=7.5,
            height=256,
            width=256,
        ).images[0]

        # Nombre de archivo basado en el prompt
        nombre_archivo = peticion + ".png"
        img.save(nombre_archivo)
        print(f"  -> Guardada: {nombre_archivo}")
    except Exception as e:
        print(f"  -> Error generando '{peticion}': {e}", file=sys.stderr)

