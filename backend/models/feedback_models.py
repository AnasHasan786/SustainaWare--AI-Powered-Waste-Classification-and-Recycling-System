import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Text, DateTime, CheckConstraint, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class UserFeedback(Base):
    __tablename__ = 'user_feedback'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Use UUID
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    rating = Column(Float, nullable=False)  # Changed from Integer to Float
    feedback_text = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', backref="feedbacks", lazy='joined')

    __table_args__ = (CheckConstraint('rating >= 1.0 AND rating <= 5.0', name='valid_rating_range'),)

    def __repr__(self) -> str:
        return f"<UserFeedback(user_id={self.user_id}, rating={self.rating})>"
