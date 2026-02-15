#!/usr/bin/env python3
"""Initialize POS Widget tables."""

import asyncio
import sys
sys.path.insert(0, '/home/dario/src')

async def init_widget_tables():
    from dario_app.database import init_db
    
    try:
        await init_db()
        print("✅ Tablas de POS Widget inicializadas correctamente")
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_widget_tables())
