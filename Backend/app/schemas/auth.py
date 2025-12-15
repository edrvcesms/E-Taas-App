from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class AdminRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: bool = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class VerifyEmailOTP(BaseModel):
    username: str
    email: EmailStr
    password: str
    otp: str