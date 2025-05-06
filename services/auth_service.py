from models.user_model import User
from schemas.user_schemas import UserRegisterSchema
from schemas.login_schemas import UserLoginSchema
from utils.hashing import hash_password, verify_password
from utils.jwt import create_access_token
from schemas.login_schemas import AdminLoginSchema
from schemas.login_schemas import SuperAdminLoginSchema

# Registro
async def register_user(data: UserRegisterSchema):
    if data.password != data.confirm_password:
        raise ValueError("Las contraseñas no coinciden")

    existing_user = await User.find_one(
        {"$or": [{"username": data.username}, {"email": data.email}]}
    )
    if existing_user:
        raise ValueError("El usuario o email ya existen")

    hashed_pw = hash_password(data.password)

    user = User(
        username=data.username,
        email=data.email,
        password=hashed_pw,
        role="user"
    )

    await user.insert()
    return user

# Login
async def login_user(data: UserLoginSchema):
    user = await User.find_one({
        "$or": [{"username": data.username_or_email}, {"email": data.username_or_email}]
    })

    if not user:
        raise ValueError("Usuario no encontrado")

    if not verify_password(data.password, user.password):
        raise ValueError("Contraseña incorrecta")

    if user.role != "user":
        raise ValueError("Acceso no autorizado para este login")

    token_data = {"sub": str(user.id), "role": user.role}
    token = create_access_token(token_data)

    return token

async def login_admin(data: AdminLoginSchema):
    user = await User.find_one({
        "$or": [{"username": data.username_or_email}, {"email": data.username_or_email}]
    })

    if not user:
        raise ValueError("Admin not found")

    if not verify_password(data.password, user.password):
        raise ValueError("Incorrect password")

    if user.role != "admin":
        raise ValueError("Access denied: not an admin")

    token_data = {"sub": str(user.id), "role": user.role}
    return create_access_token(token_data)

async def login_superadmin(data: SuperAdminLoginSchema):
    user = await User.find_one({
        "$or": [{"username": data.username_or_email}, {"email": data.username_or_email}]
    })

    if not user:
        raise ValueError("Superadmin not found")

    if not verify_password(data.password, user.password):
        raise ValueError("Incorrect password")

    if user.role != "superadmin":
        raise ValueError("Access denied: not a superadmin")

    token_data = {"sub": str(user.id), "role": user.role}
    return create_access_token(token_data)