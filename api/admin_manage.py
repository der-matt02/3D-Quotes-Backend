from fastapi import APIRouter, Depends, HTTPException, status
from schemas.admin_schemas import AdminCreateSchema, AdminOutSchema
from services.admin_service import create_admin
from dependencies.auth import get_current_user
from models.user_model import User
from schemas.admin_schemas import AdminListSchema
from services.admin_service import list_admins
from typing import List
from schemas.admin_schemas import AdminUpdateSchema
from services.admin_service import update_admin
from services.admin_service import delete_admin
from fastapi import Response

router = APIRouter(prefix="/admin", tags=["Admin Management"])

@router.post("/create", response_model=AdminOutSchema)
async def superadmin_create_admin(
    data: AdminCreateSchema,
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "superadmin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only superadmins can create admins")

    try:
        admin = await create_admin(data, created_by_superadmin=current_user)
        return AdminOutSchema(
            id=str(admin.id),
            username=admin.username,
            email=admin.email,
            role=admin.role
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list", response_model=List[AdminListSchema])
async def get_all_admins(current_user: User = Depends(get_current_user)):
    if current_user.role != "superadmin":
        raise HTTPException(status_code=403, detail="Only superadmins can view admins")

    admins = await list_admins()
    return [
        AdminListSchema(
            id=str(admin.id),
            username=admin.username,
            email=admin.email,
            role=admin.role,
            is_active=admin.is_active
        ) for admin in admins
    ]

@router.put("/update/{admin_id}", response_model=AdminOutSchema)
async def update_admin_data(
    admin_id: str,
    data: AdminUpdateSchema,
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "superadmin":
        raise HTTPException(status_code=403, detail="Only superadmins can update admins")

    updated = await update_admin(admin_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Admin not found")

    return AdminOutSchema(
        id=str(updated.id),
        username=updated.username,
        email=updated.email,
        role=updated.role
    )

@router.delete("/delete/{admin_id}", status_code=204)
async def delete_admin_account(
    admin_id: str,
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "superadmin":
        raise HTTPException(status_code=403, detail="Only superadmins can delete admins")

    success = await delete_admin(admin_id)
    if not success:
        raise HTTPException(status_code=404, detail="Admin not found or cannot be deleted")

    return Response(status_code=204)

