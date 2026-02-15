#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
import sys
from textwrap import shorten

DB_PATH = "empresa.db"

# =======================
# ANSI / Estilo consola
# =======================
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDER = "\033[4m"

FG_BLACK   = "\033[30m"
FG_RED     = "\033[31m"
FG_GREEN   = "\033[32m"
FG_YELLOW  = "\033[33m"
FG_BLUE    = "\033[34m"
FG_MAGENTA = "\033[35m"
FG_CYAN    = "\033[36m"
FG_WHITE   = "\033[37m"

BG_BLACK   = "\033[40m"
BG_RED     = "\033[41m"
BG_GREEN   = "\033[42m"
BG_YELLOW  = "\033[43m"
BG_BLUE    = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN    = "\033[46m"
BG_WHITE   = "\033[47m"

CLEAR = "\033[2J"
HOME = "\033[0;0H"

# Box-drawing
HL = "─"
VL = "│"
TL = "┌"
TR = "┐"
BL = "└"
BR = "┘"
TJ = "┬"
BJ = "┴"
LJ = "├"
RJ = "┤"
CJ = "┼"

PAGE_SIZE = 20
TRUNC = 40  # truncado visual por celda

def cls():
    print(CLEAR + HOME, end="")

def banner():
    title = f"{BOLD}{FG_CYAN}Programa de gestión{RESET}"
    author = f"{DIM}(c) 2025 Jose Vicente Carratala{RESET}"
    bar = HL * 60
    print(f"{TL}{bar}{TR}")
    print(f"{VL} {title:<58}{VL}")
    print(f"{VL} {author:<58}{VL}")
    print(f"{BL}{bar}{BR}")

def pause(msg="Pulsa una tecla para continuar..."):
    try:
        input(f"{DIM}{msg}{RESET}")
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)

def error(msg):
    print(f"{FG_RED}{BOLD}✗ {msg}{RESET}")

def success(msg):
    print(f"{FG_GREEN}{BOLD}✓ {msg}{RESET}")

def info(msg):
    print(f"{FG_CYAN}{msg}{RESET}")

def ask(prompt):
    return input(f"{FG_YELLOW}? {prompt}{RESET}")

def ask_int(prompt, minv=None, maxv=None):
    while True:
        val = input(f"{FG_YELLOW}? {prompt}{RESET}")
        try:
            n = int(val)
            if minv is not None and n < minv:
                error(f"El valor debe ser ≥ {minv}.")
                continue
            if maxv is not None and n > maxv:
                error(f"El valor debe ser ≤ {maxv}.")
                continue
            return n
        except ValueError:
            error("Introduce un número válido.")

def connect(db_path):
    try:
        return sqlite3.connect(db_path)
    except sqlite3.Error as e:
        error(f"No se pudo abrir la BD: {e}")
        sys.exit(1)

# =======================
# Utilidades de esquema
# =======================
def list_tables(cur):
    cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)
    return [r[0] for r in cur.fetchall()]

def table_info(cur, table):
    cur.execute(f"PRAGMA table_info({table});")
    # cid, name, type, notnull, dflt_value, pk
    cols = cur.fetchall()
    return cols

def primary_keys(columns_info):
    # Devuelve lista de nombres de columnas que forman la PK (orden por cid/PRAGMA)
    pks = [c[1] for c in columns_info if c[5] > 0]
    # PRAGMA pk>0 indica orden, así que ordenamos por c[5]
    pks = [c[1] for c in sorted(columns_info, key=lambda x: x[5] if x[5] else 0) if c[5] > 0]
    return pks

def column_names(columns_info):
    return [c[1] for c in columns_info]

def is_integer_pk_autoinc(columns_info, col_name):
    # Heurística: tipo contiene "INT" y es PK
    for c in columns_info:
        if c[1] == col_name:
            return c[5] > 0 and "INT" in (c[2] or "").upper()
    return False

# =======================
# Render de tablas
# =======================
def format_table(headers, rows, max_width=TRUNC):
    # calcular anchos
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            cell_s = "" if cell is None else str(cell)
            lw = len(cell_s)
            if lw > max_width:
                lw = max_width
            if lw > widths[i]:
                widths[i] = lw

    def hline(left, mid, right):
        parts = []
        for w in widths:
            parts.append(HL * (w + 2))
        return left + mid.join(parts) + right

    def render_row(values):
        cells = []
        for i, v in enumerate(values):
            s = "" if v is None else str(v)
            s = shorten(s, width=widths[i], placeholder="…") if len(s) > widths[i] else s
            cells.append(f" {s:<{widths[i]}} ")
        return VL + VL.join(cells) + VL

    top = hline(TL, TJ, TR)
    sep = hline(LJ, CJ, RJ)
    bot = hline(BL, BJ, BR)

    lines = [top, render_row([f"{BOLD}{h}{RESET}" for h in headers]), sep]
    for r in rows:
        lines.append(render_row(r))
    lines.append(bot)
    return "\n".join(lines)

