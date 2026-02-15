#!/usr/bin/env python3
"""Quick setup of production database using direct SQLite."""

import sqlite3
import bcrypt
from pathlib import Path

db_path = Path('/home/dario/src/data/org_dbs/org_1.db')
db_path.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

try:
    # Create organizations table
    print("✓ Creating organizations table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO organizations (id, nombre) VALUES (1, 'Default Organization')")
    
    # Create secciones_produccion table
    print("✓ Creating secciones_produccion table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secciones_produccion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            codigo TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            tipo TEXT,
            capacidad_diaria REAL,
            capacidad_operarios INTEGER,
            supervisor_id INTEGER,
            supervisor_nombre TEXT,
            activa BOOLEAN DEFAULT 1,
            ubicacion TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_modificacion TIMESTAMP,
            notas TEXT
        )
    """)
    
    # Create usuarios table
    print("✓ Creating usuarios table...")
    cursor.execute("""
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
    """)
    
    # Check what we have
    cursor.execute("SELECT COUNT(*) FROM secciones_produccion")
    sec_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    user_count = cursor.fetchone()[0]
    
    print(f"Current database state:")
    print(f"  Secciones: {sec_count}")
    print(f"  Usuarios: {user_count}")
    
    # Seed secciones if empty
    if sec_count == 0:
        print("✓ Seeding 16 production sections...")
        sections_data = [
            (1, "SEC-ENS-01", "Ensamblaje Línea 1", "Línea de ensamblaje", "ensamblaje", 100.0, 3, "Jefe Ensamblaje 1", 1, "Nave A - Línea 1"),
            (1, "SEC-ENS-02", "Ensamblaje Línea 2", "Línea de ensamblaje", "ensamblaje", 100.0, 4, "Jefe Ensamblaje 2", 1, "Nave A - Línea 2"),
            (1, "SEC-ENS-03", "Ensamblaje Línea 3", "Línea de ensamblaje", "ensamblaje", 100.0, 5, "Jefe Ensamblaje 3", 1, "Nave A - Línea 3"),
            (1, "SEC-ENS-04", "Ensamblaje Línea 4", "Línea de ensamblaje", "ensamblaje", 100.0, 6, "Jefe Ensamblaje 4", 1, "Nave A - Línea 4"),
            (1, "SEC-ENS-05", "Ensamblaje Línea 5", "Línea de ensamblaje", "ensamblaje", 100.0, 7, "Jefe Ensamblaje 5", 1, "Nave A - Línea 5"),
            (1, "SEC-ENS-06", "Ensamblaje Línea 6", "Línea de ensamblaje", "ensamblaje", 100.0, 5, "Jefe Ensamblaje 6", 1, "Nave A - Línea 6"),
            (1, "SEC-ENS-07", "Ensamblaje Línea 7", "Línea de ensamblaje", "ensamblaje", 100.0, 4, "Jefe Ensamblaje 7", 1, "Nave A - Línea 7"),
            (1, "SEC-PIN-01", "Pintura Cabina 1", "Cabina de pintura", "pintura", 80.0, 4, "Jefe Pintura 1", 1, "Nave B - Cabina 1"),
            (1, "SEC-PIN-02", "Pintura Cabina 2", "Cabina de pintura", "pintura", 80.0, 4, "Jefe Pintura 2", 1, "Nave B - Cabina 2"),
            (1, "SEC-PIN-03", "Pintura Cabina 3", "Cabina de pintura", "pintura", 80.0, 4, "Jefe Pintura 3", 1, "Nave B - Cabina 3"),
            (1, "SEC-MEC-01", "Mecanizado Celda 1", "Mecanizado CNC", "mecanizado", 60.0, 5, "Jefe Mecanizado 1", 1, "Nave C - Celda 1"),
            (1, "SEC-MEC-02", "Mecanizado Celda 2", "Mecanizado CNC", "mecanizado", 60.0, 5, "Jefe Mecanizado 2", 1, "Nave C - Celda 2"),
            (1, "SEC-MEC-03", "Mecanizado Celda 3", "Mecanizado CNC", "mecanizado", 60.0, 5, "Jefe Mecanizado 3", 1, "Nave C - Celda 3"),
            (1, "SEC-EMB-01", "Embalaje Mesa 1", "Mesa de embalaje", "empaque", 120.0, 3, "Jefe Embalaje 1", 1, "Nave D - Mesa 1"),
            (1, "SEC-EMB-02", "Embalaje Mesa 2", "Mesa de embalaje", "empaque", 120.0, 3, "Jefe Embalaje 2", 1, "Nave D - Mesa 2"),
            (1, "SEC-EMB-03", "Embalaje Mesa 3", "Mesa de embalaje", "empaque", 120.0, 3, "Jefe Embalaje 3", 1, "Nave D - Mesa 3"),
        ]
        
        cursor.executemany("""
            INSERT INTO secciones_produccion 
            (organization_id, codigo, nombre, descripcion, tipo, capacidad_diaria, capacidad_operarios, supervisor_nombre, activa, ubicacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sections_data)
        conn.commit()
        print(f"  ✓ {len(sections_data)} sections created")
    
    # Seed usuarios if empty
    if user_count == 0:
        print("✓ Creating 87 production workers...")
        pwd_hash = bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode()
        
        # Create supervisores
        supervisores = [
            (1, "supervisor_ens_1", "supervisor1@empresa.com", "Supervisor Ensamblaje 1", "Juan", "García", pwd_hash),
            (1, "supervisor_ens_2", "supervisor2@empresa.com", "Supervisor Ensamblaje 2", "Carlos", "López", pwd_hash),
            (1, "supervisor_ens_3", "supervisor3@empresa.com", "Supervisor Ensamblaje 3", "María", "Rodríguez", pwd_hash),
            (1, "supervisor_ens_4", "supervisor4@empresa.com", "Supervisor Ensamblaje 4", "José", "Martínez", pwd_hash),
            (1, "supervisor_ens_5", "supervisor5@empresa.com", "Supervisor Ensamblaje 5", "Antonio", "Sánchez", pwd_hash),
            (1, "supervisor_ens_6", "supervisor6@empresa.com", "Supervisor Ensamblaje 6", "Francisco", "Pérez", pwd_hash),
            (1, "supervisor_ens_7", "supervisor7@empresa.com", "Supervisor Ensamblaje 7", "Pedro", "González", pwd_hash),
            (1, "supervisor_pin_1", "supervisor8@empresa.com", "Supervisor Pintura 1", "Luis", "Fernández", pwd_hash),
            (1, "supervisor_pin_2", "supervisor9@empresa.com", "Supervisor Pintura 2", "Miguel", "Díaz", pwd_hash),
            (1, "supervisor_pin_3", "supervisor10@empresa.com", "Supervisor Pintura 3", "Roberto", "Cruz", pwd_hash),
            (1, "supervisor_mec_1", "supervisor11@empresa.com", "Supervisor Mecanizado 1", "Javier", "Moreno", pwd_hash),
            (1, "supervisor_mec_2", "supervisor12@empresa.com", "Supervisor Mecanizado 2", "Andrés", "Ruiz", pwd_hash),
            (1, "supervisor_mec_3", "supervisor13@empresa.com", "Supervisor Mecanizado 3", "David", "Vargas", pwd_hash),
            (1, "supervisor_emb_1", "supervisor14@empresa.com", "Supervisor Embalaje 1", "Alfredo", "Salas", pwd_hash),
            (1, "supervisor_emb_2", "supervisor15@empresa.com", "Supervisor Embalaje 2", "Raúl", "Torres", pwd_hash),
            (1, "supervisor_emb_3", "supervisor16@empresa.com", "Supervisor Embalaje 3", "Eduardo", "Flores", pwd_hash),
        ]
        
        # Create operarios
        operarios = [(1, f"operario_{i:02d}", f"operario{i}@empresa.com", f"Operario {i}", f"Nombre{i}", f"Apellido{i}", pwd_hash) for i in range(1, 71)]
        
        all_users = supervisores + operarios
        
        cursor.executemany("""
            INSERT INTO usuarios 
            (organization_id, username, email, nombre_completo, nombre, apellidos, hashed_password)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, all_users)
        conn.commit()
        print(f"  ✓ {len(supervisores)} supervisores created")
        print(f"  ✓ {len(operarios)} operarios created")
    
    conn.commit()
    print("✓ Database setup complete!")

finally:
    conn.close()
