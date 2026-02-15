#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

PROJECT_DIR = "/var/www/html/dam2526/Primero/Programación/012-Inteligencia Artificial/002-Entrenar IA personalizada/101-Ejercicios/"
MODEL_PATH = os.path.join(PROJECT_DIR, "qwen25-05b-jvc-merged")

# Cache HF en sitio escribible
os.environ["HF_HOME"] = "/tmp/hf-cache"
os.makedirs(os.environ["HF_HOME"], exist_ok=True)

# Offline defensivo
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"

FALLBACK_EXACT = "No lo sé basándome en mi entrenamiento."

# Lazy-loaded singletons
_TOKENIZER = None
_MODEL = None


def build_prompt_qa(user_question: str) -> str:
    instruction = (
        "Instrucciones estrictas:\n"
        "- Responde únicamente con información aprendida en tu entrenamiento (fine-tuning).\n"
        "- No inventes datos.\n"
        f"- Si la respuesta NO está en tu entrenamiento, responde EXACTAMENTE y SOLO con esta frase (sin añadir nada):\n"
        f"{FALLBACK_EXACT}\n"
        "- Prohibido añadir explicaciones, notas, justificaciones o texto extra.\n"
        "\n"
    )
    return f"{instruction}Pregunta: {user_question}\nRespuesta:"


def clean_answer(text: str) -> str:
    if not text:
        return FALLBACK_EXACT

    t = text.strip()

    # If fallback appears anywhere, return only fallback.
    if FALLBACK_EXACT in t:
        return FALLBACK_EXACT

    # Return only first non-empty line.
    for line in t.splitlines():
        line = line.strip()
        if line:
            return line

    return FALLBACK_EXACT


def load_model():
    global _TOKENIZER, _MODEL
    if _TOKENIZER is not None and _MODEL is not None:
        return _TOKENIZER, _MODEL

    _TOKENIZER = AutoTokenizer.from_pretrained(
        MODEL_PATH,
        local_files_only=True,
        fix_mistral_regex=True
    )

    use_cuda = torch.cuda.is_available()
    _MODEL = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        local_files_only=True,
        device_map="auto" if use_cuda else None,
        dtype=torch.float16 if use_cuda else torch.float32
    )
    if not use_cuda:
        _MODEL.to("cpu")
    _MODEL.eval()

    return _TOKENIZER, _MODEL


def infer(question: str, max_new_tokens: int = 64) -> str:
    tokenizer, model = load_model()

    prompt_text = build_prompt_qa(question)
    inputs = tokenizer(prompt_text, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    input_len = inputs["input_ids"].shape[-1]

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            num_beams=1,
            repetition_penalty=1.05,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
        )

    gen_ids = output_ids[0, input_len:]
    raw = tokenizer.decode(gen_ids, skip_special_tokens=True)
    return clean_answer(raw)


def main():
    if len(sys.argv) < 2:
        print("No prompt provided", file=sys.stderr)
        sys.exit(1)

    question = sys.argv[1]
    print(infer(question))


if __name__ == "__main__":
    main()

