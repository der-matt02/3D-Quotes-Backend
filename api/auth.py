from fastapi import APIRouter, HTTPException
from schemas.user_schemas import UserRegisterSchema, UserOutSchema
from services.auth_service import register_user

router = APIRouter()

@router.post("/register", response_model=UserOutSchema)
async def register(data: UserRegisterSchema):
    try:
        user = await register_user(data)
        return UserOutSchema(
            id=str(user.id),
            username=user.username,
            email=user.email,
            role=user.role
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
