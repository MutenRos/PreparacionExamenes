#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_articulos_blog.py

Genera artículos para el blog a partir de archivos Markdown en ./documentos,
usando Ollama local (modelo: qwen2.5:7b-instruct-q4_0) y guardándolos en SQLite.

CAMBIO SOLICITADO (categorías):
Para cada heading nivel 3 (### ...), la categoría del post será:

  "<nombre_del_archivo_sin_extension>, <heading_nivel_1_actual>, <heading_nivel_2_actual>"

Ejemplo:
"Backpropagation explicado visualmente, El problema que resuelve backpropagation, Ajustar miles o millones de parámetros"

Reglas:
- Por cada .md en ./documentos:
  - Usar TODO el documento como contexto.
  - Por cada ### (nivel 3):
    - title = heading nivel 3 sin numeración ("Lección 1.1.1 — ..." -> "...")
    - category = "Archivo, H1, H2" (según contexto donde aparece ese ###)
    - content = artículo en Markdown generado por Ollama.

- Inserta solo si no existe ya un post con el mismo (title, category).
- Guarda Markdown en posts.content (blog.php lo renderiza a HTML).

Requisitos:
- Ollama corriendo en localhost:11434
- requests: pip install requests
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests

# Logging configurado con formato legible
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# =========================
# CONFIG
# =========================
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct-q4_0")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")

SCRIPT_DIR = Path(__file__).resolve().parent
DOCS_DIR = SCRIPT_DIR / "documentos"
DB_PATH = SCRIPT_DIR / "blog.sqlite"

REQUEST_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "240"))
RETRIES = 3
SLEEP_BETWEEN_CALLS = 0.6

CACHE_DIR = SCRIPT_DIR / ".cache_articulos"
CACHE_DIR.mkdir(exist_ok=True)


# =========================
# DATA STRUCTURES
# =========================
@dataclass
class H3Item:
    file_stem: str
    h1: str
    h2: str
    h3_raw: str
    h3_title: str
    category: str


# =========================
# HELPERS
# =========================
def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def normalize_newlines(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def ensure_db(db_path: Path) -> None:
    conn = sqlite3.connect(str(db_path))
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              date TEXT NOT NULL,
              title TEXT NOT NULL,
              content TEXT NOT NULL,
              category TEXT NOT NULL
            );
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_posts_date ON posts(date DESC);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_posts_category ON posts(category);")
        conn.commit()
    finally:
        conn.close()


def post_exists(conn: sqlite3.Connection, title: str, category: str) -> bool:
    cur = conn.execute(
        "SELECT 1 FROM posts WHERE title = ? AND category = ? LIMIT 1",
        (title, category),
    )
    return cur.fetchone() is not None


def insert_post(conn: sqlite3.Connection, title: str, content_md: str, category: str) -> None:
    conn.execute(
        "INSERT INTO posts(date, title, content, category) VALUES(?, ?, ?, ?)",
        (now_iso(), title, content_md, category),
    )
    conn.commit()


def cache_key(file_path: Path, title: str, category: str) -> Path:
    base = f"{file_path.name}__{title}__{category}"
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "_", base)[:180]
    return CACHE_DIR / f"{safe}.json"


def strip_numbering_from_h3(title: str) -> str:
    """
    "Lección 1.1.1 — Por qué ajustar pesos es difícil" -> "Por qué ajustar pesos es difícil"
    """
    t = title.strip()

    # Quitar prefijos tipo "Lección", "Leccion", "Lesson", "Tema", etc.
    t = re.sub(r"^(lecci[oó]n|lesson|tema|cap[ií]tulo|unidad)\s*", "", t, flags=re.IGNORECASE)

    # Quitar numeración inicial "1.2.3", "1)", "1.2 —", etc.
    t = re.sub(r"^\s*\d+(?:[\.\-]\d+){0,6}\s*[\)\.\-–—:]*\s*", "", t)

    # Quitar separadores iniciales
    t = re.sub(r"^\s*[–—-]\s*", "", t)

    # Normalizar espacios
    t = re.sub(r"\s{2,}", " ", t).strip()
    return t if t else title.strip()


