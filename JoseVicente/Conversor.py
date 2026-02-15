#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convierte repositorios con "Contenidos básicos.md" suelto al nuevo formato:

Para cada carpeta del proyecto:
- Si existe un archivo "Contenidos básicos.md" directamente dentro de la carpeta,
  y el nombre de la carpeta NO es "001-Contenidos básicos",
  entonces:
    1) crear (si no existe) la subcarpeta "001-Contenidos básicos"
    2) mover "Contenidos básicos.md" dentro de esa subcarpeta
- Si el destino ya contiene un archivo con el mismo nombre, NO se sobreescribe (se omite).
- Se respetan EXCLUDE_DIRS.
"""

import os
import shutil
from pathlib import Path
from typing import Iterable

# Mismos nombres que el generador
OUTPUT_SUBFOLDER = "001-Contenidos básicos"
OUTPUT_FILENAME = "Contenidos básicos.md"

# Directorios a excluir en cualquier nivel
EXCLUDE_DIRS = {
    ".git",
    # añade aquí "node_modules", ".venv", "dist", "build", "moodledata", etc.
}


def is_excluded_dir(name: str) -> bool:
    return name in EXCLUDE_DIRS


def iter_all_dirs(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, _filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not is_excluded_dir(d)]
        yield Path(dirpath)


def main():
    base = Path(__file__).resolve().parent
    moved = 0
    skipped = 0

    for folder in iter_all_dirs(base):
        # No actuar dentro de la propia carpeta de salida
        if folder.name == OUTPUT_SUBFOLDER:
            continue

        src_file = folder / OUTPUT_FILENAME
        if not src_file.exists() or not src_file.is_file():
            continue

        # Si ya está en el nuevo formato (archivo dentro de 001-Contenidos básicos), no hacer nada
        # (Eso ocurriría cuando el 'folder' sea la subcarpeta contenedora)
        if folder.name == OUTPUT_SUBFOLDER:
            continue

        dest_dir = folder / OUTPUT_SUBFOLDER
        dest_file = dest_dir / OUTPUT_FILENAME

        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"[!] No se pudo crear {dest_dir}: {e}")
            skipped += 1
            continue

        if dest_file.exists():
            print(f"[→] Ya existe destino; omito mover: {dest_file}")
            skipped += 1
            continue

        try:
            shutil.move(str(src_file), str(dest_file))
            print(f"[✓] Movido: {src_file}  ->  {dest_file}")
            moved += 1
        except Exception as e:
            print(f"[!] No se pudo mover {src_file} -> {dest_file}: {e}")
            skipped += 1

    print(f"\nHecho. Movidos: {moved}  |  Omitidos: {skipped}")


if __name__ == "__main__":
    main()

