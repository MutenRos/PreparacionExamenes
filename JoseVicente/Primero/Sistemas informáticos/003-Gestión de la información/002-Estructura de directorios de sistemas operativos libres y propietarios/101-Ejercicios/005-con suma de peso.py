# -*- coding: utf-8 -*-
import os

carpeta = "/var/www/html/dam2526/Primero/Programación"

def format_size(num_bytes: int) -> str:
    """Return a human-readable size (B, KB, MB, GB)."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024.0

def get_dir_size(path: str) -> int:
    """Return total size (in bytes) of all files under a directory."""
    total = 0
    try:
        with os.scandir(path) as it:
            for entry in it:
                try:
                    if entry.is_file(follow_symlinks=False):
                        total += entry.stat(follow_symlinks=False).st_size
                    elif entry.is_dir(follow_symlinks=False):
                        total += get_dir_size(entry.path)
                except (PermissionError, FileNotFoundError):
                    # Skip entries we can't stat
                    continue
    except (PermissionError, FileNotFoundError):
        pass
    return total

def print_tree(path: str, prefix: str = ""):
    """
    Print the tree of 'path' using 'prefix' for indentation.
    Directories first, then files, with proper ├── / └── and │.
    """
    try:
        entries = list(os.scandir(path))
    except (PermissionError, FileNotFoundError):
        return

    # Sort: directories first, then files, both alphabetically
    entries.sort(key=lambda e: (not e.is_dir(follow_symlinks=False), e.name.lower()))

    count = len(entries)
    for index, entry in enumerate(entries):
        is_last = (index == count - 1)
        connector = "└── " if is_last else "├── "

        if entry.is_dir(follow_symlinks=False):
            dir_size_bytes = get_dir_size(entry.path)
            dir_size_str = format_size(dir_size_bytes)
            print(f"{prefix}{connector}📁 {entry.name} ({dir_size_str})")
            # For children, extend prefix:
            # if this is the last child, no vertical bar for further siblings
            child_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(entry.path, child_prefix)
        else:
            try:
                size_bytes = entry.stat(follow_symlinks=False).st_size
            except (PermissionError, FileNotFoundError):
                size_bytes = 0
            size_str = format_size(size_bytes)
            print(f"{prefix}{connector}📄 {entry.name} ({size_str})")

if __name__ == "__main__":
    root_size = format_size(get_dir_size(carpeta))
    root_name = os.path.basename(carpeta.rstrip("/")) or carpeta
    print(f"📁 {root_name} ({root_size})")
    print_tree(carpeta)

