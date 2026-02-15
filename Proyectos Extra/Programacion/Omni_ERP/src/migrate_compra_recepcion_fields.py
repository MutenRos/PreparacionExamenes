#!/usr/bin/env python3
"""Migration script to add reception tracking fields to Compra table."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


async def main():
    """Add reception tracking columns to compras table."""
    try:
        from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
        from sqlalchemy import text
        from dario_app.database import Base, ORG_DB_DIR, MASTER_DATABASE_URL
        from dario_app.modules.compras.models import Compra

        print("🔄 Adding reception tracking fields to purchases...")

        # SQL to add columns (SQLite compatible)
        add_columns_sql = """
        ALTER TABLE compras ADD COLUMN estado_recepcion VARCHAR(20) NOT NULL DEFAULT 'no_recibida';
        ALTER TABLE compras ADD COLUMN cantidad_items_esperados INTEGER NOT NULL DEFAULT 0;
        ALTER TABLE compras ADD COLUMN cantidad_items_recibidos INTEGER NOT NULL DEFAULT 0;
        ALTER TABLE compras ADD COLUMN fecha_primera_recepcion DATETIME;
        """

        # Try to add columns to master DB
        try:
            engine = create_async_engine(MASTER_DATABASE_URL, echo=False)
            async with engine.begin() as conn:
                for sql in add_columns_sql.split(';'):
                    sql = sql.strip()
                    if sql:
                        try:
                            await conn.execute(text(sql))
                            print(f"✅ Master DB: {sql[:50]}...")
                        except Exception as e:
                            if "duplicate column" in str(e).lower():
                                print(f"ℹ️  Column already exists (skipping)")
                            else:
                                print(f"⚠️  {e}")
            await engine.dispose()
            print("✅ Master DB updated")
        except Exception as e:
            print(f"⚠️  Master DB error: {e}")

        # Add columns to all existing org databases
        org_db_dir = Path(ORG_DB_DIR)
        if org_db_dir.exists():
            org_dbs = list(org_db_dir.glob("org_*.db"))
            for org_db_path in org_dbs:
                org_id = int(org_db_path.stem.split("_")[1])
                db_url = f"sqlite+aiosqlite:///{org_db_path}"
                
                try:
                    engine = create_async_engine(db_url, echo=False)
                    async with engine.begin() as conn:
                        for sql in add_columns_sql.split(';'):
                            sql = sql.strip()
                            if sql:
                                try:
                                    await conn.execute(text(sql))
                                except Exception as e:
                                    if "duplicate column" not in str(e).lower():
                                        print(f"⚠️  Org {org_id}: {e}")
                    await engine.dispose()
                    print(f"✅ Org {org_id} DB updated")
                except Exception as e:
                    print(f"⚠️  Org {org_id} error: {e}")

        print("\n✅ Reception tracking fields successfully added!")
        print("\nNew columns in 'compras' table:")
        print("  • estado_recepcion (no_recibida, parcial, completa)")
        print("  • cantidad_items_esperados")
        print("  • cantidad_items_recibidos")
        print("  • fecha_primera_recepcion")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
