#!/usr/bin/env python
"""Script para crear una cuenta de prueba con plan básico y venta registrada."""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from dario_app.core.config import settings
from dario_app.modules.auth.utils import get_password_hash
from dario_app.modules.clientes.models import Cliente
from dario_app.modules.pos.models import VentaPOS, VentaPOSDetalle
from dario_app.modules.tenants.models import Organization
from dario_app.modules.usuarios.models import Usuario


async def main():
    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///"), echo=False
    )

    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as db:
        # Check if test account already exists
        result = await db.execute(
            select(Organization).where(Organization.nombre == "Test Plan Básico")
        )
        existing = result.scalar_one_or_none()

        if existing:
            print("❌ La cuenta de prueba ya existe")
            await engine.dispose()
            return

        # Create organization with basic plan
        org = Organization(
            nombre="Test Plan Básico",
            plan="basic",
            estado="active",
            limite_usuarios=1,
            limite_productos=500,
            limite_sucursales=1,
        )
        db.add(org)
        await db.flush()

        # Create user for the organization
        user = Usuario(
            organization_id=org.id,
            email="test.basico@tiendaretail.com",
            nombre_completo="Test Usuario",
            hashed_password=get_password_hash("test123"),
            rol="admin",
            estado="active",
        )
        db.add(user)
        await db.flush()

        print(f"✅ Organización creada: {org.nombre} (ID: {org.id})")
        print(f"✅ Usuario creado: {user.email}")

        # Register customer in admin organization (org_id=1)
        admin_org = await db.execute(select(Organization).where(Organization.id == 1))
        admin_org = admin_org.scalar_one_or_none()

        if admin_org:
            # Create customer in admin organization
            cliente = Cliente(
                organization_id=1,
                nombre="Test Usuario",
                email="test.basico@tiendaretail.com",
                tipo_documento="DNI",
                notas=f"Cliente registrado desde script - Plan: BASIC - Org: {org.nombre}",
            )
            db.add(cliente)
            await db.flush()

            print(f"✅ Cliente creado en admin: {cliente.nombre}")

            # Create sale for basic plan ($29)
            precio = 29.00
            subtotal = Decimal(str(precio))
            impuesto = subtotal * Decimal("0.18")  # 18% tax
            total = subtotal + impuesto

            # Generate transaction number
            result = await db.execute(select(VentaPOS).where(VentaPOS.organization_id == 1))
            ventas_count = len(result.scalars().all())
            numero = f"SUBS-{datetime.now().strftime('%Y%m%d')}-{ventas_count + 1:04d}"

            venta_pos = VentaPOS(
                organization_id=1,
                numero=numero,
                cliente_id=cliente.id,
                subtotal=float(subtotal),
                descuento=0.00,
                impuesto=float(impuesto),
                total=float(total),
                metodo_pago="online",
                monto_pagado=float(total),
                cambio=0.00,
                estado="completada",
                notas=f"Suscripción Plan BASIC - Organización: {org.nombre}",
            )
            db.add(venta_pos)
            await db.flush()

            # Create detail line
            detalle = VentaPOSDetalle(
                venta_id=venta_pos.id,
                producto_id=None,
                cantidad=1,
                precio_unitario=float(precio),
                descuento=0.00,
                subtotal=float(precio),
                organization_id=1,
            )
            db.add(detalle)

            # Update customer loyalty
            cliente.puntos_lealtad = 29
            cliente.total_compras = subtotal
            cliente.nivel_lealtad = "Bronce"

            await db.commit()

            print(f"✅ Venta registrada: {numero}")
            print(f"   - Total: ${total:.2f} (Subtotal: ${subtotal:.2f} + IVA: ${impuesto:.2f})")
            print("   - Puntos lealtad: 29")
            print("   - Nivel: Bronce")

        print("\n" + "=" * 60)
        print("✨ CREDENCIALES DE PRUEBA:")
        print("=" * 60)
        print("Email:    test.basico@tiendaretail.com")
        print("Password: test123")
        print("Plan:     BASIC ($29/mes)")
        print("=" * 60)
        print("\n📊 Accede a tu panel admin para ver:")
        print("   • Cliente: http://localhost:5000/app/clientes")
        print("   • Venta:   http://localhost:5000/app/pos (ver transacción)")
        print("   • Reportes: http://localhost:5000/app/reportes")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
