#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
from datetime import datetime

import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model

# -----------------------------
# CONFIG
# -----------------------------
DATA_PATH = "outputs/*.jsonl"

BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
OUTPUT_DIR = "./qwen25-05b-jvc"          # adapter output (not merged)

MAX_LENGTH = 512

# With ~20 examples, you need MANY steps. Two options:
# - Use many epochs (easiest)
# - Or use max_steps (most explicit)
NUM_EPOCHS = 80                               # <- increase a lot for tiny dataset
LR = 2e-4
BATCH_SIZE = 1
GRAD_ACCUM = 4

LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05

SYSTEM_PROMPT = (
    "Eres un asistente en español. Responde de forma clara y precisa."
)

# -----------------------------
# Reporting helper (optional)
# -----------------------------
def generate_markdown_report(start_dt, end_dt, device, dataset_size, training_args, train_metrics):
    duration = end_dt - start_dt
    epoch = int(end_dt.timestamp())
    timestamp_str = end_dt.strftime("%Y%m%d_%H%M%S")
    report_name = f"reporte_entrenamiento_{timestamp_str}_{epoch}.md"
    report_path = os.path.join(OUTPUT_DIR, report_name)

    try:
        import transformers
        tver = transformers.__version__
    except Exception:
        tver = "unknown"

    try:
        import peft as peft_mod
        pver = peft_mod.__version__
    except Exception:
        pver = "unknown"

    lines = []
    lines.append("# Informe de entrenamiento (LoRA SFT Qwen2.5)\n")
    lines.append("## Resumen\n")
    lines.append(f"- Inicio: {start_dt}")
    lines.append(f"- Fin: {end_dt}")
    lines.append(f"- Duración: {duration}")
    lines.append(f"- Modelo base: `{BASE_MODEL}`")
    lines.append(f"- Output: `{OUTPUT_DIR}`")
    lines.append(f"- Dataset size: {dataset_size}")
    lines.append(f"- Device: {device}")
    lines.append("")
    lines.append("## Entorno\n")
    lines.append(f"- OS: {platform.platform()}")
    lines.append(f"- Python: {platform.python_version()}")
    lines.append(f"- Torch: {torch.__version__}")
    lines.append(f"- Transformers: {tver}")
    lines.append(f"- PEFT: {pver}")
    lines.append(f"- CUDA available: {torch.cuda.is_available()}")
    lines.append("")
    lines.append("## TrainingArguments\n")
    for k, v in sorted(training_args.to_dict().items()):
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Métricas\n")
    if train_metrics:
        for k, v in train_metrics.items():
            lines.append(f"- {k}: {v}")
    else:
        lines.append("- (sin métricas)")
    lines.append("")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"📝 Reporte: {report_path}")


def main():
    start_dt = datetime.now()

    # Device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"💻 Device: {device}")

    # Load dataset
    print("📥 Loading dataset...")
    raw = load_dataset("json", data_files=DATA_PATH, split="train")
    print(f"✅ Loaded: {len(raw)} examples")

    # Tokenizer
    print("✅ Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Base model
    print("✅ Loading base model...")
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        device_map="auto" if device == "cuda" else None,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    )
    if device == "cpu":
        model.to("cpu")

    # LoRA
    print("✅ Applying LoRA...")
    lora = LoraConfig(
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ],
    )
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    # -----
    # Build text + labels (answer-only loss)
    # -----
    print("🧱 Building chat samples + answer-only labels...")

    def build_tokens(example):
        q = example.get("question", "")
        a = example.get("answer", "")
        if not isinstance(q, str):
            q = str(q)
        if not isinstance(a, str):
            a = str(a)

        # Prompt WITHOUT answer (used only to compute prompt length)
        conv_prompt = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": q},
            {"role": "assistant", "content": ""},  # empty assistant
        ]

        # Full conversation WITH answer
        conv_full = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": q},
            {"role": "assistant", "content": a},
        ]

        # Render both using the same chat template
        prompt_text = tokenizer.apply_chat_template(
            conv_prompt, tokenize=False, add_generation_prompt=False
        )
        full_text = tokenizer.apply_chat_template(
            conv_full, tokenize=False, add_generation_prompt=False
        )

        # Tokenize full text
        tok = tokenizer(
            full_text,
            truncation=True,
            max_length=MAX_LENGTH,
            padding="max_length",
        )

        # Tokenize prompt to get prompt length (in tokens) aligned with same tokenizer
        prompt_tok = tokenizer(
            prompt_text,
            truncation=True,
            max_length=MAX_LENGTH,
            padding="max_length",
        )

        input_ids = tok["input_ids"]
        attn = tok["attention_mask"]

        # Labels: only answer tokens contribute
        labels = input_ids.copy()

        # Mask everything up to prompt length
        prompt_len = 0
        # Compute prompt_len as number of non-pad tokens in prompt_tok
        # (attention_mask gives non-pad count)
        prompt_len = int(sum(prompt_tok["attention_mask"]))

        for i in range(min(prompt_len, len(labels))):
            labels[i] = -100

        # Mask padding in labels too
        for i in range(len(labels)):
            if attn[i] == 0:
                labels[i] = -100

        tok["labels"] = labels
        return tok

    tokenized = raw.map(build_tokens, remove_columns=raw.column_names)

    # -----
    # Training args
    # -----
    print("✅ TrainingArguments...")
    args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        overwrite_output_dir=True,

        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM,
        learning_rate=LR,
        weight_decay=0.0,
        warmup_ratio=0.03,

        logging_steps=10,
        save_steps=200,
        save_total_limit=2,

        fp16=(device == "cuda"),
        bf16=False,

        report_to="none",
        dataloader_pin_memory=False,
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized,
    )

    # Train
    print("🚂 Training...")
    out = trainer.train()
    print("🏁 Done.")

    # Save adapter + tokenizer
    print("💾 Saving adapter + tokenizer...")
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    # Report
    end_dt = datetime.now()
    metrics = getattr(out, "metrics", None) if out is not None else None
    generate_markdown_report(start_dt, end_dt, device, len(raw), args, metrics)


if __name__ == "__main__":
    main()

