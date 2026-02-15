#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def main():
    base_dir = os.getcwd()
    target_name = "201-Criterios de evaluación"
    new_file = "Criterios de evaluación.md"

    for root, dirs, files in os.walk(base_dir):
        # Check if the current folder is named "201-Criterios de evaluación"
        if os.path.basename(root) == target_name:
            # Check if folder is empty (no files, no subdirs)
            if not dirs and not files:
                file_path = os.path.join(root, new_file)
                if not os.path.exists(file_path):
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write("")  # create empty file
                    print(f"Created: {file_path}")
                else:
                    print(f"File already exists: {file_path}")

if __name__ == "__main__":
    main()

