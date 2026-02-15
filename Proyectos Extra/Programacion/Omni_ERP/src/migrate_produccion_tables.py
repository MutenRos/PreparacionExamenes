#!/usr/bin/env python3
"""Migrate new produccion tables: registro_trabajo, incidencias_produccion, solicitudes_material_produccion."""
import asyncio
import sys

sys.path.insert(0, "/home/dario/omni-solutions/products/erp/backend")


async def main():
    from dario_app.database import get_tenant_engine
    from dario_app.modules.produccion_ordenes.models import Base as ProduccionBase
    from sqlalchemy import inspect

    org_id = 1  # Default tenant
    
    try:
        engine = get_tenant_engine(org_id)
        
        # Create all tables from produccion models
        async with engine.begin() as conn:
            await conn.run_sync(ProduccionBase.metadata.create_all)
        
        # Verify tables were created
        async with engine.connect() as conn:
            tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
            
        if 'registro_trabajo' in tables:
            print("✅ Tabla registro_trabajo creada")
        if 'incidencias_produccion' in tables:
            print("✅ Tabla incidencias_produccion creada")
        if 'solicitudes_material_produccion' in tables:
            print("✅ Tabla solicitudes_material_produccion creada")
            
        print(f"✅ Migración completada exitosamente. Total de tablas: {len(tables)}")
        return 0
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
