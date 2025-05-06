from pydantic import BaseModel

class UserLoginSchema(BaseModel):
    username_or_email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AdminLoginSchema(BaseModel):
    username_or_email: str
    password: str

class SuperAdminLoginSchema(BaseModel):
    username_or_email: str
    password: str
