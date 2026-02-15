from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from dario_app.modules.usuarios.models import Permission, Role, RolePermission
from dario_app.modules.usuarios.permissions_data import PERMISSIONS_BY_CATEGORY, DEFAULT_ROLES

async def seed_tenant_permissions(db: AsyncSession, org_id: int):
    """
    Seeds the database with default permissions and roles for a tenant.
    Idempotent: can be run multiple times without duplicating data.
    """
    print(f"[PERMISSIONS] Seeding permissions for Org {org_id}...")
    
    # 1. Sync Permissions
    all_permissions_map = {}  # code -> Permission object
    
    for category, perms in PERMISSIONS_BY_CATEGORY.items():
        for p_data in perms:
            code = p_data["code"]
            
            # Check if exists
            result = await db.execute(select(Permission).where(Permission.codigo == code))
            existing_perm = result.scalar_one_or_none()
            
            if not existing_perm:
                new_perm = Permission(
                    codigo=code,
                    nombre=p_data["name"],
                    descripcion=p_data["desc"],
                    # categoria=category  # Temporarily removed to fix schema mismatch
                )
                db.add(new_perm)
                await db.flush()
                all_permissions_map[code] = new_perm
            else:
                # Update category if missing or changed (optional, but good for maintenance)
                if existing_perm.categoria != category:
                    existing_perm.categoria = category
                all_permissions_map[code] = existing_perm
    
    # 2. Sync Roles
    for role_name, role_data in DEFAULT_ROLES.items():
        # Check if role exists
        result = await db.execute(
            select(Role).where(Role.organization_id == org_id, Role.nombre == role_name)
        )
        role = result.scalar_one_or_none()
        
        if not role:
            role = Role(
                organization_id=org_id,
                nombre=role_name,
                descripcion=role_data["description"],
                es_sistema=True  # Mark as system role so it's not easily deleted
            )
            db.add(role)
            await db.flush()
        
        # 3. Assign Permissions to Role
        target_perms = role_data["permissions"]
        
        perms_to_assign = []
        if "*" in target_perms:
            # Assign ALL permissions
            perms_to_assign = list(all_permissions_map.values())
        else:
            for code in target_perms:
                if code in all_permissions_map:
                    perms_to_assign.append(all_permissions_map[code])
        
        # Get current permissions for this role
        current_role_perms_result = await db.execute(
            select(RolePermission).where(RolePermission.role_id == role.id)
        )
        current_role_perms = current_role_perms_result.scalars().all()
        current_perm_ids = {rp.permission_id for rp in current_role_perms}
        
        for perm in perms_to_assign:
            if perm.id not in current_perm_ids:
                rp = RolePermission(role_id=role.id, permission_id=perm.id)
                db.add(rp)
                
    await db.commit()
    print(f"[PERMISSIONS] Seeding complete for Org {org_id}.")
