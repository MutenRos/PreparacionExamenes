#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

PROJECT_DIR = "/var/www/html/dam2526/Primero/Programación/012-Inteligencia Artificial/002-Entrenar IA personalizada/101-Ejercicios/"
MODEL_PATH = os.path.join(PROJECT_DIR, "qwen25-05b-jvc-merged")

# Cache de HF en sitio escribible (por si acaso)
os.environ["HF_HOME"] = "/tmp/hf-cache"
os.makedirs(os.environ["HF_HOME"], exist_ok=True)

# Extra defensivo: no Internet
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"


FALLBACK_EXACT = "No lo sé basándome en mi entrenamiento."


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def list_model_files(model_dir: str, max_items: int = 200):
    try:
        items = sorted(os.listdir(model_dir))
    except Exception as ex:
        eprint(f"[ERROR] Cannot list directory: {model_dir} -> {ex}")
        return

    eprint(f"[DEBUG] Files in {model_dir} (showing up to {max_items}):")
    for i, name in enumerate(items[:max_items], start=1):
        p = os.path.join(model_dir, name)
        try:
            sz = os.path.getsize(p)
        except Exception:
            sz = -1
        eprint(f"  {i:03d}. {name} ({sz} bytes)")
    if len(items) > max_items:
        eprint(f"  ... ({len(items) - max_items} more)")


def build_prompt_qa(user_question: str) -> str:
    """
    Formato Q/A alineado con dataset {"question","answer"}.

    Importante:
    - Forzamos que, si no sabe, responda SOLO con la frase exacta y NADA MÁS.
    - Esto NO garantiza al 100% que el modelo obedezca, por eso además recortamos en post-proceso.
    """
    instruction = (
        "Instrucciones estrictas:\n"
        "- Responde únicamente con información aprendida en tu entrenamiento (fine-tuning).\n"
        "- No inventes datos.\n"
        f"- Si la respuesta NO está en tu entrenamiento, responde EXACTAMENTE y SOLO con esta frase (sin añadir nada):\n"
        f"{FALLBACK_EXACT}\n"
        "- Prohibido añadir explicaciones, notas, justificaciones o texto extra.\n"
        "\n"
    )
    return (
        f"{instruction}"
        f"Pregunta: {user_question}\n"
        f"Respuesta:"
    )


def clean_answer(text: str) -> str:
    """
    1) Si el modelo incluye la frase de fallback pero añade texto extra, devolvemos SOLO la frase exacta.
    2) Si no incluye fallback, devolvemos la primera línea “útil” (hasta salto de línea) para evitar verborrea.
    """
    if not text:
        return FALLBACK_EXACT

    t = text.strip()

    # Si aparece el fallback, devolvemos SOLO el fallback exacto.
    if FALLBACK_EXACT in t:
        return FALLBACK_EXACT

    # Si el modelo intenta “explicar” o alargar, recorta a la primera línea.
    first_line = t.splitlines()[0].strip()
    return first_line if first_line else FALLBACK_EXACT


def main():
    if len(sys.argv) < 2:
        eprint("No prompt provided")
        sys.exit(1)

    question = sys.argv[1]

    eprint("[DEBUG] MODEL_PATH:", MODEL_PATH)
    if not os.path.isdir(MODEL_PATH):
        eprint("[ERROR] MODEL_PATH does not exist or is not a directory.")
        sys.exit(2)

    list_model_files(MODEL_PATH)

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH,
        local_files_only=True,
        fix_mistral_regex=True
    )

    use_cuda = torch.cuda.is_available()
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        local_files_only=True,
        device_map="auto" if use_cuda else None,
        dtype=torch.float16 if use_cuda else torch.float32
    )

    if not use_cuda:
        model.to("cpu")

    model.eval()

    eprint("[DEBUG] Tokenizer name_or_path:", getattr(tokenizer, "name_or_path", None))
    eprint("[DEBUG] Model config _name_or_path:", getattr(model.config, "_name_or_path", None))
    eprint("[DEBUG] CUDA available:", use_cuda)
    eprint("[DEBUG] Model device:", getattr(model, "device", "unknown"))

    prompt_text = build_prompt_qa(question)

    inputs = tokenizer(prompt_text, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    input_len = inputs["input_ids"].shape[-1]

    # Generación determinista y corta para minimizar “derivas”
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=64,
            do_sample=False,
            num_beams=1,
            repetition_penalty=1.05,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
        )

    gen_ids = output_ids[0, input_len:]
    raw = tokenizer.decode(gen_ids, skip_special_tokens=True)

    answer = clean_answer(raw)
    print(answer)


if __name__ == "__main__":
    main()

