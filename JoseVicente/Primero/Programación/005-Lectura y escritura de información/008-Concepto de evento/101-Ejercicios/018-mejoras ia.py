#!/usr/bin/env python3
import os
import sqlite3
from datetime import datetime
import tkinter as tk

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

    root = tb.Window(themename="flatly")
    root.title("Indexador y Buscador de Archivos (SQLite + ttkbootstrap)")
    root.geometry("1250x700")

    paned = ttk.PanedWindow(root, orient=HORIZONTAL)
    paned.pack(fill=BOTH, expand=True, padx=8, pady=8)

    left = ttk.Frame(paned, padding=16)
    right = ttk.Frame(paned, padding=16)
    paned.add(left, weight=1)
    paned.add(right, weight=2)

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
    ttk.Separator(left, orient=HORIZONTAL).pack(fill=X, pady=8)
    ttk.Label(left, text="Consejo: puedes indexar varios discos; luego búscalos por su nombre.",
              wraplength=420, bootstyle=SECONDARY).pack(anchor="w")

    # -------------------- LADO DERECHO (búsqueda + Treeview) --------------------
    ttk.Label(right, text="Buscar en SQLite", font=("Ubuntu", 11, "bold")).pack(anchor="w")

    # Estado búsqueda
    estado_busq = tk.StringVar(value="Sin resultados aún.")

    # --- Barra de filtros por columna (alineadas con el orden de columnas)
    filter_frame = ttk.Frame(right)
    filter_frame.pack(fill=X, pady=(8,4))

    # Definimos columnas (mismo orden en Treeview y filtros)
    cols = ("disco", "ruta", "archivo", "tamanio", "creacion", "modificacion")

    # Variables de filtro
    filtro_vars = {c: tk.StringVar() for c in cols}

    # grid headers (pequeño label sobre cada entry)
    labels = {
        "disco": "Disco",
        "ruta": "Ruta",
        "archivo": "Archivo",
        "tamanio": "Tamaño",
        "creacion": "Creación",
        "modificacion": "Modificación",
    }
    # creamos una cuadrícula con 6 columnas iguales
    for i, c in enumerate(cols):
        ttk.Label(filter_frame, text=labels[c]).grid(row=0, column=i, sticky="w", padx=4)
        ttk.Entry(filter_frame, textvariable=filtro_vars[c]).grid(row=1, column=i, sticky="ew", padx=4)
        filter_frame.columnconfigure(i, weight=1)

    # Botones Buscar/Limpiar a la derecha
    btns_frame = ttk.Frame(right)
    btns_frame.pack(fill=X, pady=(4,8))
    def limpiar_filtros():
        for v in filtro_vars.values():
            v.set("")
        llenar_tree()  # sin filtros

    def ejecutar_busqueda(event=None):
        llenar_tree()

    ttk.Button(btns_frame, text="Buscar", command=ejecutar_busqueda, bootstyle=PRIMARY).pack(side=RIGHT, padx=6)
    ttk.Button(btns_frame, text="Limpiar", command=limpiar_filtros, bootstyle=SECONDARY).pack(side=RIGHT)

    # --- Tree + Scrollbars
    tree_frame = ttk.Frame(right)
    tree_frame.pack(fill=BOTH, expand=True)

    tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=20)
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

    tree.column("disco", width=120, anchor=W)
    tree.column("ruta", width=360, anchor=W)
    tree.column("archivo", width=260, anchor=W)
    tree.column("tamanio", width=120, anchor=E)
    tree.column("creacion", width=160, anchor=W)
    tree.column("modificacion", width=160, anchor=W)

    # --- Estado visual
    ttk.Label(right, textvariable=estado_busq, bootstyle=INFO).pack(fill=X, pady=(6,0))

    # --- Ordenación por columnas (estado global)
    sort_col = tk.StringVar(value="rowid")   # por defecto
    sort_dir = tk.StringVar(value="DESC")    # DESC/ASC

    # Mapa de columnas Tree -> expresión SQL de ORDER BY
    # Para tamanio conviene cast numérico; fechas ISO ordenan bien lexicográficamente
    order_expr = {
        "disco": "disco",
        "ruta": "ruta",
        "archivo": "archivo",
        "tamanio": "CAST(tamanio AS INTEGER)",
        "creacion": "creacion",
        "modificacion": "modificacion",
        "rowid": "rowid"
    }

    # Asignar comando a cada encabezado
    def on_sort(col_clicked):
        current_col = sort_col.get()
        current_dir = sort_dir.get()
        if current_col == col_clicked:
            sort_dir.set("ASC" if current_dir == "DESC" else "DESC")
        else:
            sort_col.set(col_clicked)
            sort_dir.set("ASC")  # primera vez ascendente
        llenar_tree()

    for c in cols:
        tree.heading(c, text=labels[c], command=lambda cc=c: on_sort(cc))

    # --- utilidades tree
    def limpiar_tree():
        for i in tree.get_children():
            tree.delete(i)

    # Construye WHERE dinámico con LIKE para todos los filtros
    def construir_where_y_params():
        where = []
        params = []
        for c in cols:
            val = filtro_vars[c].get().strip()
            if val != "":
                where.append(f"{c} LIKE ?")
                params.append(f"%{val}%")
        where_clause = ("WHERE " + " AND ".join(where)) if where else ""
        return where_clause, params

    def llenar_tree():
        limpiar_tree()
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        where_clause, params = construir_where_y_params()
        order = order_expr.get(sort_col.get(), "rowid")
        direction = "ASC" if sort_dir.get() == "ASC" else "DESC"

        sql = f"""
            SELECT disco, ruta, archivo, tamanio, creacion, modificacion
            FROM archivos
            {where_clause}
            ORDER BY {order} {direction}
            LIMIT 1000
        """
        cur.execute(sql, params)
        filas = cur.fetchall()
        conn.close()

        for d, r, a, t, c, m in filas:
            tree.insert("", "end", values=(d, r, a, formato_tam(t), c, m))

        # Texto de estado
        filtros_activos = [f"{labels[c]}='{filtro_vars[c].get().strip()}'"
                           for c in cols if filtro_vars[c].get().strip() != ""]
        filtros_txt = " | ".join(filtros_activos) if filtros_activos else "sin filtros"
        estado_busq.set(
            f"{len(filas)} resultados ({filtros_txt}). Orden: {order} {direction}. Máx 1000."
        )

    # Doble clic: copiar ruta completa al portapapeles
    def on_double_click(event):
        item = tree.selection()
        if not item:
            return
        vals = tree.item(item[0], "values")
        ruta_completa = os.path.join(vals[1], vals[2])
        root.clipboard_clear()
        root.clipboard_append(ruta_completa)
        messagebox.showinfo("Ruta copiada", ruta_completa)

    tree.bind("<Double-1>", on_double_click)

    # Enter en cualquier filtro = buscar
    for c in cols:
        entry = filter_frame.grid_slaves(row=1, column=cols.index(c))[0]
        entry.bind("<Return>", lambda e: ejecutar_busqueda())

    # Carga inicial
    llenar_tree()

    root.mainloop()

if __name__ == "__main__":
    main()

