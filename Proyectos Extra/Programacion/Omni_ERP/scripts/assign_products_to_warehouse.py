#!/usr/bin/env python3
"""
Assign products to realistic warehouse locations.
Maps producto.ubicacion_almacen (e.g., "A1-P1") to almacen_ubicaciones
and distributes stock realistically.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "src" / "data" / "org_dbs" / "org_1.db"

def parse_location(loc_str):
    """Map ubicacion_almacen prefix (e.g., "A0-MISC", "A1-P1") to warehouse (pasillo, estanteria, altura, parcela)."""
    if not loc_str:
        return None
    
    loc_str = loc_str.strip().upper()
    import re
    
    # Extract prefix (e.g., "A0" from "A0-MISC" or "A1" from "A1-P1")
    match = re.match(r'([A-Z])(\d+)', loc_str)
    if not match:
        return None
    
    estanteria = match.group(1)  # A, B, C...
    pasillo_num = int(match.group(2))  # 0, 1, 2...
    
    # Map A0, A1, A2... to pasillos 1-10 cyclically
    # A0->1, A1->1, A2->2, A3->3, ... (so stock by category spreads across aisles)
    pasillo = (pasillo_num % 10) + 1 if pasillo_num > 0 else 1
    altura = (pasillo_num % 6) + 1 if pasillo_num > 0 else 3  # spread vertically
    parcela_idx = pasillo_num % 3
    parcelas = ["IZQ", "CEN", "DER"]
    parcela = parcelas[parcela_idx]
    
    if 1 <= pasillo <= 10 and 1 <= altura <= 6:
        return (pasillo, estanteria, altura, parcela)
    
    return None


def main():
    if not DB_PATH.exists():
        print("❌ org_1.db no encontrado")
        return 1
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Ensure almacen_ubicaciones exists
    cur.execute("PRAGMA table_info(almacen_ubicaciones)")
    if not cur.fetchone():
        print("⚠️ Tabla almacen_ubicaciones no existe. Ejecuta /api/demo/seed-almacen primero.")
        conn.close()
        return 1
    
    # Clear previous product assignments (but keep locations)
    cur.execute("UPDATE almacen_ubicaciones SET producto_id = NULL, ocupado = 0 WHERE organization_id = 1")
    
    assigned = 0
    skipped = 0
    assigned_by_pasillo = {}
    
    # Get all productos with stock
    cur.execute("""
        SELECT id, codigo, nombre, stock_actual, ubicacion_almacen
        FROM productos
        WHERE organization_id = 1 AND stock_actual > 0
        ORDER BY codigo
    """)
    
    for pid, codigo, nombre, stock, ubic_str in cur.fetchall():
        if not ubic_str or stock <= 0:
            skipped += 1
            continue
        
        # Parse location
        loc = parse_location(ubic_str)
        if not loc:
            skipped += 1
            continue
        
        pasillo, estanteria, altura, parcela = loc
        
        # Find matching almacen location
        cur.execute("""
            SELECT id FROM almacen_ubicaciones
            WHERE organization_id = 1 
            AND pasillo = ? AND estanteria = ? AND altura = ? AND parcela = ?
            LIMIT 1
        """, (pasillo, estanteria, altura, parcela))
        
        row = cur.fetchone()
        if row:
            ubic_id = row[0]
            # Assign product to location
            cur.execute("""
                UPDATE almacen_ubicaciones
                SET producto_id = ?, ocupado = ?
                WHERE id = ?
            """, (pid, min(int(stock), 100), ubic_id))
            assigned += 1
            assigned_by_pasillo[pasillo] = assigned_by_pasillo.get(pasillo, 0) + 1
        else:
            skipped += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Productos asignados a ubicaciones")
    print(f"   • {assigned} asignados")
    print(f"   • {skipped} sin ubicación válida")
    print(f"   • Distribución por pasillo: {assigned_by_pasillo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
