#!/usr/bin/env python3
"""
Normaliza ubicaciones de productos y movimientos al formato canónico del almacén.

Formato canónico: "pasillo/estanteria/altura/parcela" (p.ej., 1/A/3/C)
Patrones soportados para productos: "A1-P3", "A1-P3-IZQ", "A1-P3-CEN".

Acciones:
- Actualiza movimientos_almacen.ubicacion_origen a código válido (con fallback a la primera ubicación activa).
- Actualiza productos.ubicacion_almacen a código válido (con fallback opcional).

Uso:
  python3 scripts/normalize_ubicaciones.py [--org 1] [--fallback-products]
"""

import argparse
import os
import re
import sqlite3
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--org", type=int, default=1, help="organization_id a procesar")
    parser.add_argument(
        "--fallback-products",
        action="store_true",
        help="Si no se puede mapear la ubicación de producto, hacer fallback a la primera ubicación activa",
    )
    return parser.parse_args()


def get_db_path() -> Path:
    here = Path(__file__).resolve().parent.parent
    return here / "src" / "data" / "org_dbs" / "org_1.db"


def cargar_ubicaciones_validas(cur, org_id: int) -> list[str]:
    cur.execute(
        "SELECT codigo FROM almacen_ubicaciones WHERE organization_id=? AND activo=1",
        (org_id,),
    )
    return [r[0] for r in cur.fetchall()]


def canonical_from_text(texto: str | None, valid_set: set[str], fallback: str) -> str | None:
    """Convierte texto de producto a código canónico, si existe en el maestro.

    - Si ya es un código válido exacto: devuelve tal cual.
    - Patrones: 'A1-P3' o 'A1-P3-IZQ' -> '1/A/3/I'.
    - Si no mapea, devuelve None (para que el llamador decida fallback o no).
    """
    if not texto:
        return None
    up = texto.strip()
    if up in valid_set:
        return up

    m = re.match(r"^([A-Za-z])(\d+)[-_/]P(\d+)(?:[-_/](CEN|DER|IZQ|C|D|I))?$", up, re.IGNORECASE)
    if m:
        est, pasillo, altura, parcela = m.group(1), m.group(2), m.group(3), m.group(4)
        est = est.upper()
        mapa_parcela = {"CEN": "C", "DER": "D", "IZQ": "I", "C": "C", "D": "D", "I": "I"}
        letra_parcela = mapa_parcela.get((parcela or "CEN").upper(), "C")
        candidato = f"{int(pasillo)}/{est}/{int(altura)}/{letra_parcela}"
        if candidato in valid_set:
            return candidato

    return None


def normalizar_movimientos(con, org_id: int, valid: list[str]) -> int:
    cur = con.cursor()
    valid_set = set(valid)
    fallback = sorted(valid)[0] if valid else "1/A/1/C"

    cur.execute(
        "SELECT id, ubicacion_origen FROM movimientos_almacen WHERE organization_id=?",
        (org_id,),
    )
    rows = cur.fetchall()
    updated = 0
    for mid, orig in rows:
        if orig and orig in valid_set:
            continue
        nuevo = canonical_from_text(orig, valid_set, fallback)
        if not nuevo:
            nuevo = fallback
        cur.execute(
            "UPDATE movimientos_almacen SET ubicacion_origen=? WHERE id=?",
            (nuevo, mid),
        )
        updated += 1
    return updated


def normalizar_productos(con, org_id: int, valid: list[str], allow_fallback: bool) -> tuple[int, int]:
    cur = con.cursor()
    valid_set = set(valid)
    fallback = sorted(valid)[0] if valid else "1/A/1/C"

    cur.execute(
        "SELECT id, ubicacion_almacen FROM productos WHERE organization_id=?",
        (org_id,),
    )
    rows = cur.fetchall()
    updated = 0
    unmapped = 0
    for pid, up in rows:
        nuevo = canonical_from_text(up, valid_set, fallback)
        if not nuevo:
            if allow_fallback:
                nuevo = fallback
            else:
                unmapped += 1
                continue
        if nuevo != (up or ""):
            cur.execute(
                "UPDATE productos SET ubicacion_almacen=? WHERE id=?",
                (nuevo, pid),
            )
            updated += 1
    return updated, unmapped


def main():
    args = parse_args()
    db_path = get_db_path()
    if not db_path.exists():
        print(f"❌ DB no encontrada: {db_path}")
        raise SystemExit(1)

    con = sqlite3.connect(str(db_path))
    try:
        cur = con.cursor()
        valid = cargar_ubicaciones_validas(cur, args.org)
        print(f"✓ Ubicaciones activas: {len(valid)}")

        con.execute("BEGIN")
        mov_upd = normalizar_movimientos(con, args.org, valid)
        prod_upd, prod_unmapped = normalizar_productos(con, args.org, valid, allow_fallback=args.fallback_products)
        con.commit()

        print("\n=== Resumen ===")
        print(f"• Movimientos normalizados: {mov_upd}")
        print(f"• Productos normalizados: {prod_upd}")
        if not args.fallback_products and prod_unmapped:
            print(f"• Productos sin mapping (dejados igual): {prod_unmapped}")
        if args.fallback_products and prod_unmapped:
            # No debería ocurrir en modo fallback, pero por si acaso
            print(f"• Productos sin mapping (con fallback): {prod_unmapped}")
        print("================")

    except Exception as e:
        con.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        con.close()


if __name__ == "__main__":
    main()
