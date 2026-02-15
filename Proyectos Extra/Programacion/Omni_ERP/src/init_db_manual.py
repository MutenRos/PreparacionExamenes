#!/usr/bin/env python3
"""Initialize database with new tables (DocumentoManual)."""
import asyncio
import sys

# Add src to path
sys.path.insert(0, "/home/dario/src")

from dario_app.database import init_db


async def main():
    """Initialize database."""
    try:
        print("Inicializando base de datos con nuevas tablas...")
        await init_db()
        print("✅ Base de datos inicializada exitosamente")
        print("✅ Tabla DocumentoManual creada")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
