from fastapi import APIRouter, HTTPException
from schemas.user_schemas import UserRegisterSchema, UserOutSchema
from schemas.login_schemas import UserLoginSchema, TokenResponse
from services.auth_service import register_user
from services.auth_service import login_user as login_user_service
from schemas.login_schemas import AdminLoginSchema, TokenResponse
from services.auth_service import login_admin
from schemas.login_schemas import SuperAdminLoginSchema
from services.auth_service import login_superadmin
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

@router.post("/user/login", response_model=TokenResponse)
async def login_user(data: UserLoginSchema):
    try:
        token = await login_user_service(data)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/admin/login", response_model=TokenResponse)
async def admin_login(data: AdminLoginSchema):
    try:
        token = await login_admin(data)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/superadmin/login", response_model=TokenResponse)
async def superadmin_login(data: SuperAdminLoginSchema):
    try:
        token = await login_superadmin(data)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))