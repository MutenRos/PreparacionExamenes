#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import getpass
import mysql.connector
from textwrap import shorten

# ===========================
#  🎨 ESTILO Y UTILIDADES
# ===========================
class C:
    RESET="\033[0m"
    BOLD="\033[1m"
    DIM="\033[2m"
    ITAL="\033[3m"
    UL="\033[4m"

    # Colors
    WP_BG="\033[48;5;17m"       # azul admin
    WP_SIDE="\033[48;5;236m"    # sidebar gris
    WP_ACCENT="\033[38;5;45m"   # cian
    WP_GREEN="\033[38;5;42m"
    WP_RED="\033[38;5;196m"
    WP_YELLOW="\033[38;5;220m"
    WP_GREY="\033[38;5;245m"
    FG_WHITE="\033[38;5;15m"

    # Lines/blocks
    LINE="\033[38;5;240m" + "─" + "\033[0m"

def clear():
    os.system("cls" if os.name=="nt" else "clear")

def pause(msg="Pulsa ENTER para continuar…"):
    input(f"\n{C.WP_GREY}{msg}{C.RESET}")

def ask_yes_no(msg, default="n"):
    s=f"{msg} (s/n) [{'S' if default=='s' else 'N'}]: "
    ans=input(s).strip().lower()
    if ans=="":
        ans=default
    return ans=="s"

def header(titulo="Escritorio"):
    bar = "═"*60
    print(f"{C.WP_BG}{C.FG_WHITE}  🧩  JocarsaPress — Panel de Administración  {C.RESET}")
    print(f"{C.BOLD}{C.WP_ACCENT}{titulo}{C.RESET}  {C.WP_GREY}— estilo WordPress en consola{C.RESET}")
    print(C.LINE * 80)

def sidebar():
    items = [
        ("1", "Añadir entrada", "📝"),
        ("2", "Entradas (listar)", "📚"),
        ("3", "Actualizar entrada", "✏️"),
        ("4", "Eliminar entrada", "🗑️"),
        ("5", "Buscar", "🔎"),
        ("0", "Salir", "🚪"),
    ]
    print(f"{C.WP_SIDE}{C.FG_WHITE}{' '*2}Menú{C.RESET}")
    for k, txt, ic in items:
        print(f"  {C.BOLD}{ic}  {k}. {txt}{C.RESET}")
    print(C.LINE * 80)

def toast_ok(msg):
    print(f"{C.WP_GREEN}✔ {msg}{C.RESET}")

def toast_warn(msg):
    print(f"{C.WP_YELLOW}⚠ {msg}{C.RESET}")

def toast_error(msg):
    print(f"{C.WP_RED}✘ {msg}{C.RESET}")

def draw_panel(title, content):
    line = "─"*60
    print(f"{C.BOLD}{title}{C.RESET}")
    print(C.LINE * 60)
    print(content)
    print(C.LINE * 60)

def trunc(s, width):
    if s is None:
        return ""
    return shorten(str(s), width=width, placeholder="…")

# ===========================
#  🗄️ CONEXIÓN
# ===========================
def conectar():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="blog2526",
            password="blog2526",
            database="blog2526",
            autocommit=False
        )
    except Exception as e:
        toast_error(f"No se pudo conectar a MySQL: {e}")
        sys.exit(1)

# ===========================
#  🧱 CAPA DATOS (SEGURO)
# ===========================
def insertar_entrada(conn, titulo, contenido, fecha, autor_id):
    sql = "INSERT INTO entradas (titulo, contenido, fecha, autor) VALUES (%s,%s,%s,%s)"
    with conn.cursor() as cur:
        cur.execute(sql, (titulo, contenido, fecha, autor_id))
    conn.commit()

def actualizar_entrada(conn, ident, titulo, contenido, fecha, autor_id):
    sql = """
    UPDATE entradas
       SET titulo=%s, contenido=%s, fecha=%s, autor=%s
     WHERE Identificador=%s
    """
    with conn.cursor() as cur:
        cur.execute(sql, (titulo, contenido, fecha, autor_id, ident))
    conn.commit()

def eliminar_entrada(conn, ident):
    sql = "DELETE FROM entradas WHERE Identificador=%s"
    with conn.cursor() as cur:
        cur.execute(sql, (ident,))
    conn.commit()

