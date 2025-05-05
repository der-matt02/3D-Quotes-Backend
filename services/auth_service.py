from models.user_model import User
from schemas.user_schemas import UserRegisterSchema
from utils.hashing import hash_password

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
