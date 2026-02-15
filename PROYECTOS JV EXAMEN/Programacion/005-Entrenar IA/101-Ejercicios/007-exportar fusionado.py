#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Modelo base de Hugging Face
BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"

# Carpeta donde guardaste los adaptadores tras el entrenamiento
ADAPTER_PATH = "./qwen25-05b-jvc"

# Carpeta de salida con el modelo ya fusionado (base + LoRA)
OUT_PATH = "./qwen25-05b-jvc-merged"


def main():
    os.makedirs(OUT_PATH, exist_ok=True)

    use_cuda = torch.cuda.is_available()
    dtype = torch.float16 if use_cuda else torch.float32

    print("Cargando modelo base:", BASE_MODEL)
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=dtype,
        device_map="auto" if use_cuda else None,
    )

    print("Cargando adaptadores LoRA desde:", ADAPTER_PATH)
    model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)

    print("Fusionando LoRA en el modelo base (merge_and_unload)...")
    merged = model.merge_and_unload()
    merged.eval()

    print("Guardando modelo fusionado en:", OUT_PATH)
    merged.save_pretrained(
        OUT_PATH,
        safe_serialization=True,  # -> model.safetensors
    )

    # IMPORTANTE: guardar el tokenizer desde el ADAPTER_PATH (o desde donde entrenaste)
    # porque puede incluir added_tokens/chat_template, etc.
    print("Guardando tokenizer desde:", ADAPTER_PATH)
    tokenizer = AutoTokenizer.from_pretrained(ADAPTER_PATH, use_fast=True)
    tokenizer.save_pretrained(OUT_PATH)

    print("✅ Modelo fusionado guardado correctamente.")


if __name__ == "__main__":
    main()