def listar_entradas(conn, offset=0, limit=10, q=None):
    # Se asume vista con columnas: id, titulo, contenido, fecha, id_autor, nombre_autor
    base = "SELECT * FROM entradas_con_autores"
    params=[]
    if q:
        base += " WHERE titulo LIKE %s OR contenido LIKE %s OR fecha LIKE %s OR autor LIKE %s"
        like = f"%{q}%"
        params=[like, like, like, like]
    order = " ORDER BY fecha DESC, Identificador DESC"
    pag = " LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    sql = base + order + pag
    with conn.cursor() as cur:
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
    total = contar_entradas(conn, q)
    return rows, total

def contar_entradas(conn, q=None):
    base = "SELECT COUNT(*) FROM entradas_con_autores"
    params=[]
    if q:
        base += " WHERE titulo LIKE %s OR contenido LIKE %s OR fecha LIKE %s OR autor LIKE %s"
        like=f"%{q}%"
        params=[like, like, like, like]
    with conn.cursor() as cur:
        cur.execute(base, tuple(params))
        (n,) = cur.fetchone()
    return n

def existe_id(conn, ident):
    sql = "SELECT 1 FROM entradas WHERE Identificador=%s"
    with conn.cursor() as cur:
        cur.execute(sql, (ident,))
        return cur.fetchone() is not None

# ===========================
#  🖥️ RENDER TABLA
# ===========================
COLS = [
    ("ID", 5),
    ("Título", 24),
    ("Fecha", 10),
    ("Autor", 16),
]

def render_fila(row):
    """
    row esperado (6 columnas): 
    0: Identificador, 1: titulo, 2: contenido, 3: fecha, 4: id_autor, 5: nombre_autor
    Ajusta si tu vista difiere.
    """
    ident = str(row[0])
    titulo = row[1]
    fecha = row[3]
    autor = row[5] if len(row) > 5 else row[4]
    return [
        trunc(ident, COLS[0][1]),
        trunc(titulo, COLS[1][1]),
        trunc(str(fecha), COLS[2][1]),
        trunc(str(autor), COLS[3][1]),
    ]

