"""Add secciones_produccion table and update ordenes_produccion workflow."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from dario_app.config import settings

def run_migration():
    """Run the migration to add secciones_produccion and update workflow."""
    engine = create_engine(str(settings.DATABASE_URL))
    
    with engine.connect() as conn:
        # Create secciones_produccion table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS secciones_produccion (
                id SERIAL PRIMARY KEY,
                organization_id INTEGER NOT NULL,
                codigo VARCHAR(50) UNIQUE NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                tipo VARCHAR(50) DEFAULT 'otro',
                capacidad_diaria FLOAT,
                capacidad_operarios INTEGER,
                supervisor_id INTEGER REFERENCES usuarios(id),
                supervisor_nombre VARCHAR(100),
                activa BOOLEAN DEFAULT TRUE,
                ubicacion VARCHAR(200),
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_modificacion TIMESTAMP,
                notas TEXT
            );
        """))
        
        # Create indexes
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_secciones_org 
            ON secciones_produccion(organization_id);
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_secciones_codigo 
            ON secciones_produccion(codigo);
        """))
        
        # Add new columns to ordenes_produccion
        try:
            conn.execute(text("""
                ALTER TABLE ordenes_produccion 
                ADD COLUMN IF NOT EXISTS seccion_produccion_id INTEGER 
                REFERENCES secciones_produccion(id);
            """))
        except Exception as e:
            print(f"Column seccion_produccion_id might already exist: {e}")
        
        try:
            conn.execute(text("""
                ALTER TABLE ordenes_produccion 
                ADD COLUMN IF NOT EXISTS fecha_asignacion TIMESTAMP;
            """))
        except Exception as e:
            print(f"Column fecha_asignacion might already exist: {e}")
        
        try:
            conn.execute(text("""
                ALTER TABLE ordenes_produccion 
                ADD COLUMN IF NOT EXISTS fecha_aceptacion TIMESTAMP;
            """))
        except Exception as e:
            print(f"Column fecha_aceptacion might already exist: {e}")
        
        # Create index on foreign key
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_ordenes_seccion 
            ON ordenes_produccion(seccion_produccion_id);
        """))
        
        conn.commit()
        print("✅ Migration completed successfully!")
        print("   - Created secciones_produccion table")
        print("   - Added workflow columns to ordenes_produccion")
        print("   - Created indexes")

if __name__ == "__main__":
    run_migration()
