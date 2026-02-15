import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from dario_app.database import create_tenant_db

async def update_tenant_db():
    print("Updating tenant DB schema...")
    try:
        # Force update of tenant 1
        await create_tenant_db(1)
        print("Tenant DB updated successfully.")
    except Exception as e:
        print(f"Update failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(update_tenant_db())