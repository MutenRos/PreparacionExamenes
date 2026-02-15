"""Upgrade admin account to PRO plan."""

import asyncio
import sys

sys.path.insert(0, "/home/dario/src")

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


async def upgrade_admin():
    """Upgrade admin organization to PRO plan."""
    
    # Direct connection to master database
    MASTER_DATABASE_URL = "sqlite+aiosqlite:////home/dario/src/data/erp.db"
    
    engine = create_async_engine(MASTER_DATABASE_URL, echo=False, future=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Check if org exists
        result = await session.execute(
            text("SELECT id, nombre, plan FROM organizations WHERE slug = 'admin-system'")
        )
        row = result.fetchone()

        if row:
            org_id, nombre, current_plan = row
            print(f"✓ Organización encontrada: {nombre}")
            print(f"  Plan actual: {current_plan}")
            
            # Update to pro plan
            await session.execute(
                text("UPDATE organizations SET plan = 'pro' WHERE slug = 'admin-system'")
            )
            await session.commit()
            
            # Verify
            result = await session.execute(
                text("SELECT plan FROM organizations WHERE slug = 'admin-system'")
            )
            new_plan = result.scalar()
            
            print(f"✅ Plan actualizado a: {new_plan}")
            print(f"✅ Tipo de plan: PRO - Plan Basic completado")
            print(f"✅ Estado: active")
        else:
            print("❌ Organización admin no encontrada")
            print("   Revisa la base de datos o ejecuta create_admin.py primero")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(upgrade_admin())
