#!/usr/bin/env python3
"""
Example: Complete workflow for purchase order reception and logistics.

This script demonstrates how to use the new reception system:
1. Create a receipt (albarán) for a purchase order
2. System automatically creates logistics movements
3. Assign warehouse workers
4. Mark movements as completed
5. Reconcile with external invoice
"""

import asyncio
import httpx
from decimal import Decimal

# Configuration
BASE_URL = "http://localhost:8001"
ORG_ID = 1
ADMIN_TOKEN = "your_jwt_token_here"  # Replace with actual token

headers = {
    "Authorization": f"Bearer {ADMIN_TOKEN}",
    "Content-Type": "application/json",
}


async def example_complete_workflow():
    """
    Example: Recepción de compra con distribución automática.
    
    Scenario:
    - Purchase order 123 with 100 units of Product A
    - There's an active production order needing 60 units
    - Remaining 40 units go to main storage
    """
    
    async with httpx.AsyncClient() as client:
        print("=" * 70)
        print("📦 SISTEMA DE RECEPCIÓN - EJEMPLO COMPLETO")
        print("=" * 70)
        
        # Step 1: Create receipt for purchase order
        print("\n1️⃣ Creando albarán de recepción...\n")
        
        receipt_payload = {
            "compra_id": 123,
            "items_recibidos": [
                {
                    "compra_detalle_id": 45,
                    "cantidad_recibida": 100,
                    "lotes_recibidos": "LOT-2025-001",
                    "fechas_vencimiento": "2026-12-31",
                    "notas": "Inspección de calidad OK"
                }
            ],
            "usuario_id": 1,
            "notas": "Recepción sin incidencias"
        }
        
        response = await client.post(
            f"{BASE_URL}/api/recepcion/albaranes",
            json=receipt_payload,
            headers=headers,
        )
        
        if response.status_code == 201:
            receipt_data = response.json()
            albaran_id = receipt_data["id"]
            print(f"✅ Albarán creado: {receipt_data['numero']}")
            print(f"   Estado: {receipt_data['estado']}")
            print(f"   Items recibidos: {receipt_data['items_recibidos']}/{receipt_data['total_items']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return
        
        # Step 2: Get logistics movements created automatically
        print("\n2️⃣ Consultando movimientos logísticos creados automáticamente...\n")
        
        response = await client.get(
            f"{BASE_URL}/api/recepcion/movimientos?estado=pendiente",
            headers=headers,
        )
        
        if response.status_code == 200:
            movements_data = response.json()
            print(f"✅ Movimientos encontrados: {movements_data['total']}")
            
            for mov in movements_data["movimientos"]:
                print(f"\n   📍 {mov['numero']}")
                print(f"      Producto: ID {mov['producto_id']}")
                print(f"      Cantidad: {mov['cantidad']}")
                print(f"      Origen: {mov['ubicacion_origen']}")
                print(f"      Destino: {mov['ubicacion_destino']}")
                if mov["orden_produccion_id"]:
                    print(f"      Orden Producción: OP-{mov['orden_produccion_id']}")
                print(f"      Estado: {mov['estado']}")
                print(f"      Carretillero: {'No asignado' if not mov['carretillero_id'] else f'ID {mov['carretillero_id']}'}")
        else:
            print(f"❌ Error: {response.status_code}")
            return
        
        # Step 3: Assign warehouse workers (if movements exist)
        print("\n3️⃣ Asignando carretilleros a movimientos...\n")
        
        # Assuming we have at least 2 movements from Step 2
        if movements_data["movimientos"]:
            for idx, mov in enumerate(movements_data["movimientos"][:2]):
                movement_id = mov["id"]
                # Assign different workers
                carretillero_id = 7 if idx == 0 else 8
                
                response = await client.post(
                    f"{BASE_URL}/api/recepcion/movimientos/{movement_id}/asignar-carretillero",
                    json={"carretillero_id": carretillero_id},
                    headers=headers,
                )
                
                if response.status_code == 200:
                    mov_data = response.json()
                    print(f"✅ {mov_data['numero']}: Asignado a carretillero {carretillero_id}")
                    print(f"   Estado: {mov_data['estado']}")
                else:
                    print(f"❌ Error asignando {movement_id}: {response.status_code}")
        
        # Step 4: Mark movements as completed
        print("\n4️⃣ Completando movimientos...\n")
        
        if movements_data["movimientos"]:
            for mov in movements_data["movimientos"][:2]:
                movement_id = mov["id"]
                
                response = await client.post(
                    f"{BASE_URL}/api/recepcion/movimientos/{movement_id}/completar",
                    headers=headers,
                )
                
                if response.status_code == 200:
                    mov_data = response.json()
                    print(f"✅ {mov_data['numero']}: Completado")
                    print(f"   Destino final: {mov_data['ubicacion_destino']}")
                else:
                    print(f"❌ Error completando: {response.status_code}")
        
        # Step 5: Reconcile with external invoice
        print("\n5️⃣ Reconciliando con factura externa...\n")
        
        invoice_payload = {
            "numero_factura": "FAC-PROV-2025-001234",
            "monto_factura": Decimal("5000.00")
        }
        
        response = await client.post(
            f"{BASE_URL}/api/recepcion/albaranes/{albaran_id}/reconciliar-factura",
            json=invoice_payload,
            headers=headers,
        )
        
        if response.status_code == 200:
            receipt_data = response.json()
            print(f"✅ Albarán reconciliado")
            print(f"   Número de factura: {invoice_payload['numero_factura']}")
            print(f"   Estado: {receipt_data['estado']}")
        else:
            print(f"❌ Error reconciliando: {response.status_code}")
        
        # Step 6: Get pending movements
        print("\n6️⃣ Consultando movimientos pendientes de asignación...\n")
        
        response = await client.get(
            f"{BASE_URL}/api/recepcion/reportes/pendientes-asignacion",
            headers=headers,
        )
        
        if response.status_code == 200:
            pending_data = response.json()
            print(f"✅ Movimientos sin asignar: {pending_data['total']}")
            if pending_data["movimientos"]:
                for mov in pending_data["movimientos"][:3]:
                    print(f"   • {mov['numero']}: {mov['cantidad']} unidades → {mov['ubicacion_destino']}")
            else:
                print("   (No hay movimientos pendientes)")
        else:
            print(f"❌ Error: {response.status_code}")
        
        print("\n" + "=" * 70)
        print("✨ Flujo completo ejecutado exitosamente!")
        print("=" * 70)


async def example_partial_receipt():
    """
    Example: Partial reception of purchase order.
    
    Scenario:
    - Purchase order 456 with 100 units expected
    - We receive only 60 units (partial)
    - System still creates movements for what we got
    """
    
    async with httpx.AsyncClient() as client:
        print("\n\n" + "=" * 70)
        print("📦 EJEMPLO: RECEPCIÓN PARCIAL")
        print("=" * 70)
        
        print("\n1️⃣ Recibiendo 60 de 100 unidades esperadas...\n")
        
        receipt_payload = {
            "compra_id": 456,
            "items_recibidos": [
                {
                    "compra_detalle_id": 99,
                    "cantidad_recibida": 60,  # Less than ordered
                    "lotes_recibidos": "LOT-2025-002",
                    "fechas_vencimiento": "2026-06-15",
                    "notas": "40 unidades llegaran en segundo envio"
                }
            ],
            "usuario_id": 1,
            "notas": "Recepción parcial - Falta segundo envio"
        }
        
        response = await client.post(
            f"{BASE_URL}/api/recepcion/albaranes",
            json=receipt_payload,
            headers=headers,
        )
        
        if response.status_code == 201:
            receipt_data = response.json()
            print(f"✅ Albarán creado: {receipt_data['numero']}")
            print(f"   Estado: {receipt_data['estado']}")
            print(f"   Items recibidos: {receipt_data['items_recibidos']}/{receipt_data['total_items']}")
            print(f"\n   ⚠️ Cantidad diferencia: 40 unidades (aún no llegadas)")
        else:
            print(f"❌ Error: {response.status_code}")
        
        print("\n" + "=" * 70)


async def main():
    """Run all examples."""
    try:
        await example_complete_workflow()
        await example_partial_receipt()
    except Exception as e:
        print(f"\n❌ Error ejecutando ejemplos: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║  🚀 EJEMPLOS DEL SISTEMA DE RECEPCIÓN Y LOGÍSTICA INTERNA         ║
    ║                                                                    ║
    ║  Requisitos:                                                       ║
    ║  - Servidor OmniERP ejecutándose en http://localhost:8001         ║
    ║  - JWT token válido (admin)                                        ║
    ║  - Al menos una compra en la BD (ID 123, 456)                     ║
    ║                                                                    ║
    ║  Nota: Reemplaza 'your_jwt_token_here' con un token real          ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)
    
    asyncio.run(main())
