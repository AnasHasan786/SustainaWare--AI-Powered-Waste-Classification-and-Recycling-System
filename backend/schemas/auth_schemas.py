from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from uuid import UUID

# ----------------- User Authentication Schemas -----------------
class UserBase(BaseModel):
    """Base schema for user-related data"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=6, max_length=128)

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)

class User(BaseModel):
    """Schema for retrieving user data"""
    id: UUID
    name: str
    email: EmailStr
    created_at: datetime
    is_verified: bool
    is_admin: bool  

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    is_verified: bool
    is_admin: bool

    class Config:
        orm_mode = True


# ----------------- Token Schemas -----------------
class TokenData(BaseModel):
    """Schema for storing token-related data"""
    user_id: UUID
    email: EmailStr
    is_admin: bool

class TokenResponse(BaseModel):
    """Schema for token response data"""
    access_token: str
    token_type: Literal["bearer"] = "bearer"

# ----------------- Email Verification & Password Reset -----------------
class VerifyEmail(BaseModel):
    """Schema for verifying email"""
    token: str

class ForgotPasswordRequest(BaseModel):
    """Schema for requesting a password reset"""
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    """Schema for resetting the password"""
    token: str
    new_password: str = Field(..., min_length=6, max_length=128)

class VerifyCodeRequest(BaseModel):
    """Schema for verifying a code (e.g., OTP)"""
    code: str

# ----------------- Google Authentication -----------------
class GoogleAuthRequest(BaseModel):
    """Schema for Google OAuth authentication"""
    token: str