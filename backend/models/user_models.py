import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class User(Base):
    """
    User model representing users in the system.
    Stores basic user details and authentication-related fields.
    """
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)  
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255), nullable=True, unique=True)  
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}, email={self.email}, is_admin={self.is_admin})>"

    def is_admin_user(self) -> bool:
        """Check if the user has admin privileges."""
        return self.is_admin

    def is_verified_user(self) -> bool:
        """Check if the user's email is verified."""
        return self.is_verified

    class Config:
        orm_mode = True
