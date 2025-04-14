from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID
from ..config.db_config import get_db
from ..models.user_models import User
from ..models.feedback_models import UserFeedback 
from ..schemas.feedback_schemas import UserFeedbackCreate, UserFeedbackSchema  
from ..services.auth_service import get_current_user, get_current_admin 
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/", response_model=UserFeedbackSchema, status_code=status.HTTP_201_CREATED)
async def submit_feedback(
    feedback: UserFeedbackCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Submit user feedback.
    """
    if not current_user or not hasattr(current_user, "id"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    logger.info(f"Submitting feedback for user: {current_user.id}")

    try:
        new_feedback = UserFeedback(
            user_id=current_user.id,
            rating=feedback.rating,
            feedback_text=feedback.feedback_text if feedback.feedback_text else "",  
            timestamp=datetime.utcnow()
        )

        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)

        return UserFeedbackSchema.from_orm(new_feedback)
    
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")



@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_feedbacks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  
):
    """
    Retrieve all user feedback (Accessible to admins or authenticated users).
    """
    if not current_user or not hasattr(current_user, "id"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    logger.info("Fetching all feedbacks...")

    try:
        # Fetch distinct feedbacks by grouping on UserFeedback.id
        feedbacks = (
            db.query(
                UserFeedback.id,
                UserFeedback.feedback_text,
                UserFeedback.rating,
                UserFeedback.timestamp,
                User.name.label("user_name"), 
            )
            .join(User, UserFeedback.user_id == User.id)  
            .filter(UserFeedback.id.isnot(None))
            .order_by(UserFeedback.timestamp.desc())  
            .all()
        )




        if not feedbacks:
            return []

        feedback_list = [
            {
                "id": fb.id,
                "user_name": fb.user_name,  
                "feedback_text": fb.feedback_text,
                "rating": fb.rating,
                "timestamp": fb.timestamp
            }
            for fb in feedbacks
        ]

        return feedback_list

    except Exception as e:
        logger.error(f"Error retrieving feedbacks: {str(e)}", exc_info=True)  
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve feedbacks")



@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_feedbacks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Only authenticated users can retrieve their own feedback
):
    """
    Retrieve the feedback submitted by the authenticated user.
    """
    if not current_user or not hasattr(current_user, "id"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    logger.info(f"Fetching feedback for user: {current_user.id}")

    try:
        # Query feedback filtered by the current user's ID
        feedbacks = (
            db.query(UserFeedback)
            .filter(UserFeedback.user_id == current_user.id)  
            .order_by(UserFeedback.timestamp.desc())
            .all()
        )

        if not feedbacks:
            return []

        feedback_list = [
            {
                "id": fb.id,
                "feedback_text": fb.feedback_text,
                "rating": fb.rating,
                "timestamp": fb.timestamp
            }
            for fb in feedbacks
        ]

        return feedback_list

    except Exception as e:
        logger.error(f"Error retrieving feedbacks: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve feedbacks")



@router.delete("/{feedback_id}", status_code=status.HTTP_200_OK)
async def delete_feedback(
    feedback_id: UUID,  # Use UUID type for the ID
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  
):
    """
    Delete a feedback entry by ID (User or Admin).
    """
    logger.info(f"User {current_user.id} deleting feedback: {feedback_id}")

    try:
        feedback = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()

        if not feedback:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
        
        # Ensure the feedback belongs to the current user
        if feedback.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own feedback")

        db.delete(feedback)
        db.commit()
        
        return {
            "success": True,
            "message": "Feedback deleted successfully"
        }

    except Exception as e:
        logger.error(f"Error deleting feedback: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete feedback")