def print_table(rows, page, page_size, total):
    # Encabezado
    cols_line = " | ".join([f"{C.BOLD}{name:<{w}}{C.RESET}" for name, w in COLS])
    sep = "-+-".join(["-"*w for _, w in COLS])
    print(cols_line)
    print(sep)
    # Filas
    for r in rows:
        datos = render_fila(r)
        line = " | ".join([f"{val:<{COLS[i][1]}}" for i, val in enumerate(datos)])
        print(line)

    # Footer paginación
    pages = max(1, (total + page_size - 1)//page_size)
    print("\n" + C.LINE*80)
    print(f"  Página {page}/{pages}  •  Total: {total}  •  Por página: {page_size}")
    print(C.LINE*80)

# ===========================
#  🧑‍💻 INPUTS
# ===========================
def input_nonempty(prompt):
    while True:
        v = input(prompt).strip()
        if v != "":
            return v
        toast_warn("Este campo no puede quedar vacío.")

def input_int(prompt):
    while True:
        v = input(prompt).strip()
        if v.isdigit():
            return int(v)
        toast_warn("Introduce un número válido.")

def input_date(prompt):
    # Acepta cualquier string, pero sugiere formato
    v = input(f"{prompt} (sugerido YYYY-MM-DD): ").strip()
    return v if v else time.strftime("%Y-%m-%d")

# ===========================
#  🧭 ACCIONES
# ===========================
def accion_insertar(conn):
    header("Añadir nueva entrada")
    titulo = input_nonempty("Título: ")
    contenido = input_nonempty("Contenido: ")
    fecha = input_date("Fecha")
    autor_id = input_int("ID autor (numérico): ")
    draw_panel("Previsualización", f"📝 {C.BOLD}{titulo}{C.RESET}\n{C.DIM}{fecha}{C.RESET}\n\n{contenido}\n\n👤 Autor ID: {autor_id}")
    if ask_yes_no("¿Publicar esta entrada?", "s"):
        try:
            insertar_entrada(conn, titulo, contenido, fecha, autor_id)
            toast_ok("Entrada publicada.")
        except Exception as e:
            conn.rollback()
            toast_error(f"Error insertando: {e}")
    else:
        toast_warn("Operación cancelada.")
    pause()

def accion_listar(conn, q=None):
    page=1
    page_size=10
    while True:
        clear()
        header("Entradas")
        sidebar()
        offset=(page-1)*page_size
        rows,total = listar_entradas(conn, offset=offset, limit=page_size, q=q)
        if total==0:
            toast_warn("No hay entradas que coincidan." if q else "No hay entradas aún.")
            print("\nOpciones: [A]ñadir, [B]uscar, [M]enú")
        else:
            print_table(rows, page, page_size, total)
            print("Opciones: [N]ext, [P]rev, [A]ñadir, [B]uscar, [M]enú")
        op=input("→ ").strip().lower()
        if op=="n" and (offset+page_size)<total:
            page+=1
        elif op=="p" and page>1:
            page-=1
        elif op=="a":
            accion_insertar(conn)
        elif op=="b":
            q=input("Buscar (título/contenido/fecha/autor): ").strip()
            page=1
        elif op=="m" or op=="":
            break

def accion_actualizar(conn):
    header("Actualizar entrada")
    ident = input_int("ID (Identificador) a actualizar: ")
    if not existe_id(conn, ident):
        toast_error("No existe una entrada con ese ID.")
        return pause()
    titulo = input_nonempty("Nuevo título: ")
    contenido = input_nonempty("Nuevo contenido: ")
    fecha = input_date("Nueva fecha")
    autor_id = input_int("Nuevo ID autor: ")
    draw_panel("Confirmación de cambios",
               f"ID: {ident}\nTítulo: {titulo}\nFecha: {fecha}\nAutor ID: {autor_id}\n\nContenido:\n{contenido}")
    if ask_yes_no("¿Aplicar cambios?", "s"):
        try:
            actualizar_entrada(conn, ident, titulo, contenido, fecha, autor_id)
            toast_ok("Entrada actualizada.")
        except Exception as e:
            conn.rollback()
            toast_error(f"Error actualizando: {e}")
    else:
        toast_warn("Operación cancelada.")
    pause()

def accion_eliminar(conn):
    header("Eliminar entrada")
    ident = input_int("ID (Identificador) a eliminar: ")
    if not existe_id(conn, ident):
        toast_error("No existe una entrada con ese ID.")
        return pause()
    if ask_yes_no(f"¿Seguro que deseas eliminar la entrada {ident}? Esta acción no se puede deshacer.", "n"):
        try:
            eliminar_entrada(conn, ident)
            toast_ok("Entrada eliminada.")
        except Exception as e:
            conn.rollback()
            toast_error(f"Error eliminando: {e}")
    else:
        toast_warn("Operación cancelada.")
    pause()

def accion_buscar(conn):
    header("Buscar")
    q=input("Texto a buscar (en título, contenido, fecha o autor): ").strip()
    accion_listar(conn, q=q)

# ===========================
#  🚀 APP
# ===========================
def main():
    conn = conectar()
    try:
        while True:
            clear()
            header("Escritorio")
            sidebar()
            print(f"{C.BOLD}Consejo:{C.RESET} Usa {C.WP_ACCENT}N/P{C.RESET} para paginar en el listado. Ítems tipo WordPress en consola 😉")
            print()
            print("Selecciona una opción:")
            print("  1) Añadir entrada  📝")
            print("  2) Entradas        📚")
            print("  3) Actualizar      ✏️")
            print("  4) Eliminar        🗑️")
            print("  5) Buscar          🔎")
            print("  0) Salir           🚪")
            op = input("\n→ ").strip()
            if op=="1":
                accion_insertar(conn)
            elif op=="2":
                accion_listar(conn)
            elif op=="3":
                accion_actualizar(conn)
            elif op=="4":
                accion_eliminar(conn)
            elif op=="5":
                accion_buscar(conn)
            elif op=="0":
                clear()
                print(f"{C.DIM}Cerrando sesión del panel…{C.RESET}")
                break
            else:
                toast_warn("Opción no válida.")
                time.sleep(1)
    finally:
        try:
            conn.close()
        except:
            pass

if __name__ == "__main__":
    main()

