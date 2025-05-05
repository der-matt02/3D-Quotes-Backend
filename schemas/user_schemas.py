from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

class UserOutSchema(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True
