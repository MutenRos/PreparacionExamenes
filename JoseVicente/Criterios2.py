#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

EXCLUDE_DIRS = {'.git', '__pycache__', '.venv', 'venv', '.idea', '.vscode'}
TARGET_FILENAME = "Criterios de evaluacion.md"

def depth_from_base(path: str, base: str) -> int:
    rel = os.path.relpath(path, base)
    if rel == ".":
        return 0
    return len(rel.split(os.sep))

def main():
    base_dir = os.getcwd()

    for root, dirs, files in os.walk(base_dir):
        # excluir directorios no deseados del recorrido
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        # calcular nivel (0=base, 1=curso, 2=asignatura, 3=unidad didáctica, 4=subunidad, ...)
        level = depth_from_base(root, base_dir)

        # solo actuar en nivel 3 (unidad didáctica)
        if level == 3:
            target_path = os.path.join(root, TARGET_FILENAME)
            if not os.path.exists(target_path):
                # crea vacío (o añade una cabecera si prefieres)
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write("")  # dejar vacío
                print(f"Creado: {target_path}")
            else:
                print(f"Ya existe: {target_path}")

if __name__ == "__main__":
    main()

