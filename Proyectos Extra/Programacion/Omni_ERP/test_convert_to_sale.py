#!/usr/bin/env python3
"""
Test suite para la conversión de Proyectos a Ventas (Cotizaciones)
Valida el flujo completo: crear proyecto → agregar tareas → convertir a venta
"""

import asyncio
import httpx
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"
ADMIN_TOKEN = None  # Se obtendrá dinámicamente
ORG_ID = None

async def test_convert_project_to_sale():
    """Test completo de conversión de proyecto a venta"""
    
    async with httpx.AsyncClient() as client:
        print("=" * 70)
        print("TEST: CONVERSIÓN DE PROYECTO A VENTA")
        print("=" * 70)
        
        # 1. OBTENER TOKEN (login como admin)
        print("\n1️⃣  Obteniendo token de autenticación...")
        try:
            login_response = await client.post(
                f"{BASE_URL}/api/auth/login",
                json={"username": "admin", "password": "admin123"}
            )
            if login_response.status_code != 200:
                print(f"❌ No se pudo autenticar: {login_response.text}")
                return
            
            auth_data = login_response.json()
            token = auth_data.get("access_token")
            org_id = auth_data.get("organization_id", 1)
            print(f"✅ Autenticado. Token: {token[:20]}... | Org: {org_id}")
        except Exception as e:
            print(f"❌ Error en autenticación: {e}")
            return
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # 2. CREAR PROYECTO
        print("\n2️⃣  Creando proyecto...")
        project_data = {
            "project_code": f"TEST-{datetime.now().strftime('%H%M%S')}",
            "name": "Proyecto Test - Conversión a Venta",
            "customer_name": "Cliente Test S.L.",
            "budget_amount": 15000.00,
            "status": "draft",
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        try:
            project_response = await client.post(
                f"{BASE_URL}/api/project-ops/projects",
                json=project_data,
                headers=headers
            )
            if project_response.status_code != 200:
                print(f"❌ Error creando proyecto: {project_response.text}")
                return
            
            project = project_response.json()
            project_id = project.get("id")
            print(f"✅ Proyecto creado: ID={project_id} | Código={project.get('project_code')}")
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        # 3. AGREGAR TAREAS AL PROYECTO
        print("\n3️⃣  Agregando tareas al proyecto...")
        tasks = []
        task_names = ["Análisis de requisitos", "Diseño técnico", "Desarrollo", "Testing"]
        
        for task_name in task_names:
            task_data = {
                "name": task_name,
                "descripcion": f"Tarea: {task_name}",
                "planned_hours": 40,
                "start_date": datetime.now().isoformat(),
                "end_date": (datetime.now() + timedelta(days=7)).isoformat()
            }
            
            try:
                task_response = await client.post(
                    f"{BASE_URL}/api/project-ops/projects/{project_id}/tasks",
                    json=task_data,
                    headers=headers
                )
                if task_response.status_code == 200:
                    task = task_response.json()
                    tasks.append(task)
                    print(f"  ✅ Tarea creada: {task_name} (ID={task.get('id')})")
                else:
                    print(f"  ❌ Error creando tarea: {task_response.text}")
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        print(f"📊 Total de tareas creadas: {len(tasks)}")
        
        # 4. CONVERTIR PROYECTO A VENTA
        print("\n4️⃣  Convertiendo proyecto a venta...")
        try:
            convert_response = await client.post(
                f"{BASE_URL}/api/project-ops/projects/{project_id}/convert-to-sale",
                headers=headers
            )
            
            if convert_response.status_code == 200:
                result = convert_response.json()
                print(f"✅ Conversión exitosa!")
                print(f"   📄 Cotización creada:")
                print(f"      - ID: {result.get('quote_id')}")
                print(f"      - Número: {result.get('quote_number')}")
                print(f"      - Cliente: {result.get('quote', {}).get('customer')}")
                print(f"      - Total: €{result.get('quote', {}).get('total', 0):.2f}")
                print(f"      - Ítems: {result.get('quote', {}).get('items_count', 0)}")
                print(f"\n   Mensaje: {result.get('message')}")
            else:
                print(f"❌ Error en conversión: {convert_response.status_code}")
                print(f"   Respuesta: {convert_response.text}")
                return
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        # 5. VALIDAR PROYECTO CONVERTIDO
        print("\n5️⃣  Validando proyecto convertido...")
        try:
            validate_response = await client.get(
                f"{BASE_URL}/api/project-ops/projects/{project_id}",
                headers=headers
            )
            
            if validate_response.status_code == 200:
                updated_project = validate_response.json()
                print(f"✅ Proyecto actualizado:")
                print(f"   - Status: {updated_project.get('status')}")
                print(f"   - Venta ID: {updated_project.get('converted_to_sale_id')}")
                print(f"   - Venta Número: {updated_project.get('converted_to_sale_number')}")
                
                # Validar status
                if updated_project.get('status') == 'converted_to_sale':
                    print("   ✅ Status correcto: converted_to_sale")
                else:
                    print(f"   ⚠️  Status inesperado: {updated_project.get('status')}")
            else:
                print(f"❌ Error validando: {validate_response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # 6. INTENTAR CONVERTIR NUEVAMENTE (debe fallar)
        print("\n6️⃣  Intentando convertir nuevamente (debe fallar)...")
        try:
            retry_response = await client.post(
                f"{BASE_URL}/api/project-ops/projects/{project_id}/convert-to-sale",
                headers=headers
            )
            
            if retry_response.status_code != 200:
                error_msg = retry_response.json().get('detail', 'Error desconocido')
                print(f"✅ Fallo esperado: {error_msg}")
            else:
                print(f"⚠️  Conversión inesperada fue exitosa")
        except Exception as e:
            print(f"ℹ️  Error (esperado): {e}")
        
        print("\n" + "=" * 70)
        print("TEST COMPLETADO ✅")
        print("=" * 70)


async def test_error_cases():
    """Test de casos de error"""
    
    async with httpx.AsyncClient() as client:
        print("\n" + "=" * 70)
        print("TEST: CASOS DE ERROR")
        print("=" * 70)
        
        # Obtener token
        login_response = await client.post(
            f"{BASE_URL}/api/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test 1: Proyecto no existente
        print("\n1️⃣  Intentando convertir proyecto inexistente...")
        response = await client.post(
            f"{BASE_URL}/api/project-ops/projects/99999/convert-to-sale",
            headers=headers
        )
        if response.status_code != 200:
            print(f"✅ Error esperado: {response.status_code}")
        else:
            print(f"⚠️  No hubo error: {response.text}")
        
        # Test 2: Crear proyecto cancelado e intentar convertir
        print("\n2️⃣  Creando proyecto cancelado e intentando convertir...")
        project_data = {
            "project_code": f"CANCEL-{datetime.now().strftime('%H%M%S')}",
            "name": "Proyecto Cancelado",
            "budget_amount": 5000.00,
            "status": "canceled"
        }
        
        create_response = await client.post(
            f"{BASE_URL}/api/project-ops/projects",
            json=project_data,
            headers=headers
        )
        
        if create_response.status_code == 200:
            canceled_project_id = create_response.json().get("id")
            
            convert_response = await client.post(
                f"{BASE_URL}/api/project-ops/projects/{canceled_project_id}/convert-to-sale",
                headers=headers
            )
            
            if convert_response.status_code != 200:
                error_msg = convert_response.json().get('detail', '')
                print(f"✅ Error esperado: {error_msg}")
            else:
                print(f"⚠️  No debería permitir conversión de proyecto cancelado")
        
        print("\n" + "=" * 70)
        print("TEST DE ERRORES COMPLETADO ✅")
        print("=" * 70)


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║           SUITE DE TESTS: CONVERSIÓN PROYECTO → VENTA               ║
╚══════════════════════════════════════════════════════════════════════╝

Este script prueba la funcionalidad de convertir proyectos en cotizaciones
de venta, validando:

✓ Creación de proyecto
✓ Agregación de tareas
✓ Conversión a venta exitosa
✓ Actualización de status del proyecto
✓ Casos de error (proyecto cancelado, etc.)

Prerequisitos:
- Servidor OmniERP corriendo en localhost:8000
- Usuario admin con contraseña admin123
""")
    
    # Ejecutar tests
    asyncio.run(test_convert_project_to_sale())
    asyncio.run(test_error_cases())