def paginated_print(headers, rows):
    if not rows:
        info("No hay registros.")
        return
    total = len(rows)
    page = 0
    while True:
        cls()
        banner()
        start = page * PAGE_SIZE
        end = min(start + PAGE_SIZE, total)
        subset = rows[start:end]
        print(f"{DIM}Mostrando {start+1}-{end} de {total}{RESET}\n")
        print(format_table(headers, subset))
        print()
        cmd = input(f"{DIM}[N]ext, [P]rev, [Q]uit ▶ {RESET}").strip().lower()
        if cmd in ("q", ""):
            break
        if cmd == "n" and end < total:
            page += 1
        elif cmd == "p" and page > 0:
            page -= 1

# =======================
# CRUD Operations
# =======================
def op_create(cur, con, table):
    cls()
    banner()
    print(f"{BOLD}Insertar en {table}{RESET}\n")
    cols = table_info(cur, table)
    names = column_names(cols)
    values = []
    for c in cols:
        name, ctype, notnull, dflt, pk = c[1], c[2], c[3], c[4], c[5]
        hint = []
        if pk: hint.append("PK")
        if notnull and dflt is None: hint.append("NOT NULL")
        if dflt is not None: hint.append(f"DEF={dflt}")
        if ctype: hint.append(ctype)
        tag = f" ({', '.join(hint)})" if hint else ""
        val = input(f"{FG_YELLOW}· {name}{RESET}{DIM}{tag}{RESET} (Enter=NULL): ").strip()
        if val == "":
            values.append(None)
        else:
            values.append(val)

    placeholders = ",".join(["?"] * len(names))
    sql = f"INSERT INTO {table} ({','.join(names)}) VALUES ({placeholders})"
    try:
        cur.execute(sql, values)
        con.commit()
        success("Registro insertado.")
    except sqlite3.Error as e:
        error(f"No se pudo insertar: {e}")
    pause()

def op_list(cur, table):
    cls()
    banner()
    print(f"{BOLD}Listado de {table}{RESET}\n")
    cols = table_info(cur, table)
    names = column_names(cols)
    try:
        cur.execute(f"SELECT {', '.join(names)} FROM {table};")
        rows = cur.fetchall()
        paginated_print(names, rows)
    except sqlite3.Error as e:
        error(f"No se pudo listar: {e}")
        pause()

def read_by_pk(cur, table, pk_cols, pk_values):
    where = " AND ".join([f"{c}=?" for c in pk_cols])
    sql = f"SELECT * FROM {table} WHERE {where} LIMIT 1;"
    cur.execute(sql, pk_values)
    return cur.fetchone()

def op_update(cur, con, table):
    cls()
    banner()
    print(f"{BOLD}Actualizar en {table}{RESET}\n")
    cols = table_info(cur, table)
    names = column_names(cols)
    pk_cols = primary_keys(cols)
    if not pk_cols:
        error("Esta tabla no tiene clave primaria definida. Actualización no soportada.")
        return pause()

    # Pedir PK(s)
    pk_values = []
    print(f"{FG_CYAN}Introduce la clave primaria para localizar el registro:{RESET}")
    for pk in pk_cols:
        v = input(f"· {pk}: ").strip()
        if v == "":
            error("La clave primaria no puede quedar vacía.")
            return pause()
        pk_values.append(v)

    # Leer registro actual
    row = read_by_pk(cur, table, pk_cols, pk_values)
    if not row:
        error("No se encontró el registro con esa PK.")
        return pause()

    # Mostrar registro actual
    print("\nRegistro actual:")
    print(format_table(names, [row]))
    print()

    # Solicitar nuevos valores (Enter = mantener)
    new_values = []
    for i, c in enumerate(cols):
        cname = c[1]
        current = row[i]
        if cname in pk_cols:
            # Bloqueamos edición de PK por simplicidad (se podría permitir)
            print(f"{DIM}{cname} (PK) = {current} (no editable){RESET}")
            new_values.append(current)
        else:
            val = input(f"{FG_YELLOW}· {cname}{RESET} {DIM}[actual: {current}]{RESET} (Enter=mantener): ")
            if val.strip() == "":
                new_values.append(current)
            else:
                new_values.append(val)

    # Construir UPDATE
    set_clause = ", ".join([f"{n}=?" for n in names if n not in pk_cols])
    where = " AND ".join([f"{c}=?" for c in pk_cols])
    params = [new_values[names.index(n)] for n in names if n not in pk_cols] + pk_values

    sql = f"UPDATE {table} SET {set_clause} WHERE {where};"
    try:
        cur.execute(sql, params)
        con.commit()
        success(f"Filas afectadas: {cur.rowcount}")
    except sqlite3.Error as e:
        error(f"No se pudo actualizar: {e}")
    pause()

