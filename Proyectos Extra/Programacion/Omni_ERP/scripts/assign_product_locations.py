#!/usr/bin/env python3
"""Assign default warehouse locations to products in org_1.db.

Rules (simple demo):
- Map by product code prefix to aisles/bins.
- Only update rows where ubicacion_almacen is NULL/empty.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "src" / "data" / "org_dbs" / "org_1.db"

PREFIX_MAP = {
    "BC": "A1-P1",  # Bomba Centrifuga
    "BS": "A1-P2",  # Bombas Sumergibles/Serie S
    "BA": "A1-P3",  # Autoaspirante
    "BD": "A2-P1",  # Diesel
    "BP": "A2-P2",  # Presion/compactas
    "BI": "A2-P3",  # Industrial/verde
}

DEFAULT_BIN = "A0-MISC"

def main():
    if not DB_PATH.exists():
        print("❌ org_1.db no encontrado. Ejecuta seed primero.")
        return 1

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(productos)")
    cols = [c[1] for c in cur.fetchall()]
    if "ubicacion_almacen" not in cols:
        print("❌ La columna ubicacion_almacen no existe. Ejecuta la migración/alter primero.")
        conn.close()
        return 1

    cur.execute("SELECT id, codigo, ubicacion_almacen FROM productos WHERE organization_id = 1")
    rows = cur.fetchall()

    updated = 0
    for pid, codigo, ubic in rows:
        if ubic and str(ubic).strip():
            continue  # keep existing
        prefix = (codigo or "")[:2]
        new_loc = PREFIX_MAP.get(prefix, DEFAULT_BIN)
        cur.execute(
            "UPDATE productos SET ubicacion_almacen = ? WHERE id = ?",
            (new_loc, pid),
        )
        updated += 1

    conn.commit()
    conn.close()

    print(f"✅ Ubicaciones asignadas: {updated} productos actualizados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
