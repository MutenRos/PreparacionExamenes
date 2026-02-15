#!/usr/bin/env python3
"""
Distribute all products across warehouse locations realistically.
Since most products share same ubicacion_almacen prefix, spread them
across available warehouse slots using round-robin.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "src" / "data" / "org_dbs" / "org_1.db"

def main():
    if not DB_PATH.exists():
        print("❌ org_1.db no encontrado")
        return 1
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Get all available warehouse locations
    cur.execute("""
        SELECT id, pasillo, estanteria, altura, parcela
        FROM almacen_ubicaciones
        WHERE organization_id = 1
        ORDER BY pasillo, estanteria, altura, parcela
    """)
    locations = cur.fetchall()
    total_locs = len(locations)
    
    if total_locs == 0:
        print("❌ No warehouse locations available")
        conn.close()
        return 1
    
    # Get all products with stock
    cur.execute("""
        SELECT id, codigo, stock_actual
        FROM productos
        WHERE organization_id = 1 AND stock_actual > 0
        ORDER BY RANDOM()
    """)
    products = cur.fetchall()
    
    # Distribute products across entire warehouse using larger spacing
    # Skip every N locations to spread them out evenly
    assigned = 0
    spacing = max(1, total_locs // (len(products) + 1))  # Space products evenly
    
    for idx, (pid, codigo, stock) in enumerate(products):
        # Use spacing to distribute across entire warehouse
        loc_idx = (idx * spacing) % total_locs
        loc_id = locations[loc_idx][0]
        
        # Ocupado = min(stock, location_capacity)
        ocupado = min(int(stock), 100)
        
        cur.execute("""
            UPDATE almacen_ubicaciones
            SET producto_id = ?, ocupado = ?
            WHERE id = ?
        """, (pid, ocupado, loc_id))
        assigned += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Productos distribuidos uniformemente en almacén")
    print(f"   • {assigned} productos asignados")
    print(f"   • {total_locs} ubicaciones disponibles")
    print(f"   • Espaciamiento: cada {spacing} ubicaciones")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