def op_delete(cur, con, table):
    cls()
    banner()
    print(f"{BOLD}Eliminar en {table}{RESET}\n")
    cols = table_info(cur, table)
    names = column_names(cols)
    pk_cols = primary_keys(cols)
    if not pk_cols:
        error("Esta tabla no tiene clave primaria definida. Eliminación no soportada.")
        return pause()

    # Pedir PK(s)
    pk_values = []
    print(f"{FG_CYAN}Introduce la clave primaria del registro a eliminar:{RESET}")
    for pk in pk_cols:
        v = input(f"· {pk}: ").strip()
        if v == "":
            error("La clave primaria no puede quedar vacía.")
            return pause()
        pk_values.append(v)

    # Confirmación mostrando el registro
    row = read_by_pk(cur, table, pk_cols, pk_values)
    if not row:
        error("No se encontró el registro con esa PK.")
        return pause()

    print("\nRegistro a eliminar:")
    print(format_table(names, [row]))
    print()
    conf = input(f"{FG_RED}{BOLD}¿Seguro que deseas eliminarlo? (s/N): {RESET}").strip().lower()
    if conf != "s":
        info("Cancelado.")
        return pause()

    where = " AND ".join([f"{c}=?" for c in pk_cols])
    sql = f"DELETE FROM {table} WHERE {where};"
    try:
        cur.execute(sql, pk_values)
        con.commit()
        success(f"Filas afectadas: {cur.rowcount}")
    except sqlite3.Error as e:
        error(f"No se pudo eliminar: {e}")
    pause()

# =======================
# Menús
# =======================
def select_table(cur):
    while True:
        cls()
        banner()
        print(f"{BOLD}Selecciona una entidad (tabla){RESET}\n")
        tables = list_tables(cur)
        if not tables:
            error("No hay tablas en la base de datos.")
            pause("Crea alguna tabla y vuelve a ejecutar. Pulsa una tecla…")
            sys.exit(0)

        for i, t in enumerate(tables, 1):
            print(f"{FG_CYAN}{i:>2}{RESET} {VL} {t}")
        print()
        op = ask_int("Tu opción elegida: ", minv=1, maxv=len(tables))
        return tables[op - 1]

def select_operation(table):
    cls()
    banner()
    print(f"{BOLD}Tabla seleccionada: {FG_GREEN}{table}{RESET}\n")
    print(f"{BOLD}Selecciona una operación:{RESET}")
    print(f"  {FG_CYAN}1{RESET} {VL} Crear un registro")
    print(f"  {FG_CYAN}2{RESET} {VL} Listado de registros")
    print(f"  {FG_CYAN}3{RESET} {VL} Actualizar un registro")
    print(f"  {FG_CYAN}4{RESET} {VL} Eliminar un registro")
    print(f"  {FG_CYAN}5{RESET} {VL} Cambiar de tabla")
    print(f"  {FG_CYAN}0{RESET} {VL} Salir")
    print()
    return ask_int("Selecciona una opción: ", minv=0, maxv=5)

# =======================
# Main loop
# =======================
def main():
    con = connect(DB_PATH)
    cur = con.cursor()

    cls()
    banner()
    pause()

    current_table = None

    while True:
        if not current_table:
            current_table = select_table(cur)

        op = select_operation(current_table)
        if op == 0:
            cls()
            info("Hasta pronto 👋")
            break
        elif op == 1:
            op_create(cur, con, current_table)
        elif op == 2:
            op_list(cur, current_table)
        elif op == 3:
            op_update(cur, con, current_table)
        elif op == 4:
            op_delete(cur, con, current_table)
        elif op == 5:
            current_table = None

    try:
        con.close()
    except Exception:
        pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cls()
        info("Interrumpido por el usuario.")

