#!/usr/bin/env python3
"""Migration script to add Receipt and Logistics tables."""
import asyncio
import sys
from pathlib import Path

# Setup path - use the correct backend directory
BACKEND_DIR = Path(__file__).parent / "dario_app"
sys.path.insert(0, str(Path(__file__).parent))


async def main():
    """Create receipt and logistics tables."""
    try:
        from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
        from dario_app.database import Base, ORG_DB_DIR, MASTER_DATABASE_URL
        
        # Import all models to register them (this ensures FK relationships work)
        from dario_app.modules.tenants.models import Organization
        from dario_app.modules.usuarios.models import Usuario
        from dario_app.modules.compras.models import Compra, CompraDetalle
        from dario_app.modules.inventario.models import Producto, Proveedor
        from dario_app.modules.produccion_ordenes.models import OrdenProduccion
        from dario_app.modules.recepcion.models import (
            Albaran,
            AlbaranDetalle,
            MovimientoLogistico,
            FacturaExterna,
        )

        print("🔄 Adding Receipt and Logistics models to database...")

        # Create tables in master DB
        engine = create_async_engine(MASTER_DATABASE_URL, echo=False)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()
        print("✅ Master DB tables created/updated")

        # Create tables in all existing org databases
        org_db_dir = Path(ORG_DB_DIR)
        if org_db_dir.exists():
            org_dbs = list(org_db_dir.glob("org_*.db"))
            for org_db_path in org_dbs:
                org_id = int(org_db_path.stem.split("_")[1])
                db_url = f"sqlite+aiosqlite:///{org_db_path}"
                
                engine = create_async_engine(db_url, echo=False)
                async with engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                await engine.dispose()
                print(f"✅ Org {org_id} DB tables created/updated")

        print("\n✅ Receipt and Logistics tables successfully added!")
        print("\nNew tables:")
        print("  - albaranes (Receipt documents)")
        print("  - albaranes_detalle (Receipt items)")
        print("  - movimientos_logisticos (Logistics movements)")
        print("  - facturas_externas (External invoices for reconciliation)")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
