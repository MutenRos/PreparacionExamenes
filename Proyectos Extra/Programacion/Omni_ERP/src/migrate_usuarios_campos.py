#!/usr/bin/env python3
"""Migration script to add email_personal and telefono columns to usuarios table."""
import asyncio
import sys

sys.path.insert(0, "/home/dario/src")


async def main():
    from sqlalchemy import text
    from dario_app.database import get_tenant_engine

    try:
        engine = get_tenant_engine(1)

        async with engine.begin() as conn:
            # Try to add email_personal column
            try:
                await conn.execute(text("""
                    ALTER TABLE usuarios
                    ADD COLUMN email_personal VARCHAR(100) NULLABLE DEFAULT NULL
                """))
                print("✓ Added email_personal column")
            except Exception as e:
                print(f"ℹ email_personal column might already exist: {str(e)[:100]}")

            # Try to add telefono column
            try:
                await conn.execute(text("""
                    ALTER TABLE usuarios
                    ADD COLUMN telefono VARCHAR(20) NULLABLE DEFAULT NULL
                """))
                print("✓ Added telefono column")
            except Exception as e:
                print(f"ℹ telefono column might already exist: {str(e)[:100]}")

        print("\n✅ Migration completed!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
