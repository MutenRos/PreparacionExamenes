#!/usr/bin/env python3
"""Create production workers (supervisores y operarios)."""

import asyncio
import sys
import bcrypt
from pathlib import Path

# Add src to path
sys.path.insert(0, '/home/dario/src')

async def main():
    from dario_app.database import get_tenant_engine, async_sessionmaker
    from dario_app.modules.usuarios.models import Usuario
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import select
    
    # Get tenant engine
    engine = get_tenant_engine(1)
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with session_maker() as session:
        # Check if data exists
        result = await session.execute(select(Usuario))
        existing = result.scalars().all()
        
        if len(existing) == 0:
            print(f"✓ Creating 87 production workers...")
            
            # Create 16 supervisores
            supervisores = [
                ("supervisor_ens_1", "supervisor1@empresa.com", "Supervisor Ensamblaje 1", "Juan", "García"),
                ("supervisor_ens_2", "supervisor2@empresa.com", "Supervisor Ensamblaje 2", "Carlos", "López"),
                ("supervisor_ens_3", "supervisor3@empresa.com", "Supervisor Ensamblaje 3", "María", "Rodríguez"),
                ("supervisor_ens_4", "supervisor4@empresa.com", "Supervisor Ensamblaje 4", "José", "Martínez"),
                ("supervisor_ens_5", "supervisor5@empresa.com", "Supervisor Ensamblaje 5", "Antonio", "Sánchez"),
                ("supervisor_ens_6", "supervisor6@empresa.com", "Supervisor Ensamblaje 6", "Francisco", "Pérez"),
                ("supervisor_ens_7", "supervisor7@empresa.com", "Supervisor Ensamblaje 7", "Pedro", "González"),
                ("supervisor_pin_1", "supervisor8@empresa.com", "Supervisor Pintura 1", "Luis", "Fernández"),
                ("supervisor_pin_2", "supervisor9@empresa.com", "Supervisor Pintura 2", "Miguel", "Díaz"),
                ("supervisor_pin_3", "supervisor10@empresa.com", "Supervisor Pintura 3", "Roberto", "Cruz"),
                ("supervisor_mec_1", "supervisor11@empresa.com", "Supervisor Mecanizado 1", "Javier", "Moreno"),
                ("supervisor_mec_2", "supervisor12@empresa.com", "Supervisor Mecanizado 2", "Andrés", "Ruiz"),
                ("supervisor_mec_3", "supervisor13@empresa.com", "Supervisor Mecanizado 3", "David", "Vargas"),
                ("supervisor_emb_1", "supervisor14@empresa.com", "Supervisor Embalaje 1", "Alfredo", "Salas"),
                ("supervisor_emb_2", "supervisor15@empresa.com", "Supervisor Embalaje 2", "Raúl", "Torres"),
                ("supervisor_emb_3", "supervisor16@empresa.com", "Supervisor Embalaje 3", "Eduardo", "Flores"),
            ]
            
            # Create 70 operarios
            operarios = []
            for i in range(1, 71):
                seccion_idx = (i - 1) % 16
                seccion_num = seccion_idx + 1
                operarios.append((
                    f"operario_{i:02d}",
                    f"operario{i}@empresa.com",
                    f"Operario {i}",
                    f"Nombre{i}",
                    f"Apellido{i}"
                ))
            
            all_users = supervisores + operarios
            pwd_hash = bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode()
            
            for username, email, nombre_completo, nombre, apellido in all_users:
                user = Usuario(
                    organization_id=1,
                    username=username,
                    email=email,
                    nombre_completo=nombre_completo,
                    nombre=nombre,
                    apellidos=apellido,
                    hashed_password=pwd_hash,
                    activo=True,
                    es_admin=False
                )
                session.add(user)
            
            await session.commit()
            print(f"  ✓ {len(supervisores)} supervisores created")
            print(f"  ✓ {len(operarios)} operarios created")
        else:
            print(f"  ✓ {len(existing)} users already exist")
    
    await engine.dispose()
    print("✓ Workers setup complete!")

if __name__ == "__main__":
    asyncio.run(main())
