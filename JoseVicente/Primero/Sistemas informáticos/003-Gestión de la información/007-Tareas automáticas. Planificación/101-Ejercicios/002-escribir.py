#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

# Directory where this Python file is located
BASE_DIR = Path(__file__).resolve().parent

# archivo.txt in the same directory
FILE_PATH = BASE_DIR / "archivo.txt"

with FILE_PATH.open("a", encoding="utf-8") as archivo:
    archivo.write("Hola que tal\n")

