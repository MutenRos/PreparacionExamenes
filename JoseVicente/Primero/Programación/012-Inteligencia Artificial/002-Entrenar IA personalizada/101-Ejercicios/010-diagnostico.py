#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import math
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

PROJECT_DIR = "/var/www/html/dam2526/Primero/Programación/012-Inteligencia Artificial/002-Entrenar IA personalizada/101-Ejercicios/"
MODEL_PATH = os.path.join(PROJECT_DIR, "qwen25-05b-jvc-merged")

os.environ["HF_HOME"] = "/tmp/hf-cache"
os.makedirs(os.environ["HF_HOME"], exist_ok=True)
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"

QUESTION = "¿A qué se dedica Jose Vicente Carratalá Sanchis profesionalmente?"
ANSWER_OK = "Jose Vicente Carratalá Sanchis se dedica al desarrollo de software, a la formación técnica en programación y a la creación de proyectos tecnológicos educativos."
ANSWER_BAD = "Es un ingeniero de telecomunicaciones."

def eprint(*a, **k):
    print(*a, file=sys.stderr, **k)

def load():
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
    eprint("[DEBUG] CUDA:", use_cuda, "| device:", getattr(model, "device", None))
    return tokenizer, model

@torch.no_grad()
def generate(model, tokenizer, prompt, max_new_tokens=96):
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    input_len = inputs["input_ids"].shape[-1]
    out = model.generate(
        **inputs,
        do_sample=False,
        num_beams=1,
        max_new_tokens=max_new_tokens,
        repetition_penalty=1.05,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
    )
    gen_ids = out[0, input_len:]
    return tokenizer.decode(gen_ids, skip_special_tokens=True).strip()

@torch.no_grad()
def neg_loglik_of_continuation(model, tokenizer, prompt, continuation):
    """
    Score = negative log-likelihood of 'continuation' given 'prompt'.
    Lower is better (more probable).
    """
    # Encode full text and prompt separately
    full = prompt + continuation
    full_ids = tokenizer(full, return_tensors="pt")["input_ids"].to(model.device)
    prompt_ids = tokenizer(prompt, return_tensors="pt")["input_ids"].to(model.device)

    # We want loss only on continuation tokens
    # labels: -100 for prompt part, actual ids for continuation part
    labels = full_ids.clone()
    labels[:, :prompt_ids.shape[1]] = -100

    outputs = model(full_ids, labels=labels)
    loss = outputs.loss  # mean loss over non -100 tokens
    # Convert to total NLL approx: mean_loss * number_of_cont_tokens
    cont_len = full_ids.shape[1] - prompt_ids.shape[1]
    total_nll = float(loss) * cont_len
    return total_nll, cont_len, float(loss)

def main():
    tokenizer, model = load()

    eprint("\n=== CHECK A: exact QA completion ===")
    prompt_a = f"Pregunta: {QUESTION}\nRespuesta:"
    gen_a = generate(model, tokenizer, prompt_a)
    print("PROMPT:\n", prompt_a, "\n---\nGEN:\n", gen_a, "\n", sep="")

    eprint("\n=== CHECK B: few-shot (your pair included) ===")
    prompt_b = (
        "Ejemplos:\n"
        "Pregunta: ¿Quién es Jose Vicente Carratalá Sanchis?\n"
        "Respuesta: Jose Vicente Carratalá Sanchis es un desarrollador de software, formador y creador de contenidos técnicos especializado en programación, sistemas e inteligencia artificial.\n"
        f"Pregunta: {QUESTION}\n"
        "Respuesta:"
    )
    gen_b = generate(model, tokenizer, prompt_b)
    print("PROMPT:\n", prompt_b, "\n---\nGEN:\n", gen_b, "\n", sep="")

    eprint("\n=== CHECK C: scoring OK vs BAD continuation ===")
    score_prompt = f"Pregunta: {QUESTION}\nRespuesta: "
    nll_ok, len_ok, mean_ok = neg_loglik_of_continuation(model, tokenizer, score_prompt, ANSWER_OK)
    nll_bad, len_bad, mean_bad = neg_loglik_of_continuation(model, tokenizer, score_prompt, ANSWER_BAD)

    print("SCORING PROMPT:\n", score_prompt, "\n", sep="")
    print(f"OK  continuation tokens={len_ok} mean_loss={mean_ok:.4f} total_nll={nll_ok:.2f}")
    print(f"BAD continuation tokens={len_bad} mean_loss={mean_bad:.4f} total_nll={nll_bad:.2f}")

    if nll_ok < nll_bad:
        print("\nRESULT: Model prefers the FINE-TUNED (OK) answer.")
    else:
        print("\nRESULT: Model prefers the WRONG (BAD) answer -> fine-tune not applied / not learned.")

if __name__ == "__main__":
    main()

