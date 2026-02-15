#!/usr/bin/env python3
"""
Inicializar campo estado_recepcion en compras existentes
Calcular cantidades esperadas y recibidas basado en datos existentes
"""

import asyncio
import os
from pathlib import Path
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from dario_app.modules.compras.models import Compra, CompraDetalle
from dario_app.modules.recepcion.models import Albaran, AlbaranDetalle


async def inicializar_estados_compras():
    """Inicializar estado_recepcion para todas las compras existentes en todas las BDs."""
    
    db_dir = Path("/home/dario/omni-solutions/products/erp/backend")
    
    # Buscar todas las BDs de organizaciones
    db_files = list(db_dir.glob("org_*.db")) + list(db_dir.glob("dario.db"))
    
    if not db_files:
        print("❌ No se encontraron archivos de BD")
        return
    
    print(f"📊 Encontradas {len(db_files)} BD(s)")
    
    for db_file in db_files:
        print(f"\n{'='*60}")
        print(f"🔄 Procesando: {db_file.name}")
        print(f"{'='*60}")
        
        try:
            # Conectar a BD específica
            engine = create_async_engine(
                f"sqlite+aiosqlite:///{db_file}",
                echo=False
            )
            
            async_session = sessionmaker(
                engine, class_=AsyncSession, expire_on_commit=False
            )
            
            async with async_session() as session:
                # Obtener todas las compras
                result = await session.execute(select(Compra))
                compras = result.scalars().all()
                
                if not compras:
                    print("  ℹ️  No hay compras en esta BD")
                    continue
                
                print(f"  📊 Total de compras: {len(compras)}")
                
                actualizadas = 0
                for compra in compras:
                    # Calcular cantidad esperada
                    result_esperado = await session.execute(
                        select(func.sum(CompraDetalle.cantidad)).where(
                            CompraDetalle.compra_id == compra.id
                        )
                    )
                    cantidad_esperada = result_esperado.scalar() or 0
                    
                    # Calcular cantidad recibida
                    result_recibido = await session.execute(
                        select(func.sum(AlbaranDetalle.cantidad_recibida)).where(
                            AlbaranDetalle.albaran_id.in_(
                                select(Albaran.id).where(Albaran.compra_id == compra.id)
                            )
                        )
                    )
                    cantidad_recibida = result_recibido.scalar() or 0
                    
                    # Determinar estado
                    if cantidad_recibida == 0:
                        estado = "no_recibida"
                    elif cantidad_recibida >= cantidad_esperada:
                        estado = "completa"
                    else:
                        estado = "parcial"
                    
                    # Solo actualizar si cambió
                    if (compra.estado_recepcion != estado or 
                        compra.cantidad_items_esperados != int(cantidad_esperada) or
                        compra.cantidad_items_recibidos != int(cantidad_recibida)):
                        
                        compra.cantidad_items_esperados = int(cantidad_esperada)
                        compra.cantidad_items_recibidos = int(cantidad_recibida)
                        compra.estado_recepcion = estado
                        actualizadas += 1
                        
                        print(f"  ✅ {compra.numero}: {estado} ({cantidad_recibida}/{cantidad_esperada})")
                
                # Guardar cambios
                if actualizadas > 0:
                    await session.commit()
                    print(f"\n  ✅ {actualizadas} compras actualizadas!")
                else:
                    print(f"  ℹ️  Todas las compras ya estaban inicializadas")
            
            await engine.dispose()
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            continue
    
    print(f"\n{'='*60}")
    print(f"✅ Inicialización completada!")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(inicializar_estados_compras())
