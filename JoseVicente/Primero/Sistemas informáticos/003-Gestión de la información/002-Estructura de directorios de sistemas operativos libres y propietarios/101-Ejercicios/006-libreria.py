#!/usr/bin/env python3
import os
import sys

def format_size(size_bytes: int) -> str:
    """Devuelve el tamaño con la unidad más conveniente."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{size:.0f} {unit}"
            else:
                return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size_bytes} B"

def folder_info(path: str, prefix: str = ""):
    """
    Recorre recursivamente la carpeta `path`.
    Devuelve: (total_size_en_bytes, lista_de_lineas_para_esta_carpeta)
    """
    lines = []
    total_size = 0

    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        # Si no hay permisos, lo indicamos y seguimos
        lines.append(f"{prefix}└── ⚠️ [Permiso denegado]")
        return 0, lines

    for index, name in enumerate(entries):
        full_path = os.path.join(path, name)
        is_last = (index == len(entries) - 1)
        connector = "└── " if is_last else "├── "

        if os.path.isdir(full_path):
            # Prefijo para los hijos de esta carpeta
            child_prefix = prefix + ("    " if is_last else "│   ")
            dir_size, sub_lines = folder_info(full_path, child_prefix)
            lines.append(f"{prefix}{connector}📁 {name} ({format_size(dir_size)})")
            lines.extend(sub_lines)
            total_size += dir_size
        else:
            try:
                file_size = os.path.getsize(full_path)
            except OSError:
                file_size = 0
            lines.append(f"{prefix}{connector}📄 {name} ({format_size(file_size)})")
            total_size += file_size

    return total_size, lines

def build_tree(root_path: str) -> str:
    """Construye el árbol completo como un string."""
    root_path = os.path.abspath(root_path)
    root_name = os.path.basename(root_path.rstrip(os.sep)) or root_path
    total_size, lines = folder_info(root_path, "")
    tree_lines = [f"📁 {root_name} ({format_size(total_size)})"]
    tree_lines.extend(lines)
    return "\n".join(tree_lines)

def main():
    # Uso: script.py INPUT_FOLDER [OUTPUT_FILE]
    if len(sys.argv) < 2:
        print(f"Uso: {os.path.basename(sys.argv[0])} CARPETA_ENTRADA [FICHERO_SALIDA]")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) >= 3 else None

    if not os.path.isdir(input_folder):
        print(f"Error: '{input_folder}' no es una carpeta válida.")
        sys.exit(1)

    tree_str = build_tree(input_folder)

    if output_file:
        # Guardar en fichero
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(tree_str + "\n")
        except OSError as e:
            print(f"Error al escribir en '{output_file}': {e}")
            sys.exit(1)
    else:
        # Mostrar por pantalla
        print(tree_str)

if __name__ == "__main__":
    main()

