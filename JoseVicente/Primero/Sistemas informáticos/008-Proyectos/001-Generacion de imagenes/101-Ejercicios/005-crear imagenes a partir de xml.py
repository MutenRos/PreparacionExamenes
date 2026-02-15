#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import time
import base64
import hashlib
import requests
import xml.etree.ElementTree as ET
from pathlib import Path

import torch
from diffusers import StableDiffusionPipeline


# =========================
# CONFIG
# =========================
XML_FILE = "producto.xml"
OUTPUT_DIR = "generated_images"   # images will be saved here (relative to script)
UPDATED_XML_FILE = "producto.updated.xml"

# ---- Ollama ----
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "llama3:latest"  # change to your local model if needed
OLLAMA_TIMEOUT = 300

# ---- Diffusers / Stable Diffusion ----
MODEL_ID = "runwayml/stable-diffusion-v1-5"  # may require HF access; swap if you use a local checkpoint
STEPS = 30
GUIDANCE = 7.5
WIDTH = 1024
HEIGHT = 576  # 16:9 (good for web banners). You can change per-section if you want.
SEED_BASE = 12345  # deterministic-ish; prompt changes still change outputs

# If you want smaller faster images:
# WIDTH = 768
# HEIGHT = 432


# =========================
# HELPERS
# =========================
def slugify(s: str, maxlen: int = 80) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"[\s_-]+", "-", s)
    s = s.strip("-")
    if not s:
        s = "image"
    return s[:maxlen]


def safe_filename_from_alt(section: str, alt: str, ext: str = ".png") -> str:
    base = slugify(f"{section}-{alt}")
    return f"{base}{ext}"


def ollama_generate_json(system: str, user: str) -> dict:
    """
    Asks Ollama to return strict JSON. Retries once if parsing fails.
    """
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": user,
        "system": system,
        "stream": False,
        "options": {
            "temperature": 0.4,
        }
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=OLLAMA_TIMEOUT)
    r.raise_for_status()
    text = r.json().get("response", "").strip()

    # Try to extract JSON even if model adds extra text.
    def extract_json(t: str) -> str:
        start = t.find("{")
        end = t.rfind("}")
        if start != -1 and end != -1 and end > start:
            return t[start:end+1]
        return t

    js = extract_json(text)
    try:
        return json.loads(js)
    except json.JSONDecodeError:
        # Retry with stricter instruction
        payload["options"]["temperature"] = 0.2
        payload["prompt"] = user + "\n\nDEVUELVE SOLO JSON. SIN TEXTO EXTRA."
        r2 = requests.post(OLLAMA_URL, json=payload, timeout=OLLAMA_TIMEOUT)
        r2.raise_for_status()
        text2 = r2.json().get("response", "").strip()
        js2 = extract_json(text2)
        return json.loads(js2)


def build_context_from_xml(root: ET.Element) -> dict:
    """
    Builds a compact context object from key fields in the XML.
    """
    def get_text(path: str) -> str:
        el = root.find(path)
        return (el.text or "").strip() if el is not None and el.text else ""

    title = get_text("./meta/title")
    category = get_text("./meta/category")
    slug = get_text("./meta/slug")

    value_prop = get_text("./hero/valueProposition")
    subtitle = get_text("./hero/subtitle")

    # Collect some bullets for richer context
    problems = [((it.text or "").strip()) for it in root.findall("./problem/items/item")]
    benefits = [((it.text or "").strip()) for it in root.findall("./benefits/items/item")]
    features = []
    for f in root.findall("./keyFeatures/feature"):
        name = (f.findtext("name") or "").strip()
        benefit = (f.findtext("benefit") or "").strip()
        if name or benefit:
            features.append({"name": name, "benefit": benefit})

    return {
        "slug": slug,
        "title": title,
        "category": category,
        "valueProposition": value_prop,
        "subtitle": subtitle,
        "problems": problems[:8],
        "benefits": benefits[:8],
        "features": features[:10],
        "style": {
            "look": "apple-like, clean, modern SaaS, minimal, premium",
            "avoid": "text, letters, logos, watermarks, UI screenshots with readable text",
            "colors": "neutral, soft gradients, subtle lighting, professional",
        }
    }


def collect_images(root: ET.Element) -> list[dict]:
    """
    Finds every <image src="..." alt="..."/> and returns list with section info.
    """
    items = []
    for img in root.findall(".//image"):
        src = img.attrib.get("src", "").strip()
        alt = img.attrib.get("alt", "").strip()

        # Identify a "section" label: parent tag (hero/problem/solution/etc)
        # ElementTree doesn't provide parent pointers, so we infer by scanning known sections.
        # We'll do a best-effort mapping by checking if this img appears under certain paths.
        section = "section"
        # crude but effective:
        if root.find("./hero//image[@src='%s']" % src) is not None:
            section = "hero"
        elif root.find("./problem//image[@src='%s']" % src) is not None:
            section = "problem"
        elif root.find("./solution//image[@src='%s']" % src) is not None:
            section = "solution"
        elif root.find("./keyFeatures//image[@src='%s']" % src) is not None:
            section = "features"
        elif root.find("./targetAudience//image[@src='%s']" % src) is not None:
            section = "audience"
        elif root.find("./useCases//image[@src='%s']" % src) is not None:
            section = "usecases"
        elif root.find("./benefits//image[@src='%s']" % src) is not None:
            section = "benefits"
        elif root.find("./integrations//image[@src='%s']" % src) is not None:
            section = "integrations"
        elif root.find("./trust//image[@src='%s']" % src) is not None:
            section = "trust"
        elif root.find("./finalCTA//image[@src='%s']" % src) is not None:
            section = "cta"
        elif root.find("./faq//image[@src='%s']" % src) is not None:
            section = "faq"

        items.append({
            "element": img,
            "src": src,
            "alt": alt,
            "section": section,
        })
    return items


