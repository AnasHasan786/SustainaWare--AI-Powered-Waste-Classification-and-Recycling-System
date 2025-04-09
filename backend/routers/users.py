from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from ..config.db_config import get_db
from ..models.user_models import User
from ..schemas.auth_schemas import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Retrieve all users."""
    users = db.query(User).all()
    return users

@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    """Delete a user by their ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
