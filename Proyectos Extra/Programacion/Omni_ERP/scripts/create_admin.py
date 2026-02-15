"""Create initial super admin account."""

import asyncio

import bcrypt
from sqlalchemy import select

from dario_app.database import master_session_maker, init_db
from dario_app.modules.tenants.models import Organization
from dario_app.modules.usuarios.models import Usuario


async def create_admin():
    """Create super admin organization and user."""
    await init_db()

    async with master_session_maker() as session:
        # Check if admin org exists
        result = await session.execute(
            select(Organization).where(Organization.slug == "admin-system")
        )
        org = result.scalar_one_or_none()

        if not org:
            # Create admin organization
            org = Organization(
                nombre="Sistema Admin",
                slug="admin-system",
                email="admin@omnisolutions",
                plan="enterprise",
                max_usuarios=999,
                max_productos=999999,
                max_sucursales=999,
                activo=True,
            )
            session.add(org)
            await session.flush()
            print(f"✅ Organización admin creada: {org.nombre}")

        # Check if admin user exists
        result = await session.execute(select(Usuario).where(Usuario.email == "admin@omnisolutions"))
        user = result.scalar_one_or_none()

        if not user:
            # Create super admin user
            password = "admin123".encode("utf-8")
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
            user = Usuario(
                organization_id=org.id,
                username="admin",
                email="admin@omnisolutions",
                hashed_password=hashed_password,
                nombre_completo="Super Admin",
                es_admin=True,
                activo=True,
            )
            session.add(user)
            await session.commit()
            print(f"✅ Usuario admin creado: {user.email}")
            print("   Email: admin@omnisolutions")
            print("   Password: admin123")
            print("   ⚠️  CAMBIAR CONTRASEÑA después del primer login!")
        else:
            print(f"ℹ️  Usuario admin ya existe: {user.email}")
            print("   Si olvidaste la contraseña, resetea con: admin123")
            # Update password anyway
            password = "admin123".encode("utf-8")
            user.hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
            await session.commit()


if __name__ == "__main__":
    asyncio.run(create_admin())
