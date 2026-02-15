#!/usr/bin/env python3
"""Simple migration runner."""
import asyncio
import os
import sys

# Ensure we're in the correct directory
os.chdir("/home/dario/src")
sys.path.insert(0, "/home/dario/src")


async def main():
    try:
        from dario_app.database import init_db

        print("Inicializando base de datos...")
        await init_db()
        print("✅ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
