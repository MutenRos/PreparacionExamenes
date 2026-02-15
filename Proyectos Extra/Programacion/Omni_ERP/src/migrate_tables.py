#!/usr/bin/env python3
"""Quick database migration script."""
import asyncio
import sys

sys.path.insert(0, "/home/dario/src")


async def main():
    from dario_app.database import get_async_engine

    try:
        engine = get_async_engine()

        # Create all tables from models
        from dario_app.modules.documentos.models import Base as DocumentosBase

        async with engine.begin() as conn:
            # Create tables
            await conn.run_sync(DocumentosBase.metadata.create_all)

        print("✅ Tabla DocumentoManual creada exitosamente")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
