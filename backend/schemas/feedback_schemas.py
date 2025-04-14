from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

# ----------------- User Feedback -----------------
class UserFeedbackBase(BaseModel):
    """Base schema for user feedback"""
    rating: float = Field(..., ge=1.0, le=5.0, description="Rating must be between 1 and 5")
    feedback_text: Optional[str] = Field(default=None, max_length=2500)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True  


class UserFeedbackCreate(UserFeedbackBase):
    """Schema for creating user feedback"""
    pass


class UserFeedbackSchema(UserFeedbackBase):
    """Schema for retrieving user feedback"""
    id: UUID  # UUID instead of int
    user_id: UUID  # UUID instead of str

    class Config:
        from_attributes = True  # Ensure compatibility with ORM objects
