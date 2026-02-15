import os

carpeta = "/var/www/html/dam2526/Primero/Programación"

def print_tree(path, indent=""):
    # Listar contenido de la carpeta
    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        print(indent + "🚫 [sin permiso]")
        return

    for i, item in enumerate(items):
        full_path = os.path.join(path, item)
        is_last = (i == len(items) - 1)

        # Seleccionar el conector según si es el último elemento
        connector = "└── " if is_last else "├── "

        if os.path.isdir(full_path):
            print(indent + connector + f"📁 {item}")
            new_indent = indent + ("    " if is_last else "│   ")
            print_tree(full_path, new_indent)
        else:
            print(indent + connector + f"📄 {item}")

print(f"📁 {os.path.basename(carpeta) or carpeta}")
print_tree(carpeta)

