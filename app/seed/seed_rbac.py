# app/seeds/seed_rbac.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Role, Permission 


ROLES = [
    {"name": "HR", "description": "Human Resources administrator"},
    {"name": "MANAGER", "description": "Manages employees and team"},
    {"name": "EMPLOYEE", "description": "Regular employee"},
]


PERMISSIONS = [
    # Employee
    {"name": "employee:create", "description": "Create employee"},
    {"name": "employee:read", "description": "View employee"},
    {"name": "employee:update", "description": "Update employee"},
    {"name": "employee:delete", "description": "Delete employee"},
    # Profile
    {"name": "profile:read", "description": "View own profile"},
    {"name": "profile:update", "description": "Update own profile"},
    # Leave
    {"name": "leave:create", "description": "Create leave request"},
    {"name": "leave:read", "description": "View leave requests"},
    {"name": "leave:approve", "description": "Approve leave request"},
    {"name": "leave:reject", "description": "Reject leave request"},
    {"name": "leave:cancel", "description": "Cancel leave request"},
    # Department
    {"name": "department:create", "description": "Create department"},
    {"name": "department:read", "description": "View departments"},
    {"name": "department:update", "description": "Update department"},
    {"name": "department:delete", "description": "Delete department"},
]


ROLE_PERMISSIONS = {
    "HR": [
        "employee:create",
        "employee:read",
        "employee:update",
        "employee:delete",
        "department:create",
        "department:read",
        "department:update",
        "department:delete",
        "leave:read",
        "leave:approve",
        "leave:reject",
        "profile:read",
        "profile:update",
    ],
    "MANAGER": [
        "employee:read",
        "department:read",
        "leave:read",
        "leave:approve",
        "leave:reject",
        "profile:read",
        "profile:update",
    ],
    "EMPLOYEE": [
        "profile:read",
        "profile:update",
        "leave:create",
        "leave:read",
        "leave:cancel",
    ],
}


async def seed_rbac(db: AsyncSession):

    # =========================
    # 1. CREATE ROLES
    # =========================

    for role_data in ROLES:

        result = await db.execute(select(Role).where(Role.name == role_data["name"]))

        role = result.scalar_one_or_none()

        if not role:
            role = Role(name=role_data["name"], description=role_data["description"])

            db.add(role)

    await db.commit()

    # =========================
    # 2. CREATE PERMISSIONS
    # =========================

    for permission_data in PERMISSIONS:

        result = await db.execute(
            select(Permission).where(Permission.name == permission_data["name"])
        )

        permission = result.scalar_one_or_none()

        if not permission:

            permission = Permission(
                name=permission_data["name"], description=permission_data["description"]
            )

            db.add(permission)

    await db.commit()

    from sqlalchemy.orm import selectinload

    # =========================
    # 3. GET ALL ROLES
    # =========================

    roles_result = await db.execute(select(Role).options(selectinload(Role.permissions)))

    roles = {role.name: role for role in roles_result.scalars().all()}

    # =========================
    # 4. GET ALL PERMISSIONS
    # =========================

    permissions_result = await db.execute(select(Permission))

    permissions = {
        permission.name: permission for permission in permissions_result.scalars().all()
    }

    # =========================
    # 5. ASSIGN PERMISSIONS
    # =========================

    for role_name, permission_names in ROLE_PERMISSIONS.items():

        role = roles.get(role_name)

        if not role:
            continue

        for permission_name in permission_names:

            permission = permissions.get(permission_name)

            if permission and permission not in role.permissions:

                role.permissions.append(permission)

    await db.commit()

    print("RBAC seed completed successfully!")