def extract_front_matter(md: str) -> Tuple[Dict[str, str], str]:
    md = normalize_newlines(md)
    if not md.startswith("---\n"):
        return {}, md

    parts = md.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, md

    fm_block = parts[0].splitlines()[1:]
    body = parts[1]

    fm: Dict[str, str] = {}
    for line in fm_block:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)\s*$", line)
        if m:
            k = m.group(1).strip()
            v = m.group(2).strip().strip('"').strip("'")
            fm[k] = v

    return fm, body


def extract_hierarchy_items(md_body: str, file_stem: str) -> List[H3Item]:
    """
    Recorre el documento en orden y para cada ### captura el H1 y H2 más recientes.
    """
    h1_current = ""
    h2_current = ""
    items: List[H3Item] = []

    for line in normalize_newlines(md_body).splitlines():
        m1 = re.match(r"^\s*#\s+(.+?)\s*$", line)
        if m1:
            h1_current = m1.group(1).strip()
            h2_current = ""  # al cambiar H1, reinicia H2
            continue

        m2 = re.match(r"^\s*##\s+(.+?)\s*$", line)
        if m2:
            h2_current = m2.group(1).strip()
            continue

        m3 = re.match(r"^\s*###\s+(.+?)\s*$", line)
        if m3:
            raw_h3 = m3.group(1).strip()
            title = strip_numbering_from_h3(raw_h3)

            # Si no hay H1/H2 en ese punto, pon placeholders (evita categoría vacía)
            h1 = h1_current.strip() if h1_current.strip() else "Sin sección principal"
            h2 = h2_current.strip() if h2_current.strip() else "Sin subsección"

            category = f"{file_stem}, {h1}, {h2}"

            items.append(
                H3Item(
                    file_stem=file_stem,
                    h1=h1,
                    h2=h2,
                    h3_raw=raw_h3,
                    h3_title=title,
                    category=category,
                )
            )

    return items


def ollama_generate(prompt: str) -> str:
    """Llama a Ollama y devuelve el texto generado, con reintentos."""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_ctx": 8192,
        },
    }

    last_err: Optional[Exception] = None
    for attempt in range(1, RETRIES + 1):
        try:
            r = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
            data = r.json()
            text = data.get("response", "")
            if not isinstance(text, str) or not text.strip():
                raise RuntimeError("Respuesta vacía de Ollama.")
            return text.strip()
        except requests.ConnectionError:
            log.warning("Ollama no disponible (intento %d/%d)", attempt, RETRIES)
            last_err = ConnectionError("No se pudo conectar a Ollama")
        except requests.Timeout:
            log.warning("Timeout en Ollama (intento %d/%d)", attempt, RETRIES)
            last_err = TimeoutError(f"Timeout tras {REQUEST_TIMEOUT}s")
        except Exception as e:
            log.warning("Error en Ollama (intento %d/%d): %s", attempt, RETRIES, e)
            last_err = e
        time.sleep(1.5 * attempt)

    raise RuntimeError(f"Fallo llamando a Ollama tras {RETRIES} intentos: {last_err}")


def build_prompt(full_doc: str, category: str, article_title: str) -> str:
    return f"""Eres un redactor técnico experto en IA aplicada a programación.
Escribe en español, con un tono claro y práctico para programadores.

CONTEXTO (documento completo, úsalo para alinear terminología y enfoque):
\"\"\"{full_doc}\"\"\"

METADATOS:
- Categoría del artículo (contexto): {category}
- Título del artículo: "{article_title}"

TAREA:
Escribe un artículo de blog en formato Markdown sobre el título indicado.
Longitud objetivo: 900 a 1400 palabras.

Estructura mínima:
1) Introducción (por qué importa)
2) Explicación principal con ejemplos (incluye 1 bloque de código corto si ayuda)
3) Errores típicos / trampas (al menos 3)
4) Checklist accionable (5-10 puntos)
5) Cierre con "Siguientes pasos" (2-4 bullets)

REGLAS:
- NO incluyas front-matter YAML.
- NO incluyas enlaces inventados.
- Devuelve SOLO el Markdown del artículo.
"""


