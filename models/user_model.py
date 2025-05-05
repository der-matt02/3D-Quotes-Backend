from beanie import Document
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Literal


class LoginMetadata(BaseModel):
    last_login: Optional[datetime]
    ip_address: Optional[str]
    failed_attempts: int = 0

class AdminMetadata(BaseModel):
    created_by: Optional[str]
    notes: Optional[str]


class User(Document):
    username: str = Field(..., unique=True)
    email: EmailStr = Field(..., unique=True)
    password: str
    role: Literal["user", "admin", "superadmin"] = "user"
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    remember_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    login_metadata: Optional[LoginMetadata] = None
    admin_metadata: Optional[AdminMetadata] = None

    class Settings:
        name = "users"  # nombre de la colección
