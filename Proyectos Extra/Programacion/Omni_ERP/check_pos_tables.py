import asyncio
import aiosqlite
from pathlib import Path

DB_PATH = Path("src/data/org_dbs/org_1.db")

async def check_pos_tables():
    if not DB_PATH.exists():
        print(f"Database {DB_PATH} not found.")
        return

    print(f"Connecting to {DB_PATH}...")
    async with aiosqlite.connect(DB_PATH) as db:
        # Check ventas_pos table
        try:
            cursor = await db.execute("PRAGMA table_info(ventas_pos)")
            columns = await cursor.fetchall()
            if not columns:
                print("Table 'ventas_pos' DOES NOT EXIST.")
            else:
                print("Table 'ventas_pos' exists. Columns:")
                for col in columns:
                    print(f"  - {col[1]} ({col[2]})")
        except Exception as e:
            print(f"Error checking ventas_pos: {e}")

        # Check organizations table
        try:
            cursor = await db.execute("PRAGMA table_info(organizations)")
            columns = await cursor.fetchall()
            if not columns:
                print("Table 'organizations' DOES NOT EXIST.")
            else:
                print("Table 'organizations' exists. Columns:")
                for col in columns:
                    print(f"  - {col[1]} ({col[2]})")
        except Exception as e:
            print(f"Error checking organizations: {e}")

if __name__ == "__main__":
    asyncio.run(check_pos_tables())
