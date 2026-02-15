#!/usr/bin/env python3
"""Setup production database with all required data."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, '/home/dario/src')

async def main():
    from dario_app.database import master_engine, create_tenant_db, get_db
    from dario_app.database import Base
    
    # Create master tables
    print("✓ Creating master database tables...")
    async with master_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create tenant database
    print("✓ Creating tenant database (org_id=1)...")
    await create_tenant_db(1)
    
    # Verify all tables were created
    from dario_app.database import get_tenant_engine
    from sqlalchemy import text
    engine = get_tenant_engine(1)
    
    async with engine.begin() as conn:
        # Check which tables exist
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = {row[0] for row in result.fetchall()}
        print(f"  Tables created: {len(tables)}")
        
        # Force create organizations table if not exists
        if 'organizations' not in tables:
            print("  Creating organizations table manually...")
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS organizations (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    activa BOOLEAN DEFAULT 1
                )
            """))
            # Insert organization 1
            await conn.execute(text("INSERT OR IGNORE INTO organizations (id, nombre) VALUES (1, 'Default Organization')"))
            tables.add('organizations')
            print("  Creating usuarios table manually...")
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    organization_id INTEGER NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    email_personal TEXT,
                    telefono TEXT,
                    dni TEXT,
                    iban TEXT,
                    hashed_password TEXT NOT NULL,
                    nombre TEXT,
                    apellidos TEXT,
                    nombre_completo TEXT,
                    activo BOOLEAN DEFAULT 1,
                    es_admin BOOLEAN DEFAULT 0,
                    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            tables.add('usuarios')
        
        if not tables:
            print("  WARNING: No tables found in org_1.db")
    
    # Now seed with production data
    print("✓ Seeding production sections...")
    from dario_app.modules.produccion_ordenes.models import SeccionProduccion, TipoSeccion
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import select
    
    # Get tenant engine
    from dario_app.database import get_tenant_engine, async_sessionmaker
    engine = get_tenant_engine(1)
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with session_maker() as session:
        # Check if data exists
        result = await session.execute(select(SeccionProduccion))
        existing = result.scalars().all()
        
        if len(existing) == 0:
            print(f"  Creating 16 production sections...")
            
            sections_data = [
                # Ensamblaje (7)
                ("SEC-ENS-01", "Ensamblaje Línea 1", "Línea de ensamblaje", TipoSeccion.ENSAMBLAJE, 100.0, 3, "Nave A - Línea 1"),
                ("SEC-ENS-02", "Ensamblaje Línea 2", "Línea de ensamblaje", TipoSeccion.ENSAMBLAJE, 100.0, 4, "Nave A - Línea 2"),
                ("SEC-ENS-03", "Ensamblaje Línea 3", "Línea de ensamblaje", TipoSeccion.ENSAMBLAJE, 100.0, 5, "Nave A - Línea 3"),
                ("SEC-ENS-04", "Ensamblaje Línea 4", "Línea de ensamblaje", TipoSeccion.ENSAMBLAJE, 100.0, 6, "Nave A - Línea 4"),
                ("SEC-ENS-05", "Ensamblaje Línea 5", "Línea de ensamblaje", TipoSeccion.ENSAMBLAJE, 100.0, 7, "Nave A - Línea 5"),
                ("SEC-ENS-06", "Ensamblaje Línea 6", "Línea de ensamblaje", TipoSeccion.ENSAMBLAJE, 100.0, 5, "Nave A - Línea 6"),
                ("SEC-ENS-07", "Ensamblaje Línea 7", "Línea de ensamblaje", TipoSeccion.ENSAMBLAJE, 100.0, 4, "Nave A - Línea 7"),
                # Pintura (3)
                ("SEC-PIN-01", "Pintura Cabina 1", "Cabina de pintura", TipoSeccion.PINTURA, 80.0, 4, "Nave B - Cabina 1"),
                ("SEC-PIN-02", "Pintura Cabina 2", "Cabina de pintura", TipoSeccion.PINTURA, 80.0, 4, "Nave B - Cabina 2"),
                ("SEC-PIN-03", "Pintura Cabina 3", "Cabina de pintura", TipoSeccion.PINTURA, 80.0, 4, "Nave B - Cabina 3"),
                # Mecanizado (3)
                ("SEC-MEC-01", "Mecanizado Celda 1", "Mecanizado CNC", TipoSeccion.OTRO, 60.0, 5, "Nave C - Celda 1"),
                ("SEC-MEC-02", "Mecanizado Celda 2", "Mecanizado CNC", TipoSeccion.OTRO, 60.0, 5, "Nave C - Celda 2"),
                ("SEC-MEC-03", "Mecanizado Celda 3", "Mecanizado CNC", TipoSeccion.OTRO, 60.0, 5, "Nave C - Celda 3"),
                # Embalaje (3)
                ("SEC-EMB-01", "Embalaje Mesa 1", "Mesa de embalaje", TipoSeccion.EMPAQUE, 120.0, 3, "Nave D - Mesa 1"),
                ("SEC-EMB-02", "Embalaje Mesa 2", "Mesa de embalaje", TipoSeccion.EMPAQUE, 120.0, 3, "Nave D - Mesa 2"),
                ("SEC-EMB-03", "Embalaje Mesa 3", "Mesa de embalaje", TipoSeccion.EMPAQUE, 120.0, 3, "Nave D - Mesa 3"),
            ]
            
            for codigo, nombre, desc, tipo, capacidad, operarios, ubicacion in sections_data:
                seccion = SeccionProduccion(
                    organization_id=1,
                    codigo=codigo,
                    nombre=nombre,
                    descripcion=desc,
                    tipo=tipo,
                    capacidad_diaria=capacidad,
                    capacidad_operarios=operarios,
                    supervisor_nombre=f"Jefe {nombre.split()[0]} {codigo.split('-')[1]}",
                    ubicacion=ubicacion,
                    activa=True
                )
                session.add(seccion)
            
            await session.commit()
            print(f"  ✓ {len(sections_data)} sections created")
        else:
            print(f"  ✓ {len(existing)} sections already exist")
    
    await engine.dispose()
    await master_engine.dispose()
    print("✓ Database setup complete!")

if __name__ == "__main__":
    asyncio.run(main())
