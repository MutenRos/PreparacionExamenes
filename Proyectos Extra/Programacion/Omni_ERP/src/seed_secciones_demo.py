"""Seed demo data for secciones produccion."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Database URL - adjust if needed
DATABASE_URL = "postgresql://dario:darioelgoat123@localhost/tenant_omnicontrol_1"

def seed_secciones():
    """Seed demo production sections."""
    engine = create_engine(DATABASE_URL)
    
    with Session(engine) as session:
        try:
            # Check if table exists
            session.execute(text("SELECT 1 FROM secciones_produccion LIMIT 1"))
            
            # Clear existing demo data
            session.execute(text("DELETE FROM secciones_produccion WHERE codigo LIKE 'SEC-%'"))
            
            # Insert demo secciones
            secciones = [
                {
                    'org_id': 1,
                    'codigo': 'SEC-CORTE-01',
                    'nombre': 'Corte y Preparación',
                    'tipo': 'corte',
                    'capacidad': 50.0,
                    'operarios': 5,
                    'supervisor': 'Juan Pérez',
                    'ubicacion': 'Planta Baja - Área A'
                },
                {
                    'org_id': 1,
                    'codigo': 'SEC-ENSAM-01',
                    'nombre': 'Ensamblaje Principal',
                    'tipo': 'ensamblaje',
                    'capacidad': 30.0,
                    'operarios': 8,
                    'supervisor': 'María García',
                    'ubicacion': 'Planta 1 - Área B'
                },
                {
                    'org_id': 1,
                    'codigo': 'SEC-PINTU-01',
                    'nombre': 'Pintura y Acabados',
                    'tipo': 'pintura',
                    'capacidad': 40.0,
                    'operarios': 4,
                    'supervisor': 'Carlos López',
                    'ubicacion': 'Planta 1 - Área C'
                },
                {
                    'org_id': 1,
                    'codigo': 'SEC-CALID-01',
                    'nombre': 'Control de Calidad',
                    'tipo': 'control_calidad',
                    'capacidad': 60.0,
                    'operarios': 3,
                    'supervisor': 'Ana Martínez',
                    'ubicacion': 'Planta 2 - QC'
                }
            ]
            
            for sec in secciones:
                session.execute(text("""
                    INSERT INTO secciones_produccion 
                    (organization_id, codigo, nombre, tipo, capacidad_diaria, capacidad_operarios, supervisor_nombre, ubicacion, activa)
                    VALUES (:org_id, :codigo, :nombre, :tipo, :capacidad, :operarios, :supervisor, :ubicacion, true)
                    ON CONFLICT (codigo) DO UPDATE SET
                        nombre = EXCLUDED.nombre,
                        supervisor_nombre = EXCLUDED.supervisor_nombre,
                        activa = true
                """), sec)
            
            session.commit()
            print(f"✅ Successfully seeded {len(secciones)} production sections!")
            
            for sec in secciones:
                print(f"   - {sec['codigo']}: {sec['nombre']}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Make sure the secciones_produccion table exists and PostgreSQL is running.")
            session.rollback()

if __name__ == "__main__":
    seed_secciones()
