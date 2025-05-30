from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class user(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    is_admin: Optional[bool] = False  # По умолчанию False

class user_login(BaseModel):
    email: str
    password: str

class user_response(BaseModel):
    first_name: str
    last_name: str
    email: str
    role: str

    class Config:
        from_attributes = True