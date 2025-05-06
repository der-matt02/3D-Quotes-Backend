from models.user_model import User
from schemas.admin_schemas import AdminCreateSchema
from utils.hashing import hash_password
from typing import List
from schemas.admin_schemas import AdminUpdateSchema
from typing import Optional
from models.user_model import AdminMetadata


async def create_admin(data: AdminCreateSchema, created_by_superadmin: User) -> User:
    existing = await User.find_one({"$or": [{"email": data.email}, {"username": data.username}]})
    if existing:
        raise ValueError("Admin with that email or username already exists")

    admin = User(
        username=data.username,
        email=data.email,
        password=hash_password(data.password),
        role="admin",
        is_active=True,
        admin_metadata={"created_by": str(created_by_superadmin.id), "notes": "Created via admin panel"}
    )

    await admin.insert()
    return admin

async def list_admins() -> List[User]:
    return await User.find({"role": "admin"}).to_list()

async def update_admin(admin_id: str, data: AdminUpdateSchema) -> Optional[User]:
    admin = await User.get(admin_id)
    if not admin or admin.role != "admin":
        return None

    if data.username is not None:
        admin.username = data.username
    if data.email is not None:
        admin.email = data.email
    if data.is_active is not None:
        admin.is_active = data.is_active
    if data.notes is not None:
        if not admin.admin_metadata:
            admin.admin_metadata = AdminMetadata()
        admin.admin_metadata.notes = data.notes

    await admin.save()
    return admin

async def delete_admin(admin_id: str) -> bool:
    admin = await User.get(admin_id)
    if not admin or admin.role != "admin":
        return False

    await admin.delete()
    return True