# =========================
# MAIN
# =========================
def parse_args() -> argparse.Namespace:
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Genera artículos de blog desde Markdown usando Ollama."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Solo muestra qué artículos se generarían, sin llamar a Ollama.",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Activa logging de nivel DEBUG.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not DOCS_DIR.is_dir():
        raise SystemExit(f"ERROR: No existe la carpeta: {DOCS_DIR}")

    ensure_db(DB_PATH)

    md_files = sorted([p for p in DOCS_DIR.glob("*.md") if p.is_file()])
    if not md_files:
        log.info("No se encontraron .md en %s", DOCS_DIR)
        return

    log.info("Encontrados %d archivos en %s", len(md_files), DOCS_DIR)
    log.info("DB: %s | Modelo: %s", DB_PATH, MODEL)
    if args.dry_run:
        log.info(">>> MODO DRY-RUN: no se generará ni insertará nada <<<")
    print("-" * 70)

    t_start = time.monotonic()
    conn = sqlite3.connect(str(DB_PATH))
    try:
        inserted = 0
        skipped = 0
        from_cache = 0
        errors = 0

        for file_idx, md_path in enumerate(md_files, 1):
            raw = read_text(md_path)
            _fm, body = extract_front_matter(raw)

            file_stem = md_path.stem.strip() or md_path.name

            items = extract_hierarchy_items(body, file_stem=file_stem)
            if not items:
                log.debug("[SKIP] %s: no hay headings ###", md_path.name)
                continue

            log.info(
                "[%d/%d] %s — %d artículos posibles",
                file_idx, len(md_files), md_path.name, len(items),
            )

            full_doc_for_context = raw.strip()

            for it in items:
                title = it.h3_title
                category = it.category

                if post_exists(conn, title, category):
                    skipped += 1
                    log.debug("  (skip) Ya existe: [%s] %s", category, title)
                    continue

                if args.dry_run:
                    log.info("  [DRY] Generaría: [%s] %s", category, title)
                    continue

                ck = cache_key(md_path, title, category)
                if ck.is_file():
                    try:
                        cached = json.loads(ck.read_text(encoding="utf-8"))
                        content_md = (cached.get("content") or "").strip()
                        if content_md:
                            insert_post(conn, title, content_md, category)
                            from_cache += 1
                            inserted += 1
                            log.info("  (cache→db) %s", title)
                            continue
                    except (json.JSONDecodeError, KeyError) as exc:
                        log.warning("  Cache corrupta para %s: %s", title, exc)

                log.info("  (gen) %s", title)
                try:
                    prompt = build_prompt(full_doc_for_context, category, title)
                    content_md = ollama_generate(prompt)
                except RuntimeError as exc:
                    log.error("  ERROR generando '%s': %s", title, exc)
                    errors += 1
                    continue

                if len(content_md.strip()) < 200:
                    log.warning("  Contenido demasiado corto para: %s (%d chars)", title, len(content_md))
                    errors += 1
                    continue

                ck.write_text(
                    json.dumps(
                        {
                            "source_file": md_path.name,
                            "category": category,
                            "title": title,
                            "generated_at": now_iso(),
                            "model": MODEL,
                            "content": content_md,
                            "hierarchy": {"h1": it.h1, "h2": it.h2, "h3_raw": it.h3_raw},
                        },
                        ensure_ascii=False,
                        indent=2,
                    ),
                    encoding="utf-8",
                )

                insert_post(conn, title, content_md, category)
                inserted += 1
                time.sleep(SLEEP_BETWEEN_CALLS)

        elapsed = time.monotonic() - t_start
        print("\n" + "=" * 70)
        log.info("Insertados: %d  (desde cache: %d)", inserted, from_cache)
        log.info("Saltados (ya existían): %d", skipped)
        log.info("Errores: %d", errors)
        log.info("Tiempo total: %.1f s", elapsed)
        log.info("Cache: %s", CACHE_DIR)
        print("=" * 70)

    finally:
        conn.close()


if __name__ == "__main__":
    main()

