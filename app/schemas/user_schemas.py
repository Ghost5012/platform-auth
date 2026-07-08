from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    # is_active: Optional[bool] = True
    # is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDB(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_superuser: bool
    role: Optional[str] = None

    class Config:
        from_attributes = True