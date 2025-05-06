from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class AdminCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class AdminOutSchema(BaseModel):
    id: str
    username: str
    email: str
    role: str

class AdminListSchema(BaseModel):
    id: str
    username: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True  # Para Pydantic v2



class AdminUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None
