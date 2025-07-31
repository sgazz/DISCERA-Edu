"""
User schemas for DISCERA API
"""
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.STUDENT


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """Schema for user in database"""
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class User(UserInDB):
    """Schema for user response"""
    pass


class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token data"""
    user_id: Optional[int] = None 