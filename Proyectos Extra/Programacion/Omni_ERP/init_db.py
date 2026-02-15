#!/usr/bin/env python3
"""
Initialize and seed the database with Bombas Omni demo data.
Run this once after deploying the application.
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / "src"))

from dario_app.database import create_tenant_db


async def main():
    """Initialize tenant database and seed data."""
    org_id = 1
    
    print("\n" + "="*70)
    print("  Initializing Bombas Omni Demo Database")
    print("="*70)
    
    # Step 1: Create tenant database
    print(f"\n1️⃣  Creating tenant database for organization {org_id}...")
    try:
        await create_tenant_db(org_id)
        print("   ✓ Database created successfully")
    except Exception as e:
        print(f"   ✗ Error creating database: {e}")
        return False
    
    # Step 2: Insert demo data
    print(f"\n2️⃣  Seeding database with Bombas Omni demo data...")
    try:
        import sqlite3
        from pathlib import Path
        
        db_path = Path(__file__).parent / "src/dario_app/data/org_dbs" / f"org_{org_id}.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check if already seeded
        cursor.execute("SELECT COUNT(*) FROM productos WHERE organization_id = 1")
        if cursor.fetchone()[0] > 0:
            print("   ℹ️  Database already seeded, skipping...")
            conn.close()
            return True
        
        now = datetime.utcnow().isoformat()
        
        # Insert proveedores
        proveedores = [
            ("Motores Industriales SA", "contacto@motores-industriales.mx", "+52 555 1234 5678", "Carlos Mendoza", "Av. Industrial 123, CDMX", "30 días", 7, "RFC: MIS-001"),
            ("Aceros y Metales Import", "ventas@aceros-metal.mx", "+52 555 2345 6789", "María González", "Blvd. Sur 456, Monterrey", "45 días", 10, "RFC: AMI-002"),
            ("Plásticos y Polímeros Ltd", "orden@plasticos-polimeros.mx", "+52 555 3456 7890", "Juan López", "Carretera Central 789, Puebla", "30 días", 5, "RFC: PPL-003"),
            ("Electrónica Profesional", "compras@electronica-pro.mx", "+52 555 4567 8901", "Roberto Sánchez", "Av. Tecnología 321, Guadalajara", "Net 30", 8, "RFC: ELP-004"),
            ("Componentes Hidráulicos", "sales@componentes-hidra.mx", "+52 555 5678 9012", "Alfredo García", "Parque Industrial 654, León", "60 días", 14, "RFC: CHI-005"),
            ("Pintura Industrial México", "ventas@pintura-industrial.mx", "+52 555 6789 0123", "Patricia Ruiz", "Zona Industrial 987, Querétaro", "Net 45", 6, "RFC: PIM-006"),
            ("Empaques y Logística", "logistica@empaques-log.mx", "+52 555 7890 1234", "Sofía Martínez", "Centro Logístico 246, Toluca", "Net 30", 3, "RFC: EYL-007"),
        ]
        
        for prov in proveedores:
            cursor.execute("""
                INSERT INTO proveedores 
                (organization_id, nombre, email, telefono, contacto_nombre, direccion, terminos_pago, dias_entrega_promedio, documento_proveedor, es_activo, creado_en, actualizado_en)
                VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
            """, (*prov, now, now))
        
        # Insert clientes
        clientes = [
            ("Hidroservicios del Norte", "Hidroservicios del Norte SA de CV", "HSN-001-0001", "empresa", "compras@hidroservicios-norte.mx", "+52 555 1000 1111", "Av. Agua 100", "Monterrey", "Nuevo León", "64000"),
            ("Sistemas de Riego Agrícola", "Sistemas de Riego Agrícola SA", "SRA-002-0002", "empresa", "ventas@riego-agricola.mx", "+52 555 2000 2222", "Carretera Federal 200", "Guanajuato", "Guanajuato", "36000"),
            ("Acuacultura México", "Acuacultura México SC", "ACM-003-0003", "empresa", "operaciones@acuacultura-mx.mx", "+52 555 3000 3333", "Puerto 300", "Veracruz", "Veracruz", "91700"),
            ("Constructoras y Proyectos", "Constructoras y Proyectos SA", "CYP-004-0004", "empresa", "adquisiciones@const-proyectos.mx", "+52 555 4000 4444", "Edificio 400", "CDMX", "CDMX", "01200"),
            ("Minería y Extracción", "Minería y Extracción Industrial", "MEI-005-0005", "empresa", "suministros@mineria-extraccion.mx", "+52 555 5000 5555", "Mina 500", "Zacatecas", "Zacatecas", "98000"),
            ("Industria Textil del Bajío", "Industria Textil del Bajío SA", "ITB-006-0006", "empresa", "compras@textil-bajio.mx", "+52 555 6000 6666", "Textile Park 600", "Aguascalientes", "Aguascalientes", "20000"),
            ("Generación de Energía Verde", "Generación de Energía Verde SA", "GEV-007-0007", "empresa", "proyectos@energia-verde.mx", "+52 555 7000 7777", "Solar Farm 700", "Durango", "Durango", "34000"),
            ("Distribuidora Integral Técnica", "Distribuidora Integral Técnica", "DIT-008-0008", "empresa", "mayorista@dist-integral.mx", "+52 555 8000 8888", "Zona Comercial 800", "Guadalajara", "Jalisco", "44100"),
        ]
        
        for cliente in clientes:
            cursor.execute("""
                INSERT INTO clientes 
                (organization_id, nombre, razon_social, nif_nie, nif_valido, tipo_cliente, email, telefono, domicilio, municipio, provincia, codigo_postal, puntos_lealtad, nivel_lealtad, total_compras, activo, creado_en, actualizado_en)
                VALUES (1, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?, ?, 0, 'Plata', 0, 1, ?, ?)
            """, (*cliente, now, now))
        
        # Insert productos
        productos = [
            ("BC-100-001", "PUMP-BC100-2024", "Bomba Centrífuga BC-100", "Bomba centrífuga de 1 HP, flujo 50 L/min, presión 2 bar", "Bombas - Acabadas", 450.00, 720.00, 20, 15, 5, 1),
            ("BS-200-001", "PUMP-BS200-2024", "Bomba Sumergible BS-200", "Bomba sumergible 2 HP, profundidad 50m, caudal 80 L/min", "Bombas - Acabadas", 680.00, 1100.00, 20, 12, 4, 1),
            ("BA-150-001", "PUMP-BA150-2024", "Bomba Axial BA-150", "Bomba axial 1.5 HP, caudal 120 L/min, para sistemas de refrigeración", "Bombas - Acabadas", 520.00, 850.00, 20, 8, 3, 1),
            ("BD-300-001", "PUMP-BD300-2024", "Bomba Diafragma BD-300", "Bomba diafragma 3 HP, caudal variable 200 L/min, baja vibración", "Bombas - Acabadas", 890.00, 1450.00, 20, 6, 2, 1),
            ("BP-180-001", "PUMP-BP180-2024", "Bomba Periférica BP-180", "Bomba periférica 2.5 HP, caudal 100 L/min, para pequeños sistemas", "Bombas - Acabadas", 620.00, 1000.00, 20, 10, 3, 1),
            ("BI-500-001", "PUMP-BI500-2024", "Bomba Industrial BI-500", "Bomba industrial de gran caudal, 5 HP, 300 L/min, aplicaciones pesadas", "Bombas - Acabadas", 1250.00, 2000.00, 20, 4, 1, 1),
            ("MOT-1HP-001", "MOTOR-1HP-IE3", "Motor Eléctrico 1 HP IE3", "Motor 1 HP 3 fases, 1700 RPM, eficiencia IE3", "Motores", 280.00, 450.00, 20, 25, 10, 0),
            ("MOT-2HP-001", "MOTOR-2HP-IE3", "Motor Eléctrico 2 HP IE3", "Motor 2 HP 3 fases, 1700 RPM, eficiencia IE3", "Motores", 420.00, 680.00, 20, 18, 8, 0),
            ("MOT-3HP-001", "MOTOR-3HP-IE3", "Motor Eléctrico 3 HP IE3", "Motor 3 HP 3 fases, 1700 RPM, eficiencia IE3", "Motores", 580.00, 950.00, 20, 12, 5, 0),
            ("MOT-5HP-001", "MOTOR-5HP-IE3", "Motor Eléctrico 5 HP IE3", "Motor 5 HP 3 fases, 1700 RPM, eficiencia IE3", "Motores", 890.00, 1450.00, 20, 8, 3, 0),
            ("CHASS-STD-001", "CHASSIS-STANDARD", "Chasis Estándar Acero", "Chasis de acero inoxidable para montaje de bombas", "Componentes", 95.00, 150.00, 1, 50, 20, 0),
            ("MANG-PVC-001", "HOSE-PVC-FLEX", "Manguito PVC Flexible", "Manguito de PVC flexible 5m para conexiones", "Componentes", 35.00, 55.00, 1, 120, 50, 0),
            ("HELM-ACERO-001", "IMPELLER-STEEL", "Hélice Acero Inoxidable", "Hélice de acero inoxidable 6 aspas para centrifugas", "Componentes", 120.00, 200.00, 1, 40, 15, 0),
            ("SELLO-MECA-001", "SEAL-MECHANICAL", "Sello Mecánico", "Sello mecánico para eje de bombas centrifugas", "Componentes", 45.00, 75.00, 1, 80, 30, 0),
            ("RODAMIENTOS-1-001", "BEARING-6206", "Rodamiento 6206", "Rodamiento de bola serie 6206", "Componentes", 28.00, 45.00, 1, 200, 80, 0),
            ("KIT-MANTEN-001", "KIT-MAINTENANCE", "Kit Mantenimiento Anual", "Kit completo de mantenimiento anual para bombas", "Servicios", 150.00, 250.00, 1, 30, 10, 1),
            ("INST-PROFESIONAL", "SERVICE-INSTALL", "Instalación Profesional", "Servicio de instalación profesional en sitio", "Servicios", 0.00, 500.00, 1, 999, 0, 1),
        ]
        
        for prod in productos:
            cursor.execute("""
                INSERT INTO productos 
                (organization_id, codigo, sku, nombre, descripcion, categoria, precio_compra, precio_venta, margen_porcentaje, stock_actual, stock_minimo, unidad_medida, activo, visible_en_pos, creado_en, actualizado_en)
                VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'unidad', 1, ?, ?, ?)
            """, (*prod, now, now))
        
        conn.commit()
        conn.close()
        
        print(f"   ✓ {len(proveedores)} suppliers inserted")
        print(f"   ✓ {len(clientes)} customers inserted")
        print(f"   ✓ {len(productos)} products inserted")
        
    except Exception as e:
        print(f"   ✗ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*70)
    print("  ✅ Database initialization completed successfully!")
    print("="*70)
    print("\nAPI endpoints available:")
    print("  - GET /api/demo/productos")
    print("  - GET /api/demo/proveedores")
    print("  - GET /api/demo/clientes")
    print("  - GET /api/demo/stats")
    print()
    
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