def ask_ollama_for_prompts(context: dict, images: list[dict]) -> list[dict]:
    """
    Ollama returns one prompt per image, tailored to section + alt + product context.
    """
    system = (
        "Eres un generador de prompts para Stable Diffusion (fotografía/3D render). "
        "Debes devolver SOLO JSON válido. "
        "Objetivo: generar imágenes tipo marketing SaaS educativo estilo Apple-like: minimal, premium, sin texto, sin logos. "
        "Evita: palabras, letras, marcas de agua, UI con texto legible. "
        "Usa escenas y metáforas visuales: orden, claridad, coordinación, educación moderna."
    )

    # Build a request list
    req = []
    for i, it in enumerate(images, 1):
        req.append({
            "id": i,
            "section": it["section"],
            "alt": it["alt"] or "",
            "original_src": it["src"] or ""
        })

    user = (
        "Contexto del producto:\n"
        f"{json.dumps(context, ensure_ascii=False, indent=2)}\n\n"
        "Necesito prompts para Stable Diffusion (inglés) para cada imagen. "
        "Devuelve JSON con la forma:\n"
        "{\n"
        '  "images": [\n'
        '    {"id": 1, "prompt": "...", "negative_prompt": "..."},\n'
        "    ...\n"
        "  ]\n"
        "}\n\n"
        "Lista de imágenes:\n"
        f"{json.dumps(req, ensure_ascii=False, indent=2)}\n\n"
        "Reglas:\n"
        "- Prompt en inglés.\n"
        "- Negative prompt fuerte contra texto/logos/watermarks.\n"
        "- Mantén coherencia estética entre todas.\n"
        "- Cada sección debe tener una metáfora visual distinta.\n"
    )

    data = ollama_generate_json(system=system, user=user)
    out = data.get("images", [])
    # Ensure mapping by id
    by_id = {x.get("id"): x for x in out if isinstance(x, dict)}
    results = []
    for i in range(1, len(images) + 1):
        x = by_id.get(i, {})
        prompt = (x.get("prompt") or "").strip()
        neg = (x.get("negative_prompt") or "").strip()
        if not prompt:
            # fallback prompt
            prompt = "clean minimal premium SaaS education concept, modern office, soft light, cinematic, ultra detailed, 35mm photo"
        if not neg:
            neg = "text, letters, words, watermark, logo, brand, low quality, blurry, jpeg artifacts"
        results.append({"id": i, "prompt": prompt, "negative_prompt": neg})
    return results


def load_pipeline():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32

    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
        safety_checker=None,  # optional
    )
    pipe = pipe.to(device)

    # Small speed/memory tweaks
    if device == "cuda":
        try:
            pipe.enable_attention_slicing()
        except Exception:
            pass

    return pipe, device


def generate_images(pipe, images: list[dict], prompts: list[dict], out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    # Pair by index
    for idx, (img_info, pr) in enumerate(zip(images, prompts), start=1):
        section = img_info["section"]
        alt = img_info["alt"] or f"image-{idx}"
        filename = safe_filename_from_alt(section, alt, ext=".png")
        out_path = out_dir / filename

        # If already exists, skip (idempotent)
        if out_path.exists():
            print(f"[{idx}/{len(images)}] SKIP exists: {out_path.name}")
        else:
            prompt = pr["prompt"]
            negative_prompt = pr["negative_prompt"]

            # deterministic-ish seed per image
            seed = SEED_BASE + idx
            g = torch.Generator(device=pipe.device.type).manual_seed(seed)

            print(f"[{idx}/{len(images)}] GEN {out_path.name}")
            # Generate
            result = pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=STEPS,
                guidance_scale=GUIDANCE,
                height=HEIGHT,
                width=WIDTH,
                generator=g,
            )
            image = result.images[0]
            image.save(out_path)

        # Update XML src to local relative path
        img_info["element"].set("src", str(Path(OUTPUT_DIR) / filename))


def main():
    xml_path = Path(XML_FILE)
    if not xml_path.exists():
        raise FileNotFoundError(f"Missing {XML_FILE} in current folder: {Path.cwd()}")

    # Parse XML
    tree = ET.parse(str(xml_path))
    root = tree.getroot()

    # Build context
    context = build_context_from_xml(root)

    # Collect images in XML
    images = collect_images(root)
    if not images:
        print("No <image .../> nodes found in XML. Nothing to do.")
        return

    print(f"Found {len(images)} images in XML.")
    print("Asking Ollama for prompts...")
    prompts = ask_ollama_for_prompts(context, images)

    # Load stable diffusion pipeline once
    print("Loading Stable Diffusion pipeline (once)...")
    pipe, device = load_pipeline()
    print(f"Device: {device}")

    # Generate images + update xml
    out_dir = Path(OUTPUT_DIR)
    generate_images(pipe, images, prompts, out_dir)

    # Write updated XML
    out_xml = Path(UPDATED_XML_FILE)
    tree.write(str(out_xml), encoding="utf-8", xml_declaration=True)
    print(f"Updated XML saved as: {out_xml}")
    print("Done.")


if __name__ == "__main__":
    main()

