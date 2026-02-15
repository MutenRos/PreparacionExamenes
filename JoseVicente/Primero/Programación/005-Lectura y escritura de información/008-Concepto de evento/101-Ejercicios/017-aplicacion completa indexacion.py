#!/usr/bin/env python3
import os
import sqlite3
from datetime import datetime
import tkinter as tk

# ttkbootstrap para mejorar el aspecto
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox, filedialog

DB_NAME = "discos.db"

# -------------------- utilidades --------------------
def asegurar_bd():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS archivos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disco TEXT,
            ruta  TEXT,
            archivo TEXT,
            tamanio INTEGER,
            creacion TEXT,
            modificacion TEXT
        )
    """)
    # Índices útiles para acelerar búsquedas
    cur.execute("CREATE INDEX IF NOT EXISTS idx_archivos_archivo ON archivos(archivo)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_archivos_ruta ON archivos(ruta)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_archivos_disco ON archivos(disco)")
    conn.commit()
    conn.close()

def formato_tam(bytes_):
    try:
        bytes_ = int(bytes_)
    except:
        return str(bytes_)
    for unidad in ("B","KB","MB","GB","TB"):
        if bytes_ < 1024:
            return f"{bytes_:.0f} {unidad}" if unidad=="B" else f"{bytes_:.2f} {unidad}"
        bytes_ /= 1024
    return f"{bytes_:.2f} PB"

# -------------------- app --------------------
def main():
    asegurar_bd()

    # Ventana con tema (elige: flatly, darkly, lumen, vapor, etc.)
    root = tb.Window(themename="flatly")
    root.title("Indexador y Buscador de Archivos (SQLite + ttkbootstrap)")
    root.geometry("1100x650")

    # PanedWindow para dividir 50/50
    paned = ttk.PanedWindow(root, orient=HORIZONTAL)
    paned.pack(fill=BOTH, expand=True, padx=8, pady=8)

    # Frames izquierdo y derecho
    left = ttk.Frame(paned, padding=16)
    right = ttk.Frame(paned, padding=16)
    paned.add(left, weight=1)
    paned.add(right, weight=1)

    # -------------------- LADO IZQUIERDO (indexación) --------------------
    ttk.Label(left, text="Indica la carpeta a indexar", font=("Ubuntu", 11, "bold")).pack(anchor="w")

    carpeta_frame = ttk.Frame(left)
    carpeta_frame.pack(fill=X, pady=6)
    carpeta_var = tk.StringVar()
    carpeta_entry = ttk.Entry(carpeta_frame, textvariable=carpeta_var)
    carpeta_entry.pack(side=LEFT, fill=X, expand=True)
    def elegir_carpeta():
        path = filedialog.askdirectory()
        if path:
            carpeta_var.set(path)
    ttk.Button(carpeta_frame, text="Elegir…", command=elegir_carpeta, bootstyle=SECONDARY).pack(side=LEFT, padx=6)

    ttk.Label(left, text="Indica el nombre del disco", font=("Ubuntu", 11, "bold")).pack(anchor="w", pady=(10,0))
    disco_var = tk.StringVar()
    ttk.Entry(left, textvariable=disco_var).pack(fill=X, pady=6)

    estado_var = tk.StringVar(value="Listo.")
    barra = ttk.Label(left, textvariable=estado_var, bootstyle=INFO)
    barra.pack(fill=X, pady=(8,0))

    def procesar():
        carpeta_inicial = carpeta_var.get().strip()
        nombre_disco = disco_var.get().strip()

        if not carpeta_inicial or not os.path.isdir(carpeta_inicial) or not nombre_disco:
            messagebox.showwarning("Datos inválidos", "Carpeta o disco no válidos")
            return

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        total = 0
        saltados = 0
        estado_var.set("Indexando… esto puede tardar según la cantidad de archivos.")
        root.update_idletasks()

        for raiz, subdirs, archivos in os.walk(carpeta_inicial):
            for arch in archivos:
                ruta_completa = os.path.join(raiz, arch)
                try:
                    tamanio = os.path.getsize(ruta_completa)
                    creacion = datetime.fromtimestamp(os.path.getctime(ruta_completa)).isoformat(timespec="seconds")
                    modificacion = datetime.fromtimestamp(os.path.getmtime(ruta_completa)).isoformat(timespec="seconds")
                    cur.execute(
                        "INSERT INTO archivos (disco, ruta, archivo, tamanio, creacion, modificacion) VALUES (?,?,?,?,?,?)",
                        (nombre_disco, raiz, arch, int(tamanio), creacion, modificacion)
                    )
                    total += 1
                    if total % 1000 == 0:
                        conn.commit()
                        estado_var.set(f"Indexados {total:,}…")
                        root.update_idletasks()
                except Exception:
                    saltados += 1
                    continue

        conn.commit()
        conn.close()
        estado_var.set(f"Proceso completado. Indexados: {total:,}. Saltados: {saltados:,}.")
        messagebox.showinfo("Completado", f"Indexación finalizada.\nIndexados: {total:,}\nSaltados: {saltados:,}")

    ttk.Button(left, text="Procesar", command=procesar, bootstyle=SUCCESS).pack(pady=16, fill=X)

    # Separador estético
    ttk.Separator(left, orient=HORIZONTAL).pack(fill=X, pady=8)
    ttk.Label(left, text="Consejo: puedes indexar varios discos; luego búscalos por su nombre.",
              wraplength=420, bootstyle=SECONDARY).pack(anchor="w")

    # -------------------- LADO DERECHO (búsqueda + Treeview) --------------------
    top_right = ttk.Frame(right)
    top_right.pack(fill=X)

    ttk.Label(top_right, text="Buscar en SQLite", font=("Ubuntu", 11, "bold")).pack(anchor="w")

    search_row = ttk.Frame(top_right)
    search_row.pack(fill=X, pady=6)

    query_var = tk.StringVar()
    entry_buscar = ttk.Entry(search_row, textvariable=query_var)
    entry_buscar.pack(side=LEFT, fill=X, expand=True)

    def ejecutar_busqueda(event=None):
        q = query_var.get().strip()
        llenar_tree(q)

    ttk.Button(search_row, text="Buscar", command=ejecutar_busqueda, bootstyle=PRIMARY).pack(side=LEFT, padx=6)
    entry_buscar.bind("<Return>", ejecutar_busqueda)

    # Tree + Scrollbar
    cols = ("disco", "ruta", "archivo", "tamanio", "creacion", "modificacion")
    tree_frame = ttk.Frame(right)
    tree_frame.pack(fill=BOTH, expand=True, pady=(8,0))

    tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=18)
    vsb = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
    hsb = ttk.Scrollbar(tree_frame, orient=HORIZONTAL, command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    tree_frame.rowconfigure(0, weight=1)
    tree_frame.columnconfigure(0, weight=1)

    # Encabezados y anchos
    tree.heading("disco", text="Disco")
    tree.heading("ruta", text="Ruta")
    tree.heading("archivo", text="Archivo")
    tree.heading("tamanio", text="Tamaño")
    tree.heading("creacion", text="Creación")
    tree.heading("modificacion", text="Modificación")

    tree.column("disco", width=100, anchor=W)
    tree.column("ruta", width=280, anchor=W)
    tree.column("archivo", width=220, anchor=W)
    tree.column("tamanio", width=100, anchor=E)
    tree.column("creacion", width=150, anchor=W)
    tree.column("modificacion", width=150, anchor=W)

    # estado derecha
    estado_busq = tk.StringVar(value="Sin resultados aún.")
    ttk.Label(right, textvariable=estado_busq, bootstyle=INFO).pack(fill=X, pady=(6,0))

    def limpiar_tree():
        for i in tree.get_children():
            tree.delete(i)

    def llenar_tree(q):
        limpiar_tree()
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        if q:
            like = f"%{q}%"
            cur.execute(
                """
                SELECT disco, ruta, archivo, CAST(tamanio AS INTEGER) AS tamanio, creacion, modificacion
                FROM archivos
                WHERE archivo LIKE ? OR ruta LIKE ? OR disco LIKE ?
                ORDER BY rowid DESC
                LIMIT 1000
                """,
                (like, like, like)
            )
        else:
            cur.execute(
                """
                SELECT disco, ruta, archivo, CAST(tamanio AS INTEGER) AS tamanio, creacion, modificacion
                FROM archivos
                ORDER BY rowid DESC
                LIMIT 1000
                """
            )

        filas = cur.fetchall()
        conn.close()

        for d, r, a, t, c, m in filas:
            tree.insert("", "end", values=(d, r, a, formato_tam(t), c, m))

        if q:
            estado_busq.set(f"{len(filas)} resultados para «{q}» (máx 1000).")
        else:
            estado_busq.set(f"Mostrando {len(filas)} últimos registros (máx 1000).")


    # Doble clic: copiar ruta completa al portapapeles (útil)
    def on_double_click(event):
        item = tree.selection()
        if not item:
            return
        vals = tree.item(item[0], "values")
        # vals: (disco, ruta, archivo, tamanio, creacion, modificacion)
        ruta_completa = os.path.join(vals[1], vals[2])
        root.clipboard_clear()
        root.clipboard_append(ruta_completa)
        messagebox.showinfo("Ruta copiada", ruta_completa)

    tree.bind("<Double-1>", on_double_click)

    # Carga inicial
    llenar_tree("")

    root.mainloop()

if __name__ == "__main__":
    main()

