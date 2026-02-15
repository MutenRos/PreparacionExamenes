#!/usr/bin/env python3
"""
Script para crear una cuenta de prueba con plan básico
y registrarla como cliente y venta en el admin.
"""
import asyncio
import os
import sys
from pathlib import Path

# Add src directory to path
src_path = str(Path(__file__).parent.parent / "src")
sys.path.insert(0, src_path)
os.chdir(src_path)

from datetime import datetime
from decimal import Decimal

import bcrypt

from dario_app.database import async_session_maker
from dario_app.modules.clientes.models import Cliente
from dario_app.modules.pos.models import VentaPOS, VentaPOSDetalle
from dario_app.modules.tenants.models import Organization
from dario_app.modules.usuarios.models import Usuario


async def crear_cuenta_prueba():
    async with async_session_maker() as db:
        try:
            # 1. Crear organización con plan básico
            org = Organization(
                nombre="Tienda La Esperanza",
                email="maria@laesperanza.com",
                telefono="+51987654321",
                direccion="Av. Principal 456, Lima",
                plan="basic",
                estado="active",
            )
            db.add(org)
            await db.flush()

            print(f"✅ Organización creada: {org.nombre} (ID: {org.id})")

            # 2. Crear usuario administrador de la organización
            password_bytes = "maria123".encode("utf-8")
            hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

            usuario = Usuario(
                organization_id=org.id,
                nombre_completo="María González",
                email="maria@laesperanza.com",
                hashed_password=hashed_password,
                rol="admin",
                activo=True,
            )
            db.add(usuario)
            await db.flush()

            print(f"✅ Usuario creado: {usuario.nombre_completo}")

            # 3. Crear cliente en la organización ADMIN (org_id=1)
            ADMIN_ORG_ID = 1
            cliente = Cliente(
                organization_id=ADMIN_ORG_ID,
                nombre="María González",
                email="maria@laesperanza.com",
                telefono="+51987654321",
                direccion="Av. Principal 456, Lima",
                tipo_documento="DNI",
                numero_documento="12345678",
                notas=f"Cliente registrado desde web - Plan: BASIC - Org: {org.nombre}",
            )
            db.add(cliente)
            await db.flush()

            print(f"✅ Cliente creado en admin (ID: {cliente.id})")

            # 4. Crear venta por el plan básico ($29)
            precio_plan = 29.00
            subtotal = Decimal(str(precio_plan))
            impuesto = subtotal * Decimal("0.18")
            total = subtotal + impuesto

            # Generar número de transacción
            numero = f"SUBS-{datetime.now().strftime('%Y%m%d')}-0001"

            venta_pos = VentaPOS(
                organization_id=ADMIN_ORG_ID,
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

            print(f"✅ Venta creada: {venta_pos.numero} - Total: S/ {total:.2f}")

            # 5. Crear detalle de venta
            detalle = VentaPOSDetalle(
                venta_id=venta_pos.id,
                producto_id=None,  # Es un servicio, no producto físico
                cantidad=1,
                precio_unitario=float(precio_plan),
                descuento=0.00,
                subtotal=float(precio_plan),
                organization_id=ADMIN_ORG_ID,
            )
            db.add(detalle)

            # 6. Actualizar puntos de lealtad del cliente
            cliente.puntos_lealtad = int(precio_plan)  # 29 puntos
            cliente.total_compras = subtotal
            cliente.nivel_lealtad = "Bronce"

            await db.commit()

            print("\n" + "=" * 70)
            print("✅ CUENTA DE PRUEBA CREADA EXITOSAMENTE")
            print("=" * 70)
            print("\n📋 DATOS DE LA CUENTA:")
            print(f"   Organización: {org.nombre}")
            print(f"   Plan:         {org.plan.upper()}")
            print(f"   Email:        {usuario.email}")
            print("   Password:     maria123")
            print(f"   Estado:       {org.estado}")

            print("\n💰 VENTA REGISTRADA EN ADMIN:")
            print(f"   Número:       {venta_pos.numero}")
            print(f"   Cliente:      {cliente.nombre}")
            print("   Plan:         Basic ($29.00)")
            print(f"   Subtotal:     S/ {subtotal:.2f}")
            print(f"   Impuesto:     S/ {impuesto:.2f}")
            print(f"   Total:        S/ {total:.2f}")
            print(f"   Estado:       {venta_pos.estado}")

            print("\n👤 CLIENTE EN ADMIN:")
            print(f"   Nombre:       {cliente.nombre}")
            print(f"   Email:        {cliente.email}")
            print(f"   Puntos:       {cliente.puntos_lealtad}")
            print(f"   Nivel:        {cliente.nivel_lealtad}")
            print(f"   Total compras: S/ {cliente.total_compras:.2f}")

            print("\n🔗 VERIFICAR EN ADMIN:")
            print("   1. Login admin: http://localhost:5000/app/login")
            print("      Email:    admin@erpdario.com")
            print("      Password: admin123")
            print("   2. Ver cliente: http://localhost:5000/app/clientes")
            print("   3. Ver venta:   http://localhost:5000/app/pos")

            print("\n🔑 ACCESO CUENTA CLIENTE:")
            print("   Login: http://localhost:5000/app/login")
            print("   Email:    maria@laesperanza.com")
            print("   Password: maria123")
            print("=" * 70)

        except Exception as e:
            await db.rollback()
            print(f"\n❌ Error: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(crear_cuenta_prueba())
